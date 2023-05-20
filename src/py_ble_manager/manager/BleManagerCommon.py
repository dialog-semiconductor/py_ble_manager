import queue
import threading

from ..ble_api.BleCommon import BLE_ERROR, BleEventBase, BLE_STATUS, BleEventResetCompleted
from ..ble_api.BleConfig import BleConfigDefault
from ..ble_api.BleGap import BLE_CONN_IDX_INVALID
from ..gtl_messages.gtl_message_base import GtlMessageBase
from ..gtl_messages.gtl_message_gapm import GapmResetCmd, GapmCmpEvt
from ..gtl_port.gapm_task import GAPM_MSG_ID, GAPM_OPERATION, gapm_reset_cmd
from ..gtl_port.rwble_hl_error import HOST_STACK_ERROR_CODE
from ..manager.BleDevParams import BleDevParamsDefault
from ..manager.BleManagerBase import BleManagerBase
from ..manager.BleManagerCommonMsgs import BleMgrCommonResetCmd, BleMgrCommonResetRsp, BLE_MGR_COMMON_CMD_OPCODE
from ..manager.BleManagerStorage import StoredDeviceQueue
from ..manager.GtlWaitQueue import GtlWaitQueue


class BleManagerCommon(BleManagerBase):

    def __init__(self,
                 mgr_response_q: queue.Queue[BLE_ERROR],
                 mgr_event_q: queue.Queue[BleEventBase],
                 adapter_command_q: queue.Queue[GtlMessageBase],
                 wait_q: GtlWaitQueue,
                 stored_device_q: StoredDeviceQueue,
                 stored_device_lock: threading.Lock(),
                 dev_params: BleDevParamsDefault,
                 dev_params_lock: threading.Lock(),
                 ble_config: BleConfigDefault = BleConfigDefault()
                 ) -> None:

        super().__init__(mgr_response_q, mgr_event_q, adapter_command_q, wait_q, stored_device_q, stored_device_lock, dev_params, dev_params_lock, ble_config)

        self.cmd_handlers = {
            BLE_MGR_COMMON_CMD_OPCODE.BLE_MGR_COMMON_RESET_CMD: self.reset_cmd_handler,
        }

    def _reset_rsp_handler(self, gtl: GapmCmpEvt, param: None):
        response = BleMgrCommonResetRsp(BLE_ERROR.BLE_ERROR_FAILED)
        evt = BleEventResetCompleted(BLE_ERROR.BLE_ERROR_FAILED)

        if gtl.parameters.status == HOST_STACK_ERROR_CODE.ATT_ERR_NO_ERROR:
            response.status = BLE_ERROR.BLE_STATUS_OK
            evt.status = BLE_ERROR.BLE_STATUS_OK

            '''
            TODO
            storage_acquire();
            storage_cleanup();
            storage_init();
            storage_release();
            '''

            # Clear waitqueue (does not call waitqueue callback functions)
            self._wait_queue_flush_all()

            # TODO
            # Set default device parameters
            # dev_params = self.dev_params_acquire()
            # dev_params = BleDevParamsDefault()
            # Update own public BD address with the one stored in NVPARAM
            # ad_ble_get_public_address(dev_params->own_addr.addr)
            # Update own IRK with the one stored in NVPARAM
            # ad_ble_get_irk(dev_params->irk.key)
            self.dev_params_release()

        self._set_status(BLE_STATUS.BLE_IS_ENABLED)
        self._mgr_response_queue_send(response)
        self._mgr_event_queue_send(evt)

    def reset_cmd_handler(self, command: BleMgrCommonResetCmd):
        self._set_status(BLE_STATUS.BLE_IS_RESET)
        self._wait_queue_add(BLE_CONN_IDX_INVALID, GAPM_MSG_ID.GAPM_CMP_EVT, GAPM_OPERATION.GAPM_RESET, self._reset_rsp_handler, None)
        gtl = GapmResetCmd(gapm_reset_cmd(GAPM_OPERATION.GAPM_RESET))
        self._adapter_command_queue_send(gtl)


'''
static const ble_mgr_cmd_handler_t h_common[BLE_MGR_CMD_GET_IDX(BLE_MGR_COMMON_LAST_CMD)] = {
        ble_mgr_common_stack_msg_handler,
        ble_mgr_common_register_cmd_handler,
#ifndef BLE_STACK_PASSTHROUGH_MODE
        ble_mgr_common_enable_cmd_handler,
        ble_mgr_common_reset_cmd_handler,               STARTED
        ble_mgr_common_read_tx_power_cmd_handler,
#endif
};
'''
