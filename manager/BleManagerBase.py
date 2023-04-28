import queue
from typing import Callable

from ble_api.BleCommon import BLE_ERROR, BleEventBase
from gtl_messages.gtl_message_base import GtlMessageBase
from manager.BleManagerCommonMsgs import BleMgrMsgBase, BleMgrMsgRsp
from manager.BleManagerStorage import StoredDeviceQueue
from manager.GtlWaitQueue import GtlWaitQueue, GtlWaitQueueElement


class BleManagerBase():
    def __init__(self,
                 mgr_response_q: queue.Queue[BLE_ERROR],
                 mgr_event_q: queue.Queue[BleEventBase],
                 adapter_command_q: queue.Queue[GtlMessageBase],
                 wait_q: GtlWaitQueue,
                 stored_device_q: StoredDeviceQueue) -> None:

        self._mgr_response_q = mgr_response_q
        self._mgr_event_q = mgr_event_q
        self._adapter_command_q = adapter_command_q
        self._wait_q = wait_q
        self.cmd_handlers = {}
        self.evt_handlers = {}
        self._stored_device_list: StoredDeviceQueue = stored_device_q

        # TODO would be nice to have dev_params here and all ble managers can access same instance

    def _adapter_command_queue_send(self, command: GtlMessageBase):
        self._adapter_command_q.put_nowait(command)

    def _mgr_event_queue_send(self, evt: BleEventBase):
        self._mgr_event_q.put_nowait(evt)

    def _mgr_response_queue_get(self) -> BleMgrMsgRsp:
        return self._mgr_response_q.get()

    def _mgr_response_queue_send(self, response: BleMgrMsgRsp):
        self._mgr_response_q.put_nowait(response)

    def _wait_queue_add(self, conn_idx: int, msg_id: int, ext_id: int, cb: Callable, param: object) -> None:
        item = GtlWaitQueueElement(conn_idx=conn_idx, msg_id=msg_id, ext_id=ext_id, cb=cb, param=param)
        self._wait_q.add(item)

    def _wait_queue_flush(self, conn_idx: int) -> None:
        self._wait_q.flush(conn_idx)

    def _task_to_connidx(self, task_id: int) -> int:  # TODO this is repeated from GtlWaitQueue. Do not have in two places
        return task_id >> 8

    def mgr_event_queue_get(self) -> BleMgrMsgBase:
        return self._mgr_event_q.get()
