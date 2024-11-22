import queue
from ..gtl_messages.gtl_message_base import GtlMessageBase
from ..gtl_messages.gtl_message_factory import GtlMessageFactory
from ..gtl_port.rwip_config import KE_API_ID
from ..tools.GtlSerialReceiver import GtlSerialReceiver


class GtlSniffer():

    def __init__(self, com_port_1: str, com_port_2: str = None, baud_rate: int = 1000000) -> None:
        self._msg_q = queue.Queue()
        self._serial_path_1 = GtlSerialReceiver(com_port_1, baud_rate, self._msg_q)
        if com_port_2:
            self._serial_path_2 = GtlSerialReceiver(com_port_2, baud_rate, self._msg_q)
        else:
            self._serial_path_2 = None

    def _get_gtl_msg_bytes(self, timeout: int = 0) -> bytes:
        try:
            msg = self._msg_q.get(timeout=timeout)
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
                raise AssertionError(f"{__class__.__name__}.{__name__}: invalid msg ID. msg.src_id={msg.src_id}, msg.dst_id={msg.dst_id} ")
        else:
            raise AssertionError(f"{__class__.__name__}.{__name__}: unhandled serial message. byte_string={byte_string.hex()}")

        return msg_string

    def get_gtl_msg_str(self, timeout: int = 0) -> bytes:
        msg: bytes = self._get_gtl_msg_bytes(timeout)
        if msg:
            return self._process_msg(msg)
        return None

    def init(self):
        self._serial_path_1.init()
        if self._serial_path_2:
            self._serial_path_2.init()
