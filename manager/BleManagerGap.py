import asyncio
from ctypes import c_uint8
from enum import IntEnum, auto
from gtl_messages.gtl_message_base import GtlMessageBase
from gtl_messages.gtl_message_gapm import GapmSetDevConfigCmd, GapmStartAdvertiseCmd, GapmCmpEvt  # , GapmStartConnectionCmd  # GapmResetCmd
from gtl_messages.gtl_message_gapc import GapcConnectionCfm, GapcConnectionReqInd, GapcGetDevInfoReqInd, GapcGetDevInfoCfm
# TODO perhaps these Gapm messages do not belong here
from gtl_port.gapm_task import GAPM_MSG_ID, gapm_cmp_evt, GAPM_OPERATION, GAPM_ADDR_TYPE, GAPM_OWN_ADDR
# gapm_set_dev_config_cmd, gapm_reset_cmd
from gtl_port.gapc_task import GAPC_MSG_ID, GAPC_DEV_INFO
from gtl_port.gapc import GAPC_FIELDS_MASK
# from gtl_messages.gtl_port.gattc_task import GATTC_MSG_ID
from gtl_port.gap import GAP_ROLE, GAP_AUTH_MASK
from .BleDevParams import BleDevParamsDefault
from gtl_port.rwble_hl_error import HOST_STACK_ERROR_CODE
from .GtlWaitQueue import GtlWaitQueue  # GtlWaitQueueElement
from ble_api.BleCommon import BLE_ERROR, BLE_EVT_CAT, BleEventBase, \
    bd_address, BLE_OWN_ADDR_TYPE, BLE_ADDR_TYPE
from ble_api.BleGap import BLE_GAP_ROLE, BLE_GAP_CONN_MODE, gap_conn_params, BLE_GAP_PHY, BleEventGapConnected, \
    BleEventGapAdvCompleted, BLE_CONN_IDX_INVALID, BLE_EVT_GAP

from .BleManagerStorage import device
from .BleManagerCommon import BLE_MGR_CMD_CAT, BleManagerBase, BleMgrMsgBase


# this is from ble_config.h
dg_configBLE_DATA_LENGTH_TX_MAX = (251)

# TODO this is from stack
ATT_DEFAULT_MTU = (23)


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


class BleMgrGapAdvStartRsp(BleMgrMsgBase):
    def __init__(self, status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ADV_START_CMD)
        self.status = status


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


class BleMgrGapRoleSetRsp(BleMgrMsgBase):
    def __init__(self,
                 new_role: BLE_GAP_ROLE = BLE_GAP_ROLE.GAP_NO_ROLE,
                 prev_role: BLE_GAP_ROLE = BLE_GAP_ROLE.GAP_NO_ROLE,
                 status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ROLE_SET_CMD)
        self.new_role = new_role
        self.prev_role = prev_role
        self.status = status


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


class BleMgrGapTxPowerSetCmd(BleMgrMsgBase):
    def __init__(self, air_operation, tx_power) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_TX_POWER_SET_CMD)


class BleMgrGapConnTxPowerSetCmd(BleMgrMsgBase):
    def __init__(self, conn_idx, tx_power) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_CONN_TX_POWER_SET_CMD)


class BleMgrGapLocalTxPowerGetCmd(BleMgrMsgBase):
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


class BleManagerGap(BleManagerBase):

    def __init__(self,
                 mgr_response_q: asyncio.Queue[BLE_ERROR],
                 mgr_event_q: asyncio.Queue[BleEventBase],
                 adapter_command_q: asyncio.Queue[BleMgrMsgBase],
                 wait_q: GtlWaitQueue) -> None:

        super().__init__(mgr_response_q, mgr_event_q, adapter_command_q, wait_q)
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
            # BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ADV_STOP_CMD: self.gap_adv_stop_cmd_handler,
            # BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_CONNECT_CMD: self.connect_cmd_handler,
        }

    def _adv_cmp_evt_hanlder(self, gtl: GapmCmpEvt):
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

    # TODO sdk passes rsp in as param. you have passed in command params
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

        response = BleMgrGapAdvStartRsp(BLE_ERROR.BLE_STATUS_OK)
        self._mgr_response_queue_send(response)

    def cmp_evt_handler(self, gtl: GapmCmpEvt):

        match gtl.parameters.operation:
            case GAPM_OPERATION.GAPM_ADV_NON_CONN \
                    | GAPM_OPERATION.GAPM_ADV_UNDIRECT \
                    | GAPM_OPERATION.GAPM_ADV_DIRECT \
                    | GAPM_OPERATION.GAPM_ADV_DIRECT_LDC:

                self._adv_cmp_evt_hanlder(gtl)
            case _:
                pass

    def get_device_info_req_evt_handler(self, gtl: GapcGetDevInfoReqInd):

        cfm = GapcGetDevInfoCfm(conidx=self._task_to_connidx(gtl.src_id))
        cfm.parameters.req = gtl.parameters.req
        match gtl.parameters.req:
            case GAPC_DEV_INFO.GAPC_DEV_NAME:
                # TODO is there an elegant way to remove ctypes c_uint8 dependency here
                name_list = []
                name_list[:0] = self.dev_params.dev_name
                cfm.parameters.info.name.value = (c_uint8 * len(self.dev_params.dev_name))(*name_list)
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

    def connected_evt_handler(self, gtl: GapcConnectionReqInd):
        print("connected_evt_handler\n")
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
        self._wait_queue_add(BLE_CONN_IDX_INVALID,
                             GAPM_MSG_ID.GAPM_CMP_EVT,
                             GAPM_OPERATION.GAPM_SET_DEV_CONFIG,
                             self._set_role_rsp,
                             command.role)

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
