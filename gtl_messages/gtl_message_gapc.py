from ctypes import *
from .gtl_message_base import *

class GapcConnectionReqInd(AbstractGtlMessage):
     def __init__(self, parameters: gapc_connection_req_ind = gapc_connection_req_ind()):

        super().__init__(msg_id=GAPC_MSG_ID.GAPC_CONNECTION_REQ_IND,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=KE_API_ID.TASK_ID_GAPC,
                         par_len=16,
                         parameters=None)

        self.parameters = parameters



