from enum import IntEnum


# fields mask definitions.
class GAPC_FIELDS_MASK(IntEnum):

    # Bit[0]
    GAPC_ROLE_MASK = 0x01
    # Bit[1]
    GAPC_ENCRYPTED_MASK = 0x02
    # Bit[5-2]
    GAPC_AUTH_MASK = 0x3C
    # Bit[6]
    GAPC_SVC_CHG_CCC_MASK = 0x40
    # Bit[7]
    GAPC_LTK_MASK = 0x80
