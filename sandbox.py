
from ctypes import *
from gtl_messages.gtl_message_gapc import *
from gtl_messages.gtl_message_gapm import *
from gtl_messages.gtl_message_gattc import *
from gtl_messages.gtl_message_gattm import *
from ble_api.BleGatts import *
from ble_api.BleGap import *
from gtl_port.gapc_task import *
from gtl_port.gattc_task import *
from gtl_port.co_bt import *
from ble_api.BleCommon import *
from manager.BleManagerGattsMsgs import BleMgrGattsGetValueRsp
from services.BleService import *

import asyncio
import aioconsole


async def user_main():
    elapsed = 0
    delay = 1
    while True:
        await asyncio.sleep(delay)
        elapsed += delay
        # print(f"User Main. elapsed={elapsed}")

async def console():
    line = await aioconsole.ainput(">>> ")
    print(line)

async def main():
    user_task = asyncio.create_task(user_main(), name='user_main')
    console_task = asyncio.create_task(console(), name='console')
    pending = [user_task, console_task]
    while True:
        done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)
   
        for task in done:
            if task is console_task:
                 console_task = asyncio.create_task(console(), name='console')
                 pending.add(console_task)


asyncio.run(main())