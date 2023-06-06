from enum import IntEnum
from enum import auto


# Information source.
class SMPC_ADDR_SRC(IntEnum):

    # Local info.
    SMPC_INFO_LOCAL = auto()
    # Peer info.
    SMPC_INFO_PEER = auto()
    # Maximum info source.
    SMPC_INFO_MAX = auto()
