from .gtl_message_base import GtlMessageBase
from gtl_port.gattm_task import GATTM_MSG_ID, gattm_add_svc_req, gattm_add_svc_rsp, gattm_att_set_value_req, gattm_att_set_value_rsp, \
    gattm_att_get_value_req, gattm_att_get_value_rsp

from gtl_port.rwip_config import KE_API_ID


class GattmAddSvcReq(GtlMessageBase):

    def __init__(self, parameters: gattm_add_svc_req = None):

        self.parameters = parameters if parameters else gattm_add_svc_req()

        super().__init__(msg_id=GATTM_MSG_ID.GATTM_ADD_SVC_REQ,
                         dst_id=KE_API_ID.TASK_ID_GATTM,
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=self.par_len,
                         parameters=self.parameters)

    def get_par_len(self):
        self._par_len = 24 * (self.parameters.svc_desc.nb_att + 1)
        return self._par_len

    def set_par_len(self, value):
        self._par_len = value

    par_len = property(get_par_len, set_par_len)


class GattmAddSvcRsp(GtlMessageBase):

    def __init__(self, parameters: gattm_add_svc_rsp = None):

        self.parameters = parameters if parameters else gattm_add_svc_rsp()

        super().__init__(msg_id=GATTM_MSG_ID.GATTM_ADD_SVC_RSP,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=KE_API_ID.TASK_ID_GATTM,
                         par_len=4,
                         parameters=self.parameters)

# TODO GATTM_SVC_GET_PERMISSION_REQ, GATTM_SVC_GET_PERMISSION_RSP


class GattmAttSetValueReq(GtlMessageBase):

    def __init__(self, parameters: gattm_att_set_value_req = None):

        self.parameters = parameters if parameters else gattm_att_set_value_req()

        super().__init__(msg_id=GATTM_MSG_ID.GATTM_ATT_SET_VALUE_REQ,
                         dst_id=KE_API_ID.TASK_ID_GATTM,
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=self.par_len,
                         parameters=self.parameters)

    def get_par_len(self):
        self._par_len = 4 + self.parameters.length
        return self._par_len

    def set_par_len(self, value):
        self._par_len = value

    par_len = property(get_par_len, set_par_len)


class GattmAttSetValueRsp(GtlMessageBase):

    def __init__(self, parameters: gattm_att_set_value_rsp = None):

        self.parameters = parameters if parameters else gattm_att_set_value_rsp()

        super().__init__(msg_id=GATTM_MSG_ID.GATTM_ATT_SET_VALUE_RSP,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=KE_API_ID.TASK_ID_GATTM,
                         par_len=4,
                         parameters=self.parameters)


class GattmAttGetValueReq(GtlMessageBase):

    def __init__(self, parameters: gattm_att_get_value_req = None):

        self.parameters = parameters if parameters else gattm_att_get_value_req()

        super().__init__(msg_id=GATTM_MSG_ID.GATTM_ATT_GET_VALUE_REQ,
                         dst_id=KE_API_ID.TASK_ID_GATTM,
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=2,
                         parameters=self.parameters)


class GattmAttGetValueRsp(GtlMessageBase):

    def __init__(self, parameters: gattm_att_get_value_rsp = None):

        self.parameters = parameters if parameters else gattm_att_get_value_rsp()

        super().__init__(msg_id=GATTM_MSG_ID.GATTM_ATT_GET_VALUE_RSP,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=KE_API_ID.TASK_ID_GATTM,
                         par_len=self.par_len,
                         parameters=self.parameters)

    def get_par_len(self):
        self._par_len = 6 + self.parameters.length
        return self._par_len

    def set_par_len(self, value):
        self._par_len = value

    par_len = property(get_par_len, set_par_len)

# GATTM_ATT_GET_VALUE_RSP
