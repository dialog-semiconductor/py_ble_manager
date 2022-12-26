
from gtl_messages.gtl_message_base import GtlMessageBase

from gtl_messages.gtl_message_gapc import GapcConnectionReqInd, GapcConnectionCfm, GapcSecurityCmd, GapcCmpEvt, GapcGetInfoCmd, \
    GapcPeerFeaturesInd, GapcBondReqInd, GapcBondCfm  # noqa: F401
from gtl_messages.gtl_port.gapc_task import GAPC_MSG_ID, gapc_connection_req_ind, gapc_connection_cfm, gapc_security_cmd, gapc_cmp_evt,\
    gapc_get_info_cmd, gapc_peer_features_ind, gapc_bond_req_ind, gapc_bond_cfm, gapc_sign_counter_ind  # noqa: F401

from gtl_messages.gtl_message_gapm import GapmDeviceReadyInd, GapmResetCmd, GapmCmpEvt, GapmSetDevConfigCmd, GapmStartAdvertiseCmd  # noqa: F401
from gtl_messages.gtl_port.gapm_task import GAPM_MSG_ID, GAPM_OPERATION, gapm_reset_cmd, gapm_cmp_evt, gapm_set_dev_config_cmd, \
    gapm_start_advertise_cmd, gapm_start_connection_cmd, GAPM_OWN_ADDR, gapm_adv_info, ADV_CHANNEL_MAP, ADV_DATA_LEN, ADV_FILTER_POLICY,\
    SCAN_RSP_DATA_LEN  # noqa: F401

from gtl_messages.gtl_port.gap import GAP_ROLE, GAP_AUTH, GAP_ADV_MODE, gap_bdaddr  # noqa: F401


class GapBase():
    def __init__(self):
        self.func_table = {}  # Child classes should override this. Best way to make this apparent in python?

    # TODO likely need to pass incoming message, also need to pass conidx
    def handle_message(self, message: GtlMessageBase):

        response = None
        # dict.get() will return None if no key found. Need to pass conidx?
        handler = self.func_table.get(message.msg_id)
        if handler:
            response = handler(message)  # handler is a bound method, does not require passing self explicity
            if not response:
                print(f"{type(self).__name__} unhandled message. message={message}")
        return response


class GapManager(GapBase):

    def default_handler(self, message):
        print(f"{type(self).__name__} default handler")
        return None

    def handle_gapm_device_ready_ind(self, message):
        # Reset the BLE Stack
        return GapmResetCmd(gapm_reset_cmd(GAPM_OPERATION.GAPM_RESET))

    def handle_gapm_cmp_evt(self, message: GapmCmpEvt = None):
        print(f"{type(self).__name__} handle_gapm_cmp_evt")
        response = None
        match message.parameters.operation:
            case GAPM_OPERATION.GAPM_RESET:
                response = self.handle_gapm_reset_cmd()
            case GAPM_OPERATION.GAPM_SET_DEV_CONFIG:
                response = self.handle_gapm_set_dev_config()
        # elif(message.parameters.operation == GAPM_OPERATION.GAPM_ADV_UNDIRECT): GAPM_START_ADVERTISE_CMD
            case _:
                print(f"{type(self).__name__}.handle_gapm_cmp_evt unhandled operation: {str(GAPM_OPERATION(message.parameters.operation))}")
            # Because this is not handled we add a GtlBaseMessage to the queue
            # print("handle_gapm_reset_completion GAPM_SET_DEV_CONFIG")

        return response

    def handle_gapm_reset_cmd(self):
        # response = GapmSetDevConfigCmd()
        # response.parameters.operation = GAPM_OPERATION.GAPM_SET_DEV_CONFIG
        # response.parameters.role = GAP_ROLE.GAP_ROLE_PERIPHERAL
        # response.parameters.att_cfg = 0x20  # TODO setup GAPM_MASK_ATT_SVC_CNG_EN
        # response.parameters.max_mtu = 512
        # response.parameters.max_txoctets = 251
        # response.parameters.max_txtime = 2120
        # return response
        return None  # call back to ble periph?

    def handle_gapm_set_dev_config(self):
        # TODO build databases
        response = None
        '''
        # TODO remove below, just testing to advertise
        response = GapmStartAdvertiseCmd()
        response.parameters.op.code = GAPM_OPERATION.GAPM_ADV_UNDIRECT
        response.parameters.op.addr_src = GAPM_OWN_ADDR.GAPM_STATIC_ADDR
        response.parameters.intv_min = 200  # 0.625 x 200 = 125ms TODO would be nicer to have adv_slots to ms. Should it belong to a class?
        response.parameters.intv_max = 200  # see above
        response.parameters.channel_map = ADV_CHANNEL_MAP.ADV_ALL_CHNLS_EN
        response.parameters.info = gapm_adv_info()
        response.parameters.info.host.mode = GAP_ADV_MODE.GAP_GEN_DISCOVERABLE
        response.parameters.info.host.adv_filt_policy = ADV_FILTER_POLICY.ADV_ALLOW_SCAN_ANY_CON_ANY
        response.parameters.info.host.adv_data_len = 27

        # TODO move this to gapm_task.py def
        adv_data_array = c_uint8 * ADV_DATA_LEN
        # TODO ensure easy to pass name from string
        # complete_local_name = "DialogPER DA14585"
        response.parameters.info.host.adv_data = adv_data_array(0x07, 0x03, 0x03, 0x18, 0x02, 0x18, 0x04, 0x18, 0x12, 0x09, 0x44, 0x69,
                                                                0x61, 0x6c, 0x6f, 0x67, 0x50, 0x45, 0x52, 0x20, 0x44, 0x41, 0x31, 0x34,
                                                                0x35, 0x38, 0x35, 0x00, 0x00, 0x00, 0x00)
        response.parameters.info.host.scan_rsp_data_len = 13
        scan_response_data_array = c_uint8 * SCAN_RSP_DATA_LEN
        response.parameters.info.host.scan_rsp_data = scan_response_data_array(0x0c, 0xff, 0xd2, 0x00, 0x53, 0x61, 0x6d, 0x70, 0x6c, 0x65,
                                                                               0x20, 0x23, 0x31, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                                                               0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                                                               0x00)
        response.parameters.info.host.peer_info = gap_bdaddr()
        '''
        return response

    def __init__(self):
        self.func_table = {
            GAPM_MSG_ID.GAPM_CMP_EVT: self.handle_gapm_cmp_evt,
            GAPM_MSG_ID.GAPM_DEVICE_READY_IND: self.handle_gapm_device_ready_ind,
            GAPM_MSG_ID.GAPM_CANCEL_CMD: self.default_handler,
        }


class GapController(GapBase):
    def default_handler(self, message):
        print(f"{type(self).__name__} default handler")
        return None

    def handle_gapc_cmp_evt(self, message: GapmCmpEvt = None):
        response = None
        # TODO
        return response

    def handle_gapc_connection_req_ind(self, message: GapmCmpEvt = None):
        response = GapcConnectionCfm()
        response.parameters.auth = GAP_AUTH.GAP_AUTH_REQ_NO_MITM_NO_BOND
        response.parameters.svc_changed_ind_enable = 0  # TODO is there an enum for this?

        return response

    def __init__(self):
        self. func_table = {
            GAPC_MSG_ID.GAPC_CMP_EVT: self.handle_gapc_cmp_evt,
            GAPC_MSG_ID.GAPC_CONNECTION_REQ_IND: self.handle_gapc_connection_req_ind,
            GAPC_MSG_ID.GAPC_BOND_CFM: self.default_handler,
        }
