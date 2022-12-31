import asyncio
from ctypes import c_uint16, c_uint8, Array
from enum import IntEnum, auto
from gtl_messages.gtl_message_base import GtlMessageBase
from gtl_messages.gtl_message_gapm import GapmResetCmd, GapmSetDevConfigCmd, GapmStartAdvertiseCmd

# TODO perhaps these Gapm messages do not belong here
from gtl_messages.gtl_port.gapm_task import GAPM_MSG_ID, gapm_reset_cmd, gapm_cmp_evt, GAPM_OPERATION, gapm_set_dev_config_cmd
from gtl_messages.gtl_port.gapc_task import GAPC_MSG_ID
from gtl_messages.gtl_port.gattc_task import GATTC_MSG_ID
from gtl_messages.gtl_port.gap import GAP_ROLE
from BleDevParams import BleDevParamsDefault
from gtl_messages.gtl_port.rwble_hl_error import HOST_STACK_ERROR_CODE
from GtlWaitQueue import GtlWaitQueue, GtlWaitQueueElement
from BleCommon import BLE_ERROR, BLE_STATUS, BLE_MGR_CMD_CAT, BleManagerBase, BleMgrCmdBase


# this is from ble_config.h
dg_configBLE_DATA_LENGTH_TX_MAX = (251)


class BleMgrGattcDiscoverSvcCmd(BleMgrCmdBase):
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
