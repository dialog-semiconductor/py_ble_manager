from adapter.BleAdapter import BleAdapter
from ble_api.BleApiBase import BleApiBase
from ble_api.BleAtt import att_uuid, ATT_PERM, ATT_ERROR
from ble_api.BleCommon import BLE_ERROR
from ble_api.BleGatt import GATT_SERVICE, GATT_PROP, GATT_EVENT
from ble_api.BleGatts import GATTS_FLAGS
from manager.BleManager import BleManager


class BleStorageApi(BleApiBase):

    def __init__(self, ble_manager: BleManager, ble_adapter: BleAdapter):
        super().__init__(ble_manager, ble_adapter)

    def put_int(self, conn_idx: int, key: int, value: int, persistent: bool) -> BLE_ERROR:

        error = BLE_ERROR.BLE_ERROR_FAILED
        dev = self.ble_manager.find_stored_device_by_conn_idx(conn_idx)
        if not dev:
            error = BLE_ERROR.BLE_ERROR_NOT_CONNECTED
        else:
            dev.app_value_put(key, persistent, value.to_bytes(4, byteorder='little'))
            error = BLE_ERROR.BLE_STATUS_OK

        return error

    def get_int(self, conn_idx: int, key: int) -> tuple[BLE_ERROR, int]:

        error = BLE_ERROR.BLE_ERROR_FAILED
        value_int = None

        dev = self.ble_manager.find_stored_device_by_conn_idx(conn_idx)
        if not dev:
            error = BLE_ERROR.BLE_ERROR_NOT_CONNECTED
        else:
            value_bytes = dev.app_value_get(key)
            if not value_bytes:
                error = BLE_ERROR.BLE_ERROR_NOT_FOUND
            else:
                value_int = int.from_bytes(value_bytes, 'little')
                error = BLE_ERROR.BLE_STATUS_OK

        return error, value_int
