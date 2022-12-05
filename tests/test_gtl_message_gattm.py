import unittest
from ctypes import *
from gtl_messages import *

# Table 70
class TestGattmAddSvcReq(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        #TODO There are multiple errors in the manual that need to be addressed
        #TODO  05000B0B001000C000000004 -> this 04 does not match with example in manual   . Par_len 0C 00 does not match below either  
        # perm 0xCC also wrong -> see forum post on this
        # Att 5 permision wrong in manual, should be 0x09 0x00 0x0A -> A0009 -> as is att 7
        #self.expected = "05 00 0B 0B 00 10 00 C0 00 00 00 10 00 CC072F2A93A6BDD84152AC0B10992EC6FEED000003280000000000000000000000000000010000000080000020EE8D0CE1F04A0CB325DC536A68862D09000A00648000000129000000000000000000000000000001000000FA8000000328000000000000000000000000000001000000000000004F43313C939242E6A876FA3BEFB4875A  498208  00640000000129000000000000000000000000000001000000FA000000022900000000000000000000000000000900020002000000"
        self.expected = "05" + \
                        "000B" + \
                        "0B00" + \
                        "1000" + \
                        "C000" + \
                        "0000" + \
                        "1000" + \
                        "CC" + \
                        "07" + \
                        "2F2A93A6BDD84152AC0B10992EC6FEED" + \
                        "0000" + \
                        "03280000000000000000000000000000" + \
                        "01000000" + \
                        "0080" + \
                        "0000" + \
                        "20EE8D0CE1F04A0CB325DC536A68862D" + \
                        "09000A00" + \
                        "6480" + \
                        "0000" + \
                        "01290000000000000000000000000000" + \
                        "01000000" + \
                        "FA80" + \
                        "0000" + \
                        "03280000000000000000000000000000" + \
                        "01000000" + \
                        "0000" + \
                        "0000" + \
                        "4F43313C939242E6A876FA3BEFB4875A" + \
                        "09000A00" + \
                        "6400" + \
                        "0000" + \
                        "01290000000000000000000000000000" + \
                        "01000000" + \
                        "FA00" + \
                        "0000" + \
                        "02290000000000000000000000000000" + \
                        "09000A00" + \
                        "0200" + \
                        "0000"

    def test_parameters_updated_after_construction(self):
        
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

        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

# Table 75
class TestGattmAddSvcRsp(unittest.TestCase):

    def setUp(self):
        self.expected = "05010B10000B00040017000000"

    def test_parameters_updated_after_construction(self):
        
        test_message = GattmAddSvcRsp()
        test_message.parameters.start_hdl = 0x17
        test_message.parameters.status = HOST_STACK_ERROR_CODE.ATT_ERR_NO_ERROR

        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

# Table 87
class TestGattmAttSetValueReq(unittest.TestCase):

    def setUp(self):
        self.expected = "05" + \
                        "0C0B" + \
                        "0B00" + \
                        "1000" + \
                        "3A00" + \
                        "1C00" + \
                        "3600" + \
                        "7B636861726163746572697374696320427D2E7B63686172616374657269737469632076616C75657D202D64656D6F2076616C75652D"

    def test_parameters_updated_after_construction(self):
        
        test_message = GattmAttSetValueReq()
        test_message.parameters.handle = 28
        value = bytearray.fromhex("7B636861726163746572697374696320427D2E7B63686172616374657269737469632076616C75657D202D64656D6F2076616C75652D")
        test_message.parameters.value = (c_uint8 * len(value)).from_buffer_copy(value)

        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

# Table 87
class TestGattmAttSetValueRsp(unittest.TestCase):

    def setUp(self):
        self.expected = "050D0B10000B0004001C000000"

    def test_parameters_updated_after_construction(self):
        
        test_message = GattmAttSetValueRsp()
        test_message.parameters.handle = 28
        test_message.parameters.status = HOST_STACK_ERROR_CODE.ATT_ERR_NO_ERROR

        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

# Table 99
class TestGattmAttGetValueReq(unittest.TestCase):

    def setUp(self):
        self.expected = "050A0B0B00100002001C00"

    def test_parameters_updated_after_construction(self):
        
        test_message = GattmAttGetValueReq()
        test_message.parameters.handle = 28

        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

# Table 99
class TestGattmAttGetValueRsp(unittest.TestCase):

    def setUp(self):
        self.expected = "050B0B10000B003C001C00360000" + \
                        "7B636861726163746572697374696320427D2E7B63686172616374657269737469632076616C75657D202D64656D6F2076616C75652D00"

    def test_parameters_updated_after_construction(self):
        
        test_message = GattmAttGetValueRsp()
        test_message.parameters.handle = 28
        value = bytearray.fromhex("7B636861726163746572697374696320427D2E7B63686172616374657269737469632076616C75657D202D64656D6F2076616C75652D")
        test_message.parameters.value = (c_uint8 * len(value)).from_buffer_copy(value)

        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

if __name__ == '__main__':
    unittest.main()
    