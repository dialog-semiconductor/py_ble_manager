
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

uuid_str = "7c37cbdc-12a2-11ed-861d-0242ac120002"
uuid_str = uuid_str.replace("-", "")

print(uuid_str)
uuid_list = [int(uuid_str[idx:idx + 2], 16) for idx in range(0, len(uuid_str), 2)]
print(uuid_list)


