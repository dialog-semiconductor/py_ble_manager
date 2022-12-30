import asyncio
import serial_asyncio
from gtl_messages.gtl_message_base import GTL_INITIATOR


class SerialStreamManager(asyncio.Protocol):

    def __init__(self, tx_queue: asyncio.Queue[bytes], rx_queue: asyncio.Queue[bytes]) -> None:
        # TODO error check queues are asyncio.Queue
        # if(not tx_queue or not rx_queue):
        #   throw error
        self.tx_queue: asyncio.Queue[bytes] = tx_queue
        self.rx_queue: asyncio.Queue[bytes] = rx_queue

    async def open_port(self, com_port: str):
        self.reader, self.writer = await serial_asyncio.open_serial_connection(url=com_port, baudrate=115200)

    async def receive(self):
        while True:
            buffer = bytes()
            buffer = await self.reader.readexactly(1)
            if (buffer[0] == GTL_INITIATOR):
                # Get msg_id, dst_id, src_id, par_len. Use par_len to read rest of message
                buffer += await self.reader.readexactly(8)
                par_len = int.from_bytes(buffer[7:9], "little", signed=False)
                if (par_len != 0):
                    buffer += await self.reader.readexactly(par_len)

                self.rx_queue.put_nowait(buffer)
            else:
                print("Received some garbage")

    async def send(self):
        while True:
            # TODO instead of infinite loop, could we instead schedule this coroutine when an item is put on the queue?
            message = await self.tx_queue.get()
            self.writer.write(message)
            await self.writer.drain()
