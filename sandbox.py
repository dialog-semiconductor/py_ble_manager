import py_ble_manager as ble
test = ble.BLE_ERROR(2) if 2 in ble.BLE_ERROR.__members__.values() else ble.BLE_ERROR.BLE_ERROR_FAILED
print(test )