from ..adapter.BleAdapter import BleAdapter
from ..manager.BleManager import BleManager


class BleApiBase():
    """Base class for BLE API layer processing classes

    :param ble_manager: BLE Manager for the framework
    :type ble_manager: BleManager
    :param ble_adapter: BLE adapter for the framework
    :type ble_adapter: BleAdapter
    """
    def __init__(self, ble_manager: BleManager, ble_adapter: BleAdapter):
        self._ble_manager = ble_manager
        self._ble_adapter = ble_adapter
