from enum import IntEnum, auto
from ble_api.BleCommon import BleEventBase, bd_address, BLE_ERROR, BLE_EVT_GAP


BLE_CONN_IDX_INVALID = 0xFFFF


# TODO prefix with BLE_GAP?
# Advertising filter policy
class ADV_FILT_POL():
    ADV_ALLOW_SCAN_ANY_CONN_ANY = 0  # Allow all scan and connect requests
    ADV_ALLOW_SCAN_WLIST_CONN_ANY = auto()  # Allow all connect requests and scan requests only from whitelist
    ADV_ALLOW_SCAN_ANY_CONN_WLIST = auto()  # Allow all scan requests and connect requests only from whitelist
    ADV_ALLOW_SCAN_WLIST_CONN_WLIST = auto()  # Allow scan and connect requests only from whitelist


# GAP device external appearance
class BLE_GAP_APPEARANCE(IntEnum):
    BLE_GAP_APPEARANCE_UNKNOWN = 0
    BLE_GAP_APPEARANCE_GENERIC_PHONE = 64
    BLE_GAP_APPEARANCE_GENERIC_COMPUTER = 128
    BLE_GAP_APPEARANCE_GENERIC_WATCH = 192
    BLE_GAP_APPEARANCE_WATCH_SPORTS_WATCH = 193
    BLE_GAP_APPEARANCE_GENERIC_CLOCK = 256
    BLE_GAP_APPEARANCE_GENERIC_DISPLAY = 320
    BLE_GAP_APPEARANCE_GENERIC_REMOTE_CONTROL = 384
    BLE_GAP_APPEARANCE_GENERIC_EYE_GLASSES = 448
    BLE_GAP_APPEARANCE_GENERIC_TAG = 512
    BLE_GAP_APPEARANCE_GENERIC_KEYRING = 576
    BLE_GAP_APPEARANCE_GENERIC_MEDIA_PLAYER = 640
    BLE_GAP_APPEARANCE_GENERIC_BARCODE_SCANNER = 704
    BLE_GAP_APPEARANCE_GENERIC_THERMOMETER = 768
    BLE_GAP_APPEARANCE_THERMOMETER_EAR = 769
    BLE_GAP_APPEARANCE_GENERIC_HEART_RATE_SENSOR = 832
    BLE_GAP_APPEARANCE_HEART_RATE_SENSOR_HEART_RATE_BELT = 833
    BLE_GAP_APPEARANCE_GENERIC_BLOOD_PRESSURE = 896
    BLE_GAP_APPEARANCE_BLOOD_PRESSURE_ARM = 897
    BLE_GAP_APPEARANCE_BLOOD_PRESSURE_WRIST = 898
    BLE_GAP_APPEARANCE_GENERIC_HID = 960
    BLE_GAP_APPEARANCE_HID_KEYBOARD = 961
    BLE_GAP_APPEARANCE_HID_MOUSE = 962
    BLE_GAP_APPEARANCE_HID_JOYSTICK = 963
    BLE_GAP_APPEARANCE_HID_GAMEPAD = 964
    BLE_GAP_APPEARANCE_HID_DIGITIZER_TABLET = 965
    BLE_GAP_APPEARANCE_HID_CARD_READER = 966
    BLE_GAP_APPEARANCE_HID_DIGITAL_PEN = 967
    BLE_GAP_APPEARANCE_HID_BARCODE_SCANNER = 968
    BLE_GAP_APPEARANCE_GENERIC_GLUCOSE_METER = 1024
    BLE_GAP_APPEARANCE_GENERIC_RUNNING_WALKING_SENSOR = 1088
    BLE_GAP_APPEARANCE_RUNNING_WALKING_SENSOR_IN_SHOE = 1089
    BLE_GAP_APPEARANCE_RUNNING_WALKING_SENSOR_ON_SHOE = 1090
    BLE_GAP_APPEARANCE_RUNNING_WALKING_SENSOR_ON_HIP = 1091
    BLE_GAP_APPEARANCE_GENERIC_CYCLING = 1152
    BLE_GAP_APPEARANCE_CYCLING_CYCLING_COMPUTER = 1153
    BLE_GAP_APPEARANCE_CYCLING_SPEED_SENSOR = 1154
    BLE_GAP_APPEARANCE_CYCLING_CADENCE_SENSOR = 1155
    BLE_GAP_APPEARANCE_CYCLING_POWER_SENSOR = 1156
    BLE_GAP_APPEARANCE_CYCLING_SPEED_AND_CADENCE_SENSOR = 1157
    BLE_GAP_APPEARANCE_GENERIC_PULSE_OXIMETER = 3136
    BLE_GAP_APPEARANCE_PULSE_OXIMETER_FINGERTIP = 3137
    BLE_GAP_APPEARANCE_PULSE_OXIMETER_WRIST_WORN = 3138
    BLE_GAP_APPEARANCE_GENERIC_WEIGHT_SCALE = 3200
    BLE_GAP_APPEARANCE_GENERIC_OUTDOOR_SPORTS_ACTIVITY = 5184
    BLE_GAP_APPEARANCE_OUTDOOR_SPORTS_ACT_LOCATION_DISPLAY = 5185
    BLE_GAP_APPEARANCE_OUTDOOR_SPORTS_ACT_LOCATION_AND_NAVIGATION_DISPLAY = 5186
    BLE_GAP_APPEARANCE_OUTDOOR_SPORTS_ACT_LOCATION_POD = 5187
    BLE_GAP_APPEARANCE_OUTDOOR_SPORTS_ACT_LOCATION_AND_NAVIGATION_POD = 5188
    BLE_GAP_APPEARANCE_LAST = auto()


# GAP connectivity modes
class BLE_GAP_CONN_MODE(IntEnum):  # TODO Remove GAP_CONN_MODE prefix
    GAP_CONN_MODE_NON_CONN = 0  # Non-connectable mode
    GAP_CONN_MODE_UNDIRECTED = auto()  # Undirected mode
    GAP_CONN_MODE_DIRECTED = auto()  # Directed mode
    GAP_CONN_MODE_DIRECTED_LDC = auto()  # Directed Low Duty Cycle mode


# GAP PHY
class BLE_GAP_PHY(IntEnum):
    BLE_GAP_PHY_1M = 0x01  # Bit rate of 1 megabit per second (Mb/s)
    BLE_GAP_PHY_2M = 0x02  # Bit rate of 2 megabit per second (Mb/s)
    BLE_GAP_PHY_CODED = 0x03  # LE Coded PHY (bit rate of 125 or 500 Kbit/s)


# GAP roles
class BLE_GAP_ROLE(IntEnum):
    GAP_NO_ROLE = 0x00  # No role
    GAP_OBSERVER_ROLE = 0x01  # Observer role
    GAP_BROADCASTER_ROLE = 0x02  # Broadcaster role
    GAP_CENTRAL_ROLE = 0x04  # Central role
    GAP_PERIPHERAL_ROLE = 0x08  # Peripheral role
    GAP_ALL_ROLES = (GAP_OBSERVER_ROLE  # All roles
                     | GAP_BROADCASTER_ROLE
                     | GAP_CENTRAL_ROLE
                     | GAP_PERIPHERAL_ROLE)


class GAP_DATA_TYPE(IntEnum):
    # Flags 
    GAP_DATA_TYPE_FLAGS = 0x01
    # Incomplete List of 16-bit Service Class UUIDs 
    GAP_DATA_TYPE_UUID16_LIST_INC = 0x02
    # Complete List of 16-bit Service Class UUIDs 
    GAP_DATA_TYPE_UUID16_LIST = 0x03
    # Incomplete List of 32-bit Service Class UUIDs 
    GAP_DATA_TYPE_UUID32_LIST_INC = 0x04
    # Complete List of 32-bit Service Class UUIDs 
    GAP_DATA_TYPE_UUID32_LIST = 0x05
    # Incomplete List of 128-bit Service Class UUIDs 
    GAP_DATA_TYPE_UUID128_LIST_INC = 0x06
    # Complete List of 128-bit Service Class UUIDs 
    GAP_DATA_TYPE_UUID128_LIST = 0x07
    # Shortened Local Name 
    GAP_DATA_TYPE_SHORT_LOCAL_NAME = 0x08
    # Complete Local Name 
    GAP_DATA_TYPE_LOCAL_NAME = 0x09
    # Tx Power Level 
    GAP_DATA_TYPE_TX_POWER_LEVEL = 0x0A
    # Class of Device 
    GAP_DATA_TYPE_CLASS_OF_DEVICE = 0x0D
    # Simple Pairing Hash C-192 
    GAP_DATA_TYPE_SP_HASH_C = 0x0E
    # Simple Pairing Randomizer R-192 
    GAP_DATA_TYPE_SP_RANDOMIZER_R = 0x0F
    # Security Manager TK Value 
    GAP_DATA_TYPE_TK_VALUE = 0x10
    # Security Manager Out of Band Flags 
    GAP_DATA_TYPE_OOB_FLAGS = 0x11
    # Slave Connection Interval Range 
    GAP_DATA_TYPE_SLAVE_CONN_INTV = 0x12

    GAP_DATA_TYPE_RESERVED1 = 0x13  # TODO Is this used for something? 
    
    # List of 16-bit Service Solicitation UUIDs 
    GAP_DATA_TYPE_UUID16_SOLIC = 0x14
    # List of 128-bit Service Solicitation UUIDs 
    GAP_DATA_TYPE_UUID128_SOLIC = 0x15
    # Service Data - 16-bit UUID 
    GAP_DATA_TYPE_UUID16_SVC_DATA = 0x16
    # Public Target Address 
    GAP_DATA_TYPE_PUBLIC_ADDRESS = 0x17
    # Random Target Address 
    GAP_DATA_TYPE_RANDOM_ADDRESS = 0x18
    # Appearance 
    GAP_DATA_TYPE_APPEARANCE = 0x19
    # Advertising Interval 
    GAP_DATA_TYPE_ADV_INTERVAL = 0x1A
    # LE Bluetooth Device Address 
    GAP_DATA_TYPE_LE_BT_ADDR = 0x1B
    # LE Role 
    GAP_DATA_TYPE_LE_ROLE = 0x1C
    # Simple Pairing Hash C 
    GAP_DATA_TYPE_SPAIR_HASH = 0x1D
    # Simple Pairing Randomizer R 
    GAP_DATA_TYPE_SPAIR_RAND = 0x1E
    # List of 32-bit Service Solicitation UUIDs 
    GAP_DATA_TYPE_UUID32_SOLIC = 0x1F
    # Service Data - 32-bit UUID 
    GAP_DATA_TYPE_UUID32_SVC_DATA = 0x20
    # Service Data - 128-bit UUID 
    GAP_DATA_TYPE_UUID128_SVC_DATA = 0x21
    # LE Secure Connections Confirmation Value 
    GAP_DATA_TYPE_LE_SEC_CONN_CFM_VAL = 0x22
    # LE Secure Connections Random Value 
    GAP_DATA_TYPE_LE_SEC_CONN_RAND_VAL = 0x23
    # URI 
    GAP_DATA_TYPE_URI = 0x24
    # Indoor Positioning 
    GAP_DATA_TYPE_INDOOR_POSITIONING = 0x25
    # Transport Discovery Data 
    GAP_DATA_TYPE_TRANSPORT_DISC_DATA = 0x26
    # LE Supported Features 
    GAP_DATA_TYPE_LE_SUPP_FEATURES = 0x27
    # Channel Map Update Indication 
    GAP_DATA_TYPE_CHNL_MAP_UPD_IND = 0x28
    # PB-ADV 
    GAP_DATA_TYPE_PB_ADV = 0x29
    # Mesh Message 
    GAP_DATA_TYPE_MESH_MESSAGE = 0x2A
    # Mesh Beacon 
    GAP_DATA_TYPE_MESH_BEACON = 0x2B
    # 3D Information Data 
    GAP_DATA_TYPE_INFO_DATA_3D = 0x3D
    # Manufacturer Specific Data 
    GAP_DATA_TYPE_MANUFACTURER_SPEC = 0xFF


# TODO prefix these enums with BLE_
# GAP discoverability modes
class GAP_DISC_MODE(IntEnum):
    GAP_DISC_MODE_NON_DISCOVERABLE = 0  # Non-Discoverable mode
    GAP_DISC_MODE_GEN_DISCOVERABLE = auto()  # General-Discoverable mode
    GAP_DISC_MODE_LIM_DISCOVERABLE = auto()  # Limited-Discoverable mode
    GAP_DISC_MODE_BROADCASTER = auto()  # Broadcaster mode


# GAP Input/Output capabilities
class GAP_IO_CAPABILITIES(IntEnum):
    GAP_IO_CAP_DISP_ONLY = 0x00  # Display only
    GAP_IO_CAP_DISP_YES_NO = 0x01  # Display yes no
    GAP_IO_CAP_KEYBOARD_ONLY = 0x02  # Keyboard only
    GAP_IO_CAP_NO_INPUT_OUTPUT = 0x03  # No input no output
    GAP_IO_CAP_KEYBOARD_DISP = 0x04  # Keyboard display


# Scanning modes
class GAP_SCAN_MODE(IntEnum):
    GAP_SCAN_GEN_DISC_MODE = 0  # General-Discoverable mode
    GAP_SCAN_LIM_DISC_MODE = 1  # Limited-Discoverable mode
    GAP_SCAN_OBSERVER_MODE = 2  # Observer mode


# Scanning types
class GAP_SCAN_TYPE(IntEnum):
    GAP_SCAN_ACTIVE = 0  # Active Scan type
    GAP_SCAN_PASSIVE = 1  # Passive Scan type


# GAP security levels
class GAP_SEC_LEVEL(IntEnum):
    GAP_SEC_LEVEL_1 = 0x00,  # No security
    GAP_SEC_LEVEL_2 = 0x01  # Unauthenticated pairing with encryption
    GAP_SEC_LEVEL_3 = 0x02  # Authenticated pairing with encryption
    GAP_SEC_LEVEL_4 = 0x03  # Authenticated LE Secure Connections pairing with
                            # encryption using a 128-bit strength encryption key


# Link Layer channel map
class gap_chnl_map():
    def __init__(self, map: bytes = None) -> None:  # TODO is ctypes array appriopriate at this layer?
        # TODO raise error on bytes len
        self.map = map if map else bytes()


# GAP connection parameters
class gap_conn_params():
    # TODO is ctypes array appriopriate at this layer?
    def __init__(self, interval_min: int = 0, interval_max: int = 0, slave_latency: int = 0, sup_timeout: int = 0) -> None:
        self.interval_min = interval_min  # Minimum connection interval
        self.interval_max = interval_max  # Maximum connection interval
        self.slave_latency = slave_latency  # Slave latency
        self.sup_timeout = sup_timeout  # Supervision timeout


# GAP scan parameters
class gap_scan_params():
    def __init__(self, interval: int = 0, window: int = 0) -> None:  # TODO is ctypes array appriopriate at this layer?
        self.interval = interval  # Scan interval
        self.window = window  # Scan window


# TODO Perhaps events belong in their own file
class BleEventGapAdvCompleted(BleEventBase):
    def __init__(self,
                 adv_type: BLE_GAP_CONN_MODE = BLE_GAP_CONN_MODE.GAP_CONN_MODE_UNDIRECTED,
                 status: BLE_ERROR = BLE_ERROR.BLE_STATUS_OK
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GAP.BLE_EVT_GAP_ADV_COMPLETED)
        self.adv_type = adv_type  # Advertising type
        self.status = status  # Completion status


class BleEventGapAdvReport(BleEventBase):
    def __init__(self,
                 type: GAP_SCAN_TYPE = GAP_SCAN_TYPE.GAP_SCAN_ACTIVE,
                 address: bd_address = None,
                 rssi: int = 0,
                 length: int = 0,
                 data: bytes = None
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GAP.BLE_EVT_GAP_ADV_COMPLETED)
        self.type = type 
        self.address = address if address else bd_address()
        self.rssi = rssi
        self.length = length
        self.data = data if data else bytes()


class BleEventGapConnected(BleEventBase):
    def __init__(self,
                 conn_idx: int = 0,
                 own_addr: bd_address = None,
                 peer_address: bd_address = None,
                 conn_params: gap_conn_params = None
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GAP.BLE_EVT_GAP_CONNECTED)
        self.conn_idx = conn_idx
        self.own_addr = own_addr if own_addr else bd_address()
        self.peer_address = peer_address if peer_address else bd_address()
        self.conn_params = conn_params if conn_params else gap_conn_params()


class BleEventGapDisconnected(BleEventBase):
    def __init__(self,
                 conn_idx: int = 0,
                 address: bd_address = None,
                 reason: int = 0,  # TODO BLE Api Enum for this?
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GAP.BLE_EVT_GAP_DISCONNECTED)
        self.conn_idx = conn_idx
        self.address = address if address else bd_address()
        self.reason = reason


class BleEventGapScanCompleted(BleEventBase):
    def __init__(self,
                 scan_type: GAP_SCAN_TYPE = GAP_SCAN_TYPE.GAP_SCAN_ACTIVE,
                 status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED,
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GAP.BLE_EVT_GAP_SCAN_COMPLETED)
        self.scan_type = scan_type
        self.status = status


class BleAdvData():
    def __init__(self,
                 type: GAP_DATA_TYPE = GAP_DATA_TYPE.GAP_DATA_TYPE_FLAGS,
                 len: int = 0,
                 data: bytes = None,
                 ) -> None:
        self.type = type
        self.len = len
        self.data = data

    def __repr__(self):
        try:
            adv_type = eval(f"GAP_DATA_TYPE({self.type})")
        except ValueError:
            adv_type = self.type

        adv_type = str(adv_type)
        return_string = f"{type(self).__name__}(type={adv_type}, "
        return_string += f"len={self.len}, "
        return_string += f"data={self.data})"

        return return_string
