import asyncio
from ctypes import c_uint8
from enum import IntEnum, auto

from .GtlWaitQueue import GtlWaitQueue
from .BleManagerCommon import BLE_MGR_CMD_CAT, BleManagerBase, BleMgrMsgBase
from ble_api.BleAtt import att_uuid, ATT_PERM, ATT_UUID_TYPE
from ble_api.BleGatt import GATT_SERVICE, GATT_PROP
from ble_api.BleCommon import BLE_ERROR, BleEventBase, BLE_EVT_CAT
from ble_api.BleGap import BLE_CONN_IDX_INVALID
from gtl_messages.gtl_message_gattm import GattmAddSvcReq, GattmAddSvcRsp
from gtl_port.attm import ATTM_PERM, ATTM_UUID_LEN, ATTM_SERVICE_TYPE, ATTM_BROADCAST, ATTM_ENC_KEY_SIZE_16_BYTES, \
    ATTM_EXTENDED_PROPERTIES, ATTM_WRITE_SIGNED, ATTM_WRITE_REQUEST

from gtl_port.gattm_task import gattm_att_desc, att_perm, att_max_len_read_ind, GATTM_MSG_ID
from gtl_port.rwble_hl_error import HOST_STACK_ERROR_CODE

from gtl_messages.gtl_message_gattc import GattcReadReqInd, GattcReadCfm
from gtl_port.gattc_task import GATTC_MSG_ID  


class BLE_CMD_GATTS_OPCODE(IntEnum):
    BLE_MGR_GATTS_SERVICE_ADD_CMD = BLE_MGR_CMD_CAT.BLE_MGR_GATTS_CMD_CAT << 8
    BLE_MGR_GATTS_SERVICE_INCLUDE_ADD_CMD = auto()
    BLE_MGR_GATTS_SERVICE_CHARACTERISTIC_ADD_CMD = auto()
    BLE_MGR_GATTS_SERVICE_DESCRIPTOR_ADD_CMD = auto()
    BLE_MGR_GATTS_SERVICE_REGISTER_CMD = auto()
    BLE_MGR_GATTS_SERVICE_ENABLE_CMD = auto()
    BLE_MGR_GATTS_SERVICE_DISABLE_CMD = auto()
    BLE_MGR_GATTS_SERVICE_CHARACTERISTIC_GET_PROP_CMD = auto()
    BLE_MGR_GATTS_SERVICE_CHARACTERISTIC_SET_PROP_CMD = auto()
    BLE_MGR_GATTS_GET_VALUE_CMD = auto()
    BLE_MGR_GATTS_SET_VALUE_CMD = auto()
    BLE_MGR_GATTS_READ_CFM_CMD = auto()
    BLE_MGR_GATTS_WRITE_CFM_CMD = auto()
    BLE_MGR_GATTS_PREPARE_WRITE_CFM_CMD = auto()
    BLE_MGR_GATTS_SEND_EVENT_CMD = auto()
    BLE_MGR_GATTS_SERVICE_CHANGED_IND_CMD = auto()
    BLE_MGR_GATTS_LAST_CMD = auto()



# TODO this resulted in circular import, need to reorganzie imports and redefine where certain enums classes located
# GATT Server flags
class GATTS_FLAGS(IntEnum):
    GATTS_FLAG_CHAR_NO_READ_REQ = 0x00  # TODO need better name
    GATTS_FLAG_CHAR_READ_REQ = 0x01        # enable ::BLE_EVT_GATTS_READ_REQ for attribute


class BleMgrGattsServiceAddCharacteristicCmd(BleMgrMsgBase):
    def __init__(self,
                 uuid: att_uuid = att_uuid(),
                 prop: GATT_PROP = GATT_PROP.GATT_PROP_NONE,
                 perm: ATT_PERM = ATT_PERM.ATT_PERM_NONE,
                 max_len: int = 0,
                 flags: GATTS_FLAGS = GATTS_FLAGS.GATTS_FLAG_CHAR_NO_READ_REQ,
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_SERVICE_CHARACTERISTIC_ADD_CMD)
        self.uuid = uuid
        self.prop = prop
        self.perm = perm
        self.max_len = max_len
        self.flags = flags


class BleMgrGattsServiceAddCharacteristicRsp(BleMgrMsgBase):
    def __init__(self,
                 status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED,
                 h_offset: int = 0,
                 h_val_offset: int = 0
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_SERVICE_CHARACTERISTIC_ADD_CMD)
        self.status = status
        self.h_offset = h_offset
        self.h_val_offset = h_val_offset


class BleMgrGattsServiceAddCmd(BleMgrMsgBase):
    def __init__(self,
                 uuid: att_uuid = None,
                 type: GATT_SERVICE = GATT_SERVICE.GATT_SERVICE_PRIMARY,
                 num_attrs: int = 0) -> None:
        super().__init__(opcode=BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_SERVICE_ADD_CMD)
        self.uuid = uuid if uuid else []  # TODO raise error is length off
        self.type = type
        self.num_attrs = num_attrs


class BleMgrGattsServiceAddRsp(BleMgrMsgBase):
    def __init__(self, status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED) -> None:
        super().__init__(opcode=BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_SERVICE_ADD_CMD)
        self.status = status


class BleMgrGattsServiceAddDescriptorCmd(BleMgrMsgBase):
    def __init__(self,
                 uuid: att_uuid = att_uuid(),
                 perm: ATT_PERM = ATT_PERM.ATT_PERM_NONE,
                 max_len: int = 0,
                 flags: GATTS_FLAGS = GATTS_FLAGS.GATTS_FLAG_CHAR_READ_REQ,
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_SERVICE_DESCRIPTOR_ADD_CMD)
        self.uuid = uuid
        self.perm = perm
        self.max_len = max_len
        self.flags = flags


class BleMgrGattsServiceAddDescriptorRsp(BleMgrMsgBase):
    def __init__(self,
                 status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED,
                 h_offset: int = 0,
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_SERVICE_DESCRIPTOR_ADD_CMD)
        self.status = status
        self.h_offset = h_offset


class BleMgrGattsServiceRegisterCmd(BleMgrMsgBase):
    def __init__(self) -> None:
        super().__init__(opcode=BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_SERVICE_REGISTER_CMD)


class BleMgrGattsServiceRegisterRsp(BleMgrMsgBase):
    def __init__(self,
                 status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED,
                 handle: int = 0) -> None:
        super().__init__(opcode=BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_SERVICE_REGISTER_CMD)
        self.status = status
        self.handle = handle


class BleEventGattsReadReq(BleEventBase):
    def __init__(self,
                 conn_idx: int = 0,
                 handle: int = 0,
                 offset: int = 0,
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GATTS.BLE_EVT_GATTS_READ_REQ)
        self.conn_idx = conn_idx
        self.handle = handle
        self.offset = offset


class BleMgrGattsReadCfmCmd(BleMgrMsgBase):
    def __init__(self,
                 conn_idx: int = 0,
                 handle: int = 0,
                 status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED,
                 value: list[int] = None
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_READ_CFM_CMD)
        self.conn_idx = conn_idx
        self.handle = handle
        self.status = status
        self.value = value


class BleMgrGattsReadCfmRsp(BleMgrMsgBase):
    def __init__(self,
                 status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED,
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_READ_CFM_CMD)
        self.status = status


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
            BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_SERVICE_DESCRIPTOR_ADD_CMD: None,  # self.service_add_descriptor_cmd_handler,
            BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_SERVICE_REGISTER_CMD: self.service_register_cmd_handler,
            BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_READ_CFM_CMD: self.read_cfm_cmd_handler,
        }

        self.evt_handlers = {
            GATTC_MSG_ID.GATTC_READ_REQ_IND: self.read_value_req_evt_handler,  # TODO why is this in Gatts and not Gattc???
        }

        self._add_svc_msg = None
        self._attr_idx = 0
        self._extended_prop = 0

    def _api_to_rwperm(self, prop: GATT_PROP, perm: ATTM_PERM, uuid_type: ATT_UUID_TYPE):

        rwperm = att_perm()

        if (prop & GATT_PROP.GATT_PROP_BROADCAST):
            rwperm.broadcast = ATTM_BROADCAST.YES

        if (prop & GATT_PROP.GATT_PROP_WRITE_NO_RESP):
            rwperm.write = ATTM_PERM.ENABLE

        if (prop & GATT_PROP.GATT_PROP_WRITE):
            rwperm.write_request = ATTM_WRITE_REQUEST.ACCEPTED

        if (prop & GATT_PROP.GATT_PROP_NOTIFY):
            rwperm.notification = ATTM_PERM.ENABLE

        if (prop & GATT_PROP.GATT_PROP_INDICATE):
            rwperm.indication = ATTM_PERM.ENABLE

        if (prop & GATT_PROP.GATT_PROP_WRITE_SIGNED):
            rwperm.write_signed = ATTM_WRITE_SIGNED.ACCEPTED

        if (prop & GATT_PROP.GATT_PROP_EXTENDED):
            rwperm.extended_properties_present = ATTM_EXTENDED_PROPERTIES.YES

        # Translate read permissions
        if (perm & ATT_PERM.ATT_PERM_READ_AUTH):
            rwperm.read = ATTM_PERM.AUTH
        elif (perm & ATT_PERM.ATT_PERM_READ_ENCRYPT):
            rwperm.read = ATTM_PERM.UNAUTH
        elif (perm & ATT_PERM.ATT_PERM_READ):
            rwperm.read = ATTM_PERM.ENABLE

        # Translate write permissions
        if (perm & ATT_PERM.ATT_PERM_WRITE_AUTH):
            rwperm.write = ATTM_PERM.AUTH
        elif (perm & ATT_PERM.ATT_PERM_WRITE_ENCRYPT):
            rwperm.write = ATTM_PERM.UNAUTH
        elif (perm & ATT_PERM.ATT_PERM_WRITE):
            rwperm.write = ATTM_PERM.ENABLE

        # Translate keysize permissions
        if (perm & ATT_PERM.ATT_PERM_KEYSIZE_16):
            rwperm.enc_key_size = ATTM_ENC_KEY_SIZE_16_BYTES.YES

        if uuid_type == ATT_UUID_TYPE.ATT_UUID_128:
            rwperm.uuid_len = ATTM_UUID_LEN.BITS_128  # TODO confusing which ATT/ATTM is coming from where. Consider renaming

        return rwperm

    def _service_register_rsp(self, gtl: GattmAddSvcRsp, param: None):
        response = BleMgrGattsServiceRegisterRsp(self._task_to_connidx(gtl.src_id))
        response.handle = gtl.parameters.start_hdl

        response.status = BLE_ERROR.BLE_STATUS_OK \
            if gtl.parameters.status == HOST_STACK_ERROR_CODE.ATT_ERR_NO_ERROR \
            else BLE_ERROR.BLE_ERROR_FAILED

        self._mgr_response_queue_send(response)

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

    def service_add_characteristic_cmd_handler(self, command: BleMgrGattsServiceAddCharacteristicCmd) -> None:

        response = BleMgrGattsServiceAddCharacteristicRsp(BLE_ERROR.BLE_ERROR_FAILED)

        # Check if there is a pending GLT message set, there should be
        if self._add_svc_msg:
            if self._add_svc_msg.parameters.svc_desc.nb_att - self._attr_idx >= 2:

                self._extended_prop = command.prop & (GATT_PROP.GATT_PROP_EXTENDED_RELIABLE_WRITE | GATT_PROP.GATT_PROP_EXTENDED_WRITABLE_AUXILIARIES)

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

    '''
    def service_add_descriptor_cmd_handler(self, command: BleMgrGattsServiceAddDescriptorCmd):

        response = BleMgrGattsServiceAddDescriptorRsp(BLE_ERROR.BLE_ERROR_FAILED)

        # Check if there is a pending GLT message set, there should be
        if self._add_svc_msg:

            # Check if there are enough free attributes left
            if (self._add_svc_msg.parameters.svc_desc.nb_att - self._attr_idx) >= 1:
                # Check if it is Extended properties descriptor and set it's value
                # TODO create method to compare att_uuid class
                if command.uuid.type == att_uuid(ATT_UUID_TYPE.ATT_UUID_16, UUID_GATT_CHAR_EXT_PROPERTIES):

                #    and command.uuid.uuid[0] = UUID_GATT_CHAR_EXT_PROPERTIES &
                    pass

                if command.uuid.type == ATT_UUID_TYPE.ATT_UUID_16:
                    self._add_svc_msg.parameters.svc_desc.atts[self._attr_idx].uuid[:2] = command.uuid.uuid
                else:
                    self._add_svc_msg.parameters.svc_desc.atts[self._attr_idx].uuid[:] = command.uuid.uuid
        self._mgr_response_queue_send(response)
    '''


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
