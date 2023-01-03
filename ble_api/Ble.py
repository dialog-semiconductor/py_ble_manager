import asyncio
from .BleApiBase import BleApiBase, BleManager, BleAdapter
# from adapter.BleAdapter import BleAdapter
# from manager.BleManager import BleManager
from manager.BleManagerGap import BleMgrGapRoleSetCmd, BleMgrGapRoleSetRsp, BleMgrGapAdvStartCmd, BleMgrGapAdvStartRsp
from manager.BleManagerCommon import BleMgrCommonResetCmd, BleMgrCommonResetRsp
from services.BleService import BleServiceBase
from .BleCommon import BleEventBase, BLE_ERROR
from .BleGap import BLE_GAP_ROLE, BLE_GAP_CONN_MODE
from .BleGatts import BleGatts


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
        self.ble_gatts = BleGatts(self.ble_manager, self.ble_adapter)

    async def _ble_reset(self) -> BLE_ERROR:
        response = BLE_ERROR.BLE_ERROR_FAILED
        command = BleMgrCommonResetCmd()
        response: BleMgrCommonResetRsp = await self.ble_manager.cmd_execute(command)
        return response.status

    async def _gap_role_set(self, role: BLE_GAP_ROLE) -> BLE_ERROR:
        response = BLE_ERROR.BLE_ERROR_FAILED
        command = BleMgrGapRoleSetCmd(role)
        response: BleMgrGapRoleSetRsp = await self.ble_manager.cmd_execute(command)
        return response.status

    async def get_event(self, timeout_seconds: float = 0) -> BleEventBase:  # TODO add timeout?
        evt = None
        try:
            timeout = timeout_seconds if timeout_seconds > 0 else None
            evt = await asyncio.wait_for(self.ble_manager._mgr_event_queue_get(), timeout)
        except asyncio.TimeoutError:
            pass

        return evt

    async def init(self) -> None:
        try:
            # Open the serial port the the 531
            await self.ble_adapter.open_serial_port()

            # Start always running BLE tasks
            self.ble_manager.init()
            self.ble_adapter.init()

        except asyncio.TimeoutError as e:
            raise e

    async def register_service(self, svc: BleServiceBase) -> BLE_ERROR:

        error = await self.ble_gatts.add_service(svc.gatt_service.uuid,
                                                 svc.gatt_service.type,
                                                 svc.gatt_service.num_attrs)
        if error == BLE_ERROR.BLE_STATUS_OK:
            for item in svc.gatt_characteristics:
                error, h_offset, h_val_offset = await self.ble_gatts.add_characteristic(item.char.uuid,
                                                                                        item.char.prop,
                                                                                        item.char.perm,
                                                                                        item.char.max_len,
                                                                                        item.char.flags)
                if error == BLE_ERROR.BLE_STATUS_OK:
                    # error = await self.ble_gatts.add_descriptor(item.descriptor)
                    # if error == BLE_ERROR.BLE_STATUS_OK:
                    pass
                else:
                    break
            error = await self.ble_gatts.register_service()

        return error

    async def start(self) -> BLE_ERROR:

        error = await self._ble_reset()
        if error == BLE_ERROR.BLE_STATUS_OK:
            error = await self._gap_role_set(BLE_GAP_ROLE.GAP_PERIPHERAL_ROLE)

        return error

    async def start_advertising(self,
                                adv_type: BLE_GAP_CONN_MODE = BLE_GAP_CONN_MODE.GAP_CONN_MODE_UNDIRECTED
                                ) -> BLE_ERROR:

        response = BLE_ERROR.BLE_ERROR_FAILED
        command = BleMgrGapAdvStartCmd(adv_type)
        response: BleMgrGapAdvStartRsp = await self.ble_manager.cmd_execute(command)
        return response.status

    def set_advertising_interval(self, adv_intv_min_ms, adv_intv_max_ms) -> None:
        self.ble_manager.gap_mgr.dev_params.adv_intv_min = self._ms_to_adv_slots(adv_intv_min_ms)
        self.ble_manager.gap_mgr.dev_params.adv_intv_max = self._ms_to_adv_slots(adv_intv_max_ms)
        # TODO save current setting in local?

    def _ms_to_adv_slots(self, time_ms) -> int:
        return int((time_ms) * 1000 // 625)
