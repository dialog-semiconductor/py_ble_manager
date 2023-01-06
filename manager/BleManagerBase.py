import asyncio

from ble_api.BleCommon import BLE_ERROR, BleEventBase
from gtl_messages.gtl_message_base import GtlMessageBase
from manager.BleManagerCommonMsgs import BleMgrMsgBase, BleMgrCommonResetCmd
from manager.BleManagerStorage import StoredDevice
from manager.GtlWaitQueue import GtlWaitQueue, GtlWaitQueueElement


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
        self.stored_device_list: list[StoredDevice] = []

        # TODO would be nice to have dev_params here and all ble managers can access same instance

    def _adapter_command_queue_send(self, command: GtlMessageBase):
        self._adapter_command_q.put_nowait(command)

    def _find_devive_by_addr():
        pass

    async def _mgr_event_queue_get(self) -> BleMgrMsgBase:
        return await self._mgr_event_q.get()

    def _mgr_event_queue_send(self, evt: BleEventBase):
        self._mgr_event_q.put_nowait(evt)

    async def _mgr_response_queue_get(self) -> BleMgrCommonResetCmd:
        return await self._mgr_response_q.get()

    def _mgr_response_queue_send(self, response: BleMgrCommonResetCmd):
        self._mgr_response_q.put_nowait(response)

    def _task_to_connidx(self, task_id):  # TODO this is repeated from GtlWaitQueue. Do not have in two places
        return task_id >> 8

    def _wait_queue_add(self, conn_idx, msg_id, ext_id, cb, param):
        item = GtlWaitQueueElement(conn_idx=conn_idx, msg_id=msg_id, ext_id=ext_id, cb=cb, param=param)
        self._wait_q.push(item)
