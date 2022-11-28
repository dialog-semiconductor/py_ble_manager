import serial
from ctypes import *
from gtl_messages import *


test_message = GattmAddSvcReq()
test_message.parameters.svc_desc.task_id = KE_API_ID.TASK_ID_GTL
test_message.parameters.svc_desc.perm_uuid_len = ATTM_UUID_LEN._128_BITS
test_message.parameters.svc_desc.perm_svc_perm = ATTM_PERM.AUTH
test_message.parameters.svc_desc.perm_enc_key_16_bytes = ATTM_ENC_KEY_SIZE_16_BYTES.NO
test_message.parameters.svc_desc.nb_att = 7

uuid_str = bytearray.fromhex("EDFEC62E99100BAC5241D8BDA6932A2F")
uuid_str.reverse()
test_message.parameters.svc_desc.uuid = (c_uint8 * ATT_UUID_128_LEN).from_buffer_copy(uuid_str)

att_list = []
# TODO is there a better way to handle 16bit ids
uuid_str = bytearray.fromhex("00")*(ATT_UUID_128_LEN-2) + bytearray.fromhex("2803") 
uuid_str.reverse()
att_list.append(gattm_att_desc(uuid=(c_uint8*ATT_UUID_128_LEN).from_buffer_copy(uuid_str),
                                perm_read=ATTM_PERM.ENABLE,
                                trigger_read_indication=ATTM_TRIGGER_READ_INDICATION.YES))

uuid_str = bytearray.fromhex("2D86686A53DC25B30C4AF0E10C8DEE20")
uuid_str.reverse()
att_list.append(gattm_att_desc(uuid=(c_uint8*ATT_UUID_128_LEN).from_buffer_copy(uuid_str),
                                perm_read=ATTM_PERM.ENABLE,
                                perm_write=ATTM_PERM.ENABLE,
                                perm_write_request=ATTM_WRITE_REQUEST.ACCEPTED,
                                uuid_len=ATTM_UUID_LEN._128_BITS,
                                max_len=100,
                                trigger_read_indication=ATTM_TRIGGER_READ_INDICATION.YES))
'''

uuid_str = bytearray.fromhex("2901") + bytearray.fromhex("00")*(ATT_UUID_128_LEN-2)
uuid_str.reverse()
att_list.append(gattm_att_desc(uuid=(c_uint8*ATT_UUID_128_LEN).from_buffer_copy(uuid_str),
                                perm_read=ATTM_PERM.ENABLE,
                                max_len=250,
                                trigger_read_indication=ATTM_TRIGGER_READ_INDICATION.YES))

uuid_str = bytearray.fromhex("2803") + bytearray.fromhex("00")*(ATT_UUID_128_LEN-2)
uuid_str.reverse()
att_list.append(gattm_att_desc(uuid=(c_uint8*ATT_UUID_128_LEN).from_buffer_copy(uuid_str),
                                perm_read=ATTM_PERM.ENABLE))

uuid_str = bytearray.fromhex("5A87B4EF3BFA76A8E64292933C31434F")
uuid_str.reverse()
att_list.append(gattm_att_desc(uuid=(c_uint8*ATT_UUID_128_LEN).from_buffer_copy(uuid_str),
                                perm_read=ATTM_PERM.ENABLE,
                                perm_write=ATTM_PERM.ENABLE,
                                perm_write_request=ATTM_WRITE_REQUEST.ACCEPTED,
                                uuid_len=ATTM_UUID_LEN._128_BITS,
                                max_len=100))

uuid_str = bytearray.fromhex("2901") + bytearray.fromhex("00")*(ATT_UUID_128_LEN-2)
uuid_str.reverse()
att_list.append(gattm_att_desc(uuid=(c_uint8*ATT_UUID_128_LEN).from_buffer_copy(uuid_str),
                                perm_read=ATTM_PERM.ENABLE,
                                max_len=250))

uuid_str = bytearray.fromhex("2902") + bytearray.fromhex("00")*(ATT_UUID_128_LEN-2)
uuid_str.reverse()
att_list.append(gattm_att_desc(uuid=(c_uint8*ATT_UUID_128_LEN).from_buffer_copy(uuid_str),
                                perm_read=ATTM_PERM.ENABLE,
                                perm_write=ATTM_PERM.ENABLE,
                                perm_write_request=ATTM_WRITE_REQUEST.ACCEPTED,
                                uuid_len=ATTM_UUID_LEN._128_BITS,
                                max_len=2))

'''
test_message.parameters.svc_desc.atts = (gattm_att_desc * len(att_list))(*att_list)

expected = "05000B0B001000C00000001000CC072F2A93A6BDD84152AC0B10992EC6FEED000003280000000000000000000000000000010000000080000020EE8D0CE1F04A0CB325DC536A68862D09000A00648000000129000000000000000000000000000001000000FA8000000328000000000000000000000000000001000000000000004F43313C939242E6A876FA3BEFB4875A49820800640000000129000000000000000000000000000001000000FA000000022900000000000000000000000000000900020002000000"

print(len(bytes.fromhex(expected)))
print(expected)
print(len(test_message.to_hex()))
print(test_message.to_hex())

print(test_message)

print(gattm_svc_desc.perm_multi)
print(gattm_svc_desc.perm_enc_key_16_bytes)
print(gattm_svc_desc.perm_svc_perm)
print(gattm_svc_desc.perm_uuid_len)
print(gattm_svc_desc.perm_primary_svc)


test = (gattm_att_desc * len(att_list))(*att_list)
test_point = pointer(test)
print(bytearray(test).hex().upper())

print(bytearray(test_message.parameters.svc_desc.atts).hex().upper())

print(test_point)
print(bytearray(test_point.contents).hex().upper())
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