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

# this is from ble_config.h
dg_configBLE_DATA_LENGTH_TX_MAX = (251)


'''
# from ad_ble.h
class ad_ble_operations(IntEnum):
    AD_BLE_OP_CMP_EVT = 0x00
    AD_BLE_OP_INIT_CMD = 0x01
    AD_BLE_OP_RESET_CMD = 0x02
    AD_BLE_OP_LAST = auto()
# end ad_ble.h


# from ble_mgr_ad_msg.c
class WaitQueueElement():
    def __init__(self,
                 rsp_op: ad_ble_operations,
                 cmd_op: ad_ble_operations,
                 cb: callable,
                 param) -> None:
        self.rsp_op = rsp_op
        self.cmd_op = cmd_op
        self.cb = cb
        self.param = param

# end ble_mgr_ad_msg.c
'''


# FROM BLE_COMMON.h
# BLE stack status
class BLE_STATUS(IntEnum):
    BLE_IS_DISABLED = 0x00
    BLE_IS_ENABLED = 0x01
    BLE_IS_BUSY = 0x02
    BLE_IS_RESET = 0x03


# BLE error code
class BLE_ERROR(IntEnum):
    BLE_STATUS_OK = 0x00,    # Success
    BLE_ERROR_FAILED = 0x01,    # Generic failure
    BLE_ERROR_ALREADY_DONE = 0x02,    # Already done
    BLE_ERROR_IN_PROGRESS = 0x03,    # Operation already in progress
    BLE_ERROR_INVALID_PARAM = 0x04,    # Invalid parameter
    BLE_ERROR_NOT_ALLOWED = 0x05,    # Not allowed
    BLE_ERROR_NOT_CONNECTED = 0x06,    # Not connected
    BLE_ERROR_NOT_SUPPORTED = 0x07,    # Not supported
    BLE_ERROR_NOT_ACCEPTED = 0x08,    # Not accepted
    BLE_ERROR_BUSY = 0x09,    # Busy
    BLE_ERROR_TIMEOUT = 0x0A,    # Request timed out
    BLE_ERROR_NOT_SUPPORTED_BY_PEER = 0x0B,    # Not supported by peer
    BLE_ERROR_CANCELED = 0x0C,    # Canceled by user
    BLE_ERROR_ENC_KEY_MISSING = 0x0D,    # encryption key missing
    BLE_ERROR_INS_RESOURCES = 0x0E,    # insufficient resources
    BLE_ERROR_NOT_FOUND = 0x0F,    # not found
    BLE_ERROR_L2CAP_NO_CREDITS = 0x10,    # no credits available on L2CAP CoC
    BLE_ERROR_L2CAP_MTU_EXCEEDED = 0x11,    # MTU exceeded on L2CAP CoC
    BLE_ERROR_INS_BANDWIDTH = 0x12,    # Insufficient bandwidth
    BLE_ERROR_LMP_COLLISION = 0x13,    # LMP collision
    BLE_ERROR_DIFF_TRANS_COLLISION = 0x14,    # Different transaction collision


'''
class ble_mgr_msg_hdr():
    def __init__(self,
                 op_code: c_uint16,  # TODO this should be enum?
                 msg_len: c_uint16,
                 payload: Array[c_uint8]) -> None:
        self.op_code = op_code
        self.msg_len = msg_len
        self.payload = payload
'''


class BLE_MGR_GAP_CMD_CAT(IntEnum):
    BLE_MGR_COMMON_CMD_CAT = 0x00
    BLE_MGR_GAP_CMD_CAT = 0x01
    BLE_MGR_GATTS_CMD_CAT = 0x02
    BLE_MGR_GATTC_CMD_CAT = 0x03
    BLE_MGR_L2CAP_CMD_CAT = 0x04
    BLE_MGR_LAST_CMD_CAT = auto()
# end FROM BLE_COMMON.h


'''
# from ble_mgr_cmd.h
class BLE_MGR_COMMON_CMD_OPCODE(IntEnum):
    BLE_MGR_COMMON_STACK_MSG = BLE_CMD_CAT.BLE_MGR_COMMON_CMD_CAT << 8
    BLE_MGR_COMMON_REGISTER_CMD = auto()
    BLE_MGR_COMMON_ENABLE_CMD = auto()
    BLE_MGR_COMMON_RESET_CMD = auto()
    BLE_MGR_COMMON_READ_TX_POWER_CMD = auto()
    BLE_MGR_COMMON_LAST_CMD = auto()
# end ble_mgr_cmd.h
'''


class BleMgrMsgHeader():
    def __init__(self, opcode) -> None:
        self.opcode = opcode
        # self.msg_len = 0
        # elf.payload = None


# TODO Move to Gap
class BLE_CMD_GAP_OPCODE(IntEnum):
    BLE_MGR_GAP_ADDRESS_SET_CMD = BLE_MGR_GAP_CMD_CAT.BLE_MGR_GAP_CMD_CAT << 8
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


# TODO Move To Gap
class BleMgrGapRoleSetCmd(BleMgrMsgHeader):
    def __init__(self, role: GAP_ROLE = GAP_ROLE.GAP_ROLE_NONE) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ROLE_SET_CMD)
        self.role = role


class BleMgrGapAdvStartCmd(BleMgrMsgHeader):
    def __init__(self, adv_type: GAPM_OPERATION = GAPM_OPERATION.GAPM_ADV_UNDIRECT) -> None:
        super().__init__(opcode=BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ADV_START_CMD)
        self.adv_type = adv_type # TODO raise error on bad arg
'''
class BleMgrCmdFactory():
    @staticmethod
    def create_command(command_type, size):
        if  command_type in BLE_CMD_GAP_OPCODE:
            return BleGapMgrFactory(command_type, size)
'''


class BleManager():

    def __init__(self,
                 app_command_q: asyncio.Queue(),
                 app_response_q: asyncio.Queue(),
                 app_event_q: asyncio.Queue(),
                 adapter_command_q: asyncio.Queue(),
                 adapter_event_q: asyncio.Queue(),
                 event_notif: asyncio.Event()) -> None:

        # TODO if x else y is so vscode will treat variable as that item for auto complete
        self.app_command_q = app_command_q if app_command_q else asyncio.Queue()
        self.app_response_q = app_response_q if app_response_q else asyncio.Queue()
        self.app_event_q = app_event_q if app_event_q else asyncio.Queue()
        self.adapter_commnand_q = adapter_command_q if adapter_command_q else asyncio.Queue()
        self.adapter_event_q = adapter_event_q if adapter_event_q else asyncio.Queue()
        self.event_notif = event_notif if event_notif else asyncio.Event()
        self.wait_q = GtlWaitQueue()
        self.dev_params = BleDevParamsDefault()
        self.ble_stack_initialized = False
        self._reset_signal = asyncio.Event()

    def init(self):

        # TODO keeping handles so these can be cancelled somehow
        self._task = asyncio.create_task(self.manager_task(), name='BleManagerTask')

        print(f"{type(self)} Exiting init")

    async def manager_task(self):
        # TODO any setup needed
        while True:
            await self.event_notif.wait()  # Need to be careful with multiple events happening before switch to this func
            self.event_notif.clear()
            # get an item from the queue
            if not self.adapter_event_q.empty():
                item: GtlMessageBase = self.adapter_event_q.get_nowait()

                if item.parameters.operation == GAPM_OPERATION.GAPM_RESET:
                    self._reset_signal.set()

                if not self.wait_q.match(item):
                    if not self.handle_evt_or_ind(item):
                        pass

            # if item not None:
            print(f"Ble Manager Received event signal {item}")

            # TODO check if more messages in adapter event q

    def handle_evt_or_ind(self, message: GtlMessageBase):

        match message.msg_id:
            case GAPM_MSG_ID.GAPM_CMP_EVT:
                pass
            case GAPC_MSG_ID.GAPC_PARAM_UPDATE_CMD:
                pass
            case GATTC_MSG_ID.GATTC_CMP_EVT:
                pass

        return False

    async def ble_mgr_response_queue_get(self):  # add timeout ?
        return await self.app_response_q.get()

    async def ble_reset(self) -> BLE_ERROR:  # TODO should return error or somethign
        error = BLE_ERROR.BLE_ERROR_FAILED

        self._reset_signal.clear()
        self.adapter_commnand_q.put_nowait(GapmResetCmd(gapm_reset_cmd(GAPM_OPERATION.GAPM_RESET)))
        await self._reset_signal.wait()
        error = BLE_ERROR.BLE_STATUS_OK
        return error

    async def cmd_execute(self, command, handler) -> BLE_ERROR:
        ble_status = self.dev_params.status
        if ble_status == BLE_STATUS.BLE_IS_BUSY or ble_status == BLE_STATUS.BLE_IS_RESET:
            return BLE_ERROR.BLE_ERROR_BUSY

        handler(command)

        #self.adapter_commnand_q.put_nowait(command)

        response = await self.ble_mgr_response_queue_get()

        print(f"Ble. _ble_cmd_execute: command={command}, \
                response={BLE_ERROR(response)}, handler={handler}")
        return response

    def gap_role_set_handler(self, command: BleMgrGapRoleSetCmd):

        print("gap_role_set_handler")

        dev_params_gtl = self.dev_params_to_gtl()
        dev_params_gtl.parameters.role = command.role
        self._wait_queue_add(0xFFFF, GAPM_MSG_ID.GAPM_CMP_EVT, GAPM_OPERATION.GAPM_SET_DEV_CONFIG, self._gapm_set_role_rsp, command.role)
        self.adapter_commnand_q.put_nowait(dev_params_gtl)

    def gap_adv_start_cmd_handler(self, command: BleMgrGapAdvStartCmd):

        response = BLE_ERROR.BLE_ERROR_FAILED
        print("gap_adv_start_cmd_handler")
        # TODO error checks
        # Check if an advertising operation is already in progress
        # Check if length of advertising data is within limits
        self.dev_params.adv_type = command.adv_type
        message = GapmStartAdvertiseCmd()
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
        self.adapter_commnand_q.put_nowait(message)

        response = BLE_ERROR.BLE_STATUS_OK

        self.app_response_q.put_nowait(response)

        print("Exiting gap_adv_start_cmd_handler")

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

    def _wait_queue_add(self, conn_idx, msg_id, ext_id, cb, param):
        item = GtlWaitQueueElement(conn_idx=conn_idx, msg_id=msg_id, ext_id=ext_id, cb=cb, param=param)
        self.wait_q.push(item)

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

    def _task_to_connidx(self, task_id):
        return task_id >> 8
