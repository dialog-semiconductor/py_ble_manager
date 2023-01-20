
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


'''
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
'''


uuid = "8e716a7e-12a2-11ed-861d-0242ac120002"

def uuid_from_str(uuid_str: str) -> bytes:
    uuid_str = uuid_str.replace("-", "")
    uuid_list = [int(uuid_str[idx:idx + 2], 16) for idx in range(0, len(uuid_str), 2)]
    uuid_list.reverse()  # mcu is little endian
    return bytes(uuid_list)

def uuid_to_str(uuid: AttUuid) -> str:
    data = uuid.uuid
    return_string = ""
    for byte in data:
        byte_string = str(hex(byte))[2:]
        if len(byte_string) == 1:
            byte_string = "0"+ byte_string
        return_string = byte_string + return_string
    
    return return_string


att_uuid = AttUuid(uuid_from_str(uuid))

return_string = uuid_to_str(att_uuid)
print(return_string)

st = "1234"

print(bytes.fromhex(st))

print(hex(int("1")))

st = "1"

print(bytes.fromhex(st))