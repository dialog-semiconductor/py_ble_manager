from adapter.BleAdapter import BleAdapter
from ble_api.BleApiBase import BleApiBase
from ble_api.BleCommon import BLE_ERROR
from ble_api.BleGap import BLE_GAP_ROLE
from manager.BleManager import BleManager
from manager.BleManagerGapMsgs import BleMgrGapRoleSetCmd, BleMgrGapRoleSetRsp, BleMgrGapConnectCmd, \
     BleMgrGapConnectRsp

from services.BleService import BleServiceBase


class BleGapApi(BleApiBase):

    def __init__(self, ble_manager: BleManager, ble_adapter: BleAdapter):
        super().__init__(ble_manager, ble_adapter)

    async def role_set(self, role: BLE_GAP_ROLE) -> BLE_ERROR:
        response = BLE_ERROR.BLE_ERROR_FAILED
        command = BleMgrGapRoleSetCmd(role)
        response: BleMgrGapRoleSetRsp = await self.ble_manager.cmd_execute(command)
        return response.status

