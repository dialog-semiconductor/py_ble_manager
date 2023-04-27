from adapter.BleAdapter import BleAdapter
from manager.BleManager import BleManager


class BleApiBase():
    def __init__(self, ble_manager: BleManager, ble_adapter: BleAdapter):
        self._ble_manager = ble_manager
        self._ble_adapter = ble_adapter
