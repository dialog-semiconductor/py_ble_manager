import serial
from ctypes import *
from gtl_messages import *


expected = "05090C10000C001801030000001201" + \
                        "566572794C6F6E6756657279" + \
                        "4C6F6E67566572794C6F6E67" + \
                        "566572794C6F6E6756657279" + \
                        "4C6F6E67566572794C6F6E67" + \
                        "566572794C6F6E674469616C" + \
                        "6F67566572794C6F6E675665" + \
                        "72794C6F6E67566572794C6F" + \
                        "6E67566572794C6F6E675665" + \
                        "72794C6F6E67566572794C6F" + \
                        "6E67566572794C6F6E675665" + \
                        "72794C6F6E67566572794C6F" + \
                        "6E67566572794C6F6E675665" + \
                        "72794C6F6E67566572794C6F" + \
                        "6E67566572794C6F6E675665" + \
                        "72794C6F6E67566572794C6F" + \
                        "6E67566572794C6F6E675665" + \
                        "72794C6F6E67566572794C6F" + \
                        "6E67566572794C6F6E675665" + \
                        "72794C6F6E67566572794C6F" + \
                        "6E67566572794C6F6E675665" + \
                        "72794C6F6E67566572794C6F" + \
                        "6E67566572794C6F6E672048" + \
                        "6F475020446576696365"
test_message = GattcReadInd()
test_message = GattcReadInd()
test_message.parameters.handle = 4
value_str = "VeryLongVeryLongVer" + \
        "yLongVeryLongVeryLo" + \
        "ngVeryLongVeryLongD" + \
        "ialogVeryLongVeryLon" + \
        "gVeryLongVeryLongVe" + \
        "ryLongVeryLongVeryLo" + \
        "ngVeryLongVeryLongV" + \
        "eryLongVeryLongVeryL" + \
        "ongVeryLongVeryLong" + \
        "VeryLongVeryLongVer" + \
        "yLongVeryLongVeryLo" + \
        "ngVeryLongVeryLongV" + \
        "eryLongVeryLongVeryL" + \
        "ongVeryLong HoGP " + \
        "Device"
value = bytearray(value_str, 'utf-8')
test_message.parameters.value = (c_uint8 * len(value)).from_buffer_copy(value)

print(expected)
print(test_message.to_hex()) #TODO getting a different object when get req.multiple to iterate over
#print(multiple)

print("Hey")