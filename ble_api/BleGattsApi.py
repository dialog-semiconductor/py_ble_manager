from adapter.BleAdapter import BleAdapter
from ble_api.BleApiBase import BleApiBase
from ble_api.BleAtt import att_uuid, ATT_PERM, ATT_ERROR
from ble_api.BleCommon import BLE_ERROR
from ble_api.BleGatt import GATT_SERVICE, GATT_PROP
from ble_api.BleGatts import GATTS_FLAGS
from manager.BleManager import BleManager
from manager.BleManagerGattsMsgs import BleMgrGattsServiceAddCmd, BleMgrGattsServiceAddRsp, \
    BleMgrGattsServiceAddCharacteristicCmd, BleMgrGattsServiceAddCharacteristicRsp, \
    BleMgrGattsServiceAddDescriptorCmd, BleMgrGattsServiceAddDescriptorRsp, \
    BleMgrGattsServiceRegisterCmd, BleMgrGattsServiceRegisterRsp, BleMgrGattsReadCfmCmd, BleMgrGattsReadCfmRsp, \
    BleMgrGattsSetValueCmd, BleMgrGattsSetValueRsp
from services.BleService import BleServiceBase


class BleGattsApi(BleApiBase):

    def __init__(self, ble_manager: BleManager, ble_adapter: BleAdapter):
        super().__init__(ble_manager, ble_adapter)

    async def add_characteristic(self,
                                 uuid: att_uuid = att_uuid(),
                                 prop: GATT_PROP = GATT_PROP.GATT_PROP_NONE,
                                 perm: ATT_PERM = ATT_PERM.ATT_PERM_NONE,
                                 max_len: int = 0,
                                 flags: GATTS_FLAGS = GATTS_FLAGS.GATTS_FLAG_CHAR_READ_REQ,
                                 ) -> tuple[BLE_ERROR, int, int]:

        response = BLE_ERROR.BLE_ERROR_FAILED
        command = BleMgrGattsServiceAddCharacteristicCmd(uuid, prop, perm, max_len, flags)
        response: BleMgrGattsServiceAddCharacteristicRsp = await self.ble_manager.cmd_execute(command)

        # TODO just return response instead?
        return response.status, response.h_offset, response.h_val_offset

    async def add_descriptor(self,
                             uuid: att_uuid = att_uuid(),
                             prop: GATT_PROP = GATT_PROP.GATT_PROP_NONE,
                             perm: ATT_PERM = ATT_PERM.ATT_PERM_NONE,
                             max_len: int = 0,
                             flags: GATTS_FLAGS = GATTS_FLAGS.GATTS_FLAG_CHAR_READ_REQ,
                             ) -> tuple[BLE_ERROR, int]:

        response = BLE_ERROR.BLE_ERROR_FAILED

        command = BleMgrGattsServiceAddDescriptorCmd(uuid, prop, perm, max_len, flags)

        response: BleMgrGattsServiceAddDescriptorRsp = await self.ble_manager.cmd_execute(command)

        return response.status, response.h_offset

    async def add_service(self,
                          uuid: att_uuid = None,
                          type: GATT_SERVICE = GATT_SERVICE.GATT_SERVICE_PRIMARY,
                          num_attrs: int = 0
                          ) -> BLE_ERROR:

        response = BLE_ERROR.BLE_ERROR_FAILED

        command = BleMgrGattsServiceAddCmd(uuid, type, num_attrs)

        response: BleMgrGattsServiceAddRsp = await self.ble_manager.cmd_execute(command)

        return response.status

    async def register_service(self, svc: BleServiceBase) -> BLE_ERROR:

        response = BLE_ERROR.BLE_ERROR_FAILED

        command = BleMgrGattsServiceRegisterCmd()

        response: BleMgrGattsServiceRegisterRsp = await self.ble_manager.cmd_execute(command)

        if svc:
            svc.start_h = response.handle
            for char in svc.gatt_characteristics:
                char.char.handle += response.handle
                print(f"Register Service. char={char}, handle={char.char.handle}. response.handle={response.handle}")
                for desc in char.descriptors:
                    desc.handle += response.handle

            svc.end_h = svc.start_h + svc.gatt_service.num_attrs

        return response.status, svc

    async def send_read_cfm(self,
                            conn_idx: int = 0,
                            handle: int = 0,
                            status: ATT_ERROR = ATT_ERROR.ATT_ERROR_OK,
                            value: list[int] = None):

        response = BLE_ERROR.BLE_ERROR_FAILED
        command = BleMgrGattsReadCfmCmd(conn_idx, handle, status, value)
        response: BleMgrGattsReadCfmRsp = await self.ble_manager.cmd_execute(command)

        return response.status

    async def set_value(self,
                        handle: int = 0,
                        value: bytes = None):

        response = BLE_ERROR.BLE_ERROR_FAILED
        command = BleMgrGattsSetValueCmd(handle, value)
        response: BleMgrGattsSetValueRsp = await self.ble_manager.cmd_execute(command)

        return response.status
