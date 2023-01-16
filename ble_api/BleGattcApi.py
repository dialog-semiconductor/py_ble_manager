from adapter.BleAdapter import BleAdapter
from ble_api.BleApiBase import BleApiBase
from ble_api.BleAtt import AttUuid, ATT_PERM, ATT_ERROR
from ble_api.BleCommon import BLE_ERROR
from ble_api.BleGatt import GATT_SERVICE, GATT_PROP, GATT_EVENT
from ble_api.BleGatts import GATTS_FLAGS
from manager.BleManager import BleManager
from manager.BleManagerGattcMsgs import BleMgrGattcDiscoverSvcCmd, BleMgrGattcDiscoverSvcRsp


class BleGattcApi(BleApiBase):

    def __init__(self, ble_manager: BleManager, ble_adapter: BleAdapter):
        super().__init__(ble_manager, ble_adapter)

    async def discover_services(self, conn_idx: int, uuid: AttUuid):
        command = BleMgrGattcDiscoverSvcCmd(conn_idx, uuid)
        response: BleMgrGattcDiscoverSvcRsp = await self.ble_manager.cmd_execute(command)
        
        return response.status
