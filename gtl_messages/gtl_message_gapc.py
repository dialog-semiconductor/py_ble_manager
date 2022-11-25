from ctypes import *
from .gtl_message_base import *

class GapcConnectionReqInd(GtlMessageBase):
     def __init__(self, conidx: c_uint8 = 0, parameters: gapc_connection_req_ind = None):

        params = parameters if parameters else gapc_connection_req_ind()

        super().__init__(msg_id=GAPC_MSG_ID.GAPC_CONNECTION_REQ_IND,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=((conidx << 8) | KE_API_ID.TASK_ID_GAPC),
                         par_len=16,
                         parameters=params)

        self.parameters = params
        
class GapcConnectionCfm(GtlMessageBase):
    def __init__(self, conidx: c_uint8 = 0, parameters: gapc_connection_cfm = None):

        params = parameters if parameters else gapc_connection_cfm()

        super().__init__(msg_id=GAPC_MSG_ID.GAPC_CONNECTION_CFM,
                         dst_id=((conidx << 8) | KE_API_ID.TASK_ID_GAPC),
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=44,
                         parameters=params)

        self.parameters = params

class GapcSecurityCmd(GtlMessageBase):
    def __init__(self, conidx: c_uint8 = 0, parameters: gapc_security_cmd = None):

        params = parameters if parameters else gapc_security_cmd()

        super().__init__(msg_id=GAPC_MSG_ID.GAPC_SECURITY_CMD,
                         dst_id=((conidx << 8) | KE_API_ID.TASK_ID_GAPC),
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=2,
                         parameters=params)

        self.parameters = params

class GapcCmpEvt(GtlMessageBase):
    def __init__(self, conidx: c_uint8 = 0, parameters: gapc_cmp_evt = None):

        params = parameters if parameters else gapc_cmp_evt()

        super().__init__(msg_id=GAPC_MSG_ID.GAPC_CMP_EVT,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=((conidx << 8) | KE_API_ID.TASK_ID_GAPC),
                         par_len=2,
                         parameters=params)

        self.parameters = params

class GapcGetInfoCmd(GtlMessageBase):
    def __init__(self, conidx: c_uint8 = 0, parameters: gapc_get_info_cmd = None):

        params = parameters if parameters else gapc_get_info_cmd()

        super().__init__(msg_id=GAPC_MSG_ID.GAPC_GET_INFO_CMD,
                         dst_id=((conidx << 8) | KE_API_ID.TASK_ID_GAPC),
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=1,
                         parameters=params)

        self.parameters = params

class GapcPeerFeaturesInd(GtlMessageBase):
    def __init__(self, conidx: c_uint8 = 0, parameters: gapc_peer_features_ind = None):

        params = parameters if parameters else gapc_peer_features_ind()

        super().__init__(msg_id=GAPC_MSG_ID.GAPC_PEER_FEATURES_IND,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=((conidx << 8) | KE_API_ID.TASK_ID_GAPC),
                         par_len=8,
                         parameters=params)

        self.parameters = params

class GapcBondReqInd(GtlMessageBase):
    def __init__(self, conidx: c_uint8 = 0, parameters: gapc_bond_req_ind = None):

        params = parameters if parameters else gapc_bond_req_ind()

        super().__init__(msg_id=GAPC_MSG_ID.GAPC_BOND_REQ_IND,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=((conidx << 8) | KE_API_ID.TASK_ID_GAPC),
                         par_len=18,
                         parameters=params)

        self.parameters = params

# TODO need unit test 
class GapcBondCfm(GtlMessageBase):
    def __init__(self, conidx: c_uint8 = 0, parameters: gapc_bond_cfm = None):

        params = parameters if parameters else gapc_bond_cfm()

        super().__init__(msg_id=GAPC_MSG_ID.GAPC_BOND_CFM,
                         dst_id=((conidx << 8) | KE_API_ID.TASK_ID_GAPC),
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=30,
                         parameters=params)

        self.parameters = params

# TODO Next message: GAPC_BOND_IND 