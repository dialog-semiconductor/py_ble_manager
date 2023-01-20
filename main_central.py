import asyncio
import aioconsole

# TODO simplify imports for user
from ble_api.BleAtt import AttUuid, ATT_UUID_TYPE
from ble_api.BleCentral import BleCentral
from ble_api.BleCommon import BleEventBase, BdAddress, BLE_ADDR_TYPE, BLE_HCI_ERROR
from ble_api.BleGap import BleEventGapAdvReport, BleEventGapScanCompleted, GapConnParams, BleEventGapConnected, \
    BleEventGapDisconnected
from ble_api.BleGattc import BleEventGattcDiscoverSvc, BleEventGattcDiscoverCompleted, GATTC_DISCOVERY_TYPE, \
    BleEventGattcDiscoverChar, BleEventGattcDiscoverDesc, BleEventGattcBrowseCompleted, BleEventGattcBrowseSvc, \
    GATTC_ITEM_TYPE
from manager.BleManagerStorage import SearchableQueue
from services.BleService import BleServiceBase


async def user_main():
    elapsed = 0
    delay = 1
    while True:
        await asyncio.sleep(delay)
        elapsed += delay
        #print(f"User Main. elapsed={elapsed}")


async def console(ble_command_q: asyncio.Queue, ble_response_q: asyncio.Queue):
    while True:
        line = await aioconsole.ainput(">>> ")
        # TODO validate input
        ble_command_q.put_nowait(line)
        response = await ble_response_q.get()
        print(response)

async def main():
    ble_command_q = asyncio.Queue()
    ble_response_q = asyncio.Queue()
    await asyncio.gather(console(ble_command_q, ble_response_q), ble_task(ble_command_q, ble_response_q))


async def ble_task(command_q: asyncio.Queue, response_q: asyncio.Queue):

    services = SearchableQueue()

    central = BleCentral("COM17", gtl_debug=False)
    await central.init()
    await central.start()

    # await central.scan_start(GAP_SCAN_TYPE.GAP_SCAN_ACTIVE,
    #                         GAP_SCAN_MODE.GAP_SCAN_GEN_DISC_MODE,
    #                         160,
    #                         80,
    #                         False,
    #                         True)

   

    # TODO ble_gattc_browse
    console_command_task = asyncio.create_task(command_q.get(), name='GetConsoleCommand')
    ble_event_task = asyncio.create_task(central.get_event(), name='GetBleEvent')
    pending = [ble_event_task, console_command_task]

    # adv_reports= []
    while True:
        done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)

        for task in done:

             # Handle and BLE events that hace occurred
            if task is console_command_task:
                command: str = task.result()
                print(f"ble_taks received command: {command}")

                if command.find("GAPCONNECT") != -1:
                    periph_bd = BdAddress(BLE_ADDR_TYPE.PUBLIC_ADDRESS, bytes.fromhex("531B00352348"))  # addr is backwards

                    # TODO do these conversions when setting GapConnParams
                    periph_conn_params = GapConnParams(50, 70, 0, 420)
                    await central.connect(periph_bd, periph_conn_params)

                elif command.find("GAPBROWSE") != -1:
                    conn_idx = int(command.split()[1])
                    await central.browse(conn_idx, None)

                elif command.find("GAPDISCONNECT") != -1:
                    args = command.split()
                    conn_idx = int(args[1])
                    if len(args) == 3:
                        reason = BLE_HCI_ERROR(int(args[2]))
                        if reason == BLE_HCI_ERROR.BLE_HCI_ERROR_NO_ERROR:
                            reason = BLE_HCI_ERROR.BLE_HCI_ERROR_REMOTE_USER_TERM_CON
                    else:
                        reason = BLE_HCI_ERROR.BLE_HCI_ERROR_REMOTE_USER_TERM_CON
                    await central.disconect(conn_idx, reason)

                else:
                    response = "Invalid command"
                    response_q.put_nowait(response)

                console_command_task = asyncio.create_task(command_q.get(), name='GetConsoleCommand')
                pending.add(console_command_task)


            # Handle and BLE events that hace occurred
            if task is ble_event_task:
                evt: BleEventBase = task.result()  # TODO how does timeout error affect result
                # print(f"Main rx'd event: {evt}.\n")
                if evt is not None:
                    # TODO switch on event type
                    # if evt.evt_code == BLE_EVT_GAP.BLE_EVT_GAP_ADV_REPORT
                    # if isinstance(evt, BleEventGapAdvReport):
                    #     if evt.address.addr == periph_bd.addr:
                    #        pass
                        # reports = central.parse_adv_data(evt)  # only parses the adv data
                        # adv_reports.append(reports)

                    if isinstance(evt, BleEventGapScanCompleted):
                        # for report in adv_reports:
                        # report_str = None
                        # for adv_data in report:
                        #    report_str = f"adv_data={adv_data}\n"
                        # print(f"Report: {report_str}")
                        pass

                    if isinstance(evt, BleEventGapConnected):
                        handle_evt_gap_connected(central, evt)
                        response = "Success" # TODO need to refine responses
                        response_q.put_nowait(response)

                    if isinstance(evt, BleEventGapDisconnected):
                        handle_evt_gap_disconnected(central, evt)
                        response = "Success" # TODO need to refine responses
                        response_q.put_nowait(response)

                    if isinstance(evt, BleEventGattcDiscoverSvc):
                        handle_evt_gattc_discover_svc(central, evt, services)

                    if isinstance(evt, BleEventGattcDiscoverCompleted):
                        # putting this check here to avoid calling function and not awaiting as not fully implemented
                        if evt.type == GATTC_DISCOVERY_TYPE.GATTC_DISCOVERY_TYPE_SVC:
                            await handle_evt_gattc_discover_completed(central, evt, services)

                    if isinstance(evt, BleEventGattcDiscoverChar):
                        handle_evt_gattc_discover_char(central, evt)

                    if isinstance(evt, BleEventGattcDiscoverChar):
                        handle_evt_gattc_discover_char(central, evt)

                    if isinstance(evt, BleEventGattcDiscoverDesc):
                        handle_evt_gattc_discover_desc(central, evt)

                    if isinstance(evt, BleEventGattcBrowseSvc):
                        handle_evt_gattc_browse_svc(central, evt)

                    if isinstance(evt, BleEventGattcBrowseCompleted):
                        handle_evt_gattc_browse_completed(central, evt)
                        response = "Success"
                        response_q.put_nowait(response)

                ble_event_task = asyncio.create_task(central.get_event(), name='GetBleEvent')
                pending.add(ble_event_task)


def handle_evt_gattc_discover_svc(central: BleCentral, evt: BleEventGattcDiscoverSvc, services: SearchableQueue):
    service = BleServiceBase()
    service.start_h = evt.start_h
    service.end_h = evt.end_h
    services.push(service)


async def handle_evt_gattc_discover_completed(central: BleCentral, evt: BleEventGattcDiscoverCompleted, services: SearchableQueue):
    print(f"main_central handle_evt_gattc_discover_completed unimplemented. evt={evt}")

    if evt.type == GATTC_DISCOVERY_TYPE.GATTC_DISCOVERY_TYPE_SVC:
        service: BleServiceBase = services.peek_back()
        await central.discover_characteristics(evt.conn_idx, service.start_h, service.end_h, None)

    # TODO discover included services

    elif evt.type == GATTC_DISCOVERY_TYPE.GATTC_DISCOVERY_TYPE_CHARACTERISTICS:
        # await central.discover_descriptors(evt.conn_idx. )
        pass


def handle_evt_gattc_discover_char(central: BleCentral, evt: BleEventGattcDiscoverChar):
    print(f"main_central handle_evt_gattc_discover_char unimplemented. evt={evt}")
    pass


def handle_evt_gattc_discover_desc(central: BleCentral, evt: BleEventGattcDiscoverDesc):
    print(f"main_central handle_evt_gattc_discover_desc unimplemented. evt={evt}")
    pass


def handle_evt_gap_connected(central: BleCentral, evt: BleEventGapConnected):
    print(f"Conneected to: addr={[hex(x) for x in evt.peer_address.addr]}. conn_idx={evt.conn_idx}")


def handle_evt_gap_disconnected(central: BleCentral, evt: BleEventGapDisconnected):
    # TODO addr to hex str
    print(f"Disconnected from to: addr={[hex(x) for x in evt.address.addr]}")


def handle_evt_gattc_browse_svc(central: BleCentral, evt: BleEventGattcBrowseSvc):

    print(f"Service discovered: uuid={uuid_to_str(evt.uuid)}. handle={evt.start_h}")
    for item in evt.items:
        if item.type == GATTC_ITEM_TYPE.GATTC_ITEM_TYPE_DESCRIPTOR:
            print(f"\tIncluded service discovered: handle={item.handle}, uuid={uuid_to_str(item.uuid)}")
        elif item.type == GATTC_ITEM_TYPE.GATTC_ITEM_TYPE_CHARACTERISTIC:
            # TODO format properties function
            print(f"\tCharacteristic discovered: handle={item.handle}, uuid={uuid_to_str(item.uuid)}, prop={item.char_data.properties}")
        elif item.type == GATTC_ITEM_TYPE.GATTC_ITEM_TYPE_CHARACTERISTIC:
            # TODO format properties function
            print(f"\t\tDescriptor discovered: handle={item.handle}, uuid={uuid_to_str(item.uuid)}")


def handle_evt_gattc_browse_completed(central: BleCentral, evt: BleEventGattcBrowseCompleted):
    print(f"Browsing complete. evt={evt}")


def uuid_to_str(uuid: AttUuid) -> str:
    data = uuid.uuid
    return_string = ""
    if uuid.type == ATT_UUID_TYPE.ATT_UUID_128:
        for byte in data:
            byte_string = str(hex(byte))[2:]
            if len(byte_string) == 1:
                byte_string = "0" + byte_string
            return_string = byte_string + return_string
    else:
        for i in range(1, -1, -1):
            byte_string = str(hex(data[i]))[2:]
            if len(byte_string) == 1:
                byte_string = "0" + byte_string
            return_string += byte_string

    return return_string


asyncio.run(main())
