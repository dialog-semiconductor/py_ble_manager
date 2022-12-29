from enum import IntEnum, auto


class BLE_STATUS(IntEnum):
    BLE_IS_DISABLED = 0x00
    BLE_IS_ENABLED = 0x01
    BLE_IS_BUSY = 0x02
    BLE_IS_RESET = 0x03


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


class BLE_MGR_CMD_CAT(IntEnum):
    BLE_MGR_COMMON_CMD_CAT = 0x00
    BLE_MGR_GAP_CMD_CAT = 0x01
    BLE_MGR_GATTS_CMD_CAT = 0x02
    BLE_MGR_GATTC_CMD_CAT = 0x03
    BLE_MGR_L2CAP_CMD_CAT = 0x04
    BLE_MGR_LAST_CMD_CAT = auto()
