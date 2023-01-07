import asyncio
from ctypes import c_uint8

from ble_api.BleCommon import BLE_ERROR, BleEventBase, BLE_OWN_ADDR_TYPE, BLE_ADDR_TYPE
from ble_api.BleGap import BLE_GAP_ROLE, BLE_GAP_CONN_MODE, BLE_GAP_PHY, BleEventGapConnected, \
    BleEventGapAdvCompleted, BLE_CONN_IDX_INVALID
from gtl_messages.gtl_message_gapc import GapcConnectionCfm, GapcConnectionReqInd, GapcGetDevInfoReqInd, GapcGetDevInfoCfm
from gtl_messages.gtl_message_gapm import GapmSetDevConfigCmd, GapmStartAdvertiseCmd, GapmCmpEvt
from gtl_port.gap import GAP_ROLE, GAP_AUTH_MASK
from gtl_port.gapc import GAPC_FIELDS_MASK
from gtl_port.gapc_task import GAPC_MSG_ID, GAPC_DEV_INFO
from gtl_port.gapm_task import GAPM_MSG_ID, GAPM_OPERATION, GAPM_ADDR_TYPE, GAPM_OWN_ADDR
from gtl_port.rwble_hl_error import HOST_STACK_ERROR_CODE
from manager.BleDevParams import BleDevParamsDefault
from manager.BleManagerCommon import BleManagerBase
from manager.BleManagerCommonMsgs import BleMgrMsgBase
from manager.BleManagerGapMsgs import BLE_CMD_GAP_OPCODE, BleMgrGapRoleSetRsp, BleMgrGapAdvStartCmd, BleMgrGapAdvStartRsp, BleMgrGapRoleSetCmd
from manager.BleManagerStorage import StoredDeviceQueue
from manager.GtlWaitQueue import GtlWaitQueue


# TODO this is from ble_config.h
dg_configBLE_DATA_LENGTH_TX_MAX = (251)

# TODO this is from stack
ATT_DEFAULT_MTU = (23)


class BleManagerGap(BleManagerBase):

    def __init__(self,
                 mgr_response_q: asyncio.Queue[BLE_ERROR],
                 mgr_event_q: asyncio.Queue[BleEventBase],
                 adapter_command_q: asyncio.Queue[BleMgrMsgBase],
                 wait_q: GtlWaitQueue,
                 stored_device_q: StoredDeviceQueue) -> None:

        super().__init__(mgr_response_q, mgr_event_q, adapter_command_q, wait_q, stored_device_q)

        # TODO dev_params passed to base class?
        self.dev_params = BleDevParamsDefault()

        self.cmd_handlers = {
            BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ROLE_SET_CMD: self.role_set_cmd_handler,
            BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ADV_START_CMD: self.adv_start_cmd_handler,
            # BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ADV_STOP_CMD: self.gap_adv_stop_cmd_handler,
            # BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_CONNECT_CMD: self.connect_cmd_handler,
        }

        # TODO separate gapm and gapc?
        self.evt_handlers = {
            GAPM_MSG_ID.GAPM_CMP_EVT: self.cmp_evt_handler,
            GAPC_MSG_ID.GAPC_CONNECTION_REQ_IND: self.connected_evt_handler,
            GAPC_MSG_ID.GAPC_GET_DEV_INFO_REQ_IND: self.get_device_info_req_evt_handler,
            GAPC_MSG_ID.GAPC_LECB_DISCONNECT_IND: self.disconnected_evt_handler,
            # BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ADV_STOP_CMD: self.gap_adv_stop_cmd_handler,
            # BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_CONNECT_CMD: self.connect_cmd_handler,
        }

    def _adv_cmp_evt_handler(self, gtl: GapmCmpEvt):
        self.dev_params.advertising = False
        evt = BleEventGapAdvCompleted()

        match gtl.parameters.operation:
            case GAPM_OPERATION.GAPM_ADV_NON_CONN:
                evt.adv_type = BLE_GAP_CONN_MODE.GAP_CONN_MODE_NON_CONN
            case GAPM_OPERATION.GAPM_ADV_UNDIRECT:
                evt.adv_type = BLE_GAP_CONN_MODE.GAP_CONN_MODE_UNDIRECTED
            case GAPM_OPERATION.GAPM_ADV_DIRECT:
                evt.adv_type = BLE_GAP_CONN_MODE.GAP_CONN_MODE_DIRECTED
            case GAPM_OPERATION.GAPM_ADV_DIRECT_LDC:
                evt.adv_type = BLE_GAP_CONN_MODE.GAP_CONN_MODE_DIRECTED_LDC

        match gtl.parameters.status:
            case HOST_STACK_ERROR_CODE.GAP_ERR_NO_ERROR:
                evt.status = BLE_ERROR.BLE_STATUS_OK

            case HOST_STACK_ERROR_CODE.GAP_ERR_CANCELED:
                evt.status = BLE_ERROR.BLE_ERROR_CANCELED

            case HOST_STACK_ERROR_CODE.GAP_ERR_COMMAND_DISALLOWED:
                evt.status = BLE_ERROR.BLE_ERROR_NOT_ALLOWED

            case HOST_STACK_ERROR_CODE.GAP_ERR_INVALID_PARAM \
                    | HOST_STACK_ERROR_CODE.GAP_ERR_ADV_DATA_INVALID \
                    | HOST_STACK_ERROR_CODE.LL_ERR_PARAM_OUT_OF_MAND_RANGE:

                evt.status = BLE_ERROR.BLE_ERROR_INVALID_PARAM

            case HOST_STACK_ERROR_CODE.GAP_ERR_NOT_SUPPORTED \
                    | HOST_STACK_ERROR_CODE.GAP_ERR_PRIVACY_CFG_PB:

                evt.status = BLE_ERROR.BLE_ERROR_NOT_SUPPORTED

            case HOST_STACK_ERROR_CODE.GAP_ERR_TIMEOUT:
                evt.status = BLE_ERROR.BLE_ERROR_TIMEOUT
            case _:
                evt.status = gtl.parameters.status

        self._mgr_event_queue_send(evt)

    def _ble_role_to_gtl_role(self, role: BLE_GAP_ROLE):

        gtl_role = GAP_ROLE.GAP_ROLE_NONE
# if (dg_configBLE_CENTRAL == 1)  # TODO handle if defs
        if (role & BLE_GAP_ROLE.GAP_CENTRAL_ROLE):
            gtl_role |= GAP_ROLE.GAP_ROLE_CENTRAL
# endif /* (dg_configBLE_CENTRAL == 1)
# if (dg_configBLE_PERIPHERAL == 1)
        if (role & BLE_GAP_ROLE.GAP_PERIPHERAL_ROLE):
            gtl_role |= GAP_ROLE.GAP_ROLE_PERIPHERAL
# endif /* (dg_configBLE_PERIPHERAL == 1)
# if (dg_configBLE_BROADCASTER == 1)
        if (role & BLE_GAP_ROLE.GAP_BROADCASTER_ROLE):
            gtl_role |= GAP_ROLE.GAP_ROLE_BROADCASTER
# endif /* (dg_configBLE_BROADCASTER == 1) */
# if (dg_configBLE_OBSERVER == 1)
        if (role & BLE_GAP_ROLE.GAP_OBSERVER_ROLE):
            gtl_role |= GAP_ROLE.GAP_ROLE_OBSERVER
# endif /* (dg_configBLE_OBSERVER == 1) */
        return gtl_role

    def _dev_params_to_gtl(self) -> GapmSetDevConfigCmd:
        gtl = GapmSetDevConfigCmd()
        gtl.parameters.role = self._ble_role_to_gtl_role(self.dev_params.role)
        gtl.parameters.renew_dur = self.dev_params.addr_renew_duration
        gtl.parameters.att_cfg = self.dev_params.att_db_cfg
        gtl.parameters.max_mtu = self.dev_params.mtu_size
        gtl.parameters.max_mps = self.dev_params.mtu_size
        gtl.parameters.addr.addr[:] = self.dev_params.own_addr.addr
        # TODO function for this conversion?
        match self.dev_params.own_addr.addr_type:
            case BLE_OWN_ADDR_TYPE.PUBLIC_STATIC_ADDRESS:
                gtl.parameters.addr_type = GAPM_ADDR_TYPE.GAPM_CFG_ADDR_PUBLIC
            case BLE_OWN_ADDR_TYPE.PRIVATE_STATIC_ADDRESS:
                gtl.parameters.addr_type = GAPM_ADDR_TYPE.GAPM_CFG_ADDR_PRIVATE
            case BLE_OWN_ADDR_TYPE.PRIVATE_RANDOM_RESOLVABLE_ADDRESS:
                gtl.parameters.addr_type = GAPM_ADDR_TYPE.GAPM_CFG_ADDR_PRIVACY
            case BLE_OWN_ADDR_TYPE.PRIVATE_RANDOM_NONRESOLVABLE_ADDRESS:
                gtl.parameters.addr_type = GAPM_ADDR_TYPE.GAPM_CFG_ADDR_PRIVACY
        # if (dg_configBLE_PRIVACY_1_2 == 1)
            case BLE_OWN_ADDR_TYPE.PRIVATE_CNTL:
                gtl.parameters.addr_type = GAPM_ADDR_TYPE.GAPM_CFG_ADDR_PRIVACY_CNTL
        # endif /* (dg_configBLE_PRIVACY_1_2 == 1) */
            case _:
                gtl.parameters.addr_type = GAPM_ADDR_TYPE.GAPM_CFG_ADDR_PUBLIC

        gtl.parameters.irk.key[:] = self.dev_params.irk.key
        gtl.parameters.max_txoctets = dg_configBLE_DATA_LENGTH_TX_MAX
        gtl.parameters.max_txtime = (dg_configBLE_DATA_LENGTH_TX_MAX + 11 + 3) * 8

        return gtl

    def _resolve_address_from_connected_evt(self, evt: GapcConnectionReqInd, param: None):
        # Check if peer's address is random
        if evt.parameters.peer_addr_type != BLE_ADDR_TYPE.PRIVATE_ADDRESS:
            return False

        # Check if peer's address is resolvable
        if evt.parameters.peer_addr.addr[5] & 0xC0 != 0x40:
            return False
        
        # TODO gtl message
        # gtl = GapmResolvAddrCmd
        return False

    # TODO sdk passes rsp in as param. you have passed in command.params
    def _set_role_rsp(self, gtl: GapmCmpEvt, new_role: BLE_GAP_ROLE = BLE_GAP_ROLE.GAP_NO_ROLE):
        event = gtl.parameters
        response = BleMgrGapRoleSetRsp()
        response.prev_role = self.dev_params.role
        response.new_role = new_role
        response.status = BLE_ERROR.BLE_ERROR_FAILED

        match event.status:
            case HOST_STACK_ERROR_CODE.GAP_ERR_NO_ERROR:
                self.dev_params.role = new_role
                response.status = BLE_ERROR.BLE_STATUS_OK
            case HOST_STACK_ERROR_CODE.GAP_ERR_INVALID_PARAM:
                response.status = BLE_ERROR.BLE_ERROR_INVALID_PARAM
            case HOST_STACK_ERROR_CODE.GAP_ERR_NOT_SUPPORTED:
                response.status = BLE_ERROR.BLE_ERROR_NOT_ALLOWED
            case HOST_STACK_ERROR_CODE.GAP_ERR_COMMAND_DISALLOWED:
                response.status = BLE_ERROR.BLE_ERROR_NOT_ALLOWED
            case _:
                response.status = event.status

        self._mgr_response_queue_send(response)

    def adv_start_cmd_handler(self, command: BleMgrGapAdvStartCmd):

        response = BLE_ERROR.BLE_ERROR_FAILED

        # TODO error checks
        # Check if an advertising operation is already in progress
        # Check if length of advertising data is within limits
        self.dev_params.adv_type = command.adv_type
        message = GapmStartAdvertiseCmd()

        match command.adv_type:
            case BLE_GAP_CONN_MODE.GAP_CONN_MODE_NON_CONN:
                message.parameters.op.code = GAPM_OPERATION.GAPM_ADV_NON_CONN
                pass
            case BLE_GAP_CONN_MODE.GAP_CONN_MODE_UNDIRECTED:
                message.parameters.op.code = GAPM_OPERATION.GAPM_ADV_UNDIRECT
                pass
            case BLE_GAP_CONN_MODE.GAP_CONN_MODE_DIRECTED:
                message.parameters.op.code = GAPM_OPERATION.GAPM_ADV_DIRECT
                pass
            case BLE_GAP_CONN_MODE.GAP_CONN_MODE_DIRECTED_LDC:
                message.parameters.op.code = GAPM_OPERATION.GAPM_ADV_DIRECT_LDC
                pass
            case _:
                return BLE_ERROR.BLE_ERROR_NOT_ACCEPTED

        message.parameters.op.addr_src = self.dev_params.own_addr.addr_type

        match self.dev_params.own_addr.addr_type:
            case BLE_OWN_ADDR_TYPE.PUBLIC_STATIC_ADDRESS:
                message.parameters.op.addr_src = GAPM_OWN_ADDR.GAPM_STATIC_ADDR
            case BLE_OWN_ADDR_TYPE.PRIVATE_STATIC_ADDRESS:
                message.parameters.op.addr_src = GAPM_OWN_ADDR.GAPM_STATIC_ADDR
            case BLE_OWN_ADDR_TYPE.PRIVATE_RANDOM_RESOLVABLE_ADDRESS:
                message.parameters.op.addr_src = GAPM_OWN_ADDR.GAPM_GEN_RSLV_ADDR
            case BLE_OWN_ADDR_TYPE.PRIVATE_RANDOM_NONRESOLVABLE_ADDRESS:
                message.parameters.op.addr_src = GAPM_OWN_ADDR.GAPM_GEN_NON_RSLV_ADDR
            # if (dg_configBLE_PRIVACY_1_2 == 1)
            case BLE_OWN_ADDR_TYPE.PRIVATE_CNTL:
                # Generate AdvA using local IRK
                message.parameters.op.addr_src = GAPM_OWN_ADDR.GAPM_GEN_RSLV_ADDR

                # TODO need to handle getting public address. In adapter due to nvm>
                # ad_ble_get_public_address(gcmd->info.host.peer_info.addr.addr);
                # message.parameters.info.host.peer_info.addr_type = ADDR_PUBLIC;  # ADDR_PUBLIC in co_bt.py

            # endif /* (dg_configBLE_PRIVACY_1_2 == 1) */
            case _:
                message.parameters.op.addr_src = GAPM_OWN_ADDR.GAPM_STATIC_ADDR

        message.parameters.intv_min = self.dev_params.adv_intv_min
        message.parameters.intv_max = self.dev_params.adv_intv_max
        message.parameters.channel_map = self.dev_params.adv_channel_map

        if command.adv_type < BLE_GAP_CONN_MODE.GAP_CONN_MODE_DIRECTED:
            message.parameters.info.host.mode = self.dev_params.adv_mode
            message.parameters.info.host.adv_filt_policy = self.dev_params.adv_filter_policy
            message.parameters.info.host.adv_data_len = self.dev_params.adv_data_length
            adv_len = self.dev_params.adv_data_length
            message.parameters.info.host.adv_data[:adv_len] = self.dev_params.adv_data[:adv_len]

            # TODO add scan response.
        else:
            # TODO fill in for Directed adv more
            pass

        self.dev_params.advertising = True
        self._adapter_command_queue_send(message)

        response = BleMgrGapAdvStartRsp(BLE_ERROR.BLE_STATUS_OK)
        self._mgr_response_queue_send(response)

    def cmp_evt_handler(self, gtl: GapmCmpEvt) -> bool:

        match gtl.parameters.operation:
            case GAPM_OPERATION.GAPM_ADV_NON_CONN \
                    | GAPM_OPERATION.GAPM_ADV_UNDIRECT \
                    | GAPM_OPERATION.GAPM_ADV_DIRECT \
                    | GAPM_OPERATION.GAPM_ADV_DIRECT_LDC:

                self._adv_cmp_evt_handler(gtl)
            case _:
                return False
        return True

    def connected_evt_handler(self, gtl: GapcConnectionReqInd):
        evt = BleEventGapConnected()
        evt.conn_idx = self._task_to_connidx(gtl.src_id)
        evt.own_addr.addr_type = self.dev_params.own_addr.addr_type
        evt.own_addr.addr = self.dev_params.own_addr.addr 
        # if (dg_configBLE_PRIVACY_1_2 == 1)
        # evt.peer_address.addr_type = gtl.parameters.peer_addr_type & 0x01
        # else
        evt.peer_address.addr_type = gtl.parameters.peer_addr_type
        # endif
        evt.peer_address.addr = bytes(gtl.parameters.peer_addr.addr)
        evt.conn_params.interval_min = gtl.parameters.con_interval
        evt.conn_params.interval_max = gtl.parameters.con_interval
        evt.conn_params.slave_latency = gtl.parameters.con_latency
        evt.conn_params.sup_timeout = gtl.parameters.sup_to

        # if (dg_configBLE_SKIP_LATENCY_API == 1)
        # ble_mgr_skip_latency_set(evt->conn_idx, false);
        # endif /* (dg_configBLE_SKIP_LATENCY_API == 1) */

        dev = self._stored_device_list.find_device_by_address(evt.peer_address, create=True)
        dev.conn_idx = evt.conn_idx
        dev.connected = True
        dev.mtu = ATT_DEFAULT_MTU
        # if (dg_configBLE_2MBIT_PHY == 1)
        # dev.tx_phy = BLE_GAP_PHY.BLE_GAP_PHY_1M
        # dev.rx_phy = BLE_GAP_PHY.BLE_GAP_PHY_1M
        # endif /* (dg_configBLE_2MBIT_PHY == 1) */
        if dev.connecting:
            dev.master = True
            dev.connecting = False
        else:
            dev.master = False

        # if (dg_configBLE_CENTRAL == 1)  # TODO how to handle these config params
        # if dev.master:
            # TODO initiate a version exchange
        #    pass
        # endif /* (dg_configBLE_CENTRAL == 1) */

        # if (dg_configBLE_PRIVACY_1_2 == 1)
        if self.dev_params.own_addr.addr_type != BLE_OWN_ADDR_TYPE.PRIVATE_CNTL:
            # endif /* (dg_configBLE_PRIVACY_1_2 == 1) */
            pass  # TODO needs to be same as resolve addr here

        if self._resolve_address_from_connected_evt(gtl, evt):  # Note passed in gtl instead of gtl.params
            pass

        self._mgr_event_queue_send(evt)

        cfm = GapcConnectionCfm(conidx=evt.conn_idx)
        # TODO should this be GAP_AUTH_MASK
        cfm.parameters.auth = GAP_AUTH_MASK.GAP_AUTH_BOND if dev.bonded else GAP_AUTH_MASK.GAP_AUTH_NONE
        cfm.parameters.auth |= GAP_AUTH_MASK.GAP_AUTH_MITM if dev.mitm else GAP_AUTH_MASK.GAP_AUTH_NONE
        # if (dg_configBLE_SECURE_CONNECTIONS == 1)
        cfm.parameters.auth |= GAP_AUTH_MASK.GAP_AUTH_SEC if dev.secure else GAP_AUTH_MASK.GAP_AUTH_NONE
        # endif /* (dg_configBLE_SECURE_CONNECTIONS == 1) */
        # if (RWBLE_SW_VERSION >= VERSION_8_1)
        cfm.parameters.auth |= GAPC_FIELDS_MASK.GAPC_LTK_MASK if dev.remote_ltk else GAP_AUTH_MASK.GAP_AUTH_NONE
        # endif /* (RWBL
        if dev.csrk.key == b'':  # TODO need to do equiv of null check
            pass
        if dev.remote_csrk.key == b'':  # TODO need to do equiv of null check
            pass

        # TODO something with service changed characteristic value from storage
        self._adapter_command_queue_send(cfm)

    def disconnected_evt_handler(self, gtl):
        pass

    def get_device_info_req_evt_handler(self, gtl: GapcGetDevInfoReqInd):

        cfm = GapcGetDevInfoCfm(conidx=self._task_to_connidx(gtl.src_id))
        cfm.parameters.req = gtl.parameters.req
        match gtl.parameters.req:
            case GAPC_DEV_INFO.GAPC_DEV_NAME:
                cfm.parameters.info.name.value = (c_uint8 * len(self.dev_params.dev_name)).from_buffer_copy(self.dev_params.dev_name)
            case GAPC_DEV_INFO.GAPC_DEV_APPEARANCE:
                cfm.parameters.info.appearance = self.dev_params.appearance
            case GAPC_DEV_INFO.GAPC_DEV_SLV_PREF_PARAMS:
                cfm.parameters.info.slv_params.con_intv_min = self.dev_params.gap_ppcp.interval_min
                cfm.parameters.info.slv_params.con_intv_max = self.dev_params.gap_ppcp.interval_max
                cfm.parameters.info.slv_params.slave_latency = self.dev_params.gap_ppcp.slave_latency
                cfm.parameters.info.slv_params.conn_timeout = self.dev_params.gap_ppcp.sup_timeout
            case _:
                pass

        self._adapter_command_queue_send(cfm)

    def role_set_cmd_handler(self, command: BleMgrGapRoleSetCmd):
        dev_params_gtl = self._dev_params_to_gtl()
        dev_params_gtl.parameters.role = self._ble_role_to_gtl_role(command.role)
        self._wait_queue_add(BLE_CONN_IDX_INVALID,
                             GAPM_MSG_ID.GAPM_CMP_EVT,
                             GAPM_OPERATION.GAPM_SET_DEV_CONFIG,
                             self._set_role_rsp,
                             command.role)

        self._adapter_command_queue_send(dev_params_gtl)


'''
static const ble_mgr_cmd_handler_t h_gap[BLE_MGR_CMD_GET_IDX(BLE_MGR_GAP_LAST_CMD)] = {
        ble_mgr_gap_address_set_cmd_handler,
        ble_mgr_gap_device_name_set_cmd_handler,
        ble_mgr_gap_appearance_set_cmd_handler,
        ble_mgr_gap_ppcp_set_cmd_handler,
        ble_mgr_gap_adv_start_cmd_handler,              STARTED
        ble_mgr_gap_adv_stop_cmd_handler,
        ble_mgr_gap_adv_data_set_cmd_handler,
        ble_mgr_gap_adv_set_perm_id_cmd_handler,
        ble_mgr_gap_scan_start_cmd_handler,
        ble_mgr_gap_scan_stop_cmd_handler,
        ble_mgr_gap_connect_cmd_handler,
        ble_mgr_gap_connect_cancel_cmd_handler,
        ble_mgr_gap_disconnect_cmd_handler,
        ble_mgr_gap_peer_version_get_cmd_handler,
        ble_mgr_gap_peer_features_get_cmd_handler,
        ble_mgr_gap_conn_rssi_get_cmd_handler,
        ble_mgr_gap_role_set_cmd_handler,               STARTED
        ble_mgr_gap_mtu_size_set_cmd_handler,
        ble_mgr_gap_channel_map_set_cmd_handler,
        ble_mgr_gap_conn_param_update_cmd_handler,
        ble_mgr_gap_conn_param_update_reply_cmd_handler,
        ble_mgr_gap_pair_cmd_handler,
        ble_mgr_gap_pair_reply_cmd_handler,
        ble_mgr_gap_passkey_reply_cmd_handler,
        ble_mgr_gap_unpair_cmd_handler,
        ble_mgr_gap_set_sec_level_cmd_handler,
#if (dg_configBLE_SKIP_LATENCY_API == 1)
        ble_mgr_gap_skip_latency_cmd_handler,
#endif /* (dg_configBLE_SKIP_LATENCY_API == 1) */
        ble_mgr_gap_data_length_set_cmd_handler,
#if (dg_configBLE_SECURE_CONNECTIONS == 1)
        ble_mgr_gap_numeric_reply_cmd_handler,
#endif /* (dg_configBLE_SECURE_CONNECTIONS == 1) */
        ble_mgr_gap_address_resolve_cmd_handler,
#if (dg_configBLE_2MBIT_PHY == 1)
        ble_mgr_gap_phy_set_cmd_handler,
#endif /* (dg_configBLE_2MBIT_PHY == 1) */
};

void ble_mgr_gap_dev_bdaddr_ind_evt_handler(ble_gtl_msg_t *gtl);
void ble_mgr_gap_adv_report_evt_handler(ble_gtl_msg_t *gtl);
void ble_mgr_gap_connected_evt_handler(ble_gtl_msg_t *gtl);                 STARTED
void ble_mgr_gap_get_device_info_req_evt_handler(ble_gtl_msg_t *gtl);       STARTED
void ble_mgr_gap_set_device_info_req_evt_handler(ble_gtl_msg_t *gtl);
void ble_mgr_gap_disconnected_evt_handler(ble_gtl_msg_t *gtl);
void ble_mgr_gap_peer_version_ind_evt_handler(ble_gtl_msg_t *gtl);
void ble_mgr_gap_peer_features_ind_evt_handler(ble_gtl_msg_t *gtl);
void ble_mgr_gap_con_rssi_ind_handler(ble_gtl_msg_t *gtl);
void ble_mgr_gap_conn_param_update_req_evt_handler(ble_gtl_msg_t *gtl);
void ble_mgr_gap_conn_param_updated_evt_handler(ble_gtl_msg_t *gtl);
void ble_mgr_gapm__adv_cmp_evt_handler(ble_gtl_msg_t *gtl);                 STARTED
void ble_mgr_gapm_scan_cmp_evt_handler(ble_gtl_msg_t *gtl);
void ble_mgr_gapm_connect_cmp_evt_handler(ble_gtl_msg_t *gtl);
void ble_mgr_gap_bond_req_evt_handler(ble_gtl_msg_t *gtl);
void ble_mgr_gap_bond_ind_evt_handler(ble_gtl_msg_t *gtl);
void ble_mgr_gap_security_ind_evt_handler(ble_gtl_msg_t *gtl);
void ble_mgr_gap_sign_counter_ind_evt_handler(ble_gtl_msg_t *gtl);
void ble_mgr_gap_encrypt_req_ind_evt_handler(ble_gtl_msg_t *gtl);
void ble_mgr_gapc_cmp__disconnect_evt_handler(ble_gtl_msg_t *gtl);
void ble_mgr_gapc_cmp__update_params_evt_handler(ble_gtl_msg_t *gtl);
void ble_mgr_gapc_cmp__bond_evt_handler(ble_gtl_msg_t *gtl);
void ble_mgr_gapc_cmp__security_req_evt_handler(ble_gtl_msg_t *gtl);
void ble_mgr_gap_encrypt_ind_evt_handler(ble_gtl_msg_t *gtl);
void ble_mgr_gap_addr_solved_evt_handler(ble_gtl_msg_t *gtl);
void ble_mgr_gap_le_pkt_size_ind_evt_handler(ble_gtl_msg_t *gtl);
void ble_mgr_gap_cmp__data_length_set_evt_handler(ble_gtl_msg_t *gtl);
void ble_mgr_gapm_cmp__address_resolve_evt_handler(ble_gtl_msg_t *gtl);
void ble_mgr_gap_le_phy_ind_handler(ble_gtl_msg_t *gtl);
void ble_mgr_gap_le_rd_tx_pwr_lvl_enh_ind_handler(ble_gtl_msg_t *gtl);
void ble_mgr_gap_le_tx_pwr_lvl_report_ind_handler(ble_gtl_msg_t *gtl);
void ble_mgr_gap_le_path_loss_thres_ind_handler(ble_gtl_msg_t *gtl);
'''
