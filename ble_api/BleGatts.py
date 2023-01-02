from enum import IntEnum
from .BleAtt import att_uuid, ATT_PERM  # ATT_ERROR, ATT_UUID_TYPE
from .BleGatt import GATT_SERVICE, GATT_PROP
from manager.BleManagerGatts import BleMgrGattsServiceAddCmd, BleMgrGattsServiceAddRsp, \
    BleMgrGattsServiceAddCharacteristicCmd, BleMgrGattsServiceAddCharacteristicRsp, \
    BleMgrGattsServiceAddDescriptorCmd, BleMgrGattsServiceAddDescriptorRsp, \
    BleMgrGattsServiceRegisterCmd, BleMgrGattsServiceRegisterRsp
from manager.BleManager import BLE_ERROR  # BleManager
# from adapter.BleAdapter import BleAdapter
from .Ble import BleApiBase


# GATT Server flags
class GATTS_FLAGS(IntEnum):
    GATTS_FLAG_CHAR_NO_READ_REQ = 0x00  # TODO need better name
    GATTS_FLAG_CHAR_READ_REQ = 0x01        # enable ::BLE_EVT_GATTS_READ_REQ for attribute


class BleGatts(BleApiBase):

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
        return response, response.h_offset, response.h_val_offset

    async def add_descriptor(self,
                             uuid: att_uuid = att_uuid(),
                             prop: GATT_PROP = GATT_PROP.GATT_PROP_NONE,
                             perm: ATT_PERM = ATT_PERM.ATT_PERM_NONE,
                             max_len: int = 0,
                             flags: GATTS_FLAGS = GATTS_FLAGS.GATTS_FLAG_CHAR_READ_REQ,
                             h_offset: int = 0,
                             h_val_offset: int = 0
                             ) -> tuple[BLE_ERROR, int]:

        response = BLE_ERROR.BLE_ERROR_FAILED

        command = BleMgrGattsServiceAddDescriptorCmd(uuid, perm, max_len, flags)

        response: BleMgrGattsServiceAddDescriptorRsp = await self.ble_manager.cmd_execute(command)

        return response.status, response.h_offset

    async def add_service(self,
                          uuid: att_uuid = att_uuid(),
                          type: GATT_SERVICE = GATT_SERVICE.GATT_SERVICE_PRIMARY,
                          num_attrs: int = 0
                          ) -> BLE_ERROR:

        response = BLE_ERROR.BLE_ERROR_FAILED

        command = BleMgrGattsServiceAddCmd(uuid, type, num_attrs)

        response: BleMgrGattsServiceAddRsp = await self.ble_manager.cmd_execute(command)

        return response.status

    def get_num_attr(num_included_svcs: int = 0, num_chars: int = 0, num_descriptors: int = 0) -> int:
        return (1 * num_included_svcs) + (2 * num_chars) + (1 * num_descriptors)

    async def register_service(self) -> tuple[BLE_ERROR, list]:

        response = BLE_ERROR.BLE_ERROR_FAILED

        command = BleMgrGattsServiceRegisterCmd()

        response: BleMgrGattsServiceRegisterRsp = await self.ble_manager.cmd_execute(command)

        return response.status
