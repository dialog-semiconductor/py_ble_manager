from enum import IntEnum


# Error code for ATT operation (as defined by Core 4.2 specification)
class ATT_ERROR(IntEnum):
    ATT_ERROR_OK = 0x00
    ATT_ERROR_INVALID_HANDLE = 0x01
    ATT_ERROR_READ_NOT_PERMITTED = 0x02
    ATT_ERROR_WRITE_NOT_PERMITTED = 0x03
    ATT_ERROR_INVALID_PDU = 0x04
    ATT_ERROR_INSUFFICIENT_AUTHENTICATION = 0x05
    ATT_ERROR_REQUEST_NOT_SUPPORTED = 0x06
    ATT_ERROR_INVALID_OFFSET = 0x07
    ATT_ERROR_INSUFFICIENT_AUTHORIZATION = 0x08
    ATT_ERROR_PREPARE_QUEUE_FULL = 0x09
    ATT_ERROR_ATTRIBUTE_NOT_FOUND = 0x0A
    ATT_ERROR_ATTRIBUTE_NOT_LONG = 0x0B
    ATT_ERROR_INSUFFICIENT_KEY_SIZE = 0x0C
    ATT_ERROR_INVALID_VALUE_LENGTH = 0x0D
    ATT_ERROR_UNLIKELY = 0x0E
    ATT_ERROR_INSUFFICIENT_ENCRYPTION = 0x0F
    ATT_ERROR_UNSUPPORTED_GROUP_TYPE = 0x10
    ATT_ERROR_INSUFFICIENT_RESOURCES = 0x11
    ATT_ERROR_APPLICATION_ERROR = 0x80
    ATT_ERROR_CCC_DESCRIPTOR_IMPROPERLY_CONFIGURED = 0xFD
    ATT_ERROR_PROCEDURE_ALREADY_IN_PROGRESS = 0xFE


# TODO rename BLE_ATT_PERM
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


# TODO rename BLE_ATT_UUID_TYPE
class ATT_UUID_TYPE(IntEnum):
    ATT_UUID_16 = 0
    ATT_UUID_128 = 1


class AttUuid:
    def __init__(self, uuid: bytes = None) -> None:
        self.uuid = uuid if uuid else bytes([0, 0])

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self.type == other.type:
                if self.uuid == other.uuid:
                    return True
        return False

    def _get_uuid(self) -> bytes:
        return self._uuid

    def _set_uuid(self, uuid: bytes = None):
        if len(uuid) == 2 or len(uuid) == 16:
            self._uuid = uuid
            self.type = ATT_UUID_TYPE.ATT_UUID_128 if len(uuid) == 16 else ATT_UUID_TYPE.ATT_UUID_16
        else:
            raise ValueError("UUID length must be 2 or 16")

    uuid = property(_get_uuid, _set_uuid)
