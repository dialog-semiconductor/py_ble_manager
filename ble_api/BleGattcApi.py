from adapter.BleAdapter import BleAdapter
from ble_api.BleApiBase import BleApiBase
from ble_api.BleAtt import AttUuid, ATT_PERM, ATT_ERROR
from ble_api.BleCommon import BLE_ERROR
from ble_api.BleGatt import GATT_SERVICE, GATT_PROP, GATT_EVENT
from ble_api.BleGatts import GATTS_FLAGS
from manager.BleManager import BleManager
from manager.BleManagerGattcMsgs import BleMgrGattcDiscoverSvcCmd, BleMgrGattcDiscoverSvcRsp, \
    BleMgrGattcDiscoverCharCmd, BleMgrGattcDiscoverCharRsp, BleMgrGattcDiscoverDescCmd, BleMgrGattcDiscoverDescRsp, \
    BleMgrGattcBrowseCmd, BleMgrGattcBrowseRsp, BleMgrGattcReadCmd, BleMgrGattcReadRsp, BleMgrGattcWriteGenericCmd, \
    BleMgrGattcWriteGenericRsp, BleMgrGattcWriteExecuteCmd, BleMgrGattcWriteExecuteRsp


class BleGattcApi(BleApiBase):

    def __init__(self, ble_manager: BleManager, ble_adapter: BleAdapter):
        super().__init__(ble_manager, ble_adapter)

    async def browse(self,
                     conn_idx: int,
                     uuid: AttUuid) -> BLE_ERROR:

        command = BleMgrGattcBrowseCmd(conn_idx, uuid)
        resposne: BleMgrGattcBrowseRsp = await self.ble_manager.cmd_execute(command)

        return resposne.status

    async def discover_characteristics(self,
                                       conn_idx: int,
                                       start_h: int,
                                       end_h: int,
                                       uuid: AttUuid) -> BLE_ERROR:
        command = BleMgrGattcDiscoverCharCmd(conn_idx, start_h, end_h, uuid)
        response: BleMgrGattcDiscoverCharRsp = await self.ble_manager.cmd_execute(command)

        return response.status

    async def discover_descriptors(self,
                                   conn_idx: int,
                                   start_h: int,
                                   end_h: int) -> BLE_ERROR:

        command = BleMgrGattcDiscoverDescCmd(conn_idx, start_h, end_h)
        response: BleMgrGattcDiscoverDescRsp = await self.ble_manager.cmd_execute(command)

        return response.status

    async def discover_services(self, conn_idx: int, uuid: AttUuid):
        command = BleMgrGattcDiscoverSvcCmd(conn_idx, uuid)
        response: BleMgrGattcDiscoverSvcRsp = await self.ble_manager.cmd_execute(command)

        return response.status

    async def read(self, conn_idx: int, handle: int, offset: int) -> BLE_ERROR:
        command = BleMgrGattcReadCmd(conn_idx, handle, offset)
        response: BleMgrGattcReadRsp = await self.ble_manager.cmd_execute(command)

        return response.status

    async def write(self, conn_idx: int, handle: int, offset: int, value: bytes) -> BLE_ERROR:
        command = BleMgrGattcWriteGenericCmd(conn_idx=conn_idx, handle=handle, offset=offset, value=value)
        response: BleMgrGattcWriteGenericRsp = await self.ble_manager.cmd_execute(command)

        return response.status

    async def write_no_resp(self, conn_idx: int, handle: int, signed_write: bool, value: bytes) -> BLE_ERROR:
        command = BleMgrGattcWriteGenericCmd(conn_idx=conn_idx,
                                             handle=handle,
                                             no_response=True,
                                             signed_write=signed_write,
                                             value=value)
        response: BleMgrGattcWriteGenericRsp = await self.ble_manager.cmd_execute(command)

        return response.status

    async def write_prepare(self, conn_idx: int, handle: int, offset: int, value: bytes) -> BLE_ERROR:
        command = BleMgrGattcWriteGenericCmd(conn_idx=conn_idx,
                                             handle=handle,
                                             prepare=True,
                                             offset=offset,
                                             value=value)
        response: BleMgrGattcWriteGenericRsp = await self.ble_manager.cmd_execute(command)

        return response.status

    async def write_execute(self, conn_idx: int, commit: bool) -> BLE_ERROR:
        command = BleMgrGattcWriteExecuteCmd(conn_idx, commit)
        response: BleMgrGattcWriteExecuteRsp = await self.ble_manager.cmd_execute(command)

        return response.status
