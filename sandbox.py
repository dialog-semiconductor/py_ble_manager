import serial
from ctypes import *
from gtl_messages import *

test_message = GapmStartAdvertiseCmd()
test_message.parameters.op.code = GAPM_OPERATION.GAPM_ADV_UNDIRECT
test_message.parameters.op.addr_src = GAPM_OWN_ADDR.GAPM_STATIC_ADDR
test_message.parameters.intv_min = 200 # 0.625 x 200 = 125ms TODO would be nicer to have adv_slots to ms. Should it belong to a class?
test_message.parameters.intv_max = 200 # see above
test_message.parameters.channel_map = ADV_CHANNEL_MAP.ADV_ALL_CHNLS_EN 
test_message.parameters.info = gapm_adv_info()
test_message.parameters.info.host.mode = GAP_ADV_MODE.GAP_GEN_DISCOVERABLE
test_message.parameters.info.host.adv_filt_policy = ADV_FILTER_POLICY.ADV_ALLOW_SCAN_ANY_CON_ANY
test_message.parameters.info.host.adv_data_len = 27

# TODO move this to gapm_task.py def
adv_data_array = c_uint8*ADV_DATA_LEN
# TODO ensure easy to pass name from string
#complete_local_name = "DialogPER DA14585"
test_message.parameters.info.host.adv_data = adv_data_array(0x07, 0x03, 0x03, 0x18, 0x02, 0x18, 0x04, 0x18, 0x12, 0x09, 0x44, 0x69, 
                                                            0x61, 0x6c, 0x6f, 0x67, 0x50, 0x45, 0x52, 0x20, 0x44, 0x41, 0x31, 0x34,
                                                            0x35, 0x38, 0x35, 0x00, 0x00, 0x00, 0x00)
test_message.parameters.info.host.scan_rsp_data_len = 13
scan_response_data_array = c_uint8*SCAN_RSP_DATA_LEN
test_message.parameters.info.host.scan_rsp_data = scan_response_data_array(0x0c, 0xff, 0xd2, 0x00, 0x53, 0x61, 0x6d, 0x70, 0x6c, 0x65,
                                                                        0x20, 0x23, 0x31, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                                                        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                                                        0x00)
test_message.parameters.info.host.peer_info = gap_bdaddr()     

print(test_message.to_hex())