import asyncio
from Ble import BlePeripheral


async def user_main():
    elapsed = 0
    delay = 1
    # asyncio.all_tasks -> test printing all running tasks
    while True:
        await asyncio.sleep(delay)
        elapsed += delay
        print(f"User Main. elapsed={elapsed}")


async def main():
    # ble_task = asyncio.create_task(test.run())
    # task1 = asyncio.create_task(user_main())
    # await ble_task
    # await task1

    # TODO should wait for serial port to open before attempting to interact with peripheral
    await asyncio.gather(user_main(), ble_task())  # need to move this to another func and create a main loop


async def ble_task():
    periph = BlePeripheral("COM40")

    print("Main Opening port")
    # Open the serial port the the 531
    await periph.init()

    print("Mian Serial port opened")

    # periph.register_app
    await periph.start()

    periph.set_advertising_interval((20) * 1000 // 625, (30) * 1000 // 625)

    await periph.start_advertising()
    # TODO register app

    print("Main After periph.init()")

    # TODO GAP_ERR_PRIVACY_CFG_PB from adv command

    while True:
        # handle messages

        # other stuff

        # must always yeild in a task to give others a chance to run
        await asyncio.sleep(1)


asyncio.run(main())

# TODO unit tests fail when pushed from remote
