import asyncio
# from ctypes import c_uint16, c_uint8, Array
from enum import IntEnum, auto
from gtl_messages.gtl_message_base import GtlMessageBase
from gtl_messages.gtl_message_gapm import GapmSetDevConfigCmd, GapmStartAdvertiseCmd, GapmStartConnectionCmd  # GapmResetCmd
from gtl_messages.gtl_message_gapc import GapcConnectionCfm
# TODO perhaps these Gapm messages do not belong here
from gtl_messages.gtl_port.gapm_task import GAPM_MSG_ID, gapm_cmp_evt, GAPM_OPERATION  # gapm_set_dev_config_cmd, gapm_reset_cmd
from gtl_messages.gtl_port.gapc_task import GAPC_MSG_ID
# from gtl_messages.gtl_port.gattc_task import GATTC_MSG_ID
from gtl_messages.gtl_port.gap import GAP_ROLE
from BleDevParams import BleDevParamsDefault
from gtl_messages.gtl_port.rwble_hl_error import HOST_STACK_ERROR_CODE
from GtlWaitQueue import GtlWaitQueue  # GtlWaitQueueElement
from BleCommon import BLE_ERROR, BLE_MGR_CMD_CAT, BleManagerBase, BleMgrMsgBase, BLE_EVT_CAT  # BLE_STATUS
from BleGap import BLE_GAP_ROLE, BLE_GAP_CONN_MODE  # TODO dont like these files referencing eachother

# this is from ble_config.h
dg_configBLE_DATA_LENGTH_TX_MAX = (251)

class BleMgrGapAddressSetCmd(BleMgrMsgBase):
    def __init__(self, address, renew_dur) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ADDRESS_SET_CMD)


class BleMgrGapDeviceNameSetCmd(BleMgrMsgBase):
    def __init__(self, name, perm) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_DEVICE_NAME_SET_CMD)


class BleMgrGapAppearanceSetCmd(BleMgrMsgBase):
    def __init__(self, appearance, perm) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_APPEARANCE_SET_CMD)


class BleMgrGapPpcpSetCmd(BleMgrMsgBase):
    def __init__(self, gap_ppcp) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_PPCP_SET_CMD)


class BleMgrGapAdvStartCmd(BleMgrMsgBase):
    def __init__(self, adv_type: BLE_GAP_CONN_MODE = BLE_GAP_CONN_MODE.GAP_CONN_MODE_UNDIRECTED) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ADV_START_CMD)
        self.adv_type = adv_type  # TODO raise error on bad arg


class BleMgrGapAdvStopCmd(BleMgrMsgBase):
    def __init__(self) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ADV_STOP_CMD)


class BleMgrGapAdvDataSetCmd(BleMgrMsgBase):
    def __init__(self, adv_data_len, adv_data, scan_rsp_data_len, scan_rsp_data) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ADV_DATA_SET_CMD)


class BleMgrGapAdvSetPermIdCmd(BleMgrMsgBase):
    def __init__(self, permutation_idx) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ADV_SET_PERMUTATION_CMD)


class BleMgrGapScanStartCmd(BleMgrMsgBase):
    def __init__(self, type, mode, interval, window, filt_wlist, filt_dupl) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_SCAN_START_CMD)


class BleMgrGapScanStopCmd(BleMgrMsgBase):
    def __init__(self) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_SCAN_STOP_CMD)


class BleMgrGapConnectCmd(BleMgrMsgBase):
    def __init__(self, peer_addr, conn_params, ce_len_min, ce_len_max) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_CONNECT_CMD)


class BleMgrGapConnectCancelCmd(BleMgrMsgBase):
    def __init__(self) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_CONNECT_CANCEL_CMD)


class BleMgrGapDisconnectCmd(BleMgrMsgBase):
    def __init__(self, conn_idx, reason) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_DISCONNECT_CMD)


class BleMgrGapPeerVersionGetCmd(BleMgrMsgBase):
    def __init__(self, conn_idx) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_PEER_VERSION_GET_CMD)


class BleMgrGapPeerFeaturesGetCmd(BleMgrMsgBase):
    def __init__(self, conn_idx) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_PEER_FEATURES_GET_CMD)
        

class BleMgrGapConnRssiGetCmd(BleMgrMsgBase):
    def __init__(self, conn_idx) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_CONN_RSSI_GET_CMD)


class BleMgrGapRoleSetCmd(BleMgrMsgBase):
    def __init__(self, role: BLE_GAP_ROLE = BLE_GAP_ROLE.GAP_NO_ROLE) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ROLE_SET_CMD)
        self.role = role


class BleMgrGapMtuSizeSetCmd(BleMgrMsgBase):
    def __init__(self, mtu_size) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_MTU_SIZE_SET_CMD)


class BleMgrGapChannelMapSetCmd(BleMgrMsgBase):
    def __init__(self, channel_map) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_CHANNEL_MAP_SET_CMD)


class BleMgrGapConnParamUpdateCmd(BleMgrMsgBase):
    def __init__(self, conn_idx, conn_params) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_CONN_PARAM_UPDATE_CMD)


class BleMgrGapConnParamUpdateReplyCmd(BleMgrMsgBase):
    def __init__(self, conn_idx, accept) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_CONN_PARAM_UPDATE_REPLY_CMD)


class BleMgrGapPairCmd(BleMgrMsgBase):
    def __init__(self, conn_idx, bond) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_PAIR_CMD)


class BleMgrGapPairReplyCmd(BleMgrMsgBase):
    def __init__(self, conn_idx, accept, bond) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_PAIR_REPLY_CMD)


class BleMgrGapPasskeyReplyCmd(BleMgrMsgBase):
    def __init__(self, conn_idx, accept, passkey) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_PASSKEY_REPLY_CMD)


class BleMgrGapNumericReplyCmd(BleMgrMsgBase):
    def __init__(self, conn_idx, accept) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_NUMERIC_REPLY_CMD)


class BleMgrGapUnpairCmd(BleMgrMsgBase):
    def __init__(self, addr) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_UNPAIR_CMD)


class BleMgrGapSetSecLevelCmd(BleMgrMsgBase):
    def __init__(self, conn_idx, level) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_SET_SEC_LEVEL_CMD)


# TODO ble_mgr_gap_skip_latency_cmd_t 

class BleMgrGapDataLengthSetCmd(BleMgrMsgBase):
    def __init__(self, conn_idx, tx_length, tx_time) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_DATA_LENGTH_SET_CMD)


class BleMgrGapAddressResolveCmd(BleMgrMsgBase):
    def __init__(self, address) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ADDRESS_RESOLVE_CMD)


class BleMgrGapPhySetCmd(BleMgrMsgBase):
    def __init__(self, conn_idx, tx_phy, rx_phy) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_PHY_SET_CMD)


class BleMgrGapPhySetCmd(BleMgrMsgBase):
    def __init__(self, air_operation, tx_power) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_TX_POWER_SET_CMD)


class BleMgrGapConnTxPowerSetCmd(BleMgrMsgBase):
    def __init__(self, conn_idx, tx_power) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_CONN_TX_POWER_SET_CMD)


class BleMgrGapPhySetCmd(BleMgrMsgBase):
    def __init__(self, conn_idx, phy) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_LOCAL_TX_POWER_GET_CMD)


class BleMgrGapReadRemoteTxPowerLevelCmd(BleMgrMsgBase):
    def __init__(self, air_operation, phy) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_REMOTE_TX_POWER_GET_CMD)


class BleMgrGapSetPathLossReportParamsCmd(BleMgrMsgBase):
    def __init__(self, conn_idx, high_thres, high_hyst, low_thres, low_hyst, min_time_spent) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_PATH_LOSS_REPORT_PARAMS_SET_CMD)


class BleMgrGapSetPathLossReportEnableCmd(BleMgrMsgBase):
    def __init__(self, conn_idx, enable) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_PATH_LOSS_REPORT_EN_CMD)


class BleMgrGapSetTxPowerReportEnableCmd(BleMgrMsgBase):
    def __init__(self, conn_idx, loc_en, rem_en) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_TX_PWR_REPORT_EN_CMD)


class BleMgrGapRfPathCompensationSetCmd(BleMgrMsgBase):
    def __init__(self, conn_idx, rf_tx_path_compens, rf_rx_path_compens) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_RF_PATH_COMPENSATION_SET_CMD)


class BLE_CMD_GAP_OPCODE(IntEnum):
    BLE_MGR_GAP_ADDRESS_SET_CMD = BLE_MGR_CMD_CAT.BLE_MGR_GAP_CMD_CAT << 8
    BLE_MGR_GAP_DEVICE_NAME_SET_CMD = auto()
    BLE_MGR_GAP_APPEARANCE_SET_CMD = auto()
    BLE_MGR_GAP_PPCP_SET_CMD = auto()
    BLE_MGR_GAP_ADV_START_CMD = auto()
    BLE_MGR_GAP_ADV_STOP_CMD = auto()
    BLE_MGR_GAP_ADV_DATA_SET_CMD = auto()
    BLE_MGR_GAP_ADV_SET_PERMUTATION_CMD = auto()
    BLE_MGR_GAP_SCAN_START_CMD = auto()
    BLE_MGR_GAP_SCAN_STOP_CMD = auto()
    BLE_MGR_GAP_CONNECT_CMD = auto()
    BLE_MGR_GAP_CONNECT_CANCEL_CMD = auto()
    BLE_MGR_GAP_DISCONNECT_CMD = auto()
    BLE_MGR_GAP_PEER_VERSION_GET_CMD = auto()
    BLE_MGR_GAP_PEER_FEATURES_GET_CMD = auto()
    BLE_MGR_GAP_CONN_RSSI_GET_CMD = auto()
    BLE_MGR_GAP_ROLE_SET_CMD = auto()
    BLE_MGR_GAP_MTU_SIZE_SET_CMD = auto()
    BLE_MGR_GAP_CHANNEL_MAP_SET_CMD = auto()
    BLE_MGR_GAP_CONN_PARAM_UPDATE_CMD = auto()
    BLE_MGR_GAP_CONN_PARAM_UPDATE_REPLY_CMD = auto()
    BLE_MGR_GAP_PAIR_CMD = auto()
    BLE_MGR_GAP_PAIR_REPLY_CMD = auto()
    BLE_MGR_GAP_PASSKEY_REPLY_CMD = auto()
    BLE_MGR_GAP_UNPAIR_CMD = auto()
    BLE_MGR_GAP_SET_SEC_LEVEL_CMD = auto()
# if (dg_configBLE_SKIP_LATENCY_API == 1) # TODO need to handle these defines
    BLE_MGR_GAP_SKIP_LATENCY_CMD = auto()
# endif /* (dg_configBLE_SKIP_LATENCY_API == 1) 
    BLE_MGR_GAP_DATA_LENGTH_SET_CMD = auto()
# if (dg_configBLE_SECURE_CONNECTIONS == 1)
    BLE_MGR_GAP_NUMERIC_REPLY_CMD = auto()
# endif /* (dg_configBLE_SECURE_CONNECTIONS == 1) 
    BLE_MGR_GAP_ADDRESS_RESOLVE_CMD = auto()
# if (dg_configBLE_2MBIT_PHY == 1)
    BLE_MGR_GAP_PHY_SET_CMD = auto()
# endif /* (dg_configBLE_2MBIT_PHY == 1) 
    BLE_MGR_GAP_TX_POWER_SET_CMD = auto()
    BLE_MGR_GAP_CONN_TX_POWER_SET_CMD = auto()
    BLE_MGR_GAP_LOCAL_TX_POWER_GET_CMD = auto()
    BLE_MGR_GAP_REMOTE_TX_POWER_GET_CMD = auto()
    BLE_MGR_GAP_PATH_LOSS_REPORT_PARAMS_SET_CMD = auto()
    BLE_MGR_GAP_PATH_LOSS_REPORT_EN_CMD = auto()
    BLE_MGR_GAP_TX_PWR_REPORT_EN_CMD = auto()
    BLE_MGR_GAP_RF_PATH_COMPENSATION_SET_CMD = auto()
    BLE_MGR_GAP_LAST_CMD = auto()


class ble_evt_gap(IntEnum):
    # Connection established
    BLE_EVT_GAP_CONNECTED = BLE_EVT_CAT.BLE_EVT_CAT_GAP << 8
    # Advertising report
    BLE_EVT_GAP_ADV_REPORT = auto()
    # Disconnection event
    BLE_EVT_GAP_DISCONNECTED = auto()
    # Disconnect failed event
    BLE_EVT_GAP_DISCONNECT_FAILED = auto()
    # Advertising operation completed
    BLE_EVT_GAP_ADV_COMPLETED = auto()
    # Scan operation completed
    BLE_EVT_GAP_SCAN_COMPLETED = auto()
    # Connection parameter update request from peer
    BLE_EVT_GAP_CONN_PARAM_UPDATE_REQ = auto()
    # Connection parameters updated
    BLE_EVT_GAP_CONN_PARAM_UPDATED = auto()
    # Pairing request
    BLE_EVT_GAP_PAIR_REQ = auto()
    # Pairing completed
    BLE_EVT_GAP_PAIR_COMPLETED = auto()
    # Security request from peer
    BLE_EVT_GAP_SECURITY_REQUEST = auto()
    # Passkey notification
    BLE_EVT_GAP_PASSKEY_NOTIFY = auto()
    # Passkey request
    BLE_EVT_GAP_PASSKEY_REQUEST = auto()
    # Security level changed indication
    BLE_EVT_GAP_SEC_LEVEL_CHANGED = auto()
    # Random address resolved
    BLE_EVT_GAP_ADDRESS_RESOLVED = auto()
    # Set security level failed
    BLE_EVT_GAP_SET_SEC_LEVEL_FAILED = auto()
    # Connection parameters update completed
    BLE_EVT_GAP_CONN_PARAM_UPDATE_COMPLETED = auto()
    # Data length changed
    BLE_EVT_GAP_DATA_LENGTH_CHANGED = auto()
    # Data length set failed
    BLE_EVT_GAP_DATA_LENGTH_SET_FAILED = auto()
    # Connection operation completed
    BLE_EVT_GAP_CONNECTION_COMPLETED = auto()
    # Numeric request
    BLE_EVT_GAP_NUMERIC_REQUEST = auto()
    # Address resolution failed
    BLE_EVT_GAP_ADDRESS_RESOLUTION_FAILED = auto()
    # Long Term Key missing
    BLE_EVT_GAP_LTK_MISSING = auto()
    # Air Operation BD Address
    BLE_EVT_GAP_AIR_OP_BDADDR = auto()
# if (dg_configBLE_2MBIT_PHY == 1)
    # PHY set completed event
    BLE_EVT_GAP_PHY_SET_COMPLETED = auto()
    # PHY changed
    BLE_EVT_GAP_PHY_CHANGED = auto()
# endif /* (dg_configBLE_2MBIT_PHY == 1)
    # Peer version
    BLE_EVT_GAP_PEER_VERSION = auto()
    # Peer features
    BLE_EVT_GAP_PEER_FEATURES = auto()
    # Local Transmit Power Level event
    BLE_EVT_GAP_LOCAL_TX_PWR = auto()
    # Transmit Power Reporting
    BLE_EVT_GAP_TX_PWR_REPORT = auto()
    # Path Loss Threshold
    BLE_EVT_GAP_PATH_LOSS_THRES = auto()
# if BLE_SSP_DEBUG
    # LTK
    BLE_EVT_GAP_LTK = auto()
# endif


class BleManagerGap(BleManagerBase):

    def __init__(self,
                 adapter_command_q: asyncio.Queue(),
                 app_response_q: asyncio.Queue(),
                 wait_q: GtlWaitQueue()) -> None:

        super().__init__(adapter_command_q, app_response_q, wait_q)
        self.dev_params = BleDevParamsDefault()

        self.cmd_handlers = {
            BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ROLE_SET_CMD: self.role_set_cmd_handler,
            BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ADV_START_CMD: self.adv_start_cmd_handler,
            # BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ADV_STOP_CMD: self.gap_adv_stop_cmd_handler,
            # BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_CONNECT_CMD: self.connect_cmd_handler,
        }

        # TODO separate gapm and gapc?
        self.evt_handlers = {
            GAPM_MSG_ID.GAPM_CMP_EVT: None,
            GAPC_MSG_ID.GAPC_CONNECTION_REQ_IND: self.connected_evt_handler,
            # BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ADV_STOP_CMD: self.gap_adv_stop_cmd_handler,
            # BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_CONNECT_CMD: self.connect_cmd_handler,
        }

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
        gtl.parameters.role = self._ble_role_to_gtl_role(self.dev_params.role)  # TODO sdk has a function for this
        gtl.parameters.renew_dur = self.dev_params.addr_renew_duration
        gtl.parameters.att_cfg = self.dev_params.att_db_cfg
        gtl.parameters.max_mtu = self.dev_params.mtu_size
        gtl.parameters.max_mps = self.dev_params.mtu_size
        gtl.parameters.addr.addr[:] = self.dev_params.own_addr.addr.addr
        # TODO switch on dev_params.addr_type
        gtl.parameters.addr_type = self.dev_params.own_addr.addr_type
        gtl.parameters.irk.key[:] = self.dev_params.irk.key
        gtl.parameters.max_txoctets = dg_configBLE_DATA_LENGTH_TX_MAX
        gtl.parameters.max_txtime = (dg_configBLE_DATA_LENGTH_TX_MAX + 11 + 3) * 8

        return gtl

    def _set_role_rsp(self, message: GtlMessageBase, param: BLE_GAP_ROLE = BLE_GAP_ROLE.GAP_NO_ROLE):
        event: gapm_cmp_evt = message.parameters
        response = BLE_ERROR.BLE_ERROR_FAILED

        match event.status:
            case HOST_STACK_ERROR_CODE.GAP_ERR_NO_ERROR:
                self.dev_params.role = param
                response = BLE_ERROR.BLE_STATUS_OK
            case HOST_STACK_ERROR_CODE.GAP_ERR_INVALID_PARAM:
                response = BLE_ERROR.BLE_ERROR_INVALID_PARAM
            case HOST_STACK_ERROR_CODE.GAP_ERR_NOT_SUPPORTED:
                response = BLE_ERROR.BLE_ERROR_NOT_ALLOWED
            case HOST_STACK_ERROR_CODE.GAP_ERR_COMMAND_DISALLOWED:
                response = BLE_ERROR.BLE_ERROR_NOT_ALLOWED
            case _:
                response = event.status

        self.app_response_q.put_nowait(response)

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

        # TODO switch case for dev_params.own_addr.addr_type
        message.parameters.op.addr_src = self.dev_params.own_addr.addr_type  # TODO need to use own_address_t

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
        self.adapter_command_q.put_nowait(message)

        response = BLE_ERROR.BLE_STATUS_OK

        self.app_response_q.put_nowait(response)

    def connected_evt_handler(self, evt: GtlMessageBase):
        cfm = GapcConnectionCfm()
        pass

    def role_set_cmd_handler(self, command: BleMgrGapRoleSetCmd):
        dev_params_gtl = self._dev_params_to_gtl()
        dev_params_gtl.parameters.role = self._ble_role_to_gtl_role(command.role)
        self._wait_queue_add(0xFFFF, GAPM_MSG_ID.GAPM_CMP_EVT, GAPM_OPERATION.GAPM_SET_DEV_CONFIG, self._set_role_rsp, command.role)
        self.adapter_command_q.put_nowait(dev_params_gtl)


'''
    def gap_adv_stop_cmd_handler(self, command: BleMgrGapAdvStopCmd):

        # if not self.dev_params.advertising:
        #     response = BLE_ERROR.BLE_ERROR_NOT_ALLOWED
        # else:
        #    self._send_gapm_cancel_cmd(command)
        pass

    def _send_gapm_cancel_cmd(self, operation):
        # command = GapmCancelCmd
        pass
'''

'''
# TODO
static const ble_mgr_cmd_handler_t h_gap[BLE_MGR_CMD_GET_IDX(BLE_MGR_GAP_LAST_CMD)] = {
        ble_mgr_gap_address_set_cmd_handler,
        ble_mgr_gap_device_name_set_cmd_handler,
        ble_mgr_gap_appearance_set_cmd_handler,
        ble_mgr_gap_ppcp_set_cmd_handler,
        
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
#endif /* (dg_configBLE_SKIP_LATENCY_API == 1) 
        ble_mgr_gap_data_length_set_cmd_handler,
#if (dg_configBLE_SECURE_CONNECTIONS == 1)
        ble_mgr_gap_numeric_reply_cmd_handler,
#endif /* (dg_configBLE_SECURE_CONNECTIONS == 1) 
        ble_mgr_gap_address_resolve_cmd_handler,
#if (dg_configBLE_2MBIT_PHY == 1)
        ble_mgr_gap_phy_set_cmd_handler,
#endif /* (dg_configBLE_2MBIT_PHY == 1) 
};
'''
