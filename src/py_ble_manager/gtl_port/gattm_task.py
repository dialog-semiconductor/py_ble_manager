from ctypes import Array, cast, c_uint8, c_uint16, LittleEndianStructure, pointer, POINTER
from enum import auto, IntEnum

from .att import ATT_UUID_128_LEN
from .attm import attm_svc_perm, att_perm, att_max_len_read_ind

from .rwble_hl_error import HOST_STACK_ERROR_CODE
from .rwip_config import KE_API_ID

GAPM_LE_LENGTH_EXT_OCTETS_MIN = 27
GAPM_LE_LENGTH_EXT_OCTETS_MAX = 251
GAPM_LE_LENGTH_EXT_TIME_MIN = 328
GAPM_LE_LENGTH_EXT_TIME_MAX = 2120


# GATT Task messages
class GATTM_MSG_ID(IntEnum):

    # Database Management */
    # Add service in database request
    GATTM_ADD_SVC_REQ = (KE_API_ID.TASK_ID_GATTM << 8)  # 0B00
    # Add service in database response
    GATTM_ADD_SVC_RSP = auto()

    # Service management */
    # Get permission settings of service request
    GATTM_SVC_GET_PERMISSION_REQ = auto()
    # Get permission settings of service response
    GATTM_SVC_GET_PERMISSION_RSP = auto()
    # Set permission settings of service request
    GATTM_SVC_SET_PERMISSION_REQ = auto()
    # Set permission settings of service response
    GATTM_SVC_SET_PERMISSION_RSP = auto()

    # Attribute Manipulation */
    # Get permission settings of attribute request
    GATTM_ATT_GET_PERMISSION_REQ = auto()
    # Get permission settings of attribute response
    GATTM_ATT_GET_PERMISSION_RSP = auto()
    # Set permission settings of attribute request
    GATTM_ATT_SET_PERMISSION_REQ = auto()
    # Set permission settings of attribute response
    GATTM_ATT_SET_PERMISSION_RSP = auto()

    # Get attribute value request
    GATTM_ATT_GET_VALUE_REQ = auto()
    # Get attribute value response
    GATTM_ATT_GET_VALUE_RSP = auto()
    # Set attribute value request
    GATTM_ATT_SET_VALUE_REQ = auto()
    # Set attribute value response
    GATTM_ATT_SET_VALUE_RSP = auto()

    # Debug messages */
    # DEBUG ONLY: Destroy Attribute database request
    GATTM_DESTROY_DB_REQ = auto()
    # DEBUG ONLY: Destroy Attribute database response
    GATTM_DESTROY_DB_RSP = auto()
    # DEBUG ONLY: Retrieve list of services request
    GATTM_SVC_GET_LIST_REQ = auto()
    # DEBUG ONLY: Retrieve list of services response
    GATTM_SVC_GET_LIST_RSP = auto()
    # DEBUG ONLY: Retrieve information of attribute request
    GATTM_ATT_GET_INFO_REQ = auto()
    # DEBUG ONLY: Retrieve information of attribute response
    GATTM_ATT_GET_INFO_RSP = auto()


# Attribute Description
class gattm_att_desc(LittleEndianStructure):
    def __init__(self,
                 uuid: c_uint8 * ATT_UUID_128_LEN = (c_uint8 * ATT_UUID_128_LEN)(),
                 perm: att_perm = att_perm(),
                 max_len_read_ind: att_max_len_read_ind = att_max_len_read_ind()
                 ):

        self.uuid = uuid
        self.perm = perm
        self.max_len_read_ind = max_len_read_ind
        super().__init__(uuid=self.uuid,
                         perm=self.perm,
                         max_len_read_ind=self.max_len_read_ind,
                         padding=0)

                # Attribute UUID (LSB First)
    _fields_ = [("uuid", c_uint8 * ATT_UUID_128_LEN),
                # Attribute Permission (@see attm_perm_mask)
                ("perm", att_perm),
                ("max_len_read_ind", att_max_len_read_ind),
                ("padding", c_uint16)]


# Service description
class gattm_svc_desc(LittleEndianStructure):
    def __init__(self,
                 start_hdl: c_uint16 = 0,
                 task_id: KE_API_ID = KE_API_ID.TASK_ID_GTL,
                 perm: attm_svc_perm = attm_svc_perm(),
                 uuid: (c_uint8 * ATT_UUID_128_LEN) = (c_uint8 * ATT_UUID_128_LEN)(),
                 atts: Array[gattm_att_desc] = None,
                 ):
        self.start_hdl = start_hdl
        self.task_id = task_id
        self.perm = perm
        self.uuid = uuid
        self.atts = atts
        super().__init__(start_hdl=self.start_hdl,
                         task_id=self.task_id,
                         perm=self.perm,
                         nb_att=self.nb_att,
                         uuid=self.uuid,
                         __padding__=0,
                         _atts=self._atts)

                # Attribute Start Handle (0 = dynamically allocated)
    _fields_ = [("start_hdl", c_uint16),
                # Task identifier that manages service
                ("task_id", c_uint16),
                # Service permissions (@see enum attm_svc_perm_mask)
                ("perm", attm_svc_perm),
                # Number of attributes
                ("nb_att", c_uint8),
                # Service  UUID
                ("uuid", c_uint8 * ATT_UUID_128_LEN),
                # if RWBLE_SW_VERSION_MAJOR >= 8
                ("__padding__", c_uint16),
                # endif
                # List of attribute description present in service.
                ("_atts", POINTER(gattm_att_desc))]

    def get_atts(self):
        # self._atts is a pointer to gattm_att_desc (LP_gattm_att_desc)
        # here we
        # 1. cast to a pointer to an array (LP_gattm_att_desc_Array_x where x is some positive integer)
        # 2. return the contents, providing the underlying array
        return cast(self._atts, POINTER(gattm_att_desc * self.nb_att)).contents

    def set_atts(self, value: Array[gattm_att_desc]):
        self._atts = value if value else pointer(gattm_att_desc())
        self.nb_att = len(value) if value else 1

    atts = property(get_atts, set_atts)


# Add service in database request
class gattm_add_svc_req(LittleEndianStructure):
    def __init__(self, svc_desc: gattm_svc_desc = gattm_svc_desc()):
        self.svc_desc = svc_desc
        super().__init__(svc_desc=self.svc_desc)

                # service description
    _fields_ = [("svc_desc", gattm_svc_desc)]


# Add service in database response
class gattm_add_svc_rsp(LittleEndianStructure):

    def __init__(self,
                 start_hdl: c_uint16 = 0,
                 status: HOST_STACK_ERROR_CODE = HOST_STACK_ERROR_CODE.ATT_ERR_NO_ERROR
                 ):
        self.start_hdl = start_hdl
        self.status = status
        super().__init__(start_hdl=self.start_hdl,
                         status=self.status,
                         padding=0)

                # Start handle of allocated service in attribute database
    _fields_ = [("start_hdl", c_uint16),
                # Return status of service allocation in attribute database.
                ("status", c_uint8),
                ("padding", c_uint8)]


# Service management
# Get permission settings of service request
class gattm_svc_get_permission_req(LittleEndianStructure):

    def __init__(self,
                 start_hdl: c_uint16 = 0,
                 ) -> None:
        self.start_hdl = start_hdl

        super().__init__(start_hdl=self.start_hdl,)

                # Service start attribute handle
    _fields_ = [("start_hdl", c_uint16)]


# Get permission settings of service response
class gattm_svc_get_permission_rsp(LittleEndianStructure):

    def __init__(self,
                 start_hdl: c_uint16 = 0,
                 perm: attm_svc_perm = attm_svc_perm(),
                 status: HOST_STACK_ERROR_CODE = HOST_STACK_ERROR_CODE.ATT_ERR_NO_ERROR
                 ) -> None:
        self.start_hdl = start_hdl
        self.perm = perm
        self.status = status
        super().__init__(start_hdl=self.start_hdl,
                         perm=self.perm,
                         status=self.status)

                # Service start attribute handle
    _fields_ = [("start_hdl", c_uint16),
                # service permission
                ("perm", attm_svc_perm),
                # Return status
                ("status", c_uint8)]


# Set permission settings of service request
class gattm_svc_set_permission_req(LittleEndianStructure):
    def __init__(self,
                 start_hdl: c_uint16 = 0,
                 perm: attm_svc_perm = attm_svc_perm(),
                 ) -> None:
        self.start_hdl = start_hdl
        self.perm = perm
        super().__init__(start_hdl=self.start_hdl,
                         perm=self.perm,
                         padding=0)

                # Service start attribute handle
    _fields_ = [("start_hdl", c_uint16),
                # service permission
                ("perm", attm_svc_perm),
                ("padding", c_uint8)]


# Set permission settings of service response
class gattm_svc_set_permission_rsp(LittleEndianStructure):
    def __init__(self,
                 start_hdl: c_uint16 = 0,
                 status: HOST_STACK_ERROR_CODE = HOST_STACK_ERROR_CODE.ATT_ERR_NO_ERROR
                 ) -> None:

        self.start_hdl = start_hdl
        self.status = status
        super().__init__(start_hdl=self.start_hdl,
                         status=self.status,
                         padding=0)

                # Service start attribute handle
    _fields_ = [("start_hdl", c_uint16),
                # Return status
                ("status", c_uint8),
                ("padding", c_uint8)]


# Get attribute value request
class gattm_att_get_value_req(LittleEndianStructure):

    def __init__(self, handle: c_uint16 = 0):
        self.handle = handle
        super().__init__(handle=self.handle)

                # Handle of the attribute
    _fields_ = [("handle", c_uint16)]


# Get attribute value response
class gattm_att_get_value_rsp(LittleEndianStructure):

    def __init__(self,
                 handle: c_uint16 = 0,
                 status: HOST_STACK_ERROR_CODE = HOST_STACK_ERROR_CODE.ATT_ERR_NO_ERROR,
                 value: Array[c_uint8] = 0):
        self.handle = handle
        self.status = status
        self.value = value
        super().__init__(handle=self.handle,
                         length=self.length,
                         status=self.status,
                         _value=self._value,
                         padding=0)

                # Handle of the attribute
    _fields_ = [("handle", c_uint16),
                # Attribute value length
                ("length", c_uint16),
                # Return status
                ("status", c_uint8),
                # Attribute value
                ("_value", POINTER(c_uint8)),
                ("paddong", c_uint8)]

    def get_value(self):
        return cast(self._value, POINTER(c_uint8 * self.length)).contents

    def set_value(self, new_value: Array[c_uint8]):
        if new_value and len(new_value) > 512:
            raise ValueError("Maximum length is 512")
        self._value = new_value if new_value else pointer(c_uint8(0))
        self.length = len(new_value) if new_value else 1

    value = property(get_value, set_value)


# Set attribute value request
class gattm_att_set_value_req(LittleEndianStructure):
    def __init__(self,
                 handle: c_uint16 = 0,
                 value: Array[c_uint8] = None
                 ):
        self.handle = handle
        self.value = value
        super().__init__(handle=self.handle,
                         length=self.length,
                         _value=self._value)

                # Handle of the attribute
    _fields_ = [("handle", c_uint16),
                # Attribute value length
                ("length", c_uint16),
                # Attribute value
                ("_value", POINTER(c_uint8))]

    def get_value(self):
        return cast(self._value, POINTER(c_uint8 * self.length)).contents

    def set_value(self, new_value: Array[c_uint8]):
        if new_value and len(new_value) > 512:
            raise ValueError("Maximum length is 512")
        self._value = new_value if new_value else pointer(c_uint8(0))
        self.length = len(new_value) if new_value else 1

    value = property(get_value, set_value)


# Set attribute value response
class gattm_att_set_value_rsp(LittleEndianStructure):

    def __init__(self,
                 handle: c_uint16 = 0,
                 status: HOST_STACK_ERROR_CODE = HOST_STACK_ERROR_CODE.ATT_ERR_NO_ERROR
                 ):

        self.handle = handle
        self.status = status
        super().__init__(handle=self.handle,
                         status=self.status,
                         padding=0)

                # Handle of the attribute
    _fields_ = [("handle", c_uint16),
                # Return status
                ("status", c_uint8),
                ("padding", c_uint8)]
