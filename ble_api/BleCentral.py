from ble_api.BleDeviceBase import BleDeviceBase
from ble_api.BleCommon import BLE_ERROR, bd_address
from ble_api.BleGap import BLE_GAP_ROLE, gap_conn_params, GAP_SCAN_TYPE, GAP_SCAN_MODE


class BleCentral(BleDeviceBase):
    def __init__(self, com_port: str):
        super().__init__(com_port)

    async def start(self) -> BLE_ERROR:
        return await super().start(BLE_GAP_ROLE.GAP_CENTRAL_ROLE)

    async def connect(self, peer_addr: bd_address, conn_params: gap_conn_params) -> None:
        return await self.ble_gap.connect(peer_addr, conn_params)

    async def scan_start(self,
                         type: GAP_SCAN_TYPE = GAP_SCAN_TYPE.GAP_SCAN_ACTIVE,
                         mode: GAP_SCAN_MODE = GAP_SCAN_MODE.GAP_SCAN_GEN_DISC_MODE,
                         interval: int = 0,
                         window: int = 0,
                         filt_wlist: bool = False,
                         filt_dupl: bool = False
                         ) -> BLE_ERROR:

        return await self.ble_gap.scan_start(type, mode, interval, window, filt_wlist, filt_dupl)