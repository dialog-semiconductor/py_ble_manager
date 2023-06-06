from enum import IntEnum


ATT_UUID_128_LEN = 0x0010


# Characteristic Properties Bit
class ATT_CHAR_PROP(IntEnum):
    BROADCAST = 0x01,
    READ = 0x02,
    WRITE_NO_RESP = 0x04
    WRITE = 0x08,
    NOTIFY = 0x10
    INDICATE = 0x20
    AUTH = 0x40
    EXT_PROP = 0x80
