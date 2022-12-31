import asyncio

from .BleGap import BLE_GAP_ROLE, BLE_GAP_CONN_MODE
from manager.BleManager import BleManager, BLE_ERROR
from adapter.BleAdapter import BleAdapter
from manager.BleManagerGap import BleMgrGapRoleSetCmd, BleMgrGapAdvStartCmd
from .BleCommon import BleMgrCommonResetCmd


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

        self.ble_manager = BleManager(app_command_q, app_resposne_q, app_event_q, adapter_command_q, adapter_event_q)
        self.ble_adapter = BleAdapter(com_port, adapter_command_q, adapter_event_q)

    async def _ble_reset(self) -> BLE_ERROR:
        response = BLE_ERROR.BLE_ERROR_FAILED
        command = BleMgrCommonResetCmd()
        # TODO remove handler arg entirely??
        response = await self.ble_manager.cmd_execute(command, self.ble_manager.common_mgr.reset_cmd_handler)

        return response

    async def _gap_role_set(self, role: BLE_GAP_ROLE) -> BLE_ERROR:
        response = BLE_ERROR.BLE_ERROR_FAILED
        command = BleMgrGapRoleSetCmd(role)
        # TODO remove handler arg entirely ??
        response = await self.ble_manager.cmd_execute(command, self.ble_manager.gap_mgr.role_set_cmd_handler)

        return response

    async def init(self) -> None:
        try:
            # Open the serial port the the 531
            await self.ble_adapter.open_serial_port()

            # Start always running BLE tasks
            self.ble_manager.init()
            self.ble_adapter.init()

        except asyncio.TimeoutError as e:
            raise e

    async def start(self) -> BLE_ERROR:

        error = BLE_ERROR.BLE_ERROR_FAILED
        error = await self._ble_reset()
        if error == BLE_ERROR.BLE_STATUS_OK:
            error = await self._gap_role_set(BLE_GAP_ROLE.GAP_PERIPHERAL_ROLE)

        return error

    def set_advertising_interval(self, adv_intv_min, adv_intv_max) -> BLE_ERROR:
        self.ble_manager.dev_params.adv_intv_min = int(adv_intv_min)
        self.ble_manager.dev_params.adv_intv_max = int(adv_intv_max)

        return BLE_ERROR.BLE_STATUS_OK

    async def start_advertising(self, adv_type: BLE_GAP_CONN_MODE = BLE_GAP_CONN_MODE.GAP_CONN_MODE_UNDIRECTED) -> BLE_ERROR:

        response = BLE_ERROR.BLE_ERROR_FAILED

        command = BleMgrGapAdvStartCmd(adv_type)
        # TODO remove handler arg entirely
        response = await self.ble_manager.cmd_execute(command, self.ble_manager.gap_mgr.adv_start_cmd_handler)

        return response
