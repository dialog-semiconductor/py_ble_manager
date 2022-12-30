from enum import IntEnum, auto


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


# GAP connectivity modes
class BLE_GAP_CONN_MODE(IntEnum):
    GAP_CONN_MODE_NON_CONN = auto()  # Non-connectable mode
    GAP_CONN_MODE_UNDIRECTED = auto()  # Undirected mode
    GAP_CONN_MODE_DIRECTED = auto()  # Directed mode
    GAP_CONN_MODE_DIRECTED_LDC = auto()  # Directed Low Duty Cycle mode
