import asyncio
# from ctypes import c_uint16, c_uint8, Array
# from enum import IntEnum, auto
from gtl_messages.gtl_message_base import GtlMessageBase
# from gtl_messages.gtl_message_gapm import GapmResetCmd, GapmSetDevConfigCmd, GapmStartAdvertiseCmd

# from gtl_messages.gtl_port.rwble_hl_error import HOST_STACK_ERROR_CODE
from .GtlWaitQueue import GtlWaitQueue  # , GtlWaitQueueElement
from ble_api.BleCommon import BLE_ERROR, BLE_STATUS, BleEventBase
from .BleManagerCommon import BLE_MGR_CMD_CAT, BleManagerBase, BleManagerCommon, BleMgrMsgBase
from .BleManagerGap import BleManagerGap   # , BleMgrGapRoleSetCmd, BLE_CMD_GAP_OPCODE
from .BleManagerGatts import BleManagerGatts
# this is from ble_config.h
dg_configBLE_DATA_LENGTH_TX_MAX = (251)


class BleManager(BleManagerBase):

    def __init__(self,
                 mgr_command_q: asyncio.Queue[BleMgrMsgBase],
                 mgr_response_q: asyncio.Queue[BLE_ERROR],
                 mgr_event_q: asyncio.Queue[BleEventBase],
                 adapter_command_q: asyncio.Queue[BleMgrMsgBase],
                 adapter_event_q: asyncio.Queue[GtlMessageBase]) -> None:

        # TODO if x else y is so vscode will treat variable as that item for auto complete
        self._mgr_command_q: asyncio.Queue[BleMgrMsgBase] = mgr_command_q
        self._mgr_response_q: asyncio.Queue[BLE_ERROR] = mgr_response_q
        self._mgr_event_q: asyncio.Queue = mgr_event_q
        self._adapter_commnand_q: asyncio.Queue[GtlMessageBase] = adapter_command_q
        self._adapter_event_q: asyncio.Queue[GtlMessageBase] = adapter_event_q
        self._wait_q = GtlWaitQueue()
        self._ble_stack_initialized = False
        self.gap_mgr = BleManagerGap(self._mgr_response_q, self._mgr_event_q, self._adapter_commnand_q, self._wait_q)
        self.common_mgr = BleManagerCommon(self._mgr_response_q, self._mgr_event_q, self._adapter_commnand_q, self._wait_q)
        self.gatts_mgr = BleManagerGatts(self._mgr_response_q, self._mgr_event_q, self._adapter_commnand_q, self._wait_q)

        self.cmd_handlers = {
            BLE_MGR_CMD_CAT.BLE_MGR_COMMON_CMD_CAT: self.common_mgr,
            BLE_MGR_CMD_CAT.BLE_MGR_GAP_CMD_CAT: self.gap_mgr,
            BLE_MGR_CMD_CAT.BLE_MGR_GATTS_CMD_CAT: self.gatts_mgr,
            BLE_MGR_CMD_CAT.BLE_MGR_GATTC_CMD_CAT: None,
            BLE_MGR_CMD_CAT.BLE_MGR_L2CAP_CMD_CAT: None,
        }

    async def _adapter_event_queue_get(self) -> BleEventBase:
        return await self._adapter_event_q.get()

    def _mgr_command_queue_send(self, command: BleMgrMsgBase):
        self._mgr_command_q.put_nowait(command)

    async def _api_commmand_queue_get(self) -> BleMgrMsgBase:
        return await self._mgr_command_q.get()

    def _handle_evt_or_ind(self, message: GtlMessageBase):

        # TODO make list of handlers from all avail classes. If get back a handler, call it
        event_handlers = [self.gap_mgr.evt_handlers, self.gatts_mgr]

        for handlers in event_handlers:
            handler = handlers.get(message.msg_id)
            if handler:
                handler(message)
                return True
        return False

    def _task_done_handler(self, task: asyncio.Task):
        if task.exception():
            task.result()  # Raise the exception

    async def _manager_task(self):

        # TODO function for creating these tasks so dont have in two spots
        self._command_q_task = asyncio.create_task(self._api_commmand_queue_get(), name='BleMgrReadCommandQueueTask')
        self._event_q_task = asyncio.create_task(self._adapter_event_queue_get(), name='BleMgrReadEventQueueTask')

        pending = [self._command_q_task, self._event_q_task]

        while True:
            done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)

            for task in done:
                if task is self._event_q_task:
                    # This is from the adapter_event_q
                    self._process_event_queue(task.result())
                    self._event_q_task = asyncio.create_task(self._adapter_event_queue_get(), name='BleMgrReadEventQueueTask')
                    pending.add(self._event_q_task)

                elif task is self._command_q_task:
                    # This is from the mgr_command_q
                    self._process_command_queue(task.result())
                    self._command_q_task = asyncio.create_task(self._api_commmand_queue_get(), name='BleMgrReadCommandQueueTask')
                    pending.add(self._command_q_task)

    def _process_command_queue(self, command: BleMgrMsgBase):

        category = command.opcode >> 8

        mgr: BleManagerBase = self.cmd_handlers.get(category)
        cmd_handler = mgr.cmd_handlers.get(command.opcode)

        # assert cmd_handler  # Should always have a handler

        if cmd_handler:
            cmd_handler(command)
        else:
            print(f"BleManager._process_command_queue. Unhandled command={command}\n")

    def _process_event_queue(self, event: GtlMessageBase):

        if not self._wait_q.match(event):
            if not self._handle_evt_or_ind(event):
                print(f"BleManager._process_event_queue. Unhandled event={event}\n")

    def init(self):
        # TODO keeping handles so these can be cancelled somehow
        self._mgr_task = asyncio.create_task(self._manager_task(), name='BleManagerTask')
        self._mgr_task.add_done_callback(self._task_done_handler)

    async def cmd_execute(self, command) -> BLE_ERROR:
        ble_status = self.gap_mgr.dev_params.status
        if ble_status == BLE_STATUS.BLE_IS_BUSY or ble_status == BLE_STATUS.BLE_IS_RESET:
            return BLE_ERROR.BLE_ERROR_BUSY

        # handler(command)
        print(f"CMD_EXECUTE: cmd={command}\n")
        self._mgr_command_queue_send(command)
        response = await self._mgr_response_queue_get()

        return response
