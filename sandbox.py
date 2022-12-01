import serial
from ctypes import *
from gtl_messages import *




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

list_to_array = (gattm_att_desc * len(att_list))(*att_list)
print(list_to_array)

# ASSIGNING AN ARRAY TO THE POINTER WORKS
test = gattm_svc_desc(atts=list_to_array)

print(test.atts)
print(test.atts[0])
print(test.atts[0].max_len)
print(test.atts[1])
print(test.atts[1].max_len)

att_list = []


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

# SETTING A NEW ARRAY WORKS TOO                        
test.atts = (gattm_att_desc * len(att_list))(*att_list)

print()

for i in range(3):
    print(f"uuid: {test.atts[i].uuid}, read: {test.atts[i].perm_read}, write: {test.atts[i].perm_write}, write requuest: {test.atts[i].perm_write_request}, uuid_len: {test.atts[i].uuid_len}, max_len: {test.atts[i].max_len}, trigger: {test.atts[i].trigger_read_indication} ")

print(test.atts)
print(len(test.atts))

print(GattmAddSvcReq())