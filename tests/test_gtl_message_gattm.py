import unittest
from ctypes import *
from gtl_messages import *

# Table 70
class TestGattmAddSvcReq(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        #TODO  05000B0B001000C000000004 -> this 04 does not match with example in manual   . Par_len 0C 00 does not match below either  
        # perm 0xCC also wrong -> see forum post on this
        #self.expected = "05 00 0B 0B 00 10 00 C0 00 00 00 10 00 CC072F2A93A6BDD84152AC0B10992EC6FEED000003280000000000000000000000000000010000000080000020EE8D0CE1F04A0CB325DC536A68862D09000A00648000000129000000000000000000000000000001000000FA8000000328000000000000000000000000000001000000000000004F43313C939242E6A876FA3BEFB4875A49820800640000000129000000000000000000000000000001000000FA000000022900000000000000000000000000000900020002000000"
        self.expected = "05000B0B001000C00000001000CC072F2A93A6BDD84152AC0B10992EC6FEED000003280000000000000000000000000000010000000080000020EE8D0CE1F04A0CB325DC536A68862D09000A00648000000129000000000000000000000000000001000000FA8000000328000000000000000000000000000001000000000000004F43313C939242E6A876FA3BEFB4875A49820800640000000129000000000000000000000000000001000000FA000000022900000000000000000000000000000900020002000000"

    def test_parameters_updated_after_construction(self):
        
        test_message = GattmAddSvcReq()
        test_message.parameters.svc_desc.task_id = KE_API_ID.TASK_ID_GTL
        test_message.parameters.svc_desc.perm.uuid_len = ATTM_UUID_LEN._128_BITS
        test_message.parameters.svc_desc.perm.svc_perm = ATTM_PERM.AUTH
        test_message.parameters.svc_desc.perm.enc_key_16_bytes = ATTM_ENC_KEY_SIZE_16_BYTES.NO
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
                                        max_len=100))

        uuid_str = bytearray.fromhex("00")*(ATT_UUID_128_LEN-2) + bytearray.fromhex("2901")
        uuid_str.reverse()
        att_list.append(gattm_att_desc(uuid=(c_uint8*ATT_UUID_128_LEN).from_buffer_copy(uuid_str),
                                        perm_read=ATTM_PERM.ENABLE,
                                        max_len=250,
                                        trigger_read_indication=ATTM_TRIGGER_READ_INDICATION.YES))

        uuid_str =  bytearray.fromhex("00")*(ATT_UUID_128_LEN-2) + bytearray.fromhex("2803")
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

        uuid_str = bytearray.fromhex("00")*(ATT_UUID_128_LEN-2) + bytearray.fromhex("2901")
        uuid_str.reverse()
        att_list.append(gattm_att_desc(uuid=(c_uint8*ATT_UUID_128_LEN).from_buffer_copy(uuid_str),
                                        perm_read=ATTM_PERM.ENABLE,
                                        max_len=250))

        uuid_str = bytearray.fromhex("00")*(ATT_UUID_128_LEN-2) + bytearray.fromhex("2902")
        uuid_str.reverse()
        att_list.append(gattm_att_desc(uuid=(c_uint8*ATT_UUID_128_LEN).from_buffer_copy(uuid_str),
                                        perm_read=ATTM_PERM.ENABLE,
                                        perm_write=ATTM_PERM.ENABLE,
                                        perm_write_request=ATTM_WRITE_REQUEST.ACCEPTED,
                                        uuid_len=ATTM_UUID_LEN._128_BITS,
                                        max_len=2))


        test_message.parameters.svc_desc.atts = (gattm_att_desc * len(att_list))(*att_list)
        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")


if __name__ == '__main__':
    unittest.main()
    