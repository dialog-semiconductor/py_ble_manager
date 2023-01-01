import asyncio
from enum import IntEnum, auto

from .GtlWaitQueue import GtlWaitQueue
from .BleManagerCommon import BLE_MGR_CMD_CAT, BleManagerBase, BleMgrMsgBase


class BleMgrGattcDiscoverSvcCmd(BleMgrMsgBase):
    def __init__(self, conn_idx, uuid) -> None:
        super().__init__(opcode=BLE_CMD_GATTC_OPCODE.BLE_MGR_GATTC_DISCOVER_SVC_CMD)


class BLE_CMD_GATTC_OPCODE(IntEnum):
    BLE_MGR_GATTC_BROWSE_CMD = BLE_MGR_CMD_CAT.BLE_MGR_GATTC_CMD_CAT << 8
    BLE_MGR_GATTC_BROWSE_RANGE_CMD = auto()
    BLE_MGR_GATTC_DISCOVER_SVC_CMD = auto()
    BLE_MGR_GATTC_DISCOVER_INCLUDE_CMD = auto()
    BLE_MGR_GATTC_DISCOVER_CHAR_CMD = auto()
    BLE_MGR_GATTC_DISCOVER_DESC_CMD = auto()
    BLE_MGR_GATTC_READ_CMD = auto()
    BLE_MGR_GATTC_WRITE_GENERIC_CMD = auto()
    BLE_MGR_GATTC_WRITE_EXECUTE_CMD = auto()
    BLE_MGR_GATTC_EXCHANGE_MTU_CMD = auto()
    BLE_MGR_GATTC_LAST_CMD = auto()


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
'''
