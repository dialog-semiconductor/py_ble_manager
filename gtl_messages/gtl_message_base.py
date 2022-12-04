
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
                # TODO need to detect if pointer type and get contents. Look at __repr__ for parsing. Make Struct to bytearray?
                #message.extend(bytearray(self.parameters)) # TODO revisit this for big endian machine
                message.extend(self._struct_to_bytearray(self.parameters))
                #print(f"message before: {message[:10]}")
                #message.extend(self.serialize(self.parameters))
        
        return message

    def to_hex(self):
        return self.to_bytes().hex().upper()

    def __eq__(self, other):
        if isinstance(other, GtlMessageBase):
            return self.to_bytes() == other.to_bytes()
        return False 

    def __repr__(self):
        message_id = str(eval(f"{type(self.msg_id).__name__}({self.msg_id})"))

        # If GAPC message, dst_id or scr_id contains conidx. Separate conidx from task_id
        if type(self.msg_id).__name__ == 'GAPC_MSG_ID':
            if self.dst_id != KE_API_ID.TASK_ID_GTL:
                destination_id = f"(conidx={(self.dst_id & 0xFF00) >> 8}, id={str(KE_API_ID(self.dst_id & 0xFF))})"
                source_id = str(KE_API_ID(self.src_id))
            else:
                source_id = f"(conidx={(self.src_id & 0xFF00) >> 8}, id={str(KE_API_ID(self.src_id & 0xFF))})"
                destination_id = str(KE_API_ID(self.dst_id))
        else:
            destination_id = str(KE_API_ID(self.dst_id))
            source_id = str(KE_API_ID(self.src_id))
            
        return_string = f'{type(self).__name__}(msg_id={message_id}, dst_id={destination_id}, src_id={source_id}, par_len={self.par_len}, parameters={type(self.parameters).__name__}'
        
        #return_string = f'{type(self).__name__}(msg_id={self.msg_id}, dst_id={KE_API_ID(self.dst_id)}, src_id={KE_API_ID(self.src_id)}, par_len={self.par_len}, parameters={type(self.parameters).__name__}'
        return_string += self._struct_to_str(self.parameters)
        return_string = return_string[:-2]
        return_string += f')'

        return return_string

    def _array_to_str(self, field_name, array):
        param_string = f'{field_name}=('
        for i in array:
            param_string += f'{i}, '
        param_string = param_string[:-2]
        param_string += f'), '
        return param_string

    def _struct_to_str(self, struct):
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
                        param_string += self._struct_to_str(sub_attr)

                # if sub_attribute is pointer, cast to array and treat the same
                elif sub_attr and hasattr(sub_attr, 'contents'):
                    public_field_name = field[0].split('_')[1]
                    ptr_underlying_array = getattr(struct, field[0].split('_')[1]) 
                    # TODO below works when pointer is to non-fundamental c type (ie for GattmAddSvcReq().parameters.svc_desc.atts)
                    # but may cause issues if pointer is to fundamental ctype (ie c_uint8). Needs to be tested 
                    for item in ptr_underlying_array:
                        param_string += self._struct_to_str(item)


                # if sub attribute is an array, traverse the array        
                elif issubclass(type(sub_attr), Array):
                    param_string += self._array_to_str(field[0], sub_attr)

                # otherwise if sub attribute is not a structure or array, get the value of the field   
                else:
                    param_string += f'{field[0]}={getattr(struct, field[0])}, '

            return_string += f'({param_string[:-2]}'
        return_string += f'), ' 
        return return_string

    def _struct_to_bytearray(self, struct):
        return_array = bytearray()
        param_array = bytearray()

        # Expect a ctypes structure
        if struct: 

            # TODO workaround for now that need to revisit. this only works if union does not have a pointer or bitfield in it. Would union ever have zero len array??
            if issubclass(type(struct), Union):
                return bytearray(struct)

            # for each field in the structure
            for field in struct._fields_:
                # get the attribute for that field
                sub_attr = getattr(struct, field[0])    
                attr_type = field[1]

                # if the sub attribute has is also a structure, call this function recursively
                if hasattr(sub_attr, '_fields_'):
                        param_array += self._struct_to_bytearray(sub_attr)

                # if sub attribute is a POINTER, convert its contents     
                elif sub_attr and hasattr(sub_attr, 'contents'):
                    sub_attr_array = getattr(struct, field[0].split('_')[1])    
                    param_array += bytearray(sub_attr_array)

                elif issubclass(type(sub_attr), Array):
                    param_array += bytearray(sub_attr)

                # some c structure use zero length array.
                # in this case additional variable added to structure to track length on underlying array pointer points to
                # we dont want this extra tracking variable to be added to the bytearray so skip it
                elif field[0][0] == "_" and field[0][-3:] == "len":
                    continue

                # bit field, Need to short circuit to not add other bitfields as additional bytes as they are already included
                elif len(field) == 3:
                    return bytearray(struct) 

                # otherwise if sub attribute is not a structure or POINTER, convert it directly 
                else:
                    # TODO Need to handle uuid endianness and should work
                    param_array += bytearray(field[1](sub_attr))

            return_array += param_array
        return return_array

'''
#TODO Seems to work but needs more testing
class GtlMesssageDynamicParLen(GtlMessageBase):

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

        super().__init__(msg_id=self.msg_id,
                         dst_id=self.dst_id,
                         src_id=self.src_id,
                         par_len=self.par_len,
                         parameters=parameters)


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
                # TODO need to detect if pointer type and get contents. Look at __repr__ for parsing. Make Struct to bytearray?
                #message.extend(bytearray(self.parameters)) # TODO revisit this for big endian machine

                print(f"message before: {message[:10]}")
                message.extend(self._struct_to_bytearray(self.parameters))
                #print(f"message before: {message[:10]}")
                #message.extend(self.serialize(self.parameters))
        
        return message
'''