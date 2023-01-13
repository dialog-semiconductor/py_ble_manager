
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

gtl = GattmAttGetValueRsp()
my_list = [1, 2 ,3,4,5,6,7,8,9,10]
gtl.parameters.value = (c_uint8 * 10)(*my_list)
response = BleMgrGattsGetValueRsp()
max_len = 10
length = min(max_len, gtl.parameters.length)
print(type(response.value))
print(response.value)
response.value = gtl.parameters.value[:length]
print(type(response.value))
print(response.value)
response.value = bytes(gtl.parameters.value[:length])
print(type(response.value))
print(response.value)