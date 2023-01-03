from enum import IntEnum, auto
from ble_api.BleCommon import BleEventBase, bd_address, BLE_ERROR, BLE_EVT_CAT


BLE_CONN_IDX_INVALID = 0xFFFF


# Advertising filter policy
class ADV_FILT_POL():
    ADV_ALLOW_SCAN_ANY_CONN_ANY = 0  # Allow all scan and connect requests
    ADV_ALLOW_SCAN_WLIST_CONN_ANY = auto()  # Allow all connect requests and scan requests only from whitelist
    ADV_ALLOW_SCAN_ANY_CONN_WLIST = auto()  # Allow all scan requests and connect requests only from whitelist
    ADV_ALLOW_SCAN_WLIST_CONN_WLIST = auto()  # Allow scan and connect requests only from whitelist


class BLE_EVT_GAP(IntEnum):
    # Connection established
    BLE_EVT_GAP_CONNECTED = BLE_EVT_CAT.BLE_EVT_CAT_GAP << 8
    # Advertising report
    BLE_EVT_GAP_ADV_REPORT = auto()
    # Disconnection event
    BLE_EVT_GAP_DISCONNECTED = auto()
    # Disconnect failed event
    BLE_EVT_GAP_DISCONNECT_FAILED = auto()
    # Advertising operation completed
    BLE_EVT_GAP_ADV_COMPLETED = auto()
    # Scan operation completed
    BLE_EVT_GAP_SCAN_COMPLETED = auto()
    # Connection parameter update request from peer
    BLE_EVT_GAP_CONN_PARAM_UPDATE_REQ = auto()
    # Connection parameters updated
    BLE_EVT_GAP_CONN_PARAM_UPDATED = auto()
    # Pairing request
    BLE_EVT_GAP_PAIR_REQ = auto()
    # Pairing completed
    BLE_EVT_GAP_PAIR_COMPLETED = auto()
    # Security request from peer
    BLE_EVT_GAP_SECURITY_REQUEST = auto()
    # Passkey notification
    BLE_EVT_GAP_PASSKEY_NOTIFY = auto()
    # Passkey request
    BLE_EVT_GAP_PASSKEY_REQUEST = auto()
    # Security level changed indication
    BLE_EVT_GAP_SEC_LEVEL_CHANGED = auto()
    # Random address resolved
    BLE_EVT_GAP_ADDRESS_RESOLVED = auto()
    # Set security level failed
    BLE_EVT_GAP_SET_SEC_LEVEL_FAILED = auto()
    # Connection parameters update completed
    BLE_EVT_GAP_CONN_PARAM_UPDATE_COMPLETED = auto()
    # Data length changed
    BLE_EVT_GAP_DATA_LENGTH_CHANGED = auto()
    # Data length set failed
    BLE_EVT_GAP_DATA_LENGTH_SET_FAILED = auto()
    # Connection operation completed
    BLE_EVT_GAP_CONNECTION_COMPLETED = auto()
    # Numeric request
    BLE_EVT_GAP_NUMERIC_REQUEST = auto()
    # Address resolution failed
    BLE_EVT_GAP_ADDRESS_RESOLUTION_FAILED = auto()
    # Long Term Key missing
    BLE_EVT_GAP_LTK_MISSING = auto()
    # Air Operation BD Address
    BLE_EVT_GAP_AIR_OP_BDADDR = auto()
# if (dg_configBLE_2MBIT_PHY == 1)
    # PHY set completed event
    BLE_EVT_GAP_PHY_SET_COMPLETED = auto()
    # PHY changed
    BLE_EVT_GAP_PHY_CHANGED = auto()
# endif /* (dg_configBLE_2MBIT_PHY == 1)
    # Peer version
    BLE_EVT_GAP_PEER_VERSION = auto()
    # Peer features
    BLE_EVT_GAP_PEER_FEATURES = auto()
    # Local Transmit Power Level event
    BLE_EVT_GAP_LOCAL_TX_PWR = auto()
    # Transmit Power Reporting
    BLE_EVT_GAP_TX_PWR_REPORT = auto()
    # Path Loss Threshold
    BLE_EVT_GAP_PATH_LOSS_THRES = auto()
# if BLE_SSP_DEBUG
    # LTK
    BLE_EVT_GAP_LTK = auto()
# endif


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


# GAP security levels
class GAP_SEC_LEVEL(IntEnum):
    GAP_SEC_LEVEL_1 = 0x00,  # No security
    GAP_SEC_LEVEL_2 = 0x01  # Unauthenticated pairing with encryption
    GAP_SEC_LEVEL_3 = 0x02  # Authenticated pairing with encryption
    GAP_SEC_LEVEL_4 = 0x03  # Authenticated LE Secure Connections pairing with
                            # encryption using a 128-bit strength encryption key


# Link Layer channel map
class gap_chnl_map():
    def __init__(self, map: list[int] = None) -> None:  # TODO is ctypes array appriopriate at this layer?
        # TODO raise error on list len
        self.map = map if map else []


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
    def __init__(self, adv_type: BLE_GAP_CONN_MODE = BLE_GAP_CONN_MODE.GAP_CONN_MODE_UNDIRECTED, status: BLE_ERROR = BLE_ERROR.BLE_STATUS_OK) -> None:
        super().__init__(evt_code=BLE_EVT_GAP.BLE_EVT_GAP_ADV_COMPLETED)
        self.adv_type = adv_type  # Advertising type
        self.status = status  # Completion status


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
                 reason: int = 0,
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GAP.BLE_EVT_GAP_DISCONNECTED)
        self.conn_idx = conn_idx
        self.address = address if address else bd_address()
        self.reason = reason
