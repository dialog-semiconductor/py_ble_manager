from ctypes import *
from .gtl_message_base import *

class GattmAddSvcReq(GtlMessageBase):
     def __init__(self, parameters: gattm_add_svc_req = None):

        params = parameters if parameters else gattm_add_svc_req()

        super().__init__(msg_id=GATTM_MSG_ID.GATTM_ADD_SVC_REQ,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=KE_API_ID.TASK_ID_GATTM,
                         par_len=24*(params.nb_att+1),
                         parameters=params)

        self.parameters = params 