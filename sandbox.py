
from ctypes import *
from gtl_messages.gtl_message_gapc import *
from gtl_messages.gtl_message_gapm import *
from gtl_messages.gtl_message_gattc import *
from gtl_messages.gtl_message_gattm import *
from ble_api.BleGatts import *
from gtl_port.gapc_task import *


f = open('messages2.txt', 'r', encoding='utf8')
f2 = open('messages3.txt', 'w', encoding='utf8')

lines = f.readlines()
#print(lines)
#contents = f.read()
#print(contents)
for row in lines:
    text = "Symbolic"
    if row.find(text) != -1:
        print(row)
        x = row.split(" .")
        print(x)
        string = x[0] + '\n'
        f2.write(string)

f.close()
f2.close()
