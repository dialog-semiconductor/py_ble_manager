
from ctypes import Array, c_uint16, Union
# These message IDs are used by __repr
from ..gtl_port.gattc_task import GATTC_MSG_ID  # noqa: F401
from ..gtl_port.gattm_task import GATTM_MSG_ID  # noqa: F401
from ..gtl_port.gapc_task import GAPC_MSG_ID  # noqa: F401
from ..gtl_port.gapm_task import GAPM_MSG_ID  # noqa: F401
from ..gtl_port.rwip_config import KE_API_ID

GTL_INITIATOR = 0x05


class GtlMessageBase():

    def __init__(self,
                 msg_id: c_uint16 = 0,
                 dst_id: KE_API_ID = KE_API_ID.TASK_ID_INVALID,
                 src_id: KE_API_ID = KE_API_ID.TASK_ID_INVALID,
                 par_len: int = 0,
                 parameters: object() = None):

        self.msg_id = msg_id
        self.dst_id = dst_id
        self.src_id = src_id
        self.par_len = par_len
        self.parameters = parameters

    def to_bytes(self):

        message = bytearray()
        message.append(GTL_INITIATOR)
        message.extend(self.msg_id.value.to_bytes(length=2, byteorder='little'))
        message.extend(self.dst_id.to_bytes(length=2, byteorder='little'))
        message.extend(self.src_id.to_bytes(length=2, byteorder='little'))
        message.extend(self.par_len.to_bytes(length=2, byteorder='little'))
        message.extend(self._struct_to_bytearray(self.parameters))

        return message

    def to_hex(self):
        return self.to_bytes().hex().upper()

    def __eq__(self, other):
        if isinstance(other, GtlMessageBase):
            return self.to_bytes() == other.to_bytes()
        return False

    def __repr__(self):
        message_id = str(eval(f"{type(self.msg_id).__name__}({self.msg_id})"))

        # If GAPC or GATTC message, dst_id or scr_id contains conidx. Separate conidx from task_id
        if type(self.msg_id).__name__ == 'GAPC_MSG_ID' or type(self.msg_id).__name__ == 'GATTC_MSG_ID':
            if self.dst_id != KE_API_ID.TASK_ID_GTL:
                destination_id = f"(conidx={(self.dst_id & 0xFF00) >> 8}, id={str(KE_API_ID(self.dst_id & 0xFF))})"
                source_id = str(KE_API_ID(self.src_id))
            else:
                source_id = f"(conidx={(self.src_id & 0xFF00) >> 8}, id={str(KE_API_ID(self.src_id & 0xFF))})"
                destination_id = str(KE_API_ID(self.dst_id))
        else:
            destination_id = str(KE_API_ID(self.dst_id))
            source_id = str(KE_API_ID(self.src_id))

        return_string = f"{type(self).__name__}(msg_id={message_id}, dst_id={destination_id}, src_id={source_id}, par_len={self.par_len}, " + \
                        f"parameters={type(self.parameters).__name__}"

        return_string += self._struct_to_str(self.parameters)
        return_string = return_string[:-2]
        return_string += ')'

        return return_string

    def _array_to_str(self, field_name, array):
        param_string = f'{field_name}=('
        for i in array:
            param_string += f'{i}, '
        param_string = param_string[:-2]
        param_string += '), '
        return param_string

    def _struct_to_str(self, struct):
        return_string = ''
        param_string = ''

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
                    underlying_array = getattr(struct, public_field_name)
                    param_string += self._array_to_str(public_field_name, underlying_array)

                # if sub attribute is an array, traverse the array
                elif issubclass(type(sub_attr), Array):
                    param_string += self._array_to_str(field[0], sub_attr)

                # otherwise if sub attribute is not a structure or array, get the value of the field
                else:
                    param_string += f'{field[0]}={getattr(struct, field[0])}, '

            return_string += f'({param_string[:-2]}'
        return_string += '), '
        return return_string

    def _struct_to_bytearray(self, struct):
        return_array = bytearray()
        param_array = bytearray()

        # Expect a ctypes structure
        if struct:

            # workaround for now that need to revisit. this only works if union does not have a pointer with a subfield that is also a pointer
            if issubclass(type(struct), Union):
                return bytearray(struct)

            # for each field in the structure
            for field in struct._fields_:
                # get the attribute for that field
                sub_attr = getattr(struct, field[0])

                # if the sub attribute has is also a structure, call this function recursively
                if hasattr(sub_attr, '_fields_'):
                    param_array += self._struct_to_bytearray(sub_attr)

                # if sub attribute is a POINTER, convert its contents
                elif sub_attr and hasattr(sub_attr, 'contents'):
                    public_field_name = field[0].split('_')[1]
                    underlying_array = getattr(struct, public_field_name)
                    param_array += bytearray(underlying_array)

                elif issubclass(type(sub_attr), Array):
                    param_array += bytearray(sub_attr)

                # bit field, Need to short circuit to not add other bitfields as additional bytes as they are already included
                elif len(field) == 3:
                    return bytearray(struct)

                # otherwise if sub attribute is not a structure or POINTER, convert it directly
                else:
                    param_array += bytearray(field[1](sub_attr))

            return_array += param_array
        return return_array
