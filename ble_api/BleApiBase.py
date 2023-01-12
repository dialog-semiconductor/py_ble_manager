from adapter.BleAdapter import BleAdapter
from manager.BleManager import BleManager


class BleApiBase():
    def __init__(self, ble_manager: BleManager, ble_adapter: BleAdapter):
        self.ble_manager = ble_manager
        self.ble_adapter = ble_adapter
