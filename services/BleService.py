from ble_api.BleAtt import att_uuid, ATT_PERM
from ble_api.BleGap import BleEventGapConnected, BleEventGapDisconnected
from ble_api.BleGatt import GATT_SERVICE, GATT_PROP
from ble_api.BleGatts import BleEventGattsReadReq, BleEventGattsWriteReq, BleEventGattsPrepareWriteReq, BleEventGattsEventSent
from manager.BleManagerGatts import GATTS_FLAGS
# TODO service Factory -> pass in num attributes, creates class based on ServiceBase?


class GattService():
    def __init__(self,
                 uuid: att_uuid = None,
                 type: GATT_SERVICE = GATT_SERVICE.GATT_SERVICE_PRIMARY,
                 num_attrs: int = 0) -> None:
        self.uuid = uuid if uuid else att_uuid()
        self.type = type
        self.num_attrs = num_attrs


class Characteristic():
    def __init__(self,
                 uuid: att_uuid = None,
                 prop: GATT_PROP = GATT_PROP.GATT_PROP_NONE,
                 perm: ATT_PERM = ATT_PERM.ATT_PERM_NONE,
                 max_len: int = 0,
                 flags: GATTS_FLAGS = GATTS_FLAGS.GATTS_FLAG_CHAR_NO_READ_REQ,
                 ) -> None:
        self.uuid = uuid if uuid else att_uuid()
        self.prop = prop
        self.perm = perm
        self.max_len = max_len
        self.flags = flags


class Descriptor():
    def __init__(self,
                 uuid: att_uuid = None,
                 perm: ATT_PERM = ATT_PERM.ATT_PERM_NONE,
                 max_len: int = 0,
                 flags: GATTS_FLAGS = GATTS_FLAGS.GATTS_FLAG_CHAR_READ_REQ,
                 ) -> None:
        self.uuid = uuid if uuid else att_uuid()
        self.perm = perm
        self.max_len = max_len
        self.flags = flags


class GattCharacteristic():
    def __init__(self,
                 char: Characteristic = None,
                 descriptor: Descriptor = None,
                 ) -> None:

        self.char = char if char else Characteristic()
        self.descriptor = descriptor if descriptor else Descriptor()


class BleServiceBase():
    def __init__(self) -> None:
        self.start_h = 0  # Service start handle
        self.end_h = 0  # Service end handle

        self.gatt_service = GattService()
        self.gatt_characteristics = [GattCharacteristic()]

    # TODO could hace dictionary with handle pointing to a characteristic Class

    def connected_evt(self, evt: BleEventGapConnected):
        pass

    def disconnected_evt(self, evt: BleEventGapDisconnected):
        pass

    def read_req(self, evt: BleEventGattsReadReq):
        pass

    def write_req(self, evt: BleEventGattsWriteReq):
        pass

    def prepare_write_req(self, evt: BleEventGattsPrepareWriteReq):
        pass

    def event_sent(self, evt: BleEventGattsEventSent):
        pass

    def cleanup(self):
        pass
