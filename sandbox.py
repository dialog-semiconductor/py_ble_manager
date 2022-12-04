import serial
from ctypes import *
from gtl_messages import *

expected = "05140E0E0010001E00010101000D10020102000000000000000000000000000000000000000000"

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

print(expected)
print(test_message.to_hex())
