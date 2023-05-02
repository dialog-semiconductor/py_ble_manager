import argparse
import concurrent.futures
import threading
import time
import queue
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.patch_stdout import patch_stdout

# TODO rethink relative import
import sys
from pathlib import Path
HERE = Path(__file__).parent
sys.path.append(str(HERE / '../../'))

import ble_devices as ble

# TODO need to rethink how configuration
ble.dg_configBLE_CENTRAL = 1
ble.dg_configBLE_PERIPHERAL = 0


def main(com_port: str):
    ble_command_q = queue.Queue()
    ble_response_q = queue.Queue()
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
    # start 2 tasks:
    #   one for handling command line input

    concurrent.futures.wait([#executor.submit(user_main),
                            executor.submit(console, ble_command_q, ble_response_q),
                            executor.submit(ble_task, com_port, ble_command_q, ble_response_q)])


def console(ble_command_q: queue.Queue, ble_response_q: queue.Queue):
    commands = ['GAPSCAN',
                'GAPCONNECT',
                'GAPBROWSE',
                'GAPDISCONNECT',
                'GATTWRITE',
                'GATTREAD',
                'GATTWRITENORESP',
                'GAPPAIR',
                'GAPSETCONNPARAM',
                'PASSKEYENTRY',
                'YESNOTENTRY']
    commands.sort()
    word_completer = WordCompleter(commands, ignore_case=True)

    session = PromptSession(completer=word_completer)
    while True:
        with patch_stdout():
            input = session.prompt('>>> ')
            ble_command_q.put_nowait(input)
            response = ble_response_q.get()
            print(f"<<< {response}")


def ble_task(com_port: str, command_q: queue.Queue, response_q: queue.Queue):

    services = ble.SearchableQueue()

    # initalize central device
    central = ble.BleCentral(com_port, gtl_debug=False)
    central.init()
    central.start()
    central.set_io_cap(ble.GAP_IO_CAPABILITIES.GAP_IO_CAP_KEYBOARD_DISP)

    # create tasks for:
    #   hanlding commands from the console
    #   responding to BLE events
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
    console_command_task = executor.submit(command_q.get)
    ble_event_task = executor.submit(central.get_event)
    pending = [ble_event_task, console_command_task]

    while True:
        # Wait for a console command or BLE event to occur
        done, pending = concurrent.futures.wait(pending, return_when=concurrent.futures.FIRST_COMPLETED)

        for task in done:
            # Handle command line input
            if task is console_command_task:
                command: str = task.result()
                error = handle_console_command(command, central)

                if error == ble.BLE_ERROR.BLE_STATUS_OK:
                    response = "OK"
                else:
                    response = f"ERROR {error}"
                response_q.put_nowait(str(response))

                # restart console command task
                console_command_task = executor.submit(command_q.get)
                pending.add(console_command_task)

            # Handle and BLE events that have occurred
            if task is ble_event_task:
                evt: ble.BleEventBase = task.result()  # TODO how does timeout error affect result
                handle_ble_event(central, evt, services)  # TODO services belongs in central??

                # restart ble event task
                ble_event_task = executor.submit(central.get_event)
                pending.add(ble_event_task)


def handle_console_command(command: str, central: ble.BleCentral) -> ble.BLE_ERROR:
    error = ble.BLE_ERROR.BLE_ERROR_FAILED
    args = command.split()
    if len(args) > 0:
        ble_func = args[0]
        match ble_func:
            case 'GAPSCAN':
                error = central.scan_start(ble.GAP_SCAN_TYPE.GAP_SCAN_ACTIVE,
                                                 ble.GAP_SCAN_MODE.GAP_SCAN_GEN_DISC_MODE,
                                                 160,
                                                 80,
                                                 False,
                                                 True)

            case "GAPCONNECT":
                if len(args) == 1:  # TODO this case just to avoid having to enter bd addr  # 531B00352348 964700352348
                    periph_bd = ble.BdAddress(ble.BLE_ADDR_TYPE.PUBLIC_ADDRESS, bytes.fromhex("531B00352348"))  # addr is backwards
                    periph_conn_params = ble.GapConnParams(50, 70, 0, 420)
                    error = central.connect(periph_bd, periph_conn_params)
                if len(args) == 2:  # TODO pass in addr 48:23:35:00:1b:53
                    # bd_info = args[1].strip(',')
                    # bd_type =  if bd_info[1] == 'P' else BLE_ADDR_TYPE.PRIVATE_ADDRESS
                    periph_bd = str_to_bd_addr(ble.BLE_ADDR_TYPE.PUBLIC_ADDRESS, args[1])
                    periph_conn_params = ble.GapConnParams(50, 70, 0, 420)
                    error = central.connect(periph_bd, periph_conn_params)

            case "GAPBROWSE":
                if len(args) == 2:
                    conn_idx = int(args[1])
                    error = central.browse(conn_idx, None)

            case "GAPDISCONNECT":
                if len(args) >= 2:
                    conn_idx = int(args[1])
                    if len(args) == 3:
                        reason = ble.BLE_HCI_ERROR(int(args[2]))
                        if reason == ble.BLE_HCI_ERROR.BLE_HCI_ERROR_NO_ERROR:
                            reason = ble.BLE_HCI_ERROR.BLE_HCI_ERROR_REMOTE_USER_TERM_CON
                    else:
                        reason = ble.BLE_HCI_ERROR.BLE_HCI_ERROR_REMOTE_USER_TERM_CON
                    error = central.disconect(conn_idx, reason)

            case "GATTWRITE":
                if len(args) == 4:
                    conn_idx = int(args[1])
                    handle = int(args[2])
                    value = bytes.fromhex(args[3])  # TODO requires leading 0 for 0x0-0xF
                    error = central.write(conn_idx, handle, 0, value)

            case "GATTWRITENORESP":
                if len(args) == 5:
                    conn_idx = int(args[1])
                    handle = int(args[2])
                    signed = bool(int(args[3]))
                    value = bytes.fromhex(args[4])  # TODO requires leading 0 for 0x0-0xF
                    error = central.write_no_resp(conn_idx, handle, signed, value)

            case "GATTWRITEPREPARE":
                # TODO not receiving GATTC_CMP_EVT after sending GattcWriteCmd
                if len(args) == 4:
                    conn_idx = int(args[1])
                    handle = int(args[2])
                    value = bytes.fromhex(args[3])
                    error = central.write_prepare(conn_idx, handle, 0, value)

            case "GATTWRITEEXECUTE":
                if len(args) == 3:
                    conn_idx = int(args[1])
                    execute = bool(int(args[2]))
                    error = central.write_execute(conn_idx, execute)

            case "GATTREAD":  # TODO char handle displayed by browse is acutally the declaration. The value is +1
                if len(args) == 3:
                    conn_idx = int(args[1])
                    handle = int(args[2])
                    error = central.read(conn_idx, handle, 0)

            case 'GAPSETCONNPARAM':
                if len(args) == 6:
                    conn_idx = int(args[1])
                    conn_params = ble.GapConnParams()
                    conn_params.interval_min = int(args[2])
                    conn_params.interval_max = int(args[3])
                    conn_params.slave_latency = int(args[4])
                    conn_params.sup_timeout = int(args[5])
                    error = central.conn_param_update(conn_idx, conn_params)

            case 'GAPPAIR':
                if len(args) == 3:
                    conn_idx = int(args[1])
                    bond = bool(int(args[2]))
                    error = central.pair(conn_idx, bond)

            case 'PASSKEYENTRY':
                if len(args) == 4:
                    conn_idx = int(args[1])
                    accept = bool(int(args[2]))
                    passkey = int(args[3])
                    error = central.passkey_reply(conn_idx, accept, passkey)

            case 'YESNOTENTRY':
                if len(args) == 3:
                    conn_idx = int(args[1])
                    accept = bool(int(args[2]))
                    error = central.numeric_reply(conn_idx, accept)

            case _:
                pass

    return error


def handle_ble_event(central: ble.BleCentral, evt: ble.BleEventBase, services):
    match evt.evt_code:
        case ble.BLE_EVT_GAP.BLE_EVT_GAP_ADV_REPORT:
            handle_evt_gap_adv_report(central, evt)
        case ble.BLE_EVT_GAP.BLE_EVT_GAP_SCAN_COMPLETED:
            handle_evt_scan_completed(central, evt)
        case ble.BLE_EVT_GAP.BLE_EVT_GAP_CONNECTED:
            handle_evt_gap_connected(central, evt)
        case ble.BLE_EVT_GAP.BLE_EVT_GAP_CONNECTION_COMPLETED:
            handle_evt_gap_connection_compelted(central, evt)
        case ble.BLE_EVT_GAP.BLE_EVT_GAP_DISCONNECTED:
            handle_evt_gap_disconnected(central, evt)
        case ble.BLE_EVT_GATTC.BLE_EVT_GATTC_DISCOVER_SVC:
            handle_evt_gattc_discover_svc(central, evt, services)
        case ble.BLE_EVT_GATTC.BLE_EVT_GATTC_DISCOVER_COMPLETED:
            if evt.type == ble.GATTC_DISCOVERY_TYPE.GATTC_DISCOVERY_TYPE_SVC:
                handle_evt_gattc_discover_completed(central, evt, services)
        case ble.BLE_EVT_GATTC.BLE_EVT_GATTC_DISCOVER_CHAR:
            handle_evt_gattc_discover_char(central, evt)
        case ble.BLE_EVT_GATTC.BLE_EVT_GATTC_DISCOVER_CHAR:
            handle_evt_gattc_discover_char(central, evt)
        case ble.BLE_EVT_GATTC.BLE_EVT_GATTC_DISCOVER_DESC:
            handle_evt_gattc_discover_desc(central, evt)
        case ble.BLE_EVT_GATTC.BLE_EVT_GATTC_BROWSE_SVC:
            handle_evt_gattc_browse_svc(central, evt)
        case ble.BLE_EVT_GATTC.BLE_EVT_GATTC_BROWSE_COMPLETED:
            handle_evt_gattc_browse_completed(central, evt)
        case ble.BLE_EVT_GATTC.BLE_EVT_GATTC_NOTIFICATION:
            handle_evt_gattc_notification(central, evt)
        case ble.BLE_EVT_GATTC.BLE_EVT_GATTC_READ_COMPLETED:
            handle_evt_gattc_read_completed(central, evt)
        case ble.BLE_EVT_GATTC.BLE_EVT_GATTC_WRITE_COMPLETED:
            handle_evt_gattc_write_completed(central, evt)
        case ble.BLE_EVT_GAP.BLE_EVT_GAP_CONN_PARAM_UPDATED:
            handle_evt_gap_conn_param_updated(central, evt)
        case ble.BLE_EVT_GAP.BLE_EVT_GAP_CONN_PARAM_UPDATE_COMPLETED:
            handle_evt_gap_conn_param_update_compelted(central, evt)
        case ble.BLE_EVT_GAP.BLE_EVT_GAP_PAIR_REQ:
            handle_evt_gap_pair_req(central, evt)
        case ble.BLE_EVT_GAP.BLE_EVT_GAP_PAIR_COMPLETED:
            handle_evt_gap_pair_completed(central, evt)
        case ble.BLE_EVT_GAP.BLE_EVT_GAP_SEC_LEVEL_CHANGED:
            handle_evt_gap_sec_level_changed(central, evt)
        case ble.BLE_EVT_GAP.BLE_EVT_GAP_PEER_FEATURES:
            handle_evt_gap_peer_features(central, evt)
        case ble.BLE_EVT_GAP.BLE_EVT_GAP_PEER_VERSION:
            handle_evt_gap_peer_version(central, evt)
        case ble.BLE_EVT_GAP.BLE_EVT_GAP_PASSKEY_NOTIFY:
            handle_evt_gap_passkey_notify(central, evt)
        case ble.BLE_EVT_GAP.BLE_EVT_GAP_ADDRESS_RESOLVED:
            handle_evt_gap_address_resolved(central, evt)
        case ble.BLE_EVT_GAP.BLE_EVT_GAP_NUMERIC_REQUEST:
            handle_evt_gap_numeric_request(central, evt)
        case _:
            print(f"Ble Task unhandled event: {evt}")
            central.handle_event_default(evt)


def handle_evt_gap_passkey_notify(central, evt: ble.BleEventGapPasskeyNotify):
    print(f"Passkey notify: conn_idx={evt.conn_idx}, passkey={evt.passkey}")


def handle_evt_gap_peer_features(central, evt: ble.BleEventGapPeerFeatures):
    print(f"Peer features: conn_idx={evt.conn_idx}, features={evt.le_features.hex()}")


def handle_evt_gap_peer_version(central, evt: ble.BleEventGapPeerVersion):
    print(f"Peer version: conn_idx={evt.conn_idx}, lmp_version={evt.lmp_version} "
          + f"company_id={evt.company_id}, lmp_subversion={evt.lmp_subversion}")


def handle_evt_gap_sec_level_changed(central, evt: ble.BleEventGapSecLevelChanged):
    print(f"Security level changed: sec_level={evt.level.name}")


def handle_evt_gap_pair_req(central, evt: ble.BleEventGapPairReq):
    print(f"Pair Request: evt={evt}")


def handle_evt_gap_pair_completed(central, evt: ble.BleEventGapPairCompleted):
    print(f"Pairing compelte: conn_idx={evt.conn_idx}, bond={evt.bond}, mitm={evt.mitm}, status={evt.status.name}")


def handle_evt_gap_conn_param_updated(central, evt: ble.BleEventGapConnParamUpdated):
    print(f"Connection Parameters updated: evt={evt}")


def handle_evt_gap_conn_param_update_compelted(central, evt: ble.BleEventGapConnParamUpdateCompleted):
    print(f"Connection Parameters update completed: evt={evt}")


def handle_evt_gap_connection_compelted(central, evt: ble.BleEventGapConnectionCompleted):
    print(f"Connection completed: status={evt.status.name}")


def handle_evt_scan_completed(central: ble.BleCentral, evt: ble.BleEventGapScanCompleted):
    # TODO status is always coming back BLE_ERROR_TIMEOUT. Is that correct?
    print(f"Scan completed: status={evt.status.name}")


def handle_evt_gap_adv_report(central: ble.BleCentral, evt: ble.BleEventGapAdvReport):
    print(f"Advertisment: address={bd_addr_to_str(evt.address)} addr_type={evt.address.addr_type} "
          + f"rssi={evt.rssi}, data={evt.data.hex()}")


def handle_evt_gattc_discover_svc(central: ble.BleCentral, evt: ble.BleEventGattcDiscoverSvc, services: ble.SearchableQueue):
    service = ble.BleServiceBase()
    service.start_h = evt.start_h
    service.end_h = evt.end_h
    services.push(service)


def handle_evt_gattc_discover_completed(central: ble.BleCentral, evt: ble.BleEventGattcDiscoverCompleted, services: ble.SearchableQueue):
    print(f"main_central handle_evt_gattc_discover_completed unimplemented. evt={evt}")

    if evt.type == ble.GATTC_DISCOVERY_TYPE.GATTC_DISCOVERY_TYPE_SVC:
        service: ble.BleServiceBase = services.peek_back()
        central.discover_characteristics(evt.conn_idx, service.start_h, service.end_h, None)

    # TODO discover included services

    elif evt.type == ble.GATTC_DISCOVERY_TYPE.GATTC_DISCOVERY_TYPE_CHARACTERISTICS:
        # central.discover_descriptors(evt.conn_idx. )
        pass


def handle_evt_gattc_discover_char(central: ble.BleCentral, evt: ble.BleEventGattcDiscoverChar):
    print(f"main_central handle_evt_gattc_discover_char unimplemented. evt={evt}")
    pass


def handle_evt_gattc_discover_desc(central: ble.BleCentral, evt: ble.BleEventGattcDiscoverDesc):
    print(f"main_central handle_evt_gattc_discover_desc unimplemented. evt={evt}")
    pass


def handle_evt_gap_connected(central: ble.BleCentral, evt: ble.BleEventGapConnected):
    print(f"Connected to: addr={bd_addr_to_str(evt.peer_address)}, conn_idx={evt.conn_idx}")


def handle_evt_gap_disconnected(central: ble.BleCentral, evt: ble.BleEventGapDisconnected):
    # TODO addr to hex str
    print(f"Disconnected from to: addr={bd_addr_to_str(evt.address)}")


def handle_evt_gattc_notification(central, evt: ble.BleEventGattcNotification):
    print(f"Received Notification: conn_idx={evt.conn_idx}, handle={evt.handle}, value=0x{evt.value.hex()}")


def handle_evt_gattc_read_completed(central, evt: ble.BleEventGattcReadCompleted):
    print(f"Read Complete: conn_idx={evt.conn_idx}, handle={evt.handle}, status={evt.status.name}, value=0x{evt.value.hex()}")


def handle_evt_gattc_write_completed(central, evt: ble.BleEventGattcWriteCompleted):
    print(f"Write Complete: conn_idx={evt.conn_idx}, handle={evt.handle}, status={evt.status.name}")


def handle_evt_gattc_browse_svc(central: ble.BleCentral, evt: ble.BleEventGattcBrowseSvc):

    print(f"Service discovered: uuid={uuid_to_str(evt.uuid)}. handle={evt.start_h}")
    for item in evt.items:
        if item.type == ble.GATTC_ITEM_TYPE.GATTC_ITEM_TYPE_INCLUDE:
            print(f"\tIncluded service discovered: handle={item.handle}, uuid={uuid_to_str(item.uuid)}")
        elif item.type == ble.GATTC_ITEM_TYPE.GATTC_ITEM_TYPE_CHARACTERISTIC:
            # TODO format properties function
            print(f"\tCharacteristic discovered: handle={item.handle}, uuid={uuid_to_str(item.uuid)}, prop={item.char_data.properties} "
                  + f"{format_properties(item.char_data.properties)}")
        elif item.type == ble.GATTC_ITEM_TYPE.GATTC_ITEM_TYPE_DESCRIPTOR:
            # TODO format properties function
            print(f"\t\tDescriptor discovered: handle={item.handle}, uuid={uuid_to_str(item.uuid)}")


def handle_evt_gattc_browse_completed(central: ble.BleCentral, evt: ble.BleEventGattcBrowseCompleted):
    print(f"Browsing complete: conn_idx={evt.conn_idx}, evt={evt.status}")


def handle_evt_gap_address_resolved(central: ble.BleCentral, evt: ble.BleEventGapAddressResolved):
    print(f"Address resolved: conn_idx={evt.conn_idx}, evt={evt}")


def handle_evt_gap_numeric_request(central: ble.BleCentral, evt: ble.BleEventGapNumericRequest):
    print(f"Numeric Request: conn_idx={evt.conn_idx}, num_key={evt.num_key}")


# TODO move these to a ultility package
def str_to_bd_addr(type: ble.BLE_ADDR_TYPE, bd_addr_str: str) -> ble.BdAddress:
    bd_addr_str = bd_addr_str.replace(":", "")
    bd_addr_list = [int(bd_addr_str[idx:idx + 2], 16) for idx in range(0, len(bd_addr_str), 2)]
    bd_addr_list.reverse()  # mcu is little endian
    return ble.BdAddress(type, bytes(bd_addr_list))


def bd_addr_to_str(bd: ble.BdAddress) -> str:
    return_string = ""
    for byte in bd.addr:
        byte_string = str(hex(byte))[2:]
        if len(byte_string) == 1:  # Add a leading 0
            byte_string = "0" + byte_string
        return_string = byte_string + ":" + return_string
    return return_string[:-1]


def uuid_to_str(uuid: ble.AttUuid) -> str:
    data = uuid.uuid
    return_string = ""
    if uuid.type == ble.ATT_UUID_TYPE.ATT_UUID_128:
        for byte in data:
            byte_string = str(hex(byte))[2:]
            if len(byte_string) == 1:  # Add a leading 0
                byte_string = "0" + byte_string
            return_string = byte_string + return_string
    else:
        for i in range(1, -1, -1):
            byte_string = str(hex(data[i]))[2:]
            if len(byte_string) == 1:
                byte_string = "0" + byte_string
            return_string += byte_string

    return return_string


def format_properties(prop: int) -> str:
    propr_str = "BRXWNISE"  # each letter corresponds to single property
    for i in range(0, 8):
        if prop & (1 << i) == 0:
            propr_str = propr_str.replace(propr_str[i], '-')
    return propr_str


def user_main():
    elapsed = 0
    delay = 1
    while True:
        time.sleep(delay)
        elapsed += delay
        print(f"User Main. elapsed={elapsed}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='main_central',
                                     description='BLE Central AT Command CLI')

    parser.add_argument("com_port")

    args = parser.parse_args()

    main(args.com_port)
