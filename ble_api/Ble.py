import asyncio

from adapter.BleAdapter import BleAdapter
from ble_api.BleApiBase import BleApiBase
from ble_api.BleAtt import ATT_ERROR
from ble_api.BleCommon import BleEventBase, BLE_ERROR
from ble_api.BleGap import BLE_GAP_ROLE, BLE_GAP_CONN_MODE, BLE_EVT_GAP, BleEventGapConnected, BleEventGapDisconnected
from ble_api.BleGatt import GATT_EVENT
from ble_api.BleGatts import BLE_EVT_GATTS, BleEventGattsReadReq, BleEventGattsWriteReq
from ble_api.BleGattsApi import BleGattsApi
from manager.BleManager import BleManager
from manager.BleManagerCommonMsgs import BleMgrCommonResetCmd, BleMgrCommonResetRsp
from manager.BleManagerGapMsgs import BleMgrGapRoleSetCmd, BleMgrGapRoleSetRsp, BleMgrGapAdvStartCmd, BleMgrGapAdvStartRsp
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
        self.ble_gatts = BleGattsApi(self.ble_manager, self.ble_adapter)

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

    def _handle_disconnected_evt(self, evt: BleEventGapDisconnected) -> None:
        for service in self._services:
            if service and service.disconnected_evt:
                service.disconnected_evt(evt)

    async def _handle_read_req_evt(self, evt: BleEventGattsReadReq) -> bool:
        service = self._find_service_by_handle(evt.handle)
        if service:
            if service.read_req:
                await service.read_req(evt)
            return True

        return False

    async def _handle_write_req_evt(self, evt: BleEventGattsWriteReq) -> bool:
        service = self._find_service_by_handle(evt.handle)
        if service:
            if service.write_req:
                await service.write_req(evt)
            return True

        return False

    def _ms_to_adv_slots(self, time_ms) -> int:
        return int((time_ms) * 1000 // 625)

    async def get_event(self, timeout_seconds: float = 0) -> BleEventBase:  # TODO add timeout?
        evt = None
        try:
            timeout = timeout_seconds if timeout_seconds > 0 else None
            evt = await asyncio.wait_for(self.ble_manager._mgr_event_queue_get(), timeout)
        except asyncio.TimeoutError:
            pass

        return evt

    async def get_value(self, handle: int, max_len: int) -> BLE_ERROR:
        error = BLE_ERROR.BLE_ERROR_FAILED
        service = self._find_service_by_handle(handle)
        if service:
            error = await self.ble_gatts.get_value(handle, max_len)
        return error

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
        # TODO not sure if included svc handled correctly                              
        if error == BLE_ERROR.BLE_STATUS_OK:
            for i in range(0, len(svc.included_services)):
                error, _ = await self.ble_gatts.add_include(svc.included_services[i].start_h)
                if error != BLE_ERROR.BLE_STATUS_OK:
                    break

            for i in range(0, len(svc.gatt_characteristics)):
                item = svc.gatt_characteristics[i]
                # TODO is there a case where you need the char declartion handle offset (h_offset)?
                error, _, svc.gatt_characteristics[i].char.handle.value = await self.ble_gatts.add_characteristic(item.char.uuid,
                                                                                                            item.char.prop,
                                                                                                            item.char.perm,
                                                                                                            item.char.max_len,
                                                                                                            item.char.flags)
                if error == BLE_ERROR.BLE_STATUS_OK:
                    for j in range(0, len(item.descriptors)):
                        desc = item.descriptors[j]
                        error, svc.gatt_characteristics[i].descriptors[j].handle.value = await self.ble_gatts.add_descriptor(desc.uuid,
                                                                                                                       desc.perm,
                                                                                                                       desc.max_len,
                                                                                                                       desc.flags)
                        if error != BLE_ERROR.BLE_STATUS_OK:
                            break
                    # Break out of both loops
                    if error != BLE_ERROR.BLE_STATUS_OK:
                        break
                else:
                    break

            if error == BLE_ERROR.BLE_STATUS_OK:

                error = await self.ble_gatts.register_service(svc)
                if error == BLE_ERROR.BLE_STATUS_OK:
                    self._services.append(svc)
                    svc.periph = self

        return error

    async def send_read_cfm(self,
                            conn_idx: int = 0, 
                            handle: int = 0, 
                            status: ATT_ERROR = ATT_ERROR.ATT_ERROR_OK, 
                            data: bytes = None
                            ) -> BLE_ERROR:

        return await self.ble_gatts.send_read_cfm(conn_idx, handle, status, data)

    async def send_write_cfm(self,
                             conn_idx: int = 0,
                             handle: int = 0,
                             status: ATT_ERROR = ATT_ERROR.ATT_ERROR_OK
                             ) -> BLE_ERROR:

        return await self.ble_gatts.send_write_cfm(conn_idx, handle, status)

    async def service_handle_event(self, evt: BleEventBase) -> bool:
        handled = False

        match evt.evt_code:
            case BLE_EVT_GAP.BLE_EVT_GAP_CONNECTED:
                self._handle_connected_evt(evt)
                # Connected event always marked as unhandled so app can handle

            case BLE_EVT_GAP.BLE_EVT_GAP_DISCONNECTED:
                self._handle_disconnected_evt(evt)
                # Disconnected event always marked as unhandled so app can handle

            case BLE_EVT_GATTS.BLE_EVT_GATTS_READ_REQ:
                handled = await self._handle_read_req_evt(evt)

            case BLE_EVT_GATTS.BLE_EVT_GATTS_WRITE_REQ:
                handled = await self._handle_write_req_evt(evt)


        return handled

        '''


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

    async def send_event(self,
                         conn_idx: int = 0,
                         handle: int = 0,
                         type: GATT_EVENT = GATT_EVENT.GATT_EVENT_NOTIFICATION,
                         value: bytes = None) -> BLE_ERROR:

        error = BLE_ERROR.BLE_ERROR_FAILED
        service = self._find_service_by_handle(handle)
        if service:
            error = await self.ble_gatts.send_event(conn_idx, handle, type, value)
        return error

    def set_advertising_interval(self, adv_intv_min_ms, adv_intv_max_ms) -> None:
        self.ble_manager.gap_mgr.dev_params.adv_intv_min = self._ms_to_adv_slots(adv_intv_min_ms)
        self.ble_manager.gap_mgr.dev_params.adv_intv_max = self._ms_to_adv_slots(adv_intv_max_ms)
        # TODO save current setting in local?

    async def set_value(self, handle: int, value: bytes) -> BLE_ERROR:
        error = BLE_ERROR.BLE_ERROR_FAILED
        service = self._find_service_by_handle(handle)
        if service:
            error = await self.ble_gatts.set_value(handle, value)
        return error
