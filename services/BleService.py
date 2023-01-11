from ble_api.BleAtt import att_uuid, ATT_PERM, ATT_ERROR
from ble_api.BleGap import BleEventGapConnected, BleEventGapDisconnected
from ble_api.BleGatt import GATT_SERVICE, GATT_PROP
from ble_api.BleGatts import GATTS_FLAGS, BleEventGattsReadReq, BleEventGattsEventSent, BleEventGattsPrepareWriteReq
from ble_api.BleCommon import BleEventBase
from ble_api.BleApiBase import BlePeripheral


class AttributeHandle():
    def __init__(self):
        self.handle = 0

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

        self._gatt_service = GattService()
        self.included_services: list[BleServiceBase] = []
        # TODO included services
        self.gatt_characteristics: list[GattCharacteristic] = []

        self.periph: BlePeripheral = None

    # TODO num_attr should be a property. Should auto calculate num attr
    def _get_num_attr(self) -> int:
        num_descriptors = 0
        for char in self.gatt_characteristics:
            num_descriptors += len(char.descriptors)
        return (1 * len(self.included_services)) + (2 * len(self.gatt_characteristics)) + (1 * num_descriptors)

    
     # TODO num_attr should be a property. Should auto calculate num attr
    #def _get_gatt_service(self):
    #    num_descriptors = 0
    #    for char in self.gatt_characteristics:
    #        num_descriptors += len(char.descriptors)
    #    self._gatt_service.num_attrs = (1 * len(self.included_services)) + (2 * len(self.gatt_characteristics)) + (1 * num_descriptors)
    #    return self._gatt_service

    #def _set_gatt_service(self, svc: GattService):
    #    self._gatt_service = svc

    # gatt_service = property(_get_gatt_service)
    
    

    def _uuid_from_str(self, uuid_str: str) -> bytes:
        uuid_str = uuid_str.replace("-", "")
        uuid_list = [int(uuid_str[idx:idx + 2], 16) for idx in range(0, len(uuid_str), 2)]
        uuid_list.reverse()  # mcu is little endian
        return bytes(uuid_list)

    def connected_evt(self, evt: BleEventGapConnected) -> None:
        pass

    def cleanup(self) -> None:
        pass

    def event_sent(self, evt: BleEventGattsEventSent) -> None:
        pass

    def disconnected_evt(self, evt: BleEventGapDisconnected) -> None:
        pass

    def prepare_write_req(self, evt: BleEventGattsPrepareWriteReq) -> None:
        pass

    def read_req(self, svc: BlePeripheral, evt: BleEventGattsReadReq) -> tuple[ATT_ERROR, bytes]:
        # Service implementations should return a status indicating any error, and the data to be read in bytes
        pass

    def write_req(self, evt: BleEventBase) -> ATT_ERROR:  # BleEventGattsWriteReq
        pass
 
