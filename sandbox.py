import serial
from ctypes import *
from gtl_messages import *

'''
test_message = GattmAddSvcReq()
test_message.parameters.svc_desc.task_id = KE_API_ID.TASK_ID_GTL
test_message.parameters.svc_desc.perm.uuid_len = ATTM_UUID_LEN._128_BITS
test_message.parameters.svc_desc.perm.svc_perm = ATTM_PERM.AUTH
test_message.parameters.svc_desc.perm.enc_key_16_bytes = ATTM_ENC_KEY_SIZE_16_BYTES.NO
test_message.parameters.svc_desc.nb_att = 7

# service uuid
uuid_str = bytearray.fromhex("EDFEC62E99100BAC5241D8BDA6932A2F")
uuid_str.reverse()
test_message.parameters.svc_desc.uuid = (c_uint8 * ATT_UUID_128_LEN).from_buffer_copy(uuid_str)

att_list = []
# att 1 
# TODO is there a better way to handle 16bit ids
uuid_str = bytearray.fromhex("00")*(ATT_UUID_128_LEN-2) + bytearray.fromhex("2803") 
uuid_str.reverse()
att = gattm_att_desc()
att.uuid = (c_uint8*ATT_UUID_128_LEN).from_buffer_copy(uuid_str)
att.perm.read = ATTM_PERM.ENABLE
att.max_len_read_ind.trigger_read_indication = ATTM_TRIGGER_READ_INDICATION.YES
att_list.append(att)

# att 2
uuid_str = bytearray.fromhex("2D86686A53DC25B30C4AF0E10C8DEE20")
uuid_str.reverse()
att = gattm_att_desc()
att.uuid = uuid=(c_uint8*ATT_UUID_128_LEN).from_buffer_copy(uuid_str)
att.perm.read = ATTM_PERM.ENABLE
att.perm.write=ATTM_PERM.ENABLE
att.perm.write_request=ATTM_WRITE_REQUEST.ACCEPTED
att.perm.uuid_len=ATTM_UUID_LEN._128_BITS
att.max_len_read_ind.max_len=100
att.max_len_read_ind.trigger_read_indication = ATTM_TRIGGER_READ_INDICATION.YES
att_list.append(att)

# att 3
uuid_str = bytearray.fromhex("00")*(ATT_UUID_128_LEN-2) + bytearray.fromhex("2901")
uuid_str.reverse()
att = gattm_att_desc()
att.uuid=(c_uint8*ATT_UUID_128_LEN).from_buffer_copy(uuid_str)
att.perm.read=ATTM_PERM.ENABLE
att.max_len_read_ind.max_len=250
att.max_len_read_ind.trigger_read_indication=ATTM_TRIGGER_READ_INDICATION.YES
att_list.append(att)

# att 4
uuid_str =  bytearray.fromhex("00")*(ATT_UUID_128_LEN-2) + bytearray.fromhex("2803")
uuid_str.reverse()
att = gattm_att_desc()
att.uuid=(c_uint8*ATT_UUID_128_LEN).from_buffer_copy(uuid_str)
att.perm.read=ATTM_PERM.ENABLE
att_list.append(att)

# att 5
uuid_str = bytearray.fromhex("5A87B4EF3BFA76A8E64292933C31434F")
uuid_str.reverse()
att = gattm_att_desc()
att.uuid=(c_uint8*ATT_UUID_128_LEN).from_buffer_copy(uuid_str)
att.perm.read=ATTM_PERM.ENABLE
att.perm.write=ATTM_PERM.ENABLE
att.perm.write_request=ATTM_WRITE_REQUEST.ACCEPTED
att.perm.uuid_len=ATTM_UUID_LEN._128_BITS
att.max_len_read_ind.max_len=100
att_list.append(att)

# att 6
uuid_str = bytearray.fromhex("00")*(ATT_UUID_128_LEN-2) + bytearray.fromhex("2901")
uuid_str.reverse()
att = gattm_att_desc()
att.uuid=(c_uint8*ATT_UUID_128_LEN).from_buffer_copy(uuid_str)
att.perm.read=ATTM_PERM.ENABLE
att.max_len_read_ind.max_len=250
att_list.append(att)

# att 7
uuid_str = bytearray.fromhex("00")*(ATT_UUID_128_LEN-2) + bytearray.fromhex("2902")
uuid_str.reverse()
att = gattm_att_desc()
att.uuid=(c_uint8*ATT_UUID_128_LEN).from_buffer_copy(uuid_str)
att.perm.read=ATTM_PERM.ENABLE
att.perm.write=ATTM_PERM.ENABLE
att.perm.write_request=ATTM_WRITE_REQUEST.ACCEPTED
att.perm.uuid_len=ATTM_UUID_LEN._128_BITS
att.max_len_read_ind.max_len=2
att_list.append(att)

test_message.parameters.svc_desc.atts = (gattm_att_desc * len(att_list))(*att_list)


print(test_message)
'''
expected = "05100C0C0010003E00120001001C003600" + \
                        "7B636861726163746572697374696320427D2E7B63686172616374657269737469632076616C75657D202D64656D6F2076616C75652D" 

        
test_message = GattcSendEvtCmd()
test_message.parameters.operation = GATTC_OPERATION.GATTC_NOTIFY
test_message.parameters.seq_num = 1
test_message.parameters.handle = 0x1C
value = bytearray.fromhex("7B636861726163746572697374696320427D2E7B63686172616374657269737469632076616C75657D202D64656D6F2076616C75652D")
test_message.parameters.value = (c_uint8 * len(value)).from_buffer_copy(value)


print(expected)
print(test_message.to_hex())
gattc_read_cfm()

huh = gapm_start_connection_cmd()
test = gattc_cmp_evt(operation=GATTC_OPERATION.GATTC_DISC_ALL_SVC)
test.operation = GATTC_OPERATION.GATTC_NOTIFY