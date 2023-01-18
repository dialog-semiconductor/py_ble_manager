from enum import IntEnum

from ble_api.BleAtt import AttUuid
from ble_api.BleCommon import BleEventBase, BLE_EVT_GATTC, BLE_ERROR
from ble_api.BleGatt import GATT_PROP

# Discovery type
class GATTC_DISCOVERY_TYPE(IntEnum):
    GATTC_DISCOVERY_TYPE_SVC = 0  # discovery services type
    GATTC_DISCOVERY_TYPE_INCLUDED = 1  # discovery included services type
    GATTC_DISCOVERY_TYPE_CHARACTERISTICS = 2  # discovery characteristics type
    GATTC_DISCOVERY_TYPE_DESCRIPTORS = 3  # discovery descriptors type


class BleEventGattcDiscoverChar(BleEventBase):
    def __init__(self,
                 conn_idx: int = 0,
                 uuid: AttUuid = None,
                 handle: int = 0,
                 value_handle: int = 0,
                 properties: int = 0,
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GATTC.BLE_EVT_GATTC_DISCOVER_COMPLETED)
        self.conn_idx = conn_idx
        self.uuid = uuid if uuid else AttUuid()
        self.handle = handle
        self.value_handle = value_handle
        self.properties = properties


class BleEventGattcDiscoverCompleted(BleEventBase):
    def __init__(self,
                 conn_idx: int = 0,
                 type: GATTC_DISCOVERY_TYPE = GATTC_DISCOVERY_TYPE.GATTC_DISCOVERY_TYPE_SVC,
                 status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED,
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GATTC.BLE_EVT_GATTC_DISCOVER_COMPLETED)
        self.conn_idx = conn_idx
        self.type = type
        self.status = status


class BleEventGattcDiscoverSvc(BleEventBase):
    def __init__(self,
                 conn_idx: int = 0,
                 uuid: AttUuid = None,
                 start_h: int = 0,
                 end_h: int = 0,
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GATTC.BLE_EVT_GATTC_DISCOVER_SVC)
        self.conn_idx = conn_idx
        self.uuid = uuid if uuid else AttUuid()
        self.start_h = start_h
        self.end_h = end_h

