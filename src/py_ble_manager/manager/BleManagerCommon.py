import queue
import threading
from typing import Callable

from ..ble_api.BleCommon import BLE_ERROR, BleEventBase, BLE_STATUS, BleEventResetCompleted
from ..ble_api.BleConfig import BleConfigDefault, BleConfigDA14531, BleConfigDA1469x, DA14531VersionInd, DA14695VersionInd, \
    BLE_HW_TYPE
from ..ble_api.BleGap import BLE_CONN_IDX_INVALID
from ..gtl_messages.gtl_message_base import GtlMessageBase
from ..gtl_messages.gtl_message_gapm import GapmResetCmd, GapmCmpEvt, GapmGetDevVersionCmd, GapmDevVersionInd
from ..gtl_port.gapm_task import GAPM_MSG_ID, GAPM_OPERATION, gapm_reset_cmd, gapm_get_dev_info_cmd
from ..gtl_port.rwble_hl_error import HOST_STACK_ERROR_CODE
from ..manager.BleDevParams import BleDevParamsDefault
from ..manager.BleManagerBase import BleManagerBase
from ..manager.BleManagerCommonMsgs import BleMgrCommonResetCmd, BleMgrCommonResetRsp, BLE_MGR_COMMON_CMD_OPCODE, \
    BleMgrCommonGetDevVersionCmd, BleMgrCommonGetDevVersionRsp

from ..manager.BleManagerStorage import StoredDeviceQueue
from ..manager.GtlWaitQueue import GtlWaitQueue
from ..manager.ResetWaitQueue import ResetWaitQueue
from .WaitQueue import WaitQueueElement


class BleManagerCommon(BleManagerBase):

    def __init__(self,
                 mgr_response_q: queue.Queue[BLE_ERROR],
                 mgr_event_q: queue.Queue[BleEventBase],
                 adapter_command_q: queue.Queue[GtlMessageBase],
                 gtl_wait_q: GtlWaitQueue,
                 stored_device_q: StoredDeviceQueue,
                 stored_device_lock: threading.RLock,
                 dev_params: BleDevParamsDefault,
                 dev_params_lock: threading.RLock,
                 ble_config: BleConfigDefault,
                 reset_wait_q: ResetWaitQueue,
                 ) -> None:

        self._reset_wait_q = reset_wait_q
        super().__init__(mgr_response_q,
                         mgr_event_q,
                         adapter_command_q,
                         gtl_wait_q,
                         stored_device_q,
                         stored_device_lock,
                         dev_params,
                         dev_params_lock,
                         ble_config)

        self.cmd_handlers = {
            BLE_MGR_COMMON_CMD_OPCODE.BLE_MGR_COMMON_RESET_CMD: self.reset_cmd_handler,
            BLE_MGR_COMMON_CMD_OPCODE.BLE_MGR_COMMON_GET_DEV_VERSION_CMD: self.get_dev_version_cmd_handler,
        }

        self.evt_handlers = {
            GAPM_MSG_ID.GAPM_DEV_VERSION_IND: self.get_dev_version_evt_handler,
        }

    def _get_dev_version_rsp_handler(self, gtl: GapmCmpEvt, response: BleMgrCommonGetDevVersionRsp):
        if gtl.parameters.status == HOST_STACK_ERROR_CODE.GAP_ERR_NO_ERROR:
            response.status = BLE_ERROR.BLE_STATUS_OK
            # overwrite the BLE config only if user is using the default
            response.config = None
            if self._ble_config == BleConfigDefault():
                if response == DA14531VersionInd():
                    response.config = BleConfigDA14531()
                elif response == DA14695VersionInd():
                    response.config = BleConfigDA1469x()
            else:
                # otherwise just update the HW type
                if response == DA14531VersionInd():
                    self._ble_config.dg_configHW_TYPE = BLE_HW_TYPE.DA14531
                elif response == DA14695VersionInd():
                    self._ble_config.dg_configHW_TYPE = BLE_HW_TYPE.DA14695

        self._mgr_response_queue_send(response)

    def _reset_rsp_handler(self, gtl: GapmCmpEvt, param: None):
        response = BleMgrCommonResetRsp(status=BLE_ERROR.BLE_ERROR_FAILED)
        evt = BleEventResetCompleted(status=BLE_ERROR.BLE_ERROR_FAILED)

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
            self._gtl_wait_queue_flush_all()

            # TODO
            self.dev_params_acquire()
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

    def _rest_wait_queue_add(self, conn_idx: int, msg_id: int, ext_id: int, cb: Callable, param: object) -> None:
        item = WaitQueueElement(conn_idx=conn_idx, msg_id=msg_id, ext_id=ext_id, cb=cb, param=param)
        self._reset_wait_q.add(item)

    def get_dev_version_cmd_handler(self, command: BleMgrCommonGetDevVersionCmd):
        # This will result in a GapmDevVersionInd event (see get_dev_version_evt_handler())
        gtl = GapmGetDevVersionCmd()
        gtl.parameters = gapm_get_dev_info_cmd(GAPM_OPERATION.GAPM_GET_DEV_VERSION)
        self._adapter_command_queue_send(gtl)

    def get_dev_version_evt_handler(self, gtl: GapmDevVersionInd):
        # put item on wait queue to wait for the GAPM_CMP_EVT
        response = BleMgrCommonGetDevVersionRsp(status=BLE_ERROR.BLE_ERROR_FAILED)
        response.hci_ver = gtl.parameters.hci_ver
        response.lmp_ver = gtl.parameters.lmp_ver
        response.host_ver = gtl.parameters.host_ver
        response.hci_subver = gtl.parameters.hci_subver
        response.lmp_subver = gtl.parameters.lmp_subver
        response.host_subver = gtl.parameters.host_subver
        response.manuf_name = gtl.parameters.manuf_name
        self._gtl_wait_queue_add(BLE_CONN_IDX_INVALID,
                                 GAPM_MSG_ID.GAPM_CMP_EVT,
                                 GAPM_OPERATION.GAPM_GET_DEV_VERSION,
                                 self._get_dev_version_rsp_handler,
                                 response)

    def reset_cmd_handler(self, command: BleMgrCommonResetCmd):
        self._set_status(BLE_STATUS.BLE_IS_RESET)
        self._mgr_event_queue_flush()
        self._rest_wait_queue_add(BLE_CONN_IDX_INVALID, GAPM_MSG_ID.GAPM_CMP_EVT, GAPM_OPERATION.GAPM_RESET, self._reset_rsp_handler, None)
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
