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

    def to_hex(self):
        return self.to_bytes().hex().upper()

# TODO Do we need this? Is is a response, not somethine we need to send.
# We could match against response from DA14531?
class GapmDeviceReadyInd(GtlMessage):
     def __init__(self):

        super().__init__(msg_id=GAPM_MSG_ID.GAPM_DEVICE_READY_IND,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=KE_API_ID.TASK_ID_GAPM,
                         par_len=0,
                         parameters=None)

class GapmResetCmd(GtlMessage):
    def __init__(self, parameters: gapm_reset_cmd = gapm_reset_cmd()):

        super().__init__(msg_id=GAPM_MSG_ID.GAPM_RESET_CMD,
                         dst_id=KE_API_ID.TASK_ID_GAPM,
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=1,
                         parameters=parameters)
                        
        self.parameters = parameters

class GapmCmpEvt(GtlMessage):
    def __init__(self, parameters: gapm_cmp_evt = gapm_cmp_evt()):

        super().__init__(msg_id=GAPM_MSG_ID.GAPM_CMP_EVT,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=KE_API_ID.TASK_ID_GAPM,
                         par_len=2,
                         parameters=parameters)

        self.parameters = parameters


class GapmSetDevConfigCmd(GtlMessage):
    def __init__(self, parameters: gapm_set_dev_config_cmd = gapm_set_dev_config_cmd()):

        super().__init__(msg_id=GAPM_MSG_ID.GAPM_SET_DEV_CONFIG_CMD,
                         dst_id=KE_API_ID.TASK_ID_GAPM,
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=44,
                         parameters=parameters)

        self.parameters = parameters

class GapmStartAdvertiseCmd(GtlMessage):
    def __init__(self, parameters: gapm_start_advertise_cmd = gapm_start_advertise_cmd()):

        super().__init__(msg_id=GAPM_MSG_ID.GAPM_START_ADVERTISE_CMD,
                         dst_id=KE_API_ID.TASK_ID_GAPM,
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=82,
                         parameters=parameters)

        self.parameters = parameters




# Unit Testing 

def test_output(expected, test_case):
    print("Expected: ", expected)
    print("Actual  : ", test_case)
    print("Equal   : ", expected == test_case)
    print()

# Table 3
expected  = "05010D10000D000000"
# Test 1
test_case = GapmDeviceReadyInd().to_hex()
test_output(expected, test_case)

# Table 5
expected = "05020D0D001000010001"
# Test 1, pass in parameters on construction
test_case = GapmResetCmd(parameters = gapm_reset_cmd(GAPM_OPERATION.GAPM_RESET)).to_hex()
test_output(expected, test_case)
# Test 2, update parameters after construction
test_message = GapmResetCmd()
test_message.parameters = gapm_reset_cmd(GAPM_OPERATION.GAPM_RESET)
test_output(expected, test_case)

# Table 6
expected = "05000D10000D0002000100"
# Test 1, pass in parameters on construction
test_case = GapmCmpEvt(parameters = gapm_cmp_evt(GAPM_OPERATION.GAPM_RESET, 
                                                 HOST_STACK_ERROR_CODE.GAP_ERR_NO_ERROR)).to_hex()
test_output(expected, test_case)
# Test 2, update parameters after construction
test_message = GapmCmpEvt()
test_message.parameters = gapm_cmp_evt(GAPM_OPERATION.GAPM_RESET, 
                                       HOST_STACK_ERROR_CODE.GAP_ERR_NO_ERROR)
test_output(expected, test_case)

# Table 8
expected = "05040D0D0010002C00030A000000000000000000000000000000000000000000000000002000000000000200000000FB0048080000"
# Test 1, TODO  pass in parameters on construction
# Test 2, update  after construction
test_message = GapmSetDevConfigCmd()
test_message.parameters.operation = GAPM_OPERATION.GAPM_SET_DEV_CONFIG
test_message.parameters.role = GAP_ROLE.GAP_ROLE_PERIPHERAL
test_message.parameters.att_cfg = 0x20 # TODO setup GAPM_MASK_ATT_SVC_CNG_EN
test_message.parameters.max_mtu = 512 
test_message.parameters.max_txoctets = 251
test_message.parameters.max_txtime = 2120
test_case = test_message.to_hex()
test_output(expected, test_case)

# Table 9
expected = "05000D10000D0002000300"
# Test 1, pass in parameters on construction
test_case = GapmCmpEvt(parameters = gapm_cmp_evt(GAPM_OPERATION.GAPM_SET_DEV_CONFIG, 
                                                 HOST_STACK_ERROR_CODE.GAP_ERR_NO_ERROR)).to_hex()
test_output(expected, test_case)
# Test 2, update parameters after construction
test_message = GapmCmpEvt()
test_message.parameters = gapm_cmp_evt(GAPM_OPERATION.GAPM_SET_DEV_CONFIG, 
                                       HOST_STACK_ERROR_CODE.GAP_ERR_NO_ERROR)
test_output(expected, test_case)

# Test 3, update individual parameters after construction
test_message = GapmCmpEvt()
test_message.parameters.operation = GAPM_OPERATION.GAPM_SET_DEV_CONFIG
test_message.parameters.status = HOST_STACK_ERROR_CODE.GAP_ERR_NO_ERROR
test_output(expected, test_case)


# Table 11
expected = "050D0D0D00100052000D000000C800C8000701001B070303180218041812094469616C6F6750455220" + \
            "44413134353835000000000D0CFFD20053616D706C6520233100000000000000000000000000000000" + \
            "000000000000000000"
# Test 2, update  after construction
test_message = GapmStartAdvertiseCmd()
test_message.parameters.op.code = GAPM_OPERATION.GAPM_ADV_UNDIRECT
test_message.parameters.op.addr_src = GAPM_ADDR_TYPE.GAPM_CFG_ADDR_STATIC
test_message.parameters.intv_min = 200 # 0.625 x 200 = 125ms TODO would be nicer to have adv_slots to ms. Should it belong to a class?
test_message.parameters.intv_max = 200 # see above
test_message.parameters.channel_map = ADV_CHANNEL_MAP.ADV_ALL_CHNLS_EN 
test_message.parameters.info = gapm_adv_info()
test_message.parameters.info.host.mode = GAP_ADV_MODE.GAP_GEN_DISCOVERABLE
test_message.parameters.info.host.adv_filt_policy = ADV_FILTER_POLICY.ADV_ALLOW_SCAN_ANY_CON_ANY
test_message.parameters.info.host.adv_data_len = 27

# TODO move this to gapm_task.py def
adv_data_array = c_uint8*ADV_DATA_LEN
# TODO ensure easy to pass name from strin 
#complete_local_name = "DialogPER DA14585"
test_message.parameters.info.host.adv_data = adv_data_array(0x07, 0x03, 0x03, 0x18, 0x02, 0x18, 0x04, 0x18, 0x12, 0x09, 0x44, 0x69, 
                                                            0x61, 0x6c, 0x6f, 0x67, 0x50, 0x45, 0x52, 0x20, 0x44, 0x41, 0x31, 0x34,
                                                            0x35, 0x38, 0x35, 0x00, 0x00, 0x00, 0x00)
test_message.parameters.info.host.scan_rsp_data_len = 13
scan_response_data_array = c_uint8*SCAN_RSP_DATA_LEN
test_message.parameters.info.host.scan_rsp_data = scan_response_data_array(0x0c, 0xff, 0xd2, 0x00, 0x53, 0x61, 0x6d, 0x70, 0x6c, 0x65,
                                                                           0x20, 0x23, 0x31, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                                                           0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                                                           0x00)
test_message.parameters.info.host.peer_info = gap_bdaddr()                                                                

test_case = test_message.to_hex()
test_output(expected, test_case)


# Hacked comms Test

ser = serial.Serial('COM13', 115200)  # open serial port
print(ser.name)         # check which port was really used

# -> GAPM_RESET_CMD
# <- GAPM_CMP_EVT(GAPM_REST)

print("Sending GAPM_RESET: ")
cmd = GapmResetCmd(parameters = gapm_reset_cmd(GAPM_OPERATION.GAPM_RESET))
print(cmd.to_hex())
ser.write(cmd.to_bytes())

print("waiting for data")
byte_string = ser.read(11)
print("data received")
print(byte_string.hex()) # GAPM_CMP_EVT: expect 0x05 0x00 0x0D 0x10 0x00 0x0D 0x00 0x02 0x00 0x01 0x

# -> GAM_SET_DEV_CONFIG_CMD
# <- GAPM_CMP_EVT(GAPM_SET_DEV_CONFIG)
print("Sending GAPM_SET_DEV_CONFIG_CMD: ")
cmd = GapmSetDevConfigCmd()
cmd.parameters.operation = GAPM_OPERATION.GAPM_SET_DEV_CONFIG
cmd.parameters.role = GAP_ROLE.GAP_ROLE_PERIPHERAL
cmd.parameters.att_cfg = 0x20 # TODO setup GAPM_MASK_ATT_SVC_CNG_EN
cmd.parameters.max_mtu = 512 
cmd.parameters.max_txoctets = 251
cmd.parameters.max_txtime = 2120
print(cmd.to_hex())
ser.write(cmd.to_bytes())

print("waiting for data")
new_string = ser.read(11)
print("data received")
print(new_string.hex()) #GAPM_CMP_EVT: expect 0x05 0x00 0x0D 0x10 0x00 0x0D 0x00 0x02 0x00 0x03 0x0

# TODO Could add diss here for test

'''
add_diss_cmd = bytes.fromhex('051B0D0D0010000E001B04140010000000730100000000')
print("Sending GAPM_PROFILE_TASK_ADD_CMD for DISS: ")
print(add_diss_cmd.hex())
ser.write(add_diss_cmd)

print("waiting for data")
new_string = ser.read(15)
print("data received")
print(new_string.hex()) #GAPM_PROFILE_ADDED_IND : expect 05 1C 0D 10 00 0D 00 06 00 14 00 14 00 0A 00
'''

cmd = GapmStartAdvertiseCmd()
cmd.parameters.op.code = GAPM_OPERATION.GAPM_ADV_UNDIRECT
cmd.parameters.op.addr_src = GAPM_ADDR_TYPE.GAPM_CFG_ADDR_STATIC
cmd.parameters.intv_min = 200 # 0.625 x 200 = 125ms TODO would be nicer to have adv_slots to ms. Should it belong to a class?
cmd.parameters.intv_max = 200 # see above
cmd.parameters.channel_map = ADV_CHANNEL_MAP.ADV_ALL_CHNLS_EN 
cmd.parameters.info = gapm_adv_info()
cmd.parameters.info.host.mode = GAP_ADV_MODE.GAP_GEN_DISCOVERABLE
cmd.parameters.info.host.adv_filt_policy = ADV_FILTER_POLICY.ADV_ALLOW_SCAN_ANY_CON_ANY
cmd.parameters.info.host.adv_data_len = 27

# TODO move this to gapm_task.py def
adv_data_array = c_uint8*ADV_DATA_LEN
# TODO ensure easy to pass name from strin 
#complete_local_name = "DialogPER DA14585"
cmd.parameters.info.host.adv_data = adv_data_array(0x07, 0x03, 0x03, 0x18, 0x02, 0x18, 0x04, 0x18, 0x12, 0x09, 0x44, 0x69, 
                                                            0x61, 0x6c, 0x6f, 0x67, 0x50, 0x45, 0x52, 0x20, 0x44, 0x41, 0x31, 0x34,
                                                            0x35, 0x38, 0x35, 0x00, 0x00, 0x00, 0x00)
cmd.parameters.info.host.scan_rsp_data_len = 13
scan_response_data_array = c_uint8*SCAN_RSP_DATA_LEN
cmd.parameters.info.host.scan_rsp_data = scan_response_data_array(0x0c, 0xff, 0xd2, 0x00, 0x53, 0x61, 0x6d, 0x70, 0x6c, 0x65,
                                                                           0x20, 0x23, 0x31, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                                                           0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                                                           0x00)
cmd.parameters.info.host.peer_info = gap_bdaddr()   
print("Sending GAPM_START_ADVERTISE_CMD: ")
print(cmd.to_hex())
ser.write(cmd.to_bytes())

print("waiting for data") # waiting to connect
new_string = ser.read(25)
print("data received")
print(new_string.hex()) #GAPC_CONNECTION_REQ_IND  : expect 05 1C 0D 10 00 0D 00 06 00 14 00 14 00 0A 00

GAPC_CONNECTION_CFM = bytes.fromhex('05020E0E0010002C000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000')
print("Sending GAPC_CONNECTION_CFM: ")
print(GAPC_CONNECTION_CFM.hex())
ser.write(GAPC_CONNECTION_CFM)

ser.close()             # close port

'''
ser.timeout = 20.0
print("waiting for data") # waiting to connect
new_string = ser.read(25)
print("data received")
print(new_string.hex())

ser.close()             # close port
'''
