import python_gtl_thread as ble
test = ble.BLE_ERROR(5) if 5 in ble.BLE_ERROR.__members__.values() else ble.BLE_ERROR.BLE_ERROR_FAILED
print(test )