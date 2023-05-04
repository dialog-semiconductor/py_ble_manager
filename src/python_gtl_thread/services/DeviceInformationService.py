
# from ..ble_api.BleAtt import ATT_PERM, ATT_ERROR
from ..ble_api.BleGap import BleEventGapConnected, BleEventGapDisconnected
# from ..ble_api.BleGatt import GATT_SERVICE, GATT_PROP
from ..ble_api.BleGatts import BleEventGattsWriteReq, BleEventGattsPrepareWriteReq, BleEventGattsEventSent, BleEventGattsReadReq
from ..services.BleService import BleServiceBase


# TODO should this be done by adding DISS task if running on 531
class DeviceInformationService(BleServiceBase):
    def __init__(self) -> None:
        super().__init__()

    def init(self):
        pass
        # self.gatt_service = GattService()

    def connected_evt(self, evt: BleEventGapConnected):
        print("DeviceInformationService connected_evt")

    def disconnected_evt(self, evt: BleEventGapDisconnected):
        print("DeviceInformationService disconnected_evt")

    def read_req(self, evt: BleEventGattsReadReq):

        print(f"DeviceInformationService read_req. evt.handle={evt.handle}")

    def write_req(self, evt: BleEventGattsWriteReq):
        print(f"DeviceInformationService write_req. Char write handle={evt.handle} value={evt.value}")

    def prepare_write_req(self, evt: BleEventGattsPrepareWriteReq):
        print("DeviceInformationService prepare_write_req")

    def event_sent(self, evt: BleEventGattsEventSent):
        print("DeviceInformationService event_sent")

    def cleanup(self):
        print("DeviceInformationService cleanup")
