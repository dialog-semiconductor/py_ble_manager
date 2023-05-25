import argparse
import sys
import time
import py_ble_manager as ble


def main(com_port):
    peripheral = ble.BlePeripheral(com_port)

    # Initialize the Python BLE Framework
    peripheral.init()

    # Start operating as a BLE peripheral
    peripheral.start()

    # Set the device name
    dev_name = "PY_BLE_MANAGER"
    peripheral.device_name_set(dev_name)

    # Set the name in the advertising data
    local_name_ad = ble.BleAdvData(ble.GAP_DATA_TYPE.GAP_DATA_TYPE_LOCAL_NAME, bytes(dev_name, 'utf-8)'))
    adv_ad_list = [local_name_ad]
    peripheral.advertising_data_set(adv_ad_list)
    print(f"Advertising as: {dev_name}")

    # Set the advertising interval
    peripheral.set_advertising_interval(adv_intv_min_ms=20, adv_intv_max_ms=30)

    # Start advertising
    peripheral.advertising_start()

    adv_start_time = time.time()
    while True:
        # Wait for asynchronous events to arrive. A timeout is set to allow for Keyboard interrupts
        evt = peripheral.get_event(timeout=1)
        now = time.time()

        if evt:
            match evt.evt_code:
                case _:
                    peripheral.handle_event_default(evt)

        # after 20 seconds have passed, stop advertising and exit the example
        if now - adv_start_time > 20:
            peripheral.advertising_stop()
            print("Adverting stopped")
            print("Exiting...")
            sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='BLE Peripheral Simple Advertise ',
                                     description='A simple example demonstrating advertising')

    parser.add_argument("com_port", type=str, help='COM port for your development kit')

    args = parser.parse_args()

    try:
        main(args.com_port)
    except KeyboardInterrupt:
        print("Exiting")
