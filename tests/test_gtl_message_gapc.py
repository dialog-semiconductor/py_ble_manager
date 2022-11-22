import unittest
from ctypes import *
from gtl_messages import *

# Table 13
class TestGapcConnectionReqInd(unittest.TestCase):

    def setUp(self):
        self.expected = bytes.fromhex("05010E10000E001000000024000000F401000002EE70CAEA80")
        self.message_type = type(GapcConnectionReqInd()).__name__
        
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

        self.assertEqual(test_message.to_bytes(), self.expected, "{0}() incorrect byte stream".format(self.message_type ))

# Table 16
class TestGapcConnectionCfm(unittest.TestCase):

    def setUp(self):
        self.expected = "05020E0E0010002C000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
        self.message_type = type(GapcConnectionCfm()).__name__

    def test_parameters_updated_after_construction(self):
        test_message = GapcConnectionCfm()

        self.assertEqual(test_message.to_hex(), self.expected, "{0}() incorrect byte stream".format(self.message_type ))

# Table 18
class TestGapcSecurityCmd(unittest.TestCase):

    def setUp(self):
        self.expected = "051A0E0E00100002000C0D"
        self.message_type = type(GapcSecurityCmd()).__name__

    def test_parameters_updated_after_construction(self):
        test_message = GapcSecurityCmd()
        test_message.parameters.operation = GAPC_OPERATION.GAPC_SECURITY_REQ
        test_message.parameters.auth = GAP_AUTH.GAP_AUTH_REQ_SECURE_CONNECTION | GAP_AUTH.GAP_AUTH_REQ_MITM_BOND

        self.assertEqual(test_message.to_hex(), self.expected, "{0}() incorrect byte stream".format(self.message_type ))


                                                

if __name__ == '__main__':
    unittest.main()