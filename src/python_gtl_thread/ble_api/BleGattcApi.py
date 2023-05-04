from ..adapter.BleAdapter import BleAdapter
from ..ble_api.BleApiBase import BleApiBase
from ..ble_api.BleAtt import AttUuid
from ..ble_api.BleCommon import BLE_ERROR
from ..manager.BleManager import BleManager
from ..manager.BleManagerGattcMsgs import BleMgrGattcDiscoverSvcCmd, BleMgrGattcDiscoverSvcRsp, \
    BleMgrGattcDiscoverCharCmd, BleMgrGattcDiscoverCharRsp, BleMgrGattcDiscoverDescCmd, BleMgrGattcDiscoverDescRsp, \
    BleMgrGattcBrowseCmd, BleMgrGattcBrowseRsp, BleMgrGattcReadCmd, BleMgrGattcReadRsp, BleMgrGattcWriteGenericCmd, \
    BleMgrGattcWriteGenericRsp, BleMgrGattcWriteExecuteCmd, BleMgrGattcWriteExecuteRsp


class BleGattcApi(BleApiBase):

    def __init__(self, ble_manager: BleManager, ble_adapter: BleAdapter):
        super().__init__(ble_manager, ble_adapter)

    def browse(self,
               conn_idx: int,
               uuid: AttUuid) -> BLE_ERROR:

        command = BleMgrGattcBrowseCmd(conn_idx, uuid)
        resposne: BleMgrGattcBrowseRsp = self._ble_manager.cmd_execute(command)

        return resposne.status

    def discover_characteristics(self,
                                 conn_idx: int,
                                 start_h: int,
                                 end_h: int,
                                 uuid: AttUuid) -> BLE_ERROR:
        command = BleMgrGattcDiscoverCharCmd(conn_idx, start_h, end_h, uuid)
        response: BleMgrGattcDiscoverCharRsp = self._ble_manager.cmd_execute(command)

        return response.status

    def discover_descriptors(self,
                             conn_idx: int,
                             start_h: int,
                             end_h: int) -> BLE_ERROR:

        command = BleMgrGattcDiscoverDescCmd(conn_idx, start_h, end_h)
        response: BleMgrGattcDiscoverDescRsp = self._ble_manager.cmd_execute(command)

        return response.status

    def discover_services(self, conn_idx: int, uuid: AttUuid):
        command = BleMgrGattcDiscoverSvcCmd(conn_idx, uuid)
        response: BleMgrGattcDiscoverSvcRsp = self._ble_manager.cmd_execute(command)

        return response.status

    def read(self, conn_idx: int, handle: int, offset: int) -> BLE_ERROR:
        command = BleMgrGattcReadCmd(conn_idx, handle, offset)
        response: BleMgrGattcReadRsp = self._ble_manager.cmd_execute(command)

        return response.status

    def write(self, conn_idx: int, handle: int, offset: int, value: bytes) -> BLE_ERROR:
        command = BleMgrGattcWriteGenericCmd(conn_idx=conn_idx, handle=handle, offset=offset, value=value)
        response: BleMgrGattcWriteGenericRsp = self._ble_manager.cmd_execute(command)

        return response.status

    def write_no_resp(self, conn_idx: int, handle: int, signed_write: bool, value: bytes) -> BLE_ERROR:
        command = BleMgrGattcWriteGenericCmd(conn_idx=conn_idx,
                                             handle=handle,
                                             no_response=True,
                                             signed_write=signed_write,
                                             value=value)
        response: BleMgrGattcWriteGenericRsp = self._ble_manager.cmd_execute(command)

        return response.status

    def write_prepare(self, conn_idx: int, handle: int, offset: int, value: bytes) -> BLE_ERROR:
        command = BleMgrGattcWriteGenericCmd(conn_idx=conn_idx,
                                             handle=handle,
                                             prepare=True,
                                             offset=offset,
                                             value=value)
        response: BleMgrGattcWriteGenericRsp = self._ble_manager.cmd_execute(command)

        return response.status

    def write_execute(self, conn_idx: int, commit: bool) -> BLE_ERROR:
        command = BleMgrGattcWriteExecuteCmd(conn_idx, commit)
        response: BleMgrGattcWriteExecuteRsp = self._ble_manager.cmd_execute(command)

        return response.status
