
from enum import IntEnum, auto
from ble_api.BleAtt import AttUuid
from ble_api.BleCommon import BLE_ERROR
from manager.BleManagerCommonMsgs import BLE_MGR_CMD_CAT, BleMgrMsgBase, BleMgrMsgRsp, BLE_CMD_GATTC_OPCODE


class BleMgrGattcDiscoverCharCmd(BleMgrMsgBase):
    def __init__(self,
                 conn_idx: int = 0,
                 start_h: int = 0,
                 end_h: int = 0,
                 uuid: AttUuid = None) -> None:
        super().__init__(opcode=BLE_CMD_GATTC_OPCODE.BLE_MGR_GATTC_DISCOVER_CHAR_CMD)
        self.conn_idx = conn_idx
        self.start_h = start_h
        self.end_h = end_h
        self.uuid = uuid


class BleMgrGattcDiscoverCharRsp(BleMgrMsgRsp):
    def __init__(self, status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED) -> None:
        super().__init__(opcode=BLE_CMD_GATTC_OPCODE.BLE_MGR_GATTC_DISCOVER_CHAR_CMD,
                         status=status)


class BleMgrGattcDiscoverSvcCmd(BleMgrMsgBase):
    def __init__(self, conn_idx: int = 0, uuid: AttUuid = None) -> None:
        super().__init__(opcode=BLE_CMD_GATTC_OPCODE.BLE_MGR_GATTC_DISCOVER_SVC_CMD)
        self.conn_idx = conn_idx
        self.uuid = uuid


class BleMgrGattcDiscoverSvcRsp(BleMgrMsgRsp):
    def __init__(self, status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED) -> None:
        super().__init__(opcode=BLE_CMD_GATTC_OPCODE.BLE_MGR_GATTC_DISCOVER_SVC_CMD,
                         status=status)
