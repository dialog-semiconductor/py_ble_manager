from ctypes import *
from .gtl_message_base import *

class GapcConnectionReqInd(GtlMessageBase):
     def __init__(self, parameters: gapc_connection_req_ind = None):

        parms = parameters if parameters else gapc_connection_req_ind()

        super().__init__(msg_id=GAPC_MSG_ID.GAPC_CONNECTION_REQ_IND,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=KE_API_ID.TASK_ID_GAPC,
                         par_len=16,
                         parameters=parms)

        self.parameters = parms
        
class GapcConnectionCfm(GtlMessageBase):
    def __init__(self, conidx: c_uint8 = 0, parameters: gapc_connection_cfm = None):

        parms = parameters if parameters else gapc_connection_cfm()

        super().__init__(msg_id=GAPC_MSG_ID.GAPC_CONNECTION_CFM,
                         dst_id=KE_API_ID.TASK_ID_GAPC,
                         src_id=(conidx << 8) | (KE_API_ID.TASK_ID_GTL),
                         par_len=44,
                         parameters=parms)

        self.parameters = parms

class GapcSecurityCmd(GtlMessageBase):
    def __init__(self, conidx: c_uint8 = 0, parameters: gapc_security_cmd = None):

        parms = parameters if parameters else gapc_connection_cfm()

        super().__init__(msg_id=GAPC_MSG_ID.GAPC_SECURITY_CMD,
                         dst_id=KE_API_ID.TASK_ID_GAPC,
                         src_id=(conidx << 8) | (KE_API_ID.TASK_ID_GTL),
                         par_len=2,
                         parameters=parms)

        self.parameters = parms
