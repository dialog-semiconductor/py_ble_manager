from enum import IntEnum, auto


class SMP_PROP_ERROR(IntEnum):

    # No Error
    # No error has occurred during the SMP procedure.
    SMP_ERROR_NO_ERROR = 0x00

    # Request Disallowed
    # The request sent by the HL cannot be handled for some reasons (unauthorized source task,
    # role, ...)
    SMP_ERROR_REQ_DISALLOWED = 0xE1

    # Link Layer Error
    # An error has been received from the controller upon an encryption request.
    SMP_ERROR_LL_ERROR = auto()

    # Address Resolution Failed
    # The provided resolvable address has not been resolved.
    SMP_ERROR_ADDR_RESOLV_FAIL = auto()

    # Signature Verification Failed
    # The Signature Verification Failed
    SMP_ERROR_SIGN_VERIF_FAIL = auto()

    # Timeout
    # The command cannot be executed because a SMP timeout has been raised during the connection.

    SMP_ERROR_TIMEOUT = auto()

    # Encryption Key Missing
    # The encryption procedure failed because the slave device didn't find the LTK
    # needed to start an encryption session.
    SMP_ERROR_ENC_KEY_MISSING = (0xF1)

    # Encryption Not Supported
    # The encryption procedure failed because the slave device doesn't support the
    # encryption feature.

    SMP_ERROR_ENC_NOT_SUPPORTED = auto()

    # Encryption Request Timeout
    # A timeout has occurred during the start encryption session.

    SMP_ERROR_ENC_TIMEOUT = auto()
