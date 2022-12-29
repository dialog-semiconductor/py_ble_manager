import asyncio
from ctypes import c_uint16, c_uint8, Array
from enum import IntEnum, auto
from gtl_messages.gtl_message_base import GtlMessageBase
from gtl_messages.gtl_message_gapm import GapmResetCmd, GapmSetDevConfigCmd, GapmStartAdvertiseCmd

# TODO perhaps these Gapm messages do not belong here
from gtl_messages.gtl_port.gapm_task import GAPM_MSG_ID, gapm_reset_cmd, gapm_cmp_evt, GAPM_OPERATION, gapm_set_dev_config_cmd
from gtl_messages.gtl_port.gapc_task import GAPC_MSG_ID
from gtl_messages.gtl_port.gattc_task import GATTC_MSG_ID
from gtl_messages.gtl_port.gap import GAP_ROLE
from BleDevParams import BleDevParamsDefault
from gtl_messages.gtl_port.rwble_hl_error import HOST_STACK_ERROR_CODE
from GtlWaitQueue import GtlWaitQueue, GtlWaitQueueElement
from BleCommon import BLE_ERROR, BLE_STATUS, BLE_MGR_CMD_CAT


# this is from ble_config.h
dg_configBLE_DATA_LENGTH_TX_MAX = (251)


# TODO move header to common
class BleMgrMsgHeader():
    def __init__(self, opcode) -> None:
        self.opcode = opcode


class BleMgrGapRoleSetCmd(BleMgrMsgHeader):
    def __init__(self, role: GAP_ROLE = GAP_ROLE.GAP_ROLE_NONE) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ROLE_SET_CMD)
        self.role = role


class BleMgrGapAdvStartCmd(BleMgrMsgHeader):
    def __init__(self, adv_type: GAPM_OPERATION = GAPM_OPERATION.GAPM_ADV_UNDIRECT) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ADV_START_CMD)
        self.adv_type = adv_type  # TODO raise error on bad arg


class BLE_CMD_GAP_OPCODE(IntEnum):
    BLE_MGR_GAP_ADDRESS_SET_CMD = BLE_MGR_CMD_CAT.BLE_MGR_GAP_CMD_CAT << 8
    BLE_MGR_GAP_DEVICE_NAME_SET_CMD = auto()
    BLE_MGR_GAP_APPEARANCE_SET_CMD = auto()
    BLE_MGR_GAP_PPCP_SET_CMD = auto()
    BLE_MGR_GAP_ADV_START_CMD = auto()
    BLE_MGR_GAP_ADV_STOP_CMD = auto()
    BLE_MGR_GAP_ADV_DATA_SET_CMD = auto()
    BLE_MGR_GAP_ADV_SET_PERMUTATION_CMD = auto()
    BLE_MGR_GAP_SCAN_START_CMD = auto()
    BLE_MGR_GAP_SCAN_STOP_CMD = auto()
    BLE_MGR_GAP_CONNECT_CMD = auto()
    BLE_MGR_GAP_CONNECT_CANCEL_CMD = auto()
    BLE_MGR_GAP_DISCONNECT_CMD = auto()
    BLE_MGR_GAP_PEER_VERSION_GET_CMD = auto()
    BLE_MGR_GAP_PEER_FEATURES_GET_CMD = auto()
    BLE_MGR_GAP_CONN_RSSI_GET_CMD = auto()
    BLE_MGR_GAP_ROLE_SET_CMD = auto()
    BLE_MGR_GAP_MTU_SIZE_SET_CMD = auto()
    BLE_MGR_GAP_CHANNEL_MAP_SET_CMD = auto()
    BLE_MGR_GAP_CONN_PARAM_UPDATE_CMD = auto()
    BLE_MGR_GAP_CONN_PARAM_UPDATE_REPLY_CMD = auto()
    BLE_MGR_GAP_PAIR_CMD = auto()
    BLE_MGR_GAP_PAIR_REPLY_CMD = auto()
    BLE_MGR_GAP_PASSKEY_REPLY_CMD = auto()
    BLE_MGR_GAP_UNPAIR_CMD = auto()
    BLE_MGR_GAP_SET_SEC_LEVEL_CMD = auto()
# if (dg_configBLE_SKIP_LATENCY_API == 1) # TODO need to handle these defines
    BLE_MGR_GAP_SKIP_LATENCY_CMD = auto()
# endif /* (dg_configBLE_SKIP_LATENCY_API == 1) */
    BLE_MGR_GAP_DATA_LENGTH_SET_CMD = auto()
# if (dg_configBLE_SECURE_CONNECTIONS == 1)
    BLE_MGR_GAP_NUMERIC_REPLY_CMD = auto()
# endif /* (dg_configBLE_SECURE_CONNECTIONS == 1) */
    BLE_MGR_GAP_ADDRESS_RESOLVE_CMD = auto()
# if (dg_configBLE_2MBIT_PHY == 1)
    BLE_MGR_GAP_PHY_SET_CMD = auto()
# endif /* (dg_configBLE_2MBIT_PHY == 1) */
    BLE_MGR_GAP_TX_POWER_SET_CMD = auto()
    BLE_MGR_GAP_CONN_TX_POWER_SET_CMD = auto()
    BLE_MGR_GAP_LOCAL_TX_POWER_GET_CMD = auto()
    BLE_MGR_GAP_REMOTE_TX_POWER_GET_CMD = auto()
    BLE_MGR_GAP_PATH_LOSS_REPORT_PARAMS_SET_CMD = auto()
    BLE_MGR_GAP_PATH_LOSS_REPORT_EN_CMD = auto()
    BLE_MGR_GAP_TX_PWR_REPORT_EN_CMD = auto()
    BLE_MGR_GAP_RF_PATH_COMPENSATION_SET_CMD = auto()
    # Dummy command opcode = auto() needs to be always defined after all commands
    BLE_MGR_GAP_LAST_CMD = auto()


class BleSubManager():
    def __init__(self,
                 adapter_command_q: asyncio.Queue(),
                 app_response_q: asyncio.Queue(),
                 mgr_wait_q: GtlWaitQueue()) -> None:

        self.adapter_command_q = adapter_command_q if adapter_command_q else asyncio.Queue()
        self.app_response_q = app_response_q if app_response_q else asyncio.Queue()
        self.mgr_wait_q = mgr_wait_q if mgr_wait_q else GtlWaitQueue()
        self.handlers = {}

    def _wait_queue_add(self, conn_idx, msg_id, ext_id, cb, param):
        item = GtlWaitQueueElement(conn_idx=conn_idx, msg_id=msg_id, ext_id=ext_id, cb=cb, param=param)
        self.mgr_wait_q.push(item)


class BleManagerGap(BleSubManager):

    def __init__(self,
                 adapter_command_q: asyncio.Queue(),
                 app_response_q: asyncio.Queue(),
                 mgr_wait_q: GtlWaitQueue()) -> None:

        super().__init__(adapter_command_q, app_response_q, mgr_wait_q)
        self.dev_params = BleDevParamsDefault()

        self.handlers = {
            BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ROLE_SET_CMD: self.gap_role_set_handler,
            BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ADV_START_CMD: self.gap_adv_start_cmd_handler
        }

    def gap_role_set_handler(self, command: BleMgrGapRoleSetCmd):

        print("gap_role_set_handler")

        dev_params_gtl = self.dev_params_to_gtl()
        # TODO getting error at role
        dev_params_gtl.parameters.role = command.role
        self._wait_queue_add(0xFFFF, GAPM_MSG_ID.GAPM_CMP_EVT, GAPM_OPERATION.GAPM_SET_DEV_CONFIG, self._gapm_set_role_rsp, command.role)
        self.adapter_command_q.put_nowait(dev_params_gtl)

    def _gapm_set_role_rsp(self, message: GtlMessageBase, param: GAP_ROLE = GAP_ROLE.GAP_ROLE_NONE):
        print("_gapm_set_role_rsp")
        event: gapm_cmp_evt = message.parameters
        response = BLE_ERROR.BLE_ERROR_FAILED

        # TODO do we need separate BLE ERROR enum at all?
        match event.status:
            case HOST_STACK_ERROR_CODE.GAP_ERR_NO_ERROR:
                self.dev_params.role = param
                response = BLE_ERROR.BLE_STATUS_OK
            case HOST_STACK_ERROR_CODE.GAP_ERR_INVALID_PARAM:
                response = BLE_ERROR.BLE_ERROR_INVALID_PARAM
            case HOST_STACK_ERROR_CODE.GAP_ERR_NOT_SUPPORTED:
                response = BLE_ERROR.BLE_ERROR_NOT_ALLOWED
            case HOST_STACK_ERROR_CODE.GAP_ERR_COMMAND_DISALLOWED:
                response = BLE_ERROR.BLE_ERROR_NOT_ALLOWED
            case _:
                response = event.status

        self.app_response_q.put_nowait(response)

    def gap_adv_start_cmd_handler(self, command: BleMgrGapAdvStartCmd):

        response = BLE_ERROR.BLE_ERROR_FAILED
        print("gap_adv_start_cmd_handler")
        # TODO error checks
        # Check if an advertising operation is already in progress
        # Check if length of advertising data is within limits
        self.dev_params.adv_type = command.adv_type
        message = GapmStartAdvertiseCmd()
        # TODO error at setting opcode
        message.parameters.op.code = command.adv_type
        message.parameters.op.addr_src = self.dev_params.own_addr.addr_type
        message.parameters.intv_min = self.dev_params.adv_intv_min
        message.parameters.intv_max = self.dev_params.adv_intv_max
        message.parameters.channel_map = self.dev_params.adv_channel_map

        if command.adv_type < GAPM_OPERATION.GAPM_ADV_DIRECT:  # TODO VERIFY THIS IS THE SAME
            message.parameters.info.host.mode = self.dev_params.adv_mode
            message.parameters.info.host.adv_filt_policy = self.dev_params.adv_filter_policy
            message.parameters.info.host.adv_data_len = self.dev_params.adv_data_length
            adv_len = self.dev_params.adv_data_length
            message.parameters.info.host.adv_data[:adv_len] = self.dev_params.adv_data[:adv_len]

            # TODO add scan response.
        else:
            # TODO fill in for Directed adv more
            pass

        self.dev_params.advertising = True
        self.adapter_command_q.put_nowait(message)

        response = BLE_ERROR.BLE_STATUS_OK

        self.app_response_q.put_nowait(response)

        print("Exiting gap_adv_start_cmd_handler")

    def dev_params_to_gtl(self) -> GapmSetDevConfigCmd:
        gtl = GapmSetDevConfigCmd()
        gtl.parameters.role = self.dev_params.role  # TODO sdk has a function for this
        gtl.parameters.renew_dur = self.dev_params.addr_renew_duration
        gtl.parameters.att_cfg = self.dev_params.att_db_cfg
        gtl.parameters.max_mtu = self.dev_params.mtu_size
        gtl.parameters.max_mps = self.dev_params.mtu_size
        gtl.parameters.addr.addr[:] = self.dev_params.own_addr.addr.addr
        # TODO switch on dev_params.addr_type
        gtl.parameters.addr_type = self.dev_params.own_addr.addr_type
        gtl.parameters.irk.key[:] = self.dev_params.irk.key
        gtl.parameters.max_txoctets = dg_configBLE_DATA_LENGTH_TX_MAX
        gtl.parameters.max_txtime = (dg_configBLE_DATA_LENGTH_TX_MAX + 11 + 3) * 8

        return gtl
