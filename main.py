import asyncio
from BleManager import BlePeripheral


async def user_main():
    elapsed = 0
    delay = 1
    while True:
        await asyncio.sleep(delay)
        elapsed += delay
        print(f"User Main. elapsed={elapsed}")

async def main():
    test = BlePeripheral("COM40")
    ble_task = asyncio.create_task(test.run())
    task1 = asyncio.create_task(user_main())
    await ble_task
    await task1


asyncio.run(main())
