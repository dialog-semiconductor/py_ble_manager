
from ctypes import *
from gtl_messages.gtl_message_gapc import *
from gtl_messages.gtl_message_gapm import *

from gtl_port.gapc_task import *

test_message = GapcGetDevInfoCfm()
test_message.parameters.req = GAPC_DEV_INFO.GAPC_DEV_NAME
name = b"Dialog GTL over SPIHDDR Demo"
test_message.parameters.info.name.value = (c_uint8 * len(name)).from_buffer_copy(name)

expected = "050B0E0E001000260000001C004469616C6F672047544C206F76657220535049484444522044656D6F000000000000"


print(expected)

print(test_message.to_hex())
print(test_message.parameters.info.name.value)