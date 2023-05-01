import concurrent.futures
import queue
import threading

from gtl_messages.gtl_message_factory import GtlMessageFactory
from gtl_messages.gtl_message_base import GtlMessageBase
from gtl_messages.gtl_message_gapm import GapmResetCmd
from gtl_port.gapm_task import GAPM_MSG_ID, GAPM_OPERATION, gapm_reset_cmd


class BleAdapter():
    def __init__(self,
                 command_q: queue.Queue[GtlMessageBase],
                 event_q: queue.Queue[GtlMessageBase],
                 serial_tx_q: queue.Queue[bytes],
                 serial_rx_q: queue.Queue[bytes],
                 shutdown_event: threading.Event,
                 gtl_debug: bool = False,
                 ) -> None:

        self.command_q: queue.Queue[GtlMessageBase] = command_q
        self.event_q: queue.Queue[GtlMessageBase] = event_q
        self.serial_tx_q: queue.Queue[bytes] = serial_tx_q
        self.serial_rx_q: queue.Queue[bytes] = serial_rx_q
        self.gtl_debug = gtl_debug
        self.ble_stack_initialized = False
        self._shutdown_event = shutdown_event

    def _adapter_task(self):

        executor = concurrent.futures.ThreadPoolExecutor(max_workers=2, thread_name_prefix='BleAdapter')

        self._tx_task = executor.submit(self._command_queue_get)
        self._rx_task = executor.submit(self._serial_rx_q_get)

        pending = [self._tx_task, self._rx_task]

        while True:

            if self._shutdown_event.is_set():
                executor.shutdown(wait=False, cancel_futures=True)
                
            done, pending = concurrent.futures.wait(pending, timeout=1, return_when=concurrent.futures.FIRST_COMPLETED)

            for task in done:
                if task is self._tx_task:
                    # This is from Ble Manager command queue.
                    if task.result():
                        self._process_command_queue(task.result())
                    if not self._shutdown_event.is_set():
                        self._tx_task = executor.submit(self._command_queue_get)
                        pending.add(self._tx_task)

                elif task is self._rx_task:
                    # This is from serial Rx queue
                    if task.result():
                        self._process_serial_rx_q(task.result())

                    if not self._shutdown_event.is_set():
                        self._rx_task = executor.submit(self._serial_rx_q_get)
                        pending.add(self._rx_task)

            if len(pending) == 0:
                break

    def _command_queue_get(self) -> GtlMessageBase:
        item = None
        while item is None:
            try:
                if self._shutdown_event.is_set():
                    print("Exiting Adapater _command_queue_get")
                    break
                item = self.command_q.get(timeout=1)
            except queue.Empty:
                pass
        return item

    def _create_reset_command(self):
        return GapmResetCmd(gapm_reset_cmd(GAPM_OPERATION.GAPM_RESET))

    def _process_command_queue(self, command: GtlMessageBase):
        self._send_serial_message(command)

    def _process_serial_rx_q(self, byte_string: bytes):
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
        self.serial_tx_q.put_nowait(message.to_bytes())

    def _serial_rx_q_get(self) -> bytes:
        item = None
        while item is None:
            try:
                if self._shutdown_event.is_set():
                    print("Exiting Adapater _serial_rx_q_get")
                    break
                item = self.serial_rx_q.get(timeout=1)
            except queue.Empty:
                pass
        return item

    def init(self):
        self._task = threading.Thread(target=self._adapter_task)
        self._task.start()
