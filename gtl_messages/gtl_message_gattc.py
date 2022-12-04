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
 
 