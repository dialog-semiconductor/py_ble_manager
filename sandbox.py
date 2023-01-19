
from ctypes import *
from gtl_messages.gtl_message_gapc import *
from gtl_messages.gtl_message_gapm import *
from gtl_messages.gtl_message_gattc import *
from gtl_messages.gtl_message_gattm import *
from ble_api.BleGatts import *
from ble_api.BleGap import *
from gtl_port.gapc_task import *
from gtl_port.gattc_task import *
from gtl_port.co_bt import *
from ble_api.BleCommon import *
from manager.BleManagerGattsMsgs import BleMgrGattsGetValueRsp
from services.BleService import *


expected = "050A0C0C0010000E000C01090003000000010000000100"

test_message = GattcWriteCmd()
test_message.parameters.operation =  GATTC_OPERATION.GATTC_WRITE
test_message.parameters.auto_execute = True
test_message.parameters.seq_num = 9
test_message.parameters.handle = 3
value = bytearray.fromhex("01")
test_message.parameters.value = (c_uint8 * len(value)).from_buffer_copy(value)

print(expected)
print(test_message.to_hex())