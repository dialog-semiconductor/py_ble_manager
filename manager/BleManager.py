import asyncio

from ble_api.BleCommon import BLE_ERROR, BLE_STATUS, BleEventBase
from gtl_messages.gtl_message_base import GtlMessageBase
from gtl_messages.gtl_message_gattc import GattcCmpEvt
from gtl_port.gattc_task import GATTC_MSG_ID, GATTC_OPERATION
from manager.BleManagerBase import BleManagerBase
from manager.BleManagerCommon import BleManagerCommon
from manager.BleManagerCommonMsgs import BLE_MGR_CMD_CAT, BleMgrMsgBase, BleMgrMsgRsp
from manager.BleManagerGap import BleManagerGap
from manager.BleManagerGattc import BleManagerGattc
from manager.BleManagerGatts import BleManagerGatts
from manager.BleManagerStorage import StoredDeviceQueue, StoredDevice
from manager.GtlWaitQueue import GtlWaitQueue


class BleManager(BleManagerBase):

    def __init__(self,
                 mgr_command_q: asyncio.Queue[BleMgrMsgBase],
                 mgr_response_q: asyncio.Queue[BLE_ERROR],
                 mgr_event_q: asyncio.Queue[BleEventBase],
                 adapter_command_q: asyncio.Queue[GtlMessageBase],
                 adapter_event_q: asyncio.Queue[GtlMessageBase]) -> None:

        self._mgr_command_q: asyncio.Queue[BleMgrMsgBase] = mgr_command_q
        self._mgr_response_q: asyncio.Queue[BLE_ERROR] = mgr_response_q
        self._mgr_event_q: asyncio.Queue = mgr_event_q
        self._adapter_commnand_q: asyncio.Queue[GtlMessageBase] = adapter_command_q
        self._adapter_event_q: asyncio.Queue[GtlMessageBase] = adapter_event_q
        self._wait_q = GtlWaitQueue()
        self._stored_device_list = StoredDeviceQueue()
        self._ble_stack_initialized = False
        self.common_mgr = BleManagerCommon(self._mgr_response_q, self._mgr_event_q, self._adapter_commnand_q, self._wait_q, self._stored_device_list)
        self.gap_mgr = BleManagerGap(self._mgr_response_q, self._mgr_event_q, self._adapter_commnand_q, self._wait_q, self._stored_device_list)
        self.gattc_mgr = BleManagerGattc(self._mgr_response_q, self._mgr_event_q, self._adapter_commnand_q, self._wait_q, self._stored_device_list)
        self.gatts_mgr = BleManagerGatts(self._mgr_response_q, self._mgr_event_q, self._adapter_commnand_q, self._wait_q, self._stored_device_list)

        self.cmd_handlers = {
            BLE_MGR_CMD_CAT.BLE_MGR_COMMON_CMD_CAT: self.common_mgr,
            BLE_MGR_CMD_CAT.BLE_MGR_GAP_CMD_CAT: self.gap_mgr,
            BLE_MGR_CMD_CAT.BLE_MGR_GATTS_CMD_CAT: self.gatts_mgr,
            BLE_MGR_CMD_CAT.BLE_MGR_GATTC_CMD_CAT: self.gattc_mgr,
            BLE_MGR_CMD_CAT.BLE_MGR_L2CAP_CMD_CAT: None,
        }

        self.evt_handlers = [self.gap_mgr.evt_handlers, self.gattc_mgr.evt_handlers, self.gatts_mgr.evt_handlers]

    async def _adapter_event_queue_get(self) -> BleEventBase:
        return await self._adapter_event_q.get()

    async def _api_commmand_queue_get(self) -> BleMgrMsgBase:
        return await self._mgr_command_q.get()

    def gattc_cmp_evt_handler(self, evt: GattcCmpEvt):
        if (evt.parameters.operation == GATTC_OPERATION.GATTC_NOTIFY
            or evt.parameters.operation == GATTC_OPERATION.GATTC_INDICATE
            or evt.parameters.operation == GATTC_OPERATION.GATTC_SVC_CHANGED):

            self.gatts_mgr.cmp_evt_handler(evt)
        else:
            self.gattc_mgr.cmp_evt_handler(evt)


    def _handle_evt_or_ind(self, message: GtlMessageBase):

        # TODO make list of handlers from all avail classes. If get back a handler, call it
        handled = False

        # If this is a GATTC_CMP_EVT need to determine if will be handled by gattc_mgr or gatts_mgr
        if message.msg_id == GATTC_MSG_ID.GATTC_CMP_EVT:
            response = self.gattc_cmp_evt_handler(message)
            if response is None:
                handled = True
            else:
                handled = response
        else:
            for handlers in self.evt_handlers:
                handler = handlers.get(message.msg_id)
                if handler:
                    response = None
                    response = handler(message)
                    if response is None:
                        handled = True
                    else:
                        handled = response
                    break
        return handled

    def _mgr_command_queue_send(self, command: BleMgrMsgBase):
        self._mgr_command_q.put_nowait(command)

    async def _mgr_task(self):

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

    def _task_done_handler(self, task: asyncio.Task):
        if task.exception():
            task.result()  # Raise the exception

    async def cmd_execute(self, command: BleMgrMsgBase) -> BLE_ERROR:
        ble_status = self.gap_mgr.dev_params.status
        if ble_status == BLE_STATUS.BLE_IS_BUSY or ble_status == BLE_STATUS.BLE_IS_RESET:
            return BleMgrMsgRsp(opcode=command.opcode, status=BLE_ERROR.BLE_ERROR_BUSY)

        self._mgr_command_queue_send(command)
        response = await self._mgr_response_queue_get()

        assert command.opcode == response.opcode

        return response

    def init(self):
        # TODO need to be able to cancel
        self._mgr_task = asyncio.create_task(self._mgr_task(), name='BleManagerTask')
        self._mgr_task.add_done_callback(self._task_done_handler)

    def find_stored_device_by_conn_idx(self, conn_idx: int) -> StoredDevice:
        return self._stored_device_list.find_device_by_conn_idx(conn_idx)
