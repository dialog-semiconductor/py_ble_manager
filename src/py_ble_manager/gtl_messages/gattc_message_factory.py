from ctypes import c_uint8

from ..gtl_messages.gtl_message_gattc import GattcReadReqInd, GattcWriteReqInd, GattcCmpEvt, GattcDiscSvcInd, GattcDiscCharInd, \
    GattcSdpSvcInd, GattcReadInd, GattcEventInd, GattcEventReqInd, GattcAttInfoReqInd, GattcMtuChangedInd, GattcDiscCharDescInd, \
    GattcSvcChangedCfgInd, GattcDiscSvcInclInd, GattcExcMtuCmd, GattcWriteCfm, GattcAttInfoCfm, GattcReadCfm, GattcSendEvtCmd, \
    GattcEventCfm, GattcDiscCmd, GattcSdpSvcDiscCmd, GattcReadCmd, GattcWriteCmd, GattcWriteExecuteCmd, GattcTransactionToErrorInd
from ..gtl_port.gattc_task import GATTC_MSG_ID, gattc_read_req_ind, gattc_write_req_ind, gattc_cmp_evt, gattc_disc_svc_ind, \
    gattc_disc_char_ind, gattc_sdp_svc_ind, gattc_sdp_att_info, gattc_read_ind, gattc_event_ind, gattc_event_req_ind, \
    gattc_att_info_req_ind, gattc_mtu_changed_ind, gattc_disc_char_desc_ind, gattc_svc_changed_cfg, gattc_disc_svc_incl_ind, \
    gattc_exc_mtu_cmd, gattc_write_cfm, gattc_att_info_cfm, gattc_read_cfm, gattc_send_evt_cmd, gattc_event_cfm, gattc_disc_cmd, \
    gattc_sdp_svc_disc_cmd, ATT_UUID_128_LEN, gattc_read_cmd, gattc_read_req, GATTC_OPERATION, gattc_read_simple, gattc_read_by_uuid, \
    gattc_read_multiple, gattc_write_cmd, gattc_execute_write_cmd
from ..gtl_port.rwip_config import KE_API_ID


class GattcMessageFactory():

    @staticmethod
    def create_message(msg_bytes: bytes):
        msg_id = GATTC_MSG_ID(int.from_bytes(msg_bytes[1:3], "little", signed=False))
        dst_id = KE_API_ID(int.from_bytes(msg_bytes[3:4], "little", signed=False))

        if dst_id != KE_API_ID.TASK_ID_GTL:
            # If task ID is not TASK_ID_GTL, then it has the connection index in the MSB
            conidx = int.from_bytes(msg_bytes[4:5], "little", signed=False)
        else:
            conidx = int.from_bytes(msg_bytes[6:7], "little", signed=False)

        params_buf = msg_bytes[9:]

        try:

            if msg_id == GATTC_MSG_ID.GATTC_EXC_MTU_CMD:
                return GattcExcMtuCmd(conidx=conidx, parameters=gattc_exc_mtu_cmd.from_buffer_copy(params_buf))

            elif msg_id == GATTC_MSG_ID.GATTC_MTU_CHANGED_IND:
                return GattcMtuChangedInd(conidx=conidx, parameters=gattc_mtu_changed_ind.from_buffer_copy(params_buf))

            elif msg_id == GATTC_MSG_ID.GATTC_WRITE_REQ_IND:
                # note from_buffer_copy fails due to POINTER in gattc_write_req_ind
                parameters = gattc_write_req_ind()
                parameters.handle = int.from_bytes(params_buf[0:2], "little", signed=False)
                parameters.offset = int.from_bytes(params_buf[2:4], "little", signed=False)

                length = int.from_bytes(params_buf[4:6], "little", signed=False)
                assert length == len(params_buf[6:]), f"Expected {length}, received: {len(params_buf[6:])}"  # Check for mismatch in value length and remaining bytes

                parameters.value = (c_uint8 * len(params_buf[6:])).from_buffer_copy(params_buf[6:])
                return GattcWriteReqInd(conidx=conidx, parameters=parameters)

            elif msg_id == GATTC_MSG_ID.GATTC_WRITE_CFM:
                return GattcWriteCfm(conidx=conidx, parameters=gattc_write_cfm.from_buffer_copy(params_buf))

            elif msg_id == GATTC_MSG_ID.GATTC_ATT_INFO_REQ_IND:
                return GattcAttInfoReqInd(conidx=conidx, parameters=gattc_att_info_req_ind.from_buffer_copy(params_buf))

            elif msg_id == GATTC_MSG_ID.GATTC_ATT_INFO_CFM:
                return GattcAttInfoCfm(conidx=conidx, parameters=gattc_att_info_cfm.from_buffer_copy(params_buf))

            elif msg_id == GATTC_MSG_ID.GATTC_READ_REQ_IND:
                return GattcReadReqInd(conidx=conidx, parameters=gattc_read_req_ind.from_buffer_copy(params_buf))

            elif msg_id == GATTC_MSG_ID.GATTC_READ_CFM:
                # note from_buffer_copy fails due to POINTER in gattc_read_cfm
                parameters = gattc_read_cfm()
                parameters.handle = int.from_bytes(params_buf[0:2], "little", signed=False)

                # parameters.length will be set when parameters.value set
                length = int.from_bytes(params_buf[2:4], "little", signed=False)

                parameters.status = int.from_bytes(params_buf[4:5], "little", signed=False)

                # value is list of c_uint8
                assert (length) == len(params_buf[5:-1]), f"Expected {length}, received: {len(params_buf[5:-1])}"  # Check for mismatch in value length and remaining bytes, -1 to account for padding

                parameters.value = (c_uint8 * length).from_buffer_copy(params_buf[5:-1])
                return GattcReadCfm(parameters=parameters)

            elif msg_id == GATTC_MSG_ID.GATTC_SEND_EVT_CMD:
                # note from_buffer_copy fails due to POINTER in gattc_send_evt_cmd
                parameters = gattc_send_evt_cmd()
                parameters.operation = int.from_bytes(params_buf[0:1], "little", signed=False)
                # one byte padding we can ignore
                # padding = int.from_bytes(params_buf[1:2], "little", signed=False)
                parameters.seq_num = int.from_bytes(params_buf[2:4], "little", signed=False)
                parameters.handle = int.from_bytes(params_buf[4:6], "little", signed=False)

                # parameters.length will be set when parameters.value set
                length = int.from_bytes(params_buf[6:8], "little", signed=False)
                # value is list of c_uint8
                assert (length) == len(params_buf[8:]), f"Expected {length}, received: {len(params_buf[8:])}"  # Check for mismatch in value length and remaining bytes

                parameters.value = (c_uint8 * length).from_buffer_copy(params_buf[8:])
                return GattcSendEvtCmd(parameters=parameters)

            elif msg_id == GATTC_MSG_ID.GATTC_CMP_EVT:
                return GattcCmpEvt(conidx=conidx, parameters=gattc_cmp_evt.from_buffer_copy(params_buf))

            elif msg_id == GATTC_MSG_ID.GATTC_EVENT_IND:
                parameters = gattc_event_ind()
                parameters.type = int.from_bytes(params_buf[0:1], "little", signed=False)
                # params_buf[1:2] skipped to account for padding

                length = int.from_bytes(params_buf[2:4], "little", signed=False)
                parameters.handle = int.from_bytes(params_buf[4:6], "little", signed=False)
                assert length == len(params_buf[6:]), f"Expected {length}, received: {len(params_buf[6:])}"  # Check for mismatch in value length and remaining bytes

                parameters.value = (c_uint8 * len(params_buf[6:])).from_buffer_copy(params_buf[6:])
                return GattcEventInd(conidx=conidx, parameters=parameters)

            elif msg_id == GATTC_MSG_ID.GATTC_EVENT_REQ_IND:
                parameters = gattc_event_req_ind()
                parameters.type = int.from_bytes(params_buf[0:1], "little", signed=False)
                # params_buf[1:2] skipped to account for padding

                length = int.from_bytes(params_buf[2:4], "little", signed=False)
                parameters.handle = int.from_bytes(params_buf[4:6], "little", signed=False)
                assert length == len(params_buf[6:]), f"Expected {length}, received: {len(params_buf[6:])}"  # Check for mismatch in value length and remaining bytes

                parameters.value = (c_uint8 * len(params_buf[6:])).from_buffer_copy(params_buf[6:])
                return GattcEventReqInd(conidx=conidx, parameters=parameters)

            elif msg_id == GATTC_MSG_ID.GATTC_EVENT_CFM:
                return GattcEventCfm(conidx=conidx, parameters=gattc_event_cfm.from_buffer_copy(params_buf))

            elif msg_id == GATTC_MSG_ID.GATTC_DISC_CMD:
                # note from_buffer_copy fails due to POINTER in gattc_disc_cmd
                parameters = gattc_disc_cmd()
                parameters.operation = int.from_bytes(params_buf[0:1], "little", signed=False)
                # parameters.uuid_len will be set when parameters.uuid set
                uuid_len = int.from_bytes(params_buf[1:2], "little", signed=False)

                parameters.seq_num = int.from_bytes(params_buf[2:4], "little", signed=False)
                parameters.start_hdl = int.from_bytes(params_buf[4:6], "little", signed=False)
                parameters.end_hdl = int.from_bytes(params_buf[6:8], "little", signed=False)

                # value is list of c_uint8
                assert (uuid_len) == len(params_buf[8:]), f"Expected {length}, received: {len(params_buf[8:])}"  # Check for mismatch in value length and remaining bytes

                parameters.uuid = (c_uint8 * uuid_len).from_buffer_copy(params_buf[8:])
                return GattcDiscCmd(parameters=parameters)

            elif msg_id == GATTC_MSG_ID.GATTC_DISC_CHAR_DESC_IND:
                parameters = gattc_disc_char_desc_ind()
                parameters.attr_hdl = int.from_bytes(params_buf[0:2], "little", signed=False)

                uuid_len = int.from_bytes(params_buf[2:3], "little", signed=False)
                assert uuid_len == len(params_buf[3:-1]), f"Expected {length}, received: {len(params_buf[3:-1])}"  # Check for mismatch in uuid_len and remaining bytes. Index to -1 to account for padding

                parameters.uuid = (c_uint8 * uuid_len).from_buffer_copy(params_buf[3:-1])
                return GattcDiscCharDescInd(conidx=conidx, parameters=parameters)

            elif msg_id == GATTC_MSG_ID.GATTC_DISC_SVC_IND:
                parameters = gattc_disc_svc_ind()
                parameters.start_hdl = int.from_bytes(params_buf[0:2], "little", signed=False)
                parameters.end_hdl = int.from_bytes(params_buf[2:4], "little", signed=False)

                uuid_len = int.from_bytes(params_buf[4:5], "little", signed=False)
                assert uuid_len == len(params_buf[5:-1]), f"Expected {length}, received: {len(params_buf[5:-1])}"  # Check for mismatch in uuid_len and remaining bytes, -1 to account for padding

                parameters.uuid = (c_uint8 * uuid_len).from_buffer_copy(params_buf[5:-1])
                return GattcDiscSvcInd(conidx=conidx, parameters=parameters)

            elif msg_id == GATTC_MSG_ID.GATTC_DISC_SVC_INCL_IND:
                # note from_buffer_copy fails due to POINTER in gattc_disc_svc_incl_ind
                parameters = gattc_disc_svc_incl_ind()
                parameters.attr_hdl = int.from_bytes(params_buf[0:2], "little", signed=False)
                parameters.start_hdl = int.from_bytes(params_buf[2:4], "little", signed=False)
                parameters.end_hdl = int.from_bytes(params_buf[4:6], "little", signed=False)

                uuid_len = int.from_bytes(params_buf[6:7], "little", signed=False)
                # Check for mismatch in uuid_len and remaining bytes, -1 to account for padding
                assert uuid_len == len(params_buf[7:-1]), f"Expected {uuid_len}, received: {len(params_buf[7:-1])}"
                parameters.uuid = (c_uint8 * uuid_len).from_buffer_copy(params_buf[7:-1])
                return GattcDiscSvcInclInd(conidx=conidx, parameters=parameters)

            elif msg_id == GATTC_MSG_ID.GATTC_DISC_CHAR_IND:
                parameters = gattc_disc_char_ind()
                parameters.attr_hdl = int.from_bytes(params_buf[0:2], "little", signed=False)
                parameters.pointer_hdl = int.from_bytes(params_buf[2:4], "little", signed=False)
                parameters.prop = int.from_bytes(params_buf[4:5], "little", signed=False)

                uuid_len = int.from_bytes(params_buf[5:6], "little", signed=False)
                # Check for mismatch in uuid_len and remaining bytes
                assert uuid_len == len(params_buf[6:]), f"Expected {uuid_len}, received: {len(params_buf[6:])}"

                parameters.uuid = (c_uint8 * uuid_len).from_buffer_copy(params_buf[6:])
                return GattcDiscCharInd(conidx=conidx, parameters=parameters)

            elif msg_id == GATTC_MSG_ID.GATTC_SDP_SVC_DISC_CMD:
                parameters = gattc_sdp_svc_disc_cmd()
                parameters.operation = int.from_bytes(params_buf[0:1], "little", signed=False)
                uuid_len = int.from_bytes(params_buf[1:2], "little", signed=False)
                parameters.seq_num = int.from_bytes(params_buf[2:4], "little", signed=False)
                parameters.start_hdl = int.from_bytes(params_buf[4:6], "little", signed=False)
                parameters.end_hdl = int.from_bytes(params_buf[6:8], "little", signed=False)

                # no assert as message has additional padding based on uuid len and will always fail
                # assert uuid_len == len(params_buf[6:])  # Check for mismatch in uuid_len and remaining bytes

                parameters.uuid = (c_uint8 * uuid_len).from_buffer_copy(params_buf[8:(8 + uuid_len)])
                return GattcSdpSvcDiscCmd(conidx=conidx, parameters=parameters)

            elif msg_id == GATTC_MSG_ID.GATTC_SDP_SVC_IND:
                parameters = gattc_sdp_svc_ind()
                parameters.uuid_len = int.from_bytes(params_buf[0:1], "little", signed=False)
                parameters.uuid = (c_uint8 * parameters.uuid_len).from_buffer_copy(params_buf[1:(1 + parameters.uuid_len)])
                # params_buf[17:18] skipped to account for padding
                parameters.start_hdl = int.from_bytes(params_buf[18:20], "little", signed=False)
                parameters.end_hdl = int.from_bytes(params_buf[20:22], "little", signed=False)
                # max size for gattc_sdp_att_info is 22
                parameters.info = (gattc_sdp_att_info * (len(params_buf[22:]) // 22)).from_buffer_copy(params_buf[22:])

                return GattcSdpSvcInd(conidx=conidx, parameters=parameters)

            elif msg_id == GATTC_MSG_ID.GATTC_READ_CMD:
                parameters = gattc_read_cmd()
                parameters.operation = int.from_bytes(params_buf[0:1], "little", signed=False)
                nb = int.from_bytes(params_buf[1:2], "little", signed=False)
                parameters.seq_num = int.from_bytes(params_buf[2:4], "little", signed=False)

                match parameters.operation:
                    case (GATTC_OPERATION.GATTC_READ
                            | GATTC_OPERATION.GATTC_READ_LONG):

                        parameters.req.simple = gattc_read_simple.from_buffer_copy(params_buf[4:])

                    case GATTC_OPERATION.GATTC_READ_BY_UUID:
                        assert f"GattcReadCmd operation={GATTC_OPERATION.GATTC_READ_BY_UUID} not supported"

                    case GATTC_OPERATION.GATTC_READ_MULTIPLE:
                        assert f"GattcReadCmd operation={GATTC_OPERATION.GATTC_READ_BY_UUID} not supported"

                return GattcReadCmd(conidx=conidx, parameters=parameters)

            elif msg_id == GATTC_MSG_ID.GATTC_READ_IND:
                parameters = gattc_read_ind()
                parameters.handle = int.from_bytes(params_buf[0:2], "little", signed=False)
                parameters.offset = int.from_bytes(params_buf[2:4], "little", signed=False)

                length = int.from_bytes(params_buf[4:6], "little", signed=False)
                assert length == len(params_buf[6:]), f"Expected {length}, received: {len(params_buf[6:])}"  # Check for mismatch in value length and remaining bytes

                parameters.value = (c_uint8 * len(params_buf[6:])).from_buffer_copy(params_buf[6:])

                return GattcReadInd(conidx=conidx, parameters=parameters)

            elif msg_id == GATTC_MSG_ID.GATTC_WRITE_CMD:
                parameters = gattc_write_cmd()
                parameters.operation = int.from_bytes(params_buf[0:1], "little", signed=False)
                parameters.auto_execute = int.from_bytes(params_buf[1:2], "little", signed=False)
                parameters.seq_num = int.from_bytes(params_buf[2:4], "little", signed=False)
                parameters.handle = int.from_bytes(params_buf[4:6], "little", signed=False)
                parameters.offset = int.from_bytes(params_buf[6:8], "little", signed=False)
                length = int.from_bytes(params_buf[8:10], "little", signed=False)
                parameters.cursor = int.from_bytes(params_buf[10:12], "little", signed=False)
                parameters.value = (c_uint8 * length).from_buffer_copy(params_buf[12:])
                return GattcWriteCmd(conidx=conidx, parameters=parameters)

            elif msg_id == GATTC_MSG_ID.GATTC_EXECUTE_WRITE_CMD:
                return GattcWriteExecuteCmd(conidx=conidx, parameters=gattc_execute_write_cmd.from_buffer_copy(params_buf))       

            elif msg_id == GATTC_MSG_ID.GATTC_SVC_CHANGED_CFG_IND:
                return GattcSvcChangedCfgInd(conidx=conidx, parameters=gattc_svc_changed_cfg.from_buffer_copy(params_buf))

            elif msg_id == GATTC_MSG_ID.GATTC_TRANSACTION_TO_ERROR_IND:
                return GattcTransactionToErrorInd(conidx=conidx)

            else:
                raise AssertionError(f"GattcMessageFactory: Message type is unhandled or not valid. message={msg_bytes.hex()}")
        except AssertionError as e:
            print(e)
            raise e
