from ctypes import *
from .gtl_message_base import *

# TODO next message GATTC_EXC_MTU_CMD, GATTC_CMP_EVT, GATTC_MTU_CHANGED_IND, GATTC_ATT_INFO_REQ_IND, GATTC_ATT_INFO_CFM

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
                         src_id= ((conidx << 8) | KE_API_ID.TASK_ID_GATTC),
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
                         src_id=((conidx << 8) | KE_API_ID.TASK_ID_GATTC), #TODO does not include conidx in manual, but all other GATTC do
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
                         par_len=24, #TODO manual say 26in example, but seems 24 is max. Example string in manual too long
                         parameters=self.parameters)
  
'''
#TODO
class GattcSdpSvcInd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gattc_sdp_svc_ind = None):

        self.parameters = parameters if parameters else gattc_sdp_svc_ind()

        super().__init__(msg_id=GATTC_MSG_ID.GATTC_SDP_SVC_IND,
                         dst_id=((conidx << 8) | KE_API_ID.TASK_ID_GATTC), 
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=22, 
                         parameters=self.parameters)

         
'''
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
        else: # self.parameters.operation == GATTC_OPERATION.GATTC_READ_MULTIPLE
            self._par_len = 4 + 4 * self.parameters.nb # TODO nb not updated properly as set_req not called when updated multiple
        return self._par_len

    def set_par_len(self, value):
        self._par_len = value

    par_len = property(get_par_len, set_par_len) 

    def to_bytes(self): #TODO Cannot find way to handle gattc_read_cmd elegantly. Should to str method be created for union as well?
        message = bytearray()
        message.append(GTL_INITIATOR)
        message.extend(self.msg_id.value.to_bytes(length=2, byteorder='little'))
        message.extend(self.dst_id.to_bytes(length=2, byteorder='little'))
        message.extend(self.src_id.to_bytes(length=2, byteorder='little'))
        message.extend(self.par_len.to_bytes(length=2, byteorder='little'))
        message.extend(self.parameters.operation.to_bytes(length=1, byteorder='little'))
        message.extend(self.parameters.nb.to_bytes(length=1, byteorder='little'))
        message.extend(self.parameters.seq_num.to_bytes(length=2, byteorder='little'))


        if self.parameters.operation == GATTC_OPERATION.GATTC_READ or self.parameters.operation == GATTC_OPERATION.GATTC_READ_LONG:
            simple = bytearray(self.parameters.req.simple)
            message.extend(simple)
        elif self.parameters.operation == GATTC_OPERATION.GATTC_READ_BY_UUID:
            message.extend(self.parameters.req.by_uuid.start_hdl.to_bytes(length=2, byteorder='little'))
            message.extend(self.parameters.req.by_uuid.end_hdl.to_bytes(length=2, byteorder='little'))
            message.extend(self.parameters.req.by_uuid.uuid_len.to_bytes(length=2, byteorder='little'))
            message.extend(bytearray(self.parameters.req.by_uuid.uuid))
        else:
            #pointer_to_array = self.parameters.req.multiple
            #underlying_array = cast(pointer_to_array, POINTER(gattc_read_multiple * self.parameters.nb)).contents
            array = self.parameters.req.multiple
            for item in array:
                message.extend(bytearray(item))
        
        return message
'''
class GattcReadInd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gattc_read_ind = None):

        self.parameters = parameters if parameters else gattc_read_ind()

        super().__init__(msg_id=GATTC_MSG_ID.GATTC_READ_IND,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=((conidx << 8) | KE_API_ID.TASK_ID_GATTC), 
                         par_len=11,
                         parameters=self.parameters)
'''
  
#TODO setup Git Action for unit tests
