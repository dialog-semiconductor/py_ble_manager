import asyncio
from ctypes import c_uint8

from ble_api.BleAtt import ATT_PERM, ATT_UUID_TYPE
from ble_api.BleCommon import BLE_ERROR, BleEventBase
from ble_api.BleGap import BLE_CONN_IDX_INVALID
from ble_api.BleGatt import GATT_SERVICE, GATT_PROP, GATT_EVENT
from ble_api.BleGatts import BleEventGattsReadReq, BleEventGattsWriteReq, BleEventGattsEventSent
from ble_api.BleUuid import UUID_GATT_CHAR_EXT_PROPERTIES
from gtl_messages.gtl_message_gattc import GattcReadReqInd, GattcReadCfm, GattcWriteCfm, GattcWriteReqInd, GattcSendEvtCmd, \
    GATTC_OPERATION, GattcCmpEvt
from gtl_messages.gtl_message_gattm import GattmAddSvcReq, GattmAddSvcRsp, GattmAttSetValueReq, GattmAttSetValueRsp
from gtl_port.attm import ATTM_PERM, ATTM_UUID_LEN, ATTM_SERVICE_TYPE, ATTM_BROADCAST, ATTM_ENC_KEY_SIZE_16_BYTES, \
    ATTM_EXTENDED_PROPERTIES, ATTM_WRITE_SIGNED, ATTM_WRITE_REQUEST
from gtl_port.gattc_task import GATTC_MSG_ID
from gtl_port.gattm_task import gattm_att_desc, att_perm, att_max_len_read_ind, GATTM_MSG_ID
from gtl_port.rwble_hl_error import HOST_STACK_ERROR_CODE
from manager.BleManagerBase import BleManagerBase
from manager.BleManagerCommonMsgs import BleMgrMsgBase
from manager.BleManagerGattsMsgs import BLE_CMD_GATTS_OPCODE, BleMgrGattsReadCfmCmd, BleMgrGattsServiceRegisterRsp, \
    BleMgrGattsReadCfmRsp, BleMgrGattsServiceAddCharacteristicCmd, BleMgrGattsServiceAddCharacteristicRsp, \
    BleMgrGattsServiceAddCmd, BleMgrGattsServiceAddRsp, BleMgrGattsServiceRegisterCmd, BleMgrGattsSetValueCmd, \
    BleMgrGattsSetValueRsp, BleMgrGattsWriteCfmCmd, BleMgrGattsWriteCfmRsp, BleMgrGattsSendEventCmd, BleMgrGattsSendEventRsp, \
    BleMgrGattsServiceAddDescriptorCmd, BleMgrGattsServiceAddDescriptorRsp
from manager.GtlWaitQueue import GtlWaitQueue


class BleManagerGatts(BleManagerBase):

    def __init__(self,
                 mgr_response_q: asyncio.Queue[BLE_ERROR],
                 mgr_event_q: asyncio.Queue[BleEventBase],
                 adapter_command_q: asyncio.Queue[BleMgrMsgBase],
                 wait_q: GtlWaitQueue) -> None:

        super().__init__(mgr_response_q, mgr_event_q, adapter_command_q, wait_q)

        self.cmd_handlers = {
            BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_SERVICE_ADD_CMD: self.service_add_cmd_handler,
            BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_SERVICE_CHARACTERISTIC_ADD_CMD: self.service_add_characteristic_cmd_handler,
            BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_SERVICE_DESCRIPTOR_ADD_CMD: self.service_add_descriptor_cmd_handler,
            BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_SERVICE_REGISTER_CMD: self.service_register_cmd_handler,
            BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_READ_CFM_CMD: self.read_cfm_cmd_handler,
            BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_SET_VALUE_CMD: self.set_value_cmd_handler,
            BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_WRITE_CFM_CMD: self.write_cfm_cmd_handler,
            BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_SEND_EVENT_CMD: self.send_event_cmd_handler,
        }

        self.evt_handlers = {
            GATTC_MSG_ID.GATTC_READ_REQ_IND: self.read_value_req_evt_handler,  # TODO why is this in Gatts and not Gattc???
            GATTC_MSG_ID.GATTC_WRITE_REQ_IND: self.write_value_req_evt_handler,   # TODO why is this in Gatts and not Gattc???
            GATTC_MSG_ID.GATTC_CMP_EVT: self.cmp_evt_handler,   # TODO why is this in Gatts and not Gattc???
        }

        self._add_svc_msg = None
        self._attr_idx = 0
        self._extended_prop = 0

    # TODO need to rethink logic of this function as SDK using |= 
    def _api_to_rwperm(self, prop: GATT_PROP, perm: ATTM_PERM, uuid_type: ATT_UUID_TYPE, current_perm: att_perm = None,):

        rwperm = current_perm if current_perm else att_perm()

        if (prop & GATT_PROP.GATT_PROP_BROADCAST):
            rwperm.broadcast |= ATTM_BROADCAST.YES

        if (prop & GATT_PROP.GATT_PROP_WRITE_NO_RESP):
            rwperm.write |= ATTM_PERM.ENABLE

        if (prop & GATT_PROP.GATT_PROP_WRITE):
            rwperm.write_request |= ATTM_WRITE_REQUEST.ACCEPTED

        if (prop & GATT_PROP.GATT_PROP_NOTIFY):
            rwperm.notification |= ATTM_PERM.ENABLE

        if (prop & GATT_PROP.GATT_PROP_INDICATE):
            rwperm.indication |= ATTM_PERM.ENABLE

        if (prop & GATT_PROP.GATT_PROP_WRITE_SIGNED):
            rwperm.write_signed |= ATTM_WRITE_SIGNED.ACCEPTED

        if (prop & GATT_PROP.GATT_PROP_EXTENDED):
            rwperm.extended_properties_present |= ATTM_EXTENDED_PROPERTIES.YES

        # Translate read permissions
        if (perm & ATT_PERM.ATT_PERM_READ_AUTH):
            rwperm.read |= ATTM_PERM.AUTH
        elif (perm & ATT_PERM.ATT_PERM_READ_ENCRYPT):
            rwperm.read |= ATTM_PERM.UNAUTH
        elif (perm & ATT_PERM.ATT_PERM_READ):
            rwperm.read |= ATTM_PERM.ENABLE

        # Translate write permissions
        if (perm & ATT_PERM.ATT_PERM_WRITE_AUTH):
            rwperm.write |= ATTM_PERM.AUTH
        elif (perm & ATT_PERM.ATT_PERM_WRITE_ENCRYPT):
            rwperm.write |= ATTM_PERM.UNAUTH
        elif (perm & ATT_PERM.ATT_PERM_WRITE):
            rwperm.write |= ATTM_PERM.ENABLE

        # Translate keysize permissions
        if (perm & ATT_PERM.ATT_PERM_KEYSIZE_16):
            rwperm.enc_key_size |= ATTM_ENC_KEY_SIZE_16_BYTES.YES

        if uuid_type == ATT_UUID_TYPE.ATT_UUID_128:
            rwperm.uuid_len |= ATTM_UUID_LEN.BITS_128  # TODO confusing which ATT/ATTM is coming from where. Consider renaming

        return rwperm

    def _service_register_rsp(self, gtl: GattmAddSvcRsp, param: object = None):
        response = BleMgrGattsServiceRegisterRsp(self._task_to_connidx(gtl.src_id))
        response.handle = gtl.parameters.start_hdl

        response.status = BLE_ERROR.BLE_STATUS_OK \
            if gtl.parameters.status == HOST_STACK_ERROR_CODE.ATT_ERR_NO_ERROR \
            else BLE_ERROR.BLE_ERROR_FAILED

        self._mgr_response_queue_send(response)

    def _set_value_rsp(self, gtl: GattmAttSetValueRsp, param: object = None):
        response = BleMgrGattsSetValueRsp(BLE_ERROR.BLE_ERROR_FAILED)
        if gtl.parameters.status == HOST_STACK_ERROR_CODE.ATT_ERR_NO_ERROR:
            response.status = BLE_ERROR.BLE_STATUS_OK

        self._mgr_response_queue_send(response)

    def cmp_evt_handler(self, evt: GattcCmpEvt) -> bool:

        match evt.parameters.operation:
            case GATTC_OPERATION.GATTC_NOTIFY:
                self.event_sent_evt_handler(evt)
            case GATTC_OPERATION.GATTC_INDICATE:
                self.event_sent_evt_handler(evt)
            case GATTC_OPERATION.GATTC_SVC_CHANGED:
                pass
            case _:
                print("BleManagerGatts cmp_evt_handler unhandled event")
                return False

        return True

    def event_sent_evt_handler(self, gtl: GattcCmpEvt):
        evt = BleEventGattsEventSent()
        evt.conn_idx = self._task_to_connidx(gtl.src_id)
        evt.handle = gtl.parameters.seq_num
        if gtl.parameters.operation == GATTC_OPERATION.GATTC_NOTIFY:
            evt.type = GATT_EVENT.GATT_EVENT_NOTIFICATION
        else:
            evt.type = GATT_EVENT.GATT_EVENT_INDICATION
        evt.status = gtl.parameters.status

        # TODO remove pending events from dev in storage queue

        self._mgr_event_queue_send(evt)

    def read_cfm_cmd_handler(self, command: BleMgrGattsReadCfmCmd):

        response = BleMgrGattsReadCfmRsp(BLE_ERROR.BLE_ERROR_FAILED)
        # TODO find device by connection ID

        cfm = GattcReadCfm(conidx=self._task_to_connidx(command.conn_idx))
        cfm.parameters.handle = command.handle
        cfm.parameters.status = command.status
        cfm.parameters.value = (c_uint8 * len(command.value))(*command.value)
        self._adapter_command_queue_send(cfm)

        response.status = BLE_ERROR.BLE_STATUS_OK

        self._mgr_response_queue_send(response)

    def read_value_req_evt_handler(self, gtl: GattcReadReqInd):
        evt = BleEventGattsReadReq(self._task_to_connidx(gtl.src_id))
        evt.handle = gtl.parameters.handle
        evt.offset = 0  # // stack always requires full value  # TODO I don't know what this means

        self._mgr_event_queue_send(evt)

    def send_event_cmd_handler(self, command: BleMgrGattsSendEventCmd):
        # TODO need to get dev from storage
        # TODO need to check if sending event pending on this char
        response = BleMgrGattsSendEventRsp(BLE_ERROR.BLE_ERROR_FAILED)
        gtl = GattcSendEvtCmd()
        gtl.parameters.handle = command.handle
        if command.type == GATT_EVENT.GATT_EVENT_NOTIFICATION:
            gtl.parameters.operation = GATTC_OPERATION.GATTC_NOTIFY
        else:
            gtl.parameters.operation = GATTC_OPERATION.GATTC_INDICATE
        gtl.parameters.seq_num = command.handle
        gtl.parameters.value = command.value

        self._adapter_command_queue_send(gtl)
        # Do not wait for GATTC_CMP_EVT, it will be handled async to avoid infinite wait

        response.status = BLE_ERROR.BLE_STATUS_OK
        self._mgr_response_queue_send(response)

    def service_add_characteristic_cmd_handler(self, command: BleMgrGattsServiceAddCharacteristicCmd) -> None:

        response = BleMgrGattsServiceAddCharacteristicRsp(BLE_ERROR.BLE_ERROR_FAILED)

        # Check if there is a pending GLT message set, there should be
        if self._add_svc_msg:
            if self._add_svc_msg.parameters.svc_desc.nb_att - self._attr_idx >= 2:

                self._extended_prop = command.prop & (GATT_PROP.GATT_PROP_EXTENDED_RELIABLE_WRITE | GATT_PROP.GATT_PROP_EXTENDED_WRITABLE_AUXILIARIES)

                 # TODO simplify calls into nested structures
                # Characteristic Attribute
                self._add_svc_msg.parameters.svc_desc.atts[self._attr_idx].uuid[:2] = [0x03, 0x28]
                self._add_svc_msg.parameters.svc_desc.atts[self._attr_idx].perm = att_perm()
                self._add_svc_msg.parameters.svc_desc.atts[self._attr_idx].max_len_read_ind = att_max_len_read_ind()
                self._attr_idx += 1
                h_offset = self._attr_idx

                # Characteristic value attribute
                self._add_svc_msg.parameters.svc_desc.atts[self._attr_idx].uuid[:] = command.uuid.uuid
                self._add_svc_msg.parameters.svc_desc.atts[self._attr_idx].perm = self._api_to_rwperm(command.prop, command.perm, command.uuid.type)
                self._add_svc_msg.parameters.svc_desc.atts[self._attr_idx].max_len_read_ind.max_len = command.max_len
                self._add_svc_msg.parameters.svc_desc.atts[self._attr_idx].max_len_read_ind.trigger_read_indication = command.flags
                self._attr_idx += 1
                h_val_offset = self._attr_idx

                response.status = BLE_ERROR.BLE_STATUS_OK
                response.h_offset = h_offset
                response.h_val_offset = h_val_offset

        self._mgr_response_queue_send(response)

    def service_add_cmd_handler(self, command: BleMgrGattsServiceAddCmd) -> None:

        response = BleMgrGattsServiceAddRsp(BLE_ERROR.BLE_ERROR_FAILED)

        # Check if there is a pending GLT message set, there should not be
        if not self._add_svc_msg:
            self._add_svc_msg = GattmAddSvcReq()
            self._attr_idx = 0

            # init array of attributes to appropriate size
            self._add_svc_msg.parameters.svc_desc.atts = (gattm_att_desc * command.num_attrs)()

            self._add_svc_msg.parameters.svc_desc.perm.svc_perm = ATTM_PERM.ENABLE

            self._add_svc_msg.parameters.svc_desc.perm.uuid_len \
                = ATTM_UUID_LEN.BITS_128 if command.uuid.type == ATT_UUID_TYPE.ATT_UUID_128 else ATTM_UUID_LEN.BITS_16

            self._add_svc_msg.parameters.svc_desc.perm.primary_svc \
                = ATTM_SERVICE_TYPE.PRIMARY_SERVICE if command.type == GATT_SERVICE.GATT_SERVICE_PRIMARY else ATTM_SERVICE_TYPE.SECONDARY_SERVICE
            self._add_svc_msg.parameters.svc_desc.nb_att = command.num_attrs

            if command.uuid.type == ATT_UUID_TYPE.ATT_UUID_16:
                self._add_svc_msg.parameters.svc_desc.uuid[:2] = command.uuid.uuid
            else:
                self._add_svc_msg.parameters.svc_desc.uuid[:] = command.uuid.uuid

            response.status = BLE_ERROR.BLE_STATUS_OK
        self._mgr_response_queue_send(response)

    def service_add_descriptor_cmd_handler(self, command: BleMgrGattsServiceAddDescriptorCmd):

        response = BleMgrGattsServiceAddDescriptorRsp(BLE_ERROR.BLE_ERROR_FAILED)

        # Check if there is a pending GLT message set, there should be
        if self._add_svc_msg:

            max_len = command.max_len
            # Check if there are enough free attributes left
            if (self._add_svc_msg.parameters.svc_desc.nb_att - self._attr_idx) >= 1:
                # Check if it is Extended properties descriptor and set it's value
                # TODO create method to compare att_uuid class
                if command.uuid.uuid == UUID_GATT_CHAR_EXT_PROPERTIES:  # TODO be carefule with endianess here
                    max_len = 0
                    if self._extended_prop & GATT_PROP.GATT_PROP_EXTENDED_RELIABLE_WRITE:
                        max_len |= 1
                    if self._extended_prop & GATT_PROP.GATT_PROP_EXTENDED_WRITABLE_AUXILIARIES:
                        max_len |= 2

                # TODO simplify calls into nested structures
                self._add_svc_msg.parameters.svc_desc.atts[self._attr_idx].uuid[:len(command.uuid.uuid)] = command.uuid.uuid
                self._add_svc_msg.parameters.svc_desc.atts[self._attr_idx].perm = self._api_to_rwperm(0, command.perm, command.uuid.type)

                if command.perm & (ATT_PERM.ATT_PERM_WRITE_ENCRYPT | ATT_PERM.ATT_PERM_WRITE_AUTH | ATT_PERM.ATT_PERM_WRITE):
                    perm = self._add_svc_msg.parameters.svc_desc.atts[self._attr_idx].perm
                    self._add_svc_msg.parameters.svc_desc.atts[self._attr_idx].perm = self._api_to_rwperm(GATT_PROP.GATT_PROP_WRITE | GATT_PROP.GATT_PROP_WRITE_NO_RESP, 0, None, perm)

                self._add_svc_msg.parameters.svc_desc.atts[self._attr_idx].max_len_read_ind.max_len = max_len
                # TODO would this ever have a read indication?
                self._attr_idx += 1
                h_offset = self._attr_idx

                response.status = BLE_ERROR.BLE_STATUS_OK
                response.h_offset = h_offset

        self._mgr_response_queue_send(response)

    def service_register_cmd_handler(self, command: BleMgrGattsServiceRegisterCmd) -> None:

        response = BleMgrGattsServiceRegisterRsp(BLE_ERROR.BLE_ERROR_FAILED)

        if self._add_svc_msg:
            self._wait_queue_add(BLE_CONN_IDX_INVALID,
                                 GATTM_MSG_ID.GATTM_ADD_SVC_RSP,
                                 0,
                                 self._service_register_rsp,
                                 None)

            self._adapter_command_queue_send(self._add_svc_msg)
            self._add_svc_msg = None  # Does this cause issue?

        else:
            self._mgr_response_queue_send(response)

    def set_value_cmd_handler(self, command: BleMgrGattsSetValueCmd):
        gtl = GattmAttSetValueReq()
        gtl.parameters.handle = command.handle
        gtl.parameters.value = (c_uint8 * len(command.value))(*command.value)
        self._wait_queue_add(BLE_CONN_IDX_INVALID,
                             GATTM_MSG_ID.GATTM_ATT_SET_VALUE_RSP,
                             0,
                             self._set_value_rsp,
                             None)
        self._adapter_command_queue_send(gtl)

    def write_cfm_cmd_handler(self, command: BleMgrGattsWriteCfmCmd):

        response = BleMgrGattsWriteCfmRsp(BLE_ERROR.BLE_ERROR_FAILED)
        # TODO need to get device from storage

        req = GattcWriteCfm()
        req.parameters.handle = command.handle
        req.parameters.status = command.status
        self._adapter_command_queue_send(req)

        response.status = BLE_ERROR.BLE_STATUS_OK
        self._mgr_response_queue_send(response)

    def write_value_req_evt_handler(self, gtl: GattcWriteReqInd):
        evt = BleEventGattsWriteReq(self._task_to_connidx(gtl.src_id))
        evt.handle = gtl.parameters.handle
        evt.offset = gtl.parameters.offset
        evt.value = bytes(gtl.parameters.value)
        self._mgr_event_queue_send(evt)


'''
static const ble_mgr_cmd_handler_t h_gatts[BLE_MGR_CMD_GET_IDX(BLE_MGR_GATTS_LAST_CMD)] = {
        ,
        ble_mgr_gatts_service_add_include_cmd_handler,
        ble_mgr_gatts_service_add_characteristic_cmd_handler,
        ble_mgr_gatts_service_add_descriptor_cmd_handler,
        ble_mgr_gatts_service_register_cmd_handler,
        ble_mgr_gatts_service_enable_cmd_handler,
        ble_mgr_gatts_service_disable_cmd_handler,
        ble_mgr_gatts_service_characteristic_get_prop_cmd_handler,
        ble_mgr_gatts_service_characteristic_set_prop_cmd_handler,
        ble_mgr_gatts_get_value_cmd_handler,
        ble_mgr_gatts_set_value_cmd_handler,
        ble_mgr_gatts_read_cfm_cmd_handler,
        ble_mgr_gatts_write_cfm_cmd_handler,
        ble_mgr_gatts_prepare_write_cfm_cmd_handler,
        ble_mgr_gatts_send_event_cmd_handler,
        ble_mgr_gatts_service_changed_ind_cmd_handler,
};

'''
