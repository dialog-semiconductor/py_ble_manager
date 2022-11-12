import serial
from gapm_task import *
#from GTL_definitions import MSG_ID_dict, ERR_CODE_dict, gapm_operation_dict
import sys
from ctypes import *
from typing import Any


GTL_INITIATOR = 0x05


class GtlMessage():
    # TODO these belong to the class, need to make for object by removing here (or make @dataclass?)
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
    
    #def creat_message_type(self, msg_id = GAPM_MSG_ID.GAPM_UNKNOWN_TASK_MSG, parameters = None):
    #    if(msg_id == GAPM_MSG_ID.GAPM_RESET_CMD):
    #        if(parameters == None):
    #            self.parameters == gapm_reset_cmd(GAPM_OPERATION.GAPM_RESET)
    #        elif(parameters )

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

    
class GapmResetCmd(GtlMessage):
    def __init__(self, 
                 par_len: int = 1,
                 parameters: gapm_reset_cmd_params = gapm_reset_cmd_params(GAPM_OPERATION.GAPM_NO_OP)):

        super().__init__(GAPM_MSG_ID.GAPM_RESET_CMD,
                         KE_API_ID.TASK_ID_GAPM,
                         KE_API_ID.TASK_ID_GTL,
                         par_len,
                         parameters)
                        
        self.parameters = parameters

class GapmCmpEvt(GtlMessage):
    def __init__(self, 
                 par_len: int = 2, # 2
                 parameters: gapm_cmp_evt_params = gapm_cmp_evt_params(GAPM_OPERATION.GAPM_NO_OP, HOST_STACK_ERROR_CODE.GAP_ERR_NO_ERROR)):

        super().__init__(GAPM_MSG_ID.GAPM_CMP_EVT,
                         KE_API_ID.TASK_ID_GTL,
                         KE_API_ID.TASK_ID_GAPM,
                         par_len,
                         parameters)

        self.parameters = parameters

   
test = GapmResetCmd(parameters = gapm_reset_cmd_params(GAPM_OPERATION.GAPM_RESET))
test.parameters.operation = GAPM_OPERATION.GAPM_CANCEL
print(test.parameters.operation)
print(test.to_bytes().hex())

test2 = GapmCmpEvt(parameters = gapm_cmp_evt_params(GAPM_OPERATION.GAPM_RESET, HOST_STACK_ERROR_CODE.GAP_ERR_NO_ERROR))
print(test2.parameters.operation)
print(test2.parameters.status)
print(test2.to_bytes().hex())

'''
gtl = GtlMessage()
gtl.msg_id = GAPM_MSG_ID.GAPM_RESET_CMD
gtl.par_len = 1
gtl.parameters = gapm_reset_cmd(GAPM_OPERATION.GAPM_RESET)

print(gtl.to_bytes().hex())

gtl2 = GtlMessage(GAPM_MSG_ID.GAPM_RESET_CMD, 1, gapm_reset_cmd(GAPM_OPERATION.GAPM_CANCEL))

print(gtl2.to_bytes().hex())
'''
#gtl3 = GtlMessage(GAPM_MSG_ID.GAPM_RESET_CMD, 1, gapm_reset_cmd(GAPM_OPERATION.GAPM_CANCEL))
#print(gtl3.to_bytes().hex())

#test = gapm_cmp_evt(1,2)

#print(test.operation)


#gtl5 = GAPM_RESET_CMD(1, gapm_reset_cmd(GAPM_OPERATION.GAPM_RESET))
#print(gtl5.to_bytes().hex())



#GAPM_RESET_CMD()

#ch_array = c_uint8 * 5
#channel_map = ch_array()
#ch_map = le_chnl_map_struct((c_uint8 * 5)(1,2,3,4,5))
#gtl4 = GtlMessage(GAPM_MSG_ID.GAPM_RESET_CMD, 1, 
#                 gapm_set_channel_map_cmd_struct(GAPM_OPERATION.GAPM_CANCEL,ch_map))
#print(gtl4.to_bytes().hex())

'''
ser = serial.Serial('COM13', 115200, timeout=1)  # open serial port
print(ser.name)         # check which port was really used


#gapm_reset_cmd = b'\x05 \x02\x0D\x0D\x00\x10\x00\x01\x00\x01'
#gapm_reset_cmd = bytes.fromhex('05020d0d001000010001')

print("Sending GAPM_RESET: ")
print(gapm_reset_cmd.hex())
ser.write(gapm_reset_cmd)
#ser.write(b'hello')     # write a string
print("waiting for data")
byte_string = ser.read(11)
print("data received")
print(byte_string.hex()) # GAPM_CMP_EVT: expect 0x05 0x00 0x0D 0x10 0x00 0x0D 0x00 0x02 0x00 0x01 0x

gapm_set_dev_config_cmd = bytes.fromhex('05040D0D0010002C00030A000000000000000000000000000000000000000000000000002000000000170000000000000000000000')
print("Sending GAPM_SET_DEV_CONFIG_CMD: ")
print(gapm_set_dev_config_cmd.hex())
ser.write(gapm_set_dev_config_cmd)

print("waiting for data")
new_string = ser.read(11)
print("data received")
print(new_string.hex()) #GAPM_CMP_EVT: expect 0x05 0x00 0x0D 0x10 0x00 0x0D 0x00 0x02 0x00 0x03 0x0

add_diss_cmd = bytes.fromhex('051B0D0D0010000E001B04140010000000730100000000')
print("Sending GAPM_PROFILE_TASK_ADD_CMD for DISS: ")
print(add_diss_cmd.hex())
ser.write(add_diss_cmd)

print("waiting for data")
new_string = ser.read(15)
print("data received")
print(new_string.hex()) #GAPM_PROFILE_ADDED_IND : expect 05 1C 0D 10 00 0D 00 06 00 14 00 14 00 0A 00

advertise_cmd = bytes.fromhex('050D0D0D00100052000D0000004C044C040701001707030318021804180E09444941475F435553545F53564300000000000000000A09FF006052572D424C4500000000000000000000000000000000000000000000000000000000')
print("Sending GAPM_START_ADVERTISE_CMD: ")
print(advertise_cmd.hex())
ser.write(advertise_cmd)

print("waiting for data") # waiting to connect
new_string = ser.read(25)
print("data received")
print(new_string.hex()) #GAPC_CONNECTION_REQ_IND  : expect 05 1C 0D 10 00 0D 00 06 00 14 00 14 00 0A 00


GAPC_CONNECTION_CFM = bytes.fromhex('05020E0E0010002C000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000')
print("Sending GAPC_CONNECTION_CFM: ")
print(GAPC_CONNECTION_CFM.hex())
ser.write(GAPC_CONNECTION_CFM)

ser.timeout = 20.0
print("waiting for data") # waiting to connect
new_string = ser.read(25)
print("data received")
print(new_string.hex())

ser.close()             # close port
'''
