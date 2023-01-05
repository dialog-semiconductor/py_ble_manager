
from ctypes import *
from gtl_messages.gtl_message_gapc import *
from gtl_messages.gtl_message_gapm import *

from gtl_port.gapc_task import *

class TestClass():
     def __init__(self) -> None:
        self.value = 10

def test_func(t: TestClass):
    t.value = 20
    print(f"inside func={t.value}")

t = TestClass()
test_func(t)
print (f"outside func={t.value}")