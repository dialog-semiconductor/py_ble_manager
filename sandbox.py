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
expected = "05030C0C0010000A00070020001A001C000000"
test_message = GattcDiscCmd()
test_message.parameters.operation = GATTC_OPERATION.GATTC_DISC_DESC_CHAR
test_message.parameters.seq_num = 0x20
test_message.parameters.start_hdl = 26
test_message.parameters.end_hdl = 28
uuid = bytearray.fromhex("0000")
test_message.parameters.uuid = (c_uint8 * len(uuid)).from_buffer_copy(uuid)
print(expected)
print(test_message.to_hex())

