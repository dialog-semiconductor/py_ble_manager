from ..gtl_messages.gtl_message_base import GTL_INITIATOR
from ..gtl_messages.gtl_message_gattm import GattmAddSvcRsp, GattmAttSetValueRsp
from ..gtl_port.gattm_task import GATTM_MSG_ID, gattm_add_svc_rsp, gattm_att_set_value_rsp


class GattmMessageFactory():

    @staticmethod
    def create_message(msg_bytes: bytes):
        msg_id = GATTM_MSG_ID(int.from_bytes(msg_bytes[1:3], "little", signed=False))
        params_buf = msg_bytes[9:]

        # TODO for each case add a check to ensure params_buf not too long for parameters variable
        try:
            if msg_id == GATTM_MSG_ID.GATTM_ADD_SVC_RSP:
                return GattmAddSvcRsp(parameters=gattm_add_svc_rsp.from_buffer_copy(params_buf))

            elif msg_id == GATTM_MSG_ID.GATTM_ATT_SET_VALUE_RSP:
                return GattmAttSetValueRsp(parameters=gattm_att_set_value_rsp.from_buffer_copy(params_buf))

            else:
                raise AssertionError(f"GattmMessageFactory: Message type is unhandled or not valid. message={msg_bytes.hex()}")
        except AssertionError as e:
            print(e)
            raise e
