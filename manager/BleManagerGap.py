import asyncio
from ctypes import c_uint8
import secrets

from ble_api.BleCommon import BLE_ERROR, BleEventBase, BLE_OWN_ADDR_TYPE, BLE_ADDR_TYPE, BLE_HCI_ERROR, \
    BdAddress
from ble_api.BleConfig import dg_configBLE_PAIR_INIT_KEY_DIST, dg_configBLE_PAIR_RESP_KEY_DIST, \
    dg_configBLE_SECURE_CONNECTIONS, dg_configBLE_DATA_LENGTH_TX_MAX, dg_configBLE_PRIVACY_1_2, \
    dg_configBLE_CENTRAL, dg_configBLE_PERIPHERAL, dg_configBLE_DATA_LENGTH_TX_MAX, \
    dg_configBLE_DATA_LENGTH_RX_MAX, ble_data_length_to_time

from ble_api.BleGap import BLE_GAP_ROLE, BLE_GAP_CONN_MODE, BleEventGapConnected, BleEventGapDisconnected,  \
    BleEventGapAdvCompleted, BLE_CONN_IDX_INVALID, GAP_SEC_LEVEL, GAP_SCAN_TYPE, BleEventGapAdvReport, \
    BleEventGapScanCompleted, BleEventGapConnectionCompleted, BleEventGapDisconnectFailed, GapConnParams, \
    BleEventGapConnParamUpdateCompleted, BleEventGapConnParamUpdated, BleEventGapConnParamUpdateReq, \
    BLE_GAP_MAX_BONDED, GAP_IO_CAPABILITIES, BLE_ENC_KEY_SIZE_MAX, GAP_SEC_LEVEL, BleEventGapPairReq, \
    BleEventGapPasskeyNotify, BleEventGapNumericRequest, BleEventGapPairCompleted, BleEventGapSecLevelChanged, \
    BleEventGapAddressResolved, BleEventGapPeerVersion, BleEventGapPeerFeatures

from gtl_messages.gtl_message_base import GtlMessageBase
from gtl_messages.gtl_message_gapc import GapcConnectionCfm, GapcConnectionReqInd, GapcGetDevInfoReqInd, GapcGetDevInfoCfm, \
    GapcDisconnectInd, GapcCmpEvt, GapcDisconnectCmd, GapcParamUpdateCmd, GapcParamUpdatedInd, GapcParamUpdateReqInd, \
    GapcParamUpdateCfm, GapcBondCfm, GapcBondCmd, GapcSecurityCmd, GapcBondReqInd, GapcBondInd, GapcGetInfoCmd, \
    GapcPeerVersionInd, GapcPeerFeaturesInd

from gtl_messages.gtl_message_gapm import GapmSetDevConfigCmd, GapmStartAdvertiseCmd, GapmCmpEvt, GapmStartConnectionCmd, \
    GapmStartScanCmd, GapmAdvReportInd, GapmCancelCmd

from gtl_port.co_bt import RAND_NB_LEN, KEY_LEN, BLE_LE_LENGTH_FEATURE
from gtl_port.co_error import CO_ERROR
from gtl_port.gap import GAP_ROLE, GAP_AUTH_MASK, gap_bdaddr, GAP_IO_CAP, GAP_OOB, GAP_AUTH_MASK, GAP_SEC_REQ, \
    GAP_TK_TYPE
from gtl_port.gapc import GAPC_FIELDS_MASK
from gtl_port.gapc_task import GAPC_MSG_ID, GAPC_DEV_INFO, GAPC_OPERATION, GAPC_BOND
from gtl_port.gapm_task import GAPM_MSG_ID, GAPM_OPERATION, GAPM_ADDR_TYPE, GAPM_OWN_ADDR, SCAN_FILTER_POLICY, \
    SCAN_DUP_FILTER_POLICY, GAPM_LE_LENGTH_EXT_OCTETS_MIN
from gtl_port.rwble_hl_error import HOST_STACK_ERROR_CODE
from manager.BleDevParams import BleDevParamsDefault
from manager.BleManagerCommon import BleManagerBase

from manager.BleManagerGapMsgs import BLE_CMD_GAP_OPCODE, BleMgrGapRoleSetRsp, BleMgrGapAdvStartCmd, BleMgrGapAdvStartRsp, \
    BleMgrGapRoleSetCmd, BleMgrGapConnectCmd, BleMgrGapScanStartCmd, BleMgrGapScanStartRsp, BleMgrGapConnectRsp, \
    BleMgrGapDisconnectCmd, BleMgrGapDisconnectRsp, BleMgrGapConnectCancelCmd, BleMgrGapConnectCancelRsp, \
    BleMgrGapConnParamUpdateCmd, BleMgrGapConnParamUpdateRsp, BleMgrGapConnParamUpdateReplyCmd, \
    BleMgrGapConnParamUpdateReplyRsp, BleMgrGapPairCmd, BleMgrGapPairRsp, BleMgrGapPairReplyCmd, BleMgrGapPairReplyRsp, \
    BleMgrGapPasskeyReplyCmd, BleMgrGapPasskeyReplyRsp, BleMgrGapNumericReplyCmd, BleMgrGapNumericReplyRsp

from manager.BleManagerStorage import StoredDeviceQueue, StoredDevice
from manager.GtlWaitQueue import GtlWaitQueue




# TODO this is from stack
ATT_DEFAULT_MTU = (23)


class BleManagerGap(BleManagerBase):

    def __init__(self,
                 mgr_response_q: asyncio.Queue[BLE_ERROR],
                 mgr_event_q: asyncio.Queue[BleEventBase],
                 adapter_command_q: asyncio.Queue[GtlMessageBase],
                 wait_q: GtlWaitQueue,
                 stored_device_q: StoredDeviceQueue) -> None:

        super().__init__(mgr_response_q, mgr_event_q, adapter_command_q, wait_q, stored_device_q)

        # TODO dev_params passed to base class?
        self.dev_params = BleDevParamsDefault()

        self.cmd_handlers = {
            BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ADDRESS_SET_CMD: None,
            BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_DEVICE_NAME_SET_CMD: None,
            BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_APPEARANCE_SET_CMD: None,
            BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_PPCP_SET_CMD: None,
            BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ADV_START_CMD: self.adv_start_cmd_handler,
            BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ADV_STOP_CMD: None,
            BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ADV_DATA_SET_CMD: None,
            BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ADV_SET_PERMUTATION_CMD: None,
            BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_SCAN_START_CMD: self.scan_start_cmd_handler,
            BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_SCAN_STOP_CMD: None,
            BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_CONNECT_CMD: self.connect_cmd_handler,
            BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_CONNECT_CANCEL_CMD: self.connect_cancel_cmd_handler,
            BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_DISCONNECT_CMD: self.disconnect_cmd_handler,
            BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_PEER_VERSION_GET_CMD: None,
            BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_PEER_FEATURES_GET_CMD: None,
            BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_CONN_RSSI_GET_CMD: None,
            BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ROLE_SET_CMD: self.role_set_cmd_handler,
            BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_MTU_SIZE_SET_CMD: None,
            BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_CHANNEL_MAP_SET_CMD: None,
            BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_CONN_PARAM_UPDATE_CMD: self.conn_param_update,
            BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_CONN_PARAM_UPDATE_REPLY_CMD: self.conn_param_update_reply_cmd_handler,
            BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_PAIR_CMD: self.pair_cmd_handler,
            BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_PAIR_REPLY_CMD: self.pair_reply_cmd_handler,
            BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_PASSKEY_REPLY_CMD: self.passkey_reply_cmd_handler,
            BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_UNPAIR_CMD: None,
            BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_SET_SEC_LEVEL_CMD: None,
            BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_SKIP_LATENCY_CMD: None,
            BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_DATA_LENGTH_SET_CMD: None,
            BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_NUMERIC_REPLY_CMD: self.numeric_reply_cmd_handler,
            BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ADDRESS_RESOLVE_CMD: None,
            BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_PHY_SET_CMD: None
        }

        # TODO separate gapm and gapc?
        self.evt_handlers = {
            GAPM_MSG_ID.GAPM_DEV_BDADDR_IND: None,
            GAPM_MSG_ID.GAPM_ADV_REPORT_IND: self.adv_report_evt_handler,
            GAPC_MSG_ID.GAPC_CONNECTION_REQ_IND: self.connected_evt_handler,
            GAPC_MSG_ID.GAPC_GET_DEV_INFO_REQ_IND: self.get_device_info_req_evt_handler,
            GAPC_MSG_ID.GAPC_SET_DEV_INFO_REQ_IND: None,
            GAPC_MSG_ID.GAPC_DISCONNECT_IND: self.disconnected_evt_handler,
            GAPC_MSG_ID.GAPC_PEER_VERSION_IND: self.peer_version_ind_evt_handler,
            GAPC_MSG_ID.GAPC_PEER_FEATURES_IND: self.peer_features_ind_evt_handler,
            GAPC_MSG_ID.GAPC_CON_RSSI_IND: None,
            GAPC_MSG_ID.GAPC_PARAM_UPDATE_REQ_IND: self.conn_param_update_req_evt_handler,
            GAPC_MSG_ID.GAPC_PARAM_UPDATED_IND: self.conn_param_updated_evt_handler,
            GAPC_MSG_ID.GAPC_BOND_REQ_IND: self.bond_req_evt_handler,
            GAPC_MSG_ID.GAPC_BOND_IND: self.bond_ind_evt_handler,
            GAPC_MSG_ID.GAPC_SECURITY_IND: None,
            GAPC_MSG_ID.GAPC_SIGN_COUNTER_IND: None,
            GAPC_MSG_ID.GAPC_ENCRYPT_REQ_IND: None,
            GAPC_MSG_ID.GAPC_ENCRYPT_IND: None,
            GAPM_MSG_ID.GAPM_ADDR_SOLVED_IND: None,
            GAPC_MSG_ID.GAPC_LE_PKT_SIZE_IND: None,
            GAPM_MSG_ID.GAPM_CMP_EVT: self.gapm_cmp_evt_handler,
            GAPC_MSG_ID.GAPC_CMP_EVT: self.gapc_cmp_evt_handler
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

    def _auth_to_sec_level(self, auth: GAP_AUTH_MASK, key_size: int):

        if auth & GAP_AUTH_MASK.GAP_AUTH_MITM:
            if (auth & GAP_AUTH_MASK.GAP_AUTH_SEC
                    and key_size == BLE_ENC_KEY_SIZE_MAX):

                sec_level = GAP_SEC_LEVEL.GAP_SEC_LEVEL_4

            else:
                sec_level = GAP_SEC_LEVEL.GAP_SEC_LEVEL_3

        else:
            sec_level = GAP_SEC_LEVEL.GAP_SEC_LEVEL_2

        return sec_level


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

    def _change_conn_data_length(self, conn_idx: int, tx_length: int, tx_time: int):
        # TODO 
        pass

    def _cmp_address_resolve_evt_handler(self, gtl: GapmCmpEvt):
        return False

    def _cmp_bond_evt_handler(self, gtl: GapcCmpEvt):

        if gtl.parameters.status == HOST_STACK_ERROR_CODE.GAP_ERR_NO_ERROR:
            # Nothing to do, we replied in GAPC_BOND_IND handler
            pass
        else:
            evt = BleEventGapPairCompleted()
            evt.conn_idx = self._task_to_connidx(gtl.src_id)
            evt.status = gtl.parameters.status
            evt.bond = False
            evt.mitm = False
            self._mgr_event_queue_send(evt)

    def _cmp_data_length_set_evt_handler(self, gtl):  # TODO called from GAPM and GAPC
        return False

    def _cmp_disconnect_evt_handler(self, gtl: GapcCmpEvt):
        # ignore if no error
        if gtl.parameters.status != HOST_STACK_ERROR_CODE.GAP_ERR_NO_ERROR:
            evt = BleEventGapDisconnectFailed()
            evt.conn_idx = self._task_to_connidx(gtl.src_id)
            match gtl.parameters.status:
                case (HOST_STACK_ERROR_CODE.GAP_ERR_INVALID_PARAM
                        | HOST_STACK_ERROR_CODE.LL_ERR_INVALID_HCI_PARAM):

                    evt.status = BLE_ERROR.BLE_ERROR_INVALID_PARAM

                case HOST_STACK_ERROR_CODE.LL_ERR_COMMAND_DISALLOWED:
                    evt.status = BLE_ERROR.BLE_ERROR_NOT_ALLOWED
                case _:
                    # evt.status = gtl.parameters.status  # TODO this throws a ValueError if not a valid BLE_ERROR
                    # need to be able to set a BLE_ERROR that is not defined. Could make a LittleEndianStructure
                    evt.status = BLE_ERROR.BLE_ERROR_FAILED

            self._mgr_event_queue_send(evt)

    def _cmp_security_req_evt_handler(self, gtl: GapcCmpEvt):
        conn_idx = self._task_to_connidx(gtl.src_id)
        dev = self._stored_device_list.find_device_by_conn_idx(conn_idx)
        if dev:
            dev.security_req_pending = False

    def _cmp_update_params_evt_handler(self, gtl: GapcCmpEvt):
        conn_idx = self._task_to_connidx(gtl.src_id)
        dev = self._stored_device_list.find_device_by_conn_idx(conn_idx)
        if dev:
            dev.updating = False

        evt = BleEventGapConnParamUpdateCompleted()
        evt.conn_idx = conn_idx
        match gtl.parameters.status:
            case HOST_STACK_ERROR_CODE.GAP_ERR_NO_ERROR:
                evt.status = BLE_ERROR.BLE_STATUS_OK
            case (HOST_STACK_ERROR_CODE.GAP_ERR_INVALID_PARAM
                    | HOST_STACK_ERROR_CODE.LL_ERR_INVALID_HCI_PARAM):

                evt.status = BLE_ERROR.BLE_ERROR_INVALID_PARAM

            case HOST_STACK_ERROR_CODE.GAP_ERR_TIMEOUT:
                evt.status = BLE_ERROR.BLE_ERROR_TIMEOUT
            case HOST_STACK_ERROR_CODE.GAP_ERR_REJECTED:
                evt.status = BLE_ERROR.BLE_ERROR_NOT_ACCEPTED
            case HOST_STACK_ERROR_CODE.LL_ERR_COMMAND_DISALLOWED:
                evt.status = BLE_ERROR.BLE_ERROR_NOT_ALLOWED
            case (HOST_STACK_ERROR_CODE.LL_ERR_UNKNOWN_HCI_COMMAND 
                    | HOST_STACK_ERROR_CODE.LL_ERR_UNSUPPORTED
                    | HOST_STACK_ERROR_CODE.LL_ERR_UNKNOWN_LMP_PDU
                    | HOST_STACK_ERROR_CODE.LL_ERR_UNSUPPORTED_LMP_PARAM_VALUE):

                evt.status = BLE_ERROR.BLE_ERROR_NOT_SUPPORTED

            case HOST_STACK_ERROR_CODE.LL_ERR_UNSUPPORTED_REMOTE_FEATURE:
                evt.status = BLE_ERROR.BLE_ERROR_NOT_SUPPORTED_BY_PEER
            case HOST_STACK_ERROR_CODE.LL_ERR_LMP_COLLISION:
                evt.status = BLE_ERROR.BLE_ERROR_LMP_COLLISION
            case HOST_STACK_ERROR_CODE.LL_ERR_DIFF_TRANSACTION_COLLISION:
                evt.status = BLE_ERROR.BLE_ERROR_DIFF_TRANS_COLLISION
            case _:
                # evt->status = gevt->status;  # TODO error if gtl.parameters.status not a valid BLE_ERROR
                evt.status = BLE_ERROR.BLE_ERROR_FAILED

        self._mgr_event_queue_send(evt)

    def _conn_cleanup(self, conn_idx: int = 0, reason: CO_ERROR = CO_ERROR.CO_ERROR_NO_ERROR) -> None:
        dev = self._stored_device_list.find_device_by_conn_idx(conn_idx)
        if dev:
            dev.pending_events_clear_handles()
            evt = BleEventGapDisconnected()
            evt.conn_idx = conn_idx
            evt.reason = reason  # TODO BLE_HCI_ERROR and CO_ERROR not one to one. Will throw value error if not valid BLE_HCI_ERROR?

            # TODO
            # Need to notify L2CAP handler so it can 'deallocate' all channels for the given conn_idx */
            # ble_mgr_l2cap_disconnect_ind(conn_idx);

            evt.address = dev.addr

            # For bonded device we only need to remove non-persistent app_values and mark device as not
            # connected; otherwise remove device from storage
            if dev.bonded:
                dev.connected = False
                dev.conn_idx = BLE_CONN_IDX_INVALID
                dev.updating = False
                dev.sec_level = GAP_SEC_LEVEL.GAP_SEC_LEVEL_1
                dev.sec_level_req = GAP_SEC_LEVEL.GAP_SEC_LEVEL_1
                dev.discon_reason = 0
                dev.app_value_remove_not_persistent()
            else:
                self._stored_device_list.remove(dev)

            self._wait_queue_flush(conn_idx)
            # if (dg_configBLE_SKIP_LATENCY_API == 1)
            # Clear skip slave latency setting
            # ble_mgr_skip_latency_set(conn_idx, false);
            # endif /* (dg_configBLE_SKIP_LATENCY_API == 1) */

            self._mgr_event_queue_send(evt)

    def _connect_cmp_evt_handler(self, gtl: GapmCmpEvt):

        self.dev_params.connecting = False

        if gtl.parameters.status == HOST_STACK_ERROR_CODE.GAP_ERR_NO_ERROR:
            dev = self._stored_device_list.find_device_by_connenting()
            if dev:
                dev.connecting = False
                if not dev.bonded:
                    self._stored_device_list.remove_device(dev)

        evt = BleEventGapConnectionCompleted()

        match gtl.parameters.status:
            case HOST_STACK_ERROR_CODE.GAP_ERR_NO_ERROR:
                evt.status = BLE_ERROR.BLE_STATUS_OK
            case HOST_STACK_ERROR_CODE.GAP_ERR_CANCELED:
                evt.status = BLE_ERROR.BLE_ERROR_NOT_ALLOWED
            case HOST_STACK_ERROR_CODE.GAP_ERR_INVALID_PARAM:
                evt.status = BLE_ERROR.BLE_ERROR_INVALID_PARAM
            case HOST_STACK_ERROR_CODE.GAP_ERR_NOT_SUPPORTED \
                    | HOST_STACK_ERROR_CODE.GAP_ERR_PRIVACY_CFG_PB:

                evt.status = BLE_ERROR.BLE_ERROR_NOT_SUPPORTED

            case HOST_STACK_ERROR_CODE.LL_ERR_UNSPECIFIED_ERROR:
                evt.status = BLE_ERROR.BLE_ERROR_INS_BANDWIDTH
            case _:
                print(f"BleManagerGap._connect_cmp_evt_handler. gtl.status = {hex(gtl.parameters.status)}")
                # evt.status = gtl.parameters.status  # TODO this throws a ValueError if not a valid BLE_ERROR
                # need to be able to set a BLE_ERROR that is not defined. Could make a LittleEndianStructure

                evt.status = BLE_ERROR.BLE_ERROR_FAILED

        self._mgr_event_queue_send(evt)

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

    def _get_peer_features(self, conn_idx: int):
        gtl = GapcGetInfoCmd(conidx=conn_idx)
        gtl.parameters.operation = GAPC_OPERATION.GAPC_GET_PEER_FEATURES
        self._adapter_command_queue_send(gtl)

    def _get_peer_version(self, conn_idx: int):
        gtl = GapcGetInfoCmd(conidx=conn_idx)
        gtl.parameters.operation = GAPC_OPERATION.GAPC_GET_PEER_VERSION
        self._adapter_command_queue_send(gtl)

    def _io_cap_to_gtl(self, io_cap: GAP_IO_CAPABILITIES):

        match io_cap:
            case GAP_IO_CAPABILITIES.GAP_IO_CAP_DISP_ONLY:
                gtl_io_cap = GAP_IO_CAP.GAP_IO_CAP_DISPLAY_ONLY
            case GAP_IO_CAPABILITIES.GAP_IO_CAP_DISP_YES_NO:
                gtl_io_cap = GAP_IO_CAP.GAP_IO_CAP_DISPLAY_YES_NO
            case GAP_IO_CAPABILITIES.GAP_IO_CAP_KEYBOARD_ONLY:
                gtl_io_cap = GAP_IO_CAP.GAP_IO_CAP_KB_ONLY
            case GAP_IO_CAPABILITIES.GAP_IO_CAP_NO_INPUT_OUTPUT:
                gtl_io_cap = GAP_IO_CAP.GAP_IO_CAP_NO_INPUT_NO_OUTPUT
            case GAP_IO_CAPABILITIES.GAP_IO_CAP_KEYBOARD_DISP:
                gtl_io_cap = GAP_IO_CAP.GAP_IO_CAP_KB_DISPLAY
            case _:
                gtl_io_cap = GAP_IO_CAP.GAP_IO_CAP_NO_INPUT_NO_OUTPUT
        return gtl_io_cap

    def _max_bonded_reached(self):
        return self._stored_device_list.count_bonded() >= BLE_GAP_MAX_BONDED

    def _resolve_address_from_connected_evt(self, evt: GapcConnectionReqInd, param: None):
        # TODO 
        # Check if peer's address is random
        if evt.parameters.peer_addr_type != BLE_ADDR_TYPE.PRIVATE_ADDRESS:
            return False

        # Check if peer's address is resolvable
        if evt.parameters.peer_addr.addr[5] & 0xC0 != 0x40:
            return False

        # TODO gtl message
        # gtl = GapmResolvAddrCmd
        return False

    def _sec_req_to_gtl(self, sec_level: GAP_SEC_LEVEL):
        gtl_sec_req = GAP_SEC_REQ.GAP_NO_SEC
        match sec_level:
            case GAP_SEC_LEVEL.GAP_SEC_LEVEL_4:
                gtl_sec_req = GAP_SEC_REQ.GAP_SEC1_SEC_PAIR_ENC
            case GAP_SEC_LEVEL.GAP_SEC_LEVEL_3:
                gtl_sec_req = GAP_SEC_REQ.GAP_SEC1_AUTH_PAIR_ENC
            case GAP_SEC_LEVEL.GAP_SEC_LEVEL_2:
                gtl_sec_req = GAP_SEC_REQ.GAP_SEC1_NOAUTH_PAIR_ENC
            case GAP_SEC_LEVEL.GAP_SEC_LEVEL_1:
                gtl_sec_req = GAP_SEC_REQ.GAP_NO_SEC

        return gtl_sec_req

    def _send_bond_cmd(self,
                       conn_idx: int,
                       io_cap: GAP_IO_CAPABILITIES,
                       bond: bool,
                       mitm: bool,
                       secure: bool):

        gtl = GapcBondCmd(conidx=conn_idx)
        gtl.parameters.pairing.iocap = self._io_cap_to_gtl(io_cap)
        gtl.parameters.pairing.oob = GAP_OOB.GAP_OOB_AUTH_DATA_NOT_PRESENT
        gtl.parameters.pairing.auth = GAP_AUTH_MASK.GAP_AUTH_BOND if bond else GAP_AUTH_MASK.GAP_AUTH_NONE
        gtl.parameters.pairing.auth |= GAP_AUTH_MASK.GAP_AUTH_MITM if mitm else GAP_AUTH_MASK.GAP_AUTH_NONE
        gtl.parameters.pairing.auth |= GAP_AUTH_MASK.GAP_AUTH_SEC if secure else GAP_AUTH_MASK.GAP_AUTH_NONE
        gtl.parameters.pairing.key_size = BLE_ENC_KEY_SIZE_MAX
        gtl.parameters.pairing.ikey_dist = dg_configBLE_PAIR_INIT_KEY_DIST
        gtl.parameters.pairing.rkey_dist = dg_configBLE_PAIR_RESP_KEY_DIST

        dev = self._stored_device_list.find_device_by_conn_idx(conn_idx)
        if not dev:
            print("_send_bond_cmd no device found")
            gtl.parameters.pairing.sec_req = GAP_SEC_REQ.GAP_NO_SEC
        else:
            gtl.parameters.pairing.sec_req = self._sec_req_to_gtl(dev.sec_level_req)

        print(f"_send_bond_command. io_cap in={io_cap}. gtl.io_cap={gtl.parameters.pairing.iocap}, gtl.auth={gtl.parameters.pairing.auth}")
        self._adapter_command_queue_send(gtl)

    def _send_security_req(self,
                           conn_idx: int,
                           bond: bool,
                           mitm: bool,
                           secure: bool):

        gtl = GapcSecurityCmd(conidx=conn_idx)
        gtl.parameters.auth = GAP_AUTH_MASK.GAP_AUTH_BOND if bond else GAP_AUTH_MASK.GAP_AUTH_NONE
        gtl.parameters.auth |= GAP_AUTH_MASK.GAP_AUTH_MITM if mitm else GAP_AUTH_MASK.GAP_AUTH_NONE
        gtl.parameters.auth |= GAP_AUTH_MASK.GAP_AUTH_SEC if secure else GAP_AUTH_MASK.GAP_AUTH_NONE

        self._adapter_command_queue_send(gtl)

    def _scan_cmp_evt_handler(self, gtl: GapmCmpEvt) -> None:

        evt = BleEventGapScanCompleted()
        self.dev_params.scanning = False

        match gtl.parameters.operation:
            case GAPM_OPERATION.GAPM_SCAN_ACTIVE:
                evt.scan_type = GAP_SCAN_TYPE.GAP_SCAN_ACTIVE
            case GAPM_OPERATION.GAPM_SCAN_PASSIVE:
                evt.scan_type = GAP_SCAN_TYPE.GAP_SCAN_PASSIVE

        match gtl.parameters.status:
            case HOST_STACK_ERROR_CODE.GAP_ERR_NO_ERROR:
                evt.status = BLE_ERROR.BLE_STATUS_OK
            case HOST_STACK_ERROR_CODE.GAP_ERR_CANCELED:
                evt.status = BLE_ERROR.BLE_ERROR_CANCELED
            case HOST_STACK_ERROR_CODE.GAP_ERR_INVALID_PARAM:
                evt.status = BLE_ERROR.BLE_ERROR_INVALID_PARAM
            case HOST_STACK_ERROR_CODE.GAP_ERR_NOT_SUPPORTED \
                    | HOST_STACK_ERROR_CODE.GAP_ERR_PRIVACY_CFG_PB:

                evt.status = BLE_ERROR.BLE_ERROR_NOT_SUPPORTED

            case HOST_STACK_ERROR_CODE.GAP_ERR_TIMEOUT:
                evt.status = BLE_ERROR.BLE_ERROR_TIMEOUT
            case HOST_STACK_ERROR_CODE.GAP_ERR_COMMAND_DISALLOWED:
                evt.status = BLE_ERROR.BLE_ERROR_NOT_ALLOWED
            case _:
                evt.status = gtl.parameters.status

        self._mgr_event_queue_send(evt)

    def _send_disconncet_cmd(self, conn_idx: int, reason: BLE_HCI_ERROR) -> None:
        gtl = GapcDisconnectCmd(conidx=conn_idx)
        gtl.parameters.reason = CO_ERROR(reason)
        self._adapter_command_queue_send(gtl)

    def _send_gapm_cancel_cmd(self, operation: GAPM_OPERATION = GAPM_OPERATION.GAPM_CANCEL) -> None:

        gtl = GapmCancelCmd()  # TODO  RWBLE >= 9.0 has additiononal cancel commands
        self._adapter_command_queue_send(gtl)

    def _send_sec_level_changed_evt(self, conn_idx: int, sec_level: GAP_AUTH_MASK):
        evt = BleEventGapSecLevelChanged()
        evt.conn_idx = conn_idx
        evt.level = sec_level
        self._mgr_event_queue_send(evt)

        # if BLE_SSP_DEBUG  # TODO not sure what this is
        # /* Also send the LTK */
        # @ send_ltk_evt(conn_idx);
        # endif

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

    def adv_report_evt_handler(self, gtl: GapmAdvReportInd) -> None:
        evt = BleEventGapAdvReport()
        # TODO is there an enum BleEventGapAdvReport.type?
        evt.type = gtl.parameters.report.evt_type
        evt.rssi = (gtl.parameters.report.rssi & 0x7F)
        evt.rssi = (-1 * evt.rssi) if (gtl.parameters.report.rssi & 0x80) else evt.rssi
        # if (dg_configBLE_PRIVACY_1_2 == 1)
        # Mask the flag indicating that the address was resolved by the controller */
        # evt->address.addr_type = gevt->report.adv_addr_type & 0x01;
        # else

        evt.address.addr_type = BLE_ADDR_TYPE(gtl.parameters.report.adv_addr_type)
        # endif /* (dg_configBLE_PRIVACY_1_2 == 1) */
        evt.address.addr = bytes(gtl.parameters.report.adv_addr.addr)
        evt.length = gtl.parameters.report.data_len
        evt.data = bytes(gtl.parameters.report.data[:evt.length])

        # evt.data = gtl.parameters.report.data[:gtl.parameters.report.data_len]

        self._mgr_event_queue_send(evt)

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
            case BLE_OWN_ADDR_TYPE.PUBLIC_STATIC_ADDRESS \
                    | BLE_OWN_ADDR_TYPE.PRIVATE_STATIC_ADDRESS:

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

    def bond_ind_evt_handler(self, gtl: GapcBondInd):
        print("bond_ind_evt_handler")
        match gtl.parameters.info:
            case GAPC_BOND.GAPC_PAIRING_SUCCEED:
                evt = BleEventGapPairCompleted()
                evt.conn_idx = self._task_to_connidx(gtl.src_id)
                evt.status = BLE_ERROR.BLE_STATUS_OK
                evt.bond = bool(gtl.parameters.data.auth & GAP_AUTH_MASK.GAP_AUTH_BOND)
                evt.mitm = bool(gtl.parameters.data.auth & GAP_AUTH_MASK.GAP_AUTH_MITM)

                dev = self._stored_device_list.find_device_by_conn_idx(evt.conn_idx)
                if dev:
                    dev.paired = True
                    dev.bonded = evt.bond
                    dev.encrypted = True
                    dev.mitm = evt.mitm
                    if dg_configBLE_SECURE_CONNECTIONS == 1:
                        dev.secure = True if (gtl.parameters.data.auth & GAP_AUTH_MASK.GAP_AUTH_SEC) else False

                    sec_level = self._auth_to_sec_level(gtl.parameters.data.auth, dev.remote_ltk.key_size)
                    if dev.sec_level != sec_level:
                        dev.sec_level = sec_level
                        self._send_sec_level_changed_evt(evt.conn_idx, sec_level)

                    if dev.bonded:
                        self._stored_device_list.move_to_front(dev)  # TODO just to access quicker??

                # TODO Privacy
                # if (dg_configBLE_PRIVACY_1_2 == 1):
                #    if self.dev_params.own_addr.addr_type == BLE_OWN_ADDR_TYPE.PRIVATE_CNTL:
                #        self.dev_params.prev_privacy_operation = BLE_MGR_RAL_OP_NONE

                # storage_mark_dirty(true); # TODO storage handling

                self._mgr_event_queue_send(evt)

            case GAPC_BOND.GAPC_PAIRING_FAILED:

                evt = BleEventGapPairCompleted()

                conn_idx = self._task_to_connidx(gtl.src_id)
                if dg_configBLE_SECURE_CONNECTIONS == 1:

                    dev = self._stored_device_list.find_device_by_conn_idx(conn_idx)
                    if dev:
                        dev.secure = False
                    # storage_mark_dirty(true); # TODO

                evt.conn_idx = conn_idx

                match gtl.parameters.data.reason:
                    case HOST_STACK_ERROR_CODE.SMP_ERROR_REM_PAIRING_NOT_SUPP:
                        evt.status = BLE_ERROR.BLE_ERROR_NOT_SUPPORTED_BY_PEER
                    case (HOST_STACK_ERROR_CODE.SMP_ERROR_REM_UNSPECIFIED_REASON
                            | HOST_STACK_ERROR_CODE.SMP_ERROR_LOC_UNSPECIFIED_REASON):

                        evt.status = BLE_ERROR.BLE_ERROR_FAILED
                    # case HOST_STACK_ERROR_CODE.SMP_ERROR_TIMEOUT:  # TODO additional SMP ERROR code sefined in smp_common.h
                    #    evt.status = BLE_ERROR.BLE_ERROR_TIMEOUT
                    case _:
                    # evt.status = gtl.parameters.data.reason # TODO will throw error if not a defined BLE_ERROR?
                        evt.status = BLE_ERROR.BLE_ERROR_FAILED

                evt.bond = False
                evt.mitm = False

                self._mgr_event_queue_send(evt)

            case GAPC_BOND.GAPC_LTK_EXCH:
                conn_idx = self._task_to_connidx(gtl.src_id)
                dev = self._stored_device_list.find_device_by_conn_idx(conn_idx)
                if dev:

                    dev.remote_ltk.key_size = gtl.parameters.data.ltk
                    for i in range(0, RAND_NB_LEN):
                        dev.remote_ltk.rand |= gtl.parameters.data.ltk.randnb.nb[i] << i
                    dev.remote_ltk.ediv = gtl.parameters.data.ltk.ediv
                    dev.remote_ltk.key = bytes(gtl.parameters.data.ltk.ltk.key[:])

                    # storage_mark_dirty(false); # TODO 

            case GAPC_BOND.GAPC_CSRK_EXCH:
                conn_idx = self._task_to_connidx(gtl.src_id)
                dev = self._stored_device_list.find_device_by_conn_idx(conn_idx)
                if dev:

                    dev.remote_csrk.key = bytes(gtl.parameters.data.csrk.key[:])
                    dev.remote_csrk.sign_cnt = 0

                    # storage_mark_dirty(false); # TODO

            case GAPC_BOND.GAPC_IRK_EXCH:

                conn_idx = self._task_to_connidx(gtl.src_id)
                dev = self._stored_device_list.find_device_by_conn_idx(conn_idx)
                if dev:
                    addr = BdAddress()
                    addr.addr_type = gtl.parameters.data.irk.addr.addr_type
                    addr.addr = bytes(gtl.parameters.data.irk.addr.addr.addr[:])

                    old_dev = self._stored_device_list.find_device_by_address(addr, False)
                    while (old_dev and old_dev != dev):

                        self._stored_device_list.remove(old_dev)
                        old_dev = self._stored_device_list.find_device_by_address(addr, False)

                    evt = BleEventGapAddressResolved()
                    dev.irk.key = bytes(gtl.parameters.data.irk.irk.key[:])
                    dev.addr.addr_type = gtl.parameters.data.irk.addr.addr_type
                    dev.addr = addr
                    evt.resolved_address = dev.addr
                    evt.conn_idx = conn_idx
                    self._mgr_event_queue_send(evt)

                    # storage_mark_dirty(false); # TODO

    def bond_req_evt_handler(self, gtl: GapcBondReqInd):

        match gtl.parameters.request:
            case GAPC_BOND.GAPC_PAIRING_REQ:
                print(f"bond_req_evt_handler GAPC_BOND.GAPC_PAIRING_REQ. auth_req={gtl.parameters.data.auth_req} " +
                      f"bond={bool(gtl.parameters.data.auth_req & GAP_AUTH_MASK.GAP_AUTH_BOND) } " +
                      f"sec={bool(gtl.parameters.data.auth_req & GAP_AUTH_MASK.GAP_AUTH_SEC)}")
                evt = BleEventGapPairReq()
                evt.conn_idx = self._task_to_connidx(gtl.src_id)
                evt.bond = bool(gtl.parameters.data.auth_req & GAP_AUTH_MASK.GAP_AUTH_BOND)

                if (dg_configBLE_SECURE_CONNECTIONS == 1):
                    if gtl.parameters.data.auth_req & GAP_AUTH_MASK.GAP_AUTH_SEC:
                        dev = self._stored_device_list.find_device_by_conn_idx(evt.conn_idx)
                        if dev:
                            dev.secure = True

                self._mgr_event_queue_send(evt)

            case GAPC_BOND.GAPC_LTK_EXCH:
                print("bond_req_evt_handler GAPC_BOND.GAPC_LTK_EXCH")
                cfm = GapcBondCfm()
                cfm.parameters.accept = 0x01
                cfm.parameters.request = GAPC_BOND.GAPC_LTK_EXCH
                cfm.parameters.data.ltk.ediv = secrets.randbits(16)
                cfm.parameters.data.ltk.key_size = gtl.parameters.data.key_size

                for i in range(0, RAND_NB_LEN):
                    cfm.parameters.data.ltk.randnb.nb[i] = secrets.randbits(8)

                for i in range(0, gtl.parameters.data.key_size):
                    cfm.parameters.data.ltk.ltk.key[i] = secrets.randbits(8)

                conn_idx = self._task_to_connidx(gtl.src_id)
                dev = self._stored_device_list.find_device_by_conn_idx(conn_idx)

                if dev:
                    # dev.ltk = cfm.parameters.data.ltk
                    dev.ltk.key_size = cfm.parameters.data.ltk.key_size

                    dev.ltk.rand = 0
                    for i in range(0, RAND_NB_LEN):
                        dev.ltk.rand |= cfm.parameters.data.ltk.randnb.nb[i] << i

                    dev.ltk.ediv = cfm.parameters.data.ltk.ediv
                    dev.ltk.key = bytes(cfm.parameters.data.ltk.ltk.key[:])
                    # TODO storage_mark_dirty(false)

                self._adapter_command_queue_send(cfm)

            case GAPC_BOND.GAPC_CSRK_EXCH:
                print("bond_req_evt_handler GAPC_BOND.GAPC_CSRK_EXCH")
                cfm = GapcBondCfm()
                cfm.parameters.accept = 0x01
                cfm.parameters.request = GAPC_BOND.GAPC_CSRK_EXCH

                for i in range(0, KEY_LEN):
                    cfm.parameters.data.csrk.key[i] = secrets.randbits(8)

                conn_idx = self._task_to_connidx(gtl.src_id)
                dev = self._stored_device_list.find_device_by_conn_idx(conn_idx)
                if dev:
                    dev.csrk.key = bytes(cfm.parameters.data.csrk.key)
                    dev.csrk.sign_cnt = 0
                    #  TODO storage_mark_dirty(false)

                self._adapter_command_queue_send(cfm)

            case GAPC_BOND.GAPC_TK_EXCH:
                print(f"bond_req_evt_handler GAPC_BOND.GAPC_TK_EXCH. tk_type={gtl.parameters.data.tk_type}")
                if gtl.parameters.data.tk_type == GAP_TK_TYPE.GAP_TK_DISPLAY:
                    cfm = GapcBondCfm()
                    cfm.parameters.accept = 0x01
                    cfm.parameters.request = GAPC_BOND.GAPC_TK_EXCH
                    passkey = secrets.randbits(32) % 1000000

                    cfm.parameters.data.tk.key[0] = passkey & 0xFF
                    cfm.parameters.data.tk.key[1] = (passkey >> 8) & 0xFF
                    cfm.parameters.data.tk.key[2] = (passkey >> 16) & 0xFF
                    cfm.parameters.data.tk.key[3] = (passkey >> 24) & 0xFF

                    self._adapter_command_queue_send(cfm)

                    evt = BleEventGapPasskeyNotify()
                    evt.conn_idx = self._task_to_connidx(gtl.src_id)
                    evt.passkey = passkey

                    self._mgr_event_queue_send(evt)

                elif gtl.parameters.data.tk_type == GAP_TK_TYPE.GAP_TK_KEY_ENTRY:
                    evt = BleEventGapPasskeyNotify()
                    evt.conn_idx = self._task_to_connidx(gtl.src_id)
                    self._mgr_event_queue_send(evt)

                elif (gtl.parameters.data.tk_type == GAP_TK_TYPE.GAP_TK_KEY_CONFIRM
                        and dg_configBLE_SECURE_CONNECTIONS == 1):

                    evt = BleEventGapNumericRequest()
                    evt.conn_idx = self._task_to_connidx(gtl.src_id)
                    evt.num_key = gtl.parameters.tk.key[0]
                    evt.num_key += gtl.parameters.tk.key[1] << 8
                    evt.num_key += gtl.parameters.tk.key[2] << 16
                    evt.num_key += gtl.parameters.tk.key[3] << 24
                    evt.num_key %= 1000000

                    self._mgr_event_queue_send(evt)

    def conn_param_update(self, command: BleMgrGapConnParamUpdateCmd):
        response = BleMgrGapConnParamUpdateRsp(BLE_ERROR.BLE_ERROR_FAILED)

        dev = self._stored_device_list.find_device_by_conn_idx(command.conn_idx)
        if not dev:
            response.status = BLE_ERROR.BLE_ERROR_NOT_CONNECTED
        elif dev.updating:
            response.status = BLE_ERROR.BLE_ERROR_IN_PROGRESS
        else:
            gtl = GapcParamUpdateCmd(conidx=command.conn_idx)
            gtl.parameters.operation = GAPC_OPERATION.GAPC_UPDATE_PARAMS
            gtl.parameters.intv_min = command.conn_params.interval_min
            gtl.parameters.intv_max = command.conn_params.interval_max
            gtl.parameters.latency = command.conn_params.slave_latency
            gtl.parameters.time_out = command.conn_params.sup_timeout

            if dev.master:
                gtl.parameters.ce_len_min = dev.ce_len_min
                gtl.parameters.ce_len_max = dev.ce_len_max

            dev.updating = True
            self._adapter_command_queue_send(gtl)
            response.status = BLE_ERROR.BLE_STATUS_OK

        self._mgr_response_queue_send(response)

    def conn_param_update_reply_cmd_handler(self, command: BleMgrGapConnParamUpdateReplyCmd):
        response = BleMgrGapConnParamUpdateReplyRsp(BLE_ERROR.BLE_ERROR_FAILED)
        dev = self._stored_device_list.find_device_by_conn_idx(command.conn_idx)

        if not dev:
            response.status = BLE_ERROR.BLE_ERROR_NOT_CONNECTED
        else:
            gtl = GapcParamUpdateCfm(conidx=command.conn_idx)
            gtl.parameters.accept = command.accept
            if command.accept and dev.master:
                gtl.parameters.ce_len_min = dev.ce_len_min
                gtl.parameters.ce_len_max = dev.ce_len_max
            dev.updating = False
            self._adapter_command_queue_send(gtl)
            response.status = BLE_ERROR.BLE_STATUS_OK

        self._mgr_response_queue_send(response)

    def conn_param_updated_evt_handler(self, gtl: GapcParamUpdatedInd):
        evt = BleEventGapConnParamUpdated()
        evt.conn_idx = self._task_to_connidx(gtl.src_id)
        evt.conn_params.interval_min = gtl.parameters.con_interval
        evt.conn_params.interval_max = gtl.parameters.con_interval
        evt.conn_params.slave_latency = gtl.parameters.con_latency
        evt.conn_params.sup_timeout = gtl.parameters.sup_to
        self._mgr_event_queue_send(evt)

    def conn_param_update_req_evt_handler(self, gtl: GapcParamUpdateReqInd):
        evt = BleEventGapConnParamUpdateReq()
        conn_idx = self._task_to_connidx(gtl.src_id)

        dev = self._stored_device_list.find_device_by_conn_idx(conn_idx)
        if dev:
            # Set the updating flag until application replies to the update request
            dev.updating = True

        evt.conn_idx = conn_idx
        evt.conn_params.interval_min = gtl.parameters.intv_min
        evt.conn_params.interval_max = gtl.parameters.intv_max
        evt.conn_params.slave_latency = gtl.parameters.latency
        evt.conn_params.sup_timeout = gtl.parameters.time_out

        self._mgr_event_queue_send(evt)

    # TODO need to test
    def connect_cancel_cmd_handler(self, command: BleMgrGapConnectCancelCmd):
        response = BleMgrGapConnectCancelRsp(BLE_ERROR.BLE_ERROR_FAILED)
        if not self.dev_params.connecting:
            response.status = BLE_ERROR.BLE_ERROR_NOT_ALLOWED
        else:
            # TODO support for additional cancel commands for RWBLE >= 9
            # send_gapm_cancel_cmd(GAPM_CANCEL_CONNECTION)
            self._send_gapm_cancel_cmd()
            response.status = BLE_ERROR.BLE_STATUS_OK

        self._mgr_response_queue_send(response)

    def connect_cmd_handler(self, command: BleMgrGapConnectCmd):
        # TODO handle privacy
        # if (dg_configBLE_PRIVACY_1_2 == 1)
        # ble_mgr_gap_ral_sync(ble_mgr_gap_connect_cmd_exec, param);
        # else
        # ble_mgr_gap_connect_cmd_exec(param); # TODO This function implemented below. Separate func?
        # endif
        response = BleMgrGapConnectRsp(BLE_ERROR.BLE_ERROR_FAILED)

        dev = self._stored_device_list.find_device_by_connenting()
        if dev:
            response = BLE_ERROR.BLE_ERROR_BUSY
        else:
            dev = self._stored_device_list.find_device_by_address(command.peer_addr, True)
            if dev:
                if dev.connected:
                    response = BLE_ERROR.BLE_ERROR_ALREADY_DONE
                else:
                    gtl = GapmStartConnectionCmd()
                    gtl.parameters.op.code = GAPM_OPERATION.GAPM_CONNECTION_DIRECT
                    match self.dev_params.own_addr.addr_type:
                        case BLE_OWN_ADDR_TYPE.PRIVATE_STATIC_ADDRESS \
                                | BLE_OWN_ADDR_TYPE.PUBLIC_STATIC_ADDRESS:

                            gtl.parameters.op.addr_src = GAPM_OWN_ADDR.GAPM_STATIC_ADDR

                        case BLE_OWN_ADDR_TYPE.PRIVATE_RANDOM_RESOLVABLE_ADDRESS \
                                | BLE_OWN_ADDR_TYPE.PRIVATE_CNTL:

                            gtl.parameters.op.addr_src = GAPM_OWN_ADDR.GAPM_GEN_RSLV_ADDR

                        case BLE_OWN_ADDR_TYPE.PRIVATE_RANDOM_NONRESOLVABLE_ADDRESS:
                            gtl.parameters.op.addr_src = GAPM_OWN_ADDR.GAPM_GEN_NON_RSLV_ADDR

                    gtl.parameters.scan_interval = self.dev_params.scan_params.interval
                    gtl.parameters.scan_window = self.dev_params.scan_params.window
                    gtl.parameters.con_intv_min = command.conn_params.interval_min
                    gtl.parameters.con_intv_max = command.conn_params.interval_max
                    gtl.parameters.con_latency = command.conn_params.slave_latency
                    gtl.parameters.superv_to = command.conn_params.sup_timeout
                    gtl.parameters.con_latency = command.conn_params.slave_latency
                    gtl.parameters.ce_len_min = command.ce_len_min if command.ce_len_min else 8  # TODO implement ifdef
                    gtl.parameters.ce_len_max = command.ce_len_max if command.ce_len_max else 8
                    gtl.parameters.nb_peers = 1
                    gtl.parameters.peers = (gap_bdaddr * gtl.parameters.nb_peers)()
                    gtl.parameters.peers[0].addr_type = command.peer_addr.addr_type
                    gtl.parameters.peers[0].addr.addr[:] = command.peer_addr.addr

                    dev.connecting = True
                    dev.ce_len_min = gtl.parameters.ce_len_min
                    dev.ce_len_max = gtl.parameters.ce_len_max

                    self._adapter_command_queue_send(gtl)
                    response.status = BLE_ERROR.BLE_STATUS_OK

        self._mgr_response_queue_send(response)

    def connected_evt_handler(self, gtl: GapcConnectionReqInd):
        evt = BleEventGapConnected()
        evt.conn_idx = self._task_to_connidx(gtl.src_id)
        evt.own_addr.addr_type = self.dev_params.own_addr.addr_type
        evt.own_addr.addr = self.dev_params.own_addr.addr
        # if (dg_configBLE_PRIVACY_1_2 == 1)
        # evt.peer_address.addr_type = gtl.parameters.peer_addr_type & 0x01
        # else
        evt.peer_address.addr_type = BLE_ADDR_TYPE(gtl.parameters.peer_addr_type)
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

        if (dg_configBLE_CENTRAL == 1):  # TODO what is best way to handle these config params
            if dev.master:
                # Initiate a Version Exchange
                self._get_peer_version(evt.conn_idx)

        # if (dg_configBLE_PRIVACY_1_2 == 1)
        if self.dev_params.own_addr.addr_type != BLE_OWN_ADDR_TYPE.PRIVATE_CNTL:
            # endif /* (dg_configBLE_PRIVACY_1_2 == 1) */
            pass  # TODO needs to be same as resolve addr here

        if self._resolve_address_from_connected_evt(gtl, evt):
            # TODO
            # dev.resolving = True  # Note passed in gtl instead of gtl.params
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

    def disconnect_cmd_handler(self, command: BleMgrGapDisconnectCmd) -> None:
        response = BleMgrGapDisconnectRsp(BLE_ERROR.BLE_ERROR_FAILED)

        dev = self._stored_device_list.find_device_by_conn_idx(command.conn_idx)

        if not dev:
            response.status = BLE_ERROR.BLE_ERROR_NOT_CONNECTED
        else:
            self._send_disconncet_cmd(command.conn_idx, command.reason)
            response.status = BLE_ERROR.BLE_STATUS_OK

        self._mgr_response_queue_send(response)

    def disconnected_evt_handler(self, gtl: GapcDisconnectInd) -> None:

        conn_idx = self._task_to_connidx(gtl.src_id)
        dev: StoredDevice = self._stored_device_list.find_device_by_conn_idx(conn_idx)

        if dev is not None:
            if dev.resolving:
                dev.discon_reason = gtl.parameters.reason
            else:
                self._conn_cleanup(conn_idx, gtl.parameters.reason)

    def gapc_cmp_evt_handler(self, gtl: GapcCmpEvt) -> bool:

        match gtl.parameters.operation:
            case GAPC_OPERATION.GAPC_DISCONNECT:
                self._cmp_disconnect_evt_handler(gtl)
            case GAPC_OPERATION.GAPC_UPDATE_PARAMS:
                self._cmp_update_params_evt_handler(gtl)
            case GAPC_OPERATION.GAPC_SET_LE_PKT_SIZE:
                # TODO should not return value
                return self._cmp_data_length_set_evt_handler(gtl)
            case (GAPC_OPERATION.GAPC_GET_PEER_VERSION
                    | GAPC_OPERATION.GAPC_GET_PEER_FEATURES
                    | GAPC_OPERATION.GAPC_GET_CON_RSSI
                    # | GAPC_OPERATION.GAPC_SET_TX_PWR
                    # | GAPC_OPERATION.GAPC_LE_RD_TX_PWR_LVL_ENH
                    # | GAPC_OPERATION.GAPC_LE_RD_REM_TX_PWR_LVL
                    # | GAPC_OPERATION.GAPC_LE_SET_PATH_LOSS_REPORT_PARAMS
                    # | GAPC_OPERATION.GAPC_LE_SET_PATH_LOSS_REPORT_EN
                    #  GAPC_OPERATION.GAPC_LE_SET_TX_PWR_REPORT_EN)
                  ):

                pass

            case GAPC_OPERATION.GAPC_BOND:
                self._cmp_bond_evt_handler(gtl)
            case GAPC_OPERATION.GAPC_ENCRYPT:
                pass
            case GAPC_OPERATION.GAPC_SECURITY_REQ:
                self._cmp_security_req_evt_handler(gtl)

            # case GAPC_OPERATION.GAPC_LE_CB_CONNECTION:  # TODO separate L2CAP Manager
            #   ble_mgr_gapc_cmp__le_cb_connection_evt_handler(gtl);

            case _:
                return False
        return True

    def gapm_cmp_evt_handler(self, gtl: GapmCmpEvt) -> bool:

        # TODO replace this with another dictionary??
        match gtl.parameters.operation:
            case GAPM_OPERATION.GAPM_ADV_NON_CONN \
                    | GAPM_OPERATION.GAPM_ADV_UNDIRECT \
                    | GAPM_OPERATION.GAPM_ADV_DIRECT \
                    | GAPM_OPERATION.GAPM_ADV_DIRECT_LDC:

                self._adv_cmp_evt_handler(gtl)

            case GAPM_OPERATION.GAPM_UPDATE_ADVERTISE_DATA:
                pass
            # case GAPM_OPERATION.GAPM_CANCEL_ADVERTISE: RWBLE >= 9
            #    pass

            case GAPM_OPERATION.GAPM_SCAN_ACTIVE \
                    | GAPM_OPERATION.GAPM_SCAN_PASSIVE:

                self._scan_cmp_evt_handler(gtl)

            case GAPM_OPERATION.GAPM_CONNECTION_DIRECT:
                self._connect_cmp_evt_handler(gtl)

            # case GAPM_OPERATION.GAPM_CANCEL_CONNECTION: RWBLE >= 9
            #    pass

            case GAPM_OPERATION.GAPM_SET_CHANNEL_MAP:
                pass
            case GAPM_OPERATION.GAPM_SET_SUGGESTED_DFLT_LE_DATA_LEN:
                # TODO should not return value
                return self._cmp_data_length_set_evt_handler(gtl)
            case GAPM_OPERATION.GAPM_RESOLV_ADDR:
                # TODO should not return value
                return self._cmp_address_resolve_evt_handler(gtl)
            case (GAPM_OPERATION.GAPM_RESET
                    | GAPM_OPERATION.GAPM_CANCEL
                    | GAPM_OPERATION.GAPM_SET_DEV_CONFIG
                    | GAPM_OPERATION.GAPM_SET_DEV_CONFIG
                    | GAPM_OPERATION.GAPM_GET_DEV_BDADDR
                    # | GAPM_OPERATION.GAPM_SET_TX_PW
                    # | GAPM_OPERATION.GAPM_LE_WR_RF_PATH_COMPENS
                    # | GAPM_OPERATION.GAPM_SET_ADV_PERMUTATION
                  ):

                pass

            case _:
                return False
        return True

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

    def numeric_reply_cmd_handler(self, command: BleMgrGapNumericReplyCmd):
        response = BleMgrGapNumericReplyRsp(BLE_ERROR.BLE_ERROR_FAILED)
        gtl = GapcBondCfm(conidx=command.conn_idx)
        gtl.parameters.request = GAPC_BOND.GAPC_TK_EXCH
        gtl.parameters.accept = command.accept
        self._adapter_command_queue_send(gtl)
        response.status = BLE_ERROR.BLE_STATUS_OK
        self._mgr_response_queue_send(response)

    def pair_cmd_handler(self, command: BleMgrGapPairCmd):
        print("pair_cmd_handler")
        response = BleMgrGapPairRsp(BLE_ERROR.BLE_ERROR_FAILED)

        secure = True if (dg_configBLE_SECURE_CONNECTIONS == 1) else False
        dev = self._stored_device_list.find_device_by_conn_idx(command.conn_idx)
        if not dev:
            response.status = BLE_ERROR.BLE_ERROR_NOT_CONNECTED
        else:
            if (not command.bond and (dev.paired or dev.bonded)):
                response.status = BLE_ERROR.BLE_ERROR_ALREADY_DONE
            else:
                # Don't exceed the max bonded devices threshold
                if (command.bond and not dev.bonded and self._max_bonded_reached()):
                    response.status = BLE_ERROR.BLE_ERROR_INS_RESOURCES

                mitm = False if self.dev_params.io_capabilities == GAP_IO_CAPABILITIES.GAP_IO_CAP_NO_INPUT_OUTPUT else True
                if dev.master:
                    if (dg_configBLE_CENTRAL == 1):
                        self._send_bond_cmd(command.conn_idx,
                                            self.dev_params.io_capabilities,
                                            command.bond,
                                            mitm,
                                            secure)
                        response.status = BLE_ERROR.BLE_STATUS_OK

                else:
                    if dg_configBLE_PERIPHERAL == 1:
                        if dev.security_req_pending:
                            response.status = BLE_ERROR.BLE_ERROR_IN_PROGRESS
                        else:
                            dev.security_req_pending = True
                            self._send_security_req(command.conn_idx,
                                                    command.bond,
                                                    mitm,
                                                    secure)
                            response.status = BLE_ERROR.BLE_STATUS_OK

        self._mgr_response_queue_send(response)

    def pair_reply_cmd_handler(self, command: BleMgrGapPairReplyCmd):
        print("pair_reply_cmd_handler")
        response = BleMgrGapPairReplyRsp(BLE_ERROR.BLE_ERROR_FAILED)

        dev = self._stored_device_list.find_device_by_conn_idx(command.conn_idx)
        if not dev:
            response.status = BLE_ERROR.BLE_ERROR_NOT_CONNECTED
        else:
            if (command.bond
                    and command.accept
                    and not dev.bonded
                    and self._max_bonded_reached()):

                response.status = BLE_ERROR.BLE_ERROR_INS_RESOURCES
            else:
                gtl = GapcBondCfm(conidx=command.conn_idx)
                gtl.parameters.request = GAPC_BOND.GAPC_PAIRING_RSP
                gtl.parameters.accept = command.accept

                if command.accept:
                    gtl.parameters.data.pairing_feat.auth = GAP_AUTH_MASK.GAP_AUTH_BOND if command.bond else GAP_AUTH_MASK.GAP_AUTH_NONE
                    if self.dev_params.io_capabilities != GAP_IO_CAPABILITIES.GAP_IO_CAP_NO_INPUT_OUTPUT:
                        gtl.parameters.data.pairing_feat.auth |= GAP_AUTH_MASK.GAP_AUTH_MITM
                    if dg_configBLE_SECURE_CONNECTIONS == 1:
                        gtl.parameters.data.pairing_feat.auth |= GAP_AUTH_MASK.GAP_AUTH_SEC

                    gtl.parameters.data.pairing_feat.oob = GAP_OOB.GAP_OOB_AUTH_DATA_NOT_PRESENT
                    gtl.parameters.data.pairing_feat.key_size = BLE_ENC_KEY_SIZE_MAX
                    gtl.parameters.data.pairing_feat.iocap = self._io_cap_to_gtl(self.dev_params.io_capabilities)
                    gtl.parameters.data.pairing_feat.ikey_dist = dg_configBLE_PAIR_INIT_KEY_DIST
                    gtl.parameters.data.pairing_feat.rkey_dist = dg_configBLE_PAIR_RESP_KEY_DIST
                    gtl.parameters.data.pairing_feat.sec_req = self._sec_req_to_gtl(dev.sec_level_req)

                print(f"pair_reply_cmd_handler. self.io_cap={self.dev_params.io_capabilities} io_cap={gtl.parameters.data.pairing_feat.iocap} pairing_feat.auth={gtl.parameters.data.pairing_feat.auth} "+
                      f"command.bond={command.bond}, sec={dg_configBLE_SECURE_CONNECTIONS}")
                self._adapter_command_queue_send(gtl)

        self._mgr_response_queue_send(response)

    def passkey_reply_cmd_handler(self, command: BleMgrGapPasskeyReplyCmd):
        print("passkey_reply_cmd_handler")
        response = BleMgrGapPasskeyReplyRsp(BLE_ERROR.BLE_ERROR_FAILED)

        gtl = GapcBondCfm(conidx=command.conn_idx)
        gtl.parameters.request = GAPC_BOND.GAPC_TK_EXCH
        gtl.parameters.accept = command.accept

        if command.accept:
            gtl.parameters.data.tk.key[0] = command.passkey & 0xFF
            gtl.parameters.data.tk.key[1] = (command.passkey >> 8) & 0xFF
            gtl.parameters.data.tk.key[2] = (command.passkey >> 16) & 0xFF
            gtl.parameters.data.tk.key[3] = (command.passkey >> 24) & 0xFF

        self._adapter_command_queue_send(gtl)
        response.status = BLE_ERROR.BLE_STATUS_OK
        self._mgr_response_queue_send(response)

    def peer_features_ind_evt_handler(self, gtl: GapcPeerFeaturesInd):
        evt = BleEventGapPeerFeatures()
        evt.conn_idx = self._task_to_connidx(gtl.src_id)
        evt.le_features = bytes(gtl.parameters.features[:])
        self._mgr_event_queue_send(evt)

        # TODO 
        '''
        if (dg_configBLE_DATA_LENGTH_RX_MAX > GAPM_LE_LENGTH_EXT_OCTETS_MIN
                or dg_configBLE_DATA_LENGTH_TX_MAX > GAPM_LE_LENGTH_EXT_OCTETS_MIN): 

                if gtl.parameters.features[0] & BLE_LE_LENGTH_FEATURE:
                    dev = self._stored_device_list.find_device_by_conn_idx(evt.conn_idx)
                    if dev and dev.master:
                        self._change_conn_data_length(evt.conn_idx, 
                                                      dg_configBLE_DATA_LENGTH_TX_MAX,
                                                      ble_data_length_to_time(dg_configBLE_DATA_LENGTH_TX_MAX))
        '''

    def peer_version_ind_evt_handler(self, gtl: GapcPeerVersionInd):
        evt = BleEventGapPeerVersion()
        evt.conn_idx = self._task_to_connidx(gtl.src_id)
        evt.lmp_version = gtl.parameters.lmp_vers
        evt.company_id = gtl.parameters.compid
        evt.lmp_subversion = gtl.parameters.lmp_subvers
        self._mgr_event_queue_send(evt)

        dev = self._stored_device_list.find_device_by_conn_idx(evt.conn_idx)
        if dev and dev.master:

            self._get_peer_features(evt.conn_idx)

    def role_set_cmd_handler(self, command: BleMgrGapRoleSetCmd):
        gtl = self._dev_params_to_gtl()
        gtl.parameters.role = self._ble_role_to_gtl_role(command.role)
        self._wait_queue_add(BLE_CONN_IDX_INVALID,
                             GAPM_MSG_ID.GAPM_CMP_EVT,
                             GAPM_OPERATION.GAPM_SET_DEV_CONFIG,
                             self._set_role_rsp,
                             command.role)

        self._adapter_command_queue_send(gtl)

    def scan_start_cmd_handler(self, command: BleMgrGapScanStartCmd):
        # TODO handle privacy, just implementing ble_mgr_gap_scan_start_cmd_exec below
        # if (dg_configBLE_PRIVACY_1_2 == 1)
        # ble_mgr_gap_ral_sync(ble_mgr_gap_scan_start_cmd_exec, param);
        # else
        # ble_mgr_gap_scan_start_cmd_exec(param);
        # endif /* (dg_configBLE_PRIVACY_1_2 == 1) */
        response = BleMgrGapScanStartRsp(BLE_ERROR.BLE_ERROR_FAILED)

        if self.dev_params.scanning:
            response.status = BLE_ERROR.BLE_ERROR_IN_PROGRESS
        else:
            gtl = GapmStartScanCmd()

            match command.type:
                case GAP_SCAN_TYPE.GAP_SCAN_ACTIVE:
                    gtl.parameters.op.code = GAPM_OPERATION.GAPM_SCAN_ACTIVE
                case GAP_SCAN_TYPE.GAP_SCAN_PASSIVE:
                    gtl.parameters.op.code = GAPM_OPERATION.GAPM_SCAN_PASSIVE

            match self.dev_params.own_addr.addr_type:
                case BLE_OWN_ADDR_TYPE.PUBLIC_STATIC_ADDRESS \
                        | BLE_OWN_ADDR_TYPE.PRIVATE_STATIC_ADDRESS:

                    gtl.parameters.op.addr_src = GAPM_OWN_ADDR.GAPM_STATIC_ADDR

                case BLE_OWN_ADDR_TYPE.PRIVATE_RANDOM_RESOLVABLE_ADDRESS \
                        | BLE_OWN_ADDR_TYPE.PRIVATE_CNTL:

                    gtl.parameters.op.addr_src = GAPM_OWN_ADDR.GAPM_GEN_RSLV_ADDR

                case BLE_OWN_ADDR_TYPE.PRIVATE_RANDOM_NONRESOLVABLE_ADDRESS:
                    gtl.parameters.op.addr_src = GAPM_OWN_ADDR.GAPM_GEN_NON_RSLV_ADDR
                case _:
                    gtl.parameters.op.addr_src = GAPM_OWN_ADDR.GAPM_STATIC_ADDR

            gtl.parameters.interval = command.interval
            gtl.parameters.window = command.window
            gtl.parameters.mode = command.mode  # TODO GAP_SCAP_MOD enum redfine

            gtl.parameters.filt_policy = (SCAN_FILTER_POLICY.SCAN_ALLOW_ADV_WLST
                                          if command.filt_wlist
                                          else SCAN_FILTER_POLICY.SCAN_ALLOW_ADV_ALL)

            gtl.parameters.filter_duplic = (SCAN_DUP_FILTER_POLICY.SCAN_FILT_DUPLIC_EN
                                            if command.filt_dupl
                                            else SCAN_DUP_FILTER_POLICY.SCAN_FILT_DUPLIC_DIS)

            self.dev_params.scanning = True
            self._adapter_command_queue_send(gtl)
            response.status = BLE_ERROR.BLE_STATUS_OK

        self._mgr_response_queue_send(response)

    def set_io_cap(self, io_cap: GAP_IO_CAPABILITIES) -> BLE_ERROR:
        self.dev_params.io_capabilities = io_cap
        return BLE_ERROR.BLE_STATUS_OK


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

Unsure about these 4
void ble_mgr_gap_le_phy_ind_handler(ble_gtl_msg_t *gtl);
void ble_mgr_gap_le_rd_tx_pwr_lvl_enh_ind_handler(ble_gtl_msg_t *gtl);
void ble_mgr_gap_le_tx_pwr_lvl_report_ind_handler(ble_gtl_msg_t *gtl);
void ble_mgr_gap_le_path_loss_thres_ind_handler(ble_gtl_msg_t *gtl);
'''
