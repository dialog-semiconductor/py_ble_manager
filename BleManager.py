import asyncio
# from ctypes import c_uint16, c_uint8, Array
# from enum import IntEnum, auto
from gtl_messages.gtl_message_base import GtlMessageBase
# from gtl_messages.gtl_message_gapm import GapmResetCmd, GapmSetDevConfigCmd, GapmStartAdvertiseCmd

# TODO perhaps these Gapm messages do not belong here
from gtl_messages.gtl_port.gapm_task import GAPM_MSG_ID  # , gapm_reset_cmd, gapm_cmp_evt, GAPM_OPERATION, gapm_set_dev_config_cmd
from gtl_messages.gtl_port.gapc_task import GAPC_MSG_ID
from gtl_messages.gtl_port.gattc_task import GATTC_MSG_ID
# from gtl_messages.gtl_port.gap import GAP_ROLE
from BleDevParams import BleDevParamsDefault
# from gtl_messages.gtl_port.rwble_hl_error import HOST_STACK_ERROR_CODE
from GtlWaitQueue import GtlWaitQueue  # , GtlWaitQueueElement
from BleCommon import BLE_ERROR, BLE_STATUS, BLE_MGR_CMD_CAT, BleManagerBase, BleManagerCommon, BleEventBase
from BleManagerGap import BleManagerGap, BleMgrCmdBase  # , BleMgrGapRoleSetCmd, BLE_CMD_GAP_OPCODE

# this is from ble_config.h
dg_configBLE_DATA_LENGTH_TX_MAX = (251)


'''
# from ad_ble.h
class ad_ble_operations(IntEnum):
    AD_BLE_OP_CMP_EVT = 0x00
    AD_BLE_OP_INIT_CMD = 0x01
    AD_BLE_OP_RESET_CMD = 0x02
    AD_BLE_OP_LAST = auto()
# end ad_ble.h


# from ble_mgr_ad_msg.c
class WaitQueueElement():
    def __init__(self,
                 rsp_op: ad_ble_operations,
                 cmd_op: ad_ble_operations,
                 cb: callable,
                 param) -> None:
        self.rsp_op = rsp_op
        self.cmd_op = cmd_op
        self.cb = cb
        self.param = param

# end ble_mgr_ad_msg.c
'''

'''
# from ble_mgr_cmd.h
class BLE_MGR_COMMON_CMD_OPCODE(IntEnum):
    BLE_MGR_COMMON_STACK_MSG = BLE_CMD_CAT.BLE_MGR_COMMON_CMD_CAT << 8
    BLE_MGR_COMMON_REGISTER_CMD = auto()
    BLE_MGR_COMMON_ENABLE_CMD = auto()
    BLE_MGR_COMMON_RESET_CMD = auto()
    BLE_MGR_COMMON_READ_TX_POWER_CMD = auto()
    BLE_MGR_COMMON_LAST_CMD = auto()
# end ble_mgr_cmd.h
'''
'''
class BleMgrCmdFactory():
    @staticmethod
    def create_command(command_type, size):
        if  command_type in BLE_CMD_GAP_OPCODE:
            return BleGapMgrFactory(command_type, size)
'''


class BleManager(BleManagerBase):

    def __init__(self,
                 app_command_q: asyncio.Queue[BleMgrCmdBase],
                 app_response_q: asyncio.Queue[BLE_ERROR],
                 app_event_q: asyncio.Queue[BleEventBase],
                 adapter_command_q: asyncio.Queue[BleMgrCmdBase],
                 adapter_event_q: asyncio.Queue[GtlMessageBase]) -> None:

        # TODO if x else y is so vscode will treat variable as that item for auto complete
        self.app_command_q: asyncio.Queue[BleMgrCmdBase] = app_command_q
        self.app_response_q: asyncio.Queue[BLE_ERROR] = app_response_q
        self.app_event_q: asyncio.Queue = app_event_q
        self.adapter_commnand_q: asyncio.Queue[GtlMessageBase] = adapter_command_q
        self.adapter_event_q: asyncio.Queue[GtlMessageBase] = adapter_event_q
        self.wait_q = GtlWaitQueue()
        self.dev_params = BleDevParamsDefault()
        self.ble_stack_initialized = False
        self.gap_mgr = BleManagerGap(self.app_response_q, self.app_event_q, self.adapter_commnand_q, self.wait_q)
        self.common_mgr = BleManagerCommon(self.app_response_q, self.app_event_q, self.adapter_commnand_q, self.wait_q)

        self.cmd_handlers = {
            BLE_MGR_CMD_CAT.BLE_MGR_COMMON_CMD_CAT: self.common_mgr,
            BLE_MGR_CMD_CAT.BLE_MGR_GAP_CMD_CAT: self.gap_mgr,
            BLE_MGR_CMD_CAT.BLE_MGR_GATTS_CMD_CAT: None,
            BLE_MGR_CMD_CAT.BLE_MGR_GATTC_CMD_CAT: None,
            BLE_MGR_CMD_CAT.BLE_MGR_L2CAP_CMD_CAT: None,
        }

    def _handle_evt_or_ind(self, message: GtlMessageBase):

        # TODO make list of handlers from all avail classes. If get back a handler, call it
        event_handlers = [self.gap_mgr.evt_handlers]

        for handlers in event_handlers:
            handler = handlers.get(message.msg_id)
            if handler:
                handler(message)
                return True
        return False

    async def _manager_task(self):

        # TODO function for creating these tasks so dont have in two spots
        self._command_q_task = asyncio.create_task(self._read_command_queue(), name='BleMgrReadCommandQueueTask')
        self._event_q_task = asyncio.create_task(self._read_event_queue(), name='BleMgrReadEventQueueTask')

        pending = [self._command_q_task, self._event_q_task]

        while True:
            done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)

            for task in done:
                result = task.result()

                if isinstance(result, GtlMessageBase):
                    # This is from the adapter_event_q
                    self._process_event_queue(result)
                    self._event_q_task = asyncio.create_task(self._read_event_queue(), name='BleMgrReadEventQueueTask')
                    pending.add(self._event_q_task)

                elif isinstance(result, BleMgrCmdBase):
                    # This is from the api_command_q
                    self._process_command_queue(result)
                    self._command_q_task = asyncio.create_task(self._read_command_queue(), name='BleMgrReadCommandQueueTask')
                    pending.add(self._command_q_task)

    def _process_command_queue(self, command: BleMgrCmdBase):

        category = command.opcode >> 8

        mgr: BleManagerBase = self.cmd_handlers.get(category)
        cmd_handler = mgr.cmd_handlers.get(command.opcode)

        # assert cmd_handler  # Should always have a handler

        if cmd_handler:
            cmd_handler(command)
        else:
            print(f"BleManager._process_command_queue. Unhandled command={command}")

    def _process_event_queue(self, event: GtlMessageBase):

        if not self.wait_q.match(event):
            if not self._handle_evt_or_ind(event):
                print(f"BleManager._process_event_queue. Unhandled event={event}")

    async def _read_command_queue(self) -> BleMgrCmdBase:
        return await self.app_command_q.get()

    async def _read_event_queue(self) -> GtlMessageBase:
        return await self.adapter_event_q.get()

    def init(self):
        # TODO keeping handles so these can be cancelled somehow
        self._mgr_task = asyncio.create_task(self._manager_task(), name='BleManagerTask')

    async def cmd_execute(self, command, handler: None) -> BLE_ERROR:
        ble_status = self.dev_params.status
        if ble_status == BLE_STATUS.BLE_IS_BUSY or ble_status == BLE_STATUS.BLE_IS_RESET:
            return BLE_ERROR.BLE_ERROR_BUSY

        # handler(command)

        self.app_command_q.put_nowait(command)
        response = await self.app_response_q.get()

        return response
