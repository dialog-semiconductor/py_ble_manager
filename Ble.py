import asyncio

# from gtl_messages.gtl_port.gapm_task import GAPM_OPERATION, gapm_reset_cmd  # TODO remove
# from gtl_messages.gtl_message_gapm import GapmResetCmd  # TODO remove
from gtl_messages.gtl_port.gap import GAP_ROLE
from gtl_messages.gtl_port.gapm_task import GAPM_OPERATION

from BleManager import BleManager, BLE_STATUS, BLE_ERROR, BleMgrGapRoleSetCmd, BLE_CMD_GAP_OPCODE, BleMgrGapAdvStartCmd  # ble_mgr_msg_hdr, BLE_MGR_COMMON_CMD_OPCODE
from BleAdapter import BleAdapter  # ad_ble_msg, AD_BLE_OPERATION


# common
class BleBase():
    pass


class BleClient(BleBase):
    pass


class BlePeripheral(BleBase):
    def __init__(self, com_port: str):

        app_command_q = asyncio.Queue()
        app_resposne_q = asyncio.Queue()
        app_event_q = asyncio.Queue()

        adapter_command_q = asyncio.Queue()
        adapter_event_q = asyncio.Queue()

        event_signal = asyncio.Event()

        self.ble_manager = BleManager(app_command_q, app_resposne_q, app_event_q, adapter_command_q, adapter_event_q, event_signal)
        self.ble_adapter = BleAdapter(com_port, adapter_command_q, adapter_event_q, event_signal)

    async def init(self):
        try:
            print("Opening serial port")
            # Open the serial port the the 531
            await self.ble_adapter.open_serial_port()
            print("Serial port opened. Starting always running tasks")

            # TODO need to start a BleManager task

            # Start always running BLE tasks
            self.ble_manager.init()
            self.ble_adapter.init()
            print("Tasks started")

        except asyncio.TimeoutError as e:
            raise e

    async def start(self) -> BLE_ERROR:

        error = BLE_ERROR.BLE_ERROR_FAILED

        error = await self.ble_manager.ble_reset()
        print(f"we have reset!!! error={error.name}, error={error}")
        if error == BLE_ERROR.BLE_STATUS_OK:

            error = await self._gap_role_set(GAP_ROLE.GAP_ROLE_PERIPHERAL)
            print("start: returned from gap_role_set")

        print(f"after if statement. error={error.name}")

        return error

    async def _gap_role_set(self, role: GAP_ROLE):
        response = BLE_ERROR.BLE_ERROR_FAILED
        print("_gap_role_set calling gap_role_set_handler")
        # TODO should have factory that creates this, doesnt make sense to manually put this enum into the already well defined class 
        command = BleMgrGapRoleSetCmd(role)
        response = await self.ble_manager.cmd_execute(command, self.ble_manager.gap_role_set_handler)

        print(f"_gap_role_set returned from gap_role_set_handler. resposne={response.name}")

        return response

    def set_advertising_interval(self, adv_intv_min, adv_intv_max):
        self.ble_manager.dev_params.adv_intv_min = adv_intv_min
        self.ble_manager.dev_params.adv_intv_max = adv_intv_max

        return BLE_ERROR.BLE_STATUS_OK

    async def start_advertising(self, adv_type: GAPM_OPERATION = GAPM_OPERATION.GAPM_ADV_UNDIRECT):

        match adv_type:
            case GAPM_OPERATION.GAPM_ADV_NON_CONN:
                pass
            case GAPM_OPERATION.GAPM_ADV_UNDIRECT:
                pass
            case  GAPM_OPERATION.GAPM_ADV_DIRECT:
                pass
            case GAPM_OPERATION.GAPM_ADV_DIRECT_LDC:
                pass
            case _:
                return BLE_ERROR.BLE_ERROR_NOT_ACCEPTED

        response = BLE_ERROR.BLE_ERROR_FAILED

        command = BleMgrGapAdvStartCmd(adv_type)
        print("start_advertising calling _gap_adv_start_cmd_handler")
        response = await self.ble_manager.cmd_execute(command, self.ble_manager.gap_adv_start_cmd_handler)

        print(f"start_advertising returned from _gap_adv_start_cmd_handler. resposne={response.name}")

        return response


'''
    def _enable(self) -> BLE_ERROR:

        error = BLE_ERROR.BLE_ERROR_FAILED
        if self.ble_manager.dev_params.status == BLE_STATUS.BLE_IS_ENABLED:
            return BLE_ERROR.BLE_ERROR_ALREADY_DONE

        command = ble_mgr_msg_hdr(opcode=BLE_MGR_COMMON_CMD_OPCODE.BLE_MGR_COMMON_ENABLE_CMD,
                                  msg_len=0)  # TODO may be 4 or 5? shuold we create ctypes struct for ble_mgr_msg_hdr?
        response = ble_mgr_msg_hdr()
        # TODO create enable command
        if not self._ble_cmd_execute(command, response, self._ble_mgr_common_enable_cmd_handler):
            return BLE_ERROR.BLE_ERROR_BUSY

        # TODO error = response->status
        return error

    async def _ble_cmd_execute(self, command: ble_mgr_msg_hdr, response: ble_mgr_msg_hdr, handler: callable):
        ble_status = self.ble_manager.dev_params.status
        if ble_status == BLE_STATUS.BLE_IS_BUSY or ble_status == BLE_STATUS.BLE_IS_RESET:
            return False

        op_code = command.op_code

        handler(command)

        response = await self.ble_manager.ble_mgr_response_queue_get()

        print(f"Ble. _ble_cmd_execute: cmd={command}, cmd opcode={op_code} \
                response={response}, rsp->opcode={response.op_code}, handler={handler}")
        return True

    # TODO move to ble_gap
    def _ble_gap_role_set(self):
        pass

    async def _ble_mgr_common_enable_cmd_handler(self, param):

        command = ad_ble_msg(operation=AD_BLE_OPERATION.AD_BLE_OP_INIT_CMD, msg_len=5)
        self.ble_manager.add_to_wait_q(command)
        self.ble_manager.adapter_commnand_q.put_nowait(command)
'''
# TODO create ble_dev_params for default device ble database
