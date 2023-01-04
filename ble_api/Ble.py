import asyncio
from .BleApiBase import BleApiBase, BleManager, BleAdapter
# from adapter.BleAdapter import BleAdapter
# from manager.BleManager import BleManager
from manager.BleManagerGap import BleMgrGapRoleSetCmd, BleMgrGapRoleSetRsp, BleMgrGapAdvStartCmd, BleMgrGapAdvStartRsp, BleEventGapConnected
from manager.BleManagerCommon import BleMgrCommonResetCmd, BleMgrCommonResetRsp
from manager.BleManagerGatts import BleEventGattsReadReq
from .BleCommon import BleEventBase, BLE_ERROR
from .BleGap import BLE_GAP_ROLE, BLE_GAP_CONN_MODE, BLE_EVT_GAP
from .BleGatts import BleGatts, BLE_EVT_GATTS
from services.BleService import BleServiceBase


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

        self._services: list[BleServiceBase] = []

    async def _ble_reset(self) -> BLE_ERROR:
        response = BLE_ERROR.BLE_ERROR_FAILED
        command = BleMgrCommonResetCmd()
        response: BleMgrCommonResetRsp = await self.ble_manager.cmd_execute(command)
        return response.status

    def _find_service_by_handle(self, handle: int) -> BleServiceBase:
        for service in self._services:
            if service and handle >= service.start_h and handle <= service.end_h:
                return service
        return None

    async def _gap_role_set(self, role: BLE_GAP_ROLE) -> BLE_ERROR:
        response = BLE_ERROR.BLE_ERROR_FAILED
        command = BleMgrGapRoleSetCmd(role)
        response: BleMgrGapRoleSetRsp = await self.ble_manager.cmd_execute(command)
        return response.status

    def _handle_connected_evt(self, evt: BleEventGapConnected) -> None:
        for service in self._services:
            if service and service.connected_evt:
                service.connected_evt(evt)

    async def _handle_read_req_evt(self, evt: BleEventGattsReadReq) -> bool:
        service = self._find_service_by_handle(evt.handle)
        if service:
            if service.read_req:
                status, data = service.read_req(evt)

                error = await self.ble_gatts.send_read_cfm(evt.conn_idx, evt.handle, status, data)
                if error != BLE_ERROR.BLE_STATUS_OK:
                    # TODO raise error? Return additional value? 
                    pass
            return True

        return False

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

    async def register_service(self, svc: BleServiceBase) -> tuple[BLE_ERROR, BleServiceBase]:

        error = await self.ble_gatts.add_service(svc.gatt_service.uuid,
                                                 svc.gatt_service.type,
                                                 svc.gatt_service.num_attrs)
        if error == BLE_ERROR.BLE_STATUS_OK:
            for i in range(0, len(svc.gatt_characteristics)):
                print(f"Adding char: {i}, {svc.gatt_characteristics[i]}")
                item = svc.gatt_characteristics[i]
                # TODO is there a case where you need the char declartion handle offset (h_offset)?
                error, char_decl, svc.gatt_characteristics[i].char.handle = await self.ble_gatts.add_characteristic(item.char.uuid,
                                                                                                            item.char.prop,
                                                                                                            item.char.perm,
                                                                                                            item.char.max_len,
                                                                                                            item.char.flags)
                print(f"ChAR ADDEDE. {i}, error={error}, decl={char_decl}, handle={svc.gatt_characteristics[i].char.handle}")
                if error == BLE_ERROR.BLE_STATUS_OK:
                    # error = await self.ble_gatts.add_descriptor(item.descriptor)
                    # if error == BLE_ERROR.BLE_STATUS_OK:
                    pass
                else:
                    break
            error, registerd_svc = await self.ble_gatts.register_service(svc)

            if error == BLE_ERROR.BLE_STATUS_OK:
                self._services.append(registerd_svc)

        return error, registerd_svc

    async def service_handle_event(self, evt: BleEventBase) -> bool:
        match evt.evt_code:
            case BLE_EVT_GAP.BLE_EVT_GAP_CONNECTED:
                self._handle_connected_evt(evt)
                return False  # make it "not handled" so app can handle _find_service_by_handle. TODO dont use multiple returns
            
            case BLE_EVT_GATTS.BLE_EVT_GATTS_READ_REQ:
                return await self._handle_read_req_evt(evt)

        return False

        '''
        case BLE_EVT_GAP.BLE_EVT_GAP_DISCONNECTED:
                disconnected_evt((const ble_evt_gap_disconnected_t *) evt);
                return false; // make it "not handled" so app can handle

        case return.BLE_EVT_GATTS_WRITE_REQ:
                return write_req((const ble_evt_gatts_write_req_t *) evt);
        case return.BLE_EVT_GATTS_PREPARE_WRITE_REQ:
                return prepare_write_req((const ble_evt_gatts_prepare_write_req_t *) evt);
        case return.BLE_EVT_GATTS_EVENT_SENT:
                return event_sent((const ble_evt_gatts_event_sent_t *) evt);
        '''

    
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
