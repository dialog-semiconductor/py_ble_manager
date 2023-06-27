from enum import IntEnum, auto


class BLE_ADDR_TYPE(IntEnum):
    """Bluetooth address type
    """
    PUBLIC_ADDRESS = 0x00  # Public Static Address
    PRIVATE_ADDRESS = 0x01  # Private Random Address


class BLE_ERROR(IntEnum):
    """BLE error code
    """
    BLE_STATUS_OK = 0x00,    # Success
    BLE_ERROR_FAILED = 0x01,    # Generic failure
    BLE_ERROR_ALREADY_DONE = 0x02,    # Already done
    BLE_ERROR_IN_PROGRESS = 0x03,    # Operation already in progress
    BLE_ERROR_INVALID_PARAM = 0x04,    # Invalid parameter
    BLE_ERROR_NOT_ALLOWED = 0x05,    # Not allowed
    BLE_ERROR_NOT_CONNECTED = 0x06,    # Not connected
    BLE_ERROR_NOT_SUPPORTED = 0x07,    # Not supported
    BLE_ERROR_NOT_ACCEPTED = 0x08,    # Not accepted
    BLE_ERROR_BUSY = 0x09,    # Busy
    BLE_ERROR_TIMEOUT = 0x0A,    # Request timed out
    BLE_ERROR_NOT_SUPPORTED_BY_PEER = 0x0B,    # Not supported by peer
    BLE_ERROR_CANCELED = 0x0C,    # Canceled by user
    BLE_ERROR_ENC_KEY_MISSING = 0x0D,    # encryption key missing
    BLE_ERROR_INS_RESOURCES = 0x0E,    # insufficient resources
    BLE_ERROR_NOT_FOUND = 0x0F,    # not found
    BLE_ERROR_L2CAP_NO_CREDITS = 0x10,    # no credits available on L2CAP CoC
    BLE_ERROR_L2CAP_MTU_EXCEEDED = 0x11,    # MTU exceeded on L2CAP CoC
    BLE_ERROR_INS_BANDWIDTH = 0x12,    # Insufficient bandwidth
    BLE_ERROR_LMP_COLLISION = 0x13,    # LMP collision
    BLE_ERROR_DIFF_TRANS_COLLISION = 0x14,    # Different transaction collision


class BLE_EVT_CAT(IntEnum):
    """BLE event categories
    """
    BLE_EVT_CAT_COMMON = auto()
    BLE_EVT_CAT_GAP = auto()
    BLE_EVT_CAT_GATTS = auto()
    BLE_EVT_CAT_GATTC = auto()
    BLE_EVT_CAT_L2CAP = auto()


class BLE_EVT_COMMON(IntEnum):
    """BLE Common events
    """
    # Connection established
    BLE_EVT_RESET_COMPLETED = BLE_EVT_CAT.BLE_EVT_CAT_COMMON << 8


class BLE_EVT_GAP(IntEnum):
    """BLE GAP events
    """
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
    # Local Transmit Power Level event*
    BLE_EVT_GAP_LOCAL_TX_PWR = auto()
    # Transmit Power Reporting
    BLE_EVT_GAP_TX_PWR_REPORT = auto()
    # Path Loss Threshold
    BLE_EVT_GAP_PATH_LOSS_THRES = auto()
# if BLE_SSP_DEBUG
    # LTK
    BLE_EVT_GAP_LTK = auto()
# endif


class BLE_EVT_GATTC(IntEnum):
    """BLE GATTC events
    """
    # Service found during browsing procedure
    BLE_EVT_GATTC_BROWSE_SVC = BLE_EVT_CAT.BLE_EVT_CAT_GATTC << 8
    # Browsing procedure completed
    BLE_EVT_GATTC_BROWSE_COMPLETED = auto()
    # Service found during discovery
    BLE_EVT_GATTC_DISCOVER_SVC = auto()
    # Included service found during discovery
    BLE_EVT_GATTC_DISCOVER_INCLUDE = auto()
    # Characteristic found during discovery
    BLE_EVT_GATTC_DISCOVER_CHAR = auto()
    # Characteristic descriptor found during discovery
    BLE_EVT_GATTC_DISCOVER_DESC = auto()
    # Discovery completed
    BLE_EVT_GATTC_DISCOVER_COMPLETED = auto()
    # Read attribute value completed
    BLE_EVT_GATTC_READ_COMPLETED = auto()
    # Write attribute value completed
    BLE_EVT_GATTC_WRITE_COMPLETED = auto()
    # Value notification received
    BLE_EVT_GATTC_NOTIFICATION = auto()
    # value indication received
    BLE_EVT_GATTC_INDICATION = auto()
    # MTU changes for peer
    BLE_EVT_GATTC_MTU_CHANGED = auto()


class BLE_EVT_GATTS(IntEnum):
    """BLE GATTS events
    """
    # Read request from peer
    BLE_EVT_GATTS_READ_REQ = BLE_EVT_CAT.BLE_EVT_CAT_GATTS << 8
    # Write request from peer
    BLE_EVT_GATTS_WRITE_REQ = auto()
    # Prepare write request from peer
    BLE_EVT_GATTS_PREPARE_WRITE_REQ = auto()
    # Event (notification or indication) sent
    BLE_EVT_GATTS_EVENT_SENT = auto()


class BLE_HCI_ERROR(IntEnum):
    """BLE HCI error code
    """
    BLE_HCI_ERROR_NO_ERROR = 0x00  # Success
    BLE_HCI_ERROR_UNKNOWN_HCI_COMMAND = 0x01  # Unknown HCI command
    BLE_HCI_ERROR_UNKNOWN_CONNECTION_ID = 0x02  # Unknown connection identifier
    BLE_HCI_ERROR_HARDWARE_FAILURE = 0x03  # Hardware failure
    BLE_HCI_ERROR_PAGE_TIMEOUT = 0x04  # Page timeout
    BLE_HCI_ERROR_AUTH_FAILURE = 0x05  # Authentication failure
    BLE_HCI_ERROR_PIN_MISSING = 0x06  # PIN or key missing
    BLE_HCI_ERROR_MEMORY_CAPA_EXCEED = 0x07  # Memory capacity exceeded
    BLE_HCI_ERROR_CON_TIMEOUT = 0x08  # Connection timeout
    BLE_HCI_ERROR_CON_LIMIT_EXCEED = 0x09  # Connection limit exceeded
    BLE_HCI_ERROR_SYNC_CON_LIMIT_DEV_EXCEED = 0x0A  # Synchronous connection limit to a device exceeded
    BLE_HCI_ERROR_ACL_CON_EXISTS = 0x0B  # ACL connection already exists
    BLE_HCI_ERROR_COMMAND_DISALLOWED = 0x0C  # Command disallowed
    BLE_HCI_ERROR_CONN_REJ_LIMITED_RESOURCES = 0x0D  # Connection rejected due to limited resources
    BLE_HCI_ERROR_CONN_REJ_SECURITY_REASONS = 0x0E  # Connection rejected due to security reasons
    BLE_HCI_ERROR_CONN_REJ_UNACCEPTABLE_BDADDR = 0x0F  # Connection rejected due to unacceptable BD_ADDR
    BLE_HCI_ERROR_CONN_ACCEPT_TIMEOUT_EXCEED = 0x10  # Connection accept timeout exceeded
    BLE_HCI_ERROR_UNSUPPORTED = 0x11  # Unsupported feature or parameter value
    BLE_HCI_ERROR_INVALID_HCI_PARAM = 0x12  # Invalid HCI command parameters
    BLE_HCI_ERROR_REMOTE_USER_TERM_CON = 0x13  # Remote User terminated connection
    BLE_HCI_ERROR_REMOTE_DEV_TERM_LOW_RESOURCES = 0x14  # Remote device terminated connection due to low resources
    BLE_HCI_ERROR_REMOTE_DEV_POWER_OFF = 0x15  # Remote device terminated connection due to power off
    BLE_HCI_ERROR_CON_TERM_BY_LOCAL_HOST = 0x16  # Connection terminated by local host
    BLE_HCI_ERROR_REPEATED_ATTEMPTS = 0x17  # Repeated attempts
    BLE_HCI_ERROR_PAIRING_NOT_ALLOWED = 0x18  # Pairing not allowed
    BLE_HCI_ERROR_UNKNOWN_LMP_PDU = 0x19  # Unknown LMP PDU
    BLE_HCI_ERROR_UNSUPPORTED_REMOTE_FEATURE = 0x1A  # Unsupported remote feature / Unsupported LMP feature
    BLE_HCI_ERROR_SCO_OFFSET_REJECTED = 0x1B  # SCO offset rejected
    BLE_HCI_ERROR_SCO_INTERVAL_REJECTED = 0x1C  # SCO interval rejected
    BLE_HCI_ERROR_SCO_AIR_MODE_REJECTED = 0x1D  # SCO air mode rejected
    BLE_HCI_ERROR_INVALID_LMP_PARAM = 0x1E  # Invalid LMP parameters / Invalid LL parameters
    BLE_HCI_ERROR_UNSPECIFIED_ERROR = 0x1F  # Unspecified error
    BLE_HCI_ERROR_UNSUPPORTED_LMP_PARAM_VALUE = 0x20  # Unsupported LMP parameter value / Unsupported LL parameter value
    BLE_HCI_ERROR_ROLE_CHANGE_NOT_ALLOWED = 0x21  # Role change not allowed
    BLE_HCI_ERROR_LMP_RSP_TIMEOUT = 0x22  # LMP response timeout / LL response timeout
    BLE_HCI_ERROR_LMP_COLLISION = 0x23  # LMP error transaction collision
    BLE_HCI_ERROR_LMP_PDU_NOT_ALLOWED = 0x24  # LMP PDU not allowed
    BLE_HCI_ERROR_ENC_MODE_NOT_ACCEPT = 0x25  # Encryption mode not acceptable
    BLE_HCI_ERROR_LINK_KEY_CANT_CHANGE = 0x26  # Link key cannot be changed
    BLE_HCI_ERROR_QOS_NOT_SUPPORTED = 0x27  # Requested QoS not supported
    BLE_HCI_ERROR_INSTANT_PASSED = 0x28  # Instant passed
    BLE_HCI_ERROR_PAIRING_WITH_UNIT_KEY_NOT_SUP = 0x29  # Pairing with unit key not supported
    BLE_HCI_ERROR_DIFF_TRANSACTION_COLLISION = 0x2A  # Different transaction collision
    BLE_HCI_ERROR_QOS_UNACCEPTABLE_PARAM = 0x2C  # QoS unacceptable parameter
    BLE_HCI_ERROR_QOS_REJECTED = 0x2D  # QoS rejected
    BLE_HCI_ERROR_CHANNEL_CLASS_NOT_SUP = 0x2E  # Channel classification not supported
    BLE_HCI_ERROR_INSUFFICIENT_SECURITY = 0x2F  # Insufficient security
    BLE_HCI_ERROR_PARAM_OUT_OF_MAND_RANGE = 0x30  # Parameter out of mandatory range
    BLE_HCI_ERROR_ROLE_SWITCH_PEND = 0x32  # Role switch pending
    BLE_HCI_ERROR_RESERVED_SLOT_VIOLATION = 0x34  # Reserved slot violation
    BLE_HCI_ERROR_ROLE_SWITCH_FAIL = 0x35  # Role switch failed
    BLE_HCI_ERROR_EIR_TOO_LARGE = 0x36  # Extended inquiry response too large
    BLE_HCI_ERROR_SP_NOT_SUPPORTED_HOST = 0x37  # Secure simple pairing not supported by host
    BLE_HCI_ERROR_HOST_BUSY_PAIRING = 0x38  # Host busy - pairing
    BLE_HCI_ERROR_CONN_REJ_NO_SUITABLE_CHANNEL = 0x39  # Connection rejected due to no suitable channel found
    BLE_HCI_ERROR_CONTROLLER_BUSY = 0x3A  # Controller busy
    BLE_HCI_ERROR_UNACCEPTABLE_CONN_INT = 0x3B  # Unacceptable connection parameters
    BLE_HCI_ERROR_DIRECT_ADV_TO = 0x3C  # Directed advertising timeout=
    BLE_HCI_ERROR_TERMINATED_MIC_FAILURE = 0x3D  # Connection terminated due to MIC failure
    BLE_HCI_ERROR_CONN_FAILED_TO_BE_EST = 0x3E  # Connection failed to be established
    BLE_HCI_ERROR_MAC_CONNECTION_FAILED = 0x3F  # MAC connection failed
    BLE_HCI_ERROR_COARSE_CLK_ADJUST_REJECTED = 0x40  # Coarse clock adjustment rejected but will try to adjust using clock dragging
    BLE_HCI_ERROR_UNKNOWN = auto()


class BLE_OWN_ADDR_TYPE(IntEnum):
    """Own device address type
    """
    PUBLIC_STATIC_ADDRESS = auto()  # Public Static Address
    PRIVATE_STATIC_ADDRESS = auto()  # Private Static Address
    PRIVATE_RANDOM_RESOLVABLE_ADDRESS = auto()  # Private Random Resolvable Address
    PRIVATE_RANDOM_NONRESOLVABLE_ADDRESS = auto()  # Private Random Non-resolvable Address
# if (dg_configBLE_PRIVACY_1_2 == 1)
    PRIVATE_CNTL = auto()  # Private Random Resolvable address using LE privacy v1.2
# endif /* (dg_configBLE_PRIVACY_1_2 == 1)


class BLE_STATUS(IntEnum):
    """BLE status
    """
    BLE_IS_DISABLED = 0x00
    BLE_IS_ENABLED = 0x01
    BLE_IS_BUSY = 0x02
    BLE_IS_RESET = 0x03


class BdAddress():
    """ Bluetooth Device address

    :ivar addr_type: address type
    :ivar addr: 6 byte address
    """
    def __init__(self, addr_type: BLE_ADDR_TYPE = BLE_ADDR_TYPE.PUBLIC_ADDRESS, addr: bytes = None) -> None:
        self.addr_type = addr_type
        self.addr = addr if addr else bytes()

    def __repr__(self):

        return f"{type(self).__name__}(addr_type={BLE_ADDR_TYPE(self.addr_type).name}, addr={list(self.addr)})"


class BleEventBase():
    """Base class for BLE events

    :ivar evt_code: event code
    """
    def __init__(self, evt_code) -> None:
        self.evt_code = evt_code

    def __repr__(self):
        evt_code = str(eval(f"{type(self.evt_code).__name__}({self.evt_code})"))
        return_string = f"{type(self).__name__}(evt_code={evt_code}, "

        members = []
        for attr in dir(self):
            if not callable(getattr(self, attr)):
                if not attr.startswith("__"):
                    if attr != "evt_code":
                        if attr == "status":
                            status_str = str(eval(f"BLE_ERROR({getattr(self, attr)}), "))
                            members.append(f"status={status_str}, ")
                        if attr == "data":
                            members.append(f"{attr}={list(getattr(self, attr))}, ")
                        else:
                            members.append(f"{attr}={getattr(self, attr)}, ")

        for member in members:
            return_string += member
        return_string = return_string[:-2]
        return_string += ")"

        return return_string


class BleEventResetCompleted(BleEventBase):
    """Class for :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_COMMON.BLE_EVT_RESET_COMPLETED` event

    :ivar evt_code: event code
    :ivar status: event status
    """

    def __init__(self,
                 status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_COMMON.BLE_EVT_RESET_COMPLETED)
        self.status = status


class Irk():
    """Identity Resolving Key

    :ivar key: 16 byte key
    """
    def __init__(self, key: bytes = None) -> None:
        self.key = key if key else bytes()


class OwnAddress():
    """Own address

    :ivar addr_type: address type
    :ivar addr: 6 byte address
    """
    def __init__(self, addr_type: BLE_OWN_ADDR_TYPE = BLE_OWN_ADDR_TYPE.PUBLIC_STATIC_ADDRESS, addr: bytes = None) -> None:
        self.addr_type = addr_type
        self.addr = addr if addr else bytes()

    def __repr__(self):

        return f"{type(self).__name__}(addr_type={BLE_OWN_ADDR_TYPE(self.addr_type).name}, addr={list(self.addr)})"
