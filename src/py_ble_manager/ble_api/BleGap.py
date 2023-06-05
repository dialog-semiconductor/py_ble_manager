from enum import IntEnum, auto
from ..ble_api.BleCommon import BleEventBase, BdAddress, BLE_ERROR, BLE_EVT_GAP, BLE_HCI_ERROR
from ..gtl_port.co_bt import ADV_DATA_LEN, BD_NAME_SIZE

BLE_CONN_IDX_INVALID = 0xFFFF
BLE_GAP_MAX_BONDED = 8      # (defaultBLE_MAX_BONDED) TODO defaultBLE_MAX_BONDED defined in ble_config.h # TODO this will be different for 531 vs 695
BLE_ENC_KEY_SIZE_MAX = 16
BLE_ADV_DATA_LEN_MAX = ADV_DATA_LEN - 3
BLE_NON_CONN_ADV_DATA_LEN_MAX = ADV_DATA_LEN
SCAN_RSP_DATA_LEN = ADV_DATA_LEN
BLE_GAP_DEVNAME_LEN_MAX = (BD_NAME_SIZE)


class ADV_FILT_POL():
    """Advertising filter policy
    """
    ADV_ALLOW_SCAN_ANY_CONN_ANY = 0  # Allow all scan and connect requests
    ADV_ALLOW_SCAN_WLIST_CONN_ANY = auto()  # Allow all connect requests and scan requests only from whitelist
    ADV_ALLOW_SCAN_ANY_CONN_WLIST = auto()  # Allow all scan requests and connect requests only from whitelist
    ADV_ALLOW_SCAN_WLIST_CONN_WLIST = auto()  # Allow scan and connect requests only from whitelist


class BLE_GAP_APPEARANCE(IntEnum):
    """GAP device external appearance
    """
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


class GAP_CONN_MODE(IntEnum):
    """GAP connectivity modes
    """
    GAP_CONN_MODE_NON_CONN = 0  # Non-connectable mode
    GAP_CONN_MODE_UNDIRECTED = auto()  # Undirected mode
    GAP_CONN_MODE_DIRECTED = auto()  # Directed mode
    GAP_CONN_MODE_DIRECTED_LDC = auto()  # Directed Low Duty Cycle mode


class BLE_GAP_PHY(IntEnum):
    """GAP PHY type
    """
    BLE_GAP_PHY_PREF_AUTO = 0x00  # No PHY preference
    BLE_GAP_PHY_1M = 0x01  # Bit rate of 1 megabit per second (Mb/s)
    BLE_GAP_PHY_2M = 0x02  # Bit rate of 2 megabit per second (Mb/s)
    BLE_GAP_PHY_CODED = 0x03  # LE Coded PHY (bit rate of 125 or 500 Kbit/s)


class BLE_GAP_ROLE(IntEnum):
    """GAP roles
    """
    GAP_NO_ROLE = 0x00  # No role
    GAP_OBSERVER_ROLE = 0x01  # Observer role
    GAP_BROADCASTER_ROLE = 0x02  # Broadcaster role
    GAP_CENTRAL_ROLE = 0x04  # Central role
    GAP_PERIPHERAL_ROLE = 0x08  # Peripheral role
    GAP_ALL_ROLES = (GAP_OBSERVER_ROLE  # All roles
                     | GAP_BROADCASTER_ROLE
                     | GAP_CENTRAL_ROLE
                     | GAP_PERIPHERAL_ROLE)


class GAP_ADV_CHANNEL(IntEnum):
    """_summary_
    Channels used for advertising
    """
    GAP_ADV_CHANNEL_37 = 0x01     # Advertising Channel 37 (2402MHz)
    GAP_ADV_CHANNEL_38 = 0x02     # Advertising Channel 38 (2426MHz)
    GAP_ADV_CHANNEL_39 = 0x04     # Advertising Channel 39 (2480MHz)


# Designed for 1:1 with ADV_HCI_TYPE
class GAP_ADV_TYPE(IntEnum):
    """GAP Advertising Type
    """

    # Connectable Undirected advertising
    CONN_UNDIR = 0x00
    # Connectable high duty cycle directed advertising
    CONN_DIR = auto()
    # Discoverable undirected advertising
    DISC_UNDIR = auto()
    # Non-connectable undirected advertising
    NONCONN_UNDIR = auto()
    # Connectable low duty cycle directed advertising
    CONN_DIR_LDC = auto()


class GAP_DATA_TYPE(IntEnum):
    """GAP Advertising Data Types, as defined by Bluetooth Core 4.2 specification

    note:: only data types valid for Advertising Data are included
    """
    GAP_DATA_TYPE_NONE = 0x00
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

    GAP_DATA_TYPE_RESERVED1 = 0x13

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


class GAP_DISC_MODE(IntEnum):
    """GAP discoverability modes
    """
    GAP_DISC_MODE_NON_DISCOVERABLE = 0  # Non-Discoverable mode
    GAP_DISC_MODE_GEN_DISCOVERABLE = auto()  # General-Discoverable mode
    GAP_DISC_MODE_LIM_DISCOVERABLE = auto()  # Limited-Discoverable mode
    GAP_DISC_MODE_BROADCASTER = auto()  # Broadcaster mode


class GAP_IO_CAPABILITIES(IntEnum):
    """GAP Input/Output capabilities
    """
    GAP_IO_CAP_DISP_ONLY = 0x00  # Display only
    GAP_IO_CAP_DISP_YES_NO = 0x01  # Display yes no
    GAP_IO_CAP_KEYBOARD_ONLY = 0x02  # Keyboard only
    GAP_IO_CAP_NO_INPUT_OUTPUT = 0x03  # No input no output
    GAP_IO_CAP_KEYBOARD_DISP = 0x04  # Keyboard display


class GAP_SCAN_MODE(IntEnum):
    """Scanning modes
    """
    GAP_SCAN_GEN_DISC_MODE = 0  # General-Discoverable mode
    GAP_SCAN_LIM_DISC_MODE = 1  # Limited-Discoverable mode
    GAP_SCAN_OBSERVER_MODE = 2  # Observer mode


class GAP_SCAN_TYPE(IntEnum):
    """Scanning types
    """
    GAP_SCAN_ACTIVE = 0  # Active Scan type
    GAP_SCAN_PASSIVE = 1  # Passive Scan type


class GAP_SEC_LEVEL(IntEnum):
    """GAP security levels
    """
    GAP_SEC_LEVEL_1 = 0x00,  # No security
    GAP_SEC_LEVEL_2 = 0x01  # Unauthenticated pairing with encryption
    GAP_SEC_LEVEL_3 = 0x02  # Authenticated pairing with encryption
    GAP_SEC_LEVEL_4 = 0x03  # Authenticated LE Secure Connections pairing with
                            # encryption using a 128-bit strength encryption key


class GapChnlMap():
    """Link Layer channel map

    :ivar map: channel map
    """

    def __init__(self, map: bytes = None) -> None:
        self.map = map if map else bytes()


class GapConnParams():
    """ GAP connection parameters

    :ivar interval_min_ms: connection interval minimum in milliseconds
    :ivar interval_max_ms: connection interval minimum in milliseconds
    :ivar slave_latency: slave latency, in number of events
    :ivar sup_timeout_ms: supervision timeout in milliseconds
    """

    def __init__(self, interval_min_ms: int = 0, interval_max_ms: int = 0, slave_latency: int = 0, sup_timeout_ms: int = 0) -> None:
        self.interval_min_ms = interval_min_ms  # Minimum connection interval
        self.interval_max_ms = interval_max_ms  # Maximum connection interval
        self.slave_latency = slave_latency  # Slave latency
        self.sup_timeout_ms = sup_timeout_ms  # Supervision timeout

    def __repr__(self) -> str:

        return f"{type(self).__name__}(interval_min_ms={self.interval_min_ms}, interval_max_ms={self.interval_max_ms} " + \
            f" slave_latency={self.slave_latency}, sup_timeout_ms={self.sup_timeout_ms})"


class GapScanParams():
    """GAP scan parameters

    :ivar interval_ms: scan interval in milliseconds
    :ivar window: scan window in milliseconds
    """

    def __init__(self, interval_ms: int = 0, window_ms: int = 0) -> None:
        self.interval_ms = interval_ms  # Scan interval
        self.window_ms = window_ms  # Scan window


class BleAdvData():
    """Advertising AD Structure

    :ivar len: length of AD structure, AD type byte + length of data
    :ivar type: AD Type
    :ivar data: data for AD structure
    """

    def __init__(self,
                 type: GAP_DATA_TYPE = GAP_DATA_TYPE.GAP_DATA_TYPE_FLAGS,
                 data: bytes = None,
                 ) -> None:
        self.type = type
        self.data = data if data else bytes()

    def _get_data(self):
        return self._data

    def _set_data(self, new_data: bytes):
        if len(new_data) <= ADV_DATA_LEN - 2:
            self._data = new_data if new_data else bytes()
            self.len = len(new_data) + 1  # len includes AD Type
        else:
            raise ValueError(f"Data cannot be longer than {ADV_DATA_LEN - 2} bytes. Was {len(new_data)} bytes")

    data = property(_get_data, _set_data)

    def __repr__(self):
        try:
            adv_type = eval(f"GAP_DATA_TYPE({self.type})")
        except ValueError:
            adv_type = self.type

        adv_type = str(adv_type)
        return_string = f"{type(self).__name__}(len={self.len}, "
        return_string += f"type={adv_type}, "
        return_string += f"data={list(self.data)})"

        return return_string


class BleEventGapAddressResolutionFailed(BleEventBase):
    """Class for :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_ADDRESS_RESOLUTION_FAILED` event

    :ivar evt_code: event code, :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_ADDRESS_RESOLUTION_FAILED`
    :ivar status: event status
    """
    def __init__(self,
                 status: BLE_ERROR = BLE_ERROR.BLE_STATUS_OK
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GAP.BLE_EVT_GAP_ADDRESS_RESOLUTION_FAILED)
        self.status = status  # Completion status


class BleEventGapAddressResolved(BleEventBase):
    """Class for :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_ADDRESS_RESOLVED` event

    :ivar evt_code: event code, :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_ADDRESS_RESOLVED`
    :ivar conn_idx: connection index
    :ivar resolved_address: static address
    :ivar address: random address
    """

    def __init__(self,
                 conn_idx: int = 0,
                 resolved_address: BdAddress = None,
                 address: BdAddress = None,
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GAP.BLE_EVT_GAP_ADDRESS_RESOLVED)
        self.conn_idx = conn_idx
        self.resolved_address = resolved_address if resolved_address else BdAddress()
        self.address = address if address else BdAddress()


class BleEventGapAdvCompleted(BleEventBase):
    """Class for :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_ADV_COMPLETED` event

    :ivar evt_code: event code, :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_ADV_COMPLETED`
    :ivar adv_type: advertising type
    :ivar status: event status
    """
    def __init__(self,
                 adv_type: GAP_CONN_MODE = GAP_CONN_MODE.GAP_CONN_MODE_UNDIRECTED,
                 status: BLE_ERROR = BLE_ERROR.BLE_STATUS_OK
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GAP.BLE_EVT_GAP_ADV_COMPLETED)
        self.adv_type = adv_type  # Advertising type
        self.status = status  # Completion status


class BleEventGapAdvReport(BleEventBase):
    """Class for :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_ADV_REPORT` event

    :ivar evt_code: event code, :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_ADV_REPORT`
    :ivar type: type of advertising packet
    :ivar address: BD address of advertising device
    :ivar rssi: received signal strength
    :ivar data: advertising data or scan response data
    """

    def __init__(self,
                 type: GAP_ADV_TYPE = GAP_ADV_TYPE.CONN_UNDIR,
                 address: BdAddress = None,
                 rssi: int = 0,
                 data: bytes = None
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GAP.BLE_EVT_GAP_ADV_REPORT)
        self.type = type
        self.address = address if address else BdAddress()
        self.rssi = rssi
        self.data = data if data else bytes()


class BleEventGapConnected(BleEventBase):
    """Class for :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_CONNECTED` event

    :ivar conn_idx: connection index, :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_CONNECTED`
    :ivar own_addr: own address
    :ivar peer_address: peer address
    :ivar conn_params: connection parameters
    """
    def __init__(self,
                 conn_idx: int = 0,
                 own_addr: BdAddress = None,
                 peer_address: BdAddress = None,
                 conn_params: GapConnParams = None
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GAP.BLE_EVT_GAP_CONNECTED)
        self.conn_idx = conn_idx
        self.own_addr = own_addr if own_addr else BdAddress()
        self.peer_address = peer_address if peer_address else BdAddress()
        self.conn_params = conn_params if conn_params else GapConnParams()


class BleEventGapConnectionCompleted(BleEventBase):
    """Class for :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_CONNECTION_COMPLETED` event

    :ivar evt_code: event code, :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_CONNECTION_COMPLETED`
    :ivar status: completion status
    """

    def __init__(self,
                 status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GAP.BLE_EVT_GAP_CONNECTION_COMPLETED)
        self.status = status


class BleEventGapConnParamUpdateCompleted(BleEventBase):
    """Class for :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_CONN_PARAM_UPDATE_COMPLETED` event

    :ivar evt_code: event code, :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_CONN_PARAM_UPDATE_COMPLETED`
    :ivar conn_idx: connection index
    :ivar status: completion status
    """

    def __init__(self,
                 conn_idx: int = 0,
                 status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GAP.BLE_EVT_GAP_CONN_PARAM_UPDATE_COMPLETED)
        self.conn_idx = conn_idx
        self.status = status


class BleEventGapConnParamUpdateReq(BleEventBase):
    """Class for :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_CONN_PARAM_UPDATE_REQ` event

    :ivar evt_code: event code, :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_CONN_PARAM_UPDATE_REQ`
    :ivar conn_idx: connection index
    :ivar conn_params: connection parameters
    """

    def __init__(self,
                 conn_idx: int = 0,
                 conn_params: GapConnParams = None
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GAP.BLE_EVT_GAP_CONN_PARAM_UPDATE_REQ)
        self.conn_idx = conn_idx
        self.conn_params = conn_params if conn_params else GapConnParams()


class BleEventGapConnParamUpdated(BleEventBase):
    """Class for :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_CONN_PARAM_UPDATED` event

    :ivar evt_code: event code, :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_CONN_PARAM_UPDATED`
    :ivar conn_idx: connection index
    :ivar conn_params: connection parameters
    """

    def __init__(self,
                 conn_idx: int = 0,
                 conn_params: GapConnParams = None
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GAP.BLE_EVT_GAP_CONN_PARAM_UPDATED)
        self.conn_idx = conn_idx
        self.conn_params = conn_params if conn_params else GapConnParams()


class BleEventGapDataLengthChanged(BleEventBase):
    """Class for :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_DATA_LENGTH_CHANGED` event

    :ivar evt_code: event code, :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_DATA_LENGTH_CHANGED`
    :ivar conn_idx: connection index
    :ivar max_rx_length: maximum number of payload octets in RX
    :ivar max_rx_time: maximum time used for RX
    :ivar max_tx_length: maximum number of payload octets in TX
    :ivar max_tx_time: maximum time used for TX
    """
    def __init__(self,
                 conn_idx: int = 0,
                 max_rx_length: int = 0,
                 max_rx_time: int = 0,
                 max_tx_length: int = 0,
                 max_tx_time: int = 0,
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GAP.BLE_EVT_GAP_DATA_LENGTH_CHANGED)
        self.conn_idx = conn_idx
        self.max_rx_length = max_rx_length
        self.max_rx_time = max_rx_time
        self.max_tx_length = max_tx_length
        self.max_tx_time = max_tx_time


class BleEventGapDataLengthSetFailed(BleEventBase):
    """Class for :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_DATA_LENGTH_SET_FAILED` event

    :ivar evt_code: event code, :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_DATA_LENGTH_SET_FAILED`
    :ivar conn_idx: connection index
    :ivar status: event status
    """
    def __init__(self,
                 conn_idx: int = 0,
                 status: BLE_ERROR = BLE_ERROR.BLE_STATUS_OK
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GAP.BLE_EVT_GAP_DATA_LENGTH_SET_FAILED)
        self.conn_idx = conn_idx  # Connection index
        self.status = status  # Completion status


class BleEventGapLtkMissing(BleEventBase):
    """Class for :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_LTK_MISSING` event

    :ivar evt_code: event code, :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_LTK_MISSING`
    :ivar conn_idx: connection index
    """

    def __init__(self,
                 conn_idx: int = 0,
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GAP.BLE_EVT_GAP_LTK_MISSING)
        self.conn_idx = conn_idx


class BleEventGapPeerFeatures(BleEventBase):
    """Class for :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_PEER_FEATURES` event

    :ivar evt_code: event code, :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_PEER_FEATURES`
    :ivar conn_idx: connection index
    :ivar le_features: 8-byte array for LE features
    """

    def __init__(self,
                 conn_idx: int = 0,
                 le_features: bytes = None
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GAP.BLE_EVT_GAP_PEER_FEATURES)
        self.conn_idx = conn_idx
        self.le_features = le_features if le_features else bytes()


class BleEventGapPeerVersion(BleEventBase):
    """Class for :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_PEER_VERSION` event

    :ivar evt_code: event code, :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_PEER_VERSION`
    :ivar conn_idx: connection index
    :ivar lmp_version: supported Bluetooth LMP Specification
    :ivar company_id: company ID
    :ivar lmp_subversion: implementation subversion
    """

    def __init__(self,
                 conn_idx: int = 0,
                 lmp_version: int = 0,
                 company_id: int = 0,
                 lmp_subversion: int = 0,
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GAP.BLE_EVT_GAP_PEER_VERSION)
        self.conn_idx = conn_idx
        self.lmp_version = lmp_version
        self.company_id = company_id
        self.lmp_subversion = lmp_subversion


class BleEventGapDisconnected(BleEventBase):
    """Class for :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_DISCONNECTED` event

    :ivar evt_code: event code, :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_DISCONNECTED`
    :ivar conn_idx: connection index
    :ivar address: BD address of disconnected device
    :ivar reason: reason of disconnection
    """

    def __init__(self,
                 conn_idx: int = 0,
                 address: BdAddress = None,
                 reason: BLE_HCI_ERROR = BLE_HCI_ERROR.BLE_HCI_ERROR_NO_ERROR,
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GAP.BLE_EVT_GAP_DISCONNECTED)
        self.conn_idx = conn_idx
        self.address = address if address else BdAddress()
        self.reason = reason


class BleEventGapDisconnectFailed(BleEventBase):
    """Class for :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_DISCONNECT_FAILED` event

    :ivar evt_code: event code, :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_DISCONNECT_FAILED`
    :ivar conn_idx: connection index
    :ivar status: error status
    """

    def __init__(self,
                 conn_idx: int = 0,
                 status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED,
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GAP.BLE_EVT_GAP_DISCONNECT_FAILED)
        self.conn_idx = conn_idx
        self.status = status


class BleEventGapNumericRequest(BleEventBase):
    """Class for :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_NUMERIC_REQUEST` event

    :ivar evt_code: event code, :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_NUMERIC_REQUEST`
    :ivar conn_idx: connection index
    :ivar num_key: numeric comparison key
    """

    def __init__(self,
                 conn_idx: int = 0,
                 num_key: int = 0,
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GAP.BLE_EVT_GAP_NUMERIC_REQUEST)
        self.conn_idx = conn_idx
        self.num_key = num_key


class BleEventGapPairCompleted(BleEventBase):
    """Class for :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_PAIR_COMPLETED` event

    :ivar evt_code: event code, :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_PAIR_COMPLETED`
    :ivar conn_idx: connection index
    :ivar status: completion status
    :ivar bond: bond enabled flag
    :ivar mitm: man in the middle (MITM) protection enabled flag
    """

    def __init__(self,
                 conn_idx: int = 0,
                 status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED,
                 bond: bool = False,
                 mitm: bool = False
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GAP.BLE_EVT_GAP_PAIR_COMPLETED)
        self.conn_idx = conn_idx
        self.status = status
        self.bond = bond
        self.mitm = mitm


class BleEventGapPairReq(BleEventBase):
    """Class for :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_PAIR_REQ` event

    :ivar evt_code: event code, :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_PAIR_REQ`
    :ivar conn_idx: connection index
    :ivar bond: enable bond
    """

    def __init__(self,
                 conn_idx: int = 0,
                 bond: bool = False,
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GAP.BLE_EVT_GAP_PAIR_REQ)
        self.conn_idx = conn_idx
        self.bond = bond


class BleEventGapPasskeyNotify(BleEventBase):
    """Class for :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_PASSKEY_NOTIFY` event

    :ivar evt_code: event code, :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_PASSKEY_NOTIFY`
    :ivar conn_idx: connection index
    :ivar passkey: passkey
    """

    def __init__(self,
                 conn_idx: int = 0,
                 passkey: int = 0,
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GAP.BLE_EVT_GAP_PASSKEY_NOTIFY)
        self.conn_idx = conn_idx
        self.passkey = passkey


class BleEventGapScanCompleted(BleEventBase):
    """Class for :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_SCAN_COMPLETED` event

    :ivar evt_code: event code, :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_SCAN_COMPLETED`
    :ivar scan_type: scan type
    :ivar status: completion status
    """

    def __init__(self,
                 scan_type: GAP_SCAN_TYPE = GAP_SCAN_TYPE.GAP_SCAN_ACTIVE,
                 status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED,
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GAP.BLE_EVT_GAP_SCAN_COMPLETED)
        self.scan_type = scan_type
        self.status = status


class BleEventGapSecLevelChanged(BleEventBase):
    """Class for :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_SEC_LEVEL_CHANGED` event

    :ivar evt_code: event code, :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_SEC_LEVEL_CHANGED`
    :ivar conn_idx: connection index
    :ivar level: security level
    """

    def __init__(self,
                 conn_idx: int = 0,
                 level: GAP_SEC_LEVEL = GAP_SEC_LEVEL.GAP_SEC_LEVEL_1,
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GAP.BLE_EVT_GAP_SEC_LEVEL_CHANGED)
        self.conn_idx = conn_idx
        self.level = level
