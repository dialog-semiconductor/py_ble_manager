#TODO Do we need these?
#define GAPM_LE_LENGTH_EXT_OCTETS_MIN   27
#define GAPM_LE_LENGTH_EXT_OCTETS_MAX   251
#define GAPM_LE_LENGTH_EXT_TIME_MIN     328
#define GAPM_LE_LENGTH_EXT_TIME_MAX     2120
#define GAPM_IDX_MAX                                 0x01

from enum import IntEnum
from enum import auto
from dataclasses import dataclass
from ctypes import *

# GAPM states
class GAPM_STATE_ID(IntEnum):
    # Idle state - no on going operation
    GAPM_IDLE = 0
    # Busy state - Configuration operation on going
    GAPM_BUSY = auto()
    # Reset state - Reset operation on going
    GAPM_DEVICE_SETUP = auto()
    GAPM_STATE_MAX = auto()


# GAP Manager Message Interface
class GAPM_MSG_ID(IntEnum):
    # Default event 
    # Command Complete event
    GAPM_CMP_EVT = 0x0D00
    # Event triggered to inform that lower layers are ready
    GAPM_DEVICE_READY_IND = auto()

    # Default commands 
    # Reset link layer and the host command
    GAPM_RESET_CMD = auto()
    # Cancel ongoing operation
    GAPM_CANCEL_CMD = auto()

    # Device Configuration 
    # Set device configuration command
    GAPM_SET_DEV_CONFIG_CMD = auto()
    # Set device channel map
    GAPM_SET_CHANNEL_MAP_CMD = auto()

    # Local device information 
    # Get local device info command
    GAPM_GET_DEV_INFO_CMD = auto()
    # Local device version indication event
    GAPM_DEV_VERSION_IND = auto()
    # Local device BD Address indication event
    GAPM_DEV_BDADDR_IND = auto()
    # Advertising channel Tx power level
    GAPM_DEV_ADV_TX_POWER_IND = auto()
    # Indication containing information about memory usage.
    GAPM_DBG_MEM_INFO_IND = auto()

    # White List 
    # White List Management Command
    GAPM_WHITE_LIST_MGT_CMD = auto()
    # White List Size indication event
    GAPM_WHITE_LIST_SIZE_IND = auto()

    # Air Operations 
    # Set advertising mode Command
    GAPM_START_ADVERTISE_CMD = auto()
    # Update Advertising Data Command - On fly update when device is advertising
    GAPM_UPDATE_ADVERTISE_DATA_CMD = auto()

    # Set Scan mode Command
    GAPM_START_SCAN_CMD = auto()
    # Advertising or scanning report information event
    GAPM_ADV_REPORT_IND = auto()

    # Set connection initialization Command
    GAPM_START_CONNECTION_CMD = auto()
    # Name of peer device indication
    GAPM_PEER_NAME_IND = auto()
    # Confirm connection to a specific device (Connection Operation in Selective mode)
    GAPM_CONNECTION_CFM = auto()

    # Security / Encryption Toolbox 
    # Resolve address command
    GAPM_RESOLV_ADDR_CMD = auto()
    # Indicate that resolvable random address has been solved
    GAPM_ADDR_SOLVED_IND = auto()
    # Generate a random address.
    GAPM_GEN_RAND_ADDR_CMD = auto()
    # Use the AES-128 block in the controller
    GAPM_USE_ENC_BLOCK_CMD = auto()
    #  AES-128 block result indication
    GAPM_USE_ENC_BLOCK_IND = auto()
    # Generate a 8-byte random number
    GAPM_GEN_RAND_NB_CMD = auto()
    # Random Number Indication
    GAPM_GEN_RAND_NB_IND = auto()

    # Profile Management 
    # Create new task for specific profile
    GAPM_PROFILE_TASK_ADD_CMD = auto()
    # Inform that profile task has been added.
    GAPM_PROFILE_ADDED_IND = auto()

    # Indicate that a message has been received on an unknown task
    GAPM_UNKNOWN_TASK_IND = auto()

    # Suggested Default Data Length indication
    GAPM_SUGG_DFLT_DATA_LEN_IND = auto()
    # Maximum Data Length indication
    GAPM_MAX_DATA_LEN_IND = auto()

    # Resolving address list management
    GAPM_RAL_MGT_CMD = auto()
    # Resolving address list size indication
    GAPM_RAL_SIZE_IND = auto()
    # Resolving address list address indication
    GAPM_RAL_ADDR_IND = auto()

    # Internal messages for timer events = auto() not part of API*/
    # Limited discoverable timeout indication
    GAPM_LIM_DISC_TO_IND = auto()
    # Scan timeout indication
    GAPM_SCAN_TO_IND = auto()
    # Address renewal timeout indication
    GAPM_ADDR_RENEW_TO_IND = auto()
    # Message received to unknown task received
    GAPM_UNKNOWN_TASK_MSG = auto()

    # Use the DHKEY P256 block in the controller
    GAPM_USE_P256_BLOCK_CMD = auto()
    #  DHKEY P256 block result indication
    GAPM_USE_P256_BLOCK_IND = auto()

# GAP Manager operation type - application interface
class GAPM_OPERATION(IntEnum):
    # No Operation (if nothing has been requested)     */
    # ************************************************ */
    # No operation
    GAPM_NO_OP = 0x00

    # Default operations                               */
    # ************************************************ */
    # Reset BLE subsystem: LL and HL.
    GAPM_RESET = auto()
    # Cancel currently executed operation.
    GAPM_CANCEL = auto()

    # Configuration operations                         */
    # ************************************************ */
    # Set device configuration
    GAPM_SET_DEV_CONFIG = auto()
    # Set device channel map
    GAPM_SET_CHANNEL_MAP = auto()

    # Retrieve device information                      */
    # ************************************************ */
    # Get Local device version
    GAPM_GET_DEV_VERSION = auto()
    # Get Local device BD Address
    GAPM_GET_DEV_BDADDR = auto()
    # Get device advertising power level
    GAPM_GET_DEV_ADV_TX_POWER = auto()

    # Operation on White list                          */
    # ************************************************ */
    # Get White List Size.
    GAPM_GET_WLIST_SIZE = auto()
    # Add devices in white list.
    GAPM_ADD_DEV_IN_WLIST = auto()
    # Remove devices form white list.
    GAPM_RMV_DEV_FRM_WLIST = auto()
    # Clear all devices from white list.
    GAPM_CLEAR_WLIST = auto()

    # Advertise mode operations                        */
    # ************************************************ */
    # Start non connectable advertising
    GAPM_ADV_NON_CONN = auto()
    # Start undirected connectable advertising
    GAPM_ADV_UNDIRECT = auto()
    # Start directed connectable advertising
    GAPM_ADV_DIRECT = auto()
    # Start directed connectable advertising using Low Duty Cycle
    GAPM_ADV_DIRECT_LDC = auto()
    # Update on the fly advertising data
    GAPM_UPDATE_ADVERTISE_DATA = auto()

    # Scan mode operations                             */
    # ************************************************ */
    # Start active scan operation
    GAPM_SCAN_ACTIVE = auto()
    # Start passive scan operation
    GAPM_SCAN_PASSIVE = auto()

    # Connection mode operations                       */
    # ************************************************ */
    # Direct connection operation
    GAPM_CONNECTION_DIRECT = auto()
    # Automatic connection operation
    GAPM_CONNECTION_AUTO = auto()
    # Selective connection operation
    GAPM_CONNECTION_SELECTIVE = auto()
    # Name Request operation (requires to start a direct connection)
    GAPM_CONNECTION_NAME_REQUEST = auto()

    # Security / Encryption Toolbox                    */
    # ************************************************ */
    # Resolve device address
    GAPM_RESOLV_ADDR = auto()
    # Generate a random address
    GAPM_GEN_RAND_ADDR = auto()
    # Use the controller's AES-128 block
    GAPM_USE_ENC_BLOCK = auto()
    # Generate a 8-byte random number
    GAPM_GEN_RAND_NB = auto()

    # Profile Management                               */
    # ************************************************ */
    # Create new task for specific profile
    GAPM_PROFILE_TASK_ADD = auto()

    # DEBUG                                            */
    # ************************************************ */
    # Get memory usage
    GAPM_DBG_GET_MEM_INFO = auto()
    # Perform a platform reset
    GAPM_PLF_RESET = auto()

    # Set Suggested Default LE Data Length
    GAPM_SET_SUGGESTED_DFLT_LE_DATA_LEN = auto()
    # Get Suggested Default LE Data Length
    GAPM_GET_SUGGESTED_DFLT_LE_DATA_LEN = auto()
    # Get Maximum LE Data Length
    GAPM_GET_MAX_LE_DATA_LEN = auto()

    # Operation on Resolving list                          */
    # ************************************************ */
    # Get resolving address list size
    GAPM_GET_RAL_SIZE = auto()
    # Get resolving local address
    GAPM_GET_RAL_LOC_ADDR = auto()
    # Get resolving peer address
    GAPM_GET_RAL_PEER_ADDR = auto()
    # Add device in resolving address list
    GAPM_ADD_DEV_IN_RAL = auto()
    # Remove device from resolving address list
    GAPM_RMV_DEV_FRM_RAL = auto()
    # Clear resolving address list
    GAPM_CLEAR_RAL = auto()

    # Use the controller's DHKEY P256 block
    GAPM_USE_P256_BLOCK = auto()

    # Set Network Privacy Mode for peer in resolving list (ESR10)
    GAPM_NETWORK_MODE_RAL = auto()
    # Set Network Privacy Mode for peer in resolving list (ESR10)
    GAPM_DEVICE_MODE_RAL = auto()

# TODO is GAPM_KEY_RENEW different value on 531?
#if !defined (__DA14531__)
    # We wanted to add one more opcode (GAPM_KEY_RENEW) and this 
    # should go on all existing platforms. But since 690 already has
    # added one opcode here, we need some kind of sync
    GAPM_DUMMY = auto()
#endif

    # Implemented as a subcase of reset. Renews our private/public key.
    GAPM_KEY_RENEW = auto()

    # Last GAPM operation flag
    GAPM_LAST = auto()





# Device Address type Configuration
class GAPM_ADDR_TYPE(IntEnum):

    # Device Address is a Public Address
    GAPM_CFG_ADDR_PUBLIC = 0
    # Device Address is a Random Static address
    GAPM_CFG_ADDR_PRIVATE = auto()
    GAPM_CFG_ADDR_STATIC = GAPM_CFG_ADDR_PRIVATE # TODO: this is an alias, will not show as member
    # Device Address generated using Privacy feature in Host
    GAPM_CFG_ADDR_PRIVACY = auto()
    # Device Address generated using Privacy feature in Controller
    GAPM_CFG_ADDR_PRIVACY_CNTL = 0x4

'''
val = [(member.name, member.value) for member in GAPM_ADDR_TYPE]

for item in val:
    print(item[0], hex(item[1]))

'''

# Own BD address source of the device
class GAPM_OWN_ADDR(IntEnum): 
   # Public or Random Static Address according to device address configuration
   GAPM_STATIC_ADDR = 0
   # Generated Random Resolvable Private Address
   GAPM_GEN_RSLV_ADDR = auto()
   # Generated Random non-Resolvable Private Address
   GAPM_GEN_NON_RSLV_ADDR = auto()


# Device Attribute write permission requirement
class GAPM_WRITE_ATT_PERM(IntEnum):

    # Disable write access
    GAPM_WRITE_DISABLE  = 0x00
    # Enable write access
    GAPM_WRITE_ENABLE   = 0x08
    # Write access requires unauthenticated link
    GAPM_WRITE_UNAUTH   = 0x10
    # Write access requires authenticated link
    GAPM_WRITE_AUTH     = 0x18
    # Write access requires secure connection authenticated link
    # TODO: not documented in GTL doc
    #GAPM_WRITE_SECURE   = PERM(WR, SECURE)


# Attribute database configuration
#    7     6    5     4     3    2    1    0
# +-----+-----+----+-----+-----+----+----+----+
# | DBG | CoC | SC | PCP | APP_PERM |NAME_PERM|
# +-----+-----+----+-----+-----+----+----+----+
# - Bit [0-1]: Device Name write permission requirements for peer device
# - Bit [2-3]: Device Appearance write permission requirements for peer device
# - Bit [4]  : Slave Preferred Connection Parameters present
# - Bit [5]  : Service change feature present in GATT attribute database.
# - Bit [6]  : CoC zero credit bahaviour
# - Bit [7]  : Enable Debug Mode

# TODO:  Do we need gapm_att_cfg_flag
'''
enum gapm_att_cfg_flag
{
    # Device Name write permission requirements for peer device (@see gapm_write_att_perm)
    GAPM_MASK_ATT_NAME_PERM           = 0x03,
    GAPM_POS_ATT_NAME_PERM            = 0x00,
    # Device Appearance write permission requirements for peer device (@see gapm_write_att_perm)
    GAPM_MASK_ATT_APPEARENCE_PERM     = 0x0C,
    GAPM_POS_ATT_APPEARENCE_PERM      = 0x02,
    # Slave Preferred Connection Parameters present in GAP attribute database.
    GAPM_MASK_ATT_SLV_PREF_CON_PAR_EN = 0x10,
    GAPM_POS_ATT_SLV_PREF_CON_PAR_EN  = 0x04,
    # Service change feature present in GATT attribute database.
    GAPM_MASK_ATT_SVC_CHG_EN          = 0x20,
    GAPM_POS_ATT_SVC_CHG_EN           = 0x05,

    # CoC zero credit bahaviour.
    GAPM_MASK_ATT_COC_NO_CREDIT_DISCARD   = 0x40,
    GAPM_POS_ATT_COC_NO_CREDIT_DISCARD    = 0x06,

#if (BLE_DEBUG)
    # Service change feature present in GATT attribute database.
    GAPM_MASK_ATT_DBG_MODE_EN          = 0x80,
    GAPM_POS_ATT_DBG_MODE_EN           = 0x07,
#endif // (BLE_DEBUG)
};
'''

#TODO" Took these definitions from co_bt.h for now. Make a co_bt.py
BD_ADDR_LEN = 6
#BD Address structure
@dataclass
class bd_addr:
    # 6-byte array address value
    addr: c_uint8 * BD_ADDR_LEN 

LE_CHNL_MAP_LEN = 0x05
# Channel map structure
@dataclass
class le_chnl_map:
    # 5-byte channel map array
    map: c_uint8 * LE_CHNL_MAP_LEN

class le_chnl_map_struct(Structure):
    _fields_ = [("map", c_uint8 * LE_CHNL_MAP_LEN)] 

#TODO end co_bt.h


#TODO Took these definitions from gap.h for now. Make a gap.py
KEY_LEN = 0x10
# Generic Security key structure
@dataclass
class gap_sec_key:
    # Key value MSB -> LSB
    key: c_uint8 * KEY_LEN

# Address information about a device address
@dataclass
class gap_bdaddr:
    # BD Address of device
    addr: bd_addr
    # BD Address type of the device
    addr_type: c_uint8

# Resolving list device information
@dataclass
class gap_ral_dev_info:
    # Identity type of the device 0: Public, 1: Random Static
    addr_type: c_uint8
    # Identity Address of the device
    addr: c_uint8 * BD_ADDR_LEN
    # Peer IRK
    peer_irk: c_uint8 * KEY_LEN
    # Local IRK
    local_irk: c_uint8 * KEY_LEN

#TODO end gap.h

#TODO Took these definitions from rwip_config.h for now. Make a rwip_config.py
# Tasks types definition, this value shall be in [0-254] range
class KE_API_ID(IntEnum):
    # Link Layer Tasks
    TASK_ID_LLM          = 0
    TASK_ID_LLC          = 1
    TASK_ID_LLD          = 2
    TASK_ID_DBG          = 3

    # BT Controller Tasks
    TASK_ID_LM           = 4
    TASK_ID_LC           = 5
    TASK_ID_LB           = 6
    TASK_ID_LD           = 7

    TASK_ID_HCI          = 8
    TASK_ID_DISPLAY      = 9

    TASK_ID_L2CC         = 10
    TASK_ID_GATTM        = 11   # Generic Attribute Profile Manager Task
    TASK_ID_GATTC        = 12   # Generic Attribute Profile Controller Task
    TASK_ID_GAPM         = 13   # Generic Access Profile Manager
    TASK_ID_GAPC         = 14   # Generic Access Profile Controller

    TASK_ID_APP          = 15
    TASK_ID_GTL          = 16

    # -----------------------------------------------------------------------------------
    # --------------------- BLE Profile TASK API Identifiers ----------------------------
    # -----------------------------------------------------------------------------------
    TASK_ID_DISS         = 20   # Device Information Service Server Task
    TASK_ID_DISC         = 21   # Device Information Service Client Task

    TASK_ID_PROXM        = 22   # Proximity Monitor Task
    TASK_ID_PROXR        = 23   # Proximity Reporter Task

    TASK_ID_FINDL        = 24   # Find Me Locator Task
    TASK_ID_FINDT        = 25   # Find Me Target Task

    TASK_ID_HTPC         = 26   # Health Thermometer Collector Task
    TASK_ID_HTPT         = 27   # Health Thermometer Sensor Task

    TASK_ID_BLPS         = 28   # Blood Pressure Sensor Task
    TASK_ID_BLPC         = 29   # Blood Pressure Collector Task

    TASK_ID_HRPS         = 30   # Heart Rate Sensor Task
    TASK_ID_HRPC         = 31   # Heart Rate Collector Task

    TASK_ID_TIPS         = 32   # Time Server Task
    TASK_ID_TIPC         = 33   # Time Client Task

    TASK_ID_SCPPS        = 34   # Scan Parameter Profile Server Task
    TASK_ID_SCPPC        = 35   # Scan Parameter Profile Client Task

    TASK_ID_BASS         = 36   # Battery Service Server Task
    TASK_ID_BASC         = 37   # Battery Service Client Task

    TASK_ID_HOGPD        = 38   # HID Device Task
    TASK_ID_HOGPBH       = 39   # HID Boot Host Task
    TASK_ID_HOGPRH       = 40   # HID Report Host Task

    TASK_ID_GLPS         = 41   # Glucose Profile Sensor Task
    TASK_ID_GLPC         = 42   # Glucose Profile Collector Task

    TASK_ID_RSCPS        = 43   # Running Speed and Cadence Profile Server Task
    TASK_ID_RSCPC        = 44   # Running Speed and Cadence Profile Collector Task

    TASK_ID_CSCPS        = 45   # Cycling Speed and Cadence Profile Server Task
    TASK_ID_CSCPC        = 46   # Cycling Speed and Cadence Profile Client Task

    TASK_ID_ANPS         = 47   # Alert Notification Profile Server Task
    TASK_ID_ANPC         = 48   # Alert Notification Profile Client Task

    TASK_ID_PASPS        = 49   # Phone Alert Status Profile Server Task
    TASK_ID_PASPC        = 50   # Phone Alert Status Profile Client Task

    TASK_ID_CPPS         = 51   # Cycling Power Profile Server Task
    TASK_ID_CPPC         = 52   # Cycling Power Profile Client Task

    TASK_ID_LANS         = 53   # Location and Navigation Profile Server Task
    TASK_ID_LANC         = 54   # Location and Navigation Profile Client Task

    TASK_ID_BMSS         = 55   # Bond Management Service Server Task
    TASK_ID_BMSC         = 56   # Bond Management Service Client Task

    TASK_ID_BCSS         = 57   # Body Composition Server
    TASK_ID_BCSC         = 58   # Body Composition Client

    TASK_ID_UDSS         = 59   # User Data Service Server Task
    TASK_ID_UDSC         = 60   # User Data Service Client Task

    TASK_ID_WSSS         = 61   # Weight Scale Service Server Task
    TASK_ID_WSSC         = 62   # Weight Scale Service Client Task

    TASK_ID_CTSS         = 63   # Current Time Service Server Task
    TASK_ID_CTSC         = 64   # Current Time Service Client Task

    TASK_ID_ANCC         = 65   # Apple Notification Center Service Client Task

    TASK_ID_GATT_CLIENT  = 66   # Generic Attribute Profile Service Client Task

    TASK_ID_SUOTAR       = 0xFC # Software Patching Over The Air Receiver

    TASK_ID_CUSTS1       = 0xFD # Custom1 Task
    TASK_ID_CUSTS2       = 0xFE # Custom2 Task

    TASK_ID_INVALID      = 0xFF # Invalid Task Identifier

#TODO end rwip_config.h


# Operation command structure in order to keep requested operation.
@dataclass
class gapm_operation_cmd:
    # GAP request type
    operation: c_uint8


# Command complete event data structure
@dataclass
class gapm_cmp_evt:
    # GAP requested operation
    operation: c_uint8
    # Status of the request
    status: c_uint8

class gtl_struct:
    def to_bytes(self):
        message = bytearray()  
        members = self.__dict__.keys()
        fields = self.__dataclass_fields__
        for member in members:
            #message.extend(getattr(self, member)to_bytes(length=sizeof(), byteorder='little'))
            if(member != 'parameters'):
                print(sizeof(getattr(self, member)))
                #message.extend(getattr(self, member).to_bytes(length=2, byteorder='little'))
            if(member == 'parameters' and getattr(self, 'par_len') > 0):
                #param_members = self.parameters.__dict__.keys()
                #for param_member in param_members:
                #     message.extend(self.parameters.to_bytes())   
                
                
                message.extend(self.parameters.to_bytes())
                #message.extend(bytearray(self.parameters))
        
        return message
        
        
        
        members = self.__dict__.keys()



        return self.operation.to_bytes(length = 1, byteorder = 'little')

#  Reset link layer and the host command
@dataclass
class gapm_reset_cmd:
    def to_bytes(self):
        return self.operation.to_bytes(length = 1, byteorder = 'little')
    
    # GAPM requested operation:
    # - GAPM_RESET: Reset BLE subsystem: LL and HL.
    operation: c_uint8

class gapm_reset_cmd_struct(Structure):
    _fields_ = [("operation", c_uint8)] 

# Set device configuration command
@dataclass
class gapm_set_dev_config_cmd:
    # GAPM requested operation:
    #  - GAPM_SET_DEV_CONFIG: Set device configuration
    #  - GAPM_SET_SUGGESTED_DFLT_LE_DATA_LEN: Set Suggested Default LE Data Length
    operation: c_uint8
    # Device Role: Central, Peripheral, Observer, Broadcaster or All roles.
    role: c_uint8

    # -------------- Privacy Config -----------------------
    # Duration before regenerate device address when privacy is enabled.
    renew_dur: c_uint16
    # Provided own Random Static Address
    addr: bd_addr
    # Device IRK used for Random Resolvable Private Address generation (LSB first)
    irk: gap_sec_key
    # Device Address Type (@see gapm_addr_type)
    # - GAPM_CFG_ADDR_PUBLIC: Device Address is a Public Static address
    # - GAPM_CFG_ADDR_PRIVATE: Device Address is a Private Static address
    # - GAPM_CFG_ADDR_PRIVACY: Device Address generated using Privacy feature
    # - GAPM_CFG_ADDR_PRIVACY_CNTL: Device Address generated using Privacy feature in
    #                               controller
    addr_type: c_uint8

    # -------------- ATT Database Config -----------------------

    # Attribute database configuration (@see gapm_att_cfg_flag)
    #    7     6    5     4     3    2    1    0
    # +-----+-----+----+-----+-----+----+----+----+
    # | DBG | RFU | SC | PCP | APP_PERM |NAME_PERM|
    # +-----+-----+----+-----+-----+----+----+----+
    # - Bit [0-1]: Device Name write permission requirements for peer device (@see gapm_write_att_perm)
    # - Bit [2-3]: Device Appearance write permission requirements for peer device (@see gapm_write_att_perm)
    # - Bit [4]  : Slave Preferred Connection Parameters present
    # - Bit [5]  : Service change feature present in GATT attribute database.
    # - Bit [6]  : Reserved
    # - Bit [7]  : Enable Debug Mode
    att_cfg: c_uint8
    # GAP service start handle
    gap_start_hdl: c_uint16
    # GATT service start handle
    gatt_start_hdl: c_uint16
    # Maximal MTU
    max_mtu: c_uint16
    # Maximal MPS
    max_mps: c_uint16

    att_cfg: c_uint16 # Not used

    # Maximal Tx octets
    max_txoctets: c_uint16
    # Maximal Tx time
    max_txtime: c_uint16
    # Privacy 1.2 Helper
    priv1_2: c_uint8

# Set device channel map
@dataclass
class gapm_set_channel_map_cmd:
    # TODO remove
    #def test(self):
    #   members = self.__dict__.keys()
    #    for member in members:
    #        print(type(self.__dataclass_fields__[member].type))
            #print(sizeof(self.__dataclass_fields__[member].type)) # TODO does not work for chmap
    
    # GAPM requested operation:
    #  - GAPM_SET_CHANNEL_MAP: Set device channel map.
    operation: c_uint8
    # Channel map
    chmap: le_chnl_map

class gapm_set_channel_map_cmd_struct(Structure):
    _fields_ = [("operation", c_uint8),
                ("chmap", le_chnl_map_struct)] 

# Get local device info command
@dataclass
class gapm_get_dev_info_cmd:
    # GAPM requested operation:
    #  - GAPM_GET_DEV_VERSION: Get Local device version
    #  - GAPM_GET_DEV_BDADDR: Get Local device BD Address
    #  - GAPM_GET_DEV_ADV_TX_POWER: Get device advertising power level
    #  - GAPM_DBG_GET_MEM_INFO: Get memory usage (debug only)
    #  - GAPM_GET_SUGGESTED_DFLT_LE_DATA_LEN: Get Suggested Default LE Data Length
    #  - GAPM_GET_MAX_LE_DATA_LEN: Get Maximum LE Data Length
    operation: c_uint8

# Local device version indication event
@dataclass
class gapm_dev_version_ind:
    # TODO remove
    #def test(self):
    #    members = self.__dict__.keys()
    #    for member in members:
    #        print(sizeof(self.__dataclass_fields__[member].type))

    # HCI version
    hci_ver: c_uint8
    # LMP version
    lmp_ver: c_uint8
    # Host version
    host_ver: c_uint8
    # HCI revision
    hci_subver: c_uint16
    # LMP subversion
    lmp_subver: c_uint16
    # Host revision
    host_subver: c_uint16
    # Manufacturer name
    manuf_name: c_uint16

# Local device BD Address indication event
@dataclass
class gapm_dev_bdaddr_ind:
    # Local device address information
    addr: gap_bdaddr

# Advertising channel Tx power level indication event
@dataclass
class gapm_dev_adv_tx_power_ind:
    # Advertising channel Tx power level
    power_lvl: c_int8

# Cancel ongoing operation
@dataclass
class gapm_cancel_cmd:
    # GAPM requested operation
    # - GAPM_CANCEL: Cancel running operation
    operation: c_uint8

# White List Management Command
@dataclass
class gapm_white_list_mgt_cmd:
    # GAPM requested operation:
    #  - GAPM_GET_WLIST_SIZE: Get White List Size.
    #  - GAPM_ADD_DEV_IN_WLIST: Add devices in white list.
    #  - GAPM_RMV_DEV_FRM_WLIST: Remove devices form white list.
    #  - GAPM_CLEAR_WLIST: Clear all devices from white list.
    operation: c_uint8
    # Number of device information present in command
    nb: c_uint8
    # Device address information that can be used to add or remove element in device list.
    
    # TODO: this is done to malloc block of memory. How to port for Python in ctypes? 
    #struct gap_bdaddr devices[__ARRAY_EMPTY];

# White List Size indication event
@dataclass
class gapm_white_list_size_ind:
    # White List size
    size: c_uint8

# Indicates suggested default data length
@dataclass
class gapm_sugg_dflt_data_len_ind:
    # Host's suggested value for the Controller's maximum transmitted number of payload octets
    suggted_max_tx_octets: c_uint16
    # Host's suggested value for the Controller's maximum packet transmission time
    suggted_max_tx_time: c_uint16

# Indicates maximum data length
@dataclass
class gapm_max_data_len_ind:
    # Maximum number of payload octets that the local Controller supports for transmission
    suppted_max_tx_octets: c_uint16
    # Maximum time, in microseconds, that the local Controller supports for transmission
    suppted_max_tx_time: c_uint16
    # Maximum number of payload octets that the local Controller supports for reception
    suppted_max_rx_octets: c_uint16
    # Maximum time, in microseconds, that the local Controller supports for reception
    suppted_max_rx_time: c_uint16

# Resolving List Management Command
@dataclass
class gapm_rslv_list_mgt_cmd:
    # GAPM requested operation:
    #  - GAPM_GET_RAL_SIZE: Get resolving List Size.
    #  - GAPM_GET_RAL_LOC_ADDR: Get resolving list local addr
    #  - GAPM_GET_RAL_PEER_ADDR: Get resolving list peer addr
    #  - GAPM_ADD_DEV_IN_RAL: Add devices in resolving list.
    #  - GAPM_RMV_DEV_FRM_RAL: Remove devices form resolving list.
    #  - GAPM_CLEAR_RAL: Clear all devices from resolving list.
    #  - GAPM_NETWORK_MODE_RAL: Set Network Privacy Mode. (ESR10)
    #  - GAPM_DEVICE_MODE_RAL: Set Network Privacy Mode. (ESR10)
    operation: c_uint8
    # Number of device information present in command
    nb: c_uint8
    # Device address information that can be used to add or remove element in device list.
    
    # TODO: this is done to malloc block of memory. How to port for Python in ctypes? 
    # struct gap_ral_dev_info devices[__ARRAY_EMPTY];

# Resolving List Size indication event
@dataclass
class gapm_ral_size_ind:
    # Resolving List size
    size: c_uint8
    
# Resolving Address indication event
@dataclass
class gapm_ral_addr_ind:
    # Resolving List operation
    operation: c_uint8
    # Resolving List address
    addr: c_uint8 * BD_ADDR_LEN

# Resolve Address command
@dataclass
class gapm_resolv_addr_cmd:
    # GAPM requested operation:
    #  - GAPM_RESOLV_ADDR: Resolve device address
    operation: c_uint8
    # Number of provided IRK (shall be > 0)
    nb_key: c_uint8
    # Random Resolvable Private Address to solve
    addr: bd_addr
    # Array of IRK used for address resolution (MSB -> LSB)

    # TODO: this is done to malloc block of memory. How to port for Python in ctypes? 
    #struct gap_sec_key irk[__ARRAY_EMPTY];

# Indicate that resolvable random address has been solved
@dataclass
class gapm_addr_solved_ind:
    # Random Resolvable Private Address solved
    addr: bd_addr
    # IRK that correctly solved the Random Resolvable Private Address
    irk: gap_sec_key
'''
# Advertising data that contains information set by host.
struct gapm_adv_host
{
    # Advertising mode :
    # - GAP_NON_DISCOVERABLE: Non discoverable mode
    # - GAP_GEN_DISCOVERABLE: General discoverable mode
    # - GAP_LIM_DISCOVERABLE: Limited discoverable mode
    # - GAP_BROADCASTER_MODE: Broadcaster mode
    uint8_t              mode;

    # Advertising filter policy:
    # - ADV_ALLOW_SCAN_ANY_CON_ANY: Allow both scan and connection requests from anyone
    # - ADV_ALLOW_SCAN_WLST_CON_ANY: Allow both scan req from White List devices only and
    #   connection req from anyone
    # - ADV_ALLOW_SCAN_ANY_CON_WLST: Allow both scan req from anyone and connection req
    #   from White List devices only
    # - ADV_ALLOW_SCAN_WLST_CON_WLST: Allow scan and connection requests from White List
    #   devices only
    uint8_t              adv_filt_policy;

    # Advertising data length - maximum 28 bytes, 3 bytes are reserved to set
    # Advertising AD type flags, shall not be set in advertising data
    uint8_t              adv_data_len;
    # Advertising data
    uint8_t              adv_data[ADV_DATA_LEN];
    # Scan response data length- maximum 31 bytes
    uint8_t              scan_rsp_data_len;
    # Scan response data
    uint8_t              scan_rsp_data[SCAN_RSP_DATA_LEN];
    # Peer Info - bdaddr
    struct gap_bdaddr peer_info;
};

# Air operation default parameters
struct gapm_air_operation
{
    # Operation code.
    uint8_t code;

    #*
     * Own BD address source of the device:
     * - GAPM_STATIC_ADDR: Public or Random Static Address according to device address configuration
     * - GAPM_GEN_RSLV_ADDR: Generated Random Resolvable Private Address
     * - GAPM_GEN_NON_RSLV_ADDR: Generated Random non-Resolvable Private Address
     */
    uint8_t addr_src;

    # Dummy data use to retrieve internal operation state (should be set to 0).
    uint16_t state;
};


# Set advertising mode Command
struct gapm_start_advertise_cmd
{
    # GAPM requested operation:
    # - GAPM_ADV_NON_CONN: Start non connectable advertising
    # - GAPM_ADV_UNDIRECT: Start undirected connectable advertising
    # - GAPM_ADV_DIRECT: Start directed connectable advertising
    # - GAPM_ADV_DIRECT_LDC: Start directed connectable advertising using Low Duty Cycle
    struct gapm_air_operation op;

    # Minimum interval for advertising
    uint16_t             intv_min;
    # Maximum interval for advertising
    uint16_t             intv_max;

    #Advertising channel map
    uint8_t              channel_map;

    # Advertising information
    union gapm_adv_info
    {
        # Host information advertising data (GAPM_ADV_NON_CONN and GAPM_ADV_UNDIRECT)
        struct gapm_adv_host host;
        #  Direct address information (GAPM_ADV_DIRECT)
        # (used only if reconnection address isn't set or host privacy is disabled)
        struct gap_bdaddr direct;
    } info;
};


# Update Advertising Data Command - On fly update when device is advertising
struct gapm_update_advertise_data_cmd
{
    # GAPM requested operation:
    #  - GAPM_UPDATE_ADVERTISE_DATA: Update on the fly advertising data
    uint8_t  operation;
    # Advertising data length - maximum 28 bytes, 3 bytes are reserved to set
    # Advertising AD type flags, shall not be set in advertising data
    uint8_t              adv_data_len;
    # Advertising data
    uint8_t              adv_data[ADV_DATA_LEN];
    # Scan response data length- maximum 31 bytes
    uint8_t              scan_rsp_data_len;
    # Scan response data
    uint8_t              scan_rsp_data[SCAN_RSP_DATA_LEN];
};

# Set scan mode Command
struct gapm_start_scan_cmd
{
    # GAPM requested operation:
    # - GAPM_SCAN_ACTIVE: Start active scan operation
    # - GAPM_SCAN_PASSIVE: Start passive scan operation
    struct gapm_air_operation op;

    # Scan interval
    uint16_t             interval;
    # Scan window size
    uint16_t             window;

    # Scanning mode :
    # - GAP_GEN_DISCOVERY: General discovery mode
    # - GAP_LIM_DISCOVERY: Limited discovery mode
    # - GAP_OBSERVER_MODE: Observer mode
    uint8_t              mode;

    # Scan filter policy:
    # - SCAN_ALLOW_ADV_ALL: Allow advertising packets from anyone
    # - SCAN_ALLOW_ADV_WLST: Allow advertising packets from White List devices only
    uint8_t              filt_policy;
    # Scan duplicate filtering policy:
    # - SCAN_FILT_DUPLIC_DIS: Disable filtering of duplicate packets
    # - SCAN_FILT_DUPLIC_EN: Enable filtering of duplicate packets
    uint8_t              filter_duplic;
};


# Advertising or scanning report information event
struct gapm_adv_report_ind
{
    # Advertising report structure
    struct adv_report report;
};


# Set connection initialization Command
struct gapm_start_connection_cmd
{
    # GAPM requested operation:
    # - GAPM_CONNECTION_DIRECT: Direct connection operation
    # - GAPM_CONNECTION_AUTO: Automatic connection operation
    # - GAPM_CONNECTION_SELECTIVE: Selective connection operation
    # - GAPM_CONNECTION_NAME_REQUEST: Name Request operation (requires to start a direct
    #   connection)
    struct gapm_air_operation op;

    # Scan interval
    uint16_t             scan_interval;
    # Scan window size
    uint16_t             scan_window;

    # Minimum of connection interval
    uint16_t             con_intv_min;
    # Maximum of connection interval
    uint16_t             con_intv_max;
    # Connection latency
    uint16_t             con_latency;
    # Link supervision timeout
    uint16_t             superv_to;
    # Minimum CE length
    uint16_t             ce_len_min;
    # Maximum CE length
    uint16_t             ce_len_max;

    # Number of peer device information present in message.
    #  Shall be 1 for GAPM_CONNECTION_DIRECT or GAPM_CONNECTION_NAME_REQUEST operations
    #  Shall be greater than 0 for other operations
    uint8_t              nb_peers;

    # Peer device information
    struct gap_bdaddr   peers[__ARRAY_EMPTY];
};


# Name of peer device indication
struct gapm_peer_name_ind
{
    # peer device bd address
    struct bd_addr addr;
    # peer device address type 0: Public, 1: Random, 2: Public ID, 3: Static Random ID
    uint8_t addr_type;
    # peer device name length
    uint8_t name_len;
    # peer device name
    uint8_t name[__ARRAY_EMPTY];
};

# Confirm connection to a specific device (Connection Operation in Selective mode)
struct gapm_connection_cfm
{
    # peer device bd address
    struct bd_addr addr;
    # peer device address type 0: Public, 1: Random, 2: Public ID, 3: Static Random ID
    uint8_t addr_type;

    # Minimum of connection interval
    uint16_t             con_intv_min;
    # Maximum of connection interval
    uint16_t             con_intv_max;
    # Connection latency
    uint16_t             con_latency;
    # Link supervision timeout
    uint16_t             superv_to;
    # Minimum CE length
    uint16_t             ce_len_min;
    # Maximum CE length
    uint16_t             ce_len_max;
};

# Generate a random address.
struct gapm_gen_rand_addr_cmd
{
    # GAPM requested operation:
    #  - GAPM_GEN_RAND_ADDR: Generate a random address
    uint8_t  operation;
    # Dummy parameter used to store the prand part of the address
    uint8_t  prand[SMPM_RAND_ADDR_PRAND_LEN];
    # Random address type @see gap_rnd_addr_type
    #  - GAPM_STATIC_ADDR: Random Static Address
    #  - GAP_NON_RSLV_ADDR: Random non-Resolvable Private Address
    #  - GAP_RSLV_ADDR: Random Resolvable Private Address
    uint8_t rnd_type;
};

# Parameters of the @ref GAPM_USE_ENC_BLOCK_CMD message
struct gapm_use_enc_block_cmd
{
    # Command Operation Code (shall be GAPM_USE_ENC_BLOCK)
    uint8_t operation;
    # Operand 1
    uint8_t operand_1[KEY_LEN];
    # Operand 2
    uint8_t operand_2[KEY_LEN];
};

# Parameters of the @ref GAPM_USE_ENC_BLOCK_IND message
struct gapm_use_enc_block_ind
{
    # Result (16 bytes)
    uint8_t result[KEY_LEN];
};

# Parameters of the @ref GAPM_GEN_RAND_NB_CMD message
struct gapm_gen_rand_nb_cmd
{
    # Command Operation Code (shall be GAPM_GEN_RAND_NB)
    uint8_t operation;
};

# Parameters of the @ref GAPM_GEN_RAND_NB_IND message
struct gapm_gen_rand_nb_ind
{
    # Generation Random Number (8 bytes)
    struct rand_nb randnb;
};

#if (KE_PROFILING)
# Retrieve information about memory usage
struct gapm_dbg_get_mem_info_cmd
{
    # GAPM requested operation:
    #  - GAPM_DBG_GET_MEM_INFO: Get memory usage
    uint8_t operation;
};

# Indication containing information about memory usage.
struct gapm_dbg_mem_info_ind
{
    # peak of memory usage measured
    uint32_t max_mem_used;
    # memory size currently used into each heaps.
    uint16_t mem_used[KE_MEM_BLOCK_MAX];
};
#endif // (KE_PROFILING)


# Create new task for specific profile
struct gapm_profile_task_add_cmd
{
    # GAPM requested operation:
    #  - GAPM_PROFILE_TASK_ADD: Add new profile task
    uint8_t  operation;
    # Security Level :
    #  7    6    5    4    3    2    1    0
    # +----+----+----+----+----+----+----+----+
    # |     Reserved      |  AUTH   |EKS | MI |
    # +----+----+----+----+----+----+----+----+
    #
    # - MI: 1 - Application task is a Multi-Instantiated task, 0 - Mono-Instantiated
    # Only applies for service - Ignored by collectors:
    # - EKS: Service needs a 16 bytes encryption key
    # - AUTH: 0 - Disable, 1 - Enable, 2 - Unauth, 3 - Auth, 4 - Sec
    uint8_t  sec_lvl;
    # Profile task identifier
    uint16_t prf_task_id;
    # Application task number
    uint16_t app_task;
    # Service start handle
    # Only applies for services - Ignored by collectors
    # 0: dynamically allocated in Attribute database
    uint16_t start_hdl;
    # 32 bits value that contains value to initialize profile (database parameters, etc...)
    uint32_t param[__ARRAY_EMPTY];
};


# Inform that profile task has been added.
struct gapm_profile_added_ind
{
    # Profile task identifier
    uint16_t prf_task_id;
    # Profile task number allocated
    uint16_t prf_task_nb;
    # Service start handle
    # Only applies for services - Ignored by collectors
    uint16_t start_hdl;
};

# Indicate that a message has been received on an unknown task
struct gapm_unknown_task_ind
{
    # Message identifier
    uint16_t msg_id;
    # Task identifier
    uint16_t task_id;
};

# Parameters of the @ref GAPM_USE_P256_BLOCK_CMD message
struct gapm_use_p256_block_cmd
{
    # Command Operation Code (shall be GAPM_USE_P256_BLOCK)
    uint8_t operation;
    # Operand 1
    uint8_t operand_1[ECDH_KEY_LEN*2];
};

# Parameters of the @ref GAPM_USE_P256_BLOCK_IND message
struct gapm_use_p256_block_ind
{
    # Result (32 bytes)
    uint8_t result[ECDH_KEY_LEN];
};

'''


