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

# Table 105
class TestGattcSendEvtCmd(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
    
        self.expected = "05100C0C0010003E00120001001C003600" + \
                        "7B636861726163746572697374696320427D2E7B63686172616374657269737469632076616C75657D202D64656D6F2076616C75652D" 

    def test_parameters_updated_after_construction(self):
        
        test_message = GattcSendEvtCmd()
        test_message.parameters.operation = GATTC_OPERATION.GATTC_NOTIFY
        test_message.parameters.seq_num = 1
        test_message.parameters.handle = 0x1C
        value = bytearray.fromhex("7B636861726163746572697374696320427D2E7B63686172616374657269737469632076616C75657D202D64656D6F2076616C75652D")
        test_message.parameters.value = (c_uint8 * len(value)).from_buffer_copy(value)
        
        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")
    
    def test_parameters_non_zero_conidx(self):
        test_message = GattcSendEvtCmd(conidx=1)
        test_message.parameters.seq_num = 1
        test_message.parameters.handle = 0x1C
        value = bytearray.fromhex("7B636861726163746572697374696320427D2E7B63686172616374657269737469632076616C75657D202D64656D6F2076616C75652D")
        test_message.parameters.value = (c_uint8 * len(value)).from_buffer_copy(value)

        self.assertNotEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

    def test_indication(self):

        # reset expected
        self.expected = "05100C0C0010000C0013000100120004000100FFFF" 

        test_message = GattcSendEvtCmd()
        test_message.parameters.operation = GATTC_OPERATION.GATTC_INDICATE
        test_message.parameters.seq_num = 1
        test_message.parameters.handle = 0x12
        value = bytearray.fromhex("0100FFFF")
        test_message.parameters.value = (c_uint8 * len(value)).from_buffer_copy(value)
        
        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

# Table 107
class TestGattcCmpEvt(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
    
        self.expected = "05000C10000C00040012000100"

    def test_parameters_updated_after_construction(self):
        
        test_message = GattcCmpEvt()
        test_message.parameters.operation = GATTC_OPERATION.GATTC_NOTIFY
        test_message.parameters.status = HOST_STACK_ERROR_CODE.ATT_ERR_NO_ERROR
        test_message.parameters.seq_num = 1
             
        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")
    
    def test_parameters_non_zero_conidx(self):
        
        test_message = GattcCmpEvt(conidx=1)
        test_message.parameters.operation = GATTC_OPERATION.GATTC_NOTIFY
        test_message.parameters.status = HOST_STACK_ERROR_CODE.ATT_ERR_NO_ERROR
        test_message.parameters.seq_num = 1

        self.assertNotEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

# Table 109
class TestGattcEventInd(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
    
        self.expected = "050C0C10000C000E001200080028000010000100000000"

    def test_parameters_updated_after_construction(self):
        
        test_message = GattcEventInd()
        test_message.parameters.type = GATTC_OPERATION.GATTC_NOTIFY
        test_message.parameters.handle = 40
        value = bytearray.fromhex("0010000100000000")
        test_message.parameters.value = (c_uint8 * len(value)).from_buffer_copy(value)
             
        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")
    
    def test_parameters_non_zero_conidx(self):
        
        test_message = GattcEventInd(conidx=1)
        test_message.parameters.type = GATTC_OPERATION.GATTC_NOTIFY
        test_message.parameters.handle = 40
        value = bytearray.fromhex("0010000100000000")
        test_message.parameters.value = (c_uint8 * len(value)).from_buffer_copy(value)

        self.assertNotEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

# Table 111
class TestGattcEventReqInd(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
    
        self.expected = "050D0C10000C000A001300040012000100FFFF"

    def test_parameters_updated_after_construction(self):
        
        test_message = GattcEventReqInd()
        test_message.parameters.type = GATTC_OPERATION.GATTC_INDICATE
        test_message.parameters.handle = 0x12
        value = bytearray.fromhex("0100FFFF")
        test_message.parameters.value = (c_uint8 * len(value)).from_buffer_copy(value)
             
        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")
    
    def test_parameters_non_zero_conidx(self):
        
        test_message = GattcEventReqInd(conidx=1)
        test_message.parameters.type = GATTC_OPERATION.GATTC_INDICATE
        test_message.parameters.handle = 0x12
        value = bytearray.fromhex("0100FFFF")
        test_message.parameters.value = (c_uint8 * len(value)).from_buffer_copy(value)

        self.assertNotEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

# Table 113
class TestGattcEventCfm(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
    
        self.expected = "050E0C0C00100002001300"

    def test_parameters_updated_after_construction(self):
        
        test_message = GattcEventCfm()
        #TODO Typo in manual, say type instead of handle
        test_message.parameters.handle = 0x13

        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")
    
    def test_parameters_non_zero_conidx(self):
        
        test_message = GattcEventCfm(conidx=1)
        #TODO Typo in manual, say type instead of handle
        test_message.parameters.handle = 0x13

        self.assertNotEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

# Table 115
class TestGattcDiscCmd(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
    
        # TODO message string does not align with table
        self.expected = "05030C0C0010000A00070220001A001C000000"

    def test_parameters_updated_after_construction(self):
        
        test_message = GattcDiscCmd()
        test_message.parameters.operation = GATTC_OPERATION.GATTC_DISC_DESC_CHAR
        test_message.parameters.seq_num = 0x20
        test_message.parameters.start_hdl = 26
        test_message.parameters.end_hdl = 28
        uuid = bytearray.fromhex("0000")
        test_message.parameters.uuid = (c_uint8 * len(uuid)).from_buffer_copy(uuid)
        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")
    
    def test_parameters_non_zero_conidx(self):
        
        test_message = GattcDiscCmd(conidx=1)
        test_message.parameters.operation = GATTC_OPERATION.GATTC_DISC_DESC_CHAR
        test_message.parameters.seq_num = 0x20
        test_message.parameters.start_hdl = 26
        test_message.parameters.end_hdl = 28
        uuid = bytearray.fromhex("0000")
        test_message.parameters.uuid = (c_uint8 * len(uuid)).from_buffer_copy(uuid)

        self.assertNotEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")


# Table 117
class TestGattcDiscCharDescInd(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.expected = "05070C10000C0006001A0002032800"

    def test_parameters_updated_after_construction(self):
        
        test_message = GattcDiscCharDescInd()
        test_message.parameters.attr_hdl = 26
        uuid = bytearray.fromhex("0328")
        test_message.parameters.uuid = (c_uint8 * len(uuid)).from_buffer_copy(uuid)
        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")
    
    def test_parameters_non_zero_conidx(self):
        
        test_message = GattcDiscCharDescInd(conidx=1)
        test_message.parameters.attr_hdl = 26
        uuid = bytearray.fromhex("0328")
        test_message.parameters.uuid = (c_uint8 * len(uuid)).from_buffer_copy(uuid)

        self.assertNotEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

# Table 122
class TestGattcDiscSvcInd(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        # TODO expected string does mot match table
        self.expected = "05040C10000C0008000100050002180100"

    def test_parameters_updated_after_construction(self):
        
        test_message = GattcDiscSvcInd()
        test_message.parameters.start_hdl = 1
        test_message.parameters.end_hdl = 5
        uuid = bytearray.fromhex("1801")
        test_message.parameters.uuid = (c_uint8 * len(uuid)).from_buffer_copy(uuid)
        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")
    
    def test_parameters_non_zero_conidx(self):
        
        test_message = GattcDiscSvcInd(conidx=1)
        test_message.parameters.start_hdl = 1
        test_message.parameters.end_hdl = 5
        uuid = bytearray.fromhex("1801")
        test_message.parameters.uuid = (c_uint8 * len(uuid)).from_buffer_copy(uuid)

        self.assertNotEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

# Table 127
class TestGattcDiscSvcInclInd(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        # TODO expected string does mot match table
        self.expected = "05050C10000C000A00150009000C00020F1800"

    def test_parameters_updated_after_construction(self):
        
        test_message = GattcDiscSvcInclInd()
        test_message.parameters.attr_hdl = 21
        test_message.parameters.start_hdl = 9
        test_message.parameters.end_hdl = 12
        uuid = bytearray.fromhex("0F18")
        test_message.parameters.uuid = (c_uint8 * len(uuid)).from_buffer_copy(uuid)
        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")
    
    def test_parameters_non_zero_conidx(self):
        
        test_message = GattcDiscSvcInclInd(conidx=1)
        test_message.parameters.attr_hdl = 21
        test_message.parameters.start_hdl = 9
        test_message.parameters.end_hdl = 12
        uuid = bytearray.fromhex("0F18")
        test_message.parameters.uuid = (c_uint8 * len(uuid)).from_buffer_copy(uuid)

        self.assertNotEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

# Table 132
class TestGattcDiscCharInd(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        # TODO expected string does mot match table
        self.expected = "05060C10000C000800020003000202002A"

    def test_parameters_updated_after_construction(self):
        
        test_message = GattcDiscCharInd()
        test_message.parameters.attr_hdl = 2
        test_message.parameters.pointer_hdl = 3
        test_message.parameters.prop = ATT_CHAR_PROP.READ
        uuid = bytearray.fromhex("002A")
        test_message.parameters.uuid = (c_uint8 * len(uuid)).from_buffer_copy(uuid)
        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")
    
    def test_parameters_non_zero_conidx(self):
        
        test_message = GattcDiscCharInd(conidx=1)
        test_message.parameters.attr_hdl = 2
        test_message.parameters.pointer_hdl = 3
        test_message.parameters.prop = ATT_CHAR_PROP.READ
        uuid = bytearray.fromhex("002A")
        test_message.parameters.uuid = (c_uint8 * len(uuid)).from_buffer_copy(uuid)

        self.assertNotEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

# Table 136
class TestGattcSdpSvcDiscCmd(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        # TODO expected string does mot match table
        self.expected = "05190C0C0010001800150220000100FFFF01180000000000000000000000000000"

    def test_parameters_updated_after_construction(self):
        
        test_message = GattcSdpSvcDiscCmd()
        test_message.parameters.operation = GATTC_OPERATION.GATTC_SDP_DISC_SVC
        test_message.parameters.seq_num = 0x20
        test_message.parameters.start_hdl = 1
        test_message.parameters.end_hdl = 0xFFFF
        uuid = bytearray.fromhex("0118")
        test_message.parameters.uuid = (c_uint8 * len(uuid)).from_buffer_copy(uuid)
        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")
    
    def test_parameters_non_zero_conidx(self):
        
        test_message = GattcSdpSvcDiscCmd(conidx=1)
        test_message.parameters.operation = GATTC_OPERATION.GATTC_SDP_DISC_SVC
        test_message.parameters.seq_num = 0x20
        test_message.parameters.start_hdl = 1
        test_message.parameters.end_hdl = 0xFFFF
        uuid = bytearray.fromhex("0118")
        test_message.parameters.uuid = (c_uint8 * len(uuid)).from_buffer_copy(uuid)

        self.assertNotEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")


# Table 146
class TestGattcReadCmd_GATTC_READ(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.expected = "05080C0C0010000A0008000B00040000000000"

    def test_parameters_updated_after_construction(self):
        
        test_message = GattcReadCmd()
        test_message.parameters.operation = GATTC_OPERATION.GATTC_READ
        test_message.parameters.seq_num = 0x0B
        test_message.parameters.req.simple.handle = 0x04

        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")
    
    def test_parameters_non_zero_conidx(self):
        
        test_message = GattcReadCmd(conidx=1)
        test_message.parameters.operation = GATTC_OPERATION.GATTC_READ
        test_message.parameters.seq_num = 0x0B
        test_message.parameters.req.simple.handle = 0x04

        self.assertNotEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

# Table 150
class TestGattcReadCmd_GATTC_READ_LONG(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.expected = "05080C0C0010000A0009002100030000000000"

    def test_parameters_updated_after_construction(self):
        
        test_message = GattcReadCmd()
        test_message.parameters.operation = GATTC_OPERATION.GATTC_READ_LONG
        test_message.parameters.seq_num = 0x21
        test_message.parameters.req.simple.handle = 0x03

        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")
    
    def test_parameters_non_zero_conidx(self):
        
        test_message = GattcReadCmd(conidx=1)
        test_message.parameters.operation = GATTC_OPERATION.GATTC_READ_LONG
        test_message.parameters.seq_num = 0x21
        test_message.parameters.req.simple.handle = 0x03

        self.assertNotEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

# Table 153
class TestGattcReadCmd_GATTC_READ_BY_UUID(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        # TODO string is wrong in manual
        self.expected = "05080C0C0010000C000A001B000100FFFF02002A00"

    def test_parameters_updated_after_construction(self):
        
        test_message = GattcReadCmd()
        test_message.parameters.operation = GATTC_OPERATION.GATTC_READ_BY_UUID
        test_message.parameters.seq_num = 0x1B
        test_message.parameters.req.by_uuid.start_hdl = 1
        test_message.parameters.req.by_uuid.end_hdl = 0xFFFF
        uuid = bytearray.fromhex("2A00")
        test_message.parameters.req.by_uuid.uuid = (c_uint8 * len(uuid)).from_buffer_copy(uuid)

        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")
    
    def test_parameters_non_zero_conidx(self):
        
        test_message = GattcReadCmd(conidx=1)
        test_message.parameters.operation = GATTC_OPERATION.GATTC_READ_BY_UUID
        test_message.parameters.seq_num = 0x1B
        test_message.parameters.req.by_uuid.start_hdl = 1
        test_message.parameters.req.by_uuid.end_hdl = 0xFFFF
        uuid = bytearray.fromhex("2A00")
        test_message.parameters.req.by_uuid.uuid = (c_uint8 * len(uuid)).from_buffer_copy(uuid)

        self.assertNotEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

# Table 156
class TestGattcReadCmd_GATTC_READ_MULTIPLE(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        # TODO string is wrong in manual
        self.expected = "05080C0C0010000C000B0216000400050005000200"

    def test_parameters_updated_after_construction(self):
        
        test_message = GattcReadCmd()
        test_message.parameters.operation = GATTC_OPERATION.GATTC_READ_MULTIPLE
        test_message.parameters.seq_num = 0x16
        # Note had issue creating array, then assigning handle/len for each item in array, then assigning array to req.multiple
        test_message.parameters.req.multiple = (gattc_read_multiple * 2)()
        test_message.parameters.req.multiple[0].handle = 4
        test_message.parameters.req.multiple[0].len = 5
        test_message.parameters.req.multiple[1].handle = 5
        test_message.parameters.req.multiple[1].len = 2

        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")
    
    def test_parameters_non_zero_conidx(self):
        
        test_message = GattcReadCmd(conidx=1)
        test_message.parameters.operation = GATTC_OPERATION.GATTC_READ_BY_UUID
        test_message.parameters.operation = GATTC_OPERATION.GATTC_READ_MULTIPLE
        test_message.parameters.seq_num = 0x16
        # Note had issue creating array, then assigning handle/len for each item in array, then assigning array to req.multiple
        test_message.parameters.req.multiple = (gattc_read_multiple * 2)()
        test_message.parameters.req.multiple[0].handle = 4
        test_message.parameters.req.multiple[0].len = 5
        test_message.parameters.req.multiple[1].handle = 5
        test_message.parameters.req.multiple[1].len = 2


        self.assertNotEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")


if __name__ == '__main__':
    unittest.main()
    