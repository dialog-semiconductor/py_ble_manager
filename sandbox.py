import serial
from ctypes import *
from gtl_messages import *

expected = "05000B0B001000C00000001000CC072F2A93A6BDD84152AC0B10992EC6FEED000003280000000000000000000000000000010000000080000020EE8D0CE1F04A0CB325DC536A68862D09000A00648000000129000000000000000000000000000001000000FA8000000328000000000000000000000000000001000000000000004F43313C939242E6A876FA3BEFB4875A49820800640000000129000000000000000000000000000001000000FA000000022900000000000000000000000000000900020002000000"


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
uuid_str = bytearray.fromhex("2803") + bytearray.fromhex("00")*(ATT_UUID_128_LEN-2)
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
                                max_len=100))

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


test_message.parameters.svc_desc.atts = (gattm_att_desc * len(att_list))(*att_list)


class test_class(Structure):
    def __init__(self, 
                start_hdl: c_uint16 = 0,
                task_id: KE_API_ID = 0):
        self.start_hdl = start_hdl
        self.task_id = task_id

        super().__init__(start_hdl=self.start_hdl,
                        task_id=self.task_id,)

                # Attribute Start Handle (0 = dynamically allocated)
    _fields_ = [("start_hdl", c_uint16),
                # Task identifier that manages service
                ("task_id", c_uint16)]



help = test_class()
help.start_hdl = 5
help.task_id = 9


print(test_message.to_hex())
print(len(test_message.to_bytes()))

expected_bytes = bytes.fromhex(expected)
print(expected)
print(len(expected_bytes))

class test_perm(Structure):
    def __init__(self, 
                 multi: ATTM_TASK_MULTI_INSTANTIATED = ATTM_TASK_MULTI_INSTANTIATED.NO, 
                 enc_key_16_bytes: ATTM_ENC_KEY_SIZE_16_BYTES = ATTM_ENC_KEY_SIZE_16_BYTES.NO, 
                 svc_perm: ATTM_PERM = ATTM_PERM.UNAUTH, 
                 uuid_len: ATTM_UUID_LEN = ATTM_UUID_LEN._16_BITS, 
                 primary_svc: ATTM_SERVICE_TYPE = ATTM_SERVICE_TYPE.PRIMARY_SERVICE
                ):

        self.multi = multi
        self.enc_key_16_bytes = enc_key_16_bytes
        self.svc_perm = svc_perm
        self.uuid_len = uuid_len
        self.primary_svc = primary_svc

        super().__init__(multi=self.multi,
                         enc_key_16_bytes=self.enc_key_16_bytes,
                         svc_perm=self.svc_perm,
                         uuid_len=self.uuid_len,
                         primary_svc=self.primary_svc)

                # Service permissions (@see enum attm_svc_perm_mask)
    _fields_ = [("multi", c_uint8, 1),
                ("enc_key_16_bytes", c_uint8, 1),
                ("svc_perm", c_uint8, 3),
                ("uuid_len", c_uint8, 2),
                ("primary_svc", c_uint8, 1)] 
                
helper = test_perm()
helper.multi = ATTM_TASK_MULTI_INSTANTIATED.YES
#helper.enc_key_16_bytes =  ATTM_ENC_KEY_SIZE_16_BYTES.NO 
helper.svc_perm = ATTM_PERM.UNAUTH
#helper.uuid_len = ATTM_UUID_LEN._128_BITS
helper.primary_svc = ATTM_SERVICE_TYPE.PRIMARY_SERVICE
print(bytearray(helper))