import unittest
from gtl_messages.gtl_message_gapc import *
from gtl_messages.gtl_port.co_bt import BD_ADDR_LEN
from gtl_messages.gtl_port.gapc_task import *

# Table 13
class TestGapcConnectionReqInd(unittest.TestCase):

    def setUp(self):
        self.expected = "05010E10000E001000000024000000F401000002EE70CAEA80"
        
    def test_parameters_updated_after_construction(self):
        test_message = GapcConnectionReqInd()

        test_message.parameters.conhdl = 0
        test_message.parameters .con_interval = 36 # (36 × 1.25 ms = 45 ms)
        test_message.parameters.con_latency = 0
        test_message.parameters.sup_to = 500 # (500 x 10 = 5000ms = 5s)
        test_message.parameters.clk_accuracy = 0 
        test_message.parameters.peer_addr_type = 0 # Public

        # TODO need make array type 
        bd = c_uint8 * BD_ADDR_LEN
        # TODO having to put in this array backwards. Any way to address?
        test_message.parameters.peer_addr = bd_addr(addr=bd(0x02, 0xEE, 0x70, 0xCA, 0xEA, 0x80))

        
        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

    def test_parameters_non_zero_conidx(self):
        test_message = GapcConnectionReqInd(conidx=1)

        test_message.parameters.conhdl = 0
        test_message.parameters .con_interval = 36 # (36 × 1.25 ms = 45 ms)
        test_message.parameters.con_latency = 0
        test_message.parameters.sup_to = 500 # (500 x 10 = 5000ms = 5s)
        test_message.parameters.clk_accuracy = 0 
        test_message.parameters.peer_addr_type = 0 # Public

        # TODO need make array type 
        bd = c_uint8 * BD_ADDR_LEN
        # TODO having to put in this array backwards. Any way to address?
        test_message.parameters.peer_addr = bd_addr(addr=bd(0x02, 0xEE, 0x70, 0xCA, 0xEA, 0x80))

        self.assertNotEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

# Table 16
class TestGapcConnectionCfm(unittest.TestCase):

    def setUp(self):
        self.expected = "05020E0E0010002C000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"

    def test_parameters_updated_after_construction(self):
        test_message = GapcConnectionCfm()

        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

    def test_parameters_non_zero_conidx(self):
        test_message = GapcConnectionCfm(conidx=1)
        self.assertNotEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")


# Table 18
class TestGapcSecurityCmd(unittest.TestCase):

    def setUp(self):
        self.expected = "051A0E0E00100002000C0D"

    def test_parameters_updated_after_construction(self):
        test_message = GapcSecurityCmd()
        test_message.parameters.operation = GAPC_OPERATION.GAPC_SECURITY_REQ
        test_message.parameters.auth = GAP_AUTH.GAP_AUTH_REQ_SECURE_CONNECTION | GAP_AUTH.GAP_AUTH_REQ_MITM_BOND

        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

    def test_parameters_non_zero_conidx(self):
        test_message = GapcSecurityCmd(conidx=0)
        self.assertNotEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")
                                                
# Table 20
class TestGapcCmpEvt_GAPC_SERCUIRT_REQ(unittest.TestCase):

    def setUp(self):
        self.expected = "05000E10000E0002000C00"

    def test_parameters_updated_after_construction(self):
        test_message = GapcCmpEvt()
        test_message.parameters.operation = GAPC_OPERATION.GAPC_SECURITY_REQ
        test_message.parameters.status = HOST_STACK_ERROR_CODE.GAP_ERR_NO_ERROR

        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

    def test_parameters_non_zero_conidx(self):
        test_message = GapcCmpEvt(conidx=1)
        test_message.parameters.operation = GAPC_OPERATION.GAPC_SECURITY_REQ
        test_message.parameters.status = HOST_STACK_ERROR_CODE.GAP_ERR_NO_ERROR
        self.assertNotEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")
                                                
# Table 26
class TestGapcGetInfoCmd(unittest.TestCase):

    def setUp(self):
        self.expected = "05050E0E001000010004"

    def test_parameters_updated_after_construction(self):
        test_message = GapcGetInfoCmd()
        test_message.parameters.operation = GAPC_OPERATION.GAPC_GET_PEER_FEATURES

        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

    def test_parameters_non_zero_conidx(self):
        test_message = GapcGetInfoCmd(conidx=1)
        test_message.parameters.operation = GAPC_OPERATION.GAPC_GET_PEER_FEATURES
        self.assertNotEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

# Table 27
class TestGapcPeerFeaturesInd(unittest.TestCase):

    def setUp(self):
        # TODO Alot of these E's in the maanual are unicode in the document (U+0395 instead of U+0045)
        self.expected = "05080E10000E000800FF00000000000000"

    def test_parameters_updated_after_construction(self):
        test_message = GapcPeerFeaturesInd()
        features = bytearray(bytes.fromhex('FF00000000000000'))
        test_message.parameters.features = (c_uint8 * LE_FEATS_LEN).from_buffer_copy(features)

        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

    def test_parameters_non_zero_conidx(self):
        test_message = GapcPeerFeaturesInd(conidx=1)
        features = bytearray(bytes.fromhex('FF00000000000000'))
        test_message.parameters.features = (c_uint8 * LE_FEATS_LEN).from_buffer_copy(features)
        self.assertNotEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")
            
# Table 31 
class TestGapcBondReqInd(unittest.TestCase):

    def setUp(self):
        self.expected_legacy = "05130E10000E001200000500000000000000000000000000000000"
        self.expected_secure_connections = "05130E10000E001200000D00000000000000000000000000000000"

    def test_parameters_updated_after_construction_legacy(self):
        test_message = GapcBondReqInd()
        test_message.parameters.request = GAPC_BOND.GAPC_PAIRING_REQ
        test_message.parameters.data.auth_req = GAP_AUTH.GAP_AUTH_REQ_MITM_BOND

        self.assertEqual(test_message.to_hex(), self.expected_legacy, f"{type(test_message).__name__}() incorrect byte stream")

    def test_parameters_non_zero_conidx_legacy(self):
        test_message = GapcBondReqInd(conidx=1)
        test_message.parameters.request = GAPC_BOND.GAPC_PAIRING_REQ
        test_message.parameters.data.auth_req = GAP_AUTH.GAP_AUTH_REQ_MITM_BOND

        self.assertNotEqual(test_message.to_hex(), self.expected_legacy, f"{type(test_message).__name__}() incorrect byte stream")
            
    def test_parameters_updated_after_construction_secure(self):
        test_message = GapcBondReqInd()
        test_message.parameters.request = GAPC_BOND.GAPC_PAIRING_REQ
        test_message.parameters.data.auth_req = GAP_AUTH.GAP_AUTH_REQ_MITM_BOND | GAP_AUTH.GAP_AUTH_REQ_SECURE_CONNECTION

        self.assertEqual(test_message.to_hex(), self.expected_secure_connections, f"{type(test_message).__name__}() incorrect byte stream")

    def test_parameters_non_zero_conidx_secure(self):
        test_message = GapcBondReqInd(conidx=1)
        test_message.parameters.request = GAPC_BOND.GAPC_PAIRING_REQ
        test_message.parameters.data.auth_req = GAP_AUTH.GAP_AUTH_REQ_MITM_BOND | GAP_AUTH.GAP_AUTH_REQ_SECURE_CONNECTION

        self.assertNotEqual(test_message.to_hex(), self.expected_secure_connections, f"{type(test_message).__name__}() incorrect byte stream")

# Table 33
class TestGapcBondCfm(unittest.TestCase):

    def setUp(self):
        self.expected = "05140E0E0010001E00010101000D10020102000000000000000000000000000000000000000000"

    def test_parameters_updated_after_construction(self):
        test_message = GapcBondCfm()
        test_message.parameters.request = GAPC_BOND.GAPC_PAIRING_RSP
        test_message.parameters.accept = 0x01 # TODO enum for this?        
        test_message.parameters.data.pairing_feat.iocap = GAP_IO_CAP.GAP_IO_CAP_DISPLAY_YES_NO
        test_message.parameters.data.pairing_feat.oob = GAP_OOB.GAP_OOB_AUTH_DATA_NOT_PRESENT
        test_message.parameters.data.pairing_feat.auth = GAP_AUTH.GAP_AUTH_REQ_SECURE_CONNECTION | GAP_AUTH.GAP_AUTH_REQ_MITM_BOND
        # Key size 16 bytes by default
        test_message.parameters.data.pairing_feat.ikey_dist = GAP_KDIST.GAP_KDIST_IDKEY # initiator should distribute IRK for random address resolution
        test_message.parameters.data.pairing_feat.rkey_dist = GAP_KDIST.GAP_KDIST_ENCKEY # responder distributes LTK 
        test_message.parameters.data.pairing_feat.sec_req = GAP_SEC_REQ.GAP_SEC1_AUTH_PAIR_ENC # minimum security requirements, MITM is required. Peer cannot pair without MITM

        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

    def test_parameters_non_zero_conidx(self):
        test_message = GapcBondCfm(conidx=1)
        test_message.parameters.request = GAPC_BOND.GAPC_PAIRING_RSP
        test_message.parameters.accept = 0x01 # TODO enum for this?        
        test_message.parameters.data.pairing_feat.iocap = GAP_IO_CAP.GAP_IO_CAP_DISPLAY_YES_NO
        test_message.parameters.data.pairing_feat.oob = GAP_OOB.GAP_OOB_AUTH_DATA_NOT_PRESENT
        test_message.parameters.data.pairing_feat.auth = GAP_AUTH.GAP_AUTH_REQ_SECURE_CONNECTION | GAP_AUTH.GAP_AUTH_REQ_MITM_BOND
        # Key size 16 bytes by default
        test_message.parameters.data.pairing_feat.ikey_dist = GAP_KDIST.GAP_KDIST_IDKEY # initiator should distribute IRK for random address resolution
        test_message.parameters.data.pairing_feat.rkey_dist = GAP_KDIST.GAP_KDIST_ENCKEY # responder distributes LTK 
        test_message.parameters.data.pairing_feat.sec_req = GAP_SEC_REQ.GAP_SEC1_AUTH_PAIR_ENC # minimum security requirements, MITM is required. Peer cannot pair without MITM

        self.assertNotEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")
         
# Table 166
class TestGapcSignCounterInd(unittest.TestCase):

    def setUp(self):
        self.expected = "051C0E10000E0008000200000000000000"

    def test_parameters_updated_after_construction(self):
        test_message = GapcSignCounterInd()
        test_message.parameters.local_sign_counter = 2

        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

    def test_parameters_non_zero_conidx(self):
        test_message = GapcSignCounterInd(conidx=1)
        test_message.parameters.local_sign_counter = 2
        
        self.assertNotEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")
         

if __name__ == '__main__':
    unittest.main()