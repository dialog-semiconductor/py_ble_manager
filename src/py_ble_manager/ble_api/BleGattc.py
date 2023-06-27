from enum import IntEnum

from ..ble_api.BleAtt import AttUuid, ATT_ERROR
from ..ble_api.BleCommon import BleEventBase, BLE_EVT_GATTC, BLE_ERROR


class GATTC_DISCOVERY_TYPE(IntEnum):
    """GATT Discovery type
    """
    GATTC_DISCOVERY_TYPE_SVC = 0  # discovery services type
    GATTC_DISCOVERY_TYPE_INCLUDED = 1  # discovery included services type
    GATTC_DISCOVERY_TYPE_CHARACTERISTICS = 2  # discovery characteristics type
    GATTC_DISCOVERY_TYPE_DESCRIPTORS = 3  # discovery descriptors type


class GATTC_ITEM_TYPE(IntEnum):
    """Service item type
    """
    GATTC_ITEM_TYPE_NONE = 0  # invalid or unknown item
    GATTC_ITEM_TYPE_INCLUDE = 1  # included service
    GATTC_ITEM_TYPE_CHARACTERISTIC = 2  # characteristic
    GATTC_ITEM_TYPE_DESCRIPTOR = 3  # characteristic description


class GattcIncludedServiceData():
    """GATT Service data

    :ivar start_h: included service start handle
    :ivar end_h: included service end handle
    """

    def __init__(self,
                 start_h: int = 0,
                 end_h: int = 0):
        self.start_h = start_h
        self.end_h = end_h


class GattcCharacteristicData():
    """GATT Characteristic data

    :ivar value_handle: characteristic value handle
    :ivar properties: characteristic properties
    """

    def __init__(self,
                 value_handle: int = 0,
                 properties: int = 0):
        self.value_handle = value_handle
        self.properties = properties


class GattcItem():
    """Service item definition

    :ivar uuid: item uuid
    :ivar handle: item handle
    :ivar type: item type
    :ivar service_data: included service data
    :ivar char_data: characteristic data
    """

    def __init__(self,
                 uuid: AttUuid = None,
                 handle: int = 0,
                 type: GATTC_ITEM_TYPE = GATTC_ITEM_TYPE.GATTC_ITEM_TYPE_NONE,
                 service_data: GattcIncludedServiceData = None,  # note sdk uses union for service data / char data but using two members instead.
                 char_data: GattcCharacteristicData = None):

        self.uuid = uuid
        self.handle = handle
        self.type = type
        self.service_data = service_data
        self.char_data = char_data


class BleEventGattcBrowseSvc(BleEventBase):
    """Class for :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GATTC.BLE_EVT_GATTC_BROWSE_SVC` event

    :ivar evt_code: event code, :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GATTC.BLE_EVT_GATTC_BROWSE_SVC`
    :ivar conn_idx: connection index
    :ivar uuid: service uuid
    :ivar start_h: service start handle
    :ivar end_h: service end handle
    :ivar num_items: number of items in service
    :ivar items: items found in service
    """

    def __init__(self,
                 conn_idx: int = 0,
                 uuid: AttUuid = None,
                 start_h: int = 0,
                 end_h: int = 0,
                 num_items: int = 0,
                 items: list[GattcItem] = None
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GATTC.BLE_EVT_GATTC_BROWSE_SVC)
        self.conn_idx = conn_idx
        self.uuid = uuid if uuid else AttUuid()
        self.start_h = start_h
        self.end_h = end_h
        self.num_items = num_items
        self.items = items if items else []


class BleEventGattcBrowseCompleted(BleEventBase):
    """Class for :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GATTC.BLE_EVT_GATTC_BROWSE_COMPLETED` event

    :ivar evt_code: event code, :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GATTC.BLE_EVT_GATTC_BROWSE_COMPLETED`
    :ivar conn_idx: connection index
    :ivar status: browsing status
    """

    def __init__(self,
                 conn_idx: int = 0,
                 status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GATTC.BLE_EVT_GATTC_BROWSE_COMPLETED)
        self.conn_idx = conn_idx
        self.status = status


class BleEventGattcDiscoverChar(BleEventBase):
    """Class for :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GATTC.BLE_EVT_GATTC_DISCOVER_CHAR` event

    :ivar evt_code: event code, :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GATTC.BLE_EVT_GATTC_DISCOVER_CHAR`
    :ivar conn_idx: connection index
    :ivar uuid: characteristic UUID
    :ivar handle: characteristic handle
    :ivar value_handle: characteristic value handle
    :ivar properties: characteristic properties
    """

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
    """Class for :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GATTC.BLE_EVT_GATTC_DISCOVER_COMPLETED` event

    :ivar evt_code: event code, :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GATTC.BLE_EVT_GATTC_DISCOVER_COMPLETED`
    :ivar conn_idx: connection index
    :ivar type: discovery type
    :ivar status: discovery status
    """

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
    """Class for :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GATTC.BLE_EVT_GATTC_DISCOVER_DESC` event

    :ivar evt_code: event code, :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GATTC.BLE_EVT_GATTC_DISCOVER_DESC`
    :ivar conn_idx: connection index
    :ivar uuid: characteristic descriptor UUID
    :ivar handle: characteristic descriptor handle
    """

    def __init__(self,
                 conn_idx: int = 0,
                 uuid: AttUuid = None,
                 handle: int = 0
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GATTC.BLE_EVT_GATTC_DISCOVER_DESC)
        self.conn_idx = conn_idx
        self.uuid = uuid if uuid else AttUuid()
        self.handle = handle


class BleEventGattcDiscoverInclude(BleEventBase):
    """Class for :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GATTC.BLE_EVT_GATTC_DISCOVER_INCLUDE` event

    :ivar evt_code: event code, :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GATTC.BLE_EVT_GATTC_DISCOVER_INCLUDE`
    :ivar conn_idx: connection index
    :ivar handle: include attribute handle
    :ivar uuid: included service UUID
    :ivar start_h: included service start handle
    :ivar end_h: included service end handle
    """

    def __init__(self,
                 conn_idx: int = 0,
                 handle: int = 0,
                 uuid: AttUuid = None,
                 start_h: int = 0,
                 end_h: int = 0
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GATTC.BLE_EVT_GATTC_DISCOVER_INCLUDE)
        self.conn_idx = conn_idx
        self.handle = handle
        self.uuid = uuid if uuid else AttUuid()
        self.start_h = start_h
        self.end_h = end_h


class BleEventGattcDiscoverSvc(BleEventBase):
    """Class for :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GATTC.BLE_EVT_GATTC_DISCOVER_SVC` event

    :ivar evt_code: event code, :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GATTC.BLE_EVT_GATTC_DISCOVER_SVC`
    :ivar conn_idx: connection index
    :ivar uuid: service UUID
    :ivar start_h: service start handle
    :ivar end_h: service end handle
    """

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


class BleEventGattcNotification(BleEventBase):
    """Class for :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GATTC.BLE_EVT_GATTC_NOTIFICATION` event

    :ivar evt_code: event code, :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GATTC.BLE_EVT_GATTC_NOTIFICATION`
    :ivar conn_idx: connection index
    :ivar handle: attribute handle
    :ivar value: data value
    """

    def __init__(self,
                 conn_idx: int = 0,
                 handle: int = 0,
                 value: bytes = None,
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GATTC.BLE_EVT_GATTC_NOTIFICATION)
        self.conn_idx = conn_idx
        self.handle = handle
        self.value = value if value else bytes()


class BleEventGattcIndication(BleEventBase):
    """Class for :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GATTC.BLE_EVT_GATTC_INDICATION` event

    :ivar evt_code: event code, :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GATTC.BLE_EVT_GATTC_INDICATION`
    :ivar conn_idx: connection index
    :ivar handle: attribute handle
    :ivar value: data value
    """

    def __init__(self,
                 conn_idx: int = 0,
                 handle: int = 0,
                 value: bytes = None,
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GATTC.BLE_EVT_GATTC_INDICATION)
        self.conn_idx = conn_idx
        self.handle = handle
        self.value = value if value else bytes()


class BleEventGattcMtuChanged(BleEventBase):
    """Class for :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GATTC.BLE_EVT_GATTC_MTU_CHANGED` event

    :ivar evt_code: event code, :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GATTC.BLE_EVT_GATTC_MTU_CHANGED`
    :ivar conn_idx: connection index
    :ivar handle: current MTU
    """

    def __init__(self,
                 conn_idx: int = 0,
                 mtu: int = 0,
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GATTC.BLE_EVT_GATTC_MTU_CHANGED)
        self.conn_idx = conn_idx
        self.mtu = mtu


class BleEventGattcReadCompleted(BleEventBase):
    """Class for :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GATTC.BLE_EVT_GATTC_READ_COMPLETED` event

    :ivar evt_code: event code, :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GATTC.BLE_EVT_GATTC_READ_COMPLETED`
    :ivar conn_idx: connection index
    :ivar handle: attribute handle
    :ivar status: operation status
    :ivar offset: value offset
    :ivar value: data value
    """

    def __init__(self,
                 conn_idx: int = 0,
                 handle: int = 0,
                 status: ATT_ERROR = ATT_ERROR.ATT_ERROR_OK,
                 offset: int = 0,
                 value: bytes = None,
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GATTC.BLE_EVT_GATTC_READ_COMPLETED)
        self.conn_idx = conn_idx
        self.handle = handle
        self.status = status
        self.offset = offset
        self.value = value if value else bytes()


class BleEventGattcWriteCompleted(BleEventBase):
    """Class for :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GATTC.BLE_EVT_GATTC_WRITE_COMPLETED` event

    :ivar evt_code: event code, :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GATTC.BLE_EVT_GATTC_WRITE_COMPLETED`
    :ivar conn_idx: connection index
    :ivar handle: attribute handle (will be 0 for write_execute())
    :ivar status: operation status
    :ivar operation: operation type
    """

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
