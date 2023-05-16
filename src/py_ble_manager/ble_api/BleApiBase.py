from ..manager.BleManager import BleManager


class BleApiBase():
    """Base class for BLE API layer processing classes

    :param ble_manager: BLE Manager for the framework
    :type ble_manager: BleManager
    """

    def __init__(self, ble_manager: BleManager):
        self._ble_manager = ble_manager
