
from ctypes import *
from gtl_messages.gtl_message_gapc import *
from gtl_messages.gtl_message_gapm import *
from gtl_messages.gtl_message_gattc import *
from gtl_messages.gtl_message_gattm import *
from ble_api.BleGatts import *
from gtl_port.gapc_task import *
from gtl_port.gattc_task import *

expected = "051A0C10000C00580002011800000000000000000000000000000006000900022008000000000000000000000000000000000000000302052A00000000000000000000000000000000000004020229000000000000000000000000000000000000"

test_message = GattcSdpSvcInd()
uuid = bytes.fromhex("0118")
test_message.parameters.uuid = (c_uint8 * len(uuid)).from_buffer_copy(uuid)
test_message.parameters.start_hdl = 6
test_message.parameters.end_hdl = 9

info_list = []
info = gattc_sdp_att_info()
info.att_type = GATTC_SDP_ATT_TYPE.GATTC_SDP_ATT_CHAR
info.att_char.prop = 0x20
info.att_char.handle = 0x0008    
info_list.append(info)

info = gattc_sdp_att_info()
info.att_type = GATTC_SDP_ATT_TYPE.GATTC_SDP_ATT_VAL
uuid = bytes.fromhex("052A")
info.att.uuid = (c_uint8 * len(uuid)).from_buffer_copy(uuid)   
info_list.append(info)

info = gattc_sdp_att_info()
info.att_type = GATTC_SDP_ATT_TYPE.GATTC_SDP_ATT_DESC
info == GATTC_SDP_ATT_TYPE.GATTC_SDP_ATT_DESC
uuid = bytes.fromhex("0229")
info.att.uuid = (c_uint8 * len(uuid)).from_buffer_copy(uuid)  
info_list.append(info)


test_message.parameters.info = (gattc_sdp_att_info * len(info_list))(*info_list)

print(expected)
print(test_message.to_hex())