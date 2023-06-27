from ..ble_api.BleApiBase import BleApiBase
from ..ble_api.BleCommon import BLE_ERROR
from ..manager.BleManager import BleManager


class BleStorageApi(BleApiBase):

    def __init__(self, ble_manager: BleManager):
        super().__init__(ble_manager)

    def get_buffer(self, conn_idx: int, key: int) -> tuple[bytes, BLE_ERROR]:
        return self._ble_manager.storage_get_buffer(conn_idx, key)

    def get_int(self, conn_idx: int, key: int) -> tuple[int, BLE_ERROR]:
        return self._ble_manager.storage_get_int(conn_idx, key)

    def put_buffer(self, conn_idx: int, key: int, value: bytes, persistent: bool) -> BLE_ERROR:
        return self._ble_manager.storage_put_buffer(conn_idx, key, value, persistent)

    def put_int(self, conn_idx: int, key: int, value: int, persistent: bool) -> BLE_ERROR:
        return self._ble_manager.storage_put_int(conn_idx, key, value, persistent)