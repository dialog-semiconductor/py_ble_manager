
from ctypes import *
from gtl_messages.gtl_message_gapc import *
from gtl_messages.gtl_message_gapm import *
from gtl_messages.gtl_message_gattc import *
from gtl_messages.gtl_message_gattm import *
from ble_api.BleGatts import *
from gtl_port.gapc_task import *


first  = gapc_connection_cfm()
second = gapc_connection_cfm()

list1 = [1,2,3,4,5,6]
first.lcsrk.key[:6] = (c_uint8 * 6)(*list1)

list2 = [7,8,9,10,11,12]
second.lcsrk.key[:6] = (c_uint8 * 6)(*list2)


print(second.lcsrk.key == first.lcsrk.key)

for i in range(0,6):
    print(f"first[{i}]={first.lcsrk.key[i]}. second[{i}]={second.lcsrk.key[i]}")
