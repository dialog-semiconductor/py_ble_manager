import asyncio
from enum import IntEnum, auto

from .GtlWaitQueue import GtlWaitQueue
from .BleManagerCommon import BLE_MGR_CMD_CAT, BleManagerBase, BleMgrMsgBase
from ble_api.BleAtt import att_uuid, ATT_PERM
from ble_api.BleGatt import GATT_SERVICE, GATT_PROP
from ble_api.BleGatts import GATTS_FLAGS


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


class BleMgrGattsServiceAddCmd(BleMgrMsgBase):
    def __init__(self,
                 uuid: att_uuid = att_uuid(),
                 type: GATT_SERVICE = GATT_SERVICE.GATT_SERVICE_PRIMARY,
                 num_attrs: int = 0) -> None:
        super().__init__(opcode=BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_SERVICE_ADD_CMD)
        self.uuid = uuid
        self.type = type
        self.num_attrs = num_attrs


class BleMgrGattsServiceAddCharacteristicCmd(BleMgrMsgBase):
    def __init__(self,
                 uuid: att_uuid = att_uuid(),
                 prop: GATT_PROP = GATT_PROP.GATT_PROP_NONE,
                 perm: ATT_PERM = ATT_PERM.ATT_PERM_NONE,
                 max_len: int = 0,
                 flags: GATTS_FLAGS = GATTS_FLAGS.GATTS_FLAG_CHAR_READ_REQ,
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_SERVICE_CHARACTERISTIC_ADD_CMD)
        self.uuid = uuid
        self.prop = prop
        self.perm = perm
        self.max_len = max_len
        self.flags = flags


class BleManagerGattc(BleManagerBase):

    def __init__(self,
                 adapter_command_q: asyncio.Queue(),
                 app_response_q: asyncio.Queue(),
                 wait_q: GtlWaitQueue()) -> None:

        super().__init__(adapter_command_q, app_response_q, wait_q)

        '''
        self.cmd_handlers = {
            BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ROLE_SET_CMD: self.gap_role_set_cmd_handler,
            BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ADV_START_CMD: self.gap_adv_start_cmd_handler
        }
        '''


class BleManagerGatts(BleManagerBase):

    def __init__(self,
                 adapter_command_q: asyncio.Queue(),
                 app_response_q: asyncio.Queue(),
                 wait_q: GtlWaitQueue()) -> None:

        super().__init__(adapter_command_q, app_response_q, wait_q)

        '''
        self.handlers = {
            BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ROLE_SET_CMD: self.gap_role_set_cmd_handler,
            BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ADV_START_CMD: self.gap_adv_start_cmd_handler
        }
        '''


'''
static const ble_mgr_cmd_handler_t h_gatts[BLE_MGR_CMD_GET_IDX(BLE_MGR_GATTS_LAST_CMD)] = {
        ble_mgr_gatts_service_add_cmd_handler,
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
'''
