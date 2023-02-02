import asyncio
from adapter.BleAdapter import BleAdapter
from ble_api.BleAtt import ATT_ERROR
from ble_api.BleCommon import BleEventBase, BLE_ERROR
from ble_api.BleGap import BLE_GAP_ROLE, BLE_GAP_CONN_MODE, BLE_EVT_GAP, BleEventGapConnected, \
    BleEventGapDisconnected, GAP_IO_CAPABILITIES
from ble_api.BleGapApi import BleGapApi
from ble_api.BleGatt import GATT_EVENT
from ble_api.BleGattcApi import BleGattcApi
from ble_api.BleGatts import BLE_EVT_GATTS, BleEventGattsReadReq, BleEventGattsWriteReq
from ble_api.BleGattsApi import BleGattsApi
from ble_api.BleStorageApi import BleStorageApi
from manager.BleManager import BleManager
from manager.BleManagerCommonMsgs import BleMgrCommonResetCmd, BleMgrCommonResetRsp
from manager.BleManagerGapMsgs import BleMgrGapRoleSetCmd, BleMgrGapRoleSetRsp, BleMgrGapAdvStartCmd, BleMgrGapAdvStartRsp
from services.BleService import BleServiceBase


class BleDeviceBase():
    def __init__(self, com_port: str, gtl_debug: bool = False):
        app_command_q = asyncio.Queue()
        app_resposne_q = asyncio.Queue()
        app_event_q = asyncio.Queue()

        adapter_command_q = asyncio.Queue()
        adapter_event_q = asyncio.Queue()

        self._ble_manager = BleManager(app_command_q, app_resposne_q, app_event_q, adapter_command_q, adapter_event_q)
        self._ble_adapter = BleAdapter(com_port, adapter_command_q, adapter_event_q, gtl_debug)
        self._ble_gap = BleGapApi(self._ble_manager, self._ble_adapter)
        self._ble_gattc = BleGattcApi(self._ble_manager, self._ble_adapter)
        self._ble_gatts = BleGattsApi(self._ble_manager, self._ble_adapter)
        self._ble_storage = BleStorageApi(self._ble_manager, self._ble_adapter)

        self._services: list[BleServiceBase] = []

    async def _ble_reset(self) -> BLE_ERROR:
        response = BLE_ERROR.BLE_ERROR_FAILED
        command = BleMgrCommonResetCmd()
        response: BleMgrCommonResetRsp = await self._ble_manager.cmd_execute(command)
        return response.status

    async def init(self) -> None:
        try:
            # Open the serial port the the 531
            await self._ble_adapter.open_serial_port()

            # Start always running BLE tasks
            self._ble_manager.init()
            self._ble_adapter.init()
        except asyncio.TimeoutError as e:
            raise e

    async def get_event(self, timeout_seconds: float = 0) -> BleEventBase:
        evt = None
        try:
            timeout = timeout_seconds if timeout_seconds > 0 else None
            evt = await asyncio.wait_for(self._ble_manager.mgr_event_queue_get(), timeout)
        except asyncio.TimeoutError:
            pass

        return evt

    async def numeric_reply(self, conn_idx: int, accept: bool):
        return await self._ble_gap.numeric_reply(conn_idx, accept)

    def set_io_cap(self, io_cap: GAP_IO_CAPABILITIES) -> BLE_ERROR:
        return self._ble_manager.set_io_cap(io_cap)

    async def start(self, role: BLE_GAP_ROLE) -> BLE_ERROR:

        error = await self._ble_reset()
        if error == BLE_ERROR.BLE_STATUS_OK:
            error = await self._ble_gap.role_set(role)

        return error

    def storage_get_int(self, conn_idx: int, key: int) -> tuple[BLE_ERROR, int]:
        return self._ble_storage.get_int(conn_idx, key)

    def storage_put_int(self, conn_idx: int, key: int, value: int, persistent: bool) -> BLE_ERROR:
        return self._ble_storage.put_int(conn_idx, key, value, persistent)
