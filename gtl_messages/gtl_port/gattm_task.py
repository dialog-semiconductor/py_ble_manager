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

'''

/**
 * Attribute Description
 */
struct gattm_att_desc
{
    /** Attribute UUID (LSB First) */
    uint8_t uuid[ATT_UUID_128_LEN];
    /**
     *  Attribute Permission (@see attm_perm_mask)
     */
    att_perm_type perm;

    /**
     *  15   14   13   12   11   10   9    8    7    6    5    4    3    2    1    0
     * +----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
     * | RI |                               MAX_LEN                                    |
     * +----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
     *
     * Bit [0-14]: Maximum Attribute Length
     * Bit [15]  : Trigger Read Indication (0 = Value present in Database,
     *                                      1 = Value not present in Database)
     *
     * For Included Services and Characteristic Declarations, this field contains targeted
     * handle.
     *
     * For Characteristic Extended Properties, this field contains 2 byte value
     *
     * Not used Client Characteristic Configuration and Server Characteristic Configuration,
     * this field is not used.
     */
    uint16_t max_len;
};

'''

# Service description
class gattm_svc_desc(Structure):
    def __init__(self, 
                 start_hdl: c_uint16 = 0,
                 task_id: c_uint16 = 0, # TODO is this a KE_API_ID?
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