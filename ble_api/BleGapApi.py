from adapter.BleAdapter import BleAdapter
from ble_api.BleApiBase import BleApiBase
from ble_api.BleCommon import BLE_ERROR, BdAddress, BLE_HCI_ERROR
from ble_api.BleGap import BLE_GAP_ROLE, GapConnParams, BLE_GAP_CONN_MODE, GAP_SCAN_TYPE, GAP_SCAN_MODE
from manager.BleManager import BleManager
from manager.BleManagerGapMsgs import BleMgrGapRoleSetCmd, BleMgrGapRoleSetRsp, BleMgrGapConnectCmd, \
    BleMgrGapConnectRsp, BleMgrGapAdvStartCmd, BleMgrGapAdvStartRsp, BleMgrGapScanStartCmd, \
    BleMgrGapScanStartRsp, BleMgrGapDisconnectCmd, BleMgrGapDisconnectRsp, BleMgrGapConnectCancelCmd, \
    BleMgrGapConnectCancelRsp

from services.BleService import BleServiceBase


class BleGapApi(BleApiBase):

    def __init__(self, ble_manager: BleManager, ble_adapter: BleAdapter):
        super().__init__(ble_manager, ble_adapter)

    async def connect(self, peer_addr: BdAddress, conn_params: GapConnParams) -> BLE_ERROR:

        command = BleMgrGapConnectCmd(peer_addr, conn_params)
        resposne: BleMgrGapConnectRsp = await self._ble_manager.cmd_execute(command)

        return resposne.status

    async def connect_cancel(self) -> BLE_ERROR:

        command = BleMgrGapConnectCancelCmd()
        resposne: BleMgrGapConnectCancelRsp = await self._ble_manager.cmd_execute(command)

        return resposne.status

    async def disconnect(self, conn_idx: int, reason: BLE_HCI_ERROR) -> BLE_ERROR:

        command = BleMgrGapDisconnectCmd(conn_idx, reason)
        resposne: BleMgrGapDisconnectRsp = await self._ble_manager.cmd_execute(command)

        return resposne.status

    async def role_set(self, role: BLE_GAP_ROLE) -> BLE_ERROR:

        command = BleMgrGapRoleSetCmd(role)
        response: BleMgrGapRoleSetRsp = await self._ble_manager.cmd_execute(command)

        return response.status

    async def scan_start(self,
                         type: GAP_SCAN_TYPE = GAP_SCAN_TYPE.GAP_SCAN_ACTIVE, 
                         mode: GAP_SCAN_MODE = GAP_SCAN_MODE.GAP_SCAN_GEN_DISC_MODE,
                         interval: int = 0,
                         window: int = 0,
                         filt_wlist: bool = False,
                         filt_dupl: bool = False
                         ) -> BLE_ERROR:

        command = BleMgrGapScanStartCmd(type, mode, interval, window, filt_wlist, filt_dupl)
        response: BleMgrGapScanStartRsp = await self._ble_manager.cmd_execute(command)

        return response.status

    async def start_advertising(self,
                                adv_type: BLE_GAP_CONN_MODE = BLE_GAP_CONN_MODE.GAP_CONN_MODE_UNDIRECTED
                                ) -> BLE_ERROR:

        command = BleMgrGapAdvStartCmd(adv_type)
        response: BleMgrGapAdvStartRsp = await self._ble_manager.cmd_execute(command)

        return response.status
