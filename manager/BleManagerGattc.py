import asyncio
from ctypes import c_uint8

from ble_api.BleAtt import ATT_UUID_TYPE, AttUuid
from ble_api.BleCommon import BleEventBase, BLE_ERROR
from ble_api.BleGattc import BleEventGattcDiscoverSvc, BleEventGattcDiscoverCompleted, GATTC_DISCOVERY_TYPE
from gtl_messages.gtl_message_base import GtlMessageBase
from gtl_messages.gtl_message_gattc import GattcDiscCmd, GattcDiscSvcInd, GattcCmpEvt
from gtl_port.gattc_task import GATTC_OPERATION, GATTC_MSG_ID
from gtl_port.rwble_hl_error import HOST_STACK_ERROR_CODE
from manager.BleManagerBase import BleManagerBase
from manager.BleManagerCommonMsgs import BleMgrMsgBase
from manager.BleManagerGattcMsgs import BLE_CMD_GATTC_OPCODE, BleMgrGattcDiscoverSvcCmd, BleMgrGattcDiscoverSvcRsp
from manager.BleManagerStorage import StoredDeviceQueue
from manager.GtlWaitQueue import GtlWaitQueue


class BleManagerGattc(BleManagerBase):

    def __init__(self,
                 mgr_response_q: asyncio.Queue[BLE_ERROR],
                 mgr_event_q: asyncio.Queue[BleEventBase],
                 adapter_command_q: asyncio.Queue[GtlMessageBase],
                 wait_q: GtlWaitQueue,
                 stored_device_q: StoredDeviceQueue) -> None:

        super().__init__(mgr_response_q, mgr_event_q, adapter_command_q, wait_q, stored_device_q)

        self.cmd_handlers = {
            BLE_CMD_GATTC_OPCODE.BLE_MGR_GATTC_DISCOVER_SVC_CMD: self.discover_svc_cmd_handler,
        }

        self.evt_handlers = {
            # Ble Manager calls cmp_evt_handler directly as it determines if gatts or gattc is the appropriate handler
            # GATTC_MSG_ID.GATTC_CMP_EVT: self.cmp_evt_handler,
            GATTC_MSG_ID.GATTC_DISC_SVC_IND: self.disc_svc_ind_evt_handler,
        }

    def _cmp_discovery_evt_handler(self, gtl: GattcCmpEvt):
        evt = BleEventGattcDiscoverCompleted()
        evt.conn_idx = self._task_to_connidx(gtl.src_id)
        if (gtl.parameters.status == HOST_STACK_ERROR_CODE.ATT_ERR_NO_ERROR 
                or gtl.parameters.status == HOST_STACK_ERROR_CODE.ATT_ERR_ATTRIBUTE_NOT_FOUND):

            evt.status = BLE_ERROR.BLE_STATUS_OK
        else:
            evt.status = BLE_ERROR.BLE_ERROR_FAILED

        match gtl.parameters.operation:
            case (GATTC_OPERATION.GATTC_DISC_ALL_SVC
                    | GATTC_OPERATION.GATTC_DISC_BY_UUID_SVC):

                evt.type = GATTC_DISCOVERY_TYPE.GATTC_DISCOVERY_TYPE_SVC

            case GATTC_OPERATION.GATTC_DISC_INCLUDED_SVC:
                evt.type = GATTC_DISCOVERY_TYPE.GATTC_DISCOVERY_TYPE_INCLUDED

            case (GATTC_OPERATION.GATTC_DISC_ALL_CHAR
                    | GATTC_OPERATION.GATTC_DISC_BY_UUID_CHAR):

                evt.type = GATTC_DISCOVERY_TYPE.GATTC_DISCOVERY_TYPE_CHARACTERISTICS

            case GATTC_OPERATION.GATTC_DISC_DESC_CHAR:
                evt.type = GATTC_DISCOVERY_TYPE.GATTC_DISCOVERY_TYPE_DESCRIPTORS

        self._mgr_event_queue_send(evt)

    def cmp_evt_handler(self, gtl: GattcCmpEvt):

        match gtl.parameters.operation:
            case (GATTC_OPERATION.GATTC_DISC_BY_UUID_SVC 
                    | GATTC_OPERATION.GATTC_DISC_BY_UUID_CHAR
                    | GATTC_OPERATION.GATTC_DISC_ALL_SVC
                    | GATTC_OPERATION.GATTC_DISC_ALL_CHAR
                    | GATTC_OPERATION.GATTC_DISC_DESC_CHAR
                    | GATTC_OPERATION.GATTC_DISC_INCLUDED_SVC):

                self._cmp_discovery_evt_handler(gtl)
            case _:
                print("BleManagerGattc cmp_evt_handler unhandled event")
                return False

        return True

    def disc_svc_ind_evt_handler(self, gtl: GattcDiscSvcInd):
        evt = BleEventGattcDiscoverSvc()
        evt.conn_idx = self._task_to_connidx(gtl.src_id)
        evt.start_h = gtl.parameters.start_hdl
        evt.end_h = gtl.parameters.end_hdl
        evt.uuid.uuid = bytes(gtl.parameters.uuid)
        self._mgr_event_queue_send(evt)

    def discover_svc_cmd_handler(self, command: BleMgrGattcDiscoverSvcCmd):
        response = BleMgrGattcDiscoverSvcRsp(BLE_ERROR.BLE_ERROR_FAILED)

        dev = self._stored_device_list.find_device_by_conn_idx(command.conn_idx)
        if not dev:
            response.status = BLE_ERROR.BLE_ERROR_NOT_CONNECTED
        else:
            gtl = GattcDiscCmd()
            # depends on uuid default to None in BleMgrGattcDiscoverSvcCmd
            if command.uuid:
                gtl.parameters.operation = GATTC_OPERATION.GATTC_DISC_BY_UUID_SVC
                gtl.parameters.uuid = (c_uint8 * len(command.uuid.uuid)).from_buffer_copy(command.uuid.uuid)
            else:
                gtl.parameters.operation = GATTC_OPERATION.GATTC_DISC_ALL_SVC
                gtl.parameters.uuid = (c_uint8 * 2)()

            gtl.parameters.seq_num = command.conn_idx
            gtl.parameters.start_hdl = 1
            gtl.parameters.end_hdl = 0xFFFF

            self._adapter_command_queue_send(gtl)

            response.status = BLE_ERROR.BLE_STATUS_OK

        self._mgr_response_queue_send(response)


'''
static const ble_mgr_cmd_handler_t h_gattc[BLE_MGR_CMD_GET_IDX(BLE_MGR_GATTC_LAST_CMD)] = {
        ble_mgr_gattc_browse_cmd_handler,
        ble_mgr_gattc_browse_range_cmd_handler,
        ble_mgr_gattc_discover_svc_cmd_handler,
        ble_mgr_gattc_discover_include_cmd_handler,
        ble_mgr_gattc_discover_char_cmd_handler,
        ble_mgr_gattc_discover_desc_cmd_handler,
        ble_mgr_gattc_read_cmd_handler,
        ble_mgr_gattc_write_generic_cmd_handler,
        ble_mgr_gattc_write_execute_cmd_handler,
        ble_mgr_gattc_exchange_mtu_cmd_handler,
};

void ble_mgr_gattc_mtu_changed_ind_evt_handler(ble_gtl_msg_t *gtl);
void ble_mgr_gattc_sdp_svc_ind_evt_handler(ble_gtl_msg_t *gtl);
void ble_mgr_gattc_cmp__browse_evt_handler(ble_gtl_msg_t *gtl);
void ble_mgr_gattc_disc_svc_ind_evt_handler(ble_gtl_msg_t *gtl);
void ble_mgr_gattc_disc_svc_incl_ind_evt_handler(ble_gtl_msg_t *gtl);
void ble_mgr_gattc_disc_char_ind_evt_handler(ble_gtl_msg_t *gtl);
void ble_mgr_gattc_disc_char_desc_ind_evt_handler(ble_gtl_msg_t *gtl);
void ble_mgr_gattc_cmp__discovery_evt_handler(ble_gtl_msg_t *gtl);
void ble_mgr_gattc_read_ind_evt_handler(ble_gtl_msg_t *gtl);
void ble_mgr_gattc_cmp__read_evt_handler(ble_gtl_msg_t *gtl);
void ble_mgr_gattc_cmp__write_evt_handler(ble_gtl_msg_t *gtl);
void ble_mgr_gattc_event_ind_evt_handler(ble_gtl_msg_t *gtl);
void ble_mgr_gattc_event_req_ind_evt_handler(ble_gtl_msg_t *gtl);
void ble_mgr_gattc_svc_changed_cfg_ind_evt_handler(ble_gtl_msg_t *gtl);

'''
