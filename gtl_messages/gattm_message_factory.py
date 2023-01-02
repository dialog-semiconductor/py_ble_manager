from .gtl_message_base import GTL_INITIATOR
from .gtl_message_gattm import GattmAddSvcRsp

from gtl_port.gattm_task import GATTM_MSG_ID, gattm_add_svc_rsp


class GattmMessageFactory():

    @staticmethod
    def create_message(msg_bytes: bytes):
        assert (len(msg_bytes) >= 9)

        assert (int.from_bytes(msg_bytes[:1], "little", signed=False) == GTL_INITIATOR)

        # First byte is GTL header
        msg_id = GATTM_MSG_ID(int.from_bytes(msg_bytes[1:3], "little", signed=False))

        params_buf = msg_bytes[9:]

        # TODO for each case add a check to ensure params_buf not too long for parameters variable
        try:
            if msg_id == GATTM_MSG_ID.GATTM_ADD_SVC_RSP:
                return GattmAddSvcRsp(parameters=gattm_add_svc_rsp.from_buffer_copy(params_buf))

            else:
                raise AssertionError(f"GattmMessageFactory: Message type is unhandled or not valid. message={msg_bytes.hex()}")
        except AssertionError as e:
            print(e)
            raise e
