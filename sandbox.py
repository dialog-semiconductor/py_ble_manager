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
test = gattc_read_req()
test.simple.handle = 0x04
test.simple.offset = 0x05
test.simple.length = 0x06





expected = "05080C0C0010000A0008000B00040000000000"
test_message = GattcReadCmd()
test_message.parameters.operation = GATTC_OPERATION.GATTC_READ
test_message.parameters.seq_num = 0x0B
test_message.parameters.req.simple.handle = 0x04
print(expected)
print(len(bytes.fromhex(expected)))
print(test_message.to_hex())
print(len(test_message.to_bytes()))
print(test_message)

'''
read = gattc_read_req()
read.simple.handle = 1
read.simple.offset = 2
read.simple.length = 3

print(read.simple.handle)
print(read.simple.offset)
print(read.simple.length)


print(read.by_uuid.start_hdl)
print(read.by_uuid.end_hdl)
print(read.by_uuid.uuid_len)
for i in range(3):
    print(read.by_uuid.uuid[i])

print(test_message)

'''