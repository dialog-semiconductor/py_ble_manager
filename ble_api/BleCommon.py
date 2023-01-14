from enum import IntEnum, auto

# Bluetooth Address type
class BLE_ADDR_TYPE(IntEnum):
    PUBLIC_ADDRESS = 0x00  # Public Static Address
    PRIVATE_ADDRESS = 0x01  # Private Random Address


# BLE error code
class BLE_ERROR(IntEnum):
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


# BLE event categories
class BLE_EVT_CAT(IntEnum):
    BLE_EVT_CAT_COMMON = auto()
    BLE_EVT_CAT_GAP = auto()
    BLE_EVT_CAT_GATTS = auto()
    BLE_EVT_CAT_GATTC = auto()
    BLE_EVT_CAT_L2CAP = auto()


# TODO rename BLE_GAP_EVT? Moved here for __repr__ method of BleEventBase
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


# TODO rename BLE_GATTS_EVT? Moved here for __repr__ method of BleEventBase
class BLE_EVT_GATTS(IntEnum):
    # Read request from peer
    BLE_EVT_GATTS_READ_REQ = BLE_EVT_CAT.BLE_EVT_CAT_GATTS << 8
    # Write request from peer
    BLE_EVT_GATTS_WRITE_REQ = auto()
    # Prepare write request from peer
    BLE_EVT_GATTS_PREPARE_WRITE_REQ = auto()
    # Event (notification or indication) sent
    BLE_EVT_GATTS_EVENT_SENT = auto()


# Own Device Address type
class BLE_OWN_ADDR_TYPE(IntEnum):
    PUBLIC_STATIC_ADDRESS = auto()  # Public Static Address
    PRIVATE_STATIC_ADDRESS = auto()  # Private Static Address
    PRIVATE_RANDOM_RESOLVABLE_ADDRESS = auto()  # Private Random Resolvable Address
    PRIVATE_RANDOM_NONRESOLVABLE_ADDRESS = auto()  # Private Random Non-resolvable Address
# if (dg_configBLE_PRIVACY_1_2 == 1)
    PRIVATE_CNTL = auto()  # Private Random Resolvable address using LE privacy v1.2
# endif /* (dg_configBLE_PRIVACY_1_2 == 1) */


class BLE_STATUS(IntEnum):
    BLE_IS_DISABLED = 0x00
    BLE_IS_ENABLED = 0x01
    BLE_IS_BUSY = 0x02
    BLE_IS_RESET = 0x03


# Bluetooth Device address
class BdAddress():  # TODO rename BdAddress to differentiate from ctypes structures?
    def __init__(self, addr_type: BLE_ADDR_TYPE = BLE_ADDR_TYPE.PUBLIC_ADDRESS, addr: bytes = None) -> None:
        self.addr_type = addr_type  # TODO determine address type by addr?
        # TODO raise error on bytes len
        self.addr = addr if addr else bytes()

    def __repr__(self):

        return f"{type(self).__name__}(addr_type={BLE_ADDR_TYPE(self.addr_type)}, addr={list(self.addr)})"


class BleEventBase():
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

class Irk():
    def __init__(self, key: bytes = None) -> None:
        # TODO raise error on key len
        self.key = key if key else bytes()


class OwnAddress():
    def __init__(self, addr_type: BLE_OWN_ADDR_TYPE = BLE_OWN_ADDR_TYPE.PUBLIC_STATIC_ADDRESS, addr: bytes = None) -> None:
        self.addr_type = addr_type
        # TODO raise error on bytes len
        self.addr = addr if addr else bytes()
