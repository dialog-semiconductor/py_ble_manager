
from ctypes import *
from gtl_messages.gtl_message_gapc import *
from gtl_messages.gtl_message_gapm import *
from gtl_messages.gtl_message_gattc import *
from ble_api.BleGatts import *
from gtl_port.gapc_task import *


test_message = GattcWriteReqInd(conidx=1)
test_message.parameters.handle = 0x0B
value = bytearray.fromhex("06")
test_message.parameters.value = (c_uint8 * len(value)).from_buffer_copy(value)

print(test_message.to_bytes())
other = BleEventGattsWriteReq()
other.value = bytes(test_message.parameters.value)
print(other.value)