import serial
from ctypes import *
from gtl_messages import *


expected = "05080C0C0010000C000B0216000400050005000200"
test_message = GattcReadCmd()
test_message.parameters.operation = GATTC_OPERATION.GATTC_READ_MULTIPLE
test_message.parameters.seq_num = 0x16
test_message.parameters.req.multiple = (gattc_read_multiple * 2)()
test_message.parameters.req.multiple[0].handle = 4
test_message.parameters.req.multiple[0].len = 5
test_message.parameters.req.multiple[1].handle = 5
test_message.parameters.req.multiple[1].len = 2


print(expected)
print(test_message.to_hex()) #TODO getting a different object when get req.multiple to iterate over
#print(multiple)

print("Hey")