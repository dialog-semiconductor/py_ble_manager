from typing import Callable

from ble_api.BleAtt import ATT_PERM, ATT_ERROR
from ble_api.BleGap import BleEventGapConnected, BleEventGapDisconnected
from ble_api.BleGatt import GATT_SERVICE, GATT_PROP
from ble_api.BleGatts import GATTS_FLAGS, BleEventGattsWriteReq, BleEventGattsPrepareWriteReq, BleEventGattsEventSent, BleEventGattsReadReq
from services.BleService import BleServiceBase, GattService, GattCharacteristic, Descriptor


class CustomBleServiceCallbacks():
    def __init__(self, char1_read_callback: Callable[[], tuple[ATT_ERROR, bytes]] = None) -> None:
        # char1_read_callback is a function that takes no arguments and returns a tuple[ATT_ERROR, bytes]
        self.char1_read_callback = char1_read_callback if char1_read_callback else None


class CustomBleService(BleServiceBase):
    def __init__(self, callbacks: CustomBleServiceCallbacks = None) -> None:
        super().__init__()
        self.callbacks = callbacks if callbacks else CustomBleServiceCallbacks()
        # TODO elegant way to create callback structure? Pass them in on construction?
        # self.callbacks = {"CHAR1_APPLICATION_READ_CB", self.char1_read_callback}

    def init(self):
        self.gatt_service = GattService()
        # TODO this is confusing, simplify it
        self.gatt_service.uuid.uuid = self._uuid_from_str("7c37cbdc-12a2-11ed-861d-0242ac120002")
        self.gatt_service.type = GATT_SERVICE.GATT_SERVICE_PRIMARY

        self.gatt_characteristics = []
        my_char = GattCharacteristic()
        my_char.char.uuid.uuid = self._uuid_from_str("8e716a7e-12a2-11ed-861d-0242ac120002")
        my_char.char.prop = GATT_PROP.GATT_PROP_READ | GATT_PROP.GATT_PROP_WRITE
        my_char.char.perm = ATT_PERM.ATT_PERM_RW
        my_char.char.max_len = 2
        my_char.char.flags = GATTS_FLAGS.GATTS_FLAG_CHAR_READ_REQ
        self.gatt_characteristics.append(my_char)

        my_char = GattCharacteristic()
        my_char.char.uuid.uuid = self._uuid_from_str("3af078b6-12ae-11ed-861d-0242ac120002")
        my_char.char.prop = GATT_PROP.GATT_PROP_READ | GATT_PROP.GATT_PROP_WRITE
        my_char.char.perm = ATT_PERM.ATT_PERM_RW
        my_char.char.max_len = 2
        my_char.char.flags = GATTS_FLAGS.GATTS_FLAG_CHAR_NO_READ_REQ
        self.gatt_characteristics.append(my_char)

        my_char = GattCharacteristic()
        my_char.char.uuid.uuid = self._uuid_from_str("5af078b6-12ae-11ed-861d-0242ac120002")
        my_char.char.prop = GATT_PROP.GATT_PROP_NOTIFY
        my_char.char.perm = ATT_PERM.ATT_PERM_WRITE
        my_char.char.max_len = 2

        desc = Descriptor()
        desc.uuid.uuid = self._uuid_from_str("2901")  # User Description
        desc.perm = ATT_PERM.ATT_PERM_READ
        desc.max_len = 10
        my_char.descriptors.append(desc)

        desc = Descriptor()
        desc.uuid.uuid = self._uuid_from_str("2902")
        desc.perm = ATT_PERM.ATT_PERM_RW
        desc.max_len = 2
        my_char.descriptors.append(desc)

        self.gatt_characteristics.append(my_char)

        self.ccc = 0x0000

        # TODO included services
        self.gatt_service.num_attrs = self._get_num_attr()

    def connected_evt(self, evt: BleEventGapConnected):
        print("CustomBleService connected_evt")

    def disconnected_evt(self, evt: BleEventGapDisconnected):
        print("CustomBleService disconnected_evt")

    def read_req(self, evt: BleEventGattsReadReq):
        status = ATT_ERROR.ATT_ERROR_APPLICATION_ERROR
        data = None
        for item in self.gatt_characteristics:
            if evt.handle == item.char.handle:
                if self.callbacks.char1_read_callback:
                    status, data = self.callbacks.char1_read_callback(self)

        print(f"CustomBleService read_req. evt.handle={evt.handle}. char1.handle={self.gatt_characteristics[0].char.handle}"
              f"char2.handle={self.gatt_characteristics[1].char.handle}")
        return status, data

    def write_req(self, evt: BleEventGattsWriteReq):
        print(f"CustomBleService write_req")
        status = ATT_ERROR.ATT_ERROR_APPLICATION_ERROR
        for item in self.gatt_characteristics:
            if evt.handle == item.char.handle:
                status = ATT_ERROR.ATT_ERROR_OK
                print(f"CustomBleService write_req. Char write handle={evt.handle} value={evt.value}")

            else:
                for desc in item.descriptors:
                    if evt.handle == desc.handle:
                        status = ATT_ERROR.ATT_ERROR_OK
                        print(f"CustomBleService write_req. Desc write handle={evt.handle} value={evt.value}")
                        self.ccc = int.from_bytes(evt.value, "little")

                # TODO update value in CustomBleService?

                # if self.char1_read_callback:
                #    status, data = self.char1_read_callback(self)
        return status

    def prepare_write_req(self, evt: BleEventGattsPrepareWriteReq):
        print("CustomBleService prepare_write_req")

    def event_sent(self, evt: BleEventGattsEventSent):
        print("CustomBleService event_sent")

    def cleanup(self):
        print("CustomBleService cleanup")
