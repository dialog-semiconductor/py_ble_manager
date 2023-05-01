import concurrent.futures
import queue
import threading
from adapter.BleAdapter import BleAdapter
# from ble_api.BleAtt import ATT_ERROR
from ble_api.BleCommon import BleEventBase, BLE_ERROR
from ble_api.BleGap import BLE_GAP_ROLE, GAP_IO_CAPABILITIES  # BLE_GAP_CONN_MODE, BLE_EVT_GAP, BleEventGapConnected, \
    # BleEventGapDisconnected
from ble_api.BleGapApi import BleGapApi, GapConnParams
# from ble_api.BleGatt import GATT_EVENT
from ble_api.BleGattcApi import BleGattcApi
# from ble_api.BleGatts import BLE_EVT_GATTS, BleEventGattsReadReq, BleEventGattsWriteReq
from ble_api.BleGattsApi import BleGattsApi
from ble_api.BleStorageApi import BleStorageApi
from manager.BleManager import BleManager
from manager.BleManagerCommonMsgs import BleMgrCommonResetCmd, BleMgrCommonResetRsp
# from manager.BleManagerGapMsgs import BleMgrGapRoleSetCmd, BleMgrGapRoleSetRsp, BleMgrGapAdvStartCmd, BleMgrGapAdvStartRsp
from services.BleService import BleServiceBase
from serial_manager.SerialStreamManager import SerialStreamManager


class BleDeviceBase():
    def __init__(self, com_port: str, shutdown_event: threading.Event = threading.Event(), gtl_debug: bool = False):
        app_command_q = queue.Queue()
        app_resposne_q = queue.Queue()
        app_event_q = queue.Queue()

        adapter_command_q = queue.Queue()
        adapter_event_q = queue.Queue()
        serial_tx_q = queue.Queue()
        serial_rx_q = queue.Queue()
        self._shutdown_event = shutdown_event

        # Internal BLE framework layers
        self._ble_manager = BleManager(app_command_q, app_resposne_q, app_event_q, adapter_command_q, adapter_event_q, self._shutdown_event)
        self._ble_adapter = BleAdapter(adapter_command_q, adapter_event_q, serial_tx_q, serial_rx_q, self._shutdown_event, gtl_debug)
        self._serial_stream_manager = SerialStreamManager(com_port, serial_tx_q, serial_rx_q, self._shutdown_event)

        # Dialog APIqueue
        self._ble_gap = BleGapApi(self._ble_manager, self._ble_adapter)
        self._ble_gattc = BleGattcApi(self._ble_manager, self._ble_adapter)
        self._ble_gatts = BleGattsApi(self._ble_manager, self._ble_adapter)
        self._ble_storage = BleStorageApi(self._ble_manager, self._ble_adapter)

        self._services: list[BleServiceBase] = []

    def _ble_reset(self) -> BLE_ERROR:
        command = BleMgrCommonResetCmd()
        response: BleMgrCommonResetRsp = self._ble_manager.cmd_execute(command)
        return response.status

    def conn_param_update(self, conn_idx: int, conn_params: GapConnParams) -> BLE_ERROR:
        return self._ble_gap.conn_param_update(conn_idx, conn_params)

    def conn_param_update_reply(self, conn_idx: int, accept: bool) -> BLE_ERROR:
        return self._ble_gap.conn_param_update_reply(conn_idx, accept)

    def init(self) -> None:
        try:
            # Open the serial port the the 531
            self._serial_stream_manager.open_serial_port()  # TODO implement a timeout for opening the serial port

            # Start always running BLE tasks
            self._ble_manager.init()
            self._ble_adapter.init()
            self._serial_stream_manager.init()

        except concurrent.futures.TimeoutError as e:
            raise e

    def get_event(self) -> BleEventBase:
        evt = None
        while evt is None:
            try:
                if self._shutdown_event.is_set():
                    print("Exiting get_event")
                    return
                evt = self._ble_manager.mgr_event_queue_get(timeout=1)
            except queue.Empty:
                pass
        return evt

    def numeric_reply(self, conn_idx: int, accept: bool):
        return self._ble_gap.numeric_reply(conn_idx, accept)

    def set_io_cap(self, io_cap: GAP_IO_CAPABILITIES) -> BLE_ERROR:
        return self._ble_manager.set_io_cap(io_cap)

    def shutdown(self) -> None:
        self._shutdown_event.set()

    def start(self, role: BLE_GAP_ROLE) -> BLE_ERROR:

        error = self._ble_reset()
        if error == BLE_ERROR.BLE_STATUS_OK:
            error = self._ble_gap.role_set(role)

        return error

    def storage_get_int(self, conn_idx: int, key: int) -> tuple[BLE_ERROR, int]:
        return self._ble_storage.get_int(conn_idx, key)

    def storage_put_int(self, conn_idx: int, key: int, value: int, persistent: bool) -> BLE_ERROR:
        return self._ble_storage.put_int(conn_idx, key, value, persistent)
