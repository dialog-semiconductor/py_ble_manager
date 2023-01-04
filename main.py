import asyncio
from ble_api.Ble import BlePeripheral
from services.BleService import BleServiceBase, GattService, GattCharacteristic
from ble_api.BleGap import BleEventGapConnected, BleEventGapDisconnected
from ble_api.BleGatts import BleEventGattsWriteReq, BleEventGattsPrepareWriteReq, BleEventGattsEventSent
from manager.BleManagerGatts import BleEventGattsReadReq, BleEventGattsReadCfmCmd
from ble_api.BleAtt import ATT_PERM, ATT_ERROR
from ble_api.BleGatt import GATT_SERVICE, GATT_PROP
from manager.BleManagerGatts import GATTS_FLAGS


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
        self.gatt_service.num_attrs = self._get_num_attr(0, 2, 0)

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
        my_char.char.flags = GATTS_FLAGS.GATTS_FLAG_CHAR_READ_REQ
        self.gatt_characteristics.append(my_char)

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

    def write_req(self, evt: BleEventGattsWriteReq):
        print("CustomBleService write_req")

    def prepare_write_req(self, evt: BleEventGattsPrepareWriteReq):
        print("CustomBleService prepare_write_req")

    def event_sent(self, evt: BleEventGattsEventSent):
        print("CustomBleService event_sent")

    def cleanup(self):
        print("CustomBleService cleanup")

    def _uuid_from_str(self, uuid_str: str):
        uuid_str = uuid_str.replace("-", "")
        uuid_list = [int(uuid_str[idx:idx + 2], 16) for idx in range(0, len(uuid_str), 2)]
        uuid_list.reverse()  # mcu is little endian
        return uuid_list


def app_char1_read_callback(svc):
    print("app_char1_read_callback")
    status = ATT_ERROR.ATT_ERROR_OK
    data = 0x05
    return status, [data]


async def user_main():
    elapsed = 0
    delay = 1
    # asyncio.all_tasks -> test printing all running tasks
    while True:
        await asyncio.sleep(delay)
        elapsed += delay
        print(f"User Main. elapsed={elapsed}")


async def main():
    # ble_task = asyncio.create_task(test.run())
    # task1 = asyncio.create_task(user_main())
    # await ble_task
    # await task1

    # TODO should wait for serial port to open before attempting to interact with peripheral
    await asyncio.gather(user_main(), ble_task())  # need to move this to another func and create a main loop


async def ble_task():
    periph = BlePeripheral("COM40")

    print("Main Opening port\n")
    # Open the serial port the the 531
    await periph.init()

    print("Mian Serial port opened\n")

    # periph.register_app
    response = await periph.start()
    print(f"Main after start {response}\n")

    my_service = CustomBleService()
    my_service.init()
    my_service.char1_read_callback = app_char1_read_callback
    response, my_service = await periph.register_service(my_service)

    print(f"Main service registered {response}\n")

    # TODO call to setup database

    periph.set_advertising_interval(20, 30)

    print(" after set interval")
    response = await periph.start_advertising()
    # TODO register app

    print(f"Main After periph.init(). response={response}\n")

    # TODO GAP_ERR_PRIVACY_CFG_PB from adv command

    while True:
        # handle messages
        evt = await periph.get_event()
        handled = periph.service_handle_event(evt)
        if not handled:
            pass
        print(f"Main rx'd event: {evt}. hanlded={handled} \n")

        # other stuff

        # must always yeild in a task to give others a chance to run
        await asyncio.sleep(1)


asyncio.run(main())

# TODO unit tests fail when pushed from remote
