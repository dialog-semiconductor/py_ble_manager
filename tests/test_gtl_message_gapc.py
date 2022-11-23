import unittest
from ctypes import *
from gtl_messages import *

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

    # TODO for some reason this fails even though 0x0E is the same
    def test_parameters_updated_after_construction(self):
        test_message = GapcGetInfoCmd()
        test_message.parameters.operation = GAPC_OPERATION.GAPC_GET_PEER_FEATURES

        self.assertEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")

    def test_parameters_non_zero_conidx(self):
        test_message = GapcGetInfoCmd(conidx=1)
        test_message.parameters.operation = GAPC_OPERATION.GAPC_GET_PEER_FEATURES
        self.assertNotEqual(test_message.to_hex(), self.expected, f"{type(test_message).__name__}() incorrect byte stream")
              

if __name__ == '__main__':
    unittest.main()