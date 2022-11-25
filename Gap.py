
import asyncio
import serial_asyncio
from gtl_messages import *

class GapManager():

    def default_handler(self, message):
        print("default handler")
        return None

    def handle_gapm_device_ready_ind(self, message):      
        #print("Received GapmDeviceReadyInd()", message.msg_id)
        return GapmResetCmd(gapm_reset_cmd(GAPM_OPERATION.GAPM_RESET))

    def handle_gapm_cmp_evt(self, message: GapmCmpEvt = None):

        response = GtlMessageBase()
        if(message.parameters.operation == GAPM_OPERATION.GAPM_RESET):
            response = self.handle_gapm_reset_cmd()
        elif(message.parameters.operation == GAPM_OPERATION.GAPM_SET_DEV_CONFIG):
            response = self.handle_gapm_set_dev_config()
            pass
            # Because this is not handled we add a GtlBaseMessage to the queue
            #print("handle_gapm_reset_completion GAPM_SET_DEV_CONFIG")
        
        return response      
        
    def handle_gapm_reset_cmd(self):

        #print("default_gapm_reset_callback")
        response = GapmSetDevConfigCmd()
        response.parameters.operation = GAPM_OPERATION.GAPM_SET_DEV_CONFIG
        response.parameters.role = GAP_ROLE.GAP_ROLE_PERIPHERAL
        response.parameters.att_cfg = 0x20 # TODO setup GAPM_MASK_ATT_SVC_CNG_EN
        response.parameters.max_mtu = 512 
        response.parameters.max_txoctets = 251
        response.parameters.max_txtime = 2120
        return response

    def handle_gapm_set_dev_config(self):
        # TODO build databases

        #TODO remove below, just testing to advertise
        response = GapmStartAdvertiseCmd()
        response.parameters.op.code = GAPM_OPERATION.GAPM_ADV_UNDIRECT
        response.parameters.op.addr_src = GAPM_ADDR_TYPE.GAPM_CFG_ADDR_STATIC
        response.parameters.intv_min = 200 # 0.625 x 200 = 125ms TODO would be nicer to have adv_slots to ms. Should it belong to a class?
        response.parameters.intv_max = 200 # see above
        response.parameters.channel_map = ADV_CHANNEL_MAP.ADV_ALL_CHNLS_EN 
        response.parameters.info = gapm_adv_info()
        response.parameters.info.host.mode = GAP_ADV_MODE.GAP_GEN_DISCOVERABLE
        response.parameters.info.host.adv_filt_policy = ADV_FILTER_POLICY.ADV_ALLOW_SCAN_ANY_CON_ANY
        response.parameters.info.host.adv_data_len = 27

        # TODO move this to gapm_task.py def
        adv_data_array = c_uint8*ADV_DATA_LEN
        # TODO ensure easy to pass name from string
        #complete_local_name = "DialogPER DA14585"
        response.parameters.info.host.adv_data = adv_data_array(0x07, 0x03, 0x03, 0x18, 0x02, 0x18, 0x04, 0x18, 0x12, 0x09, 0x44, 0x69, 
                                                                    0x61, 0x6c, 0x6f, 0x67, 0x50, 0x45, 0x52, 0x20, 0x44, 0x41, 0x31, 0x34,
                                                                    0x35, 0x38, 0x35, 0x00, 0x00, 0x00, 0x00)
        response.parameters.info.host.scan_rsp_data_len = 13
        scan_response_data_array = c_uint8*SCAN_RSP_DATA_LEN
        response.parameters.info.host.scan_rsp_data = scan_response_data_array(0x0c, 0xff, 0xd2, 0x00, 0x53, 0x61, 0x6d, 0x70, 0x6c, 0x65,
                                                                                0x20, 0x23, 0x31, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                                                                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                                                                0x00)
        response.parameters.info.host.peer_info = gap_bdaddr()     
        
        return response


    func_table = {
        GAPM_MSG_ID.GAPM_CMP_EVT: handle_gapm_cmp_evt,
        GAPM_MSG_ID.GAPM_DEVICE_READY_IND: handle_gapm_device_ready_ind,
        GAPM_MSG_ID.GAPM_CANCEL_CMD: default_handler,
    }

    def handle_gap_message(self, message: GtlMessageBase):
        #print("GapManager.handle_gap_message Calling function table")
        #TODO be careful, not clear if you are calling instance func or class method
        response = None
        # dict.get() will return None if no key found
        handler = self.func_table.get(message.msg_id)
        if handler: 
            # TODO func_table is currently a class variable, make instance var?
            response = handler(self, message)
        return response
class GapController():
        pass