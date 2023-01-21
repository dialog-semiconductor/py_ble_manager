
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
import prompt_toolkit

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers.sql import SqlLexer

from prompt_toolkit import prompt
from prompt_toolkit.completion import NestedCompleter

from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout


async def user_main():
    elapsed = 0
    delay = 1
    while True:
        await asyncio.sleep(delay)
        elapsed += delay
        print(f"User Main. elapsed={elapsed}")


async def main():
    await asyncio.gather(user_main(), my_coroutine())


async def my_coroutine():
    word_completer = WordCompleter([
    'GAPCONNECT', 'GAPBROWSE', 'GAPDISCONNECT', 'GATTWRITE', 'GATTREAD'], ignore_case=True)

    completer = NestedCompleter.from_nested_dict({
    
    'GAPCONNECT': None,
    'GAPBROWSE': {
        '<conn_idx>': None,
    },
    'GAPDISCONNECT': {
        '<conn_idx>': None,
    },
    'GATTREAD': {
        '<conn_idx>': {
            '<handle>': None
        }
    },
    'GATTWRITE': {
        '<conn_idx>': {
            '<handle>': {'<value>'}
        }
    }
})

    my_completer = NestedCompleter.from_nested_dict({
        'show': {
            'version': None,
            'clock': None,
            'ip': {
                'interface': {'brief'}
            }
        },
        'exit': None,
    })

    session = PromptSession(completer=completer)
    while True:
        with patch_stdout():
            result = await session.prompt_async('Say something: ')
        print('You said: %s' % result)

asyncio.run(main())
