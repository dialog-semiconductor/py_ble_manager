import argparse
import sys
import time
import py_ble_manager as ble


def main(com_port, peripheral_addr):
    central = ble.BleCentral(com_port)

    # Initialize the Pytohn BLE Framework
    central.init()

    # Start operating as a BLE Central
    central.start()

    # Convert the address string to a BdAddress
    peripheral_addr: ble.BdAddress = ble.BleUtils.str_to_bd_addr(peripheral_addr)
    # Set the connection parameters
    connection_params = ble.GapConnParams(interval_min_ms=50, interval_max_ms=70, slave_latency=0, sup_timeout_ms=420)
    # Initiate a connection
    central.connect(peripheral_addr, connection_params)

    conn_idx = 0
    while True:
        # Wait for asynchronous events to arrive. A timeout is set to allow for Keyboard interrupts
        evt = central.get_event(timeout=1)
        if evt:
            match evt.evt_code:

                # Print out data for the connected peripheral
                case ble.BLE_EVT_GAP.BLE_EVT_GAP_CONNECTED:
                    evt: ble.BleEventGapConnected
                    conn_idx = evt.conn_idx
                    print(f"Connected to: addr={ble.BleUtils.bd_addr_to_str(evt.peer_address)}, conn_idx={evt.conn_idx}")

                # Connection has completed. Print out the status, wait 3 seconds, and initiate a disconnect
                case ble.BLE_EVT_GAP.BLE_EVT_GAP_CONNECTION_COMPLETED:
                    evt: ble.BleEventGapConnectionCompleted
                    print(f"Connection completed: status={evt.status.name}")

                    # Sleep for 3 seconds before disconnecting
                    time.sleep(3)
                    central.disconnect(conn_idx=conn_idx)

                # Disconnected from peripheral
                case ble.BLE_EVT_GAP.BLE_EVT_GAP_DISCONNECTED:
                    evt: ble.BleEventGapDisconnected
                    print(f"Disconnected from addr={ble.BleUtils.bd_addr_to_str(evt.address)}")
                    sys.exit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='BLE Central Simple Connection',
                                     description='A simple example demonstrating connecting to a peripheral')

    parser.add_argument("com_port", type=str, help='COM port for your development kit')

    parser.add_argument("peripheral_addr", help='Addresss of peripheral, e.g. 48:23:35:00:1b:53,P')

    args = parser.parse_args()

    try:
        main(args.com_port, args.peripheral_addr)
    except KeyboardInterrupt:
        print("Exiting")
