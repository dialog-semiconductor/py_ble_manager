from ctypes import *
from .gtl_message_base import *

# TODO next message GATTC_EXC_MTU_CMD, GATTC_CMP_EVT, GATTC_MTU_CHANGED_IND, GATTC_ATT_INFO_REQ_IND, GATTC_ATT_INFO_CFM

'''
class GapcConnectionReqInd(GtlMessageBase):
     def __init__(self, conidx: c_uint8 = 0, parameters: gapc_connection_req_ind = None):

        params = parameters if parameters else gapc_connection_req_ind()

        super().__init__(msg_id=GAPC_MSG_ID.GAPC_CONNECTION_REQ_IND,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=((conidx << 8) | KE_API_ID.TASK_ID_GAPC),
                         par_len=16,
                         parameters=params)

        self.parameters = params 
'''

class GattcWriteReqInd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gattc_write_req_ind = None):

        params = parameters if parameters else gattc_write_req_ind()
        p_len = 6 + params.length

        super().__init__(msg_id=GATTC_MSG_ID.GATTC_WRITE_REQ_IND,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=((conidx << 8) | KE_API_ID.TASK_ID_GATTC),
                         par_len=p_len,
                         parameters=params)

        self.parameters = params 
        self.par_len = p_len

    def get_par_len(self):
        self._par_len = 6 + self.parameters.length
        return self._par_len

    def set_par_len(self, value):
        self._par_len = value

    par_len = property(get_par_len, set_par_len)

class GattcWriteCfm(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gattc_write_cfm = None):

        params = parameters if parameters else gattc_write_cfm()

        super().__init__(msg_id=GATTC_MSG_ID.GATTC_WRITE_CFM,
                         dst_id=((conidx << 8) | KE_API_ID.TASK_ID_GATTC), 
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=4,
                         parameters=params)

        self.parameters = params 
 
class GattcReadReqInd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gattc_read_req_ind = None):

        params = parameters if parameters else gattc_read_req_ind()

        super().__init__(msg_id=GATTC_MSG_ID.GATTC_READ_REQ_IND,
                         dst_id=KE_API_ID.TASK_ID_GTL, 
                         src_id=((conidx << 8) | KE_API_ID.TASK_ID_GATTC),
                         par_len=2,
                         parameters=params)

        self.parameters = params 

class GattcReadCfm(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gattc_read_cfm = None):

        params = parameters if parameters else gattc_read_cfm()
        p_len = 6 + params.length

        super().__init__(msg_id=GATTC_MSG_ID.GATTC_READ_CFM,
                         dst_id=((conidx << 8) | KE_API_ID.TASK_ID_GATTC),
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=p_len,
                         parameters=params)

        self.parameters = params 
        self.par_len = p_len

    def get_par_len(self):
        self._par_len = 6 + self.parameters.length
        return self._par_len

    def set_par_len(self, value):
        self._par_len = value

    par_len = property(get_par_len, set_par_len)

class GattcSendEvtCmd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gattc_send_evt_cmd = None):

        params = parameters if parameters else gattc_send_evt_cmd()
        p_len = 8 + params.length

        super().__init__(msg_id=GATTC_MSG_ID.GATTC_SEND_EVT_CMD,
                         dst_id=((conidx << 8) | KE_API_ID.TASK_ID_GATTC),
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=p_len,
                         parameters=params)

        self.parameters = params 
        self.par_len = p_len

    def get_par_len(self):
        self._par_len = 8 + self.parameters.length
        return self._par_len

    def set_par_len(self, value):
        self._par_len = value

    par_len = property(get_par_len, set_par_len)

class GattcCmpEvt(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gattc_cmp_evt = None):

        params = parameters if parameters else gattc_cmp_evt()

        super().__init__(msg_id=GATTC_MSG_ID.GATTC_CMP_EVT,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id= ((conidx << 8) | KE_API_ID.TASK_ID_GATTC),
                         par_len=4,
                         parameters=params)

        self.parameters = params 

class GattcEventInd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gattc_event_ind = None):

        params = parameters if parameters else gattc_event_ind()
        p_len = 6 + params.length

        super().__init__(msg_id=GATTC_MSG_ID.GATTC_EVENT_IND,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=((conidx << 8) | KE_API_ID.TASK_ID_GATTC),
                         par_len=p_len,
                         parameters=params)

        self.parameters = params 
        self.par_len = p_len

    def get_par_len(self):
        self._par_len = 6 + self.parameters.length
        return self._par_len

    def set_par_len(self, value):
        self._par_len = value

    par_len = property(get_par_len, set_par_len)

class GattcEventReqInd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gattc_event_req_ind = None):

        params = parameters if parameters else gattc_event_req_ind()
        p_len = 6 + params.length

        super().__init__(msg_id=GATTC_MSG_ID.GATTC_EVENT_REQ_IND,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=((conidx << 8) | KE_API_ID.TASK_ID_GATTC),
                         par_len=p_len,
                         parameters=params)

        self.parameters = params 
        self.par_len = p_len

    def get_par_len(self):
        self._par_len = 6 + self.parameters.length
        return self._par_len

    def set_par_len(self, value):
        self._par_len = value

    par_len = property(get_par_len, set_par_len)

class GattcEventCfm(GtlMessageBase):

    # TODO conidx not documented for this message but every other GATTC message has one.
    def __init__(self, conidx: c_uint8 = 0, parameters: gattc_event_cfm = None):

        params = parameters if parameters else gattc_event_cfm()

        super().__init__(msg_id=GATTC_MSG_ID.GATTC_EVENT_CFM,
                         dst_id=((conidx << 8) | KE_API_ID.TASK_ID_GATTC),
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=2,
                         parameters=params)

        self.parameters = params 

class GattcDiscCmd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gattc_disc_cmd = None):

        params = parameters if parameters else gattc_disc_cmd()
        p_len = 8 + params.uuid_len

        super().__init__(msg_id=GATTC_MSG_ID.GATTC_DISC_CMD,
                         dst_id=((conidx << 8) | KE_API_ID.TASK_ID_GATTC),
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=p_len,
                         parameters=params)

        self.parameters = params 
        self.par_len = p_len

    def get_par_len(self):
        self._par_len = 8 + self.parameters.uuid_len
        return self._par_len

    def set_par_len(self, value):
        self._par_len = value

    par_len = property(get_par_len, set_par_len)

class GattcDiscCharDescInd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gattc_disc_char_desc_ind = None):

        params = parameters if parameters else gattc_disc_char_desc_ind()
        p_len = 4 + params.uuid_len

        super().__init__(msg_id=GATTC_MSG_ID.GATTC_DISC_CHAR_DESC_IND,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=((conidx << 8) | KE_API_ID.TASK_ID_GATTC),
                         par_len=p_len,
                         parameters=params)

        self.parameters = params 
        self.par_len = p_len

    def get_par_len(self):
        self._par_len = 4 + self.parameters.uuid_len
        return self._par_len

    def set_par_len(self, value):
        self._par_len = value

    par_len = property(get_par_len, set_par_len)

class GattcDiscSvcInd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gattc_disc_svc_ind = None):

        params = parameters if parameters else gattc_disc_svc_ind()
        p_len = 6 + params.uuid_len

        super().__init__(msg_id=GATTC_MSG_ID.GATTC_DISC_SVC_IND,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=((conidx << 8) | KE_API_ID.TASK_ID_GATTC),
                         par_len=p_len,
                         parameters=params)

        self.parameters = params 
        self.par_len = p_len

    def get_par_len(self):
        self._par_len = 6 + self.parameters.uuid_len
        return self._par_len

    def set_par_len(self, value):
        self._par_len = value

    par_len = property(get_par_len, set_par_len)

class GattcDiscSvcInclInd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gattc_disc_svc_incl_ind = None):

        params = parameters if parameters else gattc_disc_svc_incl_ind()
        p_len = 8 + params.uuid_len

        super().__init__(msg_id=GATTC_MSG_ID.GATTC_DISC_SVC_INCL_IND,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=((conidx << 8) | KE_API_ID.TASK_ID_GATTC),
                         par_len=p_len,
                         parameters=params)

        self.parameters = params 
        self.par_len = p_len

    def get_par_len(self):
        self._par_len = 8 + self.parameters.uuid_len
        return self._par_len

    def set_par_len(self, value):
        self._par_len = value

    par_len = property(get_par_len, set_par_len)

class GattcDiscCharInd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gattc_disc_char_ind = None):

        params = parameters if parameters else gattc_disc_char_ind()
        p_len = 6 + params.uuid_len

        super().__init__(msg_id=GATTC_MSG_ID.GATTC_DISC_CHAR_IND,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=((conidx << 8) | KE_API_ID.TASK_ID_GATTC), #TODO does not include conidx in manual, but all other GATTC do
                         par_len=p_len,
                         parameters=params)

        self.parameters = params 
        self.par_len = p_len

    def get_par_len(self):
        self._par_len = 6 + self.parameters.uuid_len
        return self._par_len

    def set_par_len(self, value):
        self._par_len = value

    par_len = property(get_par_len, set_par_len)
 
class GattcSdpSvcDiscCmd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gattc_sdp_svc_disc_cmd = None):

        params = parameters if parameters else gattc_sdp_svc_disc_cmd()

        super().__init__(msg_id=GATTC_MSG_ID.GATTC_SDP_SVC_DISC_CMD,
                         dst_id=((conidx << 8) | KE_API_ID.TASK_ID_GATTC), 
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=24, #TODO manual say 26in example, but seems 24 is max. Example string in manual too long
                         parameters=params)

        self.parameters = params 
'''
#TODO
class GattcSdpSvcInd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gattc_sdp_svc_ind = None):

        params = parameters if parameters else gattc_sdp_svc_ind()

        super().__init__(msg_id=GATTC_MSG_ID.GATTC_SDP_SVC_IND,
                         dst_id=((conidx << 8) | KE_API_ID.TASK_ID_GATTC), 
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=22, 
                         parameters=params)

        self.parameters = params 
'''

#TODO GATTC_READ_CMD
