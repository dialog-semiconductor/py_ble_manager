import serial
from ctypes import *
from gtl_messages import *

msg = GapmCmpEvt()
print(msg)


print(msg.msg_id)
print(msg.msg_id.value)

'''
test_message = GapmSetDevConfigCmd()
test_message.parameters.operation = GAPM_OPERATION.GAPM_SET_DEV_CONFIG
test_message.parameters.role = GAP_ROLE.GAP_ROLE_PERIPHERAL
test_message.parameters.att_cfg = 0x20 # TODO setup GAPM_MASK_ATT_SVC_CNG_EN
test_message.parameters.max_mtu = 512 
test_message.parameters.max_txoctets = 251
test_message.parameters.max_txtime = 2120

print(test_message)


test_message2 = GapmSetDevConfigCmd()
test_message2.parameters.operation = GAPM_OPERATION.GAPM_SET_DEV_CONFIG
test_message2.parameters.role = GAP_ROLE.GAP_ROLE_PERIPHERAL
test_message2.parameters.att_cfg = 0x20 # TODO setup GAPM_MASK_ATT_SVC_CNG_EN
test_message2.parameters.max_mtu = 512 
test_message2.parameters.max_txoctets = 251
test_message2.parameters.max_txtime = 2120

# Test mutable arguments to ctypes Strucutre
test_message2.parameters.addr.addr = (c_uint8*BD_ADDR_LEN)(1,2,3,4,5,6)

print(test_message)
print(test_message2)

print(test_message == test_message2)
'''

'''
print("Expect true: ", first_message == second_message)
print()

first_message.parameters.operation = GAPM_OPERATION.GAPM_CANCEL

print("Expect false: ", first_message == second_message)
print()

third_message = GapmCmpEvt(gapm_cmp_evt(GAPM_OPERATION.GAPM_CANCEL, HOST_STACK_ERROR_CODE.ATT_ERR_APP_ERROR))
fourth_message = GapmCmpEvt()

print("Expect false: ", third_message == fourth_message)
print()

fourth_message.parameters.operation = GAPM_OPERATION.GAPM_CANCEL

print("Expect false: ", third_message == fourth_message)
print()

fourth_message.parameters.status = HOST_STACK_ERROR_CODE.ATT_ERR_APP_ERROR

print("Expect true: ", third_message == fourth_message)
print()

print(first_message.__str__)
print(first_message.__repr__)
print(str(first_message))
print(first_message.parameters.operation)

fifth_message = GapcConnectionCfm()

print(fifth_message)
struct = gapc_connection_cfm()
print(struct)

msg = GapmCmpEvt(gapm_cmp_evt(GAPM_OPERATION.GAPM_RESET, HOST_STACK_ERROR_CODE.GAP_ERR_NO_ERROR))
test = gapm_cmp_evt.from_buffer_copy(msg.to_bytes()[9:])

print(msg.parameters.operation)
print(msg.parameters.status)
print(test.operation)
print(test.status)
'''

'''
first_message = GapmCmpEvt(gapm_cmp_evt(GAPM_OPERATION.GAPM_ADV_DIRECT))
second_message = GapmCmpEvt()

print("First : ", first_message.to_hex())
print("Second: ", second_message.to_hex())
print()

second_message.parameters.operation = GAPM_OPERATION.GAPM_ADV_NON_CONN

print("First : ", first_message.to_hex())
print("Second: ", second_message.to_hex())
print()

print("Changing to 0x0D")
second_message.parameters.operation = 0x0D

print("First : ", first_message.to_hex())
print("Second: ", second_message.to_hex())
print()

third_message = GapmCmpEvt()
third_message.parameters.operation = GAPM_OPERATION.GAPM_CANCEL

print("First : ", first_message.to_hex())
print("First sync: ", first_message.sync_test().hex().upper())
print("Second: ", second_message.to_hex())
print("Second sync: ", second_message.sync_test().hex().upper())
print("Third : ", third_message.to_hex())
print("Third sync: ", third_message.sync_test().hex().upper())
print()

ctype_test_1 = GapcConnectionCfm()
print("Ctype 1 : ", ctype_test_1.to_hex())


ctype_test_2 = GapcConnectionCfm(conidx=6)

print("Ctype 1 : ", ctype_test_1.to_hex())
print("Ctype 2 : ", ctype_test_2.to_hex())

'''


#
'''
first_message = GapmCmpEvt(gapm_cmp_evt(GAPM_OPERATION.GAPM_ADV_DIRECT))
second_message = GapmCmpEvt()
second_message.parameters.operation = GAPM_OPERATION.GAPM_ADV_NON_CONN

print("First : ", first_message.to_hex())
print("Second: ", second_message.to_hex())

third_message = GapmCmpEvt()
third_message.parameters.operation = GAPM_OPERATION.GAPM_CANCEL

print("First : ", first_message.to_hex())
print("Second: ", second_message.to_hex())
print("Third : ", third_message.to_hex())

fourth_message = GapcConnectionReqInd()

print("First : ", first_message.to_hex())
print("Second: ", second_message.to_hex())
print("Third : ", third_message.to_hex())
print("Fourth: ", fourth_message.to_hex())


first_struct = gapm_set_dev_config_cmd()
second_struct = gapm_set_dev_config_cmd()

print("First Struct: ", bytearray(first_struct).hex().upper())
print("Second Struct: ", bytearray(second_struct).hex().upper())
print()


first_struct.addr = bd_addr((c_uint8*BD_ADDR_LEN)(1, 2, 3, 4 , 5, 6))

print("First Struct: ", bytearray(first_struct).hex().upper())
print("Second Struct: ", bytearray(second_struct).hex().upper())

second_struct.addr = bd_addr((c_uint8*BD_ADDR_LEN)(7, 8, 9, 10 , 11, 12))

print("First Struct: ", bytearray(first_struct).hex().upper())
print("Second Struct: ", bytearray(second_struct).hex().upper())

'''