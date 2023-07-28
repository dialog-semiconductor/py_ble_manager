import argparse
import sys
import time
import threading
import py_ble_manager as ble


def connection_timeout_cb(central: ble.BleCentral, timeout_s: int):
    print(f"Peripheral not found in {timeout_s} seconds. Cancelling connection.")
    central.connect_cancel()


def main(com_port, peripheral_addr_str: str, timeout_s: int):
    central = ble.BleCentral(com_port)

    # Initialize the Pytohn BLE Framework
    central.init()

    # Start operating as a BLE Central
    central.start()

    # Convert the address string to a BdAddress
    peripheral_addr: ble.BdAddress = ble.BleUtils.str_to_bd_addr(peripheral_addr_str)
    # Set the connection parameters
    connection_params = ble.GapConnParams(interval_min_ms=50, interval_max_ms=70, slave_latency=0, sup_timeout_ms=420)
    # Initiate a connection
    print(f"Sending connection request to: {peripheral_addr_str}")
    central.connect(peripheral_addr, connection_params)

    # Create a timer to cancel the connection if the peripheral is not found
    connection_timer = threading.Timer(timeout_s, connection_timeout_cb, [central, timeout_s])
    connection_timer.start()

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

                # Connection has completed.
                case ble.BLE_EVT_GAP.BLE_EVT_GAP_CONNECTION_COMPLETED:
                    evt: ble.BleEventGapConnectionCompleted
                    # Print out the status
                    print(f"Connection completed: status={evt.status.name}")

                    if evt.status == ble.BLE_ERROR.BLE_STATUS_OK:
                        # Successful connection

                        # Cancel the connection timeout timer
                        connection_timer.cancel()

                        # Sleep for 3 seconds before disconnecting
                        time.sleep(3)
                        central.disconnect(conn_idx=conn_idx)
                    else:
                        # The connection was cancelled, exit
                        sys.exit(1)

                # Disconnected from peripheral
                case ble.BLE_EVT_GAP.BLE_EVT_GAP_DISCONNECTED:
                    evt: ble.BleEventGapDisconnected
                    print(f"Disconnected from addr={ble.BleUtils.bd_addr_to_str(evt.address)}")
                    sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='BLE Central Simple Connection',
                                     description='A simple example demonstrating connecting to a peripheral')

    parser.add_argument("com_port", type=str, help='COM port for your development kit')

    parser.add_argument("peripheral_addr", type=str, help='Addresss of peripheral, e.g. 48:23:35:00:1b:53,P')

    parser.add_argument("timeout_s", type=int, help='Time (in seconds) to wait for a connection to be established before cancelling the connection')

    args = parser.parse_args()

    try:
        main(args.com_port, args.peripheral_addr, args.timeout_s)
    except KeyboardInterrupt:
        print("Exiting")
