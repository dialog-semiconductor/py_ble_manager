import asyncio

# TODO simplify imports for user
from ble_api.BleCentral import BleCentral
from ble_api.BleCommon import BleEventBase
from ble_api.BleGap import GAP_SCAN_TYPE, GAP_SCAN_MODE, BleEventGapAdvReport, BleAdvData


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

    await central.scan_start(GAP_SCAN_TYPE.GAP_SCAN_ACTIVE,
                             GAP_SCAN_MODE.GAP_SCAN_GEN_DISC_MODE,
                             160,
                             80,
                             False,
                             True)

    ble_event_task = asyncio.create_task(central.get_event(), name='GetBleEvent')
    pending = [ble_event_task]

    while True:
        done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)

        adv_reports= []
        for task in done:

            # Handle and BLE events that hace occurred
            if task is ble_event_task:
                evt: BleEventBase = task.result()  # TODO how does timeout error affect result
                print(f"Main rx'd event: {evt}.\n")
                if evt is not None:
                    # TODO switch on event type
                    if isinstance(evt, BleEventGapAdvReport):
                        adv_reports.append(evt)
                        parse_adv_data(evt)

                ble_event_task = asyncio.create_task(central.get_event(), name='GetBleEvent')
                pending.add(ble_event_task)


# TODO data length seems wrong
def parse_adv_data(evt: BleEventGapAdvReport):
    data_ptr = 0
    adv_data_structs: BleAdvData = []
    print(f"Parsing evt.data={list(evt.data)}")
    if len(evt.data) > 0:
        while data_ptr <= 31 and data_ptr < evt.length:

            struct = BleAdvData(type=evt.data[data_ptr])
            data_ptr += 1
            struct.len = evt.data[data_ptr]
            data_ptr += 1
            struct.data = evt.data[data_ptr:(data_ptr + struct.len)]
            data_ptr += struct.len
            adv_data_structs.append(struct)

    for adv in adv_data_structs:
        print(f"Rx'd Adv Data: {adv}")


asyncio.run(main())
