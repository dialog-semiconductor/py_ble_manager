import asyncio

from adapter.BleAdapter import BleAdapter
from ble_api.BleDeviceBase import BleDeviceBase
from ble_api.BleAtt import ATT_ERROR
from ble_api.BleCommon import BleEventBase, BLE_ERROR, bd_address
from ble_api.BleGap import BLE_GAP_ROLE, gap_conn_params, GAP_SCAN_TYPE, GAP_SCAN_MODE, BLE_GAP_CONN_MODE, BLE_EVT_GAP, BleEventGapConnected, BleEventGapDisconnected
from ble_api.BleGatt import GATT_EVENT
from ble_api.BleGatts import BLE_EVT_GATTS, BleEventGattsReadReq, BleEventGattsWriteReq
from ble_api.BleGattsApi import BleGattsApi
from ble_api.BleStorageApi import BleStorageApi
from manager.BleManager import BleManager
from manager.BleManagerCommonMsgs import BleMgrCommonResetCmd, BleMgrCommonResetRsp
from manager.BleManagerGapMsgs import BleMgrGapRoleSetCmd, BleMgrGapRoleSetRsp, BleMgrGapAdvStartCmd, BleMgrGapAdvStartRsp
from services.BleService import BleServiceBase


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

