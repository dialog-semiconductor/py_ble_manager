import asyncio

from adapter.BleAdapter import BleAdapter
from ble_api.BleDeviceBase import BleDeviceBase
from ble_api.BleAtt import ATT_ERROR
from ble_api.BleCommon import BleEventBase, BLE_ERROR
from ble_api.BleGap import BLE_GAP_ROLE, BLE_GAP_CONN_MODE, BLE_EVT_GAP, BleEventGapConnected, BleEventGapDisconnected
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

    async def connect(self) -> None:
        pass

