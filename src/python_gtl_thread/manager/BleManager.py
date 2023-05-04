import concurrent.futures
import queue
import threading

from ..ble_api.BleGap import GAP_IO_CAPABILITIES
from ..ble_api.BleCommon import BLE_ERROR, BLE_STATUS, BleEventBase
from ..ble_api.BleConfig import BleConfigDefault
from ..gtl_messages.gtl_message_base import GtlMessageBase
from ..gtl_messages.gtl_message_gattc import GattcCmpEvt
from ..gtl_port.gattc_task import GATTC_MSG_ID, GATTC_OPERATION
from ..manager.BleDevParams import BleDevParamsDefault
from ..manager.BleManagerBase import BleManagerBase
from ..manager.BleManagerCommon import BleManagerCommon
from ..manager.BleManagerCommonMsgs import BLE_MGR_CMD_CAT, BleMgrMsgBase, BleMgrMsgRsp
from ..manager.BleManagerGap import BleManagerGap
from ..manager.BleManagerGattc import BleManagerGattc
from ..manager.BleManagerGatts import BleManagerGatts
from ..manager.BleManagerStorage import StoredDeviceQueue, StoredDevice
from ..manager.GtlWaitQueue import GtlWaitQueue


class BleManager(BleManagerBase):

    def __init__(self,
                 mgr_command_q: queue.Queue[BleMgrMsgBase],
                 mgr_response_q: queue.Queue[BLE_ERROR],
                 mgr_event_q: queue.Queue[BleEventBase],
                 adapter_command_q: queue.Queue[GtlMessageBase],
                 adapter_event_q: queue.Queue[GtlMessageBase],
                 shutdown_event: threading.Event,
                 config: BleConfigDefault) -> None:

        self._mgr_command_q: queue.Queue[BleMgrMsgBase] = mgr_command_q
        self._mgr_response_q: queue.Queue[BLE_ERROR] = mgr_response_q
        self._mgr_event_q: queue.Queue = mgr_event_q
        self._adapter_commnand_q: queue.Queue[GtlMessageBase] = adapter_command_q
        self._adapter_event_q: queue.Queue[GtlMessageBase] = adapter_event_q
        self._wait_q = GtlWaitQueue()
        self._stored_device_list = StoredDeviceQueue()
        self._stored_device_lock = threading.Lock()
        self._ble_stack_initialized = False
        self._dev_params = BleDevParamsDefault()
        self._dev_params_lock = threading.Lock()
        self._mgr_lock = threading.Lock()
        self._shutdown_event = shutdown_event
        self._ble_config = config
        self.common_mgr = BleManagerCommon(self._mgr_response_q,
                                           self._mgr_event_q,
                                           self._adapter_commnand_q,
                                           self._wait_q,
                                           self._stored_device_list,
                                           self._stored_device_lock,
                                           self._dev_params,
                                           self._dev_params_lock,
                                           self._ble_config)
        self.gap_mgr = BleManagerGap(self._mgr_response_q,
                                     self._mgr_event_q,
                                     self._adapter_commnand_q,
                                     self._wait_q,
                                     self._stored_device_list,
                                     self._stored_device_lock,
                                     self._dev_params,
                                     self._dev_params_lock,
                                     self._ble_config)
        self.gattc_mgr = BleManagerGattc(self._mgr_response_q,
                                         self._mgr_event_q,
                                         self._adapter_commnand_q,
                                         self._wait_q,
                                         self._stored_device_list,
                                         self._stored_device_lock,
                                         self._dev_params,
                                         self._dev_params_lock,
                                         self._ble_config)
        self.gatts_mgr = BleManagerGatts(self._mgr_response_q,
                                         self._mgr_event_q,
                                         self._adapter_commnand_q,
                                         self._wait_q,
                                         self._stored_device_list,
                                         self._stored_device_lock,
                                         self._dev_params,
                                         self._dev_params_lock,
                                         self._ble_config)

        self.cmd_handlers = {
            BLE_MGR_CMD_CAT.BLE_MGR_COMMON_CMD_CAT: self.common_mgr,
            BLE_MGR_CMD_CAT.BLE_MGR_GAP_CMD_CAT: self.gap_mgr,
            BLE_MGR_CMD_CAT.BLE_MGR_GATTS_CMD_CAT: self.gatts_mgr,
            BLE_MGR_CMD_CAT.BLE_MGR_GATTC_CMD_CAT: self.gattc_mgr,
            BLE_MGR_CMD_CAT.BLE_MGR_L2CAP_CMD_CAT: None,
        }

        self.evt_handlers = [self.gap_mgr.evt_handlers, self.gattc_mgr.evt_handlers, self.gatts_mgr.evt_handlers]

    def _adapter_event_queue_get(self) -> BleEventBase:
        item = None
        while item is None:
            try:
                if self._shutdown_event.is_set():
                    break
                item = self._adapter_event_q.get(timeout=1)
            except queue.Empty:
                pass
        return item

    def _api_commmand_queue_get(self) -> BleMgrMsgBase:
        item = None
        while item is None:
            try:
                if self._shutdown_event.is_set():
                    break
                item = self._mgr_command_q.get(timeout=1)
            except queue.Empty:
                pass
        return item

    def _gattc_cmp_evt_handler(self, evt: GattcCmpEvt):
        if (evt.parameters.operation == GATTC_OPERATION.GATTC_NOTIFY
                or evt.parameters.operation == GATTC_OPERATION.GATTC_INDICATE):

            self.gatts_mgr.cmp_evt_handler(evt)
        else:
            self.gattc_mgr.cmp_evt_handler(evt)

    def _handle_evt_or_ind(self, message: GtlMessageBase):

        is_handled = False

        # If this is a GATTC_CMP_EVT need to determine if will be handled by gattc_mgr or gatts_mgr
        if message.msg_id == GATTC_MSG_ID.GATTC_CMP_EVT:
            response = self._gattc_cmp_evt_handler(message)
            if response is None:
                is_handled = True
            else:
                is_handled = response
        else:
            for handlers in self.evt_handlers:
                handler = handlers.get(message.msg_id)
                if handler:
                    response = None
                    response = handler(message)
                    if response is None:
                        is_handled = True
                    else:
                        is_handled = response
                    break
        return is_handled

    def _mgr_command_queue_send(self, command: BleMgrMsgBase):
        self._mgr_command_q.put_nowait(command)

    def _mgr_task(self):

        executor = concurrent.futures.ThreadPoolExecutor(max_workers=2, thread_name_prefix='BleMgr')

        # TODO function for creating these tasks so dont have in two spots
        self._command_q_task = executor.submit(self._api_commmand_queue_get)
        self._event_q_task = executor.submit(self._adapter_event_queue_get)

        pending = [self._command_q_task, self._event_q_task]

        while True:

            if self._shutdown_event.is_set():
                executor.shutdown(wait=False, cancel_futures=True)

            done, pending = concurrent.futures.wait(pending, timeout=1, return_when=concurrent.futures.FIRST_COMPLETED)

            for task in done:
                if task is self._event_q_task:
                    # print(f"Manager evet {task}")
                    # This is from ..the adapter_event_q
                    if task.result():
                        self._process_event_queue(task.result())
                    if not self._shutdown_event.is_set():
                        self._event_q_task = executor.submit(self._adapter_event_queue_get)
                        pending.add(self._event_q_task)

                elif task is self._command_q_task:
                    # print(f"Manager command {task}")
                    # This is from ..the mgr_command_q
                    if task.result():
                        self._process_command_queue(task.result())
                    if not self._shutdown_event.is_set():
                        self._command_q_task = executor.submit(self._api_commmand_queue_get)
                        pending.add(self._command_q_task)

            if len(pending) == 0:
                break

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

    def cmd_execute(self, command: BleMgrMsgBase) -> BLE_ERROR:
        self.mgr_dev_params_acquire()
        ble_status = self.gap_mgr._dev_params.status
        self.mgr_dev_params_release()
        if ble_status == BLE_STATUS.BLE_IS_BUSY or ble_status == BLE_STATUS.BLE_IS_RESET:
            return BleMgrMsgRsp(opcode=command.opcode, status=BLE_ERROR.BLE_ERROR_BUSY)

        self._mgr_lock.acquire()  # TODO unsure why this is needed unless calling manager functions directly
        self._mgr_command_queue_send(command)
        response = self._mgr_response_queue_get()
        self._mgr_lock.release()
        assert command.opcode == response.opcode

        return response

    def init(self):
        # TODO need to be able to cancel
        self._task = threading.Thread(target=self._mgr_task)
        self._task.start()

    def find_stored_device_by_conn_idx(self, conn_idx: int) -> StoredDevice:
        return self._stored_device_list.find_device_by_conn_idx(conn_idx)

    def set_io_cap(self, io_cap: GAP_IO_CAPABILITIES) -> BLE_ERROR:
        return self.gap_mgr.set_io_cap(io_cap)
