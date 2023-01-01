from enum import IntEnum, auto
from .BleAtt import ATT_UUID_TYPE, att_uuid, ATT_ERROR


class GATT_SERVICE(IntEnum):
    GATT_SERVICE_PRIMARY = 0
    GATT_SERVICE_SECONDARY = auto()


class BleGatts():

    def add_service(self, uuid: att_uuid = None, type: GATT_SERVICE = GATT_SERVICE.GATT_SERVICE_PRIMARY, num_attrs: int = 0) -> None:

        pass
