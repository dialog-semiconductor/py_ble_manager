import serial
from ctypes import *
from gtl_messages import *

# Hacked comms Test

ser = serial.Serial('COM13', 115200)  # open serial port
print(ser.name)         # check which port was really used

# -> GAPM_RESET_CMD
# <- GAPM_CMP_EVT(GAPM_REST)

print("Sending GAPM_RESET: ")
cmd = GapmResetCmd(parameters = gapm_reset_cmd(GAPM_OPERATION.GAPM_RESET))
ser.write(cmd.to_bytes())

print("waiting for data")
byte_string = ser.read(11)
print("data received")
print(byte_string.hex()) # GAPM_CMP_EVT: expect 0x05 0x00 0x0D 0x10 0x00 0x0D 0x00 0x02 0x00 0x01 0x

# -> GAM_SET_DEV_CONFIG_CMD
# <- GAPM_CMP_EVT(GAPM_SET_DEV_CONFIG)
print("Sending GAPM_SET_DEV_CONFIG_CMD: ")
cmd = GapmSetDevConfigCmd()
cmd.parameters.operation = GAPM_OPERATION.GAPM_SET_DEV_CONFIG
cmd.parameters.role = GAP_ROLE.GAP_ROLE_PERIPHERAL
cmd.parameters.att_cfg = 0x20 # TODO setup GAPM_MASK_ATT_SVC_CNG_EN
cmd.parameters.max_mtu = 512 
cmd.parameters.max_txoctets = 251
cmd.parameters.max_txtime = 2120
print(cmd.to_hex())
ser.write(cmd.to_bytes())

print("waiting for data")
new_string = ser.read(11)
print("data received")
print(new_string.hex()) #GAPM_CMP_EVT: expect 0x05 0x00 0x0D 0x10 0x00 0x0D 0x00 0x02 0x00 0x03 0x0

# TODO Could add diss here for test

'''
add_diss_cmd = bytes.fromhex('051B0D0D0010000E001B04140010000000730100000000')
print("Sending GAPM_PROFILE_TASK_ADD_CMD for DISS: ")
print(add_diss_cmd.hex())
ser.write(add_diss_cmd)

print("waiting for data")
new_string = ser.read(15)
print("data received")
print(new_string.hex()) #GAPM_PROFILE_ADDED_IND : expect 05 1C 0D 10 00 0D 00 06 00 14 00 14 00 0A 00
'''

cmd = GapmStartAdvertiseCmd()
cmd = GapmStartAdvertiseCmd(gapm_start_advertise_cmd())
cmd.parameters.op.code = GAPM_OPERATION.GAPM_ADV_UNDIRECT
cmd.parameters.op.addr_src = GAPM_ADDR_TYPE.GAPM_CFG_ADDR_STATIC
cmd.parameters.intv_min = 200 # 0.625 x 200 = 125ms TODO would be nicer to have adv_slots to ms. Should it belong to a class?
cmd.parameters.intv_max = 200 # see above
cmd.parameters.channel_map = ADV_CHANNEL_MAP.ADV_ALL_CHNLS_EN 
cmd.parameters.info = gapm_adv_info()
cmd.parameters.info.host.mode = GAP_ADV_MODE.GAP_GEN_DISCOVERABLE
cmd.parameters.info.host.adv_filt_policy = ADV_FILTER_POLICY.ADV_ALLOW_SCAN_ANY_CON_ANY
cmd.parameters.info.host.adv_data_len = 27

# TODO move this to gapm_task.py def
adv_data_array = c_uint8*ADV_DATA_LEN
# TODO ensure easy to pass name from strin 
#complete_local_name = "DialogPER DA14585"
cmd.parameters.info.host.adv_data = adv_data_array(0x07, 0x03, 0x03, 0x18, 0x02, 0x18, 0x04, 0x18, 0x12, 0x09, 0x44, 0x69, 
                                                            0x61, 0x6c, 0x6f, 0x67, 0x50, 0x45, 0x52, 0x20, 0x44, 0x41, 0x31, 0x34,
                                                            0x35, 0x38, 0x35, 0x00, 0x00, 0x00, 0x00)
cmd.parameters.info.host.scan_rsp_data_len = 13
scan_response_data_array = c_uint8*SCAN_RSP_DATA_LEN
cmd.parameters.info.host.scan_rsp_data = scan_response_data_array(0x0c, 0xff, 0xd2, 0x00, 0x53, 0x61, 0x6d, 0x70, 0x6c, 0x65,
                                                                           0x20, 0x23, 0x31, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                                                           0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                                                           0x00)
cmd.parameters.info.host.peer_info = gap_bdaddr()   
print("Sending GAPM_START_ADVERTISE_CMD: ")
print(cmd.to_hex())
ser.write(cmd.to_bytes())

print("waiting for data") # waiting to connect
new_string = ser.read(25)
print("data received")
print(new_string.hex()) #GAPC_CONNECTION_REQ_IND  : expect 05 1C 0D 10 00 0D 00 06 00 14 00 14 00 0A 00

GAPC_CONNECTION_CFM = bytes.fromhex('05020E0E0010002C000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000')
print("Sending GAPC_CONNECTION_CFM: ")
print(GAPC_CONNECTION_CFM.hex())
ser.write(GAPC_CONNECTION_CFM)

ser.close()             # close port

'''
ser.timeout = 20.0
print("waiting for data") # waiting to connect
new_string = ser.read(25)
print("data received")
print(new_string.hex())

ser.close()             # close port
'''
