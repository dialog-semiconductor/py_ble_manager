from ctypes import Array, c_uint8, LittleEndianStructure
from enum import auto, IntEnum


BD_ADDR_LEN = 6
BD_NAME_SIZE = 0xF8  # Was 0x20 for BLE HL
ADV_DATA_LEN = 0x1F
SCAN_RSP_DATA_LEN = 0x1F
LE_CHNL_MAP_LEN = 0x05
KEY_LEN = 0x10
RAND_NB_LEN = 0x08
LE_FEATS_LEN = 0x08
BLE_LE_LENGTH_FEATURE = 0x20


# Advertising HCI Type
class ADV_HCI_TYPE(IntEnum):

    # Connectable Undirected advertising
    ADV_CONN_UNDIR = 0x00
    # Connectable high duty cycle directed advertising
    ADV_CONN_DIR = auto()
    # Discoverable undirected advertising
    ADV_DISC_UNDIR = auto()
    # Non-connectable undirected advertising
    ADV_NONCONN_UNDIR = auto()
    # Connectable low duty cycle directed advertising
    ADV_CONN_DIR_LDC = auto()
    # Enumeration end value for advertising type value check
    ADV_END = auto()


# BD address type
class BD_ADDRESS_TYPE(IntEnum):

    # Public BD address
    ADDR_PUBLIC = 0x00
    # Random BD Address
    ADDR_RAND = auto()
    # RPA or Public
    ADDR_RPA_PUBLIC = auto()
    # RPA or Random
    ADDR_RPA_RAND = auto()
    # Enumeration end value for BD address type value check
    ADDR_END = auto()


# Advertising channels enables
class ADV_CHANNEL_MAP(IntEnum):
    # Byte value for advertising channel map for channel 37 enable
    ADV_CHNL_37_EN = 0x01
    # Byte value for advertising channel map for channel 38 enable
    ADV_CHNL_38_EN = 0x02
    # Byte value for advertising channel map for channel 39 enable
    ADV_CHNL_39_EN = 0x04
    # Byte value for advertising channel map for channel 37, 38 and 39 enable
    ADV_ALL_CHNLS_EN = 0x07
    # Enumeration end value for advertising channels enable value check
    ADV_CHNL_END = auto()


# Advertising filter policy
class ADV_FILTER_POLICY(IntEnum):

    # Allow both scan and connection requests from anyone
    ADV_ALLOW_SCAN_ANY_CON_ANY = 0x00
    # Allow both scan req from White List devices only and connection req from anyone
    ADV_ALLOW_SCAN_WLST_CON_ANY = auto()
    # Allow both scan req from anyone and connection req from White List devices only
    ADV_ALLOW_SCAN_ANY_CON_WLST = auto()
    # Allow scan and connection requests from White List devices only
    ADV_ALLOW_SCAN_WLST_CON_WLST = auto()
    # Enumeration end value for advertising filter policy value check
    ADV_ALLOW_SCAN_END = auto()


# Scan filter policy
class SCAN_FILTER_POLICY(IntEnum):
    # Allow advertising packets from anyone
    SCAN_ALLOW_ADV_ALL = 0x00
    # Allow advertising packets from White List devices only
    SCAN_ALLOW_ADV_WLST = auto()
    # Allow advertising packets from anyone + RPA
    SCAN_ALLOW_ADV_ALL_RPA = auto()
    # Allow advertising packets from White List devices only + RPA
    SCAN_ALLOW_ADV_WLST_RPA = auto()
    # Enumeration end value for scan filter policy value check
    SCAN_ALLOW_ADV_END = auto()


# Filter duplicates
class SCAN_DUP_FILTER_POLICY(IntEnum):

    # Disable filtering of duplicate packets
    SCAN_FILT_DUPLIC_DIS = 0x00
    # Enable filtering of duplicate packets
    SCAN_FILT_DUPLIC_EN = auto()
    # Enumeration end value for scan duplicate filtering value check
    SCAN_FILT_DUPLIC_END = auto()


# BD Address structure
class bd_addr(LittleEndianStructure):

    def __init__(self,
                 addr: Array = (c_uint8 * BD_ADDR_LEN)()):
        assert len(addr) == BD_ADDR_LEN
        self.addr = addr
        super().__init__(addr=self.addr)

                # 6-byte array address value
    _fields_ = [("addr", c_uint8 * BD_ADDR_LEN)]


# Channel map structure
class le_chnl_map(LittleEndianStructure):

    def __init__(self,
                 map: Array = (c_uint8 * LE_CHNL_MAP_LEN)()):
        assert len(map) == LE_CHNL_MAP_LEN
        self.map = map
        super().__init__(map=self.map)

                # 5-byte channel map array
    _fields_ = [("map", c_uint8 * LE_CHNL_MAP_LEN)]


# Random number structure
class rand_nb(LittleEndianStructure):
    def __init__(self, nb: Array = (c_uint8 * RAND_NB_LEN)()):

        assert len(nb) == RAND_NB_LEN
        self.nb = nb
        super().__init__(nb=self.nb)

                # 8-byte array for random number
    _fields_ = [("nb", c_uint8 * RAND_NB_LEN)]


# Advertising report structure
class adv_report(LittleEndianStructure):

    def __init__(self,
                 evt_type: ADV_HCI_TYPE = ADV_HCI_TYPE.ADV_CONN_UNDIR,
                 # TODO find other instances of Public vs private addr in stack and use BD_ADDRESS_TYPE
                 adv_addr_type: BD_ADDRESS_TYPE = BD_ADDRESS_TYPE.ADDR_PUBLIC,
                 adv_addr: bd_addr = bd_addr(),
                 data: c_uint8 * ADV_DATA_LEN = (c_uint8 * ADV_DATA_LEN)(),
                 rssi: c_uint8 = 0
                 ) -> None:

        self.evt_type = evt_type
        self.adv_addr_type = adv_addr_type
        self.adv_addr = adv_addr
        self.data = data
        self.rssi = rssi
        super().__init__(evt_type=self.evt_type,
                         adv_addr_type=self.adv_addr_type,
                         adv_addr=self.adv_addr,
                         data_len=self.data_len,
                         _data=self._data,
                         rssi=self.rssi)

                # Event type:
                # - ADV_CONN_UNDIR: Connectable Undirected advertising
                # - ADV_CONN_DIR: Connectable directed advertising
                # - ADV_DISC_UNDIR: Discoverable undirected advertising
                # - ADV_NONCONN_UNDIR: Non-connectable undirected advertising
    _fields_ = [("evt_type", c_uint8),
                # Advertising address type: public/random
                ("adv_addr_type", c_uint8),
                # Advertising address value
                ("adv_addr", bd_addr),
                # Data length in advertising packet
                ("data_len", c_uint8),
                # Data of advertising packet
                ("_data", c_uint8 * ADV_DATA_LEN),
                # RSSI value for advertising packet
                ("rssi", c_uint8)]

    def get_data(self):
        return self._data

    def set_data(self, new_data: Array[c_uint8]):
        self._data = (c_uint8 * ADV_DATA_LEN)()
        self._data[:len(new_data)] = new_data
        self.data_len = len(new_data)

    data = property(get_data, set_data)
