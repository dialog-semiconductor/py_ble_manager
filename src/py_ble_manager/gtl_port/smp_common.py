from enum import IntEnum
from enum import auto


class SMP_PROP_ERROR(IntEnum):

    # No Error (0x00)
    # No error has occurred during the SMP procedure.
    SMP_ERROR_NO_ERROR = 0x00,

    # Request Disallowed (0x6B if RWBLE_SW_VERSION_MAJOR < 8,
    #                     0xE1 if RWBLE_SW_VERSION_MAJOR >= 8)
    # The request sent by the HL cannot be handled for some reasons (unauthorized source task,
    # role, ...)
    SMP_ERROR_REQ_DISALLOWED = 0xE1,

    # Link Layer Error (0x6C if RWBLE_SW_VERSION_MAJOR < 8,
    #                   0xE2 if RWBLE_SW_VERSION_MAJOR >= 8)
    # An error has been received from the controller upon an encryption request.
    SMP_ERROR_LL_ERROR = auto(),

    # Address Resolution Failed (0x6D if RWBLE_SW_VERSION_MAJOR < 8,
    #                            0xE3 if RWBLE_SW_VERSION_MAJOR >= 8)
    # The provided resolvable address has not been resolved.
    SMP_ERROR_ADDR_RESOLV_FAIL = auto(),

    # Signature Verification Failed (0x6E if RWBLE_SW_VERSION_MAJOR < 8,
    #                                0xE4 if RWBLE_SW_VERSION_MAJOR >= 8)
    # The Signature Verification Failed
    SMP_ERROR_SIGN_VERIF_FAIL = auto(),

    # Timeout (0x6F if RWBLE_SW_VERSION_MAJOR < 8,
    #          0xE5 if RWBLE_SW_VERSION_MAJOR >= 8)
    # The command cannot be executed because a SMP timeout has been raised during the connection.

    SMP_ERROR_TIMEOUT = auto(),

    # Encryption Key Missing (0x7B if RWBLE_SW_VERSION_MAJOR < 8,
    #                         0xF1 if RWBLE_SW_VERSION_MAJOR >= 8)
    # The encryption procedure failed because the slave device didn't find the LTK
    # needed to start an encryption session.
    SMP_ERROR_ENC_KEY_MISSING = (0xF1),

    # Encryption Not Supported (0x7C if RWBLE_SW_VERSION_MAJOR < 8,
    #                           0xF2 if RWBLE_SW_VERSION_MAJOR >= 8)
    # The encryption procedure failed because the slave device doesn't support the
    # encryption feature.

    SMP_ERROR_ENC_NOT_SUPPORTED = auto(),

    # Encryption Request Timeout (0x7D if RWBLE_SW_VERSION_MAJOR < 8,
    #                             0xF3 if RWBLE_SW_VERSION_MAJOR >= 8)
    # A timeout has occurred during the start encryption session.

    SMP_ERROR_ENC_TIMEOUT = auto(),
