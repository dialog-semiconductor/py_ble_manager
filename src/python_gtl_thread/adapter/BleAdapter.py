import queue
import threading

from ..gtl_messages.gtl_message_factory import GtlMessageFactory
from ..gtl_messages.gtl_message_base import GtlMessageBase
from ..gtl_messages.gtl_message_gapm import GapmResetCmd
from ..gtl_port.gapm_task import GAPM_MSG_ID, GAPM_OPERATION, gapm_reset_cmd


class BleAdapter():
    def __init__(self,
                 command_q: queue.Queue[GtlMessageBase],
                 event_q: queue.Queue[GtlMessageBase],
                 serial_tx_q: queue.Queue[bytes],
                 serial_rx_q: queue.Queue[bytes],
                 gtl_debug: bool = False,
                 ) -> None:

        self.command_q: queue.Queue[GtlMessageBase] = command_q
        self.event_q: queue.Queue[GtlMessageBase] = event_q
        self.serial_tx_q: queue.Queue[bytes] = serial_tx_q
        self.serial_rx_q: queue.Queue[bytes] = serial_rx_q
        self.gtl_debug = gtl_debug
        self.ble_stack_initialized = False

    def _command_queue_get(self) -> GtlMessageBase:
        return self.command_q.get()

    def _command_queue_task(self):
        while True:
            command = self._command_queue_get()
            self._process_command_queue(command)

    def _process_command_queue(self, command: GtlMessageBase):
        self._send_serial_message(command)

    def _process_serial_rx_q(self, byte_string: bytes):
        msg = GtlMessageFactory().create_message(byte_string)  
        if self.gtl_debug:
            print(f"<-- Rx: {msg}\n")

        if msg:
            if msg.msg_id == GAPM_MSG_ID.GAPM_DEVICE_READY_IND:
                # Reset the BLE Stacks
                gtl = GapmResetCmd(gapm_reset_cmd(GAPM_OPERATION.GAPM_RESET))  # TODO send to mgr instead to give it a chance to clean up?
                self._send_serial_message(gtl)

            elif msg.msg_id == GAPM_MSG_ID.GAPM_CMP_EVT:
                self.ble_stack_initialized = True
                self.event_q.put_nowait(msg)  # Not making an adapter msg, just forwarding to manager

            else:
                if self.ble_stack_initialized:
                    self.event_q.put_nowait(msg)
        else:
            # print(f"BleAdapter unhandled serial message. byte_string={byte_string.hex()}")
            pass

    def _send_serial_message(self, message: GtlMessageBase):
        if self.gtl_debug:
            print(f"--> Tx: {message}\n")
        self.serial_tx_q.put_nowait(message.to_bytes())

    def _serial_rx_q_get(self) -> bytes:
        return self.serial_rx_q.get()

    def _serial_rx_queue_task(self):
        while True:
            serial_rx = self._serial_rx_q_get()
            self._process_serial_rx_q(serial_rx)

    def init(self):
        self._command_task = threading.Thread(target=self._command_queue_task)
        self._command_task.daemon = True
        self._command_task.start()

        self._rx_q_task = threading.Thread(target=self._serial_rx_queue_task)
        self._rx_q_task.daemon = True
        self._rx_q_task.start()
