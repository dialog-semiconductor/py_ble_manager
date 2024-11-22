import asyncio
import serial_asyncio

from py_ble_manager.gtl_messages.gtl_message_base import GTL_INITIATOR


class GtlAioSerialReceiver(asyncio.Protocol):

    def __init__(self, com_port: str, baud_rate: int, rx_queue: asyncio.Queue[bytes]) -> None:
        self._com_port: str = com_port
        self._baud_rate: int = baud_rate
        self._rx_queue: asyncio.Queue[bytes] = rx_queue

    async def _serial_task(self):
        self._serial_rx_task = asyncio.create_task(self._receive(), name='SerialStreamRx')
        pending = [self._serial_rx_task]

        while True:
            done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)

            for task in done:
                if task is self._serial_rx_task:
                    self._process_received_data(task.result())
                    self._serial_rx_task = asyncio.create_task(self._receive(), name='SerialStreamRx')
                    pending.add(self._serial_rx_task)

    def _process_received_data(self, buffer: bytes):
        if buffer:
            self._rx_queue.put_nowait(buffer)

    async def _receive(self):
        buffer = bytes()
        buffer = await self.reader.readexactly(1)
        if (buffer[0] == GTL_INITIATOR):
            # Get msg_id, dst_id, src_id, par_len. Use par_len to read rest of message
            buffer += await self.reader.readexactly(8)
            par_len = int.from_bytes(buffer[7:9], "little", signed=False)
            if (par_len != 0):
                buffer += await self.reader.readexactly(par_len)
        else:
            print("Received some garbage")
        return buffer

    def init(self):
        self._task = asyncio.create_task(self._serial_task(), name='SerialTask')

    async def open_serial_port(self):
        try:
            self.reader, self.writer = await asyncio.wait_for(serial_asyncio.open_serial_connection(url=self._com_port, baudrate=1000000), timeout=5)
        except asyncio.TimeoutError:
            print(f"{type(self)} failed to open {self._com_port}")
