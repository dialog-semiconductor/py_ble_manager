import asyncio

import ble_devices as ble
from services.CustomBleService import CustomBleService, CustomBleServiceCallbacks

ble.dg_configBLE_CENTRAL = 0
ble.dg_configBLE_PERIPHERAL = 1

async def app_char1_read_callback(svc: CustomBleService, conn_idx: int):
    print("app_char1_read_callback")
    data = 0x05
    await svc.send_char1_read_cfm(conn_idx,
                                  ble.ATT_ERROR.ATT_ERROR_OK,
                                  data.to_bytes(1, byteorder='little'))


async def app_char1_write_callback(svc: CustomBleService, conn_idx: int, value: int):
    print(f"app_char1_write_callback. conn_idx={conn_idx}, value={value}")
    await svc.send_char1_write_cfm(conn_idx, ble.ATT_ERROR.ATT_ERROR_OK)


async def app_char2_write_callback(svc: CustomBleService, conn_idx: int, value: int):
    print(f"app_char2_write_callback. conn_idx={conn_idx}, value={value}")
    await svc.send_char2_write_cfm(conn_idx, ble.ATT_ERROR.ATT_ERROR_OK)
    await svc.set_char2_value(value.to_bytes(2, byteorder='little'))


async def app_char3_ccc_changed_callback(svc: CustomBleService, conn_idx: int, value: int):
    print(f"app_char3_ccc_changed_callback. conn_idx={conn_idx}, value={value}")


async def user_main(sample_q: asyncio.Queue):
    elapsed = 0
    delay = 1
    while True:
        await asyncio.sleep(delay)
        elapsed += delay
        sample_q.put_nowait(elapsed)
        print(f"User Main. elapsed={elapsed}")


async def main():

    sample_q = asyncio.Queue()
    await asyncio.gather(user_main(sample_q), ble_task(sample_q))


async def ble_task(sample_q: asyncio.Queue):

    periph = ble.BlePeripheral("COM15", gtl_debug=True)
    await periph.init()
    await periph.start()

    my_service_callbacks = CustomBleServiceCallbacks(app_char1_read_callback,
                                                     app_char1_write_callback,
                                                     app_char2_write_callback)
    my_service = CustomBleService(my_service_callbacks)
    my_service.init()

    await periph.register_service(my_service)
    await my_service.set_char2_value((0x8692).to_bytes(2, 'little'))
    await my_service.set_char3_user_desc_value(b"Hello")

    periph.set_io_cap(ble.GAP_IO_CAPABILITIES.GAP_IO_CAP_DISP_ONLY)

    periph.set_advertising_interval(20, 30)
    await periph.start_advertising()

    timer_read_task = asyncio.create_task(sample_q.get(), name='sample_q_Read')
    ble_event_task = asyncio.create_task(periph.get_event(), name='GetBleEvent')
    pending = [timer_read_task, ble_event_task]

    while True:
        done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)

        for task in done:

            # Every second a "sample" is received from user_main
            if task is timer_read_task:
                sample: int = task.result()
                if my_service.ccc == 1:  # TODO this should come from changed callback
                    # TODO how to get conn_idx? Notify all connected method?
                    error = await my_service.notify_char3(0, sample.to_bytes(4, byteorder='little'))
                    print(f"Notification sent. sample = {sample}, error = {error}")

                timer_read_task = asyncio.create_task(sample_q.get(), name='sample_q_Read')
                pending.add(timer_read_task)

            # Handle and BLE events that hace occurred
            elif task is ble_event_task:
                evt: ble.BleEventBase = task.result()  # TODO how does timeout error affect result
                if evt is not None:
                    handled = await periph.service_handle_event(evt)
                    if not handled:
                        match evt.evt_code:
                            case ble.BLE_EVT_GAP.BLE_EVT_GAP_DISCONNECTED:
                                await periph.start_advertising()
                            case ble.BLE_EVT_GAP.BLE_EVT_GAP_PAIR_REQ:
                                evt: ble.BleEventGapPairReq
                                await periph.pair_reply(evt.conn_idx, True, False)
                            case _:
                                await periph.handle_event_default(evt)

                print(f"Main rx'd event: {evt}. hanlded={handled} \n")

                ble_event_task = asyncio.create_task(periph.get_event(), name='GetBleEvent')
                pending.add(ble_event_task)


asyncio.run(main())
