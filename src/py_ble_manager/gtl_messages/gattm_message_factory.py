from ctypes import c_uint8
from ..gtl_messages.gtl_message_gattm import GattmAddSvcReq, GattmAddSvcRsp, GattmAttSetValueRsp, GattmSvcGetPermissionReq, \
    GattmSvcGetPermissionRsp, GattmSvcSetPermissionReq, GattmSvcSetPermissionRsp, GattmAttSetValueReq, GattmAttGetValueReq,\
    GattmAttGetValueRsp
from ..gtl_port.gattm_task import GATTM_MSG_ID, gattm_add_svc_req, attm_svc_perm, gattm_add_svc_rsp, gattm_att_set_value_rsp, \
    ATT_UUID_128_LEN, gattm_att_desc, gattm_svc_get_permission_req, gattm_svc_get_permission_rsp, gattm_svc_set_permission_req, \
    gattm_svc_set_permission_rsp, gattm_att_set_value_req, gattm_att_get_value_req, gattm_att_get_value_rsp


class GattmMessageFactory():

    @staticmethod
    def create_message(msg_bytes: bytes):
        msg_id = GATTM_MSG_ID(int.from_bytes(msg_bytes[1:3], "little", signed=False))
        params_buf = msg_bytes[9:]

        try:
            if msg_id == GATTM_MSG_ID.GATTM_ADD_SVC_REQ:
                # note from_buffer_copy fails due to POINTER in gattm_svc_desc
                parameters = gattm_add_svc_req()
                parameters.svc_desc.start_hdl = int.from_bytes(params_buf[0:2], "little", signed=False)
                parameters.svc_desc.task_id = int.from_bytes(params_buf[2:4], "little", signed=False)
                parameters.svc_desc.perm = attm_svc_perm.from_buffer_copy(params_buf[4:5])

                # parameters.svc_desc.nb_att will be set when parameters.svc_desc.atts set
                nb_att = int.from_bytes(params_buf[5:6], "little", signed=False)
                parameters.svc_desc.uuid = (c_uint8 * ATT_UUID_128_LEN).from_buffer_copy(params_buf[6:22])

                # two bytes padding we can ignore
                # padding = int.from_bytes(params_buf[22:24], "little", signed=False)

                # atts is list of gattm_att_desc which is 24 bytes
                assert (nb_att * 24) == len(params_buf[24:]), f"Expected {nb_att * 24}, received: {len(params_buf[24:])}"  # Check for mismatch in value length and remaining bytes

                parameters.svc_desc.atts = (gattm_att_desc * nb_att).from_buffer_copy(params_buf[24:])
                return GattmAddSvcReq(parameters=parameters)

            elif msg_id == GATTM_MSG_ID.GATTM_ADD_SVC_RSP:
                return GattmAddSvcRsp(parameters=gattm_add_svc_rsp.from_buffer_copy(params_buf))

            elif msg_id == GATTM_MSG_ID.GATTM_SVC_GET_PERMISSION_REQ:
                return GattmSvcGetPermissionReq(parameters=gattm_svc_get_permission_req.from_buffer_copy(params_buf))

            elif msg_id == GATTM_MSG_ID.GATTM_SVC_GET_PERMISSION_RSP:
                return GattmSvcGetPermissionRsp(parameters=gattm_svc_get_permission_rsp.from_buffer_copy(params_buf))

            elif msg_id == GATTM_MSG_ID.GATTM_SVC_SET_PERMISSION_REQ:
                return GattmSvcSetPermissionReq(parameters=gattm_svc_set_permission_req.from_buffer_copy(params_buf))

            elif msg_id == GATTM_MSG_ID.GATTM_SVC_SET_PERMISSION_RSP:
                return GattmSvcSetPermissionRsp(parameters=gattm_svc_set_permission_rsp.from_buffer_copy(params_buf))

            elif msg_id == GATTM_MSG_ID.GATTM_ATT_SET_VALUE_REQ:

                # note from_buffer_copy fails due to POINTER in gattm_att_set_value_req
                parameters = gattm_att_set_value_req()
                parameters.handle = int.from_bytes(params_buf[0:2], "little", signed=False)

                # parameters.length will be set when parameters.valye set
                length = int.from_bytes(params_buf[2:4], "little", signed=False)

                # value is list of c_uint8 which is 24 bytes
                assert (length) == len(params_buf[4:]), f"Expected {length}, received: {len(params_buf[4:])}"  # Check for mismatch in value length and remaining bytes

                parameters.value = (c_uint8 * length).from_buffer_copy(params_buf[4:])
                return GattmAttSetValueReq(parameters=parameters)   

            elif msg_id == GATTM_MSG_ID.GATTM_ATT_SET_VALUE_RSP:
                return GattmAttSetValueRsp(parameters=gattm_att_set_value_rsp.from_buffer_copy(params_buf))

            elif msg_id == GATTM_MSG_ID.GATTM_ATT_GET_VALUE_REQ:
                return GattmAttGetValueReq(parameters=gattm_att_get_value_req.from_buffer_copy(params_buf))

            elif msg_id == GATTM_MSG_ID.GATTM_ATT_GET_VALUE_RSP:

                # note from_buffer_copy fails due to POINTER in gattm_att_get_value_rsp
                parameters = gattm_att_get_value_rsp()
                parameters.handle = int.from_bytes(params_buf[0:2], "little", signed=False)

                # parameters.length will be set when parameters.value set
                length = int.from_bytes(params_buf[2:4], "little", signed=False)

                parameters.status = int.from_bytes(params_buf[4:5], "little", signed=False)

                # value is list of c_uint8
                assert (length) == len(params_buf[5:-1]), f"Expected {length}, received: {len(params_buf[5:-1])}"  # Check for mismatch in value length and remaining bytes, -1 to account for padding

                parameters.value = (c_uint8 * length).from_buffer_copy(params_buf[5:-1])
                return GattmAttGetValueRsp(parameters=parameters)

            else:
                raise AssertionError(f"GattmMessageFactory: Message type is unhandled or not valid. message={msg_bytes.hex()}")
        except AssertionError as e:
            print(e)
            raise e
