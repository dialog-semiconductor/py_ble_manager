
import sys
from ctypes import *
from .gtl_port import *

GTL_INITIATOR = 0x05

class GtlMessageBase():

    def __init__(self, 
                 msg_id: c_uint8 = 0, 
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

    def __eq__(self, other):
        if isinstance(other, GtlMessageBase):
            return self.to_bytes() == other.to_bytes()
        return False 

    # TODO need to handle if parameter field is another Strucutre, and if is an array
    def __repr__(self):
        # TODO KE_API_ID(self.src_id or dst_id) will not be correct if conidx is not 0
        #print(type(self.msg_id))
        #print(type(self.msg_id).__name__)
        message_id = str(eval(f"{type(self.msg_id).__name__}({self.msg_id})"))
        if self.dst_id != KE_API_ID.TASK_ID_GTL:
            destination_id = f"(conidx={(self.dst_id & 0xFF00) >> 8}, id={str(KE_API_ID(self.dst_id & 0xFF))})"
            source_id = str(KE_API_ID(self.src_id))
        else:
            source_id = f"(conidx={(self.src_id & 0xFF00) >> 8}, id={str(KE_API_ID(self.src_id & 0xFF))})"
            destination_id = str(KE_API_ID(self.dst_id))

        print(message_id)
        return_string = f'{type(self).__name__}(msg_id={message_id}, dst_id={destination_id}, src_id={source_id}, par_len={self.par_len}, parameters={type(self.parameters).__name__}'
        
        #return_string = f'{type(self).__name__}(msg_id={self.msg_id}, dst_id={KE_API_ID(self.dst_id)}, src_id={KE_API_ID(self.src_id)}, par_len={self.par_len}, parameters={type(self.parameters).__name__}'
        return_string += self.struct_to_str(self.parameters)
        return_string = return_string[:-2]
        return_string += f')'

        return return_string

    def struct_to_str(self, struct):
        return_string = f''
        param_string = f''

        # Expect a ctypes structure
        if struct: 
            # for each field in the structure
            for field in struct._fields_:
                # get the attribute for that field
                sub_attr = getattr(struct, field[0])    

                # if the sub attribute has is also a structure, call this function recursively
                if hasattr(sub_attr, '_fields_'):
                        param_string += f'{field[0]}={type(sub_attr).__name__}'
                        param_string += self.struct_to_str(sub_attr)

                # if sub attribute is an array, traverse the array        
                elif issubclass(type(sub_attr), Array):
                    param_string += f'{field[0]}=('
                    for i in sub_attr:
                        param_string += f'{i}, '
                    param_string = param_string[:-2]
                    param_string += f'), '

                # otherwise if sub attribute is not a structure or array, get the value of the field   
                else:
                    param_string += f'{field[0]}={getattr(struct, field[0])}, '

            return_string += f'({param_string[:-2]}'
        return_string += f'), ' 
        return return_string