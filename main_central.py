import asyncio
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.patch_stdout import patch_stdout

import ble_devices as ble

ble.dg_configBLE_CENTRAL = 1
ble.dg_configBLE_PERIPHERAL = 0

async def user_main():
    elapsed = 0
    delay = 1
    while True:
        await asyncio.sleep(delay)
        elapsed += delay
        #print(f"User Main. elapsed={elapsed}")


async def console(ble_command_q: asyncio.Queue, ble_response_q: asyncio.Queue):
    commands = ['GAPSCAN',
                'GAPCONNECT',
                'GAPBROWSE',
                'GAPDISCONNECT',
                'GATTWRITE',
                'GATTREAD',
                'GATTWRITENORESP',
                'GAPPAIR',
                'GAPSETCONNPARAM',
                'PASSKEYENTRY']
    commands.sort()
    word_completer = WordCompleter(commands, ignore_case=True)

    session = PromptSession(completer=word_completer)
    while True:
        with patch_stdout():
            input = await session.prompt_async('>>> ')
            ble_command_q.put_nowait(input)
            response = await ble_response_q.get()
            print(f"<<< {response}")


async def main():
    ble_command_q = asyncio.Queue()
    ble_response_q = asyncio.Queue()
    await asyncio.gather(console(ble_command_q, ble_response_q), ble_task(ble_command_q, ble_response_q))


async def ble_task(command_q: asyncio.Queue, response_q: asyncio.Queue):

    services = ble.SearchableQueue()

    central = ble.BleCentral("COM15", gtl_debug=True)
    await central.init()
    await central.start()

    # await central.scan_start(GAP_SCAN_TYPE.GAP_SCAN_ACTIVE,
    #                         GAP_SCAN_MODE.GAP_SCAN_GEN_DISC_MODE,
    #                         160,
    #                         80,
    #                         False,
    #                         True)

    console_command_task = asyncio.create_task(command_q.get(), name='GetConsoleCommand')
    ble_event_task = asyncio.create_task(central.get_event(), name='GetBleEvent')
    pending = [ble_event_task, console_command_task]

    central.set_io_cap(ble.GAP_IO_CAPABILITIES.GAP_IO_CAP_KEYBOARD_DISP)
    # adv_reports= []
    while True:
        done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)

        for task in done:

            # Handle and BLE events that hace occurred
            if task is console_command_task:
                command: str = task.result()
                # print(f"ble_taks received command: {command}")

                error = ble.BLE_ERROR.BLE_ERROR_FAILED
                args = command.split()
                if len(args) > 0:
                    ble_func = args[0]
                    match ble_func:
                        case 'GAPSCAN':

                            error = await central.scan_start(ble.GAP_SCAN_TYPE.GAP_SCAN_ACTIVE,
                                                             ble.GAP_SCAN_MODE.GAP_SCAN_GEN_DISC_MODE,
                                                             160,
                                                             80,
                                                             False,
                                                             True)

                        case "GAPCONNECT":
                            if len(args) == 2:  # TODO pass in addr 48:23:35:00:1b:53
                                # bd_info = args[1].strip(',')
                                # bd_type =  if bd_info[1] == 'P' else BLE_ADDR_TYPE.PRIVATE_ADDRESS
                                periph_bd = str_to_bd_addr(ble.BLE_ADDR_TYPE.PUBLIC_ADDRESS, args[1])
                                print(f"periph: {periph_bd}")
                                periph_bd = ble.BdAddress(ble.BLE_ADDR_TYPE.PUBLIC_ADDRESS, bytes.fromhex("531B00352348"))  # addr is backwards
                                periph_conn_params = ble.GapConnParams(50, 70, 0, 420)
                                error = await central.connect(periph_bd, periph_conn_params)

                        case "GAPBROWSE":
                            if len(args) == 2:
                                conn_idx = int(args[1])
                                error = await central.browse(conn_idx, None)

                        case "GAPDISCONNECT":
                            if len(args) >= 2:
                                conn_idx = int(args[1])
                                if len(args) == 3:
                                    reason = ble.BLE_HCI_ERROR(int(args[2]))
                                    if reason == ble.BLE_HCI_ERROR.BLE_HCI_ERROR_NO_ERROR:
                                        reason = ble.BLE_HCI_ERROR.BLE_HCI_ERROR_REMOTE_USER_TERM_CON
                                else:
                                    reason = ble.BLE_HCI_ERROR.BLE_HCI_ERROR_REMOTE_USER_TERM_CON
                                error = await central.disconect(conn_idx, reason)

                        case "GATTWRITE":
                            if len(args) == 4:
                                conn_idx = int(args[1])
                                handle = int(args[2])
                                value = bytes.fromhex(args[3])  # TODO requires leading 0 for 0x0-0xF
                                error = await central.write(conn_idx, handle, 0, value)

                        case "GATTWRITENORESP":
                            if len(args) == 5:
                                conn_idx = int(args[1])
                                handle = int(args[2])
                                signed = bool(int(args[3]))
                                value = bytes.fromhex(args[4])  # TODO requires leading 0 for 0x0-0xF
                                error = await central.write_no_resp(conn_idx, handle, signed, value)

                        case "GATTWRITEPREPARE":
                            # TODO not receiving GATTC_CMP_EVT after sending GattcWriteCmd
                            if len(args) == 4:
                                conn_idx = int(args[1])
                                handle = int(args[2])
                                value = bytes.fromhex(args[3])
                                error = await central.write_prepare(conn_idx, handle, 0, value)

                        case "GATTWRITEEXECUTE":
                            if len(args) == 3:
                                conn_idx = int(args[1])
                                execute = bool(int(args[2]))
                                error = await central.write_execute(conn_idx, execute)

                        case "GATTREAD":  # TODO char handle displayed by browse is acutally the declaration. The value is +1
                            if len(args) == 3:
                                conn_idx = int(args[1])
                                handle = int(args[2])
                                error = await central.read(conn_idx, handle, 0)

                        case 'GAPSETCONNPARAM':
                            if len(args) == 6:
                                conn_idx = int(args[1])
                                conn_params = ble.GapConnParams()
                                conn_params.interval_min = int(args[2])
                                conn_params.interval_max = int(args[3])
                                conn_params.slave_latency = int(args[4])
                                conn_params.sup_timeout = int(args[5])
                                error = await central.conn_param_update(conn_idx, conn_params)

                        case 'GAPPAIR':
                            if len(args) == 3:
                                conn_idx = int(args[1])
                                bond = bool(int(args[2]))
                                error = await central.pair(conn_idx, bond)

                        case 'PASSKEYENTRY':
                            if len(args) == 4:
                                conn_idx = int(args[1])
                                accept = bool(int(args[2]))
                                passkey = int(args[3])
                                error = await central.passkey_reply(conn_idx, accept, passkey)

                        case _:
                            pass

                if error == ble.BLE_ERROR.BLE_STATUS_OK:
                    response = "OK"
                else:
                    response = f"ERROR {error}"
                response_q.put_nowait(str(response))

                console_command_task = asyncio.create_task(command_q.get(), name='GetConsoleCommand')
                pending.add(console_command_task)


            # Handle and BLE events that hace occurred
            if task is ble_event_task:
                evt: ble.BleEventBase = task.result()  # TODO how does timeout error affect result
                # print(f"Main rx'd event: {evt}.\n")
                if evt is not None:
                    # TODO switch on event type
                    # if evt.evt_code == BLE_EVT_GAP.BLE_EVT_GAP_ADV_REPORT
                    if isinstance(evt, ble.BleEventGapAdvReport):
                        handle_evt_gap_adv_report(central, evt)
                        # reports = central.parse_adv_data(evt)  # only parses the adv data
                        # adv_reports.append(reports)

                    elif isinstance(evt, ble.BleEventGapScanCompleted):
                        handle_evt_scan_completed(central, evt)
                        pass

                    elif isinstance(evt, ble.BleEventGapConnected):
                        handle_evt_gap_connected(central, evt)

                    elif isinstance(evt, ble.BleEventGapConnectionCompleted):
                        handle_evt_gap_connection_compelted(central, evt)

                    elif isinstance(evt, ble.BleEventGapDisconnected):
                        handle_evt_gap_disconnected(central, evt)

                    elif isinstance(evt, ble.BleEventGattcDiscoverSvc):
                        handle_evt_gattc_discover_svc(central, evt, services)

                    elif isinstance(evt, ble.BleEventGattcDiscoverCompleted):
                        # putting this check here to avoid calling function and not awaiting as not fully implemented
                        if evt.type == ble.GATTC_DISCOVERY_TYPE.GATTC_DISCOVERY_TYPE_SVC:
                            await handle_evt_gattc_discover_completed(central, evt, services)

                    elif isinstance(evt, ble.BleEventGattcDiscoverChar):
                        handle_evt_gattc_discover_char(central, evt)

                    elif isinstance(evt, ble.BleEventGattcDiscoverChar):
                        handle_evt_gattc_discover_char(central, evt)

                    elif isinstance(evt, ble.BleEventGattcDiscoverDesc):
                        handle_evt_gattc_discover_desc(central, evt)

                    elif isinstance(evt, ble.BleEventGattcBrowseSvc):
                        handle_evt_gattc_browse_svc(central, evt)

                    elif isinstance(evt, ble.BleEventGattcBrowseCompleted):
                        handle_evt_gattc_browse_completed(central, evt)

                    elif isinstance(evt, ble.BleEventGattcNotification):
                        handle_evt_gattc_notification(central, evt)

                    elif isinstance(evt, ble.BleEventGattcReadCompleted):
                        handle_evt_gattc_read_completed(central, evt)

                    elif isinstance(evt, ble.BleEventGattcWriteCompleted):
                        handle_evt_gattc_write_completed(central, evt)

                    elif isinstance(evt, ble.BleEventGapConnParamUpdated):
                        handle_evt_gap_conn_param_updated(central, evt)

                    elif isinstance(evt, ble.BleEventGapConnParamUpdateCompleted):
                        handle_evt_gap_conn_param_update_compelted(central, evt)

                    elif isinstance(evt, ble.BleEventGapPairReq):
                        handle_evt_gap_pair_req(central, evt)

                    elif isinstance(evt, ble.BleEventGapPairCompleted):
                        handle_evt_gap_pair_completed(central, evt)

                    elif isinstance(evt, ble.BleEventGapSecLevelChanged):
                        handle_evt_gap_sec_level_changed(central, evt)

                    elif isinstance(evt, ble.BleEventGapPeerFeatures):
                        handle_evt_gap_peer_features(central, evt)

                    elif isinstance(evt, ble.BleEventGapPeerVersion):
                        handle_evt_gap_peer_version(central, evt)

                    elif isinstance(evt, ble.BleEventGapPasskeyNotify):
                        handle_evt_gap_passkey_notify(central, evt)
       
                    else:
                        print(f"Ble Task unhandled event: {evt}")

                ble_event_task = asyncio.create_task(central.get_event(), name='GetBleEvent')
                pending.add(ble_event_task)


def handle_evt_gap_passkey_notify(central, evt: ble.BleEventGapPasskeyNotify):
    print(f"Passkey notify: conn_idx={evt.conn_idx}, passkey={evt.passkey}")


def handle_evt_gap_peer_features(central, evt: ble.BleEventGapPeerFeatures):
    print(f"Peer features: conn_idx={evt.conn_idx}, features={evt.le_features.hex()}")


def handle_evt_gap_peer_version(central, evt: ble.BleEventGapPeerVersion):
    print(f"Peer version: conn_idx={evt.conn_idx}, lmp_version={evt.lmp_version} " +
          f"company_id={evt.company_id}, lmp_subversion={evt.lmp_subversion}")


def handle_evt_gap_sec_level_changed(central, evt: ble.BleEventGapSecLevelChanged):
    print(f"Security level changed: sec_level={evt.level}")


def handle_evt_gap_pair_req(central, evt: ble.BleEventGapPairReq):
    print(f"Pair Request: evt={evt}")


def handle_evt_gap_pair_completed(central, evt: ble.BleEventGapPairCompleted):
    print(f"Pairing compelte: conn_idx={evt.conn_idx}, bond={evt.bond}, mitm={evt.mitm}, status={ble.BLE_ERROR(evt.status)}")


def handle_evt_gap_conn_param_updated(central, evt: ble.BleEventGapConnParamUpdated):
    print(f"Connection Parameters updated: evt={evt}")


def handle_evt_gap_conn_param_update_compelted(central, evt: ble.BleEventGapConnParamUpdateCompleted):
    print(f"Connection Parameters update completed: evt={evt}")


def handle_evt_gap_connection_compelted(central, evt: ble.BleEventGapConnectionCompleted):
    print(f"Connection completed: status={evt.status}")


def handle_evt_scan_completed(central: ble.BleCentral, evt: ble.BleEventGapScanCompleted):
    print(f"Scan completed: status={evt.status}")


def handle_evt_gap_adv_report(central: ble.BleCentral, evt: ble.BleEventGapAdvReport):
    print(f"Advertisment: address={bd_addr_to_str(evt.address)} addr_type={evt.address.addr_type} "
          + f"rssi={evt.rssi}, data={evt.data.hex()}")


def handle_evt_gattc_discover_svc(central: ble.BleCentral, evt: ble.BleEventGattcDiscoverSvc, services: ble.SearchableQueue):
    service = ble.BleServiceBase()
    service.start_h = evt.start_h
    service.end_h = evt.end_h
    services.push(service)


async def handle_evt_gattc_discover_completed(central: ble.BleCentral, evt: ble.BleEventGattcDiscoverCompleted, services: ble.SearchableQueue):
    print(f"main_central handle_evt_gattc_discover_completed unimplemented. evt={evt}")

    if evt.type == ble.GATTC_DISCOVERY_TYPE.GATTC_DISCOVERY_TYPE_SVC:
        service: ble.BleServiceBase = services.peek_back()
        await central.discover_characteristics(evt.conn_idx, service.start_h, service.end_h, None)

    # TODO discover included services

    elif evt.type == ble.GATTC_DISCOVERY_TYPE.GATTC_DISCOVERY_TYPE_CHARACTERISTICS:
        # await central.discover_descriptors(evt.conn_idx. )
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
    print(f"Read Complete: conn_idx={evt.conn_idx}, handle={evt.handle}, status={evt.status}, value=0x{evt.value.hex()}")


def handle_evt_gattc_write_completed(central, evt: ble.BleEventGattcWriteCompleted):
    print(f"Write Complete: conn_idx={evt.conn_idx}, handle={evt.handle}, status={evt.status}")


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


# TODO move these to a ultility package
def str_to_bd_addr(type: ble.BLE_ADDR_TYPE, bd_addr_str: str) -> ble.BdAddress:
    bd_addr_str = bd_addr_str.replace(":", "")
    bd_addr_list = [int(bd_addr_str[idx:idx + 2], 16) for idx in range(0, len(bd_addr_str), 2)]
    bd_addr_list.reverse()  # mcu is little endian
    return ble.BdAddress(type, bd_addr_list)

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
    for i in range(0,8):
        if prop & (1 << i) == 0:
            propr_str = propr_str.replace(propr_str[i], '-')
    return propr_str


asyncio.run(main())
