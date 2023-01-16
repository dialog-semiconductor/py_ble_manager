from enum import IntEnum, auto

from ble_api.BleCommon import BLE_ERROR, BdAddress
from ble_api.BleGap import BLE_GAP_CONN_MODE, BLE_GAP_ROLE, gap_conn_params, GAP_SCAN_TYPE, GAP_SCAN_MODE
from manager.BleManagerCommonMsgs import BLE_MGR_CMD_CAT, BleMgrMsgBase, BleMgrMsgRsp, BLE_CMD_GAP_OPCODE


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


class BleMgrGapAdvStartRsp(BleMgrMsgRsp):
    def __init__(self, status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ADV_START_CMD,
                         status=status)


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
    def __init__(self,
                 peer_addr: BdAddress = None,
                 conn_params: gap_conn_params = None,
                 ce_len_min: int = 0,
                 ce_len_max: int = 0
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_CONNECT_CMD)
        self.peer_addr = peer_addr if peer_addr else BdAddress()
        self.conn_params = conn_params if conn_params else gap_conn_params()
        self.ce_len_min = ce_len_min
        self.ce_len_max = ce_len_max


class BleMgrGapConnectRsp(BleMgrMsgRsp):
    def __init__(self, status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_CONNECT_CMD,
                         status=status)


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


class BleMgrGapRoleSetRsp(BleMgrMsgRsp):
    def __init__(self,
                 new_role: BLE_GAP_ROLE = BLE_GAP_ROLE.GAP_NO_ROLE,
                 prev_role: BLE_GAP_ROLE = BLE_GAP_ROLE.GAP_NO_ROLE,
                 status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ROLE_SET_CMD,
                         status=status)
        self.new_role = new_role
        self.prev_role = prev_role


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
    def __init__(self,
                 type: GAP_SCAN_TYPE = GAP_SCAN_TYPE.GAP_SCAN_ACTIVE, 
                 mode: GAP_SCAN_MODE = GAP_SCAN_MODE.GAP_SCAN_GEN_DISC_MODE,
                 interval: int = 0,
                 window: int = 0,
                 filt_wlist: bool = False,
                 filt_dupl: bool = False
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_SCAN_START_CMD)
        self.type = type
        self.mode = mode
        self.interval = interval
        self.window = window
        self.filt_wlist = filt_wlist
        self.filt_dupl = filt_dupl


class BleMgrGapScanStartRsp(BleMgrMsgRsp):
    def __init__(self,
                 status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_SCAN_START_CMD,
                         status=status)


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
