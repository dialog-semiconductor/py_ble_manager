import serial
from ctypes import *
from gtl_messages import *

expected = bytes.fromhex("05000D10000D0002000100")

test1 = GapmCmpEvt(gapm_cmp_evt(GAPM_OPERATION.GAPM_RESET, HOST_STACK_ERROR_CODE.GAP_ERR_NO_ERROR))

print(expected)

print(len(expected))
params = expected[9:]

print(params)

built = gapm_cmp_evt.from_buffer_copy(params)
test2 = GapmCmpEvt()
test2.parameters = built

print("Expected: ", expected)
print("test1: ", test1.to_bytes())
print("test2: ", test2.to_bytes())


test3 = GapmCmpEvt()
print(sizeof(test3.parameters))
memmove(pointer(test3.parameters), expected[9:], sizeof(test3.parameters))
print("test3: ", test3.to_bytes())

#def receiveSome(self, bytes):
#    fit = min(len(bytes), ctypes.sizeof(self))
#    ctypes.memmove(ctypes.addressof(self), bytes, fit)