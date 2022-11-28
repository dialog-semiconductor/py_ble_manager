'''
/**
 ****************************************************************************************
 *
 * @file gattm_task.h
 *
 * @brief Header file - GATTMTASK.
 *
 * Copyright (C) RivieraWaves 2009-2014
 *
 *
 ****************************************************************************************
 */

#ifndef GATTM_TASK_H_
#define GATTM_TASK_H_

/**
 ****************************************************************************************
 * @addtogroup GATTMTASK Task
 * @ingroup GATTM
 * @brief Handles ALL GATT block operations not related to a connection.
 *
 * The GATTMTASK is responsible for managing internal attribute database and state of
 * GATT controller which manage GATT block operations related to a connection.
 *
 * Messages may originate from @ref ATTM "ATTM", @ref GAP "GAP" and Application.
 *
 * @{
 ****************************************************************************************
 */
/*
 * INCLUDE FILES
 ****************************************************************************************
 */
 '''
#include "rwip_config.h"
#if (BLE_CENTRAL || BLE_PERIPHERAL)

#include "gatt.h"
#include "attm.h"
#include "gattm.h"
#include "co_utils.h"

from enum import IntEnum
from enum import auto
from ctypes import *

from .co_bt import *
from .rwip_config import *
from .rwble_hl_error import *
from .att import *
from .attm import *

'''
/*
 * DEFINES
 ****************************************************************************************
 */

/// number of GATT Process
#define GATTM_IDX_MAX                                 0x01


/// states of GATT task
enum gattm_state_id
{
    /// idle state
    GATTM_IDLE,
    /// busy state
    GATTM_BUSY,
    /// Number of defined states.
    GATTM_STATE_MAX
};
'''
# GATT Task messages
class GATTM_MSG_ID(IntEnum):

    # Database Management */
    # Add service in database request
    GATTM_ADD_SVC_REQ = (KE_API_ID.TASK_ID_GATTM << 8) #0B00
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
class gattm_att_desc(Structure):
    def __init__(self, 
                  uuid: c_uint8*ATT_UUID_128_LEN = (c_uint8*ATT_UUID_128_LEN)(),
                  perm_read: ATTM_PERM = ATTM_PERM.DISABLE,
                  perm_write: ATTM_PERM = ATTM_PERM.DISABLE,
                  perm_indication: ATTM_PERM = ATTM_PERM.DISABLE,
                  perm_notification: ATTM_PERM = ATTM_PERM.DISABLE,
                  extended_properties_present: ATTM_EXTENDED_PROPERTIES = ATTM_EXTENDED_PROPERTIES.NO,
                  perm_broadcast: ATTM_BROADCAST = ATTM_BROADCAST.NO,
                  perm_enc_key_size: ATTM_ENC_KEY_SIZE_16_BYTES = ATTM_ENC_KEY_SIZE_16_BYTES.NO,
                  perm_write_command: ATTM_WRITE_COMMAND = ATTM_WRITE_COMMAND.NOT_ACCEPTED, 
                  perm_write_signed: ATTM_WRITE_SIGNED = ATTM_WRITE_SIGNED.NOT_ACCEPTED,
                  perm_write_request: ATTM_WRITE_REQUEST = ATTM_WRITE_REQUEST.NOT_ACCEPTED,
                  uuid_len: ATTM_UUID_LEN = ATTM_UUID_LEN._16_BITS, 
                  max_len: c_uint16 = 0,
                  trigger_read_indication: ATTM_TRIGGER_READ_INDICATION = ATTM_TRIGGER_READ_INDICATION.NO,
                  ):

        self.uuid = uuid
        self.perm_read = perm_read
        self.perm_write = perm_write
        self.perm_indication = perm_indication
        self.perm_notification = perm_notification
        self.extended_properties_present = extended_properties_present
        self.perm_broadcast = perm_broadcast
        self.perm_enc_key_size = perm_enc_key_size
        self.perm_write_command = perm_write_command
        self.perm_write_signed = perm_write_signed
        self.perm_write_request = perm_write_request
        self.uuid_len = uuid_len
        self.max_len = max_len
        self.trigger_read_indication = trigger_read_indication
        super().__init__(uuid=self.uuid,
                         perm_read=self.perm_read,
                         perm_write=self.perm_write,
                         perm_indication=self.perm_indication,
                         perm_notification=self.perm_notification,
                         extended_properties_present=self.extended_properties_present,
                         perm_broadcast=self.perm_broadcast,
                         perm_write_command=self.perm_write_command,
                         perm_write_signed=self.perm_write_signed,
                         perm_write_request=self.perm_write_request,
                         uuid_len=self.uuid_len,
                         perm_reserved=0,
                         max_len=self.max_len,
                         trigger_read_indication=self.trigger_read_indication,
                         padding=0)

                # Attribute UUID (LSB First) 
    _fields_ = [("uuid", c_uint8*ATT_UUID_128_LEN),
                # Attribute Permission (@see attm_perm_mask)
                ("perm_read", c_uint32, 3),
                ("perm_write", c_uint32, 3),
                ("perm_indication", c_uint32, 3),
                ("perm_notification", c_uint32, 3),
                ("extended_properties_present", c_uint32, 1),
                ("perm_broadcast", c_uint32, 1),
                ("perm_enc_key_size", c_uint32, 1),
                ("perm_write_command", c_uint32, 1),
                ("perm_write_signed", c_uint32, 1),
                ("perm_write_request", c_uint32, 1),
                ("uuid_len", c_uint32, 2),
                ("perm_reserved", c_uint32, 12),
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
                ("max_len", c_uint16, 15),
                ("trigger_read_indication", c_uint16, 1),
                ("padding", c_uint16)]


#TODO is factory a good work around for variable length atts
# Alternative approach: make atts a POINTER
# Service description
#def gattm_svc_desc_factory(nb_att):
class gattm_svc_desc(Structure):
    def __init__(self, 
                start_hdl: c_uint16 = 0,
                task_id: KE_API_ID = 0, 
                perm_multi: ATTM_TASK_MULTI_INSTANTIATED = ATTM_TASK_MULTI_INSTANTIATED.NO, 
                perm_enc_key_16_bytes: ATTM_ENC_KEY_SIZE_16_BYTES = ATTM_ENC_KEY_SIZE_16_BYTES.NO, 
                perm_svc_perm: ATTM_PERM = ATTM_PERM.UNAUTH, 
                perm_uuid_len: ATTM_UUID_LEN = ATTM_UUID_LEN._16_BITS, 
                perm_primary_svc: ATTM_SERVICE_TYPE = ATTM_SERVICE_TYPE.PRIMARY_SERVICE, 
                nb_att: c_uint8 = 0,
                uuid: c_uint*ATT_UUID_128_LEN = (c_uint8*ATT_UUID_128_LEN)(),
                atts: POINTER(gattm_att_desc) = POINTER(gattm_att_desc)(),
                ):
        self.start_hdl = start_hdl
        self.task_id = task_id
        self.perm_multi = perm_multi
        self.perm_enc_key_16_bytes = perm_enc_key_16_bytes
        self.perm_svc_perm = perm_svc_perm
        self.perm_uuid_len = perm_uuid_len
        self.perm_primary_svc = perm_primary_svc
        self.nb_att = nb_att
        self.uuid = uuid
        self.atts = atts
        super().__init__(start_hdl=self.start_hdl,
                        task_id=self.task_id,
                        perm_multi=self.perm_multi,
                        perm_enc_key_16_bytes=self.perm_enc_key_16_bytes,
                        perm_svc_perm=self.perm_svc_perm,
                        perm_uuid_len=self.perm_uuid_len,
                        perm_primary_svc=self.perm_primary_svc,
                        nb_att=self.nb_att,
                        uuid=self.uuid,
                        __padding__=0,
                        atts=self.atts)

                # Attribute Start Handle (0 = dynamically allocated)
    _fields_ = [("start_hdl", c_uint16),
                # Task identifier that manages service
                ("task_id", c_uint16),
                # Service permissions (@see enum attm_svc_perm_mask)
                ("perm_multi", c_uint8, 1),
                ("perm_enc_key_16_bytes", c_uint8, 1),
                ("perm_svc_perm", c_uint8, 3),
                ("perm_uuid_len", c_uint8, 2),
                ("perm_primary_svc", c_uint8, 1),
                # Number of attributes
                ("nb_att", c_uint8),
                # Service  UUID
                ("uuid", c_uint8*ATT_UUID_128_LEN),
                #if RWBLE_SW_VERSION_MAJOR >= 8
                ("__padding__", c_uint16),
                #endif
                # List of attribute description present in service.
                ("atts", POINTER(gattm_att_desc))] # TODO This needs to be an array of gattm_att_desc for each uuid
    #return gattm_svc_desc

'''
# Service description
class gattm_svc_desc(Structure):
    def __init__(self, 
                 start_hdl: c_uint16 = 0,
                 task_id: KE_API_ID = 0, 
                 perm: c_uint8 = 0, # TODO need type attm_svc_perm_mask
                 nb_att: c_uint8 = 0,
                 uuid: c_uint*ATT_UUID_128_LEN = (c_uint8*ATT_UUID_128_LEN)(),
                 atts: gattm_att_desc = gattm_att_desc(),
                 ):
        self.start_hdl = start_hdl
        self.task_id = task_id
        self.perm = perm
        self.nb_att = nb_att
        self.uuid = uuid
        self.atts = atts
        super().__init__(start_hdl=self.start_hdl,
                         task_id=self.task_id,
                         perm=self.perm,
                         nb_att=self.nb_att,
                         uuid=self.uuid,
                         __padding__=0,
                         atts=self.atts)


                # Attribute Start Handle (0 = dynamically allocated)
    _fields_ = [("start_hdl", c_uint16),
                # Task identifier that manages service
                ("task_id", c_uint16),
                # Service permissions (@see enum attm_svc_perm_mask)
                ("perm", c_uint8),
                # Number of attributes
                ("nb_att", c_uint8),
                # Service  UUID
                ("uuid", c_uint8*ATT_UUID_128_LEN),
                #if RWBLE_SW_VERSION_MAJOR >= 8
                ("__padding__", c_uint16),
                #endif
                # List of attribute description present in service.
                ("atts", gattm_att_desc)]
'''

# Add service in database request
class gattm_add_svc_req(Structure):
    def __init__(self, svc_desc: gattm_svc_desc = gattm_svc_desc()):
        self.svc_desc = svc_desc
        super().__init__(svc_desc=self.svc_desc)

                # service description
    _fields_ = [("svc_desc", gattm_svc_desc)]


'''

/// Add service in database response
struct gattm_add_svc_rsp
{
    /// Start handle of allocated service in attribute database
    uint16_t start_hdl;
    /// Return status of service allocation in attribute database.
    uint8_t status;
};

/* Service management */
/// Get permission settings of service request
struct gattm_svc_get_permission_req
{
    /// Service start attribute handle
    uint16_t start_hdl;
};

/// Get permission settings of service response
struct gattm_svc_get_permission_rsp
{
    /// Service start attribute handle
    uint16_t start_hdl;
    /// service permission
    uint8_t perm;
    /// Return status
    uint8_t status;
};

/// Set permission settings of service request
struct gattm_svc_set_permission_req
{
    /// Service start attribute handle
    uint16_t start_hdl;
    /// service permission
    uint8_t perm;
};

/// Set permission settings of service response
struct gattm_svc_set_permission_rsp
{
    /// Service start attribute handle
    uint16_t start_hdl;
    /// Return status
    uint8_t status;
};


/* Attribute management */
/// Get permission settings of attribute request
struct gattm_att_get_permission_req
{
    /// Handle of the attribute
    uint16_t handle;
};

/// Get permission settings of attribute response
struct gattm_att_get_permission_rsp
{
    /// Handle of the attribute
    uint16_t handle;
    /// Attribute permission
    att_perm_type perm;
    /// Return status
    uint8_t status;
};

/// Set permission settings of attribute request
struct gattm_att_set_permission_req
{
    /// Handle of the attribute
    uint16_t handle;
    /// Attribute permission
    att_perm_type perm;
};

/// Set permission settings of attribute response
struct gattm_att_set_permission_rsp
{
    /// Handle of the attribute
    uint16_t handle;
    /// Return status
    uint8_t status;
};


/// Get attribute value request
struct gattm_att_get_value_req
{
    /// Handle of the attribute
    uint16_t handle;
};

/// Get attribute value response
struct gattm_att_get_value_rsp
{
    /// Handle of the attribute
    uint16_t handle;
    /// Attribute value length
    uint16_t length;
    /// Return status
    uint8_t status;
    /// Attribute value
    uint8_t value[__ARRAY_EMPTY];
};

/// Set attribute value request
struct gattm_att_set_value_req
{
    /// Handle of the attribute
    uint16_t handle;
    /// Attribute value length
    uint16_t length;
    /// Attribute value
    uint8_t value[__ARRAY_EMPTY];
};

/// Set attribute value response
struct gattm_att_set_value_rsp
{
    /// Handle of the attribute
    uint16_t handle;
    /// Return status
    uint8_t status;
};

/// DEBUG ONLY: Destroy Attribute database request
struct gattm_destroy_db_req
{
    /// New Gap Start Handle
    uint16_t gap_hdl;
    /// New Gatt Start Handle
    uint16_t gatt_hdl;
};

/// DEBUG ONLY: Destroy Attribute database Response
struct gattm_destroy_db_rsp
{
    /// Return status
    uint8_t status;
};


/// Service information
struct gattm_svc_info
{
    /// Service start handle
    uint16_t start_hdl;
    /// Service end handle
    uint16_t end_hdl;
    /// Service task_id
    uint16_t task_id;
    /// Service permission
    uint8_t perm;
};

/// DEBUG ONLY: Retrieve list of services response
struct gattm_svc_get_list_rsp
{
    /// Return status
    uint8_t status;
    /// Number of services
    uint8_t nb_svc;
    /// Array of information about services
    struct gattm_svc_info svc[__ARRAY_EMPTY];
};

/// DEBUG ONLY: Retrieve information of attribute request
struct  gattm_att_get_info_req
{
    /// Attribute Handle
    uint16_t handle;
};

/// DEBUG ONLY: Retrieve information of attribute response
struct  gattm_att_get_info_rsp
{
    /// Return status
    uint8_t status;
    /// UUID Length
    uint8_t uuid_len;
    /// Attribute Handle
    uint16_t handle;
    /// Attribute Permissions
    att_perm_type perm;
    /// UUID value
    uint8_t uuid[ATT_UUID_128_LEN];
};

/*
 * FUNCTION DECLARATIONS
 ****************************************************************************************
 */
extern const struct ke_state_handler gattm_default_handler;
extern ke_state_t gattm_state[GATTM_IDX_MAX];

#endif /* (BLE_CENTRAL || BLE_PERIPHERAL) */
/// @} GATTMTASK
#endif // GATTM_TASK_H_
'''