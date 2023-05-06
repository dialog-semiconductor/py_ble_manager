import threading
from ..ble_api.BleAtt import AttUuid
from ..ble_api.BleConfig import BleConfigDefault, BLE_DEVICE_TYPE
from ..ble_devices.BleDeviceBase import BleDeviceBase
from ..ble_api.BleCommon import BLE_ERROR, BdAddress, BLE_HCI_ERROR, BleEventBase, BLE_EVT_GAP
from ..ble_api.BleGap import BLE_GAP_ROLE, GapConnParams, GAP_SCAN_TYPE, GAP_SCAN_MODE, \
    BleEventGapConnParamUpdateReq


class BleCentral(BleDeviceBase):
    def __init__(self,
                 com_port: str,
                 ble_config: BleConfigDefault = BleConfigDefault(BLE_DEVICE_TYPE.CENTRAL),
                 gtl_debug: bool = False):
        super().__init__(com_port, ble_config, gtl_debug)

    def browse(self, conn_idx: int, uuid: AttUuid) -> BLE_ERROR:
        return self._ble_gattc.browse(conn_idx, uuid)

    def conn_param_update(self, conn_idx: int, conn_params: GapConnParams):
        return self._ble_gap.conn_param_update(conn_idx, conn_params)

    def connect(self, peer_addr: BdAddress, conn_params: GapConnParams) -> None:
        return self._ble_gap.connect(peer_addr, conn_params)

    def connect_cancel(self) -> None:
        return self._ble_gap.connect_cancel()

    def disconect(self, conn_idx: int, reason: BLE_HCI_ERROR) -> BLE_ERROR:
        return self._ble_gap.disconnect(conn_idx, reason)

    def discover_descriptors(self,
                             conn_idx: int,
                             start_h: int,
                             end_h: int) -> BLE_ERROR:
        return self._ble_gattc.discover_descriptors(conn_idx, start_h, end_h)

    def discover_characteristics(self,
                                 conn_idx: int,
                                 start_h: int,
                                 end_h: int,
                                 uuid: AttUuid
                                 ) -> BLE_ERROR:
        return self._ble_gattc.discover_characteristics(conn_idx, start_h, end_h, uuid)

    def discover_services(self, conn_idx: int, uuid: AttUuid):
        return self._ble_gattc.discover_services(conn_idx, uuid)

    def handle_event_default(self, evt: BleEventBase):
        match evt.evt_code:
            case BLE_EVT_GAP.BLE_EVT_GAP_CONN_PARAM_UPDATE_REQ:
                evt: BleEventGapConnParamUpdateReq = evt
                self.conn_param_update_reply(evt.conn_idx, True)

    def pair(self, conn_idx: int, bond: bool) -> BLE_ERROR:
        return self._ble_gap.pair(conn_idx, bond)

    def passkey_reply(self, conn_idx: int, accept: bool, passkey: int):
        return self._ble_gap.passkey_reply(conn_idx, accept, passkey)

    def read(self, conn_idx: int, handle: int, offset: int) -> BLE_ERROR:
        return self._ble_gattc.read(conn_idx, handle, offset)

    def scan_start(self,
                   type: GAP_SCAN_TYPE = GAP_SCAN_TYPE.GAP_SCAN_ACTIVE,
                   mode: GAP_SCAN_MODE = GAP_SCAN_MODE.GAP_SCAN_GEN_DISC_MODE,
                   interval: int = 0,
                   window: int = 0,
                   filt_wlist: bool = False,
                   filt_dupl: bool = False
                   ) -> BLE_ERROR:

        return self._ble_gap.scan_start(type, mode, interval, window, filt_wlist, filt_dupl)

    def start(self) -> BLE_ERROR:
        return super().start(BLE_GAP_ROLE.GAP_CENTRAL_ROLE)

    def write(self, conn_idx: int, handle: int, offset: int, value: bytes) -> BLE_ERROR:
        return self._ble_gattc.write(conn_idx, handle, offset, value)

    def write_no_resp(self, conn_idx: int, handle: int, signed_write: bool, value: bytes) -> BLE_ERROR:
        return self._ble_gattc.write_no_resp(conn_idx, handle, signed_write, value)

    def write_prepare(self, conn_idx: int, handle: int, offset: int, value: bytes) -> BLE_ERROR:
        return self._ble_gattc.write_prepare(conn_idx, handle, offset, value)

    def write_execute(self, conn_idx: int, commit: bool) -> BLE_ERROR:
        return self._ble_gattc.write_execute(conn_idx, commit)
