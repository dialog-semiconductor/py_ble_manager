import asyncio

# TODO simplify imports for user
from ble_api.Ble import BlePeripheral
from ble_api.BleAtt import ATT_ERROR
from ble_api.BleCommon import BleEventBase
from ble_api.BleGap import BleEventGapConnected, BleEventGapDisconnected
from ble_api.BleGatt import GATT_EVENT
from services.CustomBleService import CustomBleService


def app_char1_read_callback(svc):
    print("app_char1_read_callback")
    status = ATT_ERROR.ATT_ERROR_OK
    data = 0x05
    return status, data.to_bytes(1, byteorder='little')


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

    periph = BlePeripheral("COM40")
    await periph.init()
    await periph.start()

    my_service = CustomBleService()
    my_service.init()
    my_service.char1_read_callback = app_char1_read_callback

    await periph.register_service(my_service)
    await periph.set_value(my_service.gatt_characteristics[1].char.handle, (0x8692).to_bytes(2, 'little'))
    await periph.set_value(my_service.gatt_characteristics[2].descriptors[0].handle, b"Hello")

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
                if my_service.ccc == 1:
                    error = await periph.send_event(0,
                                                    my_service.gatt_characteristics[2].char.handle,
                                                    GATT_EVENT.GATT_EVENT_NOTIFICATION,
                                                    sample.to_bytes(4, byteorder='little'))
                    print(f"Notification sent. sample = {sample}, error = {error}")

                timer_read_task = asyncio.create_task(sample_q.get(), name='sample_q_Read')
                pending.add(timer_read_task)

            # Handle and BLE events that hace occurred
            elif task is ble_event_task:
                evt: BleEventBase = task.result()  # TODO how does timeout error affect result
                if evt is not None:
                    handled = await periph.service_handle_event(evt)
                    if not handled:
                        # Application opportunity to handle event
                        # or apply default behaior
                        pass

                print(f"Main rx'd event: {evt}. hanlded={handled} \n")

                ble_event_task = asyncio.create_task(periph.get_event(), name='GetBleEvent')
                pending.add(ble_event_task)


asyncio.run(main())
