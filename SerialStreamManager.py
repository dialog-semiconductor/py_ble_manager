import asyncio
import serial_asyncio
from gtl_messages import *
# TODO consider downsides of importing everything without namespace
from Gap import *
from MessageRouter import *

class SerialStreamManager(asyncio.Protocol):

    def __init__(self, tx_queue: asyncio.Queue(), rx_queue: asyncio.Queue()) -> None:
        # TODO error check queues are asyncio.Queue
        #if(not tx_queue or not rx_queue):
            # throw error
        self.tx_queue = tx_queue 
        self.rx_queue = rx_queue

    async def open_port(self):

        self.reader, self.writer = await serial_asyncio.open_serial_connection(url='COM13', baudrate=115200)
        #print("SerialStreamManager.open_port Port has been opened")

    async def receive(self):
        while True:
            buffer = bytes()
            #print(f"buffer: {buffer}")
            #print("Waiting for GTL_INITIATOR")
            buffer = await self.reader.readexactly(1)
            if(buffer[0] == GTL_INITIATOR):
                #print("Waiting for message header")
                buffer += await self.reader.readexactly(8)
                par_len = int.from_bytes(buffer[7:9], "little",signed=False)
                if(par_len != 0):
                    #print("Waiting for message params")
                    buffer += await self.reader.readexactly(par_len)
                
                #print(f"<-- SerialStreamManager.receive Sending: {buffer}")

                # Handle it
                # TODO awaiting here makes is so buffer is not reset and enter endless loop
                self.rx_queue.put_nowait(buffer)

                #print('Tasks count: ', len(asyncio.all_tasks()))
                #print('Tasks: ', asyncio.all_tasks())
            else:
                print("Received some garbage")
    
    async def send(self):
        while True:
            #TODO how to make vs code recongnize this is an asyncio.Queue? And that it is pulling off a GtlMessageBase message?
            # TODO instead of infinite loop, could we instead schedule this coroutine when an item is put on the queue? 
            message = await self.tx_queue.get()
            print(f"--> Tx: {message}")
            self.writer.write(message.to_bytes())
            await self.writer.drain()


# TODO move to a main file
async def main(open_serial_port_coro, serial_rx_coro, serial_tx_coro, router_handle_rx_coro):
    # TaskGroup is in 3.11
    #async with asyncio.TaskGroup() as tg:
    #    task1 = tg.create_task(coro1,)
        #task2 = tg.create_task(another_coro(...))

    #task1 = asyncio.create_task(coro1, name='OpenPort')
    serial_rx_task = asyncio.create_task(serial_rx_coro, name='StreamRx')
    router_tx_task = asyncio.create_task(serial_tx_coro, name='StreamTx')
    router_handle_rx_task = asyncio.create_task(router_handle_rx_coro, name='RouterRx')

    #print("Waiting to open port")
    # Wait until the port is open before starting any other coroutines
    await asyncio.wait_for(open_serial_port_coro, timeout=None)

    #print("Port should be open????????")
    await serial_rx_task
    await router_tx_task
    await router_handle_rx_task


tx_queue = asyncio.Queue() 
rx_queue = asyncio.Queue()

message_router = MessageRouter(tx_queue, rx_queue)
gap_manager = GapManager()
gap_controller = GapController()
message_router.register_observer(gap_manager.handle_gap_message)
serial_stream_manager = SerialStreamManager(tx_queue, rx_queue)

loop = asyncio.get_event_loop()
loop.run_until_complete(main(serial_stream_manager.open_port(), serial_stream_manager.receive(), serial_stream_manager.send(), message_router.handle_received_message()))
loop.close()