'''
#*
 ****************************************************************************************
 *
 * @file gapc_task.h
 *
 * @brief Generic Access Profile Controller Task Header.
 *
 * Copyright (C) RivieraWaves 2009-2014
 *
 ****************************************************************************************
 */
#ifndef _GAPC_TASK_H_
#define _GAPC_TASK_H_

#*
 ****************************************************************************************
 * @addtogroup GAPC_TASK Generic Access Profile Controller Task
 * @ingroup GAPC
 * @brief Handles ALL messages to/from GAP Controller block.
 *
 * It handles messages from lower and higher layers related to an ongoing connection.
 *
 * @{
 ****************************************************************************************
 */

#
 * INCLUDE FILES
 ****************************************************************************************
 */
'''
#include "rwip_config.h"
#include "ke_task.h"
#include "gap.h"
from enum import IntEnum
from enum import auto
from ctypes import *

from .rwip_config import *
from .gap import *
from .rwble_hl_error import *

'''

#if (BLE_CENTRAL || BLE_PERIPHERAL)

#
 * MACROS
 ****************************************************************************************
 */
#define GAPC_LECB_AUTH(slvl)              (slvl & 0x0003)
#define GAPC_LECB_EKS(slvl)               ((slvl >> 2) & 0x0001)

#
 * DEFINES
 ****************************************************************************************
 */

# number of GAP Controller Process
#define GAPC_IDX_MAX                                 BLE_CONNECTION_MAX

# Operation type
enum gapc_op_type
{
    # Operation used to manage Link (update params, get peer info)
    GAPC_OP_LINK_INFO    = 0x00,

    # Operation used to manage SMP
    GAPC_OP_SMP          = 0x01,

    # Operation used to manage Link Layer update (connection parameters or PHY)
    GAPC_OP_LINK_UPD     = 0x02,

#if defined (__DA14531__)
    # Operation used to manage L2CAP connection parameters update
    GAPC_OP_L2C_UPD      = 0x03,
#endif

    # Max number of operations
    GAPC_OP_MAX
};

# states of GAP Controller task
enum gapc_state_id
{
    # Connection ready state
    GAPC_READY,

    # Link Operation on-going
    GAPC_LINK_INFO_BUSY     = (1 << GAPC_OP_LINK_INFO),
    # SMP Operation  on-going
    GAPC_SMP_BUSY           = (1 << GAPC_OP_SMP),
    # Link Layer Update Operation on-going
    GAPC_LINK_UPD_BUSY      = (1 << GAPC_OP_LINK_UPD),
#if defined (__DA14531__)
    # L2CAP Connection Parameters Update Operation on-going
    GAPC_L2C_UPD_BUSY       = (1 << GAPC_OP_L2C_UPD),
    # SMP start encryption on-going
    GAPC_ENCRYPT_BUSY       = (1 << GAPC_OP_MAX),

    # Disconnection  on-going
    GAPC_DISC_BUSY          = 0x3F,
    # Free state
    GAPC_FREE               = 0X7F,
#else
    # SMP start encryption on-going
    GAPC_ENCRYPT_BUSY       = (1 << GAPC_OP_MAX),

    # Disconnection  on-going
    GAPC_DISC_BUSY          = 0x1F,
    # Free state
    GAPC_FREE               = 0X3F,
#endif
    # Number of defined states.
    GAPC_STATE_MAX
};
'''

# GAP Controller Task messages
class GAPC_MSG_ID(IntEnum):
    # Default event */
    # Command Complete event
    GAPC_CMP_EVT = (KE_API_ID.TASK_ID_GAPC << 8) #0x0E00

    # Connection state information */
    # Indicate that a connection has been established
    GAPC_CONNECTION_REQ_IND = auto()
    # Set specific link data configuration.
    GAPC_CONNECTION_CFM = auto()

    # Indicate that a link has been disconnected
    GAPC_DISCONNECT_IND = auto()

    # Link management command */
    # Request disconnection of current link command.
    GAPC_DISCONNECT_CMD = auto()

    # Peer device info */
    # Retrieve information command
    GAPC_GET_INFO_CMD = auto()
    # Peer device attribute DB info such as Device Name, Appearance or Slave Preferred Parameters
    GAPC_PEER_ATT_INFO_IND = auto()
    # Indication of peer version info
    GAPC_PEER_VERSION_IND = auto()
    # Indication of peer features info
    GAPC_PEER_FEATURES_IND = auto()
    # Indication of ongoing connection RSSI
    GAPC_CON_RSSI_IND = auto()

    # Device Name Management */
    # Peer device request local device info such as name, appearance or slave preferred parameters
    GAPC_GET_DEV_INFO_REQ_IND = auto()
    # Send requested info to peer device
    GAPC_GET_DEV_INFO_CFM = auto()
    # Peer device request to modify local device info such as name or appearance
    GAPC_SET_DEV_INFO_REQ_IND = auto()
    # Local device accept or reject device info modification
    GAPC_SET_DEV_INFO_CFM = auto()

    # Connection parameters update */
    # Perform update of connection parameters command
    GAPC_PARAM_UPDATE_CMD = auto()
    # Request of updating connection parameters indication
    GAPC_PARAM_UPDATE_REQ_IND = auto()
    # Master confirm or not that parameters proposed by slave are accepted or not
    GAPC_PARAM_UPDATE_CFM = auto()
    # Connection parameters updated indication
    GAPC_PARAM_UPDATED_IND = auto()

    # Bonding procedure */
    # Start Bonding command procedure
    GAPC_BOND_CMD = auto()
    # Bonding requested by peer device indication message.
    GAPC_BOND_REQ_IND = auto()
    # Confirm requested bond information.
    GAPC_BOND_CFM = auto()
    # Bonding information indication message
    GAPC_BOND_IND = auto()

    # Encryption procedure */
    # Start Encryption command procedure
    GAPC_ENCRYPT_CMD = auto()
    # Encryption requested by peer device indication message.
    GAPC_ENCRYPT_REQ_IND = auto()
    # Confirm requested Encryption information.
    GAPC_ENCRYPT_CFM = auto()
    # Encryption information indication message
    GAPC_ENCRYPT_IND = auto()

    # Security request procedure */
    # Start Security Request command procedure
    GAPC_SECURITY_CMD = auto()
    # Security requested by peer device indication message
    GAPC_SECURITY_IND = auto()

    # Signature procedure */
    # Indicate the current sign counters to the application
    GAPC_SIGN_COUNTER_IND = auto()

    # Device information */
    # Indication of ongoing connection Channel Map
    GAPC_CON_CHANNEL_MAP_IND = auto()

    # LE Credit Based */
    # LE credit based link creation
    GAPC_LECB_CREATE_CMD = auto()
    # LE credit based link destruction
    GAPC_LECB_DESTROY_CMD = auto()
    # LE credit based connection request
    GAPC_LECB_CONNECT_CMD = auto()
    # LE credit based connection request indication
    GAPC_LECB_CONNECT_REQ_IND = auto()
    # LE credit based connection indication
    GAPC_LECB_CONNECT_IND = auto()
    # LE credit based connection request confirmation
    GAPC_LECB_CONNECT_CFM = auto()
    # LE credit based credit addition
    GAPC_LECB_ADD_CMD = auto()
    # LE credit based credit addition indication
    GAPC_LECB_ADD_IND = auto()
    # disconnect request
    GAPC_LECB_DISCONNECT_CMD = auto()
    # disconnect indication
    GAPC_LECB_DISCONNECT_IND = auto()

    # LE Ping */
    # Update LE Ping timeout value
    GAPC_SET_LE_PING_TO_CMD = auto()
    # LE Ping timeout indication
    GAPC_LE_PING_TO_VAL_IND = auto()
    # LE Ping timeout expires indication
    GAPC_LE_PING_TO_IND = auto()

    # LE Data Length extension */
    # LE Set Data Length Command
    GAPC_SET_LE_PKT_SIZE_CMD = auto()
    # LE Set Data Length Indication
    GAPC_LE_PKT_SIZE_IND = auto()

    # ---------------------- INTERNAL API ------------------------
    # Internal messages for timer events, not part of API*/
    # Signature procedure
    GAPC_SIGN_CMD = auto()
    # Signature result
    GAPC_SIGN_IND = auto()

    # Parameter update procedure timeout indication
    GAPC_PARAM_UPDATE_TO_IND = auto()
    # Pairing procedure timeout indication
    GAPC_SMP_TIMEOUT_TIMER_IND = auto()
    # Pairing repeated attempts procedure timeout indication
    GAPC_SMP_REP_ATTEMPTS_TIMER_IND = auto()
    # Connection procedure timeout indication
    GAPC_LECB_CONN_TO_IND = auto()
    # Disconnection procedure timeout indication
    GAPC_LECB_DISCONN_TO_IND = auto()

    # Peer device sent a keypress notification
    GAPC_KEYPRESS_NOTIFICATION = auto()
    GAPC_KEYPRESS_NOTIFICATION_CMD = GAPC_KEYPRESS_NOTIFICATION
    GAPC_KEYPRESS_NOTIFICATION_IND = GAPC_KEYPRESS_NOTIFICATION


# request operation type - application interface
class GAPC_OPERATION(IntEnum):

    #                 Operation Flags                  */
    # No Operation (if nothing has been requested)     */
    # ************************************************ */
    # No operation
    GAPC_NO_OP                                    = 0x00

    # Connection management */
    # Disconnect link
    GAPC_DISCONNECT = auto()

    # Connection information */
    # Retrieve name of peer device.
    GAPC_GET_PEER_NAME = auto()
    # Retrieve peer device version info.
    GAPC_GET_PEER_VERSION = auto()
    # Retrieve peer device features.
    GAPC_GET_PEER_FEATURES = auto()
    # Get Peer device appearance
    GAPC_GET_PEER_APPEARANCE = auto()
    # Get Peer device Slaved Preferred Parameters
    GAPC_GET_PEER_SLV_PREF_PARAMS = auto()
    # Retrieve connection RSSI.
    GAPC_GET_CON_RSSI = auto()
    # Retrieve Connection Channel MAP.
    GAPC_GET_CON_CHANNEL_MAP = auto()

    # Connection parameters update */
    # Perform update of connection parameters.
    GAPC_UPDATE_PARAMS = auto()

    # Security procedures */
    # Start bonding procedure.
    GAPC_BOND = auto()
    # Start encryption procedure.
    GAPC_ENCRYPT = auto()
    # Start security request procedure
    GAPC_SECURITY_REQ = auto()

    # LE Credit Based*/
    # LE credit based connection creation
    GAPC_LE_CB_CREATE = auto()
    # LE credit based connection destruction
    GAPC_LE_CB_DESTROY = auto()
    # LE credit based connection request
    GAPC_LE_CB_CONNECTION = auto()
    # LE credit based disconnection request
    GAPC_LE_CB_DISCONNECTION = auto()
    # LE credit addition request
    GAPC_LE_CB_ADDITION = auto()

    # LE Ping*/
    # get timer timeout value
    GAPC_GET_LE_PING_TO = auto()
    # set timer timeout value
    GAPC_SET_LE_PING_TO = auto()

    #  LE Set Data Length
    GAPC_SET_LE_PKT_SIZE = auto()

    # Get Peer device central address resolution
    GAPC_GET_PEER_CENTRAL_RPA = auto()
#ESR10
    # Get Peer Resolvable Private Address only
    GAPC_GET_PEER_RPA_ONLY = auto()

    # ---------------------- INTERNAL API ------------------------
    # Packet signature */
    # sign an attribute packet
    GAPC_SIGN_PACKET = auto()
    # Verify signature or an attribute packet
    GAPC_SIGN_CHECK = auto()

    # Last GAPC operation flag
    GAPC_LAST = auto()

# Bond event type.
class GAPC_BOND(IntEnum):
    # Bond Pairing request
    GAPC_PAIRING_REQ = 0x00
    # Respond to Pairing request
    GAPC_PAIRING_RSP = auto()

    # Pairing Finished information
    GAPC_PAIRING_SUCCEED = auto()
    # Pairing Failed information
    GAPC_PAIRING_FAILED = auto()

    # Used to retrieve pairing Temporary Key
    GAPC_TK_EXCH = auto()
    # Used for Identity Resolving Key exchange
    GAPC_IRK_EXCH = auto()
    # Used for Connection Signature Resolving Key exchange
    GAPC_CSRK_EXCH = auto()
    # Used for Long Term Key exchange
    GAPC_LTK_EXCH = auto()

    # Bond Pairing request issue, Repeated attempt
    GAPC_REPEATED_ATTEMPT = auto()

'''
# List of device info that should be provided by application
enum gapc_dev_info
{
    # Device Name
    GAPC_DEV_NAME,
    # Device Appearance Icon
    GAPC_DEV_APPEARANCE,
    # Device Slave preferred parameters
    GAPC_DEV_SLV_PREF_PARAMS,
    # Device Central Address Resolution parameters
    GAPC_DEV_CENTRAL_RPA,
//ESR10
    # Device Resolvable Private Address Only parameters
    GAPC_DEV_RPA_ONLY,
    # maximum device info parameter
    GAPC_DEV_INFO_MAX,
};

# List of features available on a device
enum gapc_features_list
{
    # LE encryption
    GAPC_ENCRYPT_FEAT_MASK              = (1 << 0),
    # Connection Parameters Request Procedure
    GAPC_CONN_PARAM_REQ_FEAT_MASK       = (1 << 1),
    # Extended Reject Indication
    GAPC_EXT_REJECT_IND_FEAT_MASK       = (1 << 2),
    # Slave-intiated Features Exchange
    GAPC_SLAVE_FEAT_EXCH_FEAT_MASK      = (1 << 3),
    # LE ping
    GAPC_LE_PING_FEAT_MASK              = (1 << 4)
};

#
 * TYPE DEFINITIONS
 ****************************************************************************************
 */

# Operation command structure in order to keep requested operation.
struct gapc_operation_cmd
{
    # GAP request type
    uint8_t operation;
};
'''

# Command complete event data structure
class gapc_cmp_evt(Structure):

    def __init__(self, 
                     operation: GAPC_OPERATION = GAPC_OPERATION.GAPC_NO_OP,
                     status: HOST_STACK_ERROR_CODE = HOST_STACK_ERROR_CODE.GAP_ERR_NO_ERROR):
                 
        self.operation = operation
        self.status = status
        super().__init__(operation=self.operation,
                         status=self.status)

                # GAP request type
    _fields_ = [("operation", c_uint8),
                # Status of the request
                ("status", c_uint8)]
    
# Indicate that a connection has been established
class gapc_connection_req_ind(Structure):
    def __init__(self, 
                 conhdl: c_uint16 = 0,
                 con_interval: c_uint16 = 0,
                 con_latency: c_uint16 = 0,
                 sup_to: c_uint16 = 0,
                 clk_accuracy: c_uint8 = 0,
                 peer_addr_type: c_uint8 = 0, 
                 peer_addr: bd_addr = bd_addr((c_uint8*BD_ADDR_LEN)())):
                 
        self.conhdl = conhdl
        self.con_interval = con_interval
        self.con_latency = con_latency
        self.sup_to = sup_to
        self.clk_accuracy = clk_accuracy
        self.peer_addr_type = peer_addr_type
        self.peer_addr = peer_addr
        super().__init__(conhdl=self.conhdl,
                         con_interval=self.con_interval,
                         con_latency=self.con_latency,
                         sup_to=self.sup_to,
                         clk_accuracy=self.clk_accuracy,
                         peer_addr_type=self.peer_addr_type,
                         peer_addr=self.peer_addr)

                # Connection handle
    _fields_ = [("conhdl", c_uint16),
                # Connection interval
                ("con_interval", c_uint16),
                # Connection latency
                ("con_latency", c_uint16),
                # Link supervision timeout
                ("sup_to", c_uint16),
                # Clock accuracy
                ("clk_accuracy", c_uint8),
                # Peer address type 0: Public, 1: Random, 2: Public ID, 3: Static Random ID
                ("peer_addr_type", c_uint8),
                # Peer BT address
                ("peer_addr", bd_addr)]


# Set specific link data configuration.
class gapc_connection_cfm(Structure):
    def __init__(self, 
                 lcsrk: gap_sec_key = gap_sec_key(), 
                 lsign_counter: c_uint32 = 0,
                 rcsrk: gap_sec_key = gap_sec_key(),
                 rsign_counter: c_uint32 = 0,
                 auth: GAP_AUTH = GAP_AUTH.GAP_AUTH_REQ_NO_MITM_NO_BOND,
                 svc_changed_ind_enable: c_uint8 = 0):

        self.lcsrk = lcsrk
        self.lsign_counter = lsign_counter
        self.rcsrk = rcsrk
        self.rsign_counter = rsign_counter
        self.auth = auth
        self.svc_changed_ind_enable = svc_changed_ind_enable
        super().__init__(lcsrk=self.lcsrk,
                         lsign_counter=self.lsign_counter,
                         rcsrk=self.rcsrk,
                         rsign_counter=self.rsign_counter,
                         auth=self.auth,
                         svc_changed_ind_enable=self.svc_changed_ind_enable,
                         padding=0)

                # Local CSRK value
    _fields_ = [("lcsrk", gap_sec_key),
                # Local signature counter value
                ("lsign_counter", c_uint32),
                # Remote CSRK value
                ("rcsrk", gap_sec_key),
                # Remote signature counter value
                ("rsign_counter", c_uint32),
                # Authentication (@see gap_auth)
                ("auth", c_uint8),
                # Service Changed Indication enabled
                ("svc_changed_ind_enable", c_uint8),
                # Padding
                ("padding", c_uint16)]   

'''

# Request disconnection of current link command.
struct gapc_disconnect_cmd
{
    # GAP request type:
    # - GAPC_DISCONNECT: Disconnect link.
    uint8_t operation;

    # Reason of disconnection
    uint8_t reason;
};


# Indicate that a link has been disconnected
struct gapc_disconnect_ind
{
    # Connection handle
    uint16_t conhdl;
    # Reason of disconnection
    uint8_t reason;
};
'''

# Retrieve information command
class gapc_get_info_cmd(Structure):

    def __init__(self, 
                 operation: GAPC_OPERATION = GAPC_OPERATION.GAPC_NO_OP):

        self.operation = operation
        super().__init__(operation=self.operation)

                # GAP request type:
                # - GAPC_GET_PEER_NAME: Retrieve name of peer device.
                # - GAPC_GET_PEER_VERSION: Retrieve peer device version info.
                # - GAPC_GET_PEER_FEATURES: Retrieve peer device features.
                # - GAPC_GET_CON_RSSI: Retrieve connection RSSI.
                # - GAPC_GET_CON_CHANNEL_MAP: Retrieve Connection Channel MAP.
                # - GAPC_GET_PEER_APPEARANCE: Get Peer device appearance
                # - GAPC_GET_PEER_SLV_PREF_PARAMS: Get Peer device Slaved Preferred Parameters
                # - GAPC_GET_LE_PING_TIMEOUT: Retrieve LE Ping Timeout Value
    _fields_ = [("operation", c_uint8)]   

'''
# device information data
union gapc_dev_info_val
{
    # Device name
    struct gap_dev_name name;
    # Appearance Icon
    uint16_t appearance;
    # Slave preferred parameters
    struct gap_slv_pref slv_params;
    # Central Address Resolution
    uint8_t central_rpa;
//ESR10
    # Resolvable Private Address Only
    uint8_t rpa_only;
};

# Peer device attribute DB info such as Device Name, Appearance or Slave Preferred Parameters
struct gapc_peer_att_info_ind
{
    # Requested information
    # - GAPC_DEV_NAME: Device Name
    # - GAPC_DEV_APPEARANCE: Device Appearance Icon
    # - GAPC_DEV_SLV_PREF_PARAMS: Device Slave preferred parameters
    # - GAPC_DEV_CENTRAL_RPA: Device Central Address Resolution
//ESR10
    # - GAPC_DEV_RPA_ONLY: Device Resolvable Private Address Only
    uint8_t  req;
    # Attribute handle
    uint16_t handle;

    # device information data
    union gapc_dev_info_val info;
};

# Indication of peer version info
struct gapc_peer_version_ind
{
    # Manufacturer name
    uint16_t compid;
    # LMP subversion
    uint16_t lmp_subvers;
    # LMP version
    uint8_t  lmp_vers;
};
'''

# Indication of peer features info
class gapc_peer_features_ind(Structure):

    def __init__(self, 
                 features: Array = (c_uint8*LE_FEATS_LEN)()):

        self.features = features
        super().__init__(features=self.features)

                # 8-byte array for LE features
    _fields_ = [("features", c_uint8*LE_FEATS_LEN)]   



'''



# Indication of ongoing connection RSSI
struct gapc_con_rssi_ind
{
    # RSSI value
    uint8_t rssi;
};
# Indication of ongoing connection Channel Map
struct gapc_con_channel_map_ind
{
    # channel map value
    struct le_chnl_map ch_map;
};

# Sign counter value changed due to packet signing or signature verification.
struct gapc_sign_counter_updated_ind
{
    # New Local signature counter value
    uint32_t lsign_counter;
    # New Remote signature counter value
    uint32_t rsign_counter;
};

# Indication of LE Ping
struct gapc_le_ping_to_val_ind
{
    #Authenticated payload timeout
    uint16_t     timeout;
};


# Peer device request local device info such as name, appearance or slave preferred parameters
struct gapc_get_dev_info_req_ind
{
    # Requested information
    # - GAPC_DEV_NAME: Device Name
    # - GAPC_DEV_APPEARANCE: Device Appearance Icon
    # - GAPC_DEV_SLV_PREF_PARAMS: Device Slave preferred parameters
    # - GAPC_DEV_CENTRAL_RPA: Device Central Address Resolution
    # - GAPC_DEV_RPA_ONLY: Device Resolvable Private Address Only
    uint8_t req;
};



# Send requested info to peer device
struct gapc_get_dev_info_cfm
{
    # Requested information
    # - GAPC_DEV_NAME: Device Name
    # - GAPC_DEV_APPEARANCE: Device Appearance Icon
    # - GAPC_DEV_SLV_PREF_PARAMS: Device Slave preferred parameters
    # - GAPC_DEV_CENTRAL_RPA: Device Central Address Resolution
    # - GAPC_DEV_RPA_ONLY: Device Resolvable Private Address Only
    uint8_t req;

    # Peer device information data
    union gapc_dev_info_val info;
};

# Peer device request to modify local device info such as name or appearance
struct gapc_set_dev_info_req_ind
{
    # Requested information
    # - GAPC_DEV_NAME: Device Name
    # - GAPC_DEV_APPEARANCE: Device Appearance Icon
    uint8_t req;

    # device information data
    union gapc_set_dev_info
    {
        # Device name
        struct gap_dev_name name;
        # Appearance Icon
        uint16_t appearance;
    } info;
};

# Local device accept or reject device info modification
struct gapc_set_dev_info_cfm
{
    # Requested information
    # - GAPC_DEV_NAME: Device Name
    # - GAPC_DEV_APPEARANCE: Device Appearance Icon
    uint8_t req;

    # Status code used to know if requested has been accepted or not
    uint8_t status;
};

# Connection Parameter used to update connection parameters
struct gapc_conn_param
{
    # Connection interval minimum
    uint16_t intv_min;
    # Connection interval maximum
    uint16_t intv_max;
    # Latency
    uint16_t latency;
    # Supervision timeout
    uint16_t time_out;
};

# Perform update of connection parameters command
struct gapc_param_update_cmd
{
    # GAP request type:
    # - GAPC_UPDATE_PARAMS: Perform update of connection parameters.
    uint8_t operation;
    # Internal parameter used to manage internally l2cap packet identifier for signaling
    uint8_t pkt_id;
    # Connection interval minimum
    uint16_t intv_min;
    # Connection interval maximum
    uint16_t intv_max;
    # Latency
    uint16_t latency;
    # Supervision timeout
    uint16_t time_out;
    # Minimum Connection Event Duration
    uint16_t ce_len_min;
    # Maximum Connection Event Duration
    uint16_t ce_len_max;
};

# Request of updating connection parameters indication
struct gapc_param_update_req_ind
{
    # Connection interval minimum
    uint16_t intv_min;
    # Connection interval maximum
    uint16_t intv_max;
    # Latency
    uint16_t latency;
    # Supervision timeout
    uint16_t time_out;
};

# Connection parameters updated indication
struct gapc_param_updated_ind
{
    #Connection interval value
    uint16_t            con_interval;
    #Connection latency value
    uint16_t            con_latency;
    #Supervision timeout
    uint16_t            sup_to;
};

# Master confirm or not that parameters proposed by slave are accepted or not
struct gapc_param_update_cfm
{
    # True to accept slave connection parameters, False else.
    bool accept;
    # Minimum Connection Event Duration
    uint16_t ce_len_min;
    # Maximum Connection Event Duration
    uint16_t ce_len_max;
};
'''
# Pairing parameters
class gapc_pairing(Structure):
    def __init__(self, 
                 iocap: GAP_IO_CAP = GAP_IO_CAP.GAP_IO_CAP_DISPLAY_ONLY,
                 oob: GAP_OOB = GAP_OOB.GAP_OOB_AUTH_DATA_NOT_PRESENT,
                 auth: GAP_AUTH = GAP_AUTH.GAP_AUTH_REQ_NO_MITM_NO_BOND,
                 key_size: c_uint8 = 16,
                 ikey_dist: GAP_KDIST = GAP_KDIST.GAP_KDIST_NONE,
                 rkey_dist: GAP_KDIST = GAP_KDIST.GAP_KDIST_NONE,
                 sec_req: GAP_SEC_REQ = GAP_SEC_REQ.GAP_NO_SEC):

        self.iocap = iocap
        self.oob = oob
        self.auth = auth
        self.key_size = key_size
        self.ikey_dist = ikey_dist
        self.rkey_dist = rkey_dist
        self.sec_req = sec_req
        super().__init__(iocap=self.iocap,
                         oob=self.oob,
                         auth=self.auth,
                         key_size=self.key_size,
                         ikey_dist=self.ikey_dist,
                         rkey_dist=self.rkey_dist,
                         sec_req=self.sec_req)

                # IO capabilities (@see gap_io_cap)
    _fields_ = [("iocap", c_uint8),
                # OOB information (@see gap_oob)
                ("oob", c_uint8),
                # Authentication (@see gap_auth)
                ("auth", c_uint8),
                # Encryption key size (7 to 16)
                ("key_size", c_uint8),
                #Initiator key distribution (@see gap_kdist)
                ("ikey_dist", c_uint8),
                #Responder key distribution (@see gap_kdist)
                ("rkey_dist", c_uint8),
                # Device security requirements (minimum security level). (@see gap_sec_req)
                ("sec_req", c_uint8)]  


# Long Term Key information
class gapc_ltk(Structure):

    def __init__(self, 
                 ltk: gap_sec_key = gap_sec_key(),
                 ediv: c_uint16 = 0,
                 randnb: rand_nb = rand_nb(),
                 key_size: c_uint8 = 16):

        self.ltk = ltk
        self.ediv = ediv
        self.randnb = randnb
        self.key_size = key_size
        super().__init__(ltk=self.ltk,
                         ediv=self.ediv,
                         randnb=self.randnb,
                         key_size=self.key_size)

                # Long Term Key
    _fields_ = [("ltk", gap_sec_key),
                # Encryption Diversifier
                ("ediv", c_uint16),
                # Random Number)
                ("randnb", rand_nb),
                # Encryption key size (7 to 16)
                ("key_size", c_uint8)]  

'''
# Identity Resolving Key information
struct gapc_irk
{
    # Identity Resolving Key
    struct gap_sec_key irk;
    # Device BD Address
    struct gap_bdaddr addr;
};


# Start Bonding command procedure
struct gapc_bond_cmd
{
    # GAP request type:
    # - GAPC_BOND:  Start bonding procedure.
    uint8_t operation;
    # Pairing information
    struct gapc_pairing pairing;
};
'''
# Bond procedure requested information data
class gapc_bond_req_data(Union):

    def __init__(self, 
                 auth_req: GAP_AUTH = None,
                 key_size: c_uint8 = None,
                 tk_type: GAP_TK_TYPE = None):

        if auth_req:
            self.auth_req = auth_req
            super().__init__(auth_req=self.auth_req)
        elif key_size:
            self.key_size = key_size
            super().__init__(key_size=self.key_size)
        elif tk_type:
            self.tk_type = tk_type
            super().__init__(tk_type=self.tk_type)
        else:
            self.auth_req = 0
            super().__init__(auth_req=self.auth_req)

                # Authentication level (@see gap_auth) (if request = GAPC_PAIRING_REQ)
    _fields_ = [("auth_req", c_uint8),
                # LTK Key Size (if request = GAPC_LTK_EXCH)
                ("key_size", c_uint8),
                # Device IO used to get TK: (if request = GAPC_TK_EXCH)
                #  - GAP_TK_OOB:       TK get from out of band method
                #  - GAP_TK_DISPLAY:   TK generated and shall be displayed by local device
                #  - GAP_TK_KEY_ENTRY: TK shall be entered by user using device keyboard
                #  - GAP_TK_KEY_CONFIRM: TK shall be displayed and confirmed
                ("tk_type", c_uint8)]  

# Bonding requested by peer device indication message.
class gapc_bond_req_ind(Structure):

    def __init__(self, 
                 request: GAPC_BOND = GAPC_BOND.GAPC_PAIRING_REQ,
                 data: gapc_bond_req_data = gapc_bond_req_data(),
                 tk: gap_sec_key = gap_sec_key()):

        self.request = request
        self.data = data
        self.tk = tk
        super().__init__(request=self.request,
                         data=self.data,
                         tk=self.tk)

                # Bond request type (@see gapc_bond)
    _fields_ = [("request", c_uint8),
                # Bond procedure requested information data
                ("data", gapc_bond_req_data),
                ("tk", gap_sec_key)]

# Bond procedure information data
class gapc_bond_cfm_data(Union):

    def __init__(self, 
                 pairing_feat: gapc_pairing = None,
                 ltk: gapc_ltk = None,
                 csrk: gap_sec_key = None,
                 tk: gap_sec_key = None):

        if pairing_feat:
            self.pairing_feat = pairing_feat
            super().__init__(pairing_feat=self.pairing_feat)
        elif ltk:
            self.ltk = ltk
            super().__init__(ltk=self.ltk)
        elif csrk:
            self.csrk = csrk
            super().__init__(csrk=self.csrk)
        elif tk:
            self.tk = tk
            super().__init__(tk=self.tk)
        else:
            self.pairing_feat = gapc_pairing()
            super().__init__(pairing_feat=self.pairing_feat)

                # Pairing Features (request = GAPC_PAIRING_RSP)
    _fields_ = [("pairing_feat", gapc_pairing),
                # LTK (request = GAPC_LTK_EXCH)
                ("ltk", gapc_ltk),
                # CSRK (request = GAPC_CSRK_EXCH)
                ("csrk", gap_sec_key),
                # TK (request = GAPC_TK_EXCH)
                ("tk", gap_sec_key)]  

# Confirm requested bond information.
class gapc_bond_cfm(Structure):

    def __init__(self, 
                 request: GAPC_BOND = GAPC_BOND.GAPC_PAIRING_RSP,
                 accept: c_uint8 = 0,
                 data: gapc_bond_cfm_data = gapc_bond_cfm_data()):

        self.request = request
        self.accept = accept
        self.data = data
        super().__init__(request=self.request,
                         accept=self.accept,
                         data=self.data)

                # Bond request type (@see gapc_bond)
    _fields_ = [("request", c_uint8),
                # Request accepted
                ("accept", c_uint8),
                # Bond procedure information data
                ("data", gapc_bond_cfm_data)]


'''
# Bonding information indication message
struct gapc_bond_ind
{
    # Bond information type (@see gapc_bond)
    uint8_t info;

    # Bond procedure information data
    union gapc_bond_data
    {
        # Authentication information (@see gap_auth)
        # (if info = GAPC_PAIRING_SUCCEED)
        uint8_t auth;
        # Pairing failed reason  (if info = GAPC_PAIRING_FAILED)
        uint8_t reason;
        # Long Term Key information (if info = GAPC_LTK_EXCH)
        struct gapc_ltk ltk;
        # Identity Resolving Key information (if info = GAPC_IRK_EXCH)
        struct gapc_irk irk;
        # Connection Signature Resolving Key information (if info = GAPC_CSRK_EXCH)
        struct gap_sec_key csrk;
    } data;
};

# Start Encryption command procedure
struct gapc_encrypt_cmd
{
    # GAP request type:
    # - GAPC_ENCRYPT:  Start encryption procedure.
    uint8_t operation;
    # Long Term Key information
    struct gapc_ltk ltk;
};

# Encryption requested by peer device indication message.
struct gapc_encrypt_req_ind
{
    # Encryption Diversifier
    uint16_t ediv;
    # Random Number
    struct rand_nb rand_nb;
};

# Confirm requested Encryption information.
struct gapc_encrypt_cfm
{
    # Indicate if a LTK has been found for the peer device
    uint8_t found;
    # Long Term Key
    struct gap_sec_key ltk;
    # LTK Key Size
    uint8_t key_size;
};

# Encryption information indication message
struct gapc_encrypt_ind
{
    # Authentication  level (@see gap_auth)
    uint8_t auth;
};
'''

# Start Security Request command procedure
class gapc_security_cmd(Structure):
    def __init__(self, 
                  operation: GAPC_OPERATION = GAPC_OPERATION.GAPC_NO_OP,
                  auth: c_uint16 = GAP_AUTH.GAP_AUTH_REQ_SECURE_CONNECTION,
                 ):
                 
        self.operation = operation
        self.auth = auth
        super().__init__(operation=self.operation,
                         auth=self.auth)

                # GAP request type:
                # - GAPC_SECURITY_REQ: Start security request procedure
    _fields_ = [("operation", c_uint8),
                # Authentication level (@see gap_auth)
                ("auth", c_uint8)]


    

'''
# Security requested by peer device indication message
struct gapc_security_ind
{
    # Authentification level (@see gap_auth)
    uint8_t auth;
};
# Keypress notification message
struct gapc_keypress_notification
{
    uint8_t type;
};

# Parameters of the @ref GAPC_SIGN_COUNTER_IND message
struct gapc_sign_counter_ind
{
    # Local SignCounter value
    uint32_t local_sign_counter;
    # Peer SignCounter value
    uint32_t peer_sign_counter;
};


# Parameters of the @ref GAPC_SIGN_CMD message
struct gapc_sign_cmd
{
    # GAP request type:
    # - GAPC_SIGN_PACKET: Sign an attribute packet
    # - GAPC_SIGN_CHECK:  Verify signature or an attribute packet
    uint8_t operation;
    # Data PDU length (Bytes)
    uint16_t byte_len;
    # Data PDU + SignCounter if generation, Data PDU + SignCounter + MAC if verification
    uint8_t msg[__ARRAY_EMPTY];
};

# Parameters of the @ref GAPC_SIGN_IND message
struct gapc_sign_ind
{
    # GAP request type:
    # - GAPC_SIGN_PACKET: Sign an attribute packet
    # - GAPC_SIGN_CHECK:  Verify signature or an attribute packet
    uint8_t operation;
    # Data PDU length (Bytes)
    uint16_t byte_len;
    # Data PDU + SignCounter + MAC
    uint8_t signed_msg[__ARRAY_EMPTY];
};

# Parameters of the @ref GAPC_LECB_CREATE_CMD message
struct gapc_lecb_create_cmd
{
    # GAP request type:
    # - GAPC_LE_CB_CREATE: Allocate credit based structure
    uint8_t operation;
    # Security level
    uint16_t sec_lvl;
    # LE Protocol/Service Multiplexer
    uint16_t le_psm;
    # Channel identifier
    uint16_t cid;
    # Credit allocated for the LE Credit Based Connection
    uint16_t intial_credit;
};

# Parameters of the @ref GAPC_LECB_DESTROY_CMD message
struct gapc_lecb_destroy_cmd
{
    # GAP request type:
    # - GAPC_LE_CB_DESTROY: Destroy allocated credit based structure
    uint8_t operation;
    # LE Protocol/Service Multiplexer
    uint16_t le_psm;
};

# Parameters of the @ref GAPC_LECB_CONNECT_CMD message
struct gapc_lecb_connect_cmd
{
    # GAP request type:
    # - GAPC_LE_CB_CON: LE credit connection
    uint8_t operation;
    # Internal parameter used to manage internally l2cap packet identifier
    uint8_t pkt_id;
    # LE Protocol/Service Multiplexer
    uint16_t le_psm;
    # Channel identifier
    uint16_t cid;
    # Credit allocated for the LE Credit Based Connection
    uint16_t credit;
};

# Parameters of the @ref GAPC_LECB_CONNECT_CFM message
struct gapc_lecb_connect_cfm
{
    # LE Protocol/Service Multiplexer
    uint16_t le_psm;
    # Status
    uint16_t status;
};

# Parameters of the @ref GAPC_LECB_CONNECT_IND message
struct gapc_lecb_connect_ind
{
    # LE Protocol/Service Multiplexer
    uint16_t le_psm;
    # Destination Credit for the LE Credit Based Connection
    uint16_t dest_credit;
    # Maximum SDU size
    uint16_t max_sdu;
    # Destination CID
    uint16_t dest_cid;
};

# Parameters of the @ref GAPC_LECB_CONNECT_REQ_IND message
struct gapc_lecb_connect_req_ind
{
    # LE Protocol/Service Multiplexer
    uint16_t le_psm;
    # Destination Credit for the LE Credit Based Connection
    uint16_t dest_credit;
    # Maximum SDU size
    uint16_t max_sdu;
    # Destination CID
    uint16_t dest_cid;
};


# Parameters of the @ref GAPC_LECB_DISCONNECT_CMD message
struct gapc_lecb_disconnect_cmd
{
    # GAP request type:
    # - GAPC_LE_CB_DIS: LE credit disconnection
    uint8_t operation;
    # Internal parameter used to manage internally l2cap packet identifier
    uint8_t pkt_id;
    # LE Protocol/Service Multiplexer
    uint16_t le_psm;
};

# Parameters of the @ref GAPC_LECB_DISCONNECT_IND message
struct gapc_lecb_disconnect_ind
{
    # LE Protocol/Service Multiplexer
    uint16_t le_psm;
    # Reason
    uint16_t reason;
};

# Parameters of the @ref GAPC_LECB_ADD_CMD message
struct gapc_lecb_add_cmd
{
    # GAP request type:
    # - GAPC_LE_CB_ADD: LE credit addition
    uint8_t operation;
    # Internal parameter used to manage internally l2cap packet identifier for signaling
    uint8_t pkt_id;
    # LE Protocol/Service Multiplexer
    uint16_t le_psm;
    # Destination Credit for the LE Credit Based Connection
    uint16_t credit;
};

# Parameters of the @ref GAPC_LECB_ADD_IND message
struct gapc_lecb_add_ind
{
    # LE Protocol/Service Multiplexer
    uint16_t le_psm;
    # Source Credit for the LE Credit Based Connection
    uint16_t src_credit;
    # Destination Credit for the LE Credit Based Connection
    uint16_t dest_credit;
};


# Parameters of the @ref GAPC_SET_LE_PING_TO_CMD message
struct gapc_set_le_ping_to_cmd
{
    # GAP request type:
    # - GAPC_SET_LE_PING_TO : Set the LE Ping timeout value
    uint8_t      operation;
    # Authenticated payload timeout
    uint16_t     timeout;
};

# Parameters of the @ref GAPC_SET_LE_PKT_SIZE_CMD message
struct gapc_set_le_pkt_size_cmd
{
    # GAP request type:
    # - GAPC_SET_LE_PKT_SIZE : Set the LE Data length value
    uint8_t operation;
    # Preferred maximum number of payload octets that the local Controller should include
    # in a single Link Layer Data Channel PDU.
    uint16_t tx_octets;
    # Preferred maximum number of microseconds that the local Controller should use to transmit
    # a single Link Layer Data Channel PDU
    uint16_t tx_time;
};
    
# Parameters of the @ref GAPC_LE_PKT_SIZE_IND message
struct gapc_le_pkt_size_ind
{
    # The maximum number of payload octets in TX
    uint16_t max_tx_octets;
    # The maximum time that the local Controller will take to TX
    uint16_t max_tx_time;
    # The maximum number of payload octets in RX
    uint16_t max_rx_octets;
    # The maximum time that the local Controller will take to RX
    uint16_t max_rx_time;
};

#
 * MACROS
 ****************************************************************************************
 */


#
 * GLOBAL VARIABLE DECLARATIONS
 ****************************************************************************************
 */

#
 * FUNCTION DECLARATIONS
 ****************************************************************************************
 */
int gapc_process_op(uint8_t conidx, uint8_t op_type, void* op_msg, enum gapc_operation* supp_ops);

#
 * TASK DESCRIPTOR DECLARATIONS
 ****************************************************************************************
 */
extern const struct ke_state_handler gapc_default_handler;
extern ke_state_t gapc_state[GAPC_IDX_MAX];

#endif // (BLE_CENTRAL || BLE_PERIPHERAL)

# @} GAPC_TASK

#endif # _GAPC_TASK_H_ */
'''