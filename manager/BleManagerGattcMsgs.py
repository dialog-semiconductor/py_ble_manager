
from enum import IntEnum, auto
from ble_api.BleAtt import AttUuid
from ble_api.BleCommon import BLE_ERROR
from manager.BleManagerCommonMsgs import BLE_MGR_CMD_CAT, BleMgrMsgBase, BleMgrMsgRsp, BLE_CMD_GATTC_OPCODE


class BleMgrGattcDiscoverSvcCmd(BleMgrMsgBase):
    def __init__(self, conn_idx: int = 0, uuid: AttUuid = None) -> None:
        super().__init__(opcode=BLE_CMD_GATTC_OPCODE.BLE_MGR_GATTC_DISCOVER_SVC_CMD)
        self.conn_idx = conn_idx
        self.uuid = uuid


class BleMgrGattcDiscoverSvcRsp(BleMgrMsgRsp):
    def __init__(self, status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED) -> None:
        super().__init__(opcode=BLE_CMD_GATTC_OPCODE.BLE_MGR_GATTC_DISCOVER_SVC_CMD,
                         status=status)
