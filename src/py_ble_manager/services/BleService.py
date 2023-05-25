from ..ble_api.BleAtt import AttUuid, ATT_PERM
from ..ble_api.BleGap import BleEventGapConnected, BleEventGapDisconnected
from ..ble_api.BleGatt import GATT_SERVICE, GATT_PROP
from ..ble_api.BleGatts import GATTS_FLAG, BleEventGattsReadReq, BleEventGattsEventSent, BleEventGattsPrepareWriteReq, BleEventGattsWriteReq


class AttributeHandle():
    def __init__(self):
        self.value = 0


class GattServiceDef():
    def __init__(self,
                 uuid: AttUuid = None,
                 type: GATT_SERVICE = GATT_SERVICE.GATT_SERVICE_PRIMARY,
                 num_attrs: int = 0) -> None:
        self.uuid = uuid if uuid else AttUuid()
        self.type = type
        self.num_attrs = num_attrs


class CharacteristicDef():
    def __init__(self,
                 uuid: AttUuid = None,
                 prop: GATT_PROP = GATT_PROP.GATT_PROP_NONE,
                 perm: ATT_PERM = ATT_PERM.ATT_PERM_NONE,
                 max_len: int = 0,
                 flags: GATTS_FLAG = GATTS_FLAG.GATTS_FLAG_CHAR_NO_READ_REQ,
                 handle: AttributeHandle = None
                 ) -> None:
        self.uuid = uuid if uuid else AttUuid()
        self.prop = prop
        self.perm = perm
        self.max_len = max_len
        self.flags = flags
        self.handle = handle


class DescriptorDef():
    def __init__(self,
                 uuid: AttUuid = None,
                 perm: ATT_PERM = ATT_PERM.ATT_PERM_NONE,
                 max_len: int = 0,
                 flags: GATTS_FLAG = GATTS_FLAG.GATTS_FLAG_CHAR_READ_REQ,
                 handle: AttributeHandle = None
                 ) -> None:
        self.uuid = uuid if uuid else AttUuid()
        self.perm = perm
        self.max_len = max_len
        self.flags = flags
        self.handle = handle


class GattCharacteristicDef():
    def __init__(self,
                 char_def: CharacteristicDef = None,
                 descriptor_defs: list[DescriptorDef] = None,
                 ) -> None:

        self.char_def = char_def if char_def else CharacteristicDef()
        self.desc_defs: list[DescriptorDef] = descriptor_defs if descriptor_defs else []


class BleServiceBase():
    def __init__(self) -> None:
        self.start_h = 0  # Service start handle
        self.end_h = 0  # Service end handle

        self.callbacks = {}

        self.service_defs = GattServiceDef()
        self.incl_svc_defs: list[BleServiceBase] = []
        self.gatt_char_defs: list[GattCharacteristicDef] = []

    def _get_num_attr(self) -> int:
        num_descriptors = 0
        for char in self.gatt_char_defs:
            num_descriptors += len(char.desc_defs)
        return (1 * len(self.incl_svc_defs)) + (2 * len(self.gatt_char_defs)) + (1 * num_descriptors)

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

    def read_req(self, evt: BleEventGattsReadReq) -> None:
        pass

    def write_req(self, evt: BleEventGattsWriteReq) -> None:
        pass

    def register_peripheral(self, periph):  # BlePeripheral not type hinted as it creates import issue.
        self._periph = periph
