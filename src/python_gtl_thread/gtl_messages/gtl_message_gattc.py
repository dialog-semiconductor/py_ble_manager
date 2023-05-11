from ctypes import c_uint8
from .gtl_message_base import GtlMessageBase
from ..gtl_port.gattc_task import GATTC_MSG_ID, gattc_write_req_ind, gattc_write_cfm, gattc_read_req_ind, gattc_read_cfm, gattc_send_evt_cmd, \
    gattc_cmp_evt, gattc_event_ind, gattc_event_req_ind, gattc_event_cfm, gattc_disc_cmd, gattc_disc_char_desc_ind, gattc_disc_svc_ind, \
    gattc_disc_svc_incl_ind, gattc_disc_char_ind, gattc_sdp_svc_disc_cmd, gattc_read_cmd, GATTC_OPERATION, gattc_read_ind, gattc_write_cmd, \
    gattc_exc_mtu_cmd, gattc_mtu_changed_ind, gattc_att_info_req_ind, gattc_att_info_cfm, gattc_sdp_svc_ind, gattc_sdp_att_info, \
    GATTC_SDP_ATT_TYPE, gattc_execute_write_cmd
from ..gtl_port.rwip_config import KE_API_ID


class GattcExcMtuCmd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gattc_exc_mtu_cmd = None):

        self.parameters = parameters if parameters else gattc_exc_mtu_cmd()

        super().__init__(msg_id=GATTC_MSG_ID.GATTC_EXC_MTU_CMD,
                         dst_id=((conidx << 8) | KE_API_ID.TASK_ID_GATTC),
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=4,
                         parameters=self.parameters)


class GattcMtuChangedInd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gattc_mtu_changed_ind = None):

        self.parameters = parameters if parameters else gattc_mtu_changed_ind()

        super().__init__(msg_id=GATTC_MSG_ID.GATTC_MTU_CHANGED_IND,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=((conidx << 8) | KE_API_ID.TASK_ID_GATTC),
                         par_len=4,
                         parameters=self.parameters)


class GattcWriteReqInd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gattc_write_req_ind = None):

        self.parameters = parameters if parameters else gattc_write_req_ind()

        super().__init__(msg_id=GATTC_MSG_ID.GATTC_WRITE_REQ_IND,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=((conidx << 8) | KE_API_ID.TASK_ID_GATTC),
                         par_len=self.par_len,
                         parameters=self.parameters)

    def get_par_len(self):
        self._par_len = 6 + self.parameters.length
        return self._par_len

    def set_par_len(self, value):
        self._par_len = value

    par_len = property(get_par_len, set_par_len)


class GattcWriteCfm(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gattc_write_cfm = None):

        self.parameters = parameters if parameters else gattc_write_cfm()

        super().__init__(msg_id=GATTC_MSG_ID.GATTC_WRITE_CFM,
                         dst_id=((conidx << 8) | KE_API_ID.TASK_ID_GATTC),
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=4,
                         parameters=self.parameters)


class GattcAttInfoReqInd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gattc_att_info_req_ind = None):

        self.parameters = parameters if parameters else gattc_att_info_req_ind()

        super().__init__(msg_id=GATTC_MSG_ID.GATTC_ATT_INFO_REQ_IND,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=((conidx << 8) | KE_API_ID.TASK_ID_GATTC),
                         par_len=2,
                         parameters=self.parameters)


class GattcAttInfoCfm(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gattc_att_info_cfm = None):

        self.parameters = parameters if parameters else gattc_att_info_cfm()

        super().__init__(msg_id=GATTC_MSG_ID.GATTC_WRITE_CFM,
                         dst_id=((conidx << 8) | KE_API_ID.TASK_ID_GATTC),
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=6,
                         parameters=self.parameters)


class GattcReadReqInd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gattc_read_req_ind = None):

        self.parameters = parameters if parameters else gattc_read_req_ind()

        super().__init__(msg_id=GATTC_MSG_ID.GATTC_READ_REQ_IND,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=((conidx << 8) | KE_API_ID.TASK_ID_GATTC),
                         par_len=2,
                         parameters=self.parameters)


class GattcReadCfm(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gattc_read_cfm = None):

        self.parameters = parameters if parameters else gattc_read_cfm()

        super().__init__(msg_id=GATTC_MSG_ID.GATTC_READ_CFM,
                         dst_id=((conidx << 8) | KE_API_ID.TASK_ID_GATTC),
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=self.par_len,
                         parameters=self.parameters)

    def get_par_len(self):
        self._par_len = 6 + self.parameters.length
        return self._par_len

    def set_par_len(self, value):
        self._par_len = value

    par_len = property(get_par_len, set_par_len)


class GattcSendEvtCmd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gattc_send_evt_cmd = None):

        self.parameters = parameters if parameters else gattc_send_evt_cmd()

        super().__init__(msg_id=GATTC_MSG_ID.GATTC_SEND_EVT_CMD,
                         dst_id=((conidx << 8) | KE_API_ID.TASK_ID_GATTC),
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=self.par_len,
                         parameters=self.parameters)

    def get_par_len(self):
        self._par_len = 8 + self.parameters.length
        return self._par_len

    def set_par_len(self, value):
        self._par_len = value

    par_len = property(get_par_len, set_par_len)


class GattcCmpEvt(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gattc_cmp_evt = None):

        self.parameters = parameters if parameters else gattc_cmp_evt()

        super().__init__(msg_id=GATTC_MSG_ID.GATTC_CMP_EVT,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=((conidx << 8) | KE_API_ID.TASK_ID_GATTC),
                         par_len=4,
                         parameters=self.parameters)


class GattcEventInd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gattc_event_ind = None):

        self.parameters = parameters if parameters else gattc_event_ind()

        super().__init__(msg_id=GATTC_MSG_ID.GATTC_EVENT_IND,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=((conidx << 8) | KE_API_ID.TASK_ID_GATTC),
                         par_len=self.par_len,
                         parameters=self.parameters)

    def get_par_len(self):
        self._par_len = 6 + self.parameters.length
        return self._par_len

    def set_par_len(self, value):
        self._par_len = value

    par_len = property(get_par_len, set_par_len)


class GattcEventReqInd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gattc_event_req_ind = None):

        self.parameters = parameters if parameters else gattc_event_req_ind()

        super().__init__(msg_id=GATTC_MSG_ID.GATTC_EVENT_REQ_IND,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=((conidx << 8) | KE_API_ID.TASK_ID_GATTC),
                         par_len=self.par_len,
                         parameters=self.parameters)

    def get_par_len(self):
        self._par_len = 6 + self.parameters.length
        return self._par_len

    def set_par_len(self, value):
        self._par_len = value

    par_len = property(get_par_len, set_par_len)


class GattcEventCfm(GtlMessageBase):

    # TODO conidx not documented for this message but every other GATTC message has one.
    def __init__(self, conidx: c_uint8 = 0, parameters: gattc_event_cfm = None):

        self.parameters = parameters if parameters else gattc_event_cfm()

        super().__init__(msg_id=GATTC_MSG_ID.GATTC_EVENT_CFM,
                         dst_id=((conidx << 8) | KE_API_ID.TASK_ID_GATTC),
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=2,
                         parameters=self.parameters)


class GattcDiscCmd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gattc_disc_cmd = None):

        self.parameters = parameters if parameters else gattc_disc_cmd()

        super().__init__(msg_id=GATTC_MSG_ID.GATTC_DISC_CMD,
                         dst_id=((conidx << 8) | KE_API_ID.TASK_ID_GATTC),
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=self.par_len,
                         parameters=self.parameters)

    def get_par_len(self):
        self._par_len = 8 + self.parameters.uuid_len
        return self._par_len

    def set_par_len(self, value):
        self._par_len = value

    par_len = property(get_par_len, set_par_len)


class GattcDiscCharDescInd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gattc_disc_char_desc_ind = None):

        self.parameters = parameters if parameters else gattc_disc_char_desc_ind()

        super().__init__(msg_id=GATTC_MSG_ID.GATTC_DISC_CHAR_DESC_IND,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=((conidx << 8) | KE_API_ID.TASK_ID_GATTC),
                         par_len=self.par_len,
                         parameters=self.parameters)

    def get_par_len(self):
        self._par_len = 4 + self.parameters.uuid_len
        return self._par_len

    def set_par_len(self, value):
        self._par_len = value

    par_len = property(get_par_len, set_par_len)


class GattcDiscSvcInd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gattc_disc_svc_ind = None):

        self.parameters = parameters if parameters else gattc_disc_svc_ind()

        super().__init__(msg_id=GATTC_MSG_ID.GATTC_DISC_SVC_IND,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=((conidx << 8) | KE_API_ID.TASK_ID_GATTC),
                         par_len=self.par_len,
                         parameters=self.parameters)

    def get_par_len(self):
        self._par_len = 6 + self.parameters.uuid_len
        return self._par_len

    def set_par_len(self, value):
        self._par_len = value

    par_len = property(get_par_len, set_par_len)


class GattcDiscSvcInclInd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gattc_disc_svc_incl_ind = None):

        self.parameters = parameters if parameters else gattc_disc_svc_incl_ind()

        super().__init__(msg_id=GATTC_MSG_ID.GATTC_DISC_SVC_INCL_IND,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=((conidx << 8) | KE_API_ID.TASK_ID_GATTC),
                         par_len=self.par_len,
                         parameters=self.parameters)

    def get_par_len(self):
        self._par_len = 8 + self.parameters.uuid_len
        return self._par_len

    def set_par_len(self, value):
        self._par_len = value

    par_len = property(get_par_len, set_par_len)


class GattcDiscCharInd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gattc_disc_char_ind = None):

        self.parameters = parameters if parameters else gattc_disc_char_ind()

        super().__init__(msg_id=GATTC_MSG_ID.GATTC_DISC_CHAR_IND,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=((conidx << 8) | KE_API_ID.TASK_ID_GATTC),  # TODO does not include conidx in manual, but all other GATTC do
                         par_len=self.par_len,
                         parameters=self.parameters)

    def get_par_len(self):
        self._par_len = 6 + self.parameters.uuid_len
        return self._par_len

    def set_par_len(self, value):
        self._par_len = value

    par_len = property(get_par_len, set_par_len)


class GattcSdpSvcDiscCmd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gattc_sdp_svc_disc_cmd = None):

        self.parameters = parameters if parameters else gattc_sdp_svc_disc_cmd()

        super().__init__(msg_id=GATTC_MSG_ID.GATTC_SDP_SVC_DISC_CMD,
                         dst_id=((conidx << 8) | KE_API_ID.TASK_ID_GATTC),
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=24,  # TODO manual say 26in example, but seems 24 is max. Example string in manual too long
                         parameters=self.parameters)


class GattcSdpSvcInd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gattc_sdp_svc_ind = None):

        self.parameters = parameters if parameters else gattc_sdp_svc_ind()

        super().__init__(msg_id=GATTC_MSG_ID.GATTC_SDP_SVC_IND,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=((conidx << 8) | KE_API_ID.TASK_ID_GATTC),
                         par_len=self.par_len,
                         parameters=self.parameters)

    def get_par_len(self):
        info_length = (self.parameters.end_hdl - self.parameters.start_hdl)
        self._par_len = (info_length + 1) * 22
        return self._par_len

    def set_par_len(self, value):
        self._par_len = value

    par_len = property(get_par_len, set_par_len)

    # TODO this method not working properly
    def _struct_to_str(self, struct: gattc_sdp_svc_ind):

        param_string = ''
        param_string += f'({self._array_to_str("uuid", struct.uuid)[:-2]}, '
        param_string += f'start_hdl={struct.start_hdl}, '
        param_string += f'end_hdl={struct.end_hdl}, '

        param_string += 'info=('
        item: gattc_sdp_att_info
        for item in struct.info:
            param_string += f'gattc_sdp_att_info=(att_type={str(GATTC_SDP_ATT_TYPE(item.att_type))}, '
            match item.att_type:
                case GATTC_SDP_ATT_TYPE.GATTC_SDP_ATT_CHAR:
                    param_string += 'att_char=gattc_sdp_att_char=('
                    param_string += f'prop={item.att_char.prop}, '
                    param_string += f'handle={item.att_char.handle}'
                    param_string += ')'
                case GATTC_SDP_ATT_TYPE.GATTC_SDP_INC_SVC:
                    param_string += 'inc_svc=gattc_sdp_include_svc=('
                    param_string += f'{self._array_to_str("uuid", item.inc_svc.uuid)[:-2]}, '
                    param_string += f'prop={item.inc_svc.start_hdl}, '
                    param_string += f'handle={item.inc_svc.end_hdl}'
                    param_string += ')'
                case (GATTC_SDP_ATT_TYPE.GATTC_SDP_ATT_VAL
                      | GATTC_SDP_ATT_TYPE.GATTC_SDP_ATT_DESC):

                    param_string += 'att=gattc_sdp_att=('
                    param_string += f'uuid_len={item.att.uuid_len}, '
                    param_string += f'{self._array_to_str("uuid", item.att.uuid)[:-2]}'
                    param_string += ')'
            param_string += '), '
        param_string = param_string[:-2]
        param_string += ')'
        param_string += '), '
        return param_string

    # TODO Cannot find way to handle gattc_sdp_svc_ind elegantly. Should to str method be created for union as well?
    def _struct_to_bytearray(self, parameters: gattc_sdp_svc_ind):
        message = bytearray()
        message.extend(parameters.uuid_len.to_bytes(length=1, byteorder='little'))
        message.extend(bytearray(parameters.uuid))
        message.extend(bytearray(c_uint8(0)))  # padding
        message.extend(parameters.start_hdl.to_bytes(length=2, byteorder='little'))
        message.extend(parameters.end_hdl.to_bytes(length=2, byteorder='little'))

        info: gattc_sdp_att_info
        for info in parameters.info:
            if info.att_type == GATTC_SDP_ATT_TYPE.GATTC_SDP_ATT_CHAR:
                message.extend(bytearray(info.att_char))
            elif info.att_type == GATTC_SDP_ATT_TYPE.GATTC_SDP_INC_SVC:
                message.extend(bytearray(info.inc_svc))
            elif info.att_type == GATTC_SDP_ATT_TYPE.GATTC_SDP_ATT_VAL or info.att_type == GATTC_SDP_ATT_TYPE.GATTC_SDP_ATT_DESC:
                message.extend(bytearray(info.att))

        return message


class GattcReadCmd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gattc_read_cmd = None):

        self.parameters = parameters if parameters else gattc_read_cmd()

        super().__init__(msg_id=GATTC_MSG_ID.GATTC_READ_CMD,
                         dst_id=((conidx << 8) | KE_API_ID.TASK_ID_GATTC),
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=self.par_len,
                         parameters=self.parameters)

    def get_par_len(self):
        if self.parameters.operation == GATTC_OPERATION.GATTC_READ or self.parameters.operation == GATTC_OPERATION.GATTC_READ_LONG:
            self._par_len = 4 + 6
        elif self.parameters.operation == GATTC_OPERATION.GATTC_READ_BY_UUID:
            self._par_len = 4 + 6 + self.parameters.req.by_uuid.uuid_len
        else:  # self.parameters.operation == GATTC_OPERATION.GATTC_READ_MULTIPLE
            self._par_len = 4 + 4 * self.parameters.nb  # TODO nb not updated properly as set_req not called when updated multiple
        return self._par_len

    def set_par_len(self, value):
        self._par_len = value

    par_len = property(get_par_len, set_par_len)

    def _struct_to_str(self, struct: gattc_read_cmd):
        param_string = ''
        param_string += f'(req={str(GATTC_OPERATION(struct.operation))}, '
        param_string += f'seq_num={struct.seq_num}, '
        param_string += 'req=gattc_read_req('

        match struct.operation:
            case (GATTC_OPERATION.GATTC_READ
                    | GATTC_OPERATION.GATTC_READ_LONG):

                param_string += 'simple=gattc_read_simple('
                param_string += f'handle={struct.req.simple.handle}, '
                param_string += f'offset={struct.req.simple.offset}, '
                param_string += f'length={struct.req.simple.length})'

            case GATTC_OPERATION.GATTC_READ_BY_UUID:
                param_string += 'by_uuid=gattc_read_by_uuid('
                param_string += f'start_hdl={struct.req.by_uuid.start_hdl}, '
                param_string += f'end_hdl={struct.req.by_uuid.end_hdl}, '
                param_string += f'{self._array_to_str("uuid", struct.req.by_uuid.uuid)[:-2]})'

            case GATTC_OPERATION.GATTC_READ_MULTIPLE:
                param_string += 'multiple=('
                multiple_array = struct.req.multiple
                for item in multiple_array:
                    param_string += 'gattc_read_multiple=('
                    param_string += f'handle={item.handle}'
                    param_string += f'len={item.len}'
                    param_string += ')'
                param_string += ')'

        param_string += ')'
        param_string += '), '  # ,space This will be removed by __repr__ in GtlMessageBase
        return param_string

    # TODO Cannot find way to handle gattc_read_cmd elegantly. Should to str method be created for union as well?
    def _struct_to_bytearray(self, parameters: gattc_read_cmd):
        message = bytearray()
        message.extend(parameters.operation.to_bytes(length=1, byteorder='little'))
        message.extend(parameters.nb.to_bytes(length=1, byteorder='little'))
        message.extend(parameters.seq_num.to_bytes(length=2, byteorder='little'))

        if parameters.operation == GATTC_OPERATION.GATTC_READ or parameters.operation == GATTC_OPERATION.GATTC_READ_LONG:
            simple = bytearray(parameters.req.simple)
            message.extend(simple)
        elif self.parameters.operation == GATTC_OPERATION.GATTC_READ_BY_UUID:
            message.extend(parameters.req.by_uuid.start_hdl.to_bytes(length=2, byteorder='little'))
            message.extend(parameters.req.by_uuid.end_hdl.to_bytes(length=2, byteorder='little'))
            message.extend(parameters.req.by_uuid.uuid_len.to_bytes(length=2, byteorder='little'))
            message.extend(bytearray(parameters.req.by_uuid.uuid))
        else:
            array = parameters.req.multiple
            for item in array:
                message.extend(bytearray(item))

        return message


class GattcReadInd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gattc_read_ind = None):

        self.parameters = parameters if parameters else gattc_read_ind()

        super().__init__(msg_id=GATTC_MSG_ID.GATTC_READ_IND,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=((conidx << 8) | KE_API_ID.TASK_ID_GATTC),
                         par_len=self.par_len,
                         parameters=self.parameters)

    def get_par_len(self):
        self._par_len = 6 + self.parameters.length
        return self._par_len

    def set_par_len(self, value):
        self._par_len = value

    par_len = property(get_par_len, set_par_len)


class GattcWriteCmd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gattc_write_cmd = None):

        self.parameters = parameters if parameters else gattc_write_cmd()

        super().__init__(msg_id=GATTC_MSG_ID.GATTC_WRITE_CMD,
                         dst_id=((conidx << 8) | KE_API_ID.TASK_ID_GATTC),
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=self.par_len,
                         parameters=self.parameters)

    def get_par_len(self):
        self._par_len = 12 + self.parameters.length + self.parameters.length % 2  # TODO padding added if value is odd length?
        return self._par_len

    def set_par_len(self, value):
        self._par_len = value

    par_len = property(get_par_len, set_par_len)

    def _struct_to_bytearray(self, parameters: gattc_write_cmd):
        message = super()._struct_to_bytearray(parameters)
        if parameters.length % 2:  # TODO seems there is a padding byte added for odd length values, need confirm
            message.extend(c_uint8(0))
        return message


class GattcWriteExecuteCmd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gattc_execute_write_cmd = None):

        self.parameters = parameters if parameters else gattc_execute_write_cmd()

        super().__init__(msg_id=GATTC_MSG_ID.GATTC_EXECUTE_WRITE_CMD,
                         dst_id=((conidx << 8) | KE_API_ID.TASK_ID_GATTC),
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=4,
                         parameters=self.parameters)
