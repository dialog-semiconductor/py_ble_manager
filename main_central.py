import asyncio

# TODO simplify imports for user
from ble_api.BleCentral import BleCentral
from ble_api.BleCommon import BleEventBase, BdAddress, BLE_ADDR_TYPE
from ble_api.BleGap import BleEventGapAdvReport, BleEventGapScanCompleted, gap_conn_params, BleEventGapConnected


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

    central = BleCentral("COM40")
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

                ble_event_task = asyncio.create_task(central.get_event(), name='GetBleEvent')
                pending.add(ble_event_task)


async def handle_evt_gap_connected(central: BleCentral, evt: BleEventGapConnected):
    #central.browse
    response = await central.discover_services(evt.conn_idx, None)
    print(f"handle_evt_gap_connected. response = {response}")


asyncio.run(main())
