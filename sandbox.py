
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


evt = BleEventGattsWriteReq()
evt.conn_idx = 1
evt.handle = 2
evt.offset = 3
evt.value = b"456789"

evt2 = BleEventGapAdvCompleted()
evt2.adv_type = BLE_GAP_CONN_MODE.GAP_CONN_MODE_UNDIRECTED
evt2.status = BLE_ERROR.BLE_ERROR_BUSY

print(evt)
print(evt2)

adv = BleAdvData()

print(adv)