from typing import Callable

from ble_api.BleAtt import ATT_PERM, ATT_ERROR
from ble_api.BleCommon import BLE_ERROR
from ble_api.BleGap import BleEventGapConnected, BleEventGapDisconnected
from ble_api.BleGatt import GATT_SERVICE, GATT_PROP, GATT_EVENT
from ble_api.BleGatts import GATTS_FLAGS, BleEventGattsWriteReq, BleEventGattsPrepareWriteReq, BleEventGattsEventSent, BleEventGattsReadReq
from services.BleService import BleServiceBase, GattServiceDef, GattCharacteristicDef, DescriptorDef, AttributeHandle
from ble_api.BlePeripheral import BlePeripheral


class CustomBleService(BleServiceBase):
    # TODO this is to satisfy typing in CustomBleServiceCallbacks
    pass


class CustomBleServiceCallbacks():
    def __init__(self,
                 char1_read: Callable[[CustomBleService, int], None] = None,
                 char1_write: Callable[[CustomBleService, int, int], None] = None,
                 char2_write: Callable[[CustomBleService, int, int], None] = None,
                 char3_notif_changed: Callable[[CustomBleService, int, int], None] = None
                 ) -> None:
        # char1_read is a function that takes a CustomBleService, int  and returns nothing
        self.char1_read = char1_read
        self.char1_write = char1_write
        self.char2_write = char2_write
        self.char3_notif_changed = char3_notif_changed


class CustomBleService(BleServiceBase):
    def __init__(self, callbacks: CustomBleServiceCallbacks = None) -> None:
        super().__init__()
        self.callbacks = callbacks if callbacks else CustomBleServiceCallbacks()

        self.char_1_value_h = AttributeHandle()
        self.char_2_value_h = AttributeHandle()
        self.char_3_value_h = AttributeHandle()
        self.char_3_user_desc_h = AttributeHandle()
        self.char_3_ccc_h = AttributeHandle()

        self.periph: BlePeripheral = None

        self.ccc = 0x0000  # TODO This should be removed

    def init(self):

        # TODO this is confusing, simplify it
        self.service_defs.uuid.uuid = self._uuid_from_str("7c37cbdc-12a2-11ed-861d-0242ac120002")
        self.service_defs.type = GATT_SERVICE.GATT_SERVICE_PRIMARY

        self.char_defs = []
        char = GattCharacteristicDef()
        char.char_def.uuid.uuid = self._uuid_from_str("8e716a7e-12a2-11ed-861d-0242ac120002")
        char.char_def.prop = GATT_PROP.GATT_PROP_READ | GATT_PROP.GATT_PROP_WRITE
        char.char_def.perm = ATT_PERM.ATT_PERM_RW
        char.char_def.max_len = 2
        char.char_def.flags = GATTS_FLAGS.GATTS_FLAG_CHAR_READ_REQ
        char.char_def.handle = self.char_1_value_h  # self.char_1_value_h will be automatically updated by BlePeripheral when service registered
        self.gatt_char_defs.append(char)

        char = GattCharacteristicDef()
        char.char_def.uuid.uuid = self._uuid_from_str("3af078b6-12ae-11ed-861d-0242ac120002")
        char.char_def.prop = GATT_PROP.GATT_PROP_READ | GATT_PROP.GATT_PROP_WRITE 
        char.char_def.perm = ATT_PERM.ATT_PERM_RW
        char.char_def.max_len = 2
        char.char_def.flags = GATTS_FLAGS.GATTS_FLAG_CHAR_NO_READ_REQ
        char.char_def.handle = self.char_2_value_h
        self.gatt_char_defs.append(char)

        char = GattCharacteristicDef()
        char.char_def.uuid.uuid = self._uuid_from_str("5af078b6-12ae-11ed-861d-0242ac120002")
        char.char_def.prop = GATT_PROP.GATT_PROP_NOTIFY
        char.char_def.perm = ATT_PERM.ATT_PERM_WRITE
        char.char_def.max_len = 2
        char.char_def.handle = self.char_3_value_h

        desc = DescriptorDef()
        desc.uuid.uuid = self._uuid_from_str("2901")  # User Description
        desc.perm = ATT_PERM.ATT_PERM_READ
        desc.max_len = 10
        desc.handle = self.char_3_user_desc_h
        char.desc_defs.append(desc)

        # TODO getting a GattcReadReqInd for this descriptor?
        desc = DescriptorDef()
        desc.uuid.uuid = self._uuid_from_str("2902")
        desc.perm = ATT_PERM.ATT_PERM_RW
        desc.max_len = 2
        desc.handle = self.char_3_ccc_h
        char.desc_defs.append(desc)

        self.gatt_char_defs.append(char)

        # TODO included services
        self.service_defs.num_attrs = self._get_num_attr()

    def connected_evt(self, evt: BleEventGapConnected):
        print("CustomBleService connected_evt")

    def disconnected_evt(self, evt: BleEventGapDisconnected):
        print("CustomBleService disconnected_evt")

    async def read_req(self, evt: BleEventGattsReadReq):
        print("CustomBleService read_req")

        if evt.handle == self.char_1_value_h.value:
            if self.callbacks.char1_read:
                await self.callbacks.char1_read(self, evt.conn_idx)

        elif evt.handle == self.char_3_ccc_h.value:
            status = ATT_ERROR.ATT_ERROR_OK

            # TODO ignoring error for now
            error, value = self.periph.storage_get_int(evt.conn_idx, self.char_3_ccc_h.value)
            if error != BLE_ERROR.BLE_STATUS_OK:
                value = 0
            await self.periph.read_cfm(evt.conn_idx, evt.handle, status, value)

        else:
            await self.periph.read_cfm(evt.conn_idx, evt.handle, ATT_ERROR.ATT_ERROR_READ_NOT_PERMITTED, 0)

    async def write_req(self, evt: BleEventGattsWriteReq):
        print("CustomBleService write_req")

        if evt.handle == self.char_1_value_h.value:
            # TODO any validation on input
            if self.callbacks and self.callbacks.char1_write:
                await self.callbacks.char1_write(self, evt.conn_idx, int.from_bytes(evt.value, "little"))

        elif evt.handle == self.char_2_value_h.value:
            # TODO any validation on input
            if self.callbacks and self.callbacks.char2_write:
                await self.callbacks.char2_write(self, evt.conn_idx, int.from_bytes(evt.value, "little"))

        elif evt.handle == self.char_3_ccc_h.value:
            ccc = int.from_bytes(evt.value, "little")
            self.ccc = ccc  # TODO this should be removed
            self.periph.storage_put_int(evt.conn_idx, self.char_3_ccc_h.value, ccc, True)  # TODO this is not truly persistent right now. Is persistent btw connections? Or power cycles?

            if self.callbacks and self.callbacks.char3_notif_changed:
                self.callbacks.char3_notif_changed(self, evt.conn_idx, ccc)
            # TODO notification status change callback
            print(f"CustomerService write_req. Setting ccc={evt.value}")
            await self.periph.write_cfm(evt.conn_idx, evt.handle, ATT_ERROR.ATT_ERROR_OK)

        else:
            await self.periph.write_cfm(evt.conn_idx, evt.handle, ATT_ERROR.ATT_ERROR_WRITE_NOT_PERMITTED)

    async def prepare_write_req(self, evt: BleEventGattsPrepareWriteReq):
        if evt.handle == self.char_2_value_h.value:
            await self.periph.prepare_write_cfm(evt.conn_idx, evt.handle, 2, ATT_ERROR.ATT_ERROR_OK)
        else:
            await self.periph.prepare_write_cfm(evt.conn_idx, evt.handle, 0, ATT_ERROR.ATT_ERROR_REQUEST_NOT_SUPPORTED)

    def event_sent(self, evt: BleEventGattsEventSent):
        print("CustomBleService event_sent")

    def cleanup(self):
        print("CustomBleService cleanup")

    async def send_char1_read_cfm(self,
                                  conn_idx: int = 0,
                                  status: ATT_ERROR = ATT_ERROR.ATT_ERROR_OK,
                                  value: bytes = None
                                  ) -> BLE_ERROR:

        return await self.periph.read_cfm(conn_idx,
                                          self.char_1_value_h.value,
                                          status,
                                          value)

    async def send_char1_write_cfm(self,
                                   conn_idx: int = 0,
                                   status: ATT_ERROR = ATT_ERROR.ATT_ERROR_OK
                                   ) -> BLE_ERROR:

        return await self.periph.write_cfm(conn_idx, self.char_1_value_h.value, status)

    async def send_char2_write_cfm(self,
                                   conn_idx: int = 0,
                                   status: ATT_ERROR = ATT_ERROR.ATT_ERROR_OK
                                   ) -> BLE_ERROR:

        return await self.periph.write_cfm(conn_idx, self.char_2_value_h.value, status)

    async def set_char2_value(self,
                              value: bytes
                              ) -> BLE_ERROR:

        return await self.periph.set_value(self.char_2_value_h.value, value)

    async def set_char3_user_desc_value(self,
                                        value: bytes
                                        ) -> BLE_ERROR:

        return await self.periph.set_value(self.char_3_user_desc_h.value, value)

    async def notify_char3(self,
                           conn_idx: int = 0,
                           value: bytes = None
                           ) -> BLE_ERROR:

        return await self.periph.send_event(conn_idx,
                                            self.char_3_value_h.value,
                                            GATT_EVENT.GATT_EVENT_NOTIFICATION,
                                            value)
