import asyncio

# TODO simplify imports for user
from ble_api.BleCentral import BleCentral
from ble_api.BleCommon import BleEventBase, BdAddress, BLE_ADDR_TYPE
from ble_api.BleGap import BleEventGapAdvReport, BleEventGapScanCompleted, gap_conn_params, BleEventGapConnected
from ble_api.BleGattc import BleEventGattcDiscoverSvc, BleEventGattcDiscoverCompleted, GATTC_DISCOVERY_TYPE, \
    BleEventGattcDiscoverChar, BleEventGattcDiscoverDesc, BleEventGattcBrowseCompleted, BleEventGattcBrowseSvc

from manager.BleManagerStorage import SearchableQueue
from services.BleService import BleServiceBase

async def user_main():
    elapsed = 0
    delay = 1
    while True:
        await asyncio.sleep(delay)
        elapsed += delay
        print(f"User Main. elapsed={elapsed}")


async def main():

    await asyncio.gather(user_main(), ble_task())


async def ble_task():

    services = SearchableQueue()

    central = BleCentral("COM15")
    await central.init()
    await central.start()

    # await central.scan_start(GAP_SCAN_TYPE.GAP_SCAN_ACTIVE,
    #                         GAP_SCAN_MODE.GAP_SCAN_GEN_DISC_MODE,
    #                         160,
    #                         80,
    #                         False,
    #                         True)

    periph_bd = BdAddress(BLE_ADDR_TYPE.PUBLIC_ADDRESS, bytes.fromhex("531B00352348"))  # addr is backwards

    # TODO do these conversions when setting gap_conn_params
    periph_conn_params = gap_conn_params(50, 70, 0, 420)
    await central.connect(periph_bd, periph_conn_params)  # Getting 0xA2 status from Gtl GapmCptEvt

    # TODO ble_gattc_browse

    ble_event_task = asyncio.create_task(central.get_event(), name='GetBleEvent')
    pending = [ble_event_task]

    # adv_reports= []
    while True:
        done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)

        for task in done:

            # Handle and BLE events that hace occurred
            if task is ble_event_task:
                evt: BleEventBase = task.result()  # TODO how does timeout error affect result
                print(f"Main rx'd event: {evt}.\n")
                if evt is not None:
                    # TODO switch on event type
                    # if evt.evt_code == BLE_EVT_GAP.BLE_EVT_GAP_ADV_REPORT
                    if isinstance(evt, BleEventGapAdvReport):
                        if evt.address.addr == periph_bd.addr:
                            pass
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
                        await handle_evt_gap_connected(central, evt)

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


async def handle_evt_gap_connected(central: BleCentral, evt: BleEventGapConnected):
    #response = await central.discover_services(evt.conn_idx, None)
    #print(f"handle_evt_gap_connected. response = {response}")

    response = await central.browse(evt.conn_idx, None)
    print(f"handle_evt_gap_connected. response = {response}")


def handle_evt_gattc_browse_svc(central: BleCentral, evt: BleEventGattcDiscoverDesc):
    print(f"main_central handle_evt_gattc_browse_svc unimplemented. evt={evt}")
    pass


def handle_evt_gattc_browse_completed(central: BleCentral, evt: BleEventGattcDiscoverDesc):
    print(f"main_central handle_evt_gattc_browse_completed unimplemented. evt={evt}")
    pass



asyncio.run(main())
