import unittest
from ctypes import *
from gtl_message_gapm import *
from gtl_message_base import *
from gapm_task import *

# Table 3
class TestGapmDeviceReadyInd(unittest.TestCase):

    def setUp(self):
        self.expected  = bytes.fromhex("05010D10000D000000")
        self.message_type = type(GapmDeviceReadyInd()).__name__
    
    def test_message_creation(self):
        test_message = GapmDeviceReadyInd()
        self.assertEqual(test_message.to_bytes(), self.expected, "{0}() incorrect byte stream".format(self.message_type))

# Table 5
class TestGapmResetCmd(unittest.TestCase):

    def setUp(self):
        self.expected = bytes.fromhex("05020D0D001000010001")
        self.message_type = type(GapmResetCmd()).__name__
    
    def test_parameters_passed_on_construction(self):
        test_message = GapmResetCmd(parameters = gapm_reset_cmd(GAPM_OPERATION.GAPM_RESET))
        self.assertEqual(test_message.to_bytes(), self.expected, "{0}() incorrect byte stream".format(self.message_type))

    def test_parameters_updated_after_construction(self):
        test_message = GapmResetCmd()
        test_message.parameters = gapm_reset_cmd(GAPM_OPERATION.GAPM_RESET)
        self.assertEqual(test_message.to_bytes(), self.expected, "{0}() incorrect byte stream".format(self.message_type ))

    def test_parameters_wrong_operation(self):
        test_message = GapmResetCmd()
        test_message.parameters = gapm_reset_cmd(GAPM_OPERATION.GAPM_CANCEL)
        self.assertNotEqual(test_message.to_bytes(), self.expected, "{0}() incorrect byte stream".format(self.message_type))


# Table 6
# TODO Test individual params after construction?
class TestGapmCmpEvt_GAPM_RESET(unittest.TestCase):

    def setUp(self):
        self.expected = bytes.fromhex("05000D10000D0002000100")
        self.message_type = type(GapmCmpEvt()).__name__
        
    def test_parameters_passed_on_construction(self):
        test_message = GapmCmpEvt(parameters = gapm_cmp_evt(GAPM_OPERATION.GAPM_RESET, 
                                                            HOST_STACK_ERROR_CODE.GAP_ERR_NO_ERROR))

        self.assertEqual(test_message.to_bytes(), self.expected, "{0}() incorrect byte stream".format(self.message_type ))

    def test_parameters_updated_after_construction(self):
        test_message = GapmCmpEvt()
        test_message.parameters = gapm_cmp_evt(GAPM_OPERATION.GAPM_RESET, 
                                               HOST_STACK_ERROR_CODE.GAP_ERR_NO_ERROR)

        self.assertEqual(test_message.to_bytes(), self.expected, "{0}() incorrect byte stream".format(self.message_type ))

    def test_parameters_wrong_operation(self):
        test_message = GapmCmpEvt(parameters = gapm_cmp_evt(GAPM_OPERATION.GAPM_CANCEL, 
                                                            HOST_STACK_ERROR_CODE.GAP_ERR_NO_ERROR))

        self.assertNotEqual(test_message.to_bytes(), self.expected, "{0}() incorrect byte stream".format(self.message_type ))

    def test_parameters_wrong_host_stack_error_code(self):
        test_message = GapmCmpEvt(parameters = gapm_cmp_evt(GAPM_OPERATION.GAPM_RESET, 
                                                            HOST_STACK_ERROR_CODE.ATT_ERR_APP_ERROR))

        self.assertNotEqual(test_message.to_bytes(), self.expected, "{0}() incorrect byte stream".format(self.message_type ))

# Table 8
class TestGapmSetDevConfigCmd(unittest.TestCase):
    def setUp(self):
        self.expected = bytes.fromhex("05040D0D0010002C00030A000000000000000000000000000000000000000000000000002000000000000200000000FB0048080000")
        self.message_type = type(GapmSetDevConfigCmd()).__name__

    def test_parameters_updated_after_construction(self):
        test_message = GapmSetDevConfigCmd()
        test_message.parameters.operation = GAPM_OPERATION.GAPM_SET_DEV_CONFIG
        test_message.parameters.role = GAP_ROLE.GAP_ROLE_PERIPHERAL
        test_message.parameters.att_cfg = 0x20 # TODO setup GAPM_MASK_ATT_SVC_CNG_EN
        test_message.parameters.max_mtu = 512 
        test_message.parameters.max_txoctets = 251
        test_message.parameters.max_txtime = 2120

        self.assertEqual(test_message.to_bytes(), self.expected, "{0}() incorrect byte stream".format(self.message_type ))

# Table 9
class TestGapmCmpEvt_GAPM_SET_DEV_CONFIG(unittest.TestCase):

    def setUp(self):
        self.expected = bytes.fromhex("05000D10000D0002000300")
        self.message_type = type(GapmCmpEvt()).__name__
        
    def test_parameters_passed_on_construction(self):
        test_message = GapmCmpEvt(parameters = gapm_cmp_evt(GAPM_OPERATION.GAPM_SET_DEV_CONFIG, 
                                                            HOST_STACK_ERROR_CODE.GAP_ERR_NO_ERROR))

        self.assertEqual(test_message.to_bytes(), self.expected, "{0}() incorrect byte stream".format(self.message_type ))

    def test_parameters_updated_after_construction(self):
        test_message = GapmCmpEvt()
        test_message.parameters = gapm_cmp_evt(GAPM_OPERATION.GAPM_SET_DEV_CONFIG, 
                                               HOST_STACK_ERROR_CODE.GAP_ERR_NO_ERROR)

        self.assertEqual(test_message.to_bytes(), self.expected, "{0}() incorrect byte stream".format(self.message_type ))

    def test_parameters_wrong_operation(self):
        test_message = GapmCmpEvt(parameters = gapm_cmp_evt(GAPM_OPERATION.GAPM_CANCEL, 
                                                            HOST_STACK_ERROR_CODE.GAP_ERR_NO_ERROR))

        self.assertNotEqual(test_message.to_bytes(), self.expected, "{0}() incorrect byte stream".format(self.message_type ))

    def test_parameters_wrong_host_stack_error_code(self):
        test_message = GapmCmpEvt(parameters = gapm_cmp_evt(GAPM_OPERATION.GAPM_SET_DEV_CONFIG, 
                                                            HOST_STACK_ERROR_CODE.ATT_ERR_APP_ERROR))

        self.assertNotEqual(test_message.to_bytes(), self.expected, "{0}() incorrect byte stream".format(self.message_type ))

class TestGapmStartAdvertiseCmd(unittest.TestCase):
    def setUp(self):
        self.expected = bytes.fromhex("050D0D0D00100052000D000000C800C8000701001B070303180218041812094469616C6F6750455220" + \
                                        "44413134353835000000000D0CFFD20053616D706C6520233100000000000000000000000000000000" + \
                                        "000000000000000000")
        self.message_type = type(GapmStartAdvertiseCmd()).__name__
            
    def test_parameters_updated_after_construction(self):
        test_message = GapmStartAdvertiseCmd()
        test_message.parameters.op.code = GAPM_OPERATION.GAPM_ADV_UNDIRECT
        test_message.parameters.op.addr_src = GAPM_ADDR_TYPE.GAPM_CFG_ADDR_STATIC
        test_message.parameters.intv_min = 200 # 0.625 x 200 = 125ms TODO would be nicer to have adv_slots to ms. Should it belong to a class?
        test_message.parameters.intv_max = 200 # see above
        test_message.parameters.channel_map = ADV_CHANNEL_MAP.ADV_ALL_CHNLS_EN 
        test_message.parameters.info = gapm_adv_info()
        test_message.parameters.info.host.mode = GAP_ADV_MODE.GAP_GEN_DISCOVERABLE
        test_message.parameters.info.host.adv_filt_policy = ADV_FILTER_POLICY.ADV_ALLOW_SCAN_ANY_CON_ANY
        test_message.parameters.info.host.adv_data_len = 27

        # TODO move this to gapm_task.py def
        adv_data_array = c_uint8*ADV_DATA_LEN
        # TODO ensure easy to pass name from strin 
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

        self.assertEqual(test_message.to_bytes(), self.expected, "{0}() incorrect byte stream".format(self.message_type ))                                                           

unittest.main()
