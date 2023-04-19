import asyncio
import serial_asyncio

from gtl_messages.gtl_message_base import GTL_INITIATOR


class SerialStreamManager(asyncio.Protocol):

    def __init__(self, com_port: str, tx_queue: asyncio.Queue[bytes], rx_queue: asyncio.Queue[bytes]) -> None:
        self._tx_queue: asyncio.Queue[bytes] = tx_queue
        self._rx_queue: asyncio.Queue[bytes] = rx_queue
        self._com_port: str = com_port

    async def _serial_task(self):
        # create task to wait for data on the tx queue (e.g. data from the BLE adapter)
        self._serial_tx_task = asyncio.create_task(self._tx_queue_get(), name='SerialStreamTx')
        # create task to wait for data on the serial port
        self._serial_rx_task = asyncio.create_task(self._receive(), name='SerialStreamRx')
        pending = [self._serial_tx_task, self._serial_rx_task]

        while True:
            done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)

            for task in done:
                if task is self._serial_tx_task:
                    # We have received data on the Tx queue, send it and restart the task
                    # TODO need to rethink waiting here. The _receive task should never be
                    # be blocked for a long time or we will miss data
                    await self._send(task.result())
                    self._serial_tx_task = asyncio.create_task(self._tx_queue_get(), name='SerialStreamTx')
                    pending.add(self._serial_tx_task)

                elif task is self._serial_rx_task:
                    # This is from serial Rx queue
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

    async def _send(self, message: bytes):
        self.writer.write(message)
        await self.writer.drain()

    async def _tx_queue_get(self) -> bytes:
        return await self._tx_queue.get()

    def init(self):
        self._task = asyncio.create_task(self._serial_task(), name='SerialTask')

    async def open_serial_port(self):
        try:
            self.reader, self.writer = await asyncio.wait_for(serial_asyncio.open_serial_connection(url=self._com_port, baudrate=115200), timeout=5)
        except asyncio.TimeoutError:
            print(f"{type(self)} failed to open {self._com_port}")
