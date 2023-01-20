from enum import IntEnum

from ble_api.BleAtt import AttUuid, ATT_ERROR
from ble_api.BleCommon import BleEventBase, BLE_EVT_GATTC, BLE_ERROR
from ble_api.BleGatt import GATT_PROP


# Discovery type
class GATTC_DISCOVERY_TYPE(IntEnum):
    GATTC_DISCOVERY_TYPE_SVC = 0  # discovery services type
    GATTC_DISCOVERY_TYPE_INCLUDED = 1  # discovery included services type
    GATTC_DISCOVERY_TYPE_CHARACTERISTICS = 2  # discovery characteristics type
    GATTC_DISCOVERY_TYPE_DESCRIPTORS = 3  # discovery descriptors type


class GATTC_ITEM_TYPE(IntEnum):
    GATTC_ITEM_TYPE_NONE = 0  # invalid or unknown item
    GATTC_ITEM_TYPE_INCLUDE = 1  # included service
    GATTC_ITEM_TYPE_CHARACTERISTIC = 2  # characteristic
    GATTC_ITEM_TYPE_DESCRIPTOR = 3  # characteristic description


class GattcServiceData():
    def __init__(self,
                 start_h: int = 0,
                 end_h: int = 0):
        self.start_h = start_h
        self.end_h = end_h


class GattcCharacteristicData():
    def __init__(self,
                 value_handle: int = 0,
                 properties: int = 0):
        self.value_handle = value_handle
        self.properties = properties


class GattcItem():
    def __init__(self,
                 uuid: AttUuid = None,
                 handle: int = 0,
                 type: GATTC_ITEM_TYPE = GATTC_ITEM_TYPE.GATTC_ITEM_TYPE_NONE,
                 service_data: GattcServiceData = None,  # TODO sdk uses union for service data / char data. Use a ctype union?
                 char_data: GattcCharacteristicData = None):

        self.uuid = uuid
        self.handle = handle
        self.type = type
        self.service_data = service_data
        self.char_data = char_data


class BleEventGattcBrowseSvc(BleEventBase):
    def __init__(self,
                 conn_idx: int = 0,
                 uuid: AttUuid = None,
                 start_h: int = 0,
                 end_h: int = 0,
                 num_items: int = 0,
                 items: list[GattcItem] = None
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GATTC.BLE_EVT_GATTC_BROWSE_COMPLETED)
        self.conn_idx = conn_idx
        self.uuid = uuid if uuid else AttUuid()
        self.start_h = start_h
        self.end_h = end_h
        self.num_items = num_items
        self.items = items if items else []


class BleEventGattcBrowseCompleted(BleEventBase):
    def __init__(self,
                 conn_idx: int = 0,
                 status: int = 0  # TODO is there an enum for this?
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GATTC.BLE_EVT_GATTC_BROWSE_COMPLETED)
        self.conn_idx = conn_idx
        self.status = status


class BleEventGattcDiscoverChar(BleEventBase):
    def __init__(self,
                 conn_idx: int = 0,
                 uuid: AttUuid = None,
                 handle: int = 0,
                 value_handle: int = 0,
                 properties: int = 0,
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GATTC.BLE_EVT_GATTC_DISCOVER_CHAR)
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


class BleEventGattcDiscoverDesc(BleEventBase):
    def __init__(self,
                 conn_idx: int = 0,
                 uuid: AttUuid = None,
                 handle: int = 0
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GATTC.BLE_EVT_GATTC_DISCOVER_DESC)
        self.conn_idx = conn_idx
        self.uuid = uuid if uuid else AttUuid()
        self.handle = handle


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


class BleEventGattcReadCompleted(BleEventBase):
    def __init__(self,
                 conn_idx: int = 0,
                 handle: int = 0,
                 status: ATT_ERROR = ATT_ERROR.ATT_ERROR_OK,
                 offset: int = 0,
                 value: bytes = None,
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GATTC.BLE_EVT_GATTC_DISCOVER_SVC)
        self.conn_idx = conn_idx
        self.handle = handle
        self.status = status
        self.offset = offset
        self.value = value if value else bytes()


class BleEventGattcWriteCompleted(BleEventBase):
    def __init__(self,
                 conn_idx: int = 0,
                 handle: int = 0,
                 status: ATT_ERROR = ATT_ERROR.ATT_ERROR_OK,
                 operation: int = 0,
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GATTC.BLE_EVT_GATTC_WRITE_COMPLETED)
        self.conn_idx = conn_idx
        self.handle = handle
        self.status = status
        self.operation = operation
