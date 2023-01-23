from ble_api.BleAtt import AttUuid
from ble_api.BleDeviceBase import BleDeviceBase
from ble_api.BleCommon import BLE_ERROR, BdAddress, BLE_HCI_ERROR
from ble_api.BleGap import BLE_GAP_ROLE, GapConnParams, GAP_SCAN_TYPE, GAP_SCAN_MODE, BleEventGapAdvReport, BleAdvData, GAP_DATA_TYPE


class BleCentral(BleDeviceBase):
    def __init__(self, com_port: str, gtl_debug: bool = False):
        super().__init__(com_port, gtl_debug)

    async def browse(self, conn_idx: int, uuid: AttUuid) -> BLE_ERROR:
        return await self._ble_gattc.browse(conn_idx, uuid)

    async def connect(self, peer_addr: BdAddress, conn_params: GapConnParams) -> None:
        return await self._ble_gap.connect(peer_addr, conn_params)

    async def connect_cancel(self) -> None:
        return await self._ble_gap.connect_cancel()

    async def disconect(self, conn_idx: int, reason: BLE_HCI_ERROR) -> BLE_ERROR:
        return await self._ble_gap.disconnect(conn_idx, reason)

    async def discover_descriptors(self,
                                   conn_idx: int,
                                   start_h: int,
                                   end_h: int) -> BLE_ERROR:
        return await self._ble_gattc.discover_descriptors(conn_idx, start_h, end_h)

    async def discover_characteristics(self,
                                       conn_idx: int,
                                       start_h: int,
                                       end_h: int,
                                       uuid: AttUuid) -> BLE_ERROR:
        return await self._ble_gattc.discover_characteristics(conn_idx, start_h, end_h, uuid)

    async def discover_services(self, conn_idx: int, uuid: AttUuid):
        return await self._ble_gattc.discover_services(conn_idx, uuid)

    def parse_adv_data(self, evt: BleEventGapAdvReport) -> list[BleAdvData]:
        data_ptr = 0
        adv_data_structs: BleAdvData = []
        # print(f"Parsing evt.data={list(evt.data)}")
        if evt.length > 0:
            while data_ptr < 31 and data_ptr < evt.length:

                print(f"data{list(evt.data)}")
                print(f"data_ptr = {data_ptr}, len{evt.length}, struct = {adv_data_structs}")
                print()

                struct = BleAdvData(len=evt.data[data_ptr], type=evt.data[data_ptr + 1])

                if struct.len == 0 or struct.type == GAP_DATA_TYPE.GAP_DATA_TYPE_NONE:
                    break

                data_ptr += 2
                struct.data = evt.data[data_ptr:(data_ptr + struct.len - 1)]  # -1 as calc includes AD Type
                data_ptr += struct.len - 1  # -1 as calc includes AD Type
                adv_data_structs.append(struct)

        return adv_data_structs

    async def read(self, conn_idx: int, handle: int, offset: int) -> BLE_ERROR:
        return await self._ble_gattc.read(conn_idx, handle, offset)

    async def scan_start(self,
                         type: GAP_SCAN_TYPE = GAP_SCAN_TYPE.GAP_SCAN_ACTIVE,
                         mode: GAP_SCAN_MODE = GAP_SCAN_MODE.GAP_SCAN_GEN_DISC_MODE,
                         interval: int = 0,
                         window: int = 0,
                         filt_wlist: bool = False,
                         filt_dupl: bool = False
                         ) -> BLE_ERROR:

        return await self._ble_gap.scan_start(type, mode, interval, window, filt_wlist, filt_dupl)

    async def start(self) -> BLE_ERROR:
        return await super().start(BLE_GAP_ROLE.GAP_CENTRAL_ROLE)

    async def write(self, conn_idx: int, handle: int, offset: int, value: bytes) -> BLE_ERROR:
        return await self._ble_gattc.write(conn_idx, handle, offset, value)

    async def write_no_resp(self, conn_idx: int, handle: int, signed_write: bool, value: bytes) -> BLE_ERROR:
        return await self._ble_gattc.write_no_resp(conn_idx, handle, signed_write, value)

    async def write_prepare(self, conn_idx: int, handle: int, offset: int, value: bytes) -> BLE_ERROR:
        return await self._ble_gattc.write_prepare(conn_idx, handle, offset, value)

    async def write_execute(self, conn_idx: int, commit: bool) -> BLE_ERROR:
        return await self._ble_gattc.write_execute(conn_idx, commit)
