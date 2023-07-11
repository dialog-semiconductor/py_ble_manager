import unittest
from py_ble_manager.gtl_messages.gtl_message_gapm import *
from py_ble_manager.gtl_port.co_bt import *
from py_ble_manager.gtl_port.gapm_task import *

# Table 3
class TestGapmDeviceReadyInd(unittest.TestCase):

    def setUp(self):
        self.expected  = "05010D10000D000000"
    
    def test_message_creation(self):
        test_message = GapmDeviceReadyInd()
        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

# Table 5
class TestGapmResetCmd(unittest.TestCase):

    def setUp(self):
        self.expected = "05020D0D001000010001"
    
    def test_parameters_passed_on_construction(self):
        test_message = GapmResetCmd(parameters = gapm_reset_cmd(GAPM_OPERATION.GAPM_RESET))
        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

    def test_parameters_updated_after_construction(self):
        test_message = GapmResetCmd()
        test_message.parameters = gapm_reset_cmd(GAPM_OPERATION.GAPM_RESET)
        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

    def test_parameters_wrong_operation(self):
        test_message = GapmResetCmd()
        test_message.parameters = gapm_reset_cmd(GAPM_OPERATION.GAPM_CANCEL)
        self.assertNotEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")


# Table 6
# TODO Test individual params after construction?
class TestGapmCmpEvt_GAPM_RESET(unittest.TestCase):

    def setUp(self):
        self.expected = "05000D10000D0002000100"
        
    def test_parameters_passed_on_construction(self):
        test_message = GapmCmpEvt(parameters = gapm_cmp_evt(GAPM_OPERATION.GAPM_RESET, 
                                                            HOST_STACK_ERROR_CODE.GAP_ERR_NO_ERROR))

        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

    def test_parameters_updated_after_construction(self):
        test_message = GapmCmpEvt()
        test_message.parameters.operation = GAPM_OPERATION.GAPM_RESET
        test_message.parameters.status = HOST_STACK_ERROR_CODE.GAP_ERR_NO_ERROR

        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

    def test_parameters_wrong_operation(self):
        test_message = GapmCmpEvt(parameters = gapm_cmp_evt(GAPM_OPERATION.GAPM_CANCEL, 
                                                            HOST_STACK_ERROR_CODE.GAP_ERR_NO_ERROR))

        self.assertNotEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

    def test_parameters_wrong_host_stack_error_code(self):
        test_message = GapmCmpEvt(parameters = gapm_cmp_evt(GAPM_OPERATION.GAPM_RESET, 
                                                            HOST_STACK_ERROR_CODE.ATT_ERR_APP_ERROR))

        self.assertNotEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

# Table 8
class TestGapmSetDevConfigCmd(unittest.TestCase):
    def setUp(self):
        # TODO example in manual has maximum mps as 0x0000, but max mps must be between 23 and 512
        self.expected = "05040D0D0010002C00030A000000000000000000000000000000000000000000000000002000000000000217000000FB0048080000"

    def test_parameters_updated_after_construction(self):
        test_message = GapmSetDevConfigCmd()
        test_message.parameters.operation = GAPM_OPERATION.GAPM_SET_DEV_CONFIG
        test_message.parameters.role = GTL_GAP_ROLE.GAP_ROLE_PERIPHERAL
        test_message.parameters.att_cfg.svc_chg_present = True
        test_message.parameters.max_mtu = 512 
        test_message.parameters.max_txoctets = 251
        test_message.parameters.max_txtime = 2120

        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

# Table 9
class TestGapmCmpEvt_GAPM_SET_DEV_CONFIG(unittest.TestCase):

    def setUp(self):
        self.expected = "05000D10000D0002000300"
        
    def test_parameters_passed_on_construction(self):
        test_message = GapmCmpEvt(parameters = gapm_cmp_evt(GAPM_OPERATION.GAPM_SET_DEV_CONFIG, 
                                                            HOST_STACK_ERROR_CODE.GAP_ERR_NO_ERROR))

        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

    def test_parameters_updated_after_construction(self):
        test_message = GapmCmpEvt()
        test_message.parameters = gapm_cmp_evt(GAPM_OPERATION.GAPM_SET_DEV_CONFIG, 
                                               HOST_STACK_ERROR_CODE.GAP_ERR_NO_ERROR)

        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

    def test_parameters_wrong_operation(self):
        test_message = GapmCmpEvt(parameters = gapm_cmp_evt(GAPM_OPERATION.GAPM_CANCEL, 
                                                            HOST_STACK_ERROR_CODE.GAP_ERR_NO_ERROR))

        self.assertNotEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

    def test_parameters_wrong_host_stack_error_code(self):
        test_message = GapmCmpEvt(parameters = gapm_cmp_evt(GAPM_OPERATION.GAPM_SET_DEV_CONFIG, 
                                                            HOST_STACK_ERROR_CODE.ATT_ERR_APP_ERROR))

        self.assertNotEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

# Table 11
class TestGapmStartAdvertiseCmd(unittest.TestCase):
    def setUp(self):
        self.expected = "050D0D0D00100052000D000000C800C8000701001B070303180218041812094469616C6F6750455220" + \
                                      "44413134353835000000000D0CFFD20053616D706C6520233100000000000000000000000000000000" + \
                                      "000000000000000000"
            
    def test_parameters_updated_after_construction(self):
        test_message = GapmStartAdvertiseCmd()
        test_message.parameters.op.code = GAPM_OPERATION.GAPM_ADV_UNDIRECT
        test_message.parameters.op.addr_src = GAPM_OWN_ADDR.GAPM_STATIC_ADDR
        test_message.parameters.intv_min = 200 # 0.625 x 200 = 125ms TODO would be nicer to have adv_slots to ms. Should it belong to a class?
        test_message.parameters.intv_max = 200 # see above
        test_message.parameters.channel_map = ADV_CHANNEL_MAP.ADV_ALL_CHNLS_EN 
        test_message.parameters.info = gapm_adv_info()
        test_message.parameters.info.host.mode = GAP_ADV_MODE.GAP_GEN_DISCOVERABLE
        test_message.parameters.info.host.adv_filt_policy = ADV_FILTER_POLICY.ADV_ALLOW_SCAN_ANY_CON_ANY
        test_message.parameters.info.host.adv_data_len = 27

        # TODO move this to gapm_task.py def
        adv_data_array = c_uint8*ADV_DATA_LEN
        # TODO ensure easy to pass name from string
        #complete_local_name = "DialogPER DA14585"
        test_message.parameters.info.host.adv_data = adv_data_array(0x07, 0x03, 0x03, 0x18, 0x02, 0x18, 0x04, 0x18, 0x12, 0x09, 0x44, 0x69, 
                                                                    0x61, 0x6c, 0x6f, 0x67, 0x50, 0x45, 0x52, 0x20, 0x44, 0x41, 0x31, 0x34,
                                                                    0x35, 0x38, 0x35, 0x00, 0x00, 0x00, 0x00)
        test_message.parameters.info.host.scan_rsp_data_len = 13
        scan_response_data_array = c_uint8*SCAN_RSP_DATA_LEN
        test_message.parameters.info.host.scan_rsp_data = scan_response_data_array(0x0c, 0xff, 0xd2, 0x00, 0x53, 0x61, 0x6d, 0x70, 0x6c, 0x65,
                                                                                0x20, 0x23, 0x31, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                                                                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                                                                0x00)
        test_message.parameters.info.host.peer_info = gap_bdaddr()     

        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")          

# Table 19
class TestGapmCmpEvt_GAPM_ADV_UNDIRECT(unittest.TestCase):

    def setUp(self):
        self.expected = "05000D10000D0002000D00"
        
    def test_parameters_passed_on_construction(self):
        test_message = GapmCmpEvt(parameters = gapm_cmp_evt(GAPM_OPERATION.GAPM_ADV_UNDIRECT, 
                                                            HOST_STACK_ERROR_CODE.GAP_ERR_NO_ERROR))

        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

# Not sure these are really necessary
'''
    def test_parameters_updated_after_construction(self):
        test_message = GapmCmpEvt()
        test_message.parameters = gapm_cmp_evt(GAPM_OPERATION.GAPM_ADV_UNDIRECT, 
                                               HOST_STACK_ERROR_CODE.GAP_ERR_NO_ERROR)

        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

    def test_parameters_wrong_operation(self):
        test_message = GapmCmpEvt(parameters = gapm_cmp_evt(GAPM_OPERATION.GAPM_CANCEL, 
                                                            HOST_STACK_ERROR_CODE.GAP_ERR_NO_ERROR))

        self.assertNotEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

    def test_parameters_wrong_host_stack_error_code(self):
        test_message = GapmCmpEvt(parameters = gapm_cmp_evt(GAPM_OPERATION.GAPM_ADV_UNDIRECT, 
                                                            HOST_STACK_ERROR_CODE.ATT_ERR_APP_ERROR))

        self.assertNotEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")     
'''

# Table 22
class TestGapmStartConnectionCmd(unittest.TestCase):

    def setUp(self):
        self.expected = "05110D0D0010001D001300000080016001240024000000F401430043000109EE70CAEA800000"
        
    def test_parameters_passed_on_construction(self):
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

        addr_string = bytearray.fromhex('80EACA70EE09')
        addr_string.reverse()
        # have to pass a ctype list whose parm is the contents of a list with the data. Less covuluted way to do this?
        test_message.parameters.peers = (gap_bdaddr * 1)(*[gap_bdaddr()])

        # peers comes back as an array that we can index into directly, but editor has trouble with type TODO Typedef return type??
        test_message.parameters.peers[0].addr.addr = (c_uint8 * BD_ADDR_LEN).from_buffer_copy(addr_string)
    
        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

# Table 186
class TestGapmStartScanCmd(unittest.TestCase):

    def setUp(self):
        self.expected = "050F0D0D0010000C0012000000A000500000000000"
        
    def test_parameters_passed_on_construction(self):
        test_message = GapmStartScanCmd()
        test_message.parameters.op.code = GAPM_OPERATION.GAPM_SCAN_PASSIVE
        test_message.parameters.op.addr_src = GAPM_OWN_ADDR.GAPM_STATIC_ADDR
        test_message.parameters.interval = 160
        test_message.parameters.window = 80
        test_message.parameters.mode = GAP_SCAN_MODE.GAP_GEN_DISCOVERY
        test_message.parameters.filt_policy = SCAN_FILTER_POLICY.SCAN_ALLOW_ADV_ALL
        test_message.parameters.filter_duplic = SCAN_DUP_FILTER_POLICY.SCAN_FILT_DUPLIC_DIS

        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

# Table 187
class TestGapmAdvReportInd(unittest.TestCase):

    def setUp(self):
        self.expected = "05100D10000D00290000001BA070CAEA801B0201061107B75C49D204A34071A0B535853EB08307050978494F5400000000BD"
        
    def test_parameters_passed_on_construction(self):
        test_message = GapmAdvReportInd()
        test_message.parameters.report.adv_addr_type = BD_ADDRESS_TYPE.ADDR_PUBLIC
        addr_string = bytearray.fromhex('80EACA70A01B')
        addr_string.reverse()
        test_message.parameters.report.adv_addr.addr[:] = addr_string
        data_string = bytearray.fromhex('0201061107B75C49D204A34071A0B535853EB08307050978494F54')
        test_message.parameters.report.data = data_string 
        test_message.parameters.report.rssi = 0xBD

        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

# Table 197
class TestGapmCancelCmd(unittest.TestCase):

    def setUp(self):
        self.expected = "05030D0D001000010002"
        
    def test_parameters_passed_on_construction(self):
        test_message = GapmCancelCmd()

        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

# Table 42
class TestGapmResolvAddrCmd(unittest.TestCase):

    def setUp(self):
        self.expected = "05140D0D00100018001701BD74EB757E59872FF3AC0D0428EB37B5B6CC9E5AE867"
        
    def test_parameters_passed_on_construction(self):
        test_message = GapmResolvAddrCmd()

        addr_string = bytearray.fromhex('597E75EB74BD')  # TODO manual has different addr in comments vs hex
        addr_string.reverse()
        test_message.parameters.addr.addr = (c_uint8 * BD_ADDR_LEN).from_buffer_copy(addr_string)

        irk_string = bytearray.fromhex('67E85A9ECCB6B537EB28040DACF32F87')
        irk_string.reverse()
        test_message.parameters.irk = (gap_sec_key * 1)()
        test_message.parameters.irk[0].key = (c_uint8 * KEY_LEN).from_buffer_copy(irk_string)
        

        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

# Table 43
class TestGapmAddrSolvedInd(unittest.TestCase):

    def setUp(self):
        self.expected = "05150D10000D001600BD74EB757E59872FF3AC0D0428EB37B5B6CC9E5AE867"
        
    def test_parameters_passed_on_construction(self):
        test_message = GapmAddrSolvedInd()

        addr_string = bytearray.fromhex('597E75EB74BD')
        addr_string.reverse()
        test_message.parameters.addr.addr = (c_uint8 * BD_ADDR_LEN).from_buffer_copy(addr_string)

        irk_string = bytearray.fromhex('67E85A9ECCB6B537EB28040DACF32F87')
        irk_string.reverse()
        test_message.parameters.irk.key = (c_uint8 * KEY_LEN).from_buffer_copy(irk_string)
        

        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

# Table 221
class TestGapmGetDevVersionCmd(unittest.TestCase):

    def setUp(self):
        self.expected = "05060D0D001000010005"
        
    def test_parameters_passed_on_construction(self):
        test_message = GapmGetDevVersionCmd()

        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

# Table 223
class TestGapmDevVersionInd(unittest.TestCase):

    def setUp(self):
        self.expected = "05070D10000D000C000A0A08000F010F010E01D200"
        
    def test_parameters_passed_on_construction(self):
        test_message = GapmDevVersionInd()
        test_message.parameters.hci_ver = 0x0A
        test_message.parameters.lmp_ver = 0x0A
        test_message.parameters.host_ver = 0x08
        test_message.parameters.hci_subver = 0x010F
        test_message.parameters.lmp_subver = 0x010F
        test_message.parameters.host_subver = 0x010E
        test_message.parameters.manuf_name = 0x00D2

        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

# Table 227
class TestGapmDevBdAddrInd(unittest.TestCase):

    def setUp(self):
        self.expected = "05080D10000D000700070770CAEA8000"
        
    def test_parameters_passed_on_construction(self):
        test_message = GapmDevBdAddrInd()
        addr_string = bytearray.fromhex('80EACA700707')
        addr_string.reverse()
        test_message.parameters.addr.addr.addr = (c_uint8 * BD_ADDR_LEN).from_buffer_copy(addr_string)

        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

if __name__ == '__main__':
    unittest.main()