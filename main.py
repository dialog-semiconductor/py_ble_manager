import asyncio
from BleManager import *


async def user_main():
    print("Running user main")
    await asyncio.sleep(5)
    print("5 Seconds elapsed")
    await asyncio.sleep(5)
    print("10 Seconds elapsed")

async def main():

    test = BlePeripheral()
    ble_task = asyncio.create_task(test.run())
    task1 = asyncio.create_task(user_main())
    await ble_task
    await task1


asyncio.run(main())
