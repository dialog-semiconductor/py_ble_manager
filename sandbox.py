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
test_message = GattmAddSvcReq()
print(test_message.to_hex())

test_message = GapmStartConnectionCmd()
test_message.parameters.op.code = GAPM_OPERATION.GAPM_CONNECTION_DIRECT
test_message.parameters.op.addr_src = GAPM_OWN_ADDR.GAPM_STATIC_ADDR
test_message.parameters.scan_interval = 384 # (384 x 0.625 = 240 ms)
test_message.parameters.scan_window = 352  # (352 x 0.625 = 220 ms)
test_message.parameters.con_intv_min = 36 # (36 × 1.25 ms = 45 ms
test_message.parameters.con_intv_max = 36 # (36 × 1.25 ms = 45 ms
test_message.parameters.superv_to = 500 # (500 x 10 = 5000ms = 5s) 
test_message.parameters.ce_len_min = 67 # (67 x 0.625 = 41.875 ms)
test_message.parameters.ce_len_max = 67 # (67 x 0.625 = 41.875 ms)
test_message.parameters.nb_peers = 1

# TODO par_len needs to get updated automatically based on nb_peers 
test_message.par_len = 21+test_message.parameters.nb_peers*7+1


# TODO need api to swap endian

addr_string = bytearray.fromhex('80EACA70EE09')
addr_string.reverse()
# TODO this is super convuluted. Find a better way. Create empty list of necessary size when allocation message?

test_message.parameters.peers = (gap_bdaddr * 1)(*[gap_bdaddr()])

print(test_message.parameters.peers[0].addr.addr)
