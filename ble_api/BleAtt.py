from enum import IntEnum


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


class ATT_UUID_TYPE(IntEnum):
    ATT_UUID_16 = 0
    ATT_UUID_128 = 1


class att_uuid():
    def __init__(self, uuid: list[int] = None) -> None:
        if uuid:
            self.uuid = uuid if uuid else []

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self.type == other.type:
                if self.uuid == other.uuid:
                    return True
        return False

    def _get_uuid(self) -> list[int]:
        return self._uuid

    def _set_uuid(self, uuid: list[int] = None):
        if len(uuid) == 2 or len(uuid) == 16:
            self._uuid = uuid
            self.type = ATT_UUID_TYPE.ATT_UUID_128 if len(uuid) == 16 else ATT_UUID_TYPE.ATT_UUID_16
        else:
            raise ValueError("UUID length must be 2 or 16")

    uuid = property(_get_uuid, _set_uuid)
