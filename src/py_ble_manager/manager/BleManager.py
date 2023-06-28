import queue
import threading

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
from ..manager.ResetWaitQueue import ResetWaitQueue


class BleManager(BleManagerBase):

    def __init__(self,
                 mgr_command_q: queue.Queue[BleMgrMsgBase],
                 mgr_response_q: queue.Queue[BLE_ERROR],
                 mgr_event_q: queue.Queue[BleEventBase],
                 adapter_command_q: queue.Queue[GtlMessageBase],
                 adapter_event_q: queue.Queue[GtlMessageBase],
                 config: BleConfigDefault) -> None:

        self._mgr_command_q: queue.Queue[BleMgrMsgBase] = mgr_command_q
        self._mgr_response_q: queue.Queue[BLE_ERROR] = mgr_response_q
        self._mgr_event_q: queue.Queue = mgr_event_q
        self._adapter_command_q: queue.Queue[GtlMessageBase] = adapter_command_q
        self._adapter_event_q: queue.Queue[GtlMessageBase] = adapter_event_q
        self._gtl_wait_q = GtlWaitQueue()
        self._stored_device_list = StoredDeviceQueue()
        self._stored_device_lock = threading.RLock()
        self._ble_stack_initialized = False
        self._dev_params = BleDevParamsDefault()
        self._dev_params_lock = threading.RLock()
        self._mgr_lock = threading.Lock()
        self._ble_config = config
        self._reset_wait_q = ResetWaitQueue()
        self._common_mgr = BleManagerCommon(self._mgr_response_q,
                                            self._mgr_event_q,
                                            self._adapter_command_q,
                                            self._gtl_wait_q,
                                            self._stored_device_list,
                                            self._stored_device_lock,
                                            self._dev_params,
                                            self._dev_params_lock,
                                            self._ble_config,
                                            self._reset_wait_q)
        self._gap_mgr = BleManagerGap(self._mgr_response_q,
                                      self._mgr_event_q,
                                      self._adapter_command_q,
                                      self._gtl_wait_q,
                                      self._stored_device_list,
                                      self._stored_device_lock,
                                      self._dev_params,
                                      self._dev_params_lock,
                                      self._ble_config)
        self._gattc_mgr = BleManagerGattc(self._mgr_response_q,
                                          self._mgr_event_q,
                                          self._adapter_command_q,
                                          self._gtl_wait_q,
                                          self._stored_device_list,
                                          self._stored_device_lock,
                                          self._dev_params,
                                          self._dev_params_lock,
                                          self._ble_config)
        self._gatts_mgr = BleManagerGatts(self._mgr_response_q,
                                          self._mgr_event_q,
                                          self._adapter_command_q,
                                          self._gtl_wait_q,
                                          self._stored_device_list,
                                          self._stored_device_lock,
                                          self._dev_params,
                                          self._dev_params_lock,
                                          self._ble_config)

        self.cmd_handlers = {
            BLE_MGR_CMD_CAT.BLE_MGR_COMMON_CMD_CAT: self._common_mgr,
            BLE_MGR_CMD_CAT.BLE_MGR_GAP_CMD_CAT: self._gap_mgr,
            BLE_MGR_CMD_CAT.BLE_MGR_GATTS_CMD_CAT: self._gatts_mgr,
            BLE_MGR_CMD_CAT.BLE_MGR_GATTC_CMD_CAT: self._gattc_mgr,
            BLE_MGR_CMD_CAT.BLE_MGR_L2CAP_CMD_CAT: None,
        }

        self.evt_handlers = [self._gap_mgr.evt_handlers, self._gattc_mgr.evt_handlers, self._gatts_mgr.evt_handlers, self._common_mgr.evt_handlers]

    def _adapter_event_queue_get(self) -> BleEventBase:
        return self._adapter_event_q.get()

    def _adapter_event_queue_task(self):
        while True:
            event = self._adapter_event_queue_get()
            self._process_event_queue(event)

    def _api_commmand_queue_get(self) -> BleMgrMsgBase:
        return self._mgr_command_q.get()

    def _api_command_queue_task(self):
        while True:
            command = self._api_commmand_queue_get()
            self._process_command_queue(command)

    def _gatt_cmp_evt_handler(self, evt: GattcCmpEvt):
        if (evt.parameters.operation == GATTC_OPERATION.GATTC_NOTIFY
                or evt.parameters.operation == GATTC_OPERATION.GATTC_INDICATE):

            return self._gatts_mgr.cmp_evt_handler(evt)
        else:
            return self._gattc_mgr.cmp_evt_handler(evt)

    def _handle_evt_or_ind(self, gtl: GtlMessageBase):

        is_handled = False

        # If this is a GATTC_CMP_EVT need to determine if will be handled by _gattc_mgr or _gatts_mgr
        if gtl.msg_id == GATTC_MSG_ID.GATTC_CMP_EVT:
            is_handled = self._gatt_cmp_evt_handler(gtl)
        else:
            # loop thru Gap, Gattc, Gatts handlers to determine if a handler exists for this event
            for handlers in self.evt_handlers:
                handler = handlers.get(gtl.msg_id)
                if handler:
                    # If the handler exists, call it
                    response = None
                    response = handler(gtl)
                    # All handlers except for those that handle CMP_EVTs (e.g. xxx_cmp_evt_handler() ) will return None
                    if response is None:
                        is_handled = True
                    else:
                        # BleManagerGap.gapm_cmp_evt_handler() and BleManagerGap.gapc_cmp_evt_handler() will return bool to indicate if event has been handled
                        is_handled = response
                    break
        return is_handled

    def _mgr_command_queue_send(self, command: BleMgrMsgBase):
        self._mgr_command_q.put_nowait(command)

    def _process_command_queue(self, command: BleMgrMsgBase):

        category = command.opcode >> 8

        mgr: BleManagerBase = self.cmd_handlers.get(category)
        cmd_handler = mgr.cmd_handlers.get(command.opcode)

        if cmd_handler:
            cmd_handler(command)
        else:
            print(f"BleManager._process_command_queue. Unhandled command={command}\n")

    def _process_event_queue(self, gtl: GtlMessageBase):
        if not self._reset_wait_q.match(gtl):
            if not self._gtl_wait_q.match(gtl):
                if not self._handle_evt_or_ind(gtl):
                    print(f"BleManager._process_event_queue. Unhandled event={gtl}\n")

    def cmd_execute(self, command: BleMgrMsgBase, rsp_timeout_s: int = None) -> BLE_ERROR:
        dev_params = self.dev_params_acquire()
        ble_status = dev_params.status
        self.dev_params_release()
        if ble_status == BLE_STATUS.BLE_IS_BUSY or ble_status == BLE_STATUS.BLE_IS_RESET:
            return BleMgrMsgRsp(opcode=command.opcode, status=BLE_ERROR.BLE_ERROR_BUSY)

        self._mgr_lock.acquire()
        self._mgr_command_queue_send(command)
        response = self._mgr_response_queue_get(rsp_timeout_s)
        self._mgr_lock.release()

        return response

    def init(self):
        self._api_q_task = threading.Thread(target=self._api_command_queue_task)
        self._api_q_task.daemon = True
        self._api_q_task.start()

        self._adapter_q_task = threading.Thread(target=self._adapter_event_queue_task)
        self._adapter_q_task.daemon = True
        self._adapter_q_task.start()

    def find_stored_device_by_conn_idx(self, conn_idx: int) -> StoredDevice:
        return self._stored_device_list.find_device_by_conn_idx(conn_idx)

    def update_ble_config(self, ble_config: BleConfigDefault):
        super().update_ble_config(ble_config)
        self._common_mgr.update_ble_config(ble_config)
        self._gap_mgr.update_ble_config(ble_config)
        self._gattc_mgr.update_ble_config(ble_config)
        self._gatts_mgr.update_ble_config(ble_config)
