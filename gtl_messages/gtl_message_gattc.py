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

    def to_bytes(self):

        message = bytearray()
        message.append(GTL_INITIATOR)
        members = self.__dict__.keys()
        for member in members:
            if(member != 'parameters'):
                #TODO  _par_len used in some messages to dynamically update par_len when length of parameters can change.
                # If GtlMessageBase to_bytes used for these classes, For some reason first call to to_bytes uses initial value of par_len and second call has correct updated value
                # Here to_bytes method has been overridden. But perhaps there is someway to handle in GtlMessageBase
                if(member == '_par_len'):
                    message.extend(self.par_len.to_bytes(length=2, byteorder='little'))
                else:
                    message.extend(getattr(self, member).to_bytes(length=2, byteorder='little'))

            elif(member == 'parameters' and getattr(self, 'par_len') > 0):
                message.extend(self._struct_to_bytearray(self.parameters))

        return message
    
 