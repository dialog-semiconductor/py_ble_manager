from enum import IntEnum


class ATT_UUID_TYPE(IntEnum):
    ATT_UUID_16 = 0
    ATT_UUID_128 = 1


# ATT attribute permission
class ATT_PERM(IntEnum):
    ATT_PERM_NONE = 0
    ATT_PERM_READ = 0x01
    ATT_PERM_WRITE = 0x02
    ATT_PERM_READ_AUTH = 0x04
    ATT_PERM_WRITE_AUTH = 0x08
    ATT_PERM_READ_ENCRYPT = 0x10
    ATT_PERM_WRITE_ENCRYPT = 0x20
    ATT_PERM_KEYSIZE_16 = 0x80
    # useful combinations
    ATT_PERM_RW = ATT_PERM_READ | ATT_PERM_WRITE
    ATT_PERM_RW_AUTH = ATT_PERM_READ_AUTH | ATT_PERM_WRITE_AUTH
    ATT_PERM_RW_ENCRYPT = ATT_PERM_READ_ENCRYPT | ATT_PERM_WRITE_ENCRYPT


class att_uuid():
    # TODO ctypes array instead of list?
    def __init__(self, type: ATT_UUID_TYPE = ATT_UUID_TYPE.ATT_UUID_16, uuid: list[int] = None) -> None:
        self.type = type
        self.uuid = uuid if uuid else []  # TODO raise error if list too long or conflicts with type?


class ATT_ERROR(IntEnum):
    pass
