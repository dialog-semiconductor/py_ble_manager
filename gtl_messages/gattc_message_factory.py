from ctypes import c_uint8

from gtl_messages.gtl_message_base import GTL_INITIATOR
from gtl_messages.gtl_message_gattc import GattcReadReqInd, GattcWriteReqInd, GattcCmpEvt
from gtl_port.gattc_task import GATTC_MSG_ID, gattc_read_req_ind, gattc_write_req_ind, gattc_cmp_evt


class GattcMessageFactory():

    @staticmethod
    def create_message(msg_bytes: bytes):
        assert (len(msg_bytes) >= 9)

        assert (int.from_bytes(msg_bytes[:1], "little", signed=False) == GTL_INITIATOR)

        # First byte is GTL header
        msg_id = GATTC_MSG_ID(int.from_bytes(msg_bytes[1:3], "little", signed=False))

        params_buf = msg_bytes[9:]

        # TODO for each case add a check to ensure params_buf not too long for parameters variable
        try:
            if msg_id == GATTC_MSG_ID.GATTC_READ_REQ_IND:
                return GattcReadReqInd(parameters=gattc_read_req_ind.from_buffer_copy(params_buf))

            elif msg_id == GATTC_MSG_ID.GATTC_WRITE_REQ_IND:
                # TODO issue using from_buffer_copy due to POINTER, is there a better way to convert?
                parameters = gattc_write_req_ind()
                parameters.handle = int.from_bytes(params_buf[0:2], "little", signed=False)
                parameters.offset = int.from_bytes(params_buf[2:4], "little", signed=False)
                parameters.value = (c_uint8 * len(params_buf[6:])).from_buffer_copy(params_buf[6:])
                return GattcWriteReqInd(parameters=parameters)

            elif msg_id == GATTC_MSG_ID.GATTC_CMP_EVT:
                return GattcCmpEvt(parameters=gattc_cmp_evt.from_buffer_copy(params_buf))


            else:
                raise AssertionError(f"GattcMessageFactory: Message type is unhandled or not valid. message={msg_bytes.hex()}")
        except AssertionError as e:
            print(e)
            raise e
