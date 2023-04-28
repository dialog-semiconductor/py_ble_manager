import queue

from ble_api.BleCommon import BLE_ERROR, BleEventBase
from ble_api.BleGap import BLE_CONN_IDX_INVALID
from gtl_messages.gtl_message_base import GtlMessageBase
from gtl_messages.gtl_message_gapm import GapmResetCmd
from gtl_port.gapm_task import GAPM_MSG_ID, GAPM_OPERATION, gapm_reset_cmd
from manager.BleManagerBase import BleManagerBase
from manager.BleManagerCommonMsgs import BleMgrCommonResetCmd, BleMgrCommonResetRsp, BLE_MGR_COMMON_CMD_OPCODE
from manager.BleManagerStorage import StoredDeviceQueue
from manager.GtlWaitQueue import GtlWaitQueue


# TODO This class name is somewhat confusing given base class. Consider rename, or merge  possibly merge in BleMgrGap
class BleManagerCommon(BleManagerBase):

    def __init__(self,
                 mgr_response_q: queue.Queue[BLE_ERROR],
                 mgr_event_q: queue.Queue[BleEventBase],
                 adapter_command_q: queue.Queue[GtlMessageBase],
                 wait_q: GtlWaitQueue,
                 stored_device_q: StoredDeviceQueue
                 ) -> None:

        super().__init__(mgr_response_q, mgr_event_q, adapter_command_q, wait_q, stored_device_q)

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
        ble_mgr_common_reset_cmd_handler,               STARTED
        ble_mgr_common_read_tx_power_cmd_handler,
#endif
};
'''
