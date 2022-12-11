from ctypes import *
from .gtl_message_base import *

class GapcConnectionReqInd(GtlMessageBase):

     def __init__(self, conidx: c_uint8 = 0, parameters: gapc_connection_req_ind = None):

        self.parameters = parameters if parameters else gapc_connection_req_ind()

        super().__init__(msg_id=GAPC_MSG_ID.GAPC_CONNECTION_REQ_IND,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=((conidx << 8) | KE_API_ID.TASK_ID_GAPC),
                         par_len=16,
                         parameters=self.parameters)
  
class GapcConnectionCfm(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gapc_connection_cfm = None):

        self.parameters = parameters if parameters else gapc_connection_cfm()

        super().__init__(msg_id=GAPC_MSG_ID.GAPC_CONNECTION_CFM,
                         dst_id=((conidx << 8) | KE_API_ID.TASK_ID_GAPC),
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=44,
                         parameters=self.parameters) 

class GapcSecurityCmd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gapc_security_cmd = None):

        self.parameters = parameters if parameters else gapc_security_cmd()

        super().__init__(msg_id=GAPC_MSG_ID.GAPC_SECURITY_CMD,
                         dst_id=((conidx << 8) | KE_API_ID.TASK_ID_GAPC),
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=2,
                         parameters=self.parameters)     

class GapcCmpEvt(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gapc_cmp_evt = None):

        self.parameters = parameters if parameters else gapc_cmp_evt()

        super().__init__(msg_id=GAPC_MSG_ID.GAPC_CMP_EVT,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=((conidx << 8) | KE_API_ID.TASK_ID_GAPC),
                         par_len=2,
                         parameters=self.parameters)

class GapcGetInfoCmd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gapc_get_info_cmd = None):

        self.parameters = parameters if parameters else gapc_get_info_cmd()

        super().__init__(msg_id=GAPC_MSG_ID.GAPC_GET_INFO_CMD,
                         dst_id=((conidx << 8) | KE_API_ID.TASK_ID_GAPC),
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=1,
                         parameters=self.parameters)

class GapcPeerFeaturesInd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gapc_peer_features_ind = None):

        self.parameters = parameters if parameters else gapc_peer_features_ind()

        super().__init__(msg_id=GAPC_MSG_ID.GAPC_PEER_FEATURES_IND,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=((conidx << 8) | KE_API_ID.TASK_ID_GAPC),
                         par_len=8,
                         parameters=self.parameters)

class GapcBondReqInd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gapc_bond_req_ind = None):

        self.parameters = parameters if parameters else gapc_bond_req_ind()

        super().__init__(msg_id=GAPC_MSG_ID.GAPC_BOND_REQ_IND,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=((conidx << 8) | KE_API_ID.TASK_ID_GAPC),
                         par_len=18,
                         parameters=self.parameters)

class GapcBondCfm(GtlMessageBase):
    
    def __init__(self, conidx: c_uint8 = 0, parameters: gapc_bond_cfm = None):

        self.parameters = parameters if parameters else gapc_bond_cfm()

        super().__init__(msg_id=GAPC_MSG_ID.GAPC_BOND_CFM,
                         dst_id=((conidx << 8) | KE_API_ID.TASK_ID_GAPC),
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=30,
                         parameters=self.parameters)   

# TODO Next message: GAPC_BOND_IND, GAPC_ENCRYPT_REQ_IND, GAPC_ENCRYPT_CFM, GAPC_ENCRYPT_IND, GAPC_PARAM_UPDATE_REQ_IND, GAPC_PARAM_UPDATE_CFM, GAPC_PARAM_UPDATE_CMD, GAPC_PARAM_UPDATED_IND 