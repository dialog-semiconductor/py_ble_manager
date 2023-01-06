from ble_api.BleAtt import att_uuid, ATT_PERM, ATT_ERROR
from ble_api.BleGap import BleEventGapConnected, BleEventGapDisconnected
from ble_api.BleGatt import GATT_SERVICE, GATT_PROP
from ble_api.BleGatts import GATTS_FLAGS
from ble_api.BleCommon import BleEventBase
from manager.BleManagerGatts import BleEventGattsReadReq


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
        self.handle = 0


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
        self.handle = 0


#  TODO Subclasses with predefined perms, descriptors (e.g. notifiable with CCCD, or char with user desc)
class GattCharacteristic():
    def __init__(self,
                 char: Characteristic = None,
                 descriptor: list[Descriptor] = None,
                 ) -> None:

        self.char = char if char else Characteristic()  # TODO change to attribute or value??
        self.descriptors: list[Descriptor] = descriptor if descriptor else []


class BleServiceCallbacks():
    def __init__(self) -> None:
        pass


class BleServiceBase():
    def __init__(self) -> None:
        self.start_h = 0  # Service start handle
        self.end_h = 0  # Service end handle

        self.callbacks = {}

        self.gatt_service = GattService()
        # TODO included services
        self.gatt_characteristics: list[GattCharacteristic] = []

    # TODO num_attr should be a property. Should auto calculate num attr
    def _get_num_attr(self, num_included_svcs: int = 0, num_chars: int = 0, num_descriptors: int = 0) -> int:
        return (1 * num_included_svcs) + (2 * num_chars) + (1 * num_descriptors)

    def connected_evt(self, evt: BleEventGapConnected) -> None:
        pass

    def cleanup(self) -> None:
        pass

    def event_sent(self, evt: BleEventBase) -> None:  # TODO BleEventGattsEventSent
        pass

    def disconnected_evt(self, evt: BleEventGapDisconnected) -> None:
        pass

    def prepare_write_req(self, evt: BleEventBase) -> None:  # BleEventGattsPrepareWriteReq
        pass

    def read_req(self, evt: BleEventGattsReadReq) -> tuple[ATT_ERROR, bytes]:
        # Service implementations should return a status indicating any error, and the data to be read in bytes
        pass

    def write_req(self, evt: BleEventBase) -> ATT_ERROR:  # BleEventGattsWriteReq
        pass
