import queue
import threading
from typing import Callable, Tuple

from ..ble_api.BleCommon import BLE_ERROR, BleEventBase, BLE_STATUS
from ..ble_api.BleConfig import BleConfigDefault
from ..gtl_messages.gtl_message_base import GtlMessageBase
from ..manager.BleDevParams import BleDevParamsDefault, BleDevParams
from ..manager.BleManagerCommonMsgs import BleMgrMsgBase, BleMgrMsgRsp
from ..manager.BleManagerStorage import StoredDeviceQueue
from ..manager.GtlWaitQueue import GtlWaitQueue
from .WaitQueue import WaitQueueElement


class BleManagerBase():
    def __init__(self,
                 mgr_response_q: queue.Queue[BLE_ERROR],
                 mgr_event_q: queue.Queue[BleEventBase],
                 adapter_command_q: queue.Queue[GtlMessageBase],
                 wait_q: GtlWaitQueue,
                 stored_device_q: StoredDeviceQueue,
                 stored_device_lock: threading.RLock,
                 dev_params: BleDevParamsDefault,
                 dev_params_lock: threading.RLock,
                 config: BleConfigDefault) -> None:

        self._mgr_response_q = mgr_response_q
        self._mgr_event_q = mgr_event_q
        self._adapter_command_q = adapter_command_q
        self._gtl_wait_q = wait_q
        self.cmd_handlers = {}
        self.evt_handlers = {}
        self._stored_device_list: StoredDeviceQueue = stored_device_q
        self._stored_device_lock: threading.Lock = stored_device_lock
        self._dev_params = dev_params
        self._dev_params_lock: threading.Lock = dev_params_lock
        self._ble_config = config

    def _adapter_command_queue_send(self, command: GtlMessageBase):
        self._adapter_command_q.put_nowait(command)

    def _generic_get(self, conn_idx: int, key: int) -> Tuple[bytes, BLE_ERROR]:
        error = BLE_ERROR.BLE_ERROR_FAILED
        self.storage_acquire()
        dev = self._stored_device_list.find_device_by_conn_idx(conn_idx)
        app_value = bytes()
        if not dev:
            error = BLE_ERROR.BLE_ERROR_NOT_CONNECTED
        else:
            app_value = dev.app_value_get(key)
            if app_value:
                error = BLE_ERROR.BLE_STATUS_OK
            else:
                error = BLE_ERROR.BLE_ERROR_NOT_FOUND

        self.storage_release()
        return app_value, error

    def _generic_put(self, conn_idx: int, key: int, value: bytes, persistent: bool) -> BLE_ERROR:
        error = BLE_ERROR.BLE_ERROR_FAILED
        self.storage_acquire()
        dev = self._stored_device_list.find_device_by_conn_idx(conn_idx)
        if not dev:
            error = BLE_ERROR.BLE_ERROR_NOT_CONNECTED
        else:
            dev.app_value_put(key, value, persistent)
            error = BLE_ERROR.BLE_STATUS_OK

        self.storage_release()
        return error

    def _gtl_wait_queue_add(self, conn_idx: int, msg_id: int, ext_id: int, cb: Callable, param: object) -> None:
        item = WaitQueueElement(conn_idx=conn_idx, msg_id=msg_id, ext_id=ext_id, cb=cb, param=param)
        self._gtl_wait_q.add(item)

    def _gtl_wait_queue_flush(self, conn_idx: int) -> None:
        self._gtl_wait_q.flush(conn_idx)

    def _gtl_wait_queue_flush_all(self) -> None:
        self._gtl_wait_q.flush_all()

    def _mgr_event_queue_flush(self) -> None:
        # TODO Critical section?
        while self._mgr_event_q.qsize() != 0:
            try:
                self._mgr_event_q.get_nowait()
                print(self._mgr_event_q.qsize())
            except queue.Empty:
                break

    def _mgr_event_queue_send(self, evt: BleEventBase):
        self._mgr_event_q.put_nowait(evt)

    def _mgr_response_queue_get(self, timeout: int = None) -> BleMgrMsgRsp:
        try:
            evt = self._mgr_response_q.get(timeout=timeout)
        except queue.Empty:
            evt = None
        return evt

    def _mgr_response_queue_send(self, response: BleMgrMsgRsp):
        self._mgr_response_q.put_nowait(response)

    def _set_status(self, status: BLE_STATUS):
        dev_params = self.dev_params_acquire()
        dev_params.status = status
        self.dev_params_release()

    def _task_to_connidx(self, task_id: int) -> int:
        return task_id >> 8

    def dev_params_acquire(self):
        self._dev_params_lock.acquire()
        return self._dev_params

    def dev_params_release(self) -> None:
        self._dev_params_lock.release()

    def device_for_each(self, callback: callable, param: object):
        self._stored_device_list.for_each(callback, param)

    def mgr_event_queue_get(self, timeout=None) -> BleMgrMsgBase:
        try:
            evt = self._mgr_event_q.get(timeout=timeout)
        except queue.Empty:
            evt = None
        return evt

    def storage_get_buffer(self, conn_idx: int, key: int) -> Tuple[bytes, BLE_ERROR]:
        app_value, error = self._generic_get(conn_idx, key)
        return app_value, error

    def storage_get_int(self, conn_idx: int, key: int) -> Tuple[int, BLE_ERROR]:
        app_value, error = self._generic_get(conn_idx, key)
        return_val = None
        if app_value:
            return_val = int.from_bytes(app_value, 'little', signed=True)
        return return_val, error

    def storage_put_buffer(self, conn_idx: int, key: int, value: bytes, persistent: bool):
        return self._generic_put(conn_idx, key, value, persistent)

    def storage_put_int(self, conn_idx: int, key: int, value: int, persistent: bool):
        return self._generic_put(conn_idx, key, value.to_bytes(4, 'little', signed=True), persistent)

    def storage_acquire(self) -> BleDevParams:
        self._stored_device_lock.acquire()

    def storage_release(self) -> None:
        self._stored_device_lock.release()

    def update_ble_config(self, ble_config: BleConfigDefault):
        self._ble_config = ble_config
