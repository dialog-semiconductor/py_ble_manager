import asyncio

from ble_api.Ble import BlePeripheral
from ble_api.BleAtt import ATT_PERM, ATT_ERROR
from ble_api.BleCommon import BleEventBase
from ble_api.BleGap import BleEventGapConnected, BleEventGapDisconnected
from ble_api.BleGatt import GATT_SERVICE, GATT_PROP, GATT_EVENT
from ble_api.BleGatts import GATTS_FLAGS, BleEventGattsWriteReq, BleEventGattsPrepareWriteReq, BleEventGattsEventSent, BleEventGattsReadReq
from services.BleService import BleServiceBase, GattService, GattCharacteristic, Descriptor


class CustomBleService(BleServiceBase):
    def __init__(self) -> None:
        super().__init__()
        self.callbacks = {"CHAR1_APPLICATION_READ_CB", None,
                          "CHAR2_APPLICATION_READ_CB", None}

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

        # TODO getting error creating this char
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
        for char in self.gatt_characteristics:
            self.gatt_service.num_attrs += 2
            for desc in char.descriptors:
                self.gatt_service.num_attrs += 1

        self.char1_read_callback = None

    def connected_evt(self, evt: BleEventGapConnected):
        print("CustomBleService connected_evt")

    def disconnected_evt(self, evt: BleEventGapDisconnected):
        print("CustomBleService disconnected_evt")

    def read_req(self, evt: BleEventGattsReadReq):
        status = ATT_ERROR.ATT_ERROR_APPLICATION_ERROR
        data = None
        for item in self.gatt_characteristics:
            if evt.handle == item.char.handle:
                if self.char1_read_callback:
                    status, data = self.char1_read_callback(self)

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

                #if self.char1_read_callback:
                #    status, data = self.char1_read_callback(self)
        return status

    def prepare_write_req(self, evt: BleEventGattsPrepareWriteReq):
        print("CustomBleService prepare_write_req")

    def event_sent(self, evt: BleEventGattsEventSent):
        print("CustomBleService event_sent")

    def cleanup(self):
        print("CustomBleService cleanup")

    def _uuid_from_str(self, uuid_str: str) -> bytes:
        uuid_str = uuid_str.replace("-", "")
        uuid_list = [int(uuid_str[idx:idx + 2], 16) for idx in range(0, len(uuid_str), 2)]
        uuid_list.reverse()  # mcu is little endian
        return bytes(uuid_list)


def app_char1_read_callback(svc):
    print("app_char1_read_callback")
    status = ATT_ERROR.ATT_ERROR_OK
    data = 0x05
    return status, data.to_bytes(1, byteorder='little')


async def user_main(sample_q: asyncio.Queue):
    elapsed = 0
    delay = 1
    while True:
        await asyncio.sleep(delay)
        elapsed += delay
        sample_q.put_nowait(elapsed)
        print(f"User Main. elapsed={elapsed}")


async def main():

    sample_q = asyncio.Queue()
    # TODO should wait for serial port to open before attempting to interact with peripheral
    await asyncio.gather(user_main(sample_q), ble_task(sample_q))  # need to move this to another func and create a main loop


async def ble_task(sample_q: asyncio.Queue):

    periph = BlePeripheral("COM40")
    await periph.init()
    await periph.start()

    my_service = CustomBleService()
    my_service.init()
    my_service.char1_read_callback = app_char1_read_callback

    await periph.register_service(my_service)
    await periph.set_value(my_service.gatt_characteristics[1].char.handle, (0x8692).to_bytes(2, 'little'))
    await periph.set_value(my_service.gatt_characteristics[2].descriptors[0].handle, b"Hello")

    periph.set_advertising_interval(20, 30)
    await periph.start_advertising()

    timer_read_task = asyncio.create_task(sample_q.get(), name='sample_q_Read')
    ble_event_task = asyncio.create_task(periph.get_event(), name='GetBleEvent')
    pending = [timer_read_task, ble_event_task]

    while True:
        done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)

        for task in done:

            # Every second a "sample" is received from user_main
            if task is timer_read_task:
                sample: int = task.result()
                if my_service.ccc == 1:
                    error = await periph.send_event(0,
                                                    my_service.gatt_characteristics[2].char.handle,
                                                    GATT_EVENT.GATT_EVENT_NOTIFICATION,
                                                    sample.to_bytes(4, byteorder='little'))
                    print(f"Notification sent. sample = {sample}, error = {error}")

                timer_read_task = asyncio.create_task(sample_q.get(), name='sample_q_Read')
                pending.add(timer_read_task)

            # Handle and BLE events that hace occurred
            elif task is ble_event_task:
                evt: BleEventBase = task.result()  # TODO how does timeout error affect result
                if evt is not None:
                    handled = await periph.service_handle_event(evt)
                    if not handled:
                        # Application opportunity to handle event
                        # or apply default behaior
                        pass

                print(f"Main rx'd event: {evt}. hanlded={handled} \n")

                ble_event_task = asyncio.create_task(periph.get_event(), name='GetBleEvent')
                pending.add(ble_event_task)


asyncio.run(main())
