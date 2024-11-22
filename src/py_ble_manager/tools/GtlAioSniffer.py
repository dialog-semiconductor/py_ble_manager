import asyncio

from ..gtl_messages.gtl_message_base import GtlMessageBase
from ..gtl_messages.gtl_message_factory import GtlMessageFactory
from ..gtl_port.rwip_config import KE_API_ID
from ..tools.GtlAioSerialReceiver import GtlAioSerialReceiver


class GtlAioSniffer():

    def __init__(self, com_port_1: str, com_port_2: str = None, baud_rate: int = 1000000) -> None:
        self._msg_q: asyncio.Queue[bytes] = asyncio.Queue()

        self._serial_path_1 = GtlAioSerialReceiver(com_port_1, baud_rate, self._msg_q)
        if com_port_2:
            self._serial_path_2 = GtlAioSerialReceiver(com_port_2, baud_rate, self._msg_q)
        else:
            self._serial_path_2 = None

    async def _get_gtl_msg_bytes(self, timeout: int = 0) -> bytes:
        try:
            timeout_seconds = timeout if timeout else None
            msg = await asyncio.wait_for(self._msg_q.get(), timeout_seconds)
        except asyncio.TimeoutError:
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

    async def get_gtl_msg_str(self, timeout: int = 0) -> bytes:
        msg: bytes = await self._get_gtl_msg_bytes(timeout)
        if msg:
            return self._process_msg(msg)
        return None

    async def init(self):
        await self._serial_path_1.open_serial_port()
        self._serial_path_1.init()
        if self._serial_path_2:
            await self._serial_path_2.open_serial_port()
            self._serial_path_2.init()
