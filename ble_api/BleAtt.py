from enum import IntEnum


class ATT_UUID_TYPE(IntEnum):
    ATT_UUID_16 = 0
    ATT_UUID_128 = 1


class att_uuid():
    # TODO ctypes array instead of list?
    def __init__(self, type: ATT_UUID_TYPE = ATT_UUID_TYPE.ATT_UUID_16, uuid: list[int] = None) -> None:
        self.type = type 
        self.uuid = uuid if uuid else []  # TODO raise error if list too long or conflicts with type?


class ATT_ERROR(IntEnum):
    pass
