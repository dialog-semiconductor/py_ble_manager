
import sys
from ctypes import *
from .gtl_port import *

GTL_INITIATOR = 0x05

class GtlMessageBase():
    # msg_id: c_uint16 
    # dst_id: c_uint16
    # src_id: c_uint16
    # par_len: c_uint16
    # parameters: object()

    def __init__(self, 
                 msg_id: GAPM_MSG_ID = GAPM_MSG_ID.GAPM_UNKNOWN_TASK_MSG, 
                 dst_id: KE_API_ID = KE_API_ID.TASK_ID_INVALID,
                 src_id: KE_API_ID = KE_API_ID.TASK_ID_INVALID,
                 par_len: int = 0, 
                 parameters: object() = None ):

        self.msg_id = msg_id
        self.dst_id = dst_id
        self.src_id = src_id
        self.par_len = par_len
        self.parameters = parameters
    
    def to_bytes(self):
        message = bytearray()
        message.append(GTL_INITIATOR)

        members = self.__dict__.keys()
        for member in members:
            if(member != 'parameters'):
                message.extend(getattr(self, member).to_bytes(length=2, byteorder='little'))
            elif(member == 'parameters' and getattr(self, 'par_len') > 0):
                message.extend(bytearray(self.parameters)) # TODO revisit this for big endian machine
        
        return message

    def to_hex(self):
        return self.to_bytes().hex().upper()
