import asyncio

from .BleGap import BLE_GAP_ROLE, BLE_GAP_CONN_MODE
from manager.BleManager import BleManager, BLE_ERROR
from adapter.BleAdapter import BleAdapter
from manager.BleManagerGap import BleMgrGapRoleSetCmd, BleMgrGapRoleSetRsp, BleMgrGapAdvStartCmd, BleMgrGapAdvStartRsp
from manager.BleManagerCommon import BleMgrCommonResetCmd, BleMgrCommonResetRsp, BleMgrMsgBase
from .BleCommon import BleEventBase


# common
class BleApiBase():
    def __init__(self, ble_manager: BleManager, ble_adapter: BleAdapter):
        self.ble_manager = ble_manager
        self.ble_adapter = ble_adapter


class BleClient(BleApiBase):
    pass


class BlePeripheral(BleApiBase):
    def __init__(self, com_port: str):

        app_command_q = asyncio.Queue()
        app_resposne_q = asyncio.Queue()
        app_event_q = asyncio.Queue()

        adapter_command_q = asyncio.Queue()
        adapter_event_q = asyncio.Queue()

        self.ble_manager = BleManager(app_command_q, app_resposne_q, app_event_q, adapter_command_q, adapter_event_q)
        self.ble_adapter = BleAdapter(com_port, adapter_command_q, adapter_event_q)

    async def _ble_reset(self) -> BleMgrCommonResetRsp:
        response = BLE_ERROR.BLE_ERROR_FAILED
        command = BleMgrCommonResetCmd()
        # TODO remove handler arg entirely??
        response = await self.ble_manager.cmd_execute(command)

        return response

    async def _gap_role_set(self, role: BLE_GAP_ROLE) -> BleMgrGapRoleSetRsp:
        command = BleMgrGapRoleSetCmd(role)
        response = await self.ble_manager.cmd_execute(command)
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

    async def get_event(self, timeout_seconds: float = 0) -> BleEventBase:  # TODO add timeout?
        evt = None
        try:
            timeout = timeout_seconds if timeout_seconds > 0 else None
            evt = await asyncio.wait_for(self.ble_manager._api_event_queue_get(), timeout)
        except asyncio.TimeoutError:
            pass

        return evt

    async def start(self) -> BleMgrMsgBase:

        error = await self._ble_reset()
        if error.status == BLE_ERROR.BLE_STATUS_OK:
            error = await self._gap_role_set(BLE_GAP_ROLE.GAP_PERIPHERAL_ROLE)

        return error

    def set_advertising_interval(self, adv_intv_min, adv_intv_max) -> None:
        self.ble_manager.gap_mgr.dev_params.adv_intv_min = int(adv_intv_min)
        self.ble_manager.gap_mgr.dev_params.adv_intv_max = int(adv_intv_max)
        # TODO save current setting in local?

    async def start_advertising(self,
                                adv_type: BLE_GAP_CONN_MODE = BLE_GAP_CONN_MODE.GAP_CONN_MODE_UNDIRECTED
                                ) -> BleMgrGapAdvStartRsp:

        command = BleMgrGapAdvStartCmd(adv_type)
        response = await self.ble_manager.cmd_execute(command)
        return response
