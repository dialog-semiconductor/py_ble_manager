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

        self._command_q: queue.Queue[GtlMessageBase] = command_q
        self._event_q: queue.Queue[GtlMessageBase] = event_q
        self._serial_tx_q: queue.Queue[bytes] = serial_tx_q
        self._serial_rx_q: queue.Queue[bytes] = serial_rx_q
        self._gtl_debug = gtl_debug
        self._ble_stack_initialized = False

    def _command_queue_get(self) -> GtlMessageBase:
        return self._command_q.get()

    def _command_queue_task(self):
        while True:
            command = self._command_queue_get()
            self._process_command_queue(command)

    def _event_queue_send(self, gtl: GtlMessageBase):
        self._event_q.put_nowait(gtl)

    def _process_command_queue(self, command: GtlMessageBase):
        self._send_serial_message(command)

    def _process_serial_rx_q(self, byte_string: bytes):
        msg = GtlMessageFactory().create_message(byte_string)
        if self._gtl_debug:
            print(f"<-- Rx: {msg}\n")

        if msg:
            if msg.msg_id == GAPM_MSG_ID.GAPM_DEVICE_READY_IND:
                # Reset the BLE Stack
                gtl = GapmResetCmd(gapm_reset_cmd(GAPM_OPERATION.GAPM_RESET))
                self._send_serial_message(gtl)

            elif msg.msg_id == GAPM_MSG_ID.GAPM_CMP_EVT:
                self._ble_stack_initialized = True
                self._event_queue_send(msg)  # Not making an adapter msg, just forwarding to manager

            else:
                if self._ble_stack_initialized:
                    self._event_queue_send(msg)
        else:
            # print(f"BleAdapter unhandled serial message. byte_string={byte_string.hex()}")
            pass

    def _send_serial_message(self, message: GtlMessageBase):
        if self._gtl_debug:
            print(f"--> Tx: {message}\n")
        self._serial_tx_q.put_nowait(message.to_bytes())

    def _serial_rx_q_get(self) -> bytes:
        return self._serial_rx_q.get()

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
