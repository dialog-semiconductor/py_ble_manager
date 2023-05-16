from ctypes import c_uint8

from ..gtl_messages.gtl_message_gattc import GattcReadReqInd, GattcWriteReqInd, GattcCmpEvt, GattcDiscSvcInd, GattcDiscCharInd, \
    GattcSdpSvcInd, GattcReadInd, GattcEventInd, GattcEventReqInd, GattcAttInfoReqInd
from ..gtl_port.gattc_task import GATTC_MSG_ID, gattc_read_req_ind, gattc_write_req_ind, gattc_cmp_evt, gattc_disc_svc_ind, \
    gattc_disc_char_ind, gattc_sdp_svc_ind, gattc_sdp_att_info, gattc_read_ind, gattc_event_ind, gattc_event_req_ind, \
    gattc_att_info_req_ind
from ..gtl_port.rwip_config import KE_API_ID


class GattcMessageFactory():

    @staticmethod
    def create_message(msg_bytes: bytes):
        msg_id = GATTC_MSG_ID(int.from_bytes(msg_bytes[1:3], "little", signed=False))
        dst_id = KE_API_ID(int.from_bytes(msg_bytes[3:4], "little", signed=False))

        if dst_id != KE_API_ID.TASK_ID_GTL:
            # If task ID is not TASK_ID_GTL, then it has the connection index in the LSB
            conidx = int.from_bytes(msg_bytes[4:5], "little", signed=False)
        else:
            conidx = int.from_bytes(msg_bytes[6:7], "little", signed=False)

        params_buf = msg_bytes[9:]

        try:
            if msg_id == GATTC_MSG_ID.GATTC_READ_REQ_IND:
                return GattcReadReqInd(conidx=conidx, parameters=gattc_read_req_ind.from_buffer_copy(params_buf))

            elif msg_id == GATTC_MSG_ID.GATTC_WRITE_REQ_IND:
                # note from_buffer_copy fails due to POINTER in gattc_write_req_ind
                parameters = gattc_write_req_ind()
                parameters.handle = int.from_bytes(params_buf[0:2], "little", signed=False)
                parameters.offset = int.from_bytes(params_buf[2:4], "little", signed=False)

                length = int.from_bytes(params_buf[4:6], "little", signed=False)
                assert length == len(params_buf[6:])  # Check for mismatch in value length and remaining bytes

                parameters.value = (c_uint8 * len(params_buf[6:])).from_buffer_copy(params_buf[6:])
                return GattcWriteReqInd(conidx=conidx, parameters=parameters)

            elif msg_id == GATTC_MSG_ID.GATTC_CMP_EVT:
                return GattcCmpEvt(conidx=conidx, parameters=gattc_cmp_evt.from_buffer_copy(params_buf))

            elif msg_id == GATTC_MSG_ID.GATTC_DISC_SVC_IND:
                parameters = gattc_disc_svc_ind()
                parameters.start_hdl = int.from_bytes(params_buf[0:2], "little", signed=False)
                parameters.end_hdl = int.from_bytes(params_buf[2:4], "little", signed=False)

                length = int.from_bytes(params_buf[4:5], "little", signed=False)
                assert length == len(params_buf[5:-1])  # Check for mismatch in value length and remaining bytes

                parameters.uuid = (c_uint8 * len(params_buf[5:-1])).from_buffer_copy(params_buf[5:-1])  # -1 to account for padding
                return GattcDiscSvcInd(conidx=conidx, parameters=parameters)

            elif msg_id == GATTC_MSG_ID.GATTC_DISC_CHAR_IND:
                parameters = gattc_disc_char_ind()
                parameters.attr_hdl = int.from_bytes(params_buf[0:2], "little", signed=False)
                parameters.pointer_hdl = int.from_bytes(params_buf[2:4], "little", signed=False)
                parameters.prop = int.from_bytes(params_buf[4:5], "little", signed=False)

                length = int.from_bytes(params_buf[5:6], "little", signed=False)
                assert length == len(params_buf[6:])  # Check for mismatch in value length and remaining bytes

                parameters.uuid = (c_uint8 * len(params_buf[6:])).from_buffer_copy(params_buf[6:])
                return GattcDiscCharInd(conidx=conidx, parameters=parameters)

            elif msg_id == GATTC_MSG_ID.GATTC_SDP_SVC_IND:
                parameters = gattc_sdp_svc_ind()
                parameters.uuid_len = int.from_bytes(params_buf[0:1], "little", signed=False)
                parameters.uuid = (c_uint8 * len(params_buf[1:17])).from_buffer_copy(params_buf[1:17])
                # params_buf[17:18] skipped to account for padding
                parameters.start_hdl = int.from_bytes(params_buf[18:20], "little", signed=False)
                parameters.end_hdl = int.from_bytes(params_buf[20:22], "little", signed=False)
                # max size for gattc_sdp_att_info is 22
                parameters.info = (gattc_sdp_att_info * (len(params_buf[22:]) // 22)).from_buffer_copy(params_buf[22:])

                return GattcSdpSvcInd(conidx=conidx, parameters=parameters)

            elif msg_id == GATTC_MSG_ID.GATTC_READ_IND:
                parameters = gattc_read_ind()
                parameters.handle = int.from_bytes(params_buf[0:2], "little", signed=False)
                parameters.offset = int.from_bytes(params_buf[2:4], "little", signed=False)

                length = int.from_bytes(params_buf[4:6], "little", signed=False)
                assert length == len(params_buf[6:])  # Check for mismatch in value length and remaining bytes

                parameters.value = (c_uint8 * len(params_buf[6:])).from_buffer_copy(params_buf[6:])

                return GattcReadInd(conidx=conidx, parameters=parameters)

            elif msg_id == GATTC_MSG_ID.GATTC_EVENT_IND:
                parameters = gattc_event_ind()
                parameters.type = int.from_bytes(params_buf[0:1], "little", signed=False)
                # params_buf[1:2] skipped to account for padding

                length = int.from_bytes(params_buf[2:4], "little", signed=False)
                parameters.handle = int.from_bytes(params_buf[4:6], "little", signed=False)
                assert length == len(params_buf[6:])  # Check for mismatch in value length and remaining bytes

                parameters.value = (c_uint8 * len(params_buf[6:])).from_buffer_copy(params_buf[6:])
                return GattcEventInd(conidx=conidx, parameters=parameters)

            elif msg_id == GATTC_MSG_ID.GATTC_EVENT_IND:
                parameters = gattc_event_req_ind()
                parameters.type = int.from_bytes(params_buf[0:1], "little", signed=False)
                # params_buf[1:2] skipped to account for padding

                length = int.from_bytes(params_buf[2:4], "little", signed=False)
                parameters.handle = int.from_bytes(params_buf[4:6], "little", signed=False)
                assert length == len(params_buf[6:])  # Check for mismatch in value length and remaining bytes

                parameters.value = (c_uint8 * len(params_buf[6:])).from_buffer_copy(params_buf[6:])
                return GattcEventReqInd(conidx=conidx, parameters=parameters)

            elif msg_id == GATTC_MSG_ID.GATTC_ATT_INFO_REQ_IND:
                return GattcAttInfoReqInd(conidx=conidx, parameters=gattc_att_info_req_ind.from_buffer_copy(params_buf))

            else:
                raise AssertionError(f"GattcMessageFactory: Message type is unhandled or not valid. message={msg_bytes.hex()}")
        except AssertionError as e:
            print(e)
            raise e
