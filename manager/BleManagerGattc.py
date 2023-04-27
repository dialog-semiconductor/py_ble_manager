import asyncio
from ctypes import c_uint8

from ble_api.BleAtt import ATT_ERROR, AttUuid
from ble_api.BleCommon import BleEventBase, BLE_ERROR
from ble_api.BleGattc import BleEventGattcDiscoverSvc, BleEventGattcDiscoverCompleted, GATTC_DISCOVERY_TYPE, \
    BleEventGattcDiscoverChar, BleEventGattcDiscoverDesc, BleEventGattcBrowseSvc, BleEventGattcBrowseCompleted, \
    GattcItem, GATTC_ITEM_TYPE, GattcServiceData, GattcCharacteristicData, BleEventGattcReadCompleted,\
    BleEventGattcWriteCompleted, BleEventGattcNotification, BleEventGattcIndication
from gtl_messages.gtl_message_base import GtlMessageBase
from gtl_messages.gtl_message_gattc import GattcDiscCmd, GattcDiscSvcInd, GattcCmpEvt, GattcDiscCharInd, GattcSdpSvcDiscCmd, \
    GattcSdpSvcInd, GattcReadCmd, GattcReadInd, GattcWriteCmd, GattcEventInd, GattcEventReqInd, GattcEventCfm, \
    GattcWriteExecuteCmd
from gtl_port.gattc_task import GATTC_OPERATION, GATTC_MSG_ID, gattc_sdp_att_info, GATTC_SDP_ATT_TYPE, gattc_read_simple
from gtl_port.rwble_hl_error import HOST_STACK_ERROR_CODE
from manager.BleManagerBase import BleManagerBase
from manager.BleManagerGattcMsgs import BLE_CMD_GATTC_OPCODE, BleMgrGattcDiscoverSvcCmd, \
    BleMgrGattcDiscoverSvcRsp, BleMgrGattcDiscoverCharCmd, BleMgrGattcDiscoverCharRsp, BleMgrGattcDiscoverDescCmd, \
    BleMgrGattcDiscoverDescRsp, BleMgrGattcBrowseCmd, BleMgrGattcBrowseRsp, BleMgrGattcReadCmd, BleMgrGattcReadRsp, \
    BleMgrGattcWriteGenericCmd, BleMgrGattcWriteGenericRsp, BleMgrGattcWriteExecuteCmd, BleMgrGattcWriteExecuteRsp
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
            BLE_CMD_GATTC_OPCODE.BLE_MGR_GATTC_BROWSE_CMD: self.browse_cmd_handler,
            BLE_CMD_GATTC_OPCODE.BLE_MGR_GATTC_BROWSE_RANGE_CMD: None,
            BLE_CMD_GATTC_OPCODE.BLE_MGR_GATTC_DISCOVER_SVC_CMD: self.discover_svc_cmd_handler,
            BLE_CMD_GATTC_OPCODE.BLE_MGR_GATTC_DISCOVER_INCLUDE_CMD: None,
            BLE_CMD_GATTC_OPCODE.BLE_MGR_GATTC_DISCOVER_CHAR_CMD: self.discover_char_cmd_handler,
            BLE_CMD_GATTC_OPCODE.BLE_MGR_GATTC_DISCOVER_DESC_CMD: self.discover_desc_cmd_handler,
            BLE_CMD_GATTC_OPCODE.BLE_MGR_GATTC_READ_CMD: self.read_cmd_handler,
            BLE_CMD_GATTC_OPCODE.BLE_MGR_GATTC_WRITE_GENERIC_CMD: self.write_generic_cmd_handler,
            BLE_CMD_GATTC_OPCODE.BLE_MGR_GATTC_WRITE_EXECUTE_CMD: self.write_execute_cmd_handler,
            BLE_CMD_GATTC_OPCODE.BLE_MGR_GATTC_EXCHANGE_MTU_CMD: None,

        }

        self.evt_handlers = {
            # Ble Manager calls cmp_evt_handler directly as it determines if gatts or gattc is the appropriate handler
            # GATTC_MSG_ID.GATTC_CMP_EVT: self.cmp_evt_handler,
            GATTC_MSG_ID.GATTC_MTU_CHANGED_IND: None,
            GATTC_MSG_ID.GATTC_SDP_SVC_IND: self.sdp_svc_ind_evt_handler,
            GATTC_MSG_ID.GATTC_DISC_SVC_IND: self.disc_svc_ind_evt_handler,
            GATTC_MSG_ID.GATTC_DISC_SVC_INCL_IND: None,
            GATTC_MSG_ID.GATTC_DISC_CHAR_IND: self.disc_char_ind_evt_handler,
            GATTC_MSG_ID.GATTC_DISC_CHAR_DESC_IND: self.disc_char_desc_ind_evt_handler,
            GATTC_MSG_ID.GATTC_READ_IND: self.read_ind_evt_handler,
            GATTC_MSG_ID.GATTC_EVENT_IND: self.event_ind_evt_handler,  # Notifications
            GATTC_MSG_ID.GATTC_EVENT_REQ_IND: self.event_req_ind_evt_handler,  # Indications
            GATTC_MSG_ID.GATTC_SVC_CHANGED_CFG_IND: None,
        }

    def _cmp_browse_evt_handler(self, gtl: GattcCmpEvt):
        evt = BleEventGattcBrowseCompleted()
        evt.conn_idx = self._task_to_connidx(gtl.src_id)
        if (gtl.parameters.status == HOST_STACK_ERROR_CODE.ATT_ERR_NO_ERROR):
            evt.status = BLE_ERROR.BLE_STATUS_OK
        else:
            evt.status = BLE_ERROR.BLE_ERROR_FAILED

        self._mgr_event_queue_send(evt)

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

    def _cmp_read_evt_handler(self, gtl: GattcCmpEvt):

        # if no error ignore, we replied in read_ind_evt_handler()
        if gtl.parameters.status != HOST_STACK_ERROR_CODE.ATT_ERR_NO_ERROR:
            evt = BleEventGattcReadCompleted()
            evt.conn_idx = self._task_to_connidx(gtl.src_id)
            evt.handle = gtl.parameters.seq_num
            evt.status = gtl.parameters.status
            self._mgr_event_queue_send(evt)

    def _cmp_write_evt_handler(self, gtl: GattcCmpEvt):
        evt = BleEventGattcWriteCompleted()
        evt.conn_idx = self._task_to_connidx(gtl.src_id)
        evt.handle = gtl.parameters.seq_num
        evt.status = ATT_ERROR(gtl.parameters.status)
        evt.operation = gtl.parameters.operation
        self._mgr_event_queue_send(evt)

    def browse_cmd_handler(self, command: BleMgrGattcBrowseCmd):
        response = BleMgrGattcBrowseRsp(BLE_ERROR.BLE_ERROR_FAILED)
        dev = self._stored_device_list.find_device_by_conn_idx(command.conn_idx)
        if not dev:
            response.status = BLE_ERROR.BLE_ERROR_NOT_CONNECTED
        else:
            gtl = GattcSdpSvcDiscCmd(conidx=command.conn_idx)
            if command.uuid:
                gtl.parameters.operation = GATTC_OPERATION.GATTC_SDP_DISC_SVC
                gtl.parameters.uuid = (c_uint8 * len(command.uuid.uuid)).from_buffer_copy(command.uuid.uuid)
            else:
                gtl.parameters.operation = GATTC_OPERATION.GATTC_SDP_DISC_SVC_ALL

            gtl.parameters.start_hdl = 1
            gtl.parameters.end_hdl = 0xFFFF
            self._adapter_command_queue_send(gtl)
            response.status = BLE_ERROR.BLE_STATUS_OK

        self._mgr_response_queue_send(response)

    def cmp_evt_handler(self, gtl: GattcCmpEvt):

        match gtl.parameters.operation:

            case GATTC_OPERATION.GATTC_SVC_CHANGED:
                pass
            case (GATTC_OPERATION.GATTC_SDP_DISC_SVC
                    | GATTC_OPERATION.GATTC_SDP_DISC_SVC_ALL):

                self._cmp_browse_evt_handler(gtl)

            case (GATTC_OPERATION.GATTC_DISC_BY_UUID_SVC
                    | GATTC_OPERATION.GATTC_DISC_BY_UUID_CHAR
                    | GATTC_OPERATION.GATTC_DISC_ALL_SVC
                    | GATTC_OPERATION.GATTC_DISC_ALL_CHAR
                    | GATTC_OPERATION.GATTC_DISC_DESC_CHAR
                    | GATTC_OPERATION.GATTC_DISC_INCLUDED_SVC):

                self._cmp_discovery_evt_handler(gtl)

            case GATTC_OPERATION.GATTC_READ:
                # TODO should not return value
                return self._cmp_read_evt_handler(gtl)

            case (GATTC_OPERATION.GATTC_WRITE
                    | GATTC_OPERATION.GATTC_WRITE_NO_RESPONSE
                    | GATTC_OPERATION.GATTC_EXEC_WRITE):

                self._cmp_write_evt_handler(gtl)

            case GATTC_OPERATION.GATTC_MTU_EXCH:
                pass
            case _:
                return False

        return True

    def disc_char_ind_evt_handler(self, gtl: GattcDiscCharInd):
        evt = BleEventGattcDiscoverChar()
        evt.conn_idx = self._task_to_connidx(gtl.src_id)
        evt.uuid.uuid = bytes(gtl.parameters.uuid)
        evt.handle = gtl.parameters.attr_hdl
        evt.value_handle = gtl.parameters.pointer_hdl
        evt.properties = gtl.parameters.prop
        self._mgr_event_queue_send(evt)

    def disc_char_desc_ind_evt_handler(self, gtl: GattcDiscCharInd):
        evt = BleEventGattcDiscoverDesc()
        evt.conn_idx = self._task_to_connidx(gtl.src_id)
        evt.uuid.uuid = bytes(gtl.parameters.uuid)
        evt.handle = gtl.parameters.attr_hdl
        self._mgr_event_queue_send(evt)

    def disc_svc_ind_evt_handler(self, gtl: GattcDiscSvcInd):
        evt = BleEventGattcDiscoverSvc()
        evt.conn_idx = self._task_to_connidx(gtl.src_id)
        evt.start_h = gtl.parameters.start_hdl
        evt.end_h = gtl.parameters.end_hdl
        evt.uuid.uuid = bytes(gtl.parameters.uuid)
        self._mgr_event_queue_send(evt)

    def discover_char_cmd_handler(self, command: BleMgrGattcDiscoverCharCmd):

        response = BleMgrGattcDiscoverCharRsp(BLE_ERROR.BLE_ERROR_FAILED)

        dev = self._stored_device_list.find_device_by_conn_idx(command.conn_idx)
        if not dev:
            response.status = BLE_ERROR.BLE_ERROR_NOT_CONNECTED
        else:
            gtl = GattcDiscCmd(conidx=command.conn_idx)
            # depends on uuid default to None in BleMgrGattcDiscoverCharCmd
            if command.uuid:
                gtl.parameters.operation = GATTC_OPERATION.GATTC_DISC_BY_UUID_CHAR
                gtl.parameters.uuid = (c_uint8 * len(command.uuid.uuid)).from_buffer_copy(command.uuid.uuid)
            else:
                gtl.parameters.operation = GATTC_OPERATION.GATTC_DISC_ALL_CHAR
                gtl.parameters.uuid = (c_uint8 * 2)()

            gtl.parameters.seq_num = command.conn_idx
            gtl.parameters.start_hdl = command.start_h
            gtl.parameters.end_hdl = command.end_h
            self._adapter_command_queue_send(gtl)
            response.status = BLE_ERROR.BLE_STATUS_OK

        self._mgr_response_queue_send(response)

    # TODO discovering descriptors needs to be tested
    def discover_desc_cmd_handler(self, command: BleMgrGattcDiscoverDescCmd):
        response = BleMgrGattcDiscoverDescRsp(BLE_ERROR.BLE_ERROR_FAILED)

        dev = self._stored_device_list.find_device_by_conn_idx(command.conn_idx)
        if not dev:
            response.status = BLE_ERROR.BLE_ERROR_NOT_CONNECTED
        else:
            gtl = GattcDiscCmd(conidx=command.conn_idx)
            gtl.parameters.operation = GATTC_OPERATION.GATTC_DISC_DESC_CHAR
            gtl.parameters.uuid = (c_uint8 * 2)()
            gtl.parameters.seq_num = command.conn_idx
            gtl.parameters.start_hdl = command.start_h
            gtl.parameters.end_hdl = command.end_h
            self._adapter_command_queue_send(gtl)
            response.status = BLE_ERROR.BLE_STATUS_OK

        self._mgr_response_queue_send(response)

    def discover_svc_cmd_handler(self, command: BleMgrGattcDiscoverSvcCmd):
        response = BleMgrGattcDiscoverSvcRsp(BLE_ERROR.BLE_ERROR_FAILED)

        dev = self._stored_device_list.find_device_by_conn_idx(command.conn_idx)

        if not dev:
            response.status = BLE_ERROR.BLE_ERROR_NOT_CONNECTED
        else:
            gtl = GattcDiscCmd(conidx=command.conn_idx)
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

    def event_ind_evt_handler(self, gtl: GattcEventInd) -> None:
        # ignore if type wrong
        if gtl.parameters.type == GATTC_OPERATION.GATTC_NOTIFY:
            evt = BleEventGattcNotification()
            evt.conn_idx = self._task_to_connidx(gtl.src_id)
            evt.handle = gtl.parameters.handle
            evt.value = bytes(gtl.parameters.value)
            self._mgr_event_queue_send(evt)

    def event_req_ind_evt_handler(self, gtl: GattcEventReqInd) -> None:
        # ignore if type wrong
        if gtl.parameters.type == GATTC_OPERATION.GATTC_INDICATE:

            # Confirm indication received
            cfm = GattcEventCfm(conidx=self._task_to_connidx(gtl.src_id))
            cfm.parameters.handle = gtl.parameters.handle
            self._adapter_command_queue_send(cfm)

            evt = BleEventGattcIndication()
            evt.conn_idx = self._task_to_connidx(gtl.src_id)
            evt.handle = gtl.parameters.handle
            evt.value = bytes(gtl.parameters.value)
            self._mgr_event_queue_send(evt)

    def read_ind_evt_handler(self, gtl: GattcReadInd):  # TODO need to test
        evt = BleEventGattcReadCompleted()
        evt.conn_idx = self._task_to_connidx(gtl.src_id)
        evt.handle = gtl.parameters.handle
        evt.status = ATT_ERROR.ATT_ERROR_OK
        evt.offset = gtl.parameters.offset
        evt.value = bytes(gtl.parameters.value)
        self._mgr_event_queue_send(evt)

    def read_cmd_handler(self, command: BleMgrGattcReadCmd):  # TODO need to test
        response = BleMgrGattcReadRsp(BLE_ERROR.BLE_ERROR_FAILED)

        dev = self._stored_device_list.find_device_by_conn_idx(command.conn_idx)
        if not dev:
            response.status = BLE_ERROR.BLE_ERROR_NOT_CONNECTED
        else:
            gtl = GattcReadCmd(conidx=command.conn_idx)
            gtl.parameters.operation = GATTC_OPERATION.GATTC_READ
            gtl.parameters.seq_num = command.handle
            gtl.parameters.req.simple = gattc_read_simple()
            gtl.parameters.req.simple.handle = command.handle
            gtl.parameters.req.simple.offset = command.offset
            gtl.parameters.req.simple.length = 0
            self._adapter_command_queue_send(gtl)
            response.status = BLE_ERROR.BLE_STATUS_OK

        self._mgr_response_queue_send(response)

    def sdp_svc_ind_evt_handler(self, gtl: GattcSdpSvcInd):
        evt = BleEventGattcBrowseSvc()
        num_handles = gtl.parameters.end_hdl - gtl.parameters.start_hdl
        num_items = 0
        for i in range(0, num_handles):
            att_type = gtl.parameters.info[i].att_type

            # Value is not a separate item - it's part of the characteristic item
            if (att_type != GATTC_SDP_ATT_TYPE.GATTC_SDP_NONE and att_type != GATTC_SDP_ATT_TYPE.GATTC_SDP_ATT_VAL):
                num_items += 1

        evt.conn_idx = self._task_to_connidx(gtl.src_id)
        evt.start_h = gtl.parameters.start_hdl
        evt.end_h = gtl.parameters.end_hdl
        evt.uuid.uuid = bytes(gtl.parameters.uuid[:gtl.parameters.uuid_len])

        ignore = False
        for i in range(0, num_handles):
            info: gattc_sdp_att_info = gtl.parameters.info[i]
            if (info.att_type != GATTC_SDP_ATT_TYPE.GATTC_SDP_NONE
                    and info.att_type != GATTC_SDP_ATT_TYPE.GATTC_SDP_ATT_VAL):

                item = GattcItem()
                item.handle = gtl.parameters.start_hdl + i + 1

                match info.att_type:
                    case GATTC_SDP_ATT_TYPE.GATTC_SDP_INC_SVC:
                        # TODO  TYPE DOES NOT SEEM TO BE RECOGNIZED
                        item.type = GATTC_ITEM_TYPE.GATTC_ITEM_TYPE_INCLUDE
                        item.service_data = GattcServiceData()
                        item.service_data.start_h = info.inc_svc.start_hdl
                        item.service_data.end_h = info.inc_svc.end_hdl
                        item.uuid = AttUuid(bytes(info.inc_svc.uuid))
                    case GATTC_SDP_ATT_TYPE.GATTC_SDP_ATT_CHAR:
                        item.type = GATTC_ITEM_TYPE.GATTC_ITEM_TYPE_CHARACTERISTIC
                        item.char_data = GattcCharacteristicData()
                        item.char_data.value_handle = info.att_char.handle
                        item.char_data.properties = info.att_char.prop

                        if (info.att_char.handle > gtl.parameters.end_hdl):
                            ignore = True
                            break

                        info = gtl.parameters.info[info.att_char.handle - gtl.parameters.start_hdl - 1]
                        if (info.att_type != GATTC_SDP_ATT_TYPE.GATTC_SDP_ATT_VAL):
                            ignore = True
                            break

                        item.uuid = AttUuid(bytes(info.att.uuid[:info.att.uuid_len]))

                    case GATTC_SDP_ATT_TYPE.GATTC_SDP_ATT_DESC:
                        item.type = GATTC_ITEM_TYPE.GATTC_ITEM_TYPE_DESCRIPTOR
                        item.uuid = AttUuid(bytes(info.att.uuid[:info.att.uuid_len]))

                evt.items.append(item)
                evt.num_items += 1

        if not ignore:
            self._mgr_event_queue_send(evt)

    def write_execute_cmd_handler(self, command: BleMgrGattcWriteExecuteCmd):
        response = BleMgrGattcWriteExecuteRsp(BLE_ERROR.BLE_ERROR_FAILED)
        dev = self._stored_device_list.find_device_by_conn_idx(command.conn_idx)
        if not dev:
            response.status = BLE_ERROR.BLE_ERROR_NOT_CONNECTED
        else:
            gtl = GattcWriteExecuteCmd(conidx=command.conn_idx)
            gtl.parameters.execute = command.commit
            gtl.parameters.seq_num = 0  # make this '0' so we can handle in the same handler as other writes
                                        # attribute handle '0' means 'execute write' there
            self._adapter_command_queue_send(gtl)
            response.status = BLE_ERROR.BLE_STATUS_OK

        self._mgr_response_queue_send(response)

    def write_generic_cmd_handler(self, command: BleMgrGattcWriteGenericCmd):
        response = BleMgrGattcWriteGenericRsp(BLE_ERROR.BLE_ERROR_FAILED)

        dev = self._stored_device_list.find_device_by_conn_idx(command.conn_idx)
        if not dev:
            response.status = BLE_ERROR.BLE_ERROR_NOT_CONNECTED
        else:
            gtl = GattcWriteCmd(conidx=command.conn_idx)
            if command.no_response:
                gtl.parameters.operation = GATTC_OPERATION.GATTC_WRITE_NO_RESPONSE
                if command.signed_write:
                    if not dev.encrypted:
                        gtl.parameters.operation = GATTC_OPERATION.GATTC_WRITE_SIGNED
            else:
                gtl.parameters.operation = GATTC_OPERATION.GATTC_WRITE
                gtl.parameters.auto_execute = False if command.prepare else True
                gtl.parameters.offset = command.offset

            gtl.parameters.seq_num = command.handle
            gtl.parameters.handle = command.handle
            gtl.parameters.value = (c_uint8 * len(command.value)).from_buffer_copy(command.value)

            self._adapter_command_queue_send(gtl)
            response.status = BLE_ERROR.BLE_STATUS_OK

        self._mgr_response_queue_send(response)


'''
static const ble_mgr_cmd_handler_t h_gattc[BLE_MGR_CMD_GET_IDX(BLE_MGR_GATTC_LAST_CMD)] = {
        ble_mgr_gattc_browse_cmd_handler,               STARTED
        ble_mgr_gattc_browse_range_cmd_handler,
        ble_mgr_gattc_discover_svc_cmd_handler,         STARTED
        ble_mgr_gattc_discover_include_cmd_handler,
        ble_mgr_gattc_discover_char_cmd_handler,        STARTED
        ble_mgr_gattc_discover_desc_cmd_handler,        STARTED
        ble_mgr_gattc_read_cmd_handler,                 STARTED UNTESTED
        ble_mgr_gattc_write_generic_cmd_handler,        STARTED UNTESTED
        ble_mgr_gattc_write_execute_cmd_handler,
        ble_mgr_gattc_exchange_mtu_cmd_handler,
};

void ble_mgr_gattc_mtu_changed_ind_evt_handler(ble_gtl_msg_t *gtl);
void ble_mgr_gattc_sdp_svc_ind_evt_handler(ble_gtl_msg_t *gtl);
void ble_mgr_gattc_cmp__browse_evt_handler(ble_gtl_msg_t *gtl);             STARTED
void ble_mgr_gattc_disc_svc_ind_evt_handler(ble_gtl_msg_t *gtl);            STARTED
void ble_mgr_gattc_disc_svc_incl_ind_evt_handler(ble_gtl_msg_t *gtl);
void ble_mgr_gattc_disc_char_ind_evt_handler(ble_gtl_msg_t *gtl);           STARTED
void ble_mgr_gattc_disc_char_desc_ind_evt_handler(ble_gtl_msg_t *gtl);      STARTED UNTESTED
void ble_mgr_gattc_cmp__discovery_evt_handler(ble_gtl_msg_t *gtl);          STARTED
void ble_mgr_gattc_read_ind_evt_handler(ble_gtl_msg_t *gtl);                STARTED UNTESTED
void ble_mgr_gattc_cmp__read_evt_handler(ble_gtl_msg_t *gtl);               STARTED UNTESTED
void ble_mgr_gattc_cmp__write_evt_handler(ble_gtl_msg_t *gtl);              STARTED UNTESTED
void ble_mgr_gattc_event_ind_evt_handler(ble_gtl_msg_t *gtl);
void ble_mgr_gattc_event_req_ind_evt_handler(ble_gtl_msg_t *gtl);
void ble_mgr_gattc_svc_changed_cfg_ind_evt_handler(ble_gtl_msg_t *gtl);

'''
