import asyncio

# TODO simplify imports for user
from ble_api.BleCentral import BleCentral
from ble_api.BleAtt import ATT_ERROR
from ble_api.BleCommon import BleEventBase
from ble_api.BleGap import  GAP_SCAN_TYPE, GAP_SCAN_MODE
from ble_api.BleGatt import GATT_EVENT
from services.CustomBleService import CustomBleService, CustomBleServiceCallbacks


async def app_char1_read_callback(svc: CustomBleService, conn_idx: int):
    print("app_char1_read_callback")
    data = 0x05
    await svc.send_char1_read_cfm(conn_idx,
                                  ATT_ERROR.ATT_ERROR_OK,
                                  data.to_bytes(1, byteorder='little'))


async def app_char1_write_callback(svc: CustomBleService, conn_idx: int, value: int):
    print(f"app_char1_write_callback. conn_idx={conn_idx}, value={value}")
    await svc.send_char1_write_cfm(conn_idx, ATT_ERROR.ATT_ERROR_OK)


async def app_char2_write_callback(svc: CustomBleService, conn_idx: int, value: int):
    print(f"app_char2_write_callback. conn_idx={conn_idx}, value={value}")
    await svc.send_char2_write_cfm(conn_idx, ATT_ERROR.ATT_ERROR_OK)
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

    central = BleCentral("COM40")
    await central.init()
    await central.start()

    await central.scan_start(GAP_SCAN_TYPE.GAP_SCAN_ACTIVE,
                             GAP_SCAN_MODE.GAP_SCAN_GEN_DISC_MODE,
                             160,
                             80,
                             False,
                             True)

    timer_read_task = asyncio.create_task(sample_q.get(), name='sample_q_Read')
    ble_event_task = asyncio.create_task(central.get_event(), name='GetBleEvent')
    pending = [timer_read_task, ble_event_task]

    while True:
        done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)

        for task in done:

            # Every second a "sample" is received from user_main
            if task is timer_read_task:
                sample: int = task.result()

                timer_read_task = asyncio.create_task(sample_q.get(), name='sample_q_Read')
                pending.add(timer_read_task)

            # Handle and BLE events that hace occurred
            elif task is ble_event_task:
                evt: BleEventBase = task.result()  # TODO how does timeout error affect result
                if evt is not None:
                    handled = await central.service_handle_event(evt)
                    if not handled:
                        # Application opportunity to handle event
                        # or apply default behaior
                        pass

                print(f"Main rx'd event: {evt}. hanlded={handled} \n")

                ble_event_task = asyncio.create_task(central.get_event(), name='GetBleEvent')
                pending.add(ble_event_task)


asyncio.run(main())
