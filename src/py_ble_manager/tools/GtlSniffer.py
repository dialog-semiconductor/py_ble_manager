import queue
from ..gtl_messages.gtl_message_base import GtlMessageBase
from ..gtl_messages.gtl_message_factory import GtlMessageFactory
from ..gtl_port.rwip_config import KE_API_ID
from ..tools.GtlSerialReceiver import GtlSerialReceiver


class GtlSniffer():

    def __init__(self, com_port_rx: str, com_port_tx: str, baud_rate: int) -> None:
        self.msg_q = queue.Queue()
        self.rx_serial_path = GtlSerialReceiver(com_port_rx, baud_rate, self.msg_q)
        self.tx_serial_path = GtlSerialReceiver(com_port_tx, baud_rate, self.msg_q)

    def _get_gtl_msg_bytes(self, timeout: int = 0) -> bytes:
        try:
            msg = self.msg_q.get(timeout=timeout)
        except queue.Empty:
            msg = None
        return msg

    def _process_msg(self, byte_string: bytes) -> None:
        msg: GtlMessageBase = GtlMessageFactory.create_message(byte_string)
        if msg:
            if msg.dst_id == KE_API_ID.TASK_ID_GTL:
                msg_string = (f"<-- Rx: {msg}\n")
            elif msg.src_id == KE_API_ID.TASK_ID_GTL:
                msg_string = (f"--> Tx: {msg}\n")
            else:
                raise AssertionError("msg ID does not make sense")
        else:
            raise AssertionError(f"{__class__.__name__}.{__name__} unhandled serial message. byte_string={byte_string.hex()}")

        return msg_string

    def get_gtl_msg_str(self, timeout: int = 0) -> bytes:
        msg: bytes = self._get_gtl_msg_bytes(timeout)
        if msg:
            return self._process_msg(msg)
        return None

    def init(self):
        self.rx_serial_path.init()
        self.tx_serial_path.init()
