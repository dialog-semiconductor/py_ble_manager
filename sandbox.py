import serial
from ctypes import *
from gtl_messages import *

expected = "05010E10000E001000000024000000F401000002EE70CAEA80"

test_message = GapcConnectionReqInd()
test_message.parameters = gapc_connection_req_ind()
test_message.parameters.conhdl = 0
test_message.parameters .con_interval = 36 # (36 × 1.25 ms = 45 ms)
test_message.parameters.con_latency = 0
test_message.parameters.sup_to = 500 # (500 x 10 = 5000ms = 5s)
test_message.parameters.clk_accuracy = 0 
test_message.parameters.peer_addr_type = 0 # Public

# TODO need make array type 
bd = c_uint8 * BD_ADDR_LEN


# TODO having to put in this array backwards. Any way to address?
addr = '02EE70CAEA80'
#addr.reverse()
#print(addr)
#memmove(byref(test_message.parameters.peer_addr), ad), sizeof(test_message.parameters.peer_addr))
#test_message.parameters.peer_addr

print(expected == test_message.to_bytes())
print(expected)
print(test_message.to_hex())

next = (c_uint8*BD_ADDR_LEN)( )
for i in next:
    print(i)

gapm_adv_host()