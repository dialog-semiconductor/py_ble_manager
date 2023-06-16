from ..gtl_messages.gtl_message_base import GTL_INITIATOR
from ..gtl_messages.gapc_message_factory import GapcMessageFactory
from ..gtl_messages.gapm_message_factory import GapmMessageFactory
from ..gtl_messages.gattm_message_factory import GattmMessageFactory
from ..gtl_messages.gattc_message_factory import GattcMessageFactory
from ..gtl_port.rwip_config import KE_API_ID


class GtlMessageFactory():

    @staticmethod
    def create_message(msg_bytes: bytes):
        if len(msg_bytes) < 9:
            return None
        if int.from_bytes(msg_bytes[:1], "little", signed=False) != GTL_INITIATOR:
            return None

        # There may be a connection index in the MSB of the dst_id or src_id.
        # Only use LSB to identify
        dst_id = KE_API_ID(int.from_bytes(msg_bytes[3:4], "little", signed=False))
        src_id = KE_API_ID(int.from_bytes(msg_bytes[5:6], "little", signed=False))

        # Message type will be defined under the files associated with the non-GTL task id in the message
        message_task_id = src_id
        if (src_id == KE_API_ID.TASK_ID_GTL):
            message_task_id = dst_id

        try:
            if message_task_id == KE_API_ID.TASK_ID_GAPM:
                return GapmMessageFactory().create_message(msg_bytes)

            elif message_task_id == KE_API_ID.TASK_ID_GAPC:
                return GapcMessageFactory().create_message(msg_bytes)

            elif message_task_id == KE_API_ID.TASK_ID_GATTM:
                return GattmMessageFactory().create_message(msg_bytes)

            elif message_task_id == KE_API_ID.TASK_ID_GATTC:
                return GattcMessageFactory().create_message(msg_bytes)

            else:
                raise AssertionError(f"GtlMessageFactory: Message type is unhandled or not valid. message={msg_bytes.hex()}")
        except AssertionError as e:
            print(e)
            raise e
