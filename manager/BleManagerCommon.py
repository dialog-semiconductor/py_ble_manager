import asyncio
from enum import IntEnum, auto
from manager.GtlWaitQueue import GtlWaitQueue, GtlWaitQueueElement
from gtl_port.gapm_task import GAPM_MSG_ID, GAPM_OPERATION, gapm_reset_cmd
from gtl_messages.gtl_message_gapm import GapmResetCmd
from gtl_messages.gtl_message_base import GtlMessageBase
from ble_api.BleCommon import BLE_ERROR, BleEventBase
from ble_api.BleGap import BLE_CONN_IDX_INVALID


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


class BleMgrMsgBase():
    def __init__(self, opcode) -> None:
        self.opcode = opcode


class BleMgrCommonResetCmd(BleMgrMsgBase):
    def __init__(self) -> None:
        super().__init__(opcode=BLE_MGR_COMMON_CMD_OPCODE.BLE_MGR_COMMON_RESET_CMD)


class BleMgrCommonResetRsp(BleMgrMsgBase):
    def __init__(self, status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED) -> None:
        super().__init__(opcode=BLE_MGR_COMMON_CMD_OPCODE.BLE_MGR_COMMON_RESET_CMD)
        self.status = status


class BleManagerBase():
    def __init__(self,
                 mgr_response_q: asyncio.Queue[BLE_ERROR],
                 mgr_event_q: asyncio.Queue[BleEventBase],
                 adapter_command_q: asyncio.Queue[BleMgrMsgBase],
                 wait_q: GtlWaitQueue) -> None:

        self._mgr_response_q = mgr_response_q
        self._mgr_event_q = mgr_event_q
        self._adapter_command_q = adapter_command_q
        self._wait_q = wait_q
        self.cmd_handlers = {}
        self.evt_handlers = {}

        # TODO would be nice to have dev_params here and all ble managers can access same instance

    def _adapter_command_queue_send(self, command: GtlMessageBase):
        self._adapter_command_q.put_nowait(command)

    async def _mgr_event_queue_get(self) -> BleMgrMsgBase:
        return await self._mgr_event_q.get()

    def _mgr_event_queue_send(self, evt: BleEventBase):
        self._mgr_event_q.put_nowait(evt)

    async def _mgr_response_queue_get(self) -> BleMgrCommonResetCmd:
        return await self._mgr_response_q.get()

    def _mgr_response_queue_send(self, response: BleMgrCommonResetCmd):
        self._mgr_response_q.put_nowait(response)

    def _wait_queue_add(self, conn_idx, msg_id, ext_id, cb, param):
        item = GtlWaitQueueElement(conn_idx=conn_idx, msg_id=msg_id, ext_id=ext_id, cb=cb, param=param)
        self._wait_q.push(item)


# TODO This class name is somewhat confusing given base class. Consider rename, or merge  possibly merge in BleMgrGap
class BleManagerCommon(BleManagerBase):

    def __init__(self,
                 mgr_response_q: asyncio.Queue[BLE_ERROR],
                 mgr_event_q: asyncio.Queue[BleEventBase],
                 adapter_command_q: asyncio.Queue[BleMgrMsgBase],
                 wait_q: GtlWaitQueue) -> None:

        super().__init__(mgr_response_q, mgr_event_q, adapter_command_q, wait_q)

        self.cmd_handlers = {
            BLE_MGR_COMMON_CMD_OPCODE.BLE_MGR_COMMON_RESET_CMD: self.reset_cmd_handler,
        }

    def _create_reset_command(self):
        return GapmResetCmd(gapm_reset_cmd(GAPM_OPERATION.GAPM_RESET))

    def _reset_rsp_handler(self, message: GtlMessageBase, param: None):
        # TODO see ble_adapter_cmp_evt_reset
        # TODO set dev_params status to BLE_IS_ENABLE
        response = BleMgrCommonResetRsp(BLE_ERROR.BLE_STATUS_OK)
        self._mgr_response_queue_send(response)

        # TODO feel like reset belongs under Gap Mgr as it is dealing with GAP messages
    def reset_cmd_handler(self, command: BleMgrCommonResetCmd):
        # TODO set dev_params status to BLE_IS_RESET
        self._wait_queue_add(BLE_CONN_IDX_INVALID, GAPM_MSG_ID.GAPM_CMP_EVT, GAPM_OPERATION.GAPM_RESET, self._reset_rsp_handler, None)
        self._adapter_command_queue_send(self._create_reset_command())


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
