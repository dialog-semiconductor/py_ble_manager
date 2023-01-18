
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
from services.BleService import *


char = GattCharacteristicDef()

char.char_def.prop = GATT_PROP.GATT_PROP_READ | GATT_PROP.GATT_PROP_WRITE
char.char_def.perm = ATT_PERM.ATT_PERM_RW
char.char_def.max_len = 2
char.char_def.flags = GATTS_FLAGS.GATTS_FLAG_CHAR_READ_REQ

print(GATT_PROP.GATT_PROP_READ)
print(GATT_PROP.GATT_PROP_WRITE)
print(GATT_PROP(char.char_def.prop))
