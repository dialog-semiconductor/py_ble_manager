from enum import IntEnum, auto
from ble_api.BleCommon import BLE_ERROR


class BLE_MGR_CMD_CAT(IntEnum):
    BLE_MGR_COMMON_CMD_CAT = 0x00
    BLE_MGR_GAP_CMD_CAT = 0x01
    BLE_MGR_GATTS_CMD_CAT = 0x02
    BLE_MGR_GATTC_CMD_CAT = 0x03
    BLE_MGR_L2CAP_CMD_CAT = 0x04
    BLE_MGR_LAST_CMD_CAT = auto()


class BLE_MGR_COMMON_CMD_OPCODE(IntEnum):
    BLE_MGR_COMMON_STACK_MSG = BLE_MGR_CMD_CAT.BLE_MGR_COMMON_CMD_CAT << 8
    BLE_MGR_COMMON_REGISTER_CMD = auto()
    BLE_MGR_COMMON_ENABLE_CMD = auto()
    BLE_MGR_COMMON_RESET_CMD = auto()
    BLE_MGR_COMMON_READ_TX_POWER_CMD = auto()
    # Dummy command opcode, needs to be always defined after all commands
    BLE_MGR_COMMON_LAST_CMD = auto()


class BleMgrMsgBase():
    def __init__(self, opcode) -> None:
        self.opcode = opcode


'''
class BleMgrMsgBaseRsp(BleMgrMsgBase):  # TODO reponses should inherit fromm this class instead of BleMgrMsgBase
    def __init__(self, opcode, status: BLE_ERROR) -> None:
        self.status = status
        super().__init__(opcode=opcode)
'''


class BleMgrCommonResetCmd(BleMgrMsgBase):
    def __init__(self) -> None:
        super().__init__(opcode=BLE_MGR_COMMON_CMD_OPCODE.BLE_MGR_COMMON_RESET_CMD)


class BleMgrCommonResetRsp(BleMgrMsgBase):
    def __init__(self, status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED) -> None:
        super().__init__(opcode=BLE_MGR_COMMON_CMD_OPCODE.BLE_MGR_COMMON_RESET_CMD)
        self.status = status
