from enum import IntEnum
from .BleAtt import att_uuid, ATT_PERM  # ATT_ERROR, ATT_UUID_TYPE
from .BleGatt import GATT_SERVICE, GATT_PROP
from manager.BleManagerGatts import BleMgrGattsServiceAddCmd, BleMgrGattsServiceAddCharacteristicCmd
from manager.BleManager import BLE_ERROR  # BleManager
# from adapter.BleAdapter import BleAdapter
from .Ble import BleApiBase


# TODO this seems unnecessary
# GATT Server flags
class GATTS_FLAGS(IntEnum):
    GATTS_FLAG_CHAR_READ_REQ = 0x01        # enable ::BLE_EVT_GATTS_READ_REQ for attribute


class BleGatts(BleApiBase):

    async def add_characteristic(self,
                                 uuid: att_uuid = att_uuid(),
                                 prop: GATT_PROP = GATT_PROP.GATT_PROP_NONE,
                                 perm: ATT_PERM = ATT_PERM.ATT_PERM_NONE,
                                 max_len: int = 0,
                                 flags: GATTS_FLAGS = GATTS_FLAGS.GATTS_FLAG_CHAR_READ_REQ,
                                 h_offset: int = 0,
                                 h_val_offset: int = 0
                                 ) -> BLE_ERROR:

        response = BLE_ERROR.BLE_ERROR_FAILED

        command = BleMgrGattsServiceAddCharacteristicCmd()
        command.uuid = uuid
        command.prop = prop
        command.perm = perm
        command.max_len = max_len
        command.flags = flags
        command.perm = perm
        command.perm = perm

        response = await self.ble_manager.cmd_execute(command)

        # TODO need get h_offset and h_val_offset from resposne

        return response

    async def add_service(self,
                          uuid: att_uuid = att_uuid(),
                          type: GATT_SERVICE = GATT_SERVICE.GATT_SERVICE_PRIMARY,
                          num_attrs: int = 0
                          ) -> BLE_ERROR:

        response = BLE_ERROR.BLE_ERROR_FAILED

        command = BleMgrGattsServiceAddCmd()
        command.uuid = uuid
        command.type = type
        command.num_attrs = num_attrs

        response = await self.ble_manager.cmd_execute(command)

        return response

    def get_num_attr(num_svcs: int = 0, num_chars: int = 0, num_descriptors: int = 0) -> int:
        return (1 * num_svcs) + (2 * num_chars) + (1 * num_descriptors)
