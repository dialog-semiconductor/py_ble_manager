from ble_api.BleAtt import AttUuid
from ble_api.BleDeviceBase import BleDeviceBase
from ble_api.BleCommon import BLE_ERROR, BdAddress
from ble_api.BleGap import BLE_GAP_ROLE, gap_conn_params, GAP_SCAN_TYPE, GAP_SCAN_MODE, BleEventGapAdvReport, BleAdvData, GAP_DATA_TYPE


class BleCentral(BleDeviceBase):
    def __init__(self, com_port: str):
        super().__init__(com_port)

    async def start(self) -> BLE_ERROR:
        return await super().start(BLE_GAP_ROLE.GAP_CENTRAL_ROLE)

    async def connect(self, peer_addr: BdAddress, conn_params: gap_conn_params) -> None:
        return await self.ble_gap.connect(peer_addr, conn_params)

    async def discover_characteristics(self,
                                       conn_idx: int,
                                       start_h: int,
                                       end_h: int,
                                       uuid: AttUuid):
        return await self.ble_gattc.discover_characteristics(conn_idx, start_h, end_h, uuid)

    async def discover_services(self, conn_idx: int, uuid: AttUuid):
        return await self.ble_gattc.discover_services(conn_idx, uuid)

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

    async def scan_start(self,
                         type: GAP_SCAN_TYPE = GAP_SCAN_TYPE.GAP_SCAN_ACTIVE,
                         mode: GAP_SCAN_MODE = GAP_SCAN_MODE.GAP_SCAN_GEN_DISC_MODE,
                         interval: int = 0,
                         window: int = 0,
                         filt_wlist: bool = False,
                         filt_dupl: bool = False
                         ) -> BLE_ERROR:

        return await self.ble_gap.scan_start(type, mode, interval, window, filt_wlist, filt_dupl)
