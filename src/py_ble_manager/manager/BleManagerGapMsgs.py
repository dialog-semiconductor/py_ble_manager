from ctypes import c_uint8
from enum import IntEnum, auto
from ..ble_api.BleAtt import ATT_PERM
from ..ble_api.BleCommon import BLE_ERROR, BdAddress, BLE_HCI_ERROR, OwnAddress
from ..ble_api.BleGap import GAP_CONN_MODE, GAP_ROLE, GapConnParams, GAP_SCAN_TYPE, GAP_SCAN_MODE, \
    BLE_NON_CONN_ADV_DATA_LEN_MAX, GAP_APPEARANCE, GAP_SEC_LEVEL
from ..manager.BleManagerCommonMsgs import BleMgrMsgBase, BleMgrMsgRsp, BLE_CMD_GAP_OPCODE


# This is in ble_mgr.h in SDK. Consider moving to different file
class BLE_MGR_RAL_OP(IntEnum):
    BLE_MGR_RAL_OP_NONE = 0,
    BLE_MGR_RAL_OP_ADV_DIRECTED = auto()
    BLE_MGR_RAL_OP_ADV_UNDIRECTED = auto()
    BLE_MGR_RAL_OP_SCAN = auto()
    BLE_MGR_RAL_OP_CONNECT = auto()
    BLE_MGR_RAL_OP_NO_PRIVACY = auto()


class BleMgrGapAddressSetCmd(BleMgrMsgBase):
    def __init__(self,
                 address: OwnAddress,
                 renew_dur: int) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ADDRESS_SET_CMD)
        self.address = address
        self.renew_dur = renew_dur


class BleMgrGapAddressSetRsp(BleMgrMsgRsp):
    def __init__(self, status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ADDRESS_SET_CMD,
                         status=status)


class BleMgrGapAdvDataSetCmd(BleMgrMsgBase):
    def __init__(self,
                 adv_data_len: int = 0,
                 adv_data: (c_uint8 * BLE_NON_CONN_ADV_DATA_LEN_MAX) = (c_uint8 * BLE_NON_CONN_ADV_DATA_LEN_MAX)(),
                 scan_rsp_data_len: int = 0,
                 scan_rsp_data: (c_uint8 * BLE_NON_CONN_ADV_DATA_LEN_MAX) = (c_uint8 * BLE_NON_CONN_ADV_DATA_LEN_MAX)()
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ADV_DATA_SET_CMD)
        self.adv_data_len = adv_data_len
        self.adv_data = adv_data
        self.scan_rsp_data_len = scan_rsp_data_len
        self.scan_rsp_data = scan_rsp_data


class BleMgrGapAdvDataRsp(BleMgrMsgRsp):
    def __init__(self, status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ADV_DATA_SET_CMD,
                         status=status)


class BleMgrGapAdvStartCmd(BleMgrMsgBase):
    def __init__(self, adv_type: GAP_CONN_MODE = GAP_CONN_MODE.GAP_CONN_MODE_UNDIRECTED) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ADV_START_CMD)
        self.adv_type = adv_type


class BleMgrGapAdvStartRsp(BleMgrMsgRsp):
    def __init__(self, status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ADV_START_CMD,
                         status=status)


class BleMgrGapAdvStopCmd(BleMgrMsgBase):
    def __init__(self) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ADV_STOP_CMD)


class BleMgrGapAdvStopRsp(BleMgrMsgRsp):
    def __init__(self, status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ADV_STOP_CMD,
                         status=status)


class BleMgrGapAppearanceSetCmd(BleMgrMsgBase):
    def __init__(self,
                 appearance: GAP_APPEARANCE,
                 perm: ATT_PERM) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_APPEARANCE_SET_CMD)
        self.appearance = appearance
        self.perm = perm


class BleMgrGapAppearanceSetRsp(BleMgrMsgRsp):
    def __init__(self, status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_APPEARANCE_SET_CMD,
                         status=status)


class BleMgrGapConnectCancelCmd(BleMgrMsgBase):
    def __init__(self) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_CONNECT_CANCEL_CMD)


class BleMgrGapConnectCancelRsp(BleMgrMsgRsp):
    def __init__(self, status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_CONNECT_CANCEL_CMD,
                         status=status)


class BleMgrGapConnectCmd(BleMgrMsgBase):
    def __init__(self,
                 peer_addr: BdAddress = None,
                 conn_params: GapConnParams = None,
                 ce_len_min: int = 0,
                 ce_len_max: int = 0
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_CONNECT_CMD)
        self.peer_addr = peer_addr if peer_addr else BdAddress()
        self.conn_params = conn_params if conn_params else GapConnParams()
        self.ce_len_min = ce_len_min
        self.ce_len_max = ce_len_max


class BleMgrGapConnectRsp(BleMgrMsgRsp):
    def __init__(self, status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_CONNECT_CMD,
                         status=status)


class BleMgrGapConnParamUpdateCmd(BleMgrMsgBase):
    def __init__(self,
                 conn_idx: int,
                 conn_params: GapConnParams
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_CONN_PARAM_UPDATE_CMD)
        self.conn_idx = conn_idx
        self.conn_params = conn_params


class BleMgrGapConnParamUpdateRsp(BleMgrMsgRsp):
    def __init__(self, status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_CONN_PARAM_UPDATE_CMD,
                         status=status)


class BleMgrGapConnParamUpdateReplyCmd(BleMgrMsgBase):
    def __init__(self,
                 conn_idx: int,
                 accept: bool
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_CONN_PARAM_UPDATE_REPLY_CMD)
        self.conn_idx = conn_idx
        self.accept = accept


class BleMgrGapConnParamUpdateReplyRsp(BleMgrMsgRsp):
    def __init__(self, status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_CONN_PARAM_UPDATE_REPLY_CMD,
                         status=status)


class BleMgrGapDataLengthSetCmd(BleMgrMsgBase):
    def __init__(self,
                 conn_idx: int,
                 tx_length: int,
                 tx_time: int
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_DATA_LENGTH_SET_CMD)
        self.conn_idx = conn_idx
        self.tx_length = tx_length
        self.tx_time = tx_time


class BleMgrGapDataLengthSetRsp(BleMgrMsgRsp):
    def __init__(self, status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_DATA_LENGTH_SET_CMD,
                         status=status)


class BleMgrGapDeviceNameSetCmd(BleMgrMsgBase):
    def __init__(self,
                 name: str = "",
                 perm: ATT_PERM = ATT_PERM.ATT_PERM_NONE,
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_DEVICE_NAME_SET_CMD)
        self.name = name
        self.perm = perm


class BleMgrGapDeviceNameSetRsp(BleMgrMsgRsp):
    def __init__(self, status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_DEVICE_NAME_SET_CMD,
                         status=status)


class BleMgrGapDisconnectCmd(BleMgrMsgBase):
    def __init__(self,
                 conn_idx: int = 0,
                 reason: BLE_HCI_ERROR = BLE_HCI_ERROR.BLE_HCI_ERROR_NO_ERROR,
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_DISCONNECT_CMD)
        self.conn_idx = conn_idx
        self.reason = reason


class BleMgrGapDisconnectRsp(BleMgrMsgRsp):
    def __init__(self, status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_DISCONNECT_CMD,
                         status=status)


class BleMgrGapMtuSizeSetCmd(BleMgrMsgBase):
    def __init__(self,
                 mtu_size: int = 0
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_MTU_SIZE_SET_CMD)
        self.mtu_size = mtu_size


class BleMgrGapMtuSizeSetRsp(BleMgrMsgRsp):
    def __init__(self,
                 new_mtu_size: int = 0,
                 previous_mtu_size: int = 0,
                 status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_MTU_SIZE_SET_CMD,
                         status=status)
        self.new_mtu_size = new_mtu_size
        self.previous_mtu_size = previous_mtu_size


class BleMgrGapNumericReplyCmd(BleMgrMsgBase):
    def __init__(self,
                 conn_idx: int = 0,
                 accept: bool = False,
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_NUMERIC_REPLY_CMD)
        self.conn_idx = conn_idx
        self.accept = accept


class BleMgrGapNumericReplyRsp(BleMgrMsgRsp):
    def __init__(self, status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_NUMERIC_REPLY_CMD,
                         status=status)


class BleMgrGapPairCmd(BleMgrMsgBase):
    def __init__(self, conn_idx: int, bond: bool) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_PAIR_CMD)
        self.conn_idx = conn_idx
        self.bond = bond


class BleMgrGapPairRsp(BleMgrMsgRsp):
    def __init__(self,
                 status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_PAIR_CMD,
                         status=status)


class BleMgrGapPairReplyCmd(BleMgrMsgBase):
    def __init__(self, conn_idx: int, accept: bool, bond: bool) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_PAIR_REPLY_CMD)
        self.conn_idx = conn_idx
        self.accept = accept
        self.bond = bond


class BleMgrGapPairReplyRsp(BleMgrMsgRsp):
    def __init__(self,
                 status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_PAIR_REPLY_CMD,
                         status=status)


class BleMgrGapPasskeyReplyCmd(BleMgrMsgBase):
    def __init__(self, conn_idx: int, accept: bool, passkey: int) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_PASSKEY_REPLY_CMD)
        self.conn_idx = conn_idx
        self.accept = accept
        self.passkey = passkey


class BleMgrGapPasskeyReplyRsp(BleMgrMsgRsp):
    def __init__(self,
                 status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_PASSKEY_REPLY_CMD,
                         status=status)


class BleMgrGapPeerFeaturesGetCmd(BleMgrMsgBase):
    def __init__(self,
                 conn_idx: int) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_PEER_FEATURES_GET_CMD)
        self.conn_idx = conn_idx


class BleMgrGapPeerFeaturesGetRsp(BleMgrMsgRsp):
    def __init__(self,
                 status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_PEER_FEATURES_GET_CMD,
                         status=status)


class BleMgrGapPeerVersionGetCmd(BleMgrMsgBase):
    def __init__(self,
                 conn_idx: int) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_PEER_VERSION_GET_CMD)
        self.conn_idx = conn_idx


class BleMgrGapPeerVersionGetRsp(BleMgrMsgRsp):
    def __init__(self,
                 status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_PEER_VERSION_GET_CMD,
                         status=status)


class BleMgrGapPpcpSetCmd(BleMgrMsgBase):
    def __init__(self,
                 gap_ppcp: GapConnParams) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_PPCP_SET_CMD)
        self.gap_ppcp = gap_ppcp


class BleMgrGapPpcpSetRsp(BleMgrMsgRsp):
    def __init__(self,
                 status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_PPCP_SET_CMD,
                         status=status)


class BleMgrGapRoleSetCmd(BleMgrMsgBase):
    def __init__(self, role: GAP_ROLE = GAP_ROLE.GAP_NO_ROLE) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ROLE_SET_CMD)
        self.role = role


class BleMgrGapRoleSetRsp(BleMgrMsgRsp):
    def __init__(self,
                 new_role: GAP_ROLE = GAP_ROLE.GAP_NO_ROLE,
                 prev_role: GAP_ROLE = GAP_ROLE.GAP_NO_ROLE,
                 status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ROLE_SET_CMD,
                         status=status)
        self.new_role = new_role
        self.prev_role = prev_role


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


class BleMgrGapScanStopRsp(BleMgrMsgRsp):
    def __init__(self,
                 status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_SCAN_STOP_CMD,
                         status=status)


class BleMgrGapSetSecLevelCmd(BleMgrMsgBase):
    def __init__(self,
                 conn_idx: int = 0,
                 level: GAP_SEC_LEVEL = GAP_SEC_LEVEL.GAP_SEC_LEVEL_1
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_SET_SEC_LEVEL_CMD)
        self.conn_idx = conn_idx
        self.level = level


class BleMgrGapSetSecLevelRsp(BleMgrMsgRsp):
    def __init__(self,
                 status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_SET_SEC_LEVEL_CMD,
                         status=status)


class BleMgrGapUnpairCmd(BleMgrMsgBase):
    def __init__(self,
                 addr: BdAddress = BdAddress()
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_UNPAIR_CMD)
        self.addr = addr


class BleMgrGapUnpairRsp(BleMgrMsgRsp):
    def __init__(self,
                 status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_UNPAIR_CMD,
                         status=status)
