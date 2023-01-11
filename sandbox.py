
from ctypes import *
from gtl_messages.gtl_message_gapc import *
from gtl_messages.gtl_message_gapm import *
from gtl_messages.gtl_message_gattc import *
from gtl_messages.gtl_message_gattm import *
from ble_api.BleGatts import *
from gtl_port.gapc_task import *
from gtl_port.gattc_task import *


class Test():
    def __init__(self):
        self.first = 0
        self.second = 0
        self.third = 0

        self.handles = [self.first, self.second, self.third]

    def update_handles(self):
        self.handles[0] = 1
        self.handles[1] = 2
        self.handles[2] = 3
    
test = Test()

test.update_handles()
print(test.handles)
print(test.first)
print(test.second)
print(test.third)