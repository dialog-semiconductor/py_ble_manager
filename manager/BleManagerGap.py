import asyncio
# from ctypes import c_uint16, c_uint8, Array
from enum import IntEnum, auto
from gtl_messages.gtl_message_base import GtlMessageBase
from gtl_messages.gtl_message_gapm import GapmSetDevConfigCmd, GapmStartAdvertiseCmd, GapmCmpEvt  # , GapmStartConnectionCmd  # GapmResetCmd
from gtl_messages.gtl_message_gapc import GapcConnectionCfm, GapcConnectionReqInd
# TODO perhaps these Gapm messages do not belong here
from gtl_port.gapm_task import GAPM_MSG_ID, gapm_cmp_evt, GAPM_OPERATION, GAPM_ADDR_TYPE, GAPM_OWN_ADDR
# gapm_set_dev_config_cmd, gapm_reset_cmd
from gtl_port.gapc_task import GAPC_MSG_ID
from gtl_port.gapc import GAPC_FIELDS_MASK
# from gtl_messages.gtl_port.gattc_task import GATTC_MSG_ID
from gtl_port.gap import GAP_ROLE, GAP_AUTH_MASK
from .BleDevParams import BleDevParamsDefault
from gtl_port.rwble_hl_error import HOST_STACK_ERROR_CODE
from .GtlWaitQueue import GtlWaitQueue  # GtlWaitQueueElement
from ble_api.BleCommon import BLE_ERROR, BLE_EVT_CAT, BleEventBase, \
    bd_address, BLE_OWN_ADDR_TYPE, BLE_ADDR_TYPE
from ble_api.BleGap import BLE_GAP_ROLE, BLE_GAP_CONN_MODE, gap_conn_params, BLE_GAP_PHY  # TODO dont like these files referencing eachother
from .BleManagerStorage import device
from .BleManagerCommon import BLE_MGR_CMD_CAT, BleManagerBase, BleMgrCmdBase


# this is from ble_config.h
dg_configBLE_DATA_LENGTH_TX_MAX = (251)

# TODO this is from stack
ATT_DEFAULT_MTU = (23)


class BleMgrGapAddressSetCmd(BleMgrCmdBase):
    def __init__(self, address, renew_dur) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ADDRESS_SET_CMD)


class BleMgrGapDeviceNameSetCmd(BleMgrCmdBase):
    def __init__(self, name, perm) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_DEVICE_NAME_SET_CMD)


class BleMgrGapAppearanceSetCmd(BleMgrCmdBase):
    def __init__(self, appearance, perm) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_APPEARANCE_SET_CMD)


class BleMgrGapPpcpSetCmd(BleMgrCmdBase):
    def __init__(self, gap_ppcp) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_PPCP_SET_CMD)


class BleMgrGapAdvStartCmd(BleMgrCmdBase):
    def __init__(self, adv_type: BLE_GAP_CONN_MODE = BLE_GAP_CONN_MODE.GAP_CONN_MODE_UNDIRECTED) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ADV_START_CMD)
        self.adv_type = adv_type  # TODO raise error on bad arg


class BleMgrGapAdvStopCmd(BleMgrCmdBase):
    def __init__(self) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ADV_STOP_CMD)


class BleMgrGapAdvDataSetCmd(BleMgrCmdBase):
    def __init__(self, adv_data_len, adv_data, scan_rsp_data_len, scan_rsp_data) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ADV_DATA_SET_CMD)


class BleMgrGapAdvSetPermIdCmd(BleMgrCmdBase):
    def __init__(self, permutation_idx) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ADV_SET_PERMUTATION_CMD)


class BleMgrGapScanStartCmd(BleMgrCmdBase):
    def __init__(self, type, mode, interval, window, filt_wlist, filt_dupl) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_SCAN_START_CMD)


class BleMgrGapScanStopCmd(BleMgrCmdBase):
    def __init__(self) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_SCAN_STOP_CMD)


class BleMgrGapConnectCmd(BleMgrCmdBase):
    def __init__(self, peer_addr, conn_params, ce_len_min, ce_len_max) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_CONNECT_CMD)


class BleMgrGapConnectCancelCmd(BleMgrCmdBase):
    def __init__(self) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_CONNECT_CANCEL_CMD)


class BleMgrGapDisconnectCmd(BleMgrCmdBase):
    def __init__(self, conn_idx, reason) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_DISCONNECT_CMD)


class BleMgrGapPeerVersionGetCmd(BleMgrCmdBase):
    def __init__(self, conn_idx) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_PEER_VERSION_GET_CMD)


class BleMgrGapPeerFeaturesGetCmd(BleMgrCmdBase):
    def __init__(self, conn_idx) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_PEER_FEATURES_GET_CMD)


class BleMgrGapConnRssiGetCmd(BleMgrCmdBase):
    def __init__(self, conn_idx) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_CONN_RSSI_GET_CMD)


class BleMgrGapRoleSetCmd(BleMgrCmdBase):
    def __init__(self, role: BLE_GAP_ROLE = BLE_GAP_ROLE.GAP_NO_ROLE) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ROLE_SET_CMD)
        self.role = role


class BleMgrGapMtuSizeSetCmd(BleMgrCmdBase):
    def __init__(self, mtu_size) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_MTU_SIZE_SET_CMD)


class BleMgrGapChannelMapSetCmd(BleMgrCmdBase):
    def __init__(self, channel_map) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_CHANNEL_MAP_SET_CMD)


class BleMgrGapConnParamUpdateCmd(BleMgrCmdBase):
    def __init__(self, conn_idx, conn_params) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_CONN_PARAM_UPDATE_CMD)


class BleMgrGapConnParamUpdateReplyCmd(BleMgrCmdBase):
    def __init__(self, conn_idx, accept) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_CONN_PARAM_UPDATE_REPLY_CMD)


class BleMgrGapPairCmd(BleMgrCmdBase):
    def __init__(self, conn_idx, bond) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_PAIR_CMD)


class BleMgrGapPairReplyCmd(BleMgrCmdBase):
    def __init__(self, conn_idx, accept, bond) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_PAIR_REPLY_CMD)


class BleMgrGapPasskeyReplyCmd(BleMgrCmdBase):
    def __init__(self, conn_idx, accept, passkey) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_PASSKEY_REPLY_CMD)


class BleMgrGapNumericReplyCmd(BleMgrCmdBase):
    def __init__(self, conn_idx, accept) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_NUMERIC_REPLY_CMD)


class BleMgrGapUnpairCmd(BleMgrCmdBase):
    def __init__(self, addr) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_UNPAIR_CMD)


class BleMgrGapSetSecLevelCmd(BleMgrCmdBase):
    def __init__(self, conn_idx, level) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_SET_SEC_LEVEL_CMD)


# TODO ble_mgr_gap_skip_latency_cmd_t

class BleMgrGapDataLengthSetCmd(BleMgrCmdBase):
    def __init__(self, conn_idx, tx_length, tx_time) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_DATA_LENGTH_SET_CMD)


class BleMgrGapAddressResolveCmd(BleMgrCmdBase):
    def __init__(self, address) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ADDRESS_RESOLVE_CMD)


class BleMgrGapPhySetCmd(BleMgrCmdBase):
    def __init__(self, conn_idx, tx_phy, rx_phy) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_PHY_SET_CMD)


class BleMgrGapTxPowerSetCmd(BleMgrCmdBase):
    def __init__(self, air_operation, tx_power) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_TX_POWER_SET_CMD)


class BleMgrGapConnTxPowerSetCmd(BleMgrCmdBase):
    def __init__(self, conn_idx, tx_power) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_CONN_TX_POWER_SET_CMD)


class BleMgrGapLocalTxPowerGetCmd(BleMgrCmdBase):
    def __init__(self, conn_idx, phy) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_LOCAL_TX_POWER_GET_CMD)


class BleMgrGapReadRemoteTxPowerLevelCmd(BleMgrCmdBase):
    def __init__(self, air_operation, phy) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_REMOTE_TX_POWER_GET_CMD)


class BleMgrGapSetPathLossReportParamsCmd(BleMgrCmdBase):
    def __init__(self, conn_idx, high_thres, high_hyst, low_thres, low_hyst, min_time_spent) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_PATH_LOSS_REPORT_PARAMS_SET_CMD)


class BleMgrGapSetPathLossReportEnableCmd(BleMgrCmdBase):
    def __init__(self, conn_idx, enable) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_PATH_LOSS_REPORT_EN_CMD)


class BleMgrGapSetTxPowerReportEnableCmd(BleMgrCmdBase):
    def __init__(self, conn_idx, loc_en, rem_en) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_TX_PWR_REPORT_EN_CMD)


class BleMgrGapRfPathCompensationSetCmd(BleMgrCmdBase):
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


class BLE_EVT_GAP(IntEnum):
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


# TODO in sdk this is in ble_gap
class BleEventGapConnected(BleEventBase):
    def __init__(self, conn_idx: int = 0, own_addr: bd_address = None, peer_address: bd_address = None, conn_params: gap_conn_params = None) -> None:
        super().__init__(evt_code=BLE_EVT_GAP.BLE_EVT_GAP_CONNECTED)
        self.conn_idx = conn_idx
        self.own_addr = own_addr if own_addr else bd_address()
        self.peer_address = peer_address if peer_address else bd_address()
        self.conn_params = conn_params if conn_params else gap_conn_params()


class BleEventGapAdvCompleted(BleEventBase):
    def __init__(self, adv_type: BLE_GAP_CONN_MODE = BLE_GAP_CONN_MODE.GAP_CONN_MODE_UNDIRECTED, status: BLE_ERROR = BLE_ERROR.BLE_STATUS_OK) -> None:
        super().__init__(evt_code=BLE_EVT_GAP.BLE_EVT_GAP_ADV_COMPLETED)
        self.adv_type = adv_type  # Advertising type
        self.status = status  # Completion status


class BleManagerGap(BleManagerBase):

    def __init__(self,
                 api_response_q: asyncio.Queue[BLE_ERROR],
                 api_event_q: asyncio.Queue[BleEventBase],
                 adapter_command_q: asyncio.Queue[BleMgrCmdBase],
                 wait_q: GtlWaitQueue) -> None:

        super().__init__(api_response_q, api_event_q, adapter_command_q, wait_q)
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
            # BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ADV_STOP_CMD: self.gap_adv_stop_cmd_handler,
            # BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_CONNECT_CMD: self.connect_cmd_handler,
        }

    def _adv_cmp_evt_hanlder(self, gtl: GapmCmpEvt):
        print("_adv_cmp_evt_hanlder")
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

        self._api_event_queue_send(evt)

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

        self._api_response_queue_send(response)

    def _task_to_connidx(self, task_id):  # TODO this is repeated from GtlWaitQueue. Do not have in two places
        return task_id >> 8

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

        response = BLE_ERROR.BLE_STATUS_OK

        self._api_response_queue_send(response)

    def cmp_evt_handler(self, gtl: GapmCmpEvt):

        match gtl.parameters.operation:
            case GAPM_OPERATION.GAPM_ADV_NON_CONN \
                    | GAPM_OPERATION.GAPM_ADV_UNDIRECT \
                    | GAPM_OPERATION.GAPM_ADV_DIRECT \
                    | GAPM_OPERATION.GAPM_ADV_DIRECT_LDC:

                self._adv_cmp_evt_hanlder(gtl)
            case _:
                pass

    def connected_evt_handler(self, gtl: GapcConnectionReqInd):
        evt = BleEventGapConnected()
        evt.conn_idx = self._task_to_connidx(gtl.src_id)
        evt.own_addr.addr_type = self.dev_params.own_addr.addr_type
        evt.own_addr.addr[:] = self.dev_params.own_addr.addr
        # if (dg_configBLE_PRIVACY_1_2 == 1)
        # evt.peer_address.addr_type = gtl.parameters.peer_addr_type & 0x01
        # else
        evt.peer_address.addr_type = gtl.parameters.peer_addr_type
        evt.peer_address.addr[:] = gtl.parameters.peer_addr.addr[:]
        evt.conn_params.interval_min = gtl.parameters.con_interval
        evt.conn_params.interval_max = gtl.parameters.con_interval
        evt.conn_params.slave_latency = gtl.parameters.con_latency
        evt.conn_params.sup_timeout = gtl.parameters.sup_to

        # if (dg_configBLE_SKIP_LATENCY_API == 1)
        # ble_mgr_skip_latency_set(evt->conn_idx, false);
        # endif /* (dg_configBLE_SKIP_LATENCY_API == 1) */

        # TODO some stuff with finding the device in storage
        # dev = find_device_by_addr(&evt->peer_address, true); Below just creates dev for now instead
        dev = device()
        dev.addr = evt.peer_address

        dev.conn_idx = evt.conn_idx
        dev.connected = True
        dev.mtu = ATT_DEFAULT_MTU
        # if (dg_configBLE_2MBIT_PHY == 1)
        dev.tx_phy = BLE_GAP_PHY.BLE_GAP_PHY_1M
        dev.rx_phy = BLE_GAP_PHY.BLE_GAP_PHY_1M
        # endif /* (dg_configBLE_2MBIT_PHY == 1) */
        if dev.connecting:
            dev.master = True
            dev.connecting = False
        else:
            dev.master = False

        # if (dg_configBLE_CENTRAL == 1)
        if dev.master:
            # TODO initiate a version exchange
            pass
        # endif /* (dg_configBLE_CENTRAL == 1) */

        # if (dg_configBLE_PRIVACY_1_2 == 1)
        if self.dev_params.own_addr.addr_type != BLE_OWN_ADDR_TYPE.PRIVATE_CNTL:
            # endif /* (dg_configBLE_PRIVACY_1_2 == 1) */
            pass  # TODO needs to be same as resolve addr here

        if self._resolve_address_from_connected_evt(gtl, evt):  # Note passed in gtl instead of gtl.params
            pass

        self._api_event_queue_send(evt)

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
        if dev.csrk:  # TODO need to do equiv of null check
            pass
        if dev.remote_csrk:  # TODO need to do equiv of null check
            pass

        # TODO something with service changed characteristic value from storage
        self._adapter_command_queue_send(cfm)

    def _resolve_address_from_connected_evt(self, evt: GapcConnectionReqInd, param: None):
        # Check if peer's address is random
        if evt.parameters.peer_addr_type != BLE_ADDR_TYPE.PRIVATE_ADDRESS:
            return False

        # Check if peer's address is resolvable
        if evt.parameters.peer_addr.addr[5] & 0xC0 != 0x40:
            return False
        # TODO some gtl stuff
        return False

    def _get_peer_version(self, conn_idx: int = 0):
        pass

    def role_set_cmd_handler(self, command: BleMgrGapRoleSetCmd):
        dev_params_gtl = self._dev_params_to_gtl()
        dev_params_gtl.parameters.role = self._ble_role_to_gtl_role(command.role)
        self._wait_queue_add(0xFFFF, GAPM_MSG_ID.GAPM_CMP_EVT, GAPM_OPERATION.GAPM_SET_DEV_CONFIG, self._set_role_rsp, command.role)
        self._adapter_command_queue_send(dev_params_gtl)


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