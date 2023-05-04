from enum import IntEnum

from ..ble_api.BleCommon import BleEventBase, BLE_EVT_GATTS
from ..ble_api.BleGatt import GATT_EVENT


# TODO rename BLE_GATTS_FLAGS
# GATT Server flags
class GATTS_FLAGS(IntEnum):
    GATTS_FLAG_CHAR_NO_READ_REQ = 0x00  # TODO need better name
    GATTS_FLAG_CHAR_READ_REQ = 0x01        # enable ::BLE_EVT_GATTS_READ_REQ for attribute


class BleEventGattsEventSent(BleEventBase):
    def __init__(self,
                 conn_idx: int = 0,
                 handle: int = 0,
                 type: GATT_EVENT = GATT_EVENT.GATT_EVENT_NOTIFICATION,
                 status: bool = False
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GATTS.BLE_EVT_GATTS_EVENT_SENT)
        self.conn_idx = conn_idx
        self.handle = handle
        self.type = type
        self.status = status


class BleEventGattsPrepareWriteReq(BleEventBase):
    def __init__(self,
                 conn_idx: int = 0,
                 handle: int = 0,
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GATTS.BLE_EVT_GATTS_PREPARE_WRITE_REQ)
        self.conn_idx = conn_idx
        self.handle = handle


class BleEventGattsReadReq(BleEventBase):
    def __init__(self,
                 conn_idx: int = 0,
                 handle: int = 0,
                 offset: int = 0,
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GATTS.BLE_EVT_GATTS_READ_REQ)
        self.conn_idx = conn_idx
        self.handle = handle
        self.offset = offset


class BleEventGattsWriteReq(BleEventBase):
    def __init__(self,
                 conn_idx: int = 0,
                 handle: int = 0,
                 offset: int = 0,
                 # length: int = 0,
                 value: bytes = None,
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GATTS.BLE_EVT_GATTS_WRITE_REQ)
        self.conn_idx = conn_idx
        self.handle = handle
        self.offset = offset
        # self.length = length
        self.value = value if value else bytes()
