from enum import IntEnum, auto
from ..gtl_port.gap import GAP_KDIST


class BLE_DEVICE_TYPE(IntEnum):
    NONE = 0
    CENTRAL = auto()
    PERIPHERAL = auto()
    OBSERVER = auto()
    BROADCASTER = auto()


class BLE_HW_TYPE(IntEnum):
    NONE = 0
    DA14531 = 1
    DA14695 = 2


class BleConfigDefault():
    """Default configuration for various BLE parameters
    """
    def __init__(self, ble_device_type: BLE_DEVICE_TYPE = BLE_DEVICE_TYPE.CENTRAL):

        self.dg_configBLE_SECURE_CONNECTIONS = (1)
        self.dg_configBLE_PAIR_INIT_KEY_DIST = (GAP_KDIST.GAP_KDIST_ENCKEY | GAP_KDIST.GAP_KDIST_IDKEY | GAP_KDIST.GAP_KDIST_SIGNKEY)
        self.dg_configBLE_PAIR_RESP_KEY_DIST = (GAP_KDIST.GAP_KDIST_ENCKEY | GAP_KDIST.GAP_KDIST_IDKEY | GAP_KDIST.GAP_KDIST_SIGNKEY)
        self.dg_configBLE_PRIVACY_1_2 = (0)
        self.defaultBLE_MAX_BONDED = (3)
        self.dg_configHW_TYPE = BLE_HW_TYPE.NONE

        self.dg_configBLE_CENTRAL = 1 if ble_device_type == BLE_DEVICE_TYPE.CENTRAL else 0
        self.dg_configBLE_PERIPHERAL = 1 if ble_device_type == BLE_DEVICE_TYPE.PERIPHERAL else 0
        self.dg_configBLE_OBSERVER = 1 if ble_device_type == BLE_DEVICE_TYPE.OBSERVER else 0
        self.dg_configBLE_BROADCASTER = 1 if ble_device_type == BLE_DEVICE_TYPE.BROADCASTER else 0

        self.dg_configBLE_DATA_LENGTH_RX_MAX = 251
        self.dg_configBLE_DATA_LENGTH_TX_MAX = 251
        self.defaultBLE_STATIC_ADDRESS = bytes([0x01, 0x00, 0xF4, 0x35, 0x23, 0x48])

        assert ((self.dg_configBLE_DATA_LENGTH_RX_MAX < 251) or (self.dg_configBLE_DATA_LENGTH_RX_MAX > 27))
        assert ((self.dg_configBLE_DATA_LENGTH_TX_MAX < 251) or (self.dg_configBLE_DATA_LENGTH_TX_MAX > 27))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            members_self = [getattr(self, attr) for attr in dir(self) if not attr.startswith("__")]
            members_other = [getattr(other, attr) for attr in dir(other) if not attr.startswith("__")]
            if members_self == members_other:
                return True
        return False


class BleConfigDA14531(BleConfigDefault):
    """DA14531 configuration for various BLE parameters
    """
    def __init__(self, ble_device_type: BLE_DEVICE_TYPE = BLE_DEVICE_TYPE.CENTRAL):
        super().__init__(ble_device_type)
        self.defaultBLE_MAX_BONDED = (5)
        self.dg_configHW_TYPE = BLE_HW_TYPE.DA14531


class BleConfigDA1469x(BleConfigDefault):
    """DA14695 configuration for various BLE parameters
    """
    def __init__(self, ble_device_type: BLE_DEVICE_TYPE = BLE_DEVICE_TYPE.CENTRAL):
        super().__init__(ble_device_type)
        self.defaultBLE_MAX_BONDED = (8)
        self.dg_configHW_TYPE = BLE_HW_TYPE.DA14695


class DA14531VersionInd():
    def __init__(self):
        super().__init__()
        self.hci_ver = 10
        self.lmp_ver = 10
        self.host_ver = 8
        self.hci_subver = 271
        self.lmp_subver = 271
        self.host_subver = 270
        self.manuf_name = 210

    def __eq__(self, other):
        return (self.hci_ver == other.hci_ver
                and self.hci_ver == other.hci_ver
                and self.lmp_ver == other.lmp_ver
                and self.host_ver == other.host_ver
                and self.hci_subver == other.hci_subver
                and self.lmp_subver == other.lmp_subver
                and self.host_subver == other.host_subver
                and self.manuf_name == other.manuf_name)


class DA14695VersionInd():
    def __init__(self):
        super().__init__()
        self.hci_ver = 11
        self.lmp_ver = 11
        self.host_ver = 8
        self.hci_subver = 24
        self.lmp_subver = 24
        self.host_subver = 526
        self.manuf_name = 210

    def __eq__(self, other):
        return (self.hci_ver == other.hci_ver
                and self.hci_ver == other.hci_ver
                and self.lmp_ver == other.lmp_ver
                and self.host_ver == other.host_ver
                and self.hci_subver == other.hci_subver
                and self.lmp_subver == other.lmp_subver
                and self.host_subver == other.host_subver
                and self.manuf_name == other.manuf_name)
