from gtl_messages.gtl_message_gapm import *
from gtl_port.gapm_task import *
from gtl_port.co_bt import *

expected = "05140D0D00100018001701BD74EB757E59872FF3AC0D0428EB37B5B6CC9E5AE867"
        

test_message = GapmResolvAddrCmd()

addr_string = bytearray.fromhex('597E75EB74BD')  # TODO manual has different addr in comments vs hex
addr_string.reverse()
test_message.parameters.addr.addr = (c_uint8 * BD_ADDR_LEN).from_buffer_copy(addr_string)

irk_string = bytearray.fromhex('67E85A9ECCB6B537EB28040DACF32F87')
irk_string.reverse()
print(bytes(test_message.parameters.irk[0].key).hex())



test_message.parameters.irk[0].key = (c_uint8 * KEY_LEN).from_buffer_copy(irk_string)

print(bytes(test_message.parameters.irk[0].key).hex())
print(irk_string.hex())
print(expected)
print(test_message.to_hex())