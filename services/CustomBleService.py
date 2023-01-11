from typing import Callable

from ble_api.BleAtt import ATT_PERM, ATT_ERROR
from ble_api.BleCommon import BLE_ERROR
from ble_api.BleGap import BleEventGapConnected, BleEventGapDisconnected
from ble_api.BleGatt import GATT_SERVICE, GATT_PROP, GATT_EVENT
from ble_api.BleGatts import GATTS_FLAGS, BleEventGattsWriteReq, BleEventGattsPrepareWriteReq, BleEventGattsEventSent, BleEventGattsReadReq
from services.BleService import BleServiceBase, GattService, GattCharacteristic, Descriptor
from ble_api.Ble import BlePeripheral

class CustomBleServiceCallbacks():
    def __init__(self, char1_read_callback: Callable[[BlePeripheral, int], tuple[ATT_ERROR, bytes]] = None) -> None:
        # char1_read_callback is a function that takes a BlePeripheral, int  and returns a tuple[ATT_ERROR, bytes]
        self.char1_read_callback = char1_read_callback if char1_read_callback else None


class CustomBleService(BleServiceBase):
    def __init__(self, callbacks: CustomBleServiceCallbacks = None) -> None:
        super().__init__()
        self.callbacks = callbacks if callbacks else CustomBleServiceCallbacks()

        self.char_1_value_h = 0
        self.char_2_value_h = 0
        self.char_3_value_h = 0
        self.char_3_user_desc_h = 0
        self.char_3_ccc_h = 0
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

        # TODO getting a GattcReadReqInd for this descriptor?
        desc = Descriptor()
        desc.uuid.uuid = self._uuid_from_str("2902")
        desc.perm = ATT_PERM.ATT_PERM_RW
        desc.max_len = 2
        my_char.descriptors.append(desc)

        self.gatt_characteristics.append(my_char)

        self.ccc = 0x0000

        # TODO included services
        self.gatt_service.num_attrs = self._get_num_attr()

        self.periph: BlePeripheral = None

    def connected_evt(self, evt: BleEventGapConnected):
        print("CustomBleService connected_evt")

    def disconnected_evt(self, evt: BleEventGapDisconnected):
        print("CustomBleService disconnected_evt")

    async def read_req(self, evt: BleEventGattsReadReq):
        for item in self.gatt_characteristics:  # TODO should nto have to loop every handle to get the one you want
            if evt.handle == item.char.handle:
                if self.callbacks.char1_read_callback:
                    await self.callbacks.char1_read_callback(self, evt.conn_idx)

            else:
                desc: Descriptor
                for desc in item.descriptors:
                    if evt.handle == desc.handle:
                        status = ATT_ERROR.ATT_ERROR_OK
                        data = int.to_bytes(0, length=2, byteorder='little')
                        # TODO get ccc from storage
                        await self.periph.send_read_cfm(evt.conn_idx, evt.handle, status, data)
                       
    def write_req(self, evt: BleEventGattsWriteReq):
        print("CustomBleService write_req")
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

                # TODO To update value in databse, need to call Ble.set_value. Rethink how to achieve
        return status

    def prepare_write_req(self, evt: BleEventGattsPrepareWriteReq):
        print("CustomBleService prepare_write_req")

    def event_sent(self, evt: BleEventGattsEventSent):
        print("CustomBleService event_sent")

    def cleanup(self):
        print("CustomBleService cleanup")

    async def send_char1_read_cfm(self,
                                  conn_idx: int = 0,
                                  status: ATT_ERROR = ATT_ERROR.ATT_ERROR_OK,
                                  value: bytes = None
                                  ) -> BLE_ERROR:

        return await self.periph.send_read_cfm(conn_idx,
                                               self.gatt_characteristics[0].char.handle,
                                               status,
                                               value)

    async def set_char2_value(self,
                              value: bytes
                              ) -> BLE_ERROR:

        return await self.periph.set_value(self.char_2_value_h, value)

    async def set_char3_user_desc_value(self,
                                        value: bytes
                                        ) -> BLE_ERROR:

        return await self.periph.set_value(self.char_3_user_desc_h, value)

    async def notify_char3(self,
                           conn_idx: int = 0,
                           value: bytes = None) -> BLE_ERROR:

        return await self.periph.send_event(conn_idx,
                                            self.char_3_value_h,
                                            GATT_EVENT.GATT_EVENT_NOTIFICATION,
                                            value)
