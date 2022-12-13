import asyncio
import serial_asyncio
from gtl_messages import *
# TODO consider downsides of importing everything without namespace
from Gap import *
from MessageRouter import *
from SerialStreamManager import *

class BleBase():
    pass

class BleClient(BleBase):
    pass

class BlePeripheral(BleBase):
    def __init__(self):
        tx_queue = asyncio.Queue() 
        rx_queue = asyncio.Queue()

        self.message_router = MessageRouter(tx_queue, rx_queue)
        self.gap_manager = GapManager()
        self.gap_controller = GapController()
        self.message_router.register_observer(self.gap_manager.handle_message)
        self.message_router.register_observer(self.gap_controller.handle_message)
        self.serial_stream_manager = SerialStreamManager(tx_queue, rx_queue)

    async def run(self):
        # TaskGroup is in 3.11
        #async with asyncio.TaskGroup() as tg:
        #    task1 = tg.create_task(coro1,)
            #task2 = tg.create_task(another_coro(...))

        #task1 = asyncio.create_task(coro1, name='OpenPort')
        serial_rx_task = asyncio.create_task(self.message_router.handle_received_message(), name='StreamRx')
        router_tx_task = asyncio.create_task(self.serial_stream_manager.send(), name='StreamTx')
        router_handle_rx_task = asyncio.create_task(self.serial_stream_manager.receive(), name='RouterRx')

        #print("Waiting to open port")
        # Wait until the port is open before starting any other coroutines
        await asyncio.wait_for(self.serial_stream_manager.open_port(), timeout=None)

        #print("Port should be open????????")
        await serial_rx_task
        await router_tx_task
        await router_handle_rx_task