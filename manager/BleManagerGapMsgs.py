from enum import IntEnum, auto

from ble_api.BleCommon import BLE_ERROR
from ble_api.BleGap import BLE_GAP_CONN_MODE, BLE_GAP_ROLE
from manager.BleManagerCommonMsgs import BLE_MGR_CMD_CAT, BleMgrMsgBase


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


# TODO most of these Cmd clases need to their definition to be completed
class BleMgrGapAddressResolveCmd(BleMgrMsgBase):
    def __init__(self, address) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ADDRESS_RESOLVE_CMD)


class BleMgrGapAdvDataSetCmd(BleMgrMsgBase):
    def __init__(self, adv_data_len, adv_data, scan_rsp_data_len, scan_rsp_data) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ADV_DATA_SET_CMD)


class BleMgrGapAdvSetPermIdCmd(BleMgrMsgBase):
    def __init__(self, permutation_idx) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ADV_SET_PERMUTATION_CMD)


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


class BleMgrGapAppearanceSetCmd(BleMgrMsgBase):
    def __init__(self, appearance, perm) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_APPEARANCE_SET_CMD)


class BleMgrGapAddressSetCmd(BleMgrMsgBase):
    def __init__(self, address, renew_dur) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ADDRESS_SET_CMD)


class BleMgrGapChannelMapSetCmd(BleMgrMsgBase):
    def __init__(self, channel_map) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_CHANNEL_MAP_SET_CMD)


class BleMgrGapConnectCancelCmd(BleMgrMsgBase):
    def __init__(self) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_CONNECT_CANCEL_CMD)


class BleMgrGapConnectCmd(BleMgrMsgBase):
    def __init__(self, peer_addr, conn_params, ce_len_min, ce_len_max) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_CONNECT_CMD)


class BleMgrGapConnParamUpdateCmd(BleMgrMsgBase):
    def __init__(self, conn_idx, conn_params) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_CONN_PARAM_UPDATE_CMD)


class BleMgrGapConnParamUpdateReplyCmd(BleMgrMsgBase):
    def __init__(self, conn_idx, accept) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_CONN_PARAM_UPDATE_REPLY_CMD)


class BleMgrGapConnRssiGetCmd(BleMgrMsgBase):
    def __init__(self, conn_idx) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_CONN_RSSI_GET_CMD)


class BleMgrGapConnTxPowerSetCmd(BleMgrMsgBase):
    def __init__(self, conn_idx, tx_power) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_CONN_TX_POWER_SET_CMD)


class BleMgrGapDataLengthSetCmd(BleMgrMsgBase):
    def __init__(self, conn_idx, tx_length, tx_time) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_DATA_LENGTH_SET_CMD)


class BleMgrGapDeviceNameSetCmd(BleMgrMsgBase):
    def __init__(self, name, perm) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_DEVICE_NAME_SET_CMD)


class BleMgrGapDisconnectCmd(BleMgrMsgBase):
    def __init__(self, conn_idx, reason) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_DISCONNECT_CMD)


class BleMgrGapLocalTxPowerGetCmd(BleMgrMsgBase):
    def __init__(self, conn_idx, phy) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_LOCAL_TX_POWER_GET_CMD)


class BleMgrGapMtuSizeSetCmd(BleMgrMsgBase):
    def __init__(self, mtu_size) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_MTU_SIZE_SET_CMD)


class BleMgrGapNumericReplyCmd(BleMgrMsgBase):
    def __init__(self, conn_idx, accept) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_NUMERIC_REPLY_CMD)


class BleMgrGapPeerFeaturesGetCmd(BleMgrMsgBase):
    def __init__(self, conn_idx) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_PEER_FEATURES_GET_CMD)


class BleMgrGapPeerVersionGetCmd(BleMgrMsgBase):
    def __init__(self, conn_idx) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_PEER_VERSION_GET_CMD)


class BleMgrGapPairCmd(BleMgrMsgBase):
    def __init__(self, conn_idx, bond) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_PAIR_CMD)


class BleMgrGapPairReplyCmd(BleMgrMsgBase):
    def __init__(self, conn_idx, accept, bond) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_PAIR_REPLY_CMD)


class BleMgrGapPasskeyReplyCmd(BleMgrMsgBase):
    def __init__(self, conn_idx, accept, passkey) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_PASSKEY_REPLY_CMD)


class BleMgrGapPhySetCmd(BleMgrMsgBase):
    def __init__(self, conn_idx, tx_phy, rx_phy) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_PHY_SET_CMD)


class BleMgrGapPpcpSetCmd(BleMgrMsgBase):
    def __init__(self, gap_ppcp) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_PPCP_SET_CMD)


class BleMgrGapReadRemoteTxPowerLevelCmd(BleMgrMsgBase):
    def __init__(self, air_operation, phy) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_REMOTE_TX_POWER_GET_CMD)


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


class BleMgrGapRfPathCompensationSetCmd(BleMgrMsgBase):
    def __init__(self, conn_idx, rf_tx_path_compens, rf_rx_path_compens) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_RF_PATH_COMPENSATION_SET_CMD)


class BleMgrGapSetPathLossReportEnableCmd(BleMgrMsgBase):
    def __init__(self, conn_idx, enable) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_PATH_LOSS_REPORT_EN_CMD)


class BleMgrGapSetPathLossReportParamsCmd(BleMgrMsgBase):
    def __init__(self, conn_idx, high_thres, high_hyst, low_thres, low_hyst, min_time_spent) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_PATH_LOSS_REPORT_PARAMS_SET_CMD)


class BleMgrGapSetSecLevelCmd(BleMgrMsgBase):
    def __init__(self, conn_idx, level) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_SET_SEC_LEVEL_CMD)


class BleMgrGapSetTxPowerReportEnableCmd(BleMgrMsgBase):
    def __init__(self, conn_idx, loc_en, rem_en) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_TX_PWR_REPORT_EN_CMD)


class BleMgrGapScanStartCmd(BleMgrMsgBase):
    def __init__(self, type, mode, interval, window, filt_wlist, filt_dupl) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_SCAN_START_CMD)


class BleMgrGapScanStopCmd(BleMgrMsgBase):
    def __init__(self) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_SCAN_STOP_CMD)


class BleMgrGapSkipLatencyCmd(BleMgrMsgBase):
    def __init__(self, conn_idx, enable) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_SKIP_LATENCY_CMD)


class BleMgrGapTxPowerSetCmd(BleMgrMsgBase):
    def __init__(self, air_operation, tx_power) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_TX_POWER_SET_CMD)


class BleMgrGapUnpairCmd(BleMgrMsgBase):
    def __init__(self, addr) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_UNPAIR_CMD)
