import asyncio

from ble_api.BleCommon import BleEventBase, BLE_ERROR
from manager.BleManagerBase import BleManagerBase
from manager.BleManagerCommonMsgs import BleMgrMsgBase
from manager.BleManagerStorage import StoredDeviceQueue
from manager.GtlWaitQueue import GtlWaitQueue


class BleManagerGattc(BleManagerBase):

    def __init__(self,
                 mgr_response_q: asyncio.Queue[BLE_ERROR],
                 mgr_event_q: asyncio.Queue[BleEventBase],
                 adapter_command_q: asyncio.Queue[BleMgrMsgBase],
                 wait_q: GtlWaitQueue,
                 stored_device_q: StoredDeviceQueue) -> None:

        super().__init__(mgr_response_q, mgr_event_q, adapter_command_q, wait_q, stored_device_q)

        '''
        self.cmd_handlers = {
            BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ROLE_SET_CMD: self.gap_role_set_cmd_handler,
            BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ADV_START_CMD: self.gap_adv_start_cmd_handler
        }
        '''


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
