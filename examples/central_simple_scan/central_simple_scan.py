import argparse
import sys
import python_gtl_thread as ble


def main(com_port):
    central = ble.BleCentral(com_port)

    # Initialize the Pytohn BLE Framework
    central.init()

    # Start operating as a BLE Central
    central.start()

    # Start a scan
    central.scan_start(type=ble.GAP_SCAN_TYPE.GAP_SCAN_ACTIVE,
                       mode=ble.GAP_SCAN_MODE.GAP_SCAN_GEN_DISC_MODE,
                       interval=160,
                       window=80,
                       filt_wlist=False,
                       filt_dupl=True)

    while True:
        # Wait for asynchronus events to arrive
        evt = central.get_event()

        # Print out data for each advertisement received
        if evt.evt_code == ble.BLE_EVT_GAP.BLE_EVT_GAP_ADV_REPORT:
            # Print out received advertisement data
            evt: ble.BleEventGapAdvReport
            print(f"Advertisment: address={ble.BleUtils.bd_addr_to_str(evt.address)} "
                  + f"rssi={evt.rssi}, data={evt.data.hex()}")

        # When the scan is complete, exit
        elif evt.evt_code == ble.BLE_EVT_GAP.BLE_EVT_GAP_SCAN_COMPLETED:
            evt: ble.BleEventGapScanCompleted
            print("Scan completed")
            sys.exit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='main_central',
                                     description='BLE Central Simple Scan')

    parser.add_argument("com_port", type=str, help='COM port for your development kit')

    args = parser.parse_args()

    try:
        main(args.com_port)
    except KeyboardInterrupt:
        print("Exiting")
