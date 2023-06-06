from ctypes import c_uint8, LittleEndianStructure, c_uint16, c_uint32
from enum import IntEnum


class ATTM_SERVICE_TYPE(IntEnum):
    SECONDARY_SERVICE = 0
    PRIMARY_SERVICE = 1


class ATTM_UUID_LEN(IntEnum):
    BITS_16 = 0
    BITS_32 = 1
    BITS_128 = 2


class ATTM_PERM(IntEnum):
    DISABLE = 0
    ENABLE = 1
    UNAUTH = 2
    AUTH = 3


class ATTM_ENC_KEY_SIZE_16_BYTES(IntEnum):
    NO = 0
    YES = 1


class ATTM_TASK_MULTI_INSTANTIATED(IntEnum):
    NO = 0
    YES = 1


class ATTM_EXTENDED_PROPERTIES(IntEnum):
    NO = 0
    YES = 1


class ATTM_BROADCAST(IntEnum):
    NO = 0
    YES = 1


class ATTM_WRITE_COMMAND(IntEnum):
    NOT_ACCEPTED = 0
    ACCEPTED = 1


class ATTM_WRITE_SIGNED(IntEnum):
    NOT_ACCEPTED = 0
    ACCEPTED = 1


class ATTM_WRITE_REQUEST(IntEnum):
    NOT_ACCEPTED = 0
    ACCEPTED = 1


class ATTM_TRIGGER_READ_INDICATION(IntEnum):
    NO = 0
    YES = 1


class att_perm(LittleEndianStructure):
    def __init__(self,
                 read: ATTM_PERM = ATTM_PERM.DISABLE,
                 write: ATTM_PERM = ATTM_PERM.DISABLE,
                 indication: ATTM_PERM = ATTM_PERM.DISABLE,
                 notification: ATTM_PERM = ATTM_PERM.DISABLE,
                 extended_properties_present: ATTM_EXTENDED_PROPERTIES = ATTM_EXTENDED_PROPERTIES.NO,
                 broadcast: ATTM_BROADCAST = ATTM_BROADCAST.NO,
                 enc_key_size: ATTM_ENC_KEY_SIZE_16_BYTES = ATTM_ENC_KEY_SIZE_16_BYTES.NO,
                 write_command: ATTM_WRITE_COMMAND = ATTM_WRITE_COMMAND.NOT_ACCEPTED,
                 write_signed: ATTM_WRITE_SIGNED = ATTM_WRITE_SIGNED.NOT_ACCEPTED,
                 write_request: ATTM_WRITE_REQUEST = ATTM_WRITE_REQUEST.NOT_ACCEPTED,
                 uuid_len: ATTM_UUID_LEN = ATTM_UUID_LEN.BITS_16,
                 ):

        self.read = read
        self.write = write
        self.indication = indication
        self.notification = notification
        self.extended_properties_present = extended_properties_present
        self.broadcast = broadcast
        self.enc_key_size = enc_key_size
        self.write_command = write_command
        self.write_signed = write_signed
        self.write_request = write_request
        self.uuid_len = uuid_len
        super().__init__(read=self.read,
                         write=self.write,
                         indication=self.indication,
                         notification=self.notification,
                         extended_properties_present=self.extended_properties_present,
                         broadcast=self.broadcast,
                         write_command=self.write_command,
                         write_signed=self.write_signed,
                         write_request=self.write_request,
                         uuid_len=self.uuid_len,
                         reserved=0,)

                # Attribute Permission (@see attm_perm_mask)
    _fields_ = [("read", c_uint32, 3),
                ("write", c_uint32, 3),
                ("indication", c_uint32, 3),
                ("notification", c_uint32, 3),
                ("extended_properties_present", c_uint32, 1),
                ("broadcast", c_uint32, 1),
                ("enc_key_size", c_uint32, 1),
                ("write_command", c_uint32, 1),
                ("write_signed", c_uint32, 1),
                ("write_request", c_uint32, 1),
                ("uuid_len", c_uint32, 2),
                ("reserved", c_uint32, 12)]


class att_max_len_read_ind(LittleEndianStructure):

    def __init__(self,
                 max_len: c_uint16 = 0,
                 trigger_read_indication: ATTM_TRIGGER_READ_INDICATION = ATTM_TRIGGER_READ_INDICATION.NO,
                 ):

        self.max_len = max_len
        self.trigger_read_indication = trigger_read_indication
        super().__init__(max_len=self.max_len,
                         trigger_read_indication=self.trigger_read_indication)

                #  15   14   13   12   11   10   9    8    7    6    5    4    3    2    1    0
                # +----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
                # | RI |                               MAX_LEN                                    |
                # +----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
                #
                # Bit [0-14]: Maximum Attribute Length
                # Bit [15]  : Trigger Read Indication (0 = Value present in Database,
                #                                      1 = Value not present in Database)
                #
                # For Included Services and Characteristic Declarations, this field contains targeted
                # handle.
                #
                # For Characteristic Extended Properties, this field contains 2 byte value
                #
                # Not used Client Characteristic Configuration and Server Characteristic Configuration,
                # this field is not used.
    _fields_ = [("max_len", c_uint16, 15),
                ("trigger_read_indication", c_uint16, 1)]


#
#  Service permissions
#
#     7    6    5    4    3    2    1    0
#  +----+----+----+----+----+----+----+----+
#  | P  |UUID_LEN |      AUTH    |EKS | MI |
#  +----+----+----+----+----+----+----+----+
#
#  Bit [0]  : Task that manage service is multi-instantiated (Connection index is conveyed)
#  Bit [1]  : Encryption key Size must be 16 bytes
#  Bit [2-4]: Service Permission      (0 = Disable, 1 = Enable, 2 = UNAUTH, 3 = AUTH, 4 = SECURE)
#  Bit [5-6]: UUID Length             (0 = 16 bits, 1 = 32 bits, 2 = 128 bits, 3 = RFU)
#  Bit [7]  : Primary Service         (1 = Primary Service, 0 = Secondary Service)
#
#
class attm_svc_perm(LittleEndianStructure):
    def __init__(self,
                 multi: ATTM_TASK_MULTI_INSTANTIATED = ATTM_TASK_MULTI_INSTANTIATED.NO,
                 enc_key_16_bytes: ATTM_ENC_KEY_SIZE_16_BYTES = ATTM_ENC_KEY_SIZE_16_BYTES.NO,
                 svc_perm: ATTM_PERM = ATTM_PERM.UNAUTH,
                 uuid_len: ATTM_UUID_LEN = ATTM_UUID_LEN.BITS_16,
                 primary_svc: ATTM_SERVICE_TYPE = ATTM_SERVICE_TYPE.PRIMARY_SERVICE
                 ):

        self.multi = multi
        self.enc_key_16_bytes = enc_key_16_bytes
        self.svc_perm = svc_perm
        self.uuid_len = uuid_len
        self.primary_svc = primary_svc

        super().__init__(multi=self.multi,
                         enc_key_16_bytes=self.enc_key_16_bytes,
                         svc_perm=self.svc_perm,
                         uuid_len=self.uuid_len,
                         primary_svc=self.primary_svc)

                # Service permissions (@see enum attm_svc_perm_mask)
    _fields_ = [("multi", c_uint8, 1),
                ("enc_key_16_bytes", c_uint8, 1),
                ("svc_perm", c_uint8, 3),
                ("uuid_len", c_uint8, 2),
                ("primary_svc", c_uint8, 1)]
