import argparse
import sys
import time
import python_gtl_thread as ble

def main(com_port, peripheral_addr):
    central = ble.BleCentral(com_port)

    # Initialize the Pytohn BLE Framework
    central.init()

    # Start operating as a BLE Central 
    central.start()

    peripheral_addr = ble.BleUtils.str_to_bd_addr(peripheral_addr) 
    connection_params = ble.GapConnParams(interval_min_ms=50, interval_max_ms=70, slave_latency=0, sup_timeout_ms=420)
    central.connect(peripheral_addr, connection_params)

    conn_idx = 0
    while True:
        evt = central.get_event()
        if evt.evt_code == ble.BLE_EVT_GAP.BLE_EVT_GAP_CONNECTED:
            evt: ble.BleEventGapConnected
            conn_idx = evt.conn_idx
            print(f"Connected to: addr={ble.BleUtils.bd_addr_to_str(evt.peer_address)}, conn_idx={evt.conn_idx}")

        elif evt.evt_code == ble.BLE_EVT_GAP.BLE_EVT_GAP_CONNECTION_COMPLETED:
            evt: ble.BleEventGapConnectionCompleted
            print(f"Connection completed: status={evt.status.name}")

            # Sleep for 3 seconds before disconnecting
            time.sleep(3)
            central.disconect(conn_idx=conn_idx)

        elif evt.evt_code == ble.BLE_EVT_GAP.BLE_EVT_GAP_DISCONNECTED:
            print(f"Disconnected from addr={ble.BleUtils.bd_addr_to_str(evt.address)}")
            sys.exit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='main_central',
                                     description='BLE Central Simple Connection')

    parser.add_argument("com_port", type=str, help='COM port for your development kit')

    parser.add_argument("peripheral_addr", help='Addresss of peripheral, e.g. 48:23:35:00:1b:53,P')

    args = parser.parse_args()

    try:
        main(args.com_port, args.peripheral_addr)
    except KeyboardInterrupt:
        print("Exiting")