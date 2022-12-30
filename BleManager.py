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
from BleCommon import BLE_ERROR, BLE_STATUS, BLE_MGR_CMD_CAT, BleManagerBase
from BleManagerGap import BleManagerGap, BLE_CMD_GAP_OPCODE, BleMgrMsgHeader, BleMgrGapRoleSetCmd

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
                 app_command_q: asyncio.Queue(),
                 app_response_q: asyncio.Queue(),
                 app_event_q: asyncio.Queue(),
                 adapter_command_q: asyncio.Queue(),
                 adapter_event_q: asyncio.Queue(),
                 event_notif: asyncio.Event()) -> None:

        # TODO if x else y is so vscode will treat variable as that item for auto complete
        self.app_command_q: asyncio.Queue = app_command_q
        self.app_response_q: asyncio.Queue = app_response_q
        self.app_event_q: asyncio.Queue = app_event_q
        self.adapter_commnand_q: asyncio.Queue = adapter_command_q
        self.adapter_event_q: asyncio.Queue = adapter_event_q
        self.event_notif: asyncio.Event = event_notif
        self.wait_q = GtlWaitQueue()
        self.dev_params = BleDevParamsDefault()
        self.ble_stack_initialized = False
        self._reset_signal: asyncio.Event = asyncio.Event()
        self.gap_mgr = BleManagerGap(self.adapter_commnand_q, self.app_response_q, self.wait_q)

        self.handlers = {
            BLE_MGR_CMD_CAT.BLE_MGR_COMMON_CMD_CAT: None,
            BLE_MGR_CMD_CAT.BLE_MGR_GAP_CMD_CAT: self.gap_mgr,
            BLE_MGR_CMD_CAT.BLE_MGR_GATTS_CMD_CAT: None,
            BLE_MGR_CMD_CAT.BLE_MGR_GATTC_CMD_CAT: None,
            BLE_MGR_CMD_CAT.BLE_MGR_L2CAP_CMD_CAT: None,
        }

    def init(self):

        # TODO keeping handles so these can be cancelled somehow
        self._task = asyncio.create_task(self.manager_task(), name='BleManagerTask')

        print(f"{type(self)} Exiting init")

    async def manager_task(self):

        self._command_q_task = asyncio.create_task(self._read_command_queue(), name='BleManagerReadCommandQueueTask')
        self._event_q_task = asyncio.create_task(self._read_event_queue(), name='BleManagerReadEventQueueTask')

        pending = [self._command_q_task, self._event_q_task]
        while True:
            print("BleManager waiting on something to happen")
            done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)

            for task in done:
                result = task.result()
                print(f"Ble Manager handling completed task {task}. result={result}")

                if isinstance(result, GtlMessageBase):
                    # This is from the adapter_event_q
                    self._process_event_queue(result)
                    self._event_q_task = asyncio.create_task(self._read_event_queue(), name='BleManagerReadEventQueueTask')
                    pending.add(self._event_q_task)

                elif isinstance(result, BleMgrMsgHeader):
                    # This is from the api_command_q
                    self._process_command_queue(result)
                    self._command_q_task = asyncio.create_task(self._read_command_queue(), name='BleManagerReadCommandQueueTask')
                    pending.add(self._command_q_task)

    async def _read_command_queue(self):
        # TODO can we ditch event signal and just read queue?

        item = await self.app_command_q.get()
        return item

    async def _read_event_queue(self):
        # TODO can we ditch event signal and just read queue?
        await self.event_notif.wait()
        self.event_notif.clear()
        # get an item from the queue
        if not self.adapter_event_q.empty():
            item: GtlMessageBase = self.adapter_event_q.get_nowait()

            return item

    def _process_event_queue(self, event: GtlMessageBase):

        print(f"Ble Manager process_event_queue {event}")

        if event.parameters.operation == GAPM_OPERATION.GAPM_RESET:
            self._reset_signal.set()

        if not self.wait_q.match(event):
            if not self.handle_evt_or_ind(event):
                pass

    def _process_command_queue(self, command: BleMgrMsgHeader):

        print("Processing command queue")
        category = command.opcode >> 8

        # handler_type: dict = self.handlers.get(category)
        mgr: BleManagerBase = self.handlers.get(category)
        handler = mgr.handlers.get(command.opcode)

        print(BLE_CMD_GAP_OPCODE.BLE_MGR_GAP_ROLE_SET_CMD.value)
        # print(f"opcode={command.opcode}. cat={category}, handler_type={handler_type}, handler={handler}")
        print(f"opcode={command.opcode}. cat={category}, mgr={mgr}, handler={handler}")
        assert handler  # Should always have a handler

        if handler:
            handler(command)
        else:
            print("Handler does not exist")

        print("exiting _process_command_queue")

    def handle_evt_or_ind(self, message: GtlMessageBase):

        match message.msg_id:
            case GAPM_MSG_ID.GAPM_CMP_EVT:
                pass
            case GAPC_MSG_ID.GAPC_PARAM_UPDATE_CMD:
                pass
            case GATTC_MSG_ID.GATTC_CMP_EVT:
                pass

        return False

    async def ble_mgr_response_queue_get(self):  # add timeout ?
        return await self.app_response_q.get()

    async def ble_reset(self) -> BLE_ERROR:  # TODO should return error or somethign
        error = BLE_ERROR.BLE_ERROR_FAILED

        self._reset_signal.clear()
        self.adapter_commnand_q.put_nowait(GapmResetCmd(gapm_reset_cmd(GAPM_OPERATION.GAPM_RESET)))
        await self._reset_signal.wait()
        error = BLE_ERROR.BLE_STATUS_OK
        return error

    async def cmd_execute(self, command, handler: None) -> BLE_ERROR:
        ble_status = self.dev_params.status
        if ble_status == BLE_STATUS.BLE_IS_BUSY or ble_status == BLE_STATUS.BLE_IS_RESET:
            return BLE_ERROR.BLE_ERROR_BUSY

        # handler(command)

        self.app_command_q.put_nowait(command)

        response = await self.ble_mgr_response_queue_get()

        print(f"Ble. _ble_cmd_execute: command={command}, \
                response={BLE_ERROR(response)}, handler={handler}")
        return response

    def _wait_queue_add(self, conn_idx, msg_id, ext_id, cb, param):
        item = GtlWaitQueueElement(conn_idx=conn_idx, msg_id=msg_id, ext_id=ext_id, cb=cb, param=param)
        self.wait_q.push(item)

    def _task_to_connidx(self, task_id):
        return task_id >> 8
