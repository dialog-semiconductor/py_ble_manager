from adapter.BleAdapter import BleAdapter
from ble_api.BleApiBase import BleApiBase
from ble_api.BleCommon import BLE_ERROR, BdAddress, BLE_HCI_ERROR
from ble_api.BleGap import BLE_GAP_ROLE, GapConnParams, BLE_GAP_CONN_MODE, GAP_SCAN_TYPE, GAP_SCAN_MODE, \
    GAP_IO_CAPABILITIES
from manager.BleManager import BleManager
from manager.BleManagerGapMsgs import BleMgrGapRoleSetCmd, BleMgrGapRoleSetRsp, BleMgrGapConnectCmd, \
    BleMgrGapConnectRsp, BleMgrGapAdvStartCmd, BleMgrGapAdvStartRsp, BleMgrGapScanStartCmd, \
    BleMgrGapScanStartRsp, BleMgrGapDisconnectCmd, BleMgrGapDisconnectRsp, BleMgrGapConnectCancelCmd, \
    BleMgrGapConnectCancelRsp, BleMgrGapConnParamUpdateCmd, BleMgrGapConnParamUpdateRsp, \
    BleMgrGapConnParamUpdateReplyCmd, BleMgrGapConnParamUpdateReplyRsp, BleMgrGapPairCmd, BleMgrGapPairRsp, \
    BleMgrGapPairReplyCmd, BleMgrGapPairReplyRsp, BleMgrGapPasskeyReplyCmd, BleMgrGapPasskeyReplyRsp


class BleGapApi(BleApiBase):

    def __init__(self, ble_manager: BleManager, ble_adapter: BleAdapter):
        super().__init__(ble_manager, ble_adapter)

    async def conn_param_update_reply(self, conn_idx: int, accept: bool):
        command = BleMgrGapConnParamUpdateReplyCmd(conn_idx, accept)
        resposne: BleMgrGapConnParamUpdateReplyRsp = await self._ble_manager.cmd_execute(command)

        return resposne.status

    async def conn_param_update(self, conn_idx: int, conn_params: GapConnParams):

        command = BleMgrGapConnParamUpdateCmd(conn_idx, conn_params)
        resposne: BleMgrGapConnParamUpdateRsp = await self._ble_manager.cmd_execute(command)

        return resposne.status

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

    async def pair(self, conn_idx: int, bond: bool) -> BLE_ERROR:

        command = BleMgrGapPairCmd(conn_idx, bond)
        response: BleMgrGapPairRsp = await self._ble_manager.cmd_execute(command)

        return response.status

    async def passkey_reply(self, conn_idx: int, accept: bool, passkey: int):

        command = BleMgrGapPasskeyReplyCmd(conn_idx, accept, passkey)
        response: BleMgrGapPasskeyReplyRsp = await self._ble_manager.cmd_execute(command)

        return response.status

    async def pair_reply(self, conn_idx: int, accept: bool, bond: bool) -> BLE_ERROR:

        command = BleMgrGapPairReplyCmd(conn_idx, accept, bond)
        response: BleMgrGapPairReplyRsp = await self._ble_manager.cmd_execute(command)

        return response.status

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

    def set_io_cap(self, io_cap: GAP_IO_CAPABILITIES) -> BLE_ERROR:
        return self._ble_manager.set_io_cap(io_cap)

    async def start_advertising(self,
                                adv_type: BLE_GAP_CONN_MODE = BLE_GAP_CONN_MODE.GAP_CONN_MODE_UNDIRECTED
                                ) -> BLE_ERROR:

        command = BleMgrGapAdvStartCmd(adv_type)
        response: BleMgrGapAdvStartRsp = await self._ble_manager.cmd_execute(command)

        return response.status
