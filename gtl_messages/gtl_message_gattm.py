from ctypes import *
from .gtl_message_base import *

class GattmAddSvcReq(GtlMessageBase):
    def __init__(self, parameters: gattm_add_svc_req = None):

        params = parameters if parameters else gattm_add_svc_req()
        p_len = 24*(params.svc_desc.nb_att+1)

        super().__init__(msg_id=GATTM_MSG_ID.GATTM_ADD_SVC_REQ,
                         dst_id=KE_API_ID.TASK_ID_GATTM,
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=p_len, # TODO if user updates parameters.nb_att after construction, par_len automatically updated
                         parameters=params)

        self.parameters = params 
        self.par_len = p_len

    def get_par_len(self):
        self._par_len = 24*(self.parameters.svc_desc.nb_att+1)
        print(f"GattmAddSvcReq._par_len = {self._par_len}")
        return self._par_len

    def set_par_len(self, value):
        self._par_len = value

    par_len = property(get_par_len, set_par_len)
