import unittest
from ctypes import *
from gtl_messages import *

# Table 95
class TestGattcWriteReqInd(unittest.TestCase):

    def setUp(self):
        self.expected = "05150C10000C0019001C00000013005772697474656E2062792063656E7472616C21"

    def test_parameters_updated_after_construction(self):
        
        test_message = GattcWriteReqInd()
        test_message.parameters.handle = 28
        value = bytearray.fromhex("5772697474656E2062792063656E7472616C21")
        test_message.parameters.value = (c_uint8 * len(value)).from_buffer_copy(value)

        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")
    
    def test_parameters_non_zero_conidx(self):
        test_message = GattcWriteReqInd(conidx=1)
        test_message.parameters.handle = 28
        value = bytearray.fromhex("5772697474656E2062792063656E7472616C21")
        test_message.parameters.value = (c_uint8 * len(value)).from_buffer_copy(value)

        self.assertNotEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

# Table 95
class TestGattcWriteCfm(unittest.TestCase):

    def setUp(self):
        self.expected = "05160C0C00100004001C000000"

    def test_parameters_updated_after_construction(self):
        
        test_message = GattcWriteCfm()
        test_message.parameters.handle = 28
        test_message.parameters.status = HOST_STACK_ERROR_CODE.ATT_ERR_NO_ERROR
        
        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")
    
    def test_parameters_non_zero_conidx(self):
        test_message = GattcWriteCfm(conidx=1)
        test_message.parameters.handle = 28

        self.assertNotEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

# Table 102
class TestGattcReadReqInd(unittest.TestCase):

    def setUp(self):
        self.expected = "05130C10000C0002001900"

    def test_parameters_updated_after_construction(self):
        
        test_message = GattcReadReqInd()
        test_message.parameters.handle = 25
        
        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")
    
    def test_parameters_non_zero_conidx(self):
        test_message = GattcReadReqInd(conidx=1)
        test_message.parameters.handle = 25

        self.assertNotEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

# Table 103
class TestGattcReadCfm(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
    
        self.expected = "05140C0C0010003C001900360000" + \
                        "7B636861726163746572697374696320427D2E7B63686172616374657269737469632076616C75657D202D64656D6F2076616C75652D00"

    def test_parameters_updated_after_construction(self):
        
        test_message = GattcReadCfm()
        test_message.parameters.handle = 25
        value = bytearray.fromhex("7B636861726163746572697374696320427D2E7B63686172616374657269737469632076616C75657D202D64656D6F2076616C75652D")
        test_message.parameters.value = (c_uint8 * len(value)).from_buffer_copy(value)
        
        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")
    
    def test_parameters_non_zero_conidx(self):
        test_message = GattcReadCfm(conidx=1)
        test_message.parameters.handle = 25
        value = bytearray.fromhex("7B636861726163746572697374696320427D2E7B63686172616374657269737469632076616C75657D202D64656D6F2076616C75652D")
        test_message.parameters.value = (c_uint8 * len(value)).from_buffer_copy(value)

        self.assertNotEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")


if __name__ == '__main__':
    unittest.main()
    