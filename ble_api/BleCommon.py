import asyncio
from enum import IntEnum, auto
from manager.GtlWaitQueue import GtlWaitQueue, GtlWaitQueueElement
from gtl_messages.gtl_port.gapm_task import GAPM_MSG_ID, GAPM_OPERATION, gapm_reset_cmd
from gtl_messages.gtl_message_gapm import GapmResetCmd
from gtl_messages.gtl_message_base import GtlMessageBase


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


class BLE_MGR_CMD_CAT(IntEnum):
    BLE_MGR_COMMON_CMD_CAT = 0x00
    BLE_MGR_GAP_CMD_CAT = 0x01
    BLE_MGR_GATTS_CMD_CAT = 0x02
    BLE_MGR_GATTC_CMD_CAT = 0x03
    BLE_MGR_L2CAP_CMD_CAT = 0x04
    BLE_MGR_LAST_CMD_CAT = auto()


class BLE_MGR_COMMON_CMD_OPCODE(IntEnum):
    BLE_MGR_COMMON_STACK_MSG = BLE_MGR_CMD_CAT.BLE_MGR_COMMON_CMD_CAT << 8
    BLE_MGR_COMMON_REGISTER_CMD = auto()
    BLE_MGR_COMMON_ENABLE_CMD = auto()
    BLE_MGR_COMMON_RESET_CMD = auto()
    BLE_MGR_COMMON_READ_TX_POWER_CMD = auto()
    # Dummy command opcode, needs to be always defined after all commands
    BLE_MGR_COMMON_LAST_CMD = auto()


BLE_CONN_IDX_INVALID = 0xFFFF


class BleMgrCmdBase():
    def __init__(self, opcode) -> None:
        self.opcode = opcode


class BleMgrCommonResetCmd(BleMgrCmdBase):
    def __init__(self) -> None:
        super().__init__(opcode=BLE_MGR_COMMON_CMD_OPCODE.BLE_MGR_COMMON_RESET_CMD)


# BLE event categories
class BLE_EVT_CAT(IntEnum):
    BLE_EVT_CAT_COMMON = auto()
    BLE_EVT_CAT_GAP = auto()
    BLE_EVT_CAT_GATTS = auto()
    BLE_EVT_CAT_GATTC = auto()
    BLE_EVT_CAT_L2CAP = auto()


# Own Device Address type
class BLE_OWN_ADDR_TYPE(IntEnum):
    PUBLIC_STATIC_ADDRESS = auto()  # Public Static Address
    PRIVATE_STATIC_ADDRESS = auto()  # Private Static Address
    PRIVATE_RANDOM_RESOLVABLE_ADDRESS = auto()  # Private Random Resolvable Address
    PRIVATE_RANDOM_NONRESOLVABLE_ADDRESS = auto()  # Private Random Non-resolvable Address
# if (dg_configBLE_PRIVACY_1_2 == 1)
    PRIVATE_CNTL = auto()  # Private Random Resolvable address using LE privacy v1.2
# endif /* (dg_configBLE_PRIVACY_1_2 == 1) */


# Bluetooth Address type
class BLE_ADDR_TYPE(IntEnum):
    PUBLIC_ADDRESS = 0x00  # Public Static Address
    PRIVATE_ADDRESS = 0x01  # Private Random Address


# Bluetooth Device address
class bd_address():
    # TODO is ctypes array appriopriate at this layer?
    def __init__(self, addr_type: BLE_ADDR_TYPE = BLE_ADDR_TYPE.PUBLIC_ADDRESS, addr: list[int] = None) -> None:
        self.addr_type = addr_type
        # TODO raise error on list len
        self.addr = addr if addr else []


class own_address():
    # TODO is ctypes array appriopriate at this layer?
    def __init__(self, addr_type: BLE_OWN_ADDR_TYPE = BLE_OWN_ADDR_TYPE.PUBLIC_STATIC_ADDRESS, addr: list[int] = None) -> None:
        self.addr_type = addr_type
        # TODO raise error on list len
        self.addr = addr if addr else []


class irk():
    def __init__(self, key: list[int] = None) -> None:  # TODO is ctypes array appriopriate at this layer?
        # TODO raise error on list len
        self.key = key if key else []


class BleEventBase():
    def __init__(self, evt_code) -> None:
        self.evt_code = evt_code


class BleManagerBase():
    def __init__(self,
                 app_response_q: asyncio.Queue[BLE_ERROR],
                 app_event_q: asyncio.Queue[BleEventBase],
                 adapter_command_q: asyncio.Queue[BleMgrCmdBase],
                 wait_q: GtlWaitQueue) -> None:

        self.app_response_q = app_response_q
        self.app_event_q = app_event_q
        self.adapter_command_q = adapter_command_q
        self.wait_q = wait_q
        self.cmd_handlers = {}

        # TODO would be nice to have dev_params here and all ble managers can access same instance

    def _wait_queue_add(self, conn_idx, msg_id, ext_id, cb, param):
        item = GtlWaitQueueElement(conn_idx=conn_idx, msg_id=msg_id, ext_id=ext_id, cb=cb, param=param)
        self.wait_q.push(item)


# TODO This class name is somewhat confusing given base class. Consider rename, or merge with another class
class BleManagerCommon(BleManagerBase):

    def __init__(self,
                 app_response_q: asyncio.Queue[BLE_ERROR],
                 app_event_q: asyncio.Queue[BleEventBase],
                 adapter_command_q: asyncio.Queue[BleMgrCmdBase],
                 wait_q: GtlWaitQueue) -> None:

        super().__init__(app_response_q, app_event_q, adapter_command_q, wait_q)

        self.cmd_handlers = {
            BLE_MGR_COMMON_CMD_OPCODE.BLE_MGR_COMMON_RESET_CMD: self.reset_cmd_handler,
        }

    def _create_reset_command(self):
        return GapmResetCmd(gapm_reset_cmd(GAPM_OPERATION.GAPM_RESET))

    def _reset_rsp_handler(self, message: GtlMessageBase, param: None):
        # TODO see ble_adapter_cmp_evt_reset
        # TODO set dev_params status to BLE_IS_ENABLE
        response = BLE_ERROR.BLE_STATUS_OK
        self.app_response_q.put_nowait(response)

        # TODO feel like reset belongs under Gap Mgr as it is dealing with GAP messages
    def reset_cmd_handler(self, command: BleMgrCommonResetCmd):
        # TODO set dev_params status to BLE_IS_RESET
        self._wait_queue_add(BLE_CONN_IDX_INVALID, GAPM_MSG_ID.GAPM_CMP_EVT, GAPM_OPERATION.GAPM_RESET, self._reset_rsp_handler, None)
        self.adapter_command_q.put_nowait(self._create_reset_command())


'''
static const ble_mgr_cmd_handler_t h_common[BLE_MGR_CMD_GET_IDX(BLE_MGR_COMMON_LAST_CMD)] = {
        ble_mgr_common_stack_msg_handler,
        ble_mgr_common_register_cmd_handler,
#ifndef BLE_STACK_PASSTHROUGH_MODE
        ble_mgr_common_enable_cmd_handler,
        ble_mgr_common_reset_cmd_handler,
        ble_mgr_common_read_tx_power_cmd_handler,
#endif
};
'''
