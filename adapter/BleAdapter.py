import asyncio

from gtl_messages.gtl_message_factory import GtlMessageFactory
from adapter.SerialStreamManager import SerialStreamManager
from gtl_messages.gtl_message_base import GtlMessageBase
from gtl_messages.gtl_message_gapm import GapmResetCmd
from gtl_port.gapm_task import GAPM_MSG_ID, GAPM_OPERATION, gapm_reset_cmd


class BleAdapter():
    def __init__(self,
                 com_port: str,
                 command_q: asyncio.Queue[GtlMessageBase],
                 event_q: asyncio.Queue[GtlMessageBase],
                 gtl_debug: bool = False) -> None:

        self.gtl_debug = gtl_debug
        self.event_observers = []
        self.command_q: asyncio.Queue[GtlMessageBase] = command_q
        self.event_q: asyncio.Queue[GtlMessageBase] = event_q
        self.ble_stack_initialized = False

        self.com_port = com_port
        self.serial_tx_queue: asyncio.Queue[bytes] = asyncio.Queue()
        self.serial_rx_queue: asyncio.Queue[bytes] = asyncio.Queue()

        self.serial_stream_manager = SerialStreamManager(self.serial_tx_queue, self.serial_rx_queue)

    async def _adapter_task(self):

        self._tx_task = asyncio.create_task(self._command_queue_get(), name='BleAdapterTx')
        self._rx_task = asyncio.create_task(self._serial_rx_queue_get(), name='BleAdapterRx')

        pending = [self._tx_task, self._rx_task]

        while True:
            done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)

            for task in done:
                if task is self._tx_task:
                    # This is from Ble Manager command queue
                    self._process_command_queue(task.result())
                    self._tx_task = asyncio.create_task(self._command_queue_get(), name='BleAdapterTx')
                    pending.add(self._tx_task)

                elif self._rx_task:
                    # This is from serial Rx queue
                    self._process_serial_rx_queue(task.result())
                    self._rx_task = asyncio.create_task(self._serial_rx_queue_get(), name='BleAdapterRx')
                    pending.add(self._rx_task)

    async def _command_queue_get(self) -> GtlMessageBase:
        return await self.command_q.get()

    def _create_reset_command(self):
        return GapmResetCmd(gapm_reset_cmd(GAPM_OPERATION.GAPM_RESET))

    def _process_command_queue(self, command: GtlMessageBase):
        self._send_serial_message(command)

    def _process_serial_rx_queue(self, byte_string: bytes):
        msg = GtlMessageFactory().create_message(byte_string)  # # TODO catch error
        if self.gtl_debug:
            print(f"<-- Rx: {msg}\n")

        if msg:
            if msg.msg_id == GAPM_MSG_ID.GAPM_DEVICE_READY_IND:
                # Reset the BLE Stacks
                command = self._create_reset_command()  # TODO thin this should go to mgr instead to give it a chance to clean up
                self._send_serial_message(command)

            elif msg.msg_id == GAPM_MSG_ID.GAPM_CMP_EVT:
                self.ble_stack_initialized = True
                self.event_q.put_nowait(msg)  # Not making an adapter msg, just forwarding to manager

            else:
                self.event_q.put_nowait(msg)
        else:
            print("BleAdapter unhandled serial message")

    def _send_serial_message(self, message: GtlMessageBase):
        if self.gtl_debug:
            print(f"--> Tx: {message}\n")
        self.serial_tx_queue.put_nowait(message.to_bytes())

    async def _serial_rx_queue_get(self) -> bytes:
        return await self.serial_rx_queue.get()

    def _task_done_handler(self, task: asyncio.Task):
        if task.exception():
            task.result()  # Raise the exception

    def init(self):
        self._task = asyncio.create_task(self._adapter_task(), name='BleAdapterTask')
        self._task.add_done_callback(self._task_done_handler)

        self.serial_tx_task = asyncio.create_task(self.serial_stream_manager.send(), name='SerialStreamTx')
        self.serial_tx_task.add_done_callback(self._task_done_handler)
        self.serial_rx_task = asyncio.create_task(self.serial_stream_manager.receive(), name='SerialStreamRx')
        self.serial_rx_task.add_done_callback(self._task_done_handler)

    async def open_serial_port(self):
        try:
            await asyncio.wait_for(self.serial_stream_manager.open_port(self.com_port), timeout=5)

        except asyncio.TimeoutError:
            print(f"{type(self)} failed to open {self.com_port}")
