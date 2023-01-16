
from enum import IntEnum, auto
from ble_api.BleAtt import AttUuid
from ble_api.BleCommon import BLE_ERROR
from manager.BleManagerCommonMsgs import BLE_MGR_CMD_CAT, BleMgrMsgBase


class BLE_CMD_GATTC_OPCODE(IntEnum):
    BLE_MGR_GATTC_BROWSE_CMD = BLE_MGR_CMD_CAT.BLE_MGR_GATTC_CMD_CAT << 8
    BLE_MGR_GATTC_BROWSE_RANGE_CMD = auto()
    BLE_MGR_GATTC_DISCOVER_SVC_CMD = auto()
    BLE_MGR_GATTC_DISCOVER_INCLUDE_CMD = auto()
    BLE_MGR_GATTC_DISCOVER_CHAR_CMD = auto()
    BLE_MGR_GATTC_DISCOVER_DESC_CMD = auto()
    BLE_MGR_GATTC_READ_CMD = auto()
    BLE_MGR_GATTC_WRITE_GENERIC_CMD = auto()
    BLE_MGR_GATTC_WRITE_EXECUTE_CMD = auto()
    BLE_MGR_GATTC_EXCHANGE_MTU_CMD = auto()
    BLE_MGR_GATTC_LAST_CMD = auto()


class BleMgrGattcDiscoverSvcCmd(BleMgrMsgBase):
    def __init__(self, conn_idx: int = 0, uuid: AttUuid = None) -> None:
        super().__init__(opcode=BLE_CMD_GATTC_OPCODE.BLE_MGR_GATTC_DISCOVER_SVC_CMD)
        self.conn_idx = conn_idx
        self.uuid = uuid


class BleMgrGattcDiscoverSvcRsp(BleMgrMsgBase):
    def __init__(self, status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED) -> None:
        super().__init__(opcode=BLE_CMD_GATTC_OPCODE.BLE_MGR_GATTC_DISCOVER_SVC_CMD)
        self.status = status
