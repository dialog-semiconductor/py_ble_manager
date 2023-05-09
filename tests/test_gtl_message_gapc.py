import unittest
from src.python_gtl_thread.gtl_messages.gtl_message_gapc import *
from src.python_gtl_thread.gtl_port.co_bt import BD_ADDR_LEN
from src.python_gtl_thread.gtl_port.gapc_task import *

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

# Table 37
class TestGapcBondInd(unittest.TestCase):

    def setUp(self):
        self.expected = "05150E10000E001E0007009CD33293FE9B3F5A9F7A7391D5613A4A000000000000000000001000"

    def test_parameters_updated_after_construction(self):
        test_message = GapcBondInd()
        test_message.parameters.info = GAPC_BOND.GAPC_LTK_EXCH
        ltk = bytearray.fromhex("4A3A61D591737A9F5A3F9BFE9332D39C")
        ltk.reverse()
        test_message.parameters.data.ltk.ltk.key = (c_uint8 * len(ltk)).from_buffer_copy(ltk)
        test_message.parameters.data.ltk.key_size = 16

        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

    def test_parameters_non_zero_conidx(self):
        test_message = GapcBondInd(conidx=1)
        test_message.parameters.info = GAPC_BOND.GAPC_LTK_EXCH
        ltk = bytearray.fromhex("4A3A61D591737A9F5A3F9BFE9332D39C")
        ltk.reverse()
        test_message.parameters.data.ltk.ltk.key = (c_uint8 * len(ltk)).from_buffer_copy(ltk)
        test_message.parameters.data.ltk.key_size = 16

        self.assertNotEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

# Table 46
class TestGapcEncryptReqInd(unittest.TestCase):

    def setUp(self):
        self.expected = "05170E10000E000A003962B0CB49680745C87F"

    def test_parameters_updated_after_construction(self):
        test_message = GapcEncryptReqInd()
        test_message.parameters.ediv = 0x6239
        rand = bytearray.fromhex("7FC845076849CBB0")
        rand.reverse()
        test_message.parameters.rand_nb.nb = (c_uint8 * len(rand)).from_buffer_copy(rand)

        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

    def test_parameters_non_zero_conidx(self):
        test_message = GapcEncryptReqInd(conidx=1)
        test_message.parameters.ediv = 0x6239
        rand = bytearray.fromhex("7FC845076849CBB0")
        rand.reverse()
        test_message.parameters.rand_nb.nb = (c_uint8 * len(rand)).from_buffer_copy(rand)

        self.assertNotEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

# Table 48
class TestGapcEncryptCfm(unittest.TestCase):

    def setUp(self):
        self.expected = "05180E0E0010001200019CD33293FE9B3F5A9F7A7391D5613A4A10"

    def test_parameters_updated_after_construction(self):
        test_message = GapcEncryptCfm()
        test_message.parameters.found = 1
        ltk = bytearray.fromhex("4A3A61D591737A9F5A3F9BFE9332D39C")
        ltk.reverse()
        test_message.parameters.ltk.key = (c_uint8 * len(ltk)).from_buffer_copy(ltk)
        test_message.parameters.key_size = 16

        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

    def test_parameters_non_zero_conidx(self):
        test_message = GapcEncryptCfm(conidx=1)
        test_message.parameters.found = 1
        ltk = bytearray.fromhex("4A3A61D591737A9F5A3F9BFE9332D39C")
        ltk.reverse()
        test_message.parameters.ltk.key = (c_uint8 * len(ltk)).from_buffer_copy(ltk)
        test_message.parameters.key_size = 16

        self.assertNotEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

# Table 50
class TestGapcEncryptInd(unittest.TestCase):

    def setUp(self):
        # TODO manual has error in byte string
        self.expected = "05190E10000E00010005"

    def test_parameters_updated_after_construction(self):
        test_message = GapcEncryptInd()
        test_message.parameters.auth = GAP_AUTH.GAP_AUTH_REQ_MITM_BOND

        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

    def test_parameters_non_zero_conidx(self):
        test_message = GapcEncryptInd(conidx=1)
        test_message.parameters.auth = GAP_AUTH.GAP_AUTH_REQ_MITM_BOND

        self.assertNotEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

# Table 60
class TestGapcParamUpdateReqInd(unittest.TestCase):

    def setUp(self):
        self.expected = "050F0E10000E000800270027000000D007"

    def test_parameters_updated_after_construction(self):
        test_message = GapcParamUpdateReqInd()
        test_message.parameters.intv_min = 39 # TODO pass ms and auto convert to intervals? 
        test_message.parameters.intv_max = 39
        test_message.parameters.time_out = 2000

        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

    def test_parameters_non_zero_conidx(self):
        test_message = GapcParamUpdateReqInd(conidx=1)
        test_message.parameters.intv_min = 39 # TODO pass ms and auto convert to intervals? 
        test_message.parameters.intv_max = 39
        test_message.parameters.time_out = 2000

        self.assertNotEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

# Table 62
class TestGapcParamUpdateCfm(unittest.TestCase):

    def setUp(self):
        self.expected = "05100E0E001000060001000000FFFF"

    def test_parameters_updated_after_construction(self):
        test_message = GapcParamUpdateCfm()
        test_message.parameters.accept = 1 # TODO is there an enum for this? 
        test_message.parameters.ce_len_max = 0xFFFF

        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

    def test_parameters_non_zero_conidx(self):
        test_message = GapcParamUpdateCfm(conidx=1)
        test_message.parameters.accept = 1 # TODO is there an enum for this? 
        test_message.parameters.ce_len_max = 0xFFFF

        self.assertNotEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

# Table 64
class TestGapcParamUpdateCmd(unittest.TestCase):

    def setUp(self):
        self.expected = "050E0E0E0010000E0009000A000A000000E803FFFFFFFF"

    def test_parameters_updated_after_construction(self):
        test_message = GapcParamUpdateCmd()
        test_message.parameters.operation = GAPC_OPERATION.GAPC_UPDATE_PARAMS 
        test_message.parameters.intv_min = 10
        test_message.parameters.intv_max = 10
        test_message.parameters.time_out = 1000
        test_message.parameters.ce_len_min = 0xFFFF
        test_message.parameters.ce_len_max = 0xFFFF
        
        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

    def test_parameters_non_zero_conidx(self):
        test_message = GapcParamUpdateCmd(conidx=1)
        test_message.parameters.operation = GAPC_OPERATION.GAPC_UPDATE_PARAMS 
        test_message.parameters.intv_min = 10
        test_message.parameters.intv_max = 10
        test_message.parameters.time_out = 1000
        test_message.parameters.ce_len_min = 0xFFFF
        test_message.parameters.ce_len_max = 0xFFFF

        self.assertNotEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

# Table 67
class TestGapcParamUpdatedInd(unittest.TestCase):

    def setUp(self):
        self.expected = "05110E10000E00060027000000D007"

    def test_parameters_updated_after_construction(self):
        test_message = GapcParamUpdatedInd()
        test_message.parameters.con_interval = 39 
        test_message.parameters.con_latency = 0
        test_message.parameters.sup_to = 2000
        
        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

    def test_parameters_non_zero_conidx(self):
        test_message = GapcParamUpdatedInd(conidx=1)
        test_message.parameters.con_interval = 39 
        test_message.parameters.con_latency = 0
        test_message.parameters.sup_to = 2000

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

# Table 193
class TestGapcDisconnectCmd(unittest.TestCase):

    def setUp(self):
        self.expected = "05040E0E00100002000113"

    def test_parameters_updated_after_construction(self):
        test_message = GapcDisconnectCmd()
        test_message.parameters.reason = CO_ERROR.CO_ERROR_REMOTE_USER_TERM_CON

        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

    def test_parameters_non_zero_conidx(self):
        test_message = GapcDisconnectCmd(conidx=1)
        test_message.parameters.reason = CO_ERROR.CO_ERROR_REMOTE_USER_TERM_CON
        
        self.assertNotEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

# Table 195
class TestGapcDisconnectInd(unittest.TestCase):

    def setUp(self):
        self.expected = "05030E10000E00040000001600"

    def test_parameters_updated_after_construction(self):
        test_message = GapcDisconnectInd()
        test_message.parameters.reason = CO_ERROR.CO_ERROR_CON_TERM_BY_LOCAL_HOST

        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

    def test_parameters_non_zero_conidx(self):
        test_message = GapcDisconnectInd(conidx=1)
        test_message.parameters.reason = CO_ERROR.CO_ERROR_CON_TERM_BY_LOCAL_HOST
        
        self.assertNotEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")
    
# Table 201
class TestGapcGetDevInfoReqInd(unittest.TestCase):

    def setUp(self):
        self.expected = "050A0E10000E00010000"

    def test_parameters_updated_after_construction(self):
        test_message = GapcGetDevInfoReqInd()
        test_message.parameters.req = GAPC_DEV_INFO.GAPC_DEV_NAME

        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

    def test_parameters_non_zero_conidx(self):
        test_message = GapcGetDevInfoReqInd(conidx=1)
        test_message.parameters.req = GAPC_DEV_INFO.GAPC_DEV_NAME
        
        self.assertNotEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")
        
# Table 203
class TestGapcGetDevInfoCfm(unittest.TestCase):

    def setUp(self):
        # TODO believe table is wrong as it includes a null character in the name
        self.expected = "050B0E0E001000260000001C004469616C6F672047544C206F76657220535049484444522044656D6F000000000000"
        
    def test_parameters_updated_after_construction(self):
        test_message = GapcGetDevInfoCfm()
        test_message.parameters.req = GAPC_DEV_INFO.GAPC_DEV_NAME
        name = b"Dialog GTL over SPIHDDR Demo"
        test_message.parameters.info.name.value = (c_uint8 * len(name)).from_buffer_copy(name)

        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

    def test_parameters_non_zero_conidx(self):
        test_message = GapcGetDevInfoCfm(conidx=1)
        test_message.parameters.req = GAPC_DEV_INFO.GAPC_DEV_NAME
        name = b"Dialog GTL over SPIHDDR Demo"
        test_message.parameters.info.name.value = (c_uint8 * len(name)).from_buffer_copy(name)
        
        self.assertNotEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

# Table 253
class TestGapcPeerVersionInd(unittest.TestCase):

    def setUp(self):
        self.expected = "05070E10000E0006000F001A410900"
        
    def test_parameters_updated_after_construction(self):
        test_message = GapcPeerVersionInd()
        test_message.parameters.compid = 0x0F
        test_message.parameters.lmp_subvers = 0x411A
        test_message.parameters.lmp_vers = 0x09

        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

    def test_parameters_non_zero_conidx(self):
        test_message = GapcPeerVersionInd(conidx=1)
        test_message.parameters.compid = 0x0F
        test_message.parameters.lmp_subvers = 0x411A
        test_message.parameters.lmp_vers = 0x09

        self.assertNotEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")
                      

if __name__ == '__main__':
    unittest.main()