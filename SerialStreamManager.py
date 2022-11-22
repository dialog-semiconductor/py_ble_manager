import asyncio
import serial_asyncio
from gtl_messages import *
# TODO consider downsides of importing everything without namespace
from Gap import *
from MessageRouter import *
from GapController import *

class SerialStreamManager(asyncio.Protocol):

    async def open_port(self):
        self.reader, self.writer = await serial_asyncio.open_serial_connection(url='COM13', baudrate=115200)
        #print("SerialStreamManager.open_port Port has been opened")
    
    def register_rx_callback(self, rx_callback):
        self.rx_callback = rx_callback

    async def notify(self, byte_string):
        await self.rx_callback(byte_string)

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
                
                #print(f"SerialStreamManager.receive Sending: {buffer}")

                # Handle it
                # TODO awaiting here makes is so buffer is not reset and enter endless loop
                await self.notify(buffer)

                #print('Tasks count: ', len(asyncio.all_tasks()))
                #print('Tasks: ', asyncio.all_tasks())
            else:
                print("Received some garbage")

    def send(self, byte_string):
        #print(f"SerialStreamManager.send: {byte_string}")
        self.writer.write(byte_string)


async def main(coro1, coro2, coro3):
    # TaskGroup is in 3.11
    #async with asyncio.TaskGroup() as tg:
    #    task1 = tg.create_task(coro1,)
        #task2 = tg.create_task(another_coro(...))

    #task1 = asyncio.create_task(coro1, name='OpenPort')
    task2 = asyncio.create_task(coro2, name='StreamRx')
    task3 = asyncio.create_task(coro3, name='ParserTx')

    #print("Waiting to open port")
    await asyncio.wait_for(coro1, timeout=None)

    #print("Port should be open????????")
    await task2
    await task3


message_router = MessageRouter()
gap_manager = GapManager()
gap_controller = GapController()
message_router.register_observer(gap_manager.handle_gap_message)
serial_stream_manager = SerialStreamManager()
serial_stream_manager.register_rx_callback(message_router.handle_received_message)
message_router.register_tx_callback(serial_stream_manager.send)

loop = asyncio.get_event_loop()
loop.run_until_complete(main(serial_stream_manager.open_port(), serial_stream_manager.receive(), message_router.send()))
loop.close()