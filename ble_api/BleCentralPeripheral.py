# This is a dummy file to prevent circular dependency between BlePeripheral and BelServiceBase

class BleDeviceBase():
    pass


class BleCentral(BleDeviceBase):
    pass


class BlePeripheral(BleDeviceBase):
    pass
