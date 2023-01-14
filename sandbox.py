
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

tpye = b'\x02\x01\x06\x1b\xffL\x00\x0c\x0e\x00\xce\xf5\xbedFV|\x97z\xa3Iz\xaa\x10\x06G\x1d\xa3b\x98h'

print(len(tpye))
print(tpye.hex())

response.value = gtl.parameters.value[:]

print(type(response.value))
print(response.value)


response.value = bytes(gtl.parameters.value[:])

print(type(response.value))
print(response.value)
print(list(response.value))

byte_str = b'\x01\x02\x03\x04\x05\x06\x07\x08\t\n'
list_str = [1, 2 ,3,4,5,6,7,8,9,10]

gtl.parameters.value[:] = my_list

my_str = ""
for i in gtl.parameters.value:
    my_str += f"{i} "
print(my_str)
print(gtl.parameters.value)

gtl.parameters.value[:] = byte_str

my_str = ""
for i in gtl.parameters.value:
    my_str += f"{i} "
print(my_str)
print(gtl.parameters.value)

periph_bd = BdAddress(BLE_ADDR_TYPE.PUBLIC_ADDRESS, bytes.fromhex("482335001B53"))  # [72, 35, 53, 0, 27, 83]
print(periph_bd)
