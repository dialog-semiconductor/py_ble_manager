from enum import IntEnum, auto


class GATT_CCC(IntEnum):
    """GATT Client Characteristic Configuration bitmask values
    """
    GATT_CCC_NONE = 0x0000,
    GATT_CCC_NOTIFICATIONS = 0x0001,
    GATT_CCC_INDICATIONS = 0x0002,


class GATT_EVENT(IntEnum):
    """GATT event type
    """
    GATT_EVENT_NOTIFICATION = 0
    GATT_EVENT_INDICATION = 1


class GATT_PROP(IntEnum):
    """GATT characteristic properties
    """
    GATT_PROP_NONE = 0
    GATT_PROP_BROADCAST = 0x0001
    GATT_PROP_READ = 0x0002
    GATT_PROP_WRITE_NO_RESP = 0x0004
    GATT_PROP_WRITE = 0x0008
    GATT_PROP_NOTIFY = 0x0010
    GATT_PROP_INDICATE = 0x0020
    GATT_PROP_WRITE_SIGNED = 0x0040
    GATT_PROP_EXTENDED = 0x0080
    GATT_PROP_EXTENDED_RELIABLE_WRITE = 0x0100
    GATT_PROP_EXTENDED_WRITABLE_AUXILIARIES = 0x0200


class GATT_SERVICE(IntEnum):
    """GATT service type
    """
    GATT_SERVICE_PRIMARY = 0
    GATT_SERVICE_SECONDARY = auto()
