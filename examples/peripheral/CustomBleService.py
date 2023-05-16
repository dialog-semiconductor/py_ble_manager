from typing import Callable

import python_gtl_thread as ble


class CustomBleService(ble.BleServiceBase):
    # Predefine to satisfy typing in CustomBleServiceCallbacks
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


class CustomBleService(ble.BleServiceBase):
    def __init__(self, callbacks: CustomBleServiceCallbacks = None) -> None:
        super().__init__()
        self.callbacks = callbacks if callbacks else CustomBleServiceCallbacks()

        self.char_1_value_h = ble.AttributeHandle()
        self.char_2_value_h = ble.AttributeHandle()
        self.char_3_value_h = ble.AttributeHandle()
        self.char_3_user_desc_h = ble.AttributeHandle()
        self.char_3_ccc_h = ble.AttributeHandle()

        self.periph: ble.BlePeripheral = None

        self.ccc = 0x0000  # TODO This should be removed

    def init(self):

        # TODO this is confusing, simplify it
        self.service_defs.uuid.uuid = self._uuid_from_str("7c37cbdc-12a2-11ed-861d-0242ac120002")
        self.service_defs.type = ble.GATT_SERVICE.GATT_SERVICE_PRIMARY

        self.char_defs = []
        char = ble.GattCharacteristicDef()
        char.char_def.uuid.uuid = self._uuid_from_str("8e716a7e-12a2-11ed-861d-0242ac120002")
        char.char_def.prop = ble.GATT_PROP.GATT_PROP_READ | ble.GATT_PROP.GATT_PROP_WRITE
        char.char_def.perm = ble.ATT_PERM.ATT_PERM_RW
        char.char_def.max_len = 2
        char.char_def.flags = ble.GATTS_FLAG.GATTS_FLAG_CHAR_READ_REQ
        char.char_def.handle = self.char_1_value_h  # self.char_1_value_h will be automatically updated by ble.BlePeripheral when service registered
        self.gatt_char_defs.append(char)

        char = ble.GattCharacteristicDef()
        char.char_def.uuid.uuid = self._uuid_from_str("3af078b6-12ae-11ed-861d-0242ac120002")
        char.char_def.prop = ble.GATT_PROP.GATT_PROP_READ | ble.GATT_PROP.GATT_PROP_WRITE 
        char.char_def.perm = ble.ATT_PERM.ATT_PERM_RW
        char.char_def.max_len = 2
        char.char_def.flags = ble.GATTS_FLAG.GATTS_FLAG_CHAR_NO_READ_REQ
        char.char_def.handle = self.char_2_value_h
        self.gatt_char_defs.append(char)

        char = ble.GattCharacteristicDef()
        char.char_def.uuid.uuid = self._uuid_from_str("5af078b6-12ae-11ed-861d-0242ac120002")
        char.char_def.prop = ble.GATT_PROP.GATT_PROP_NOTIFY
        char.char_def.perm = ble.ATT_PERM.ATT_PERM_WRITE
        char.char_def.max_len = 2
        char.char_def.handle = self.char_3_value_h

        desc = ble.DescriptorDef()
        desc.uuid.uuid = self._uuid_from_str("2901")  # User Description
        desc.perm = ble.ATT_PERM.ATT_PERM_READ
        desc.max_len = 10
        desc.handle = self.char_3_user_desc_h
        char.desc_defs.append(desc)

        # TODO getting a GattcReadReqInd for this descriptor?
        desc = ble.DescriptorDef()
        desc.uuid.uuid = self._uuid_from_str("2902")
        desc.perm = ble.ATT_PERM.ATT_PERM_RW
        desc.max_len = 2
        desc.handle = self.char_3_ccc_h
        char.desc_defs.append(desc)

        self.gatt_char_defs.append(char)

        # TODO included services
        self.service_defs.num_attrs = self._get_num_attr()

    def connected_evt(self, evt: ble.BleEventGapConnected):
        print("CustomBleService connected_evt")

    def disconnected_evt(self, evt: ble.BleEventGapDisconnected):
        print("CustomBleService disconnected_evt")

    def read_req(self, evt: ble.BleEventGattsReadReq):
        print("CustomBleService read_req")

        if evt.handle == self.char_1_value_h.value:
            if self.callbacks.char1_read:
                self.callbacks.char1_read(self, evt.conn_idx)

        elif evt.handle == self.char_3_ccc_h.value:
            status = ble.ATT_ERROR.ATT_ERROR_OK

            # TODO ignoring error for now
            error, value = self.periph.storage_get_int(evt.conn_idx, self.char_3_ccc_h.value)
            if error != ble.BLE_ERROR.BLE_STATUS_OK:
                value = 0
            self.periph.read_cfm(evt.conn_idx, evt.handle, status, value)

        else:
            self.periph.read_cfm(evt.conn_idx, evt.handle, ble.ATT_ERROR.ATT_ERROR_READ_NOT_PERMITTED, 0)

    def write_req(self, evt: ble.BleEventGattsWriteReq):
        print("CustomBleService write_req")

        if evt.handle == self.char_1_value_h.value:
            # TODO any validation on input
            if self.callbacks and self.callbacks.char1_write:
                self.callbacks.char1_write(self, evt.conn_idx, int.from_bytes(evt.value, "little"))

        elif evt.handle == self.char_2_value_h.value:
            # TODO any validation on input
            if self.callbacks and self.callbacks.char2_write:
                self.callbacks.char2_write(self, evt.conn_idx, int.from_bytes(evt.value, "little"))

        elif evt.handle == self.char_3_ccc_h.value:
            ccc = int.from_bytes(evt.value, "little")
            self.ccc = ccc  # TODO this should be removed
            self.periph.storage_put_int(evt.conn_idx, self.char_3_ccc_h.value, ccc, True)  # TODO this is not truly persistent right now. Is persistent btw connections? Or power cycles?

            if self.callbacks and self.callbacks.char3_notif_changed:
                self.callbacks.char3_notif_changed(self, evt.conn_idx, ccc)
            # TODO notification status change callback
            print(f"CustomerService write_req. Setting ccc={evt.value}")
            self.periph.write_cfm(evt.conn_idx, evt.handle, ble.ATT_ERROR.ATT_ERROR_OK)

        else:
            self.periph.write_cfm(evt.conn_idx, evt.handle, ble.ATT_ERROR.ATT_ERROR_WRITE_NOT_PERMITTED)

    def prepare_write_req(self, evt: ble.BleEventGattsPrepareWriteReq):
        if evt.handle == self.char_2_value_h.value:
            self.periph.prepare_write_cfm(evt.conn_idx, evt.handle, 2, ble.ATT_ERROR.ATT_ERROR_OK)
        else:
            self.periph.prepare_write_cfm(evt.conn_idx, evt.handle, 0, ble.ATT_ERROR.ATT_ERROR_REQUEST_NOT_SUPPORTED)

    def event_sent(self, evt: ble.BleEventGattsEventSent):
        print("CustomBleService event_sent")

    def cleanup(self):
        print("CustomBleService cleanup")

    def send_char1_read_cfm(self,
                                  conn_idx: int = 0,
                                  status: ble.ATT_ERROR = ble.ATT_ERROR.ATT_ERROR_OK,
                                  value: bytes = None
                                  ) -> ble.BLE_ERROR:

        return self.periph.read_cfm(conn_idx,
                                          self.char_1_value_h.value,
                                          status,
                                          value)

    def send_char1_write_cfm(self,
                                   conn_idx: int = 0,
                                   status: ble.ATT_ERROR = ble.ATT_ERROR.ATT_ERROR_OK
                                   ) -> ble.BLE_ERROR:

        return self.periph.write_cfm(conn_idx, self.char_1_value_h.value, status)

    def send_char2_write_cfm(self,
                                   conn_idx: int = 0,
                                   status: ble.ATT_ERROR = ble.ATT_ERROR.ATT_ERROR_OK
                                   ) -> ble.BLE_ERROR:

        return self.periph.write_cfm(conn_idx, self.char_2_value_h.value, status)

    def set_char2_value(self,
                              value: bytes
                              ) -> ble.BLE_ERROR:

        return self.periph.set_value(self.char_2_value_h.value, value)

    def set_char3_user_desc_value(self,
                                        value: bytes
                                        ) -> ble.BLE_ERROR:

        return self.periph.set_value(self.char_3_user_desc_h.value, value)

    def notify_char3(self,
                           conn_idx: int = 0,
                           value: bytes = None
                           ) -> ble.BLE_ERROR:

        return self.periph.send_event(conn_idx,
                                            self.char_3_value_h.value,
                                            ble.GATT_EVENT.GATT_EVENT_NOTIFICATION,
                                            value)
    
    def register_peripheral(self, periph: ble.BlePeripheral):
        self.periph = periph