
from ctypes import *
from gtl_messages.gtl_message_gapc import *
from gtl_messages.gtl_message_gapm import *
from gtl_messages.gtl_message_gattc import *
from gtl_messages.gtl_message_gattm import *
from ble_api.BleGatts import *
from gtl_port.gapc_task import *
from gtl_port.gattc_task import *
from gtl_port.co_bt import *

expected = "05100D10000D00290000001BA070CAEA801B0201061107B75C49D204A34071A0B535853EB08307050978494F5400000000BD"
        
test_message = GapmAdvReportInd()
test_message.parameters.report.adv_addr_type = BD_ADDRESS_TYPE.ADDR_PUBLIC
addr_string = bytearray.fromhex('80EACA70A01B')
addr_string.reverse()
test_message.parameters.report.adv_addr.addr[:] = addr_string
data_string = bytearray.fromhex('0201061107B75C49D204A34071A0B535853EB08307050978494F54')
test_message.parameters.report.data = data_string 
test_message.parameters.report.rssi = 0xBD


print(expected)
print(test_message.to_hex())