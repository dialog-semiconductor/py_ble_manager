from enum import IntEnum

from ..ble_api.BleCommon import BleEventBase, BLE_EVT_GATTS
from ..ble_api.BleGatt import GATT_EVENT


# GATT Server flags
class GATTS_FLAG(IntEnum):
    """GATTS Flag to indicate if attribute supports read indications
    """
    GATTS_FLAG_CHAR_NO_READ_REQ = 0x00
    GATTS_FLAG_CHAR_READ_REQ = 0x01        # enable ::BLE_EVT_GATTS_READ_REQ for attribute


class BleEventGattsEventSent(BleEventBase):
    """Class for :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GATTS.BLE_EVT_GATTS_EVENT_SENT` event

    :ivar evt_code: event code, :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GATTS.BLE_EVT_GATTS_EVENT_SENT`
    :ivar conn_idx: connection index
    :ivar handle: attribute handle
    :ivar type: event type
    :ivar status: event status
    """

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
    """Class for :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GATTS.BLE_EVT_GATTS_PREPARE_WRITE_REQ` event

    :ivar evt_code: event code, :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GATTS.BLE_EVT_GATTS_PREPARE_WRITE_REQ`
    :ivar conn_idx: connection index
    :ivar handle: attribute handle
    """

    def __init__(self,
                 conn_idx: int = 0,
                 handle: int = 0,
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GATTS.BLE_EVT_GATTS_PREPARE_WRITE_REQ)
        self.conn_idx = conn_idx
        self.handle = handle


class BleEventGattsReadReq(BleEventBase):
    """Class for :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GATTS.BLE_EVT_GATTS_READ_REQ` event

    :ivar evt_code: event code, :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GATTS.BLE_EVT_GATTS_READ_REQ`
    :ivar conn_idx: connection index
    :ivar handle: attribute handle
    :ivar offset: attribute value offset
    """

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
    """Class for :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GATTS.BLE_EVT_GATTS_WRITE_REQ` event

    :ivar evt_code: event code, :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GATTS.BLE_EVT_GATTS_WRITE_REQ`
    :ivar conn_idx: connection index
    :ivar handle: attribute handle
    :ivar offset: attribute value offset
    :ivar offset: attribute value
    """

    def __init__(self,
                 conn_idx: int = 0,
                 handle: int = 0,
                 offset: int = 0,
                 value: bytes = None,
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GATTS.BLE_EVT_GATTS_WRITE_REQ)
        self.conn_idx = conn_idx
        self.handle = handle
        self.offset = offset
        self.value = value if value else bytes()
