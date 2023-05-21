import argparse
import sys
import py_ble_manager as ble


def main(com_port):
    central = ble.BleCentral(com_port)

    # Initialize the Python BLE Framework
    central.init()

    # Start operating as a BLE Central
    central.start()

    # Start a scan
    central.scan_start(type=ble.GAP_SCAN_TYPE.GAP_SCAN_ACTIVE,
                       mode=ble.GAP_SCAN_MODE.GAP_SCAN_GEN_DISC_MODE,
                       interval_ms=100,
                       window_ms=50,
                       filt_wlist=False,
                       filt_dupl=True)

    while True:
        # Wait for asynchronous events to arrive. A timeout is set to allow for Keyboard interrupts
        evt = central.get_event(timeout=1)
        if evt:
            match evt.evt_code:

                # Print out data for each advertisement received
                case ble.BLE_EVT_GAP.BLE_EVT_GAP_ADV_REPORT:
                    evt: ble.BleEventGapAdvReport
                    print(f"Advertisement: address={ble.BleUtils.bd_addr_to_str(evt.address)} "
                          + f"rssi={evt.rssi}, data={evt.data.hex()}")

                # When the scan is complete, exit
                case ble.BLE_EVT_GAP.BLE_EVT_GAP_SCAN_COMPLETED:
                    evt: ble.BleEventGapScanCompleted
                    print("Scan completed")
                    sys.exit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='BLE Central Simple Scan ',
                                     description='A simple example demonstrating scanning for peripherals')

    parser.add_argument("com_port", type=str, help='COM port for your development kit')

    args = parser.parse_args()

    try:
        main(args.com_port)
    except KeyboardInterrupt:
        print("Exiting")
