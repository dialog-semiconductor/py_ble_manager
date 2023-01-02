
from ctypes import *
from gtl_messages.gtl_message_gapc import *
from gtl_messages.gtl_message_gapm import *

class Int(Structure):

    _fields_ = [("first_16", c_int, 16),

                ("second_16", c_int, 16)]

x = Int()

print(x)

x = 32

print(x)

list_one = [1,2]
list_two = [1,3]

print(f"lists: {list_one == list_two}")