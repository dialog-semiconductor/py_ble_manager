from ctypes import Array, cast, c_uint8, c_uint16, LittleEndianStructure, pointer, POINTER, Union, c_bool
from enum import auto, IntEnum

from .attm import ATTM_PERM
from .co_bt import ADV_CHANNEL_MAP, ADV_DATA_LEN, ADV_FILTER_POLICY, bd_addr, SCAN_RSP_DATA_LEN, SCAN_FILTER_POLICY, \
    SCAN_DUP_FILTER_POLICY, adv_report
from .gap import GAP_ADV_MODE, gap_bdaddr, GTL_GAP_ROLE, gap_sec_key, GAP_SCAN_MODE
from .rwble_hl_error import HOST_STACK_ERROR_CODE
from .rwip_config import KE_API_ID

GAPM_LE_LENGTH_EXT_OCTETS_MIN = 27
GAPM_LE_LENGTH_EXT_OCTETS_MAX = 251
GAPM_LE_LENGTH_EXT_TIME_MIN = 328
GAPM_LE_LENGTH_EXT_TIME_MAX = 2120
GAPM_IDX_MAX = 0x01


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
    GAPM_CMP_EVT = (KE_API_ID.TASK_ID_GAPM << 8)  # 0x0D00
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

    # Implemented as a subcase of reset. Renews our private/public key.
    GAPM_KEY_RENEW = auto()

    GAPM_SET_DEFAULT_PHY = GAPM_KEY_RENEW

    # Set Tx power
    GAPM_SET_TX_PW = auto()

    # Renew random address
    GAPM_RENEW_RAND_ADDR = auto()

    # Cancel advertising operation
    GAPM_CANCEL_ADVERTISE = auto()
    # Cancel scanning operation
    GAPM_CANCEL_SCAN = auto()
    # Cancel connection operation
    GAPM_CANCEL_CONNECTION = auto()

    # Generate a new P256 public/private key pair in the Controller
    GAPM_GEN_P256_KEY = auto()

    # Perform RF calibration
    GAPM_PERFORM_RF_CALIB = auto()

# ifdef F_PCLE
    # Set the RF path gain or loss between the RF transceiver and the antenna
    GAPM_LE_WR_RF_PATH_COMPENS = auto()
# endif // F_PCLE
# endif /* (RWBLE_SW_VERSION_MAJOR >= 9) */

    # Set the primary advertising channel permutation
    GAPM_SET_ADV_PERMUTATION = auto()

    # Last GAPM operation flag
    GAPM_LAST = auto()


# Device Address type Configuration
class GAPM_ADDR_TYPE(IntEnum):

    # Device Address is a Public Address
    GAPM_CFG_ADDR_PUBLIC = 0
    # Device Address is a Random Static address
    GAPM_CFG_ADDR_PRIVATE = auto()
    GAPM_CFG_ADDR_STATIC = GAPM_CFG_ADDR_PRIVATE  # note: this is an alias, will not show as member
    # Device Address generated using Privacy feature in Host
    GAPM_CFG_ADDR_PRIVACY = auto()
    # Device Address generated using Privacy feature in Controller
    GAPM_CFG_ADDR_PRIVACY_CNTL = 0x4


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
    GAPM_WRITE_DISABLE = 0x00
    # Enable write access
    GAPM_WRITE_ENABLE = 0x08
    # Write access requires unauthenticated link
    GAPM_WRITE_UNAUTH = 0x10
    # Write access requires authenticated link
    GAPM_WRITE_AUTH = 0x18
    # Write access requires secure connection authenticated link
    # note: secure not documented in GTL doc or in 690 SDK
    # GAPM_WRITE_SECURE   = PERM(WR, SECURE)


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
class gapm_att_cfg_flag(LittleEndianStructure):

    def __init__(self,
                 dev_name_perm: ATTM_PERM = ATTM_PERM.DISABLE,
                 dev_appear_perm: ATTM_PERM = ATTM_PERM.DISABLE,
                 slv_perf_conn_params_present: c_bool = False,
                 svc_chg_present: c_bool = False,
                 enable_debug: c_bool = False):

        self.dev_name_perm = dev_name_perm
        self.dev_appear_perm = dev_appear_perm
        self.slv_perf_conn_params_present = slv_perf_conn_params_present
        self.svc_chg_present = svc_chg_present
        self.enable_debug = enable_debug

        super().__init__(dev_name_perm=self.dev_name_perm,
                         dev_appear_perm=self.dev_appear_perm,
                         slv_perf_conn_params_present=self.slv_perf_conn_params_present,
                         svc_chg_present=self.svc_chg_present,
                         reserved=0,
                         enable_debug=self.enable_debug)

    _fields_ = [("dev_name_perm", c_uint8, 2),
                ("dev_appear_perm", c_uint8, 2),
                ("slv_perf_conn_params_present", c_uint8, 1),
                ("svc_chg_present", c_uint8, 1),
                ("reserved", c_uint8, 1),
                ("enable_debug", c_uint8, 1)]


class GAPM_ATT_CFG_FLAG(IntEnum):

    # Device Name write permission requirements for peer device (@see gapm_write_att_perm)
    GAPM_MASK_ATT_NAME_PERM = 0x03
    GAPM_POS_ATT_NAME_PERM = 0x00
    # Device Appearance write permission requirements for peer device (@see gapm_write_att_perm)
    GAPM_MASK_ATT_APPEARENCE_PERM = 0x0C
    GAPM_POS_ATT_APPEARENCE_PERM = 0x02
    # Slave Preferred Connection Parameters present in GAP attribute database.
    GAPM_MASK_ATT_SLV_PREF_CON_PAR_EN = 0x10
    GAPM_POS_ATT_SLV_PREF_CON_PAR_EN = 0x04
    # Service change feature present in GATT attribute database.
    GAPM_MASK_ATT_SVC_CHG_EN = 0x20
    GAPM_POS_ATT_SVC_CHG_EN = 0x05

    # CoC zero credit bahaviour.
    GAPM_MASK_ATT_COC_NO_CREDIT_DISCARD = 0x40
    GAPM_POS_ATT_COC_NO_CREDIT_DISCARD = 0x06

    # Service change feature present in GATT attribute database.
    GAPM_MASK_ATT_DBG_MODE_EN = 0x80
    GAPM_POS_ATT_DBG_MODE_EN = 0x07


# Operation command structure in order to keep requested operation.
class gapm_operation_cmd(LittleEndianStructure):
    def __init__(self, operation: GAPM_OPERATION = GAPM_OPERATION.GAPM_NO_OP):
        self.operation = operation
        super().__init__(operation=self.operation)

                # GAP request type
    _fields_ = [("operation", c_uint8)]


# Command complete event data structure
class gapm_cmp_evt(LittleEndianStructure):
    def __init__(self,
                 operation: GAPM_OPERATION = GAPM_OPERATION.GAPM_NO_OP,
                 status: HOST_STACK_ERROR_CODE = HOST_STACK_ERROR_CODE.GAP_ERR_NO_ERROR):
        self.operation = operation
        self.status = status
        super().__init__(operation=self.operation, status=self.status)

                # GAP requested operation
    _fields_ = [("operation", c_uint8),
                # Status of the request
                ("status", c_uint8)]


#  Reset link layer and the host command
class gapm_reset_cmd(LittleEndianStructure):
    def __init__(self, operation: GAPM_OPERATION = GAPM_OPERATION.GAPM_NO_OP):
        self.operation = operation
        super().__init__(operation=self.operation)

                # GAPM requested operation:
                # - GAPM_RESET: Reset BLE subsystem: LL and HL.
    _fields_ = [("operation", c_uint8)]


# Set device configuration command
class gapm_set_dev_config_cmd(LittleEndianStructure):
    def __init__(self,
                 operation: GAPM_OPERATION = GAPM_OPERATION.GAPM_SET_DEV_CONFIG,
                 role: GTL_GAP_ROLE = GTL_GAP_ROLE.GAP_ROLE_NONE,
                 renew_dur: c_uint16 = 0,
                 addr: bd_addr = bd_addr(),
                 irk: gap_sec_key = gap_sec_key(),
                 addr_type: GAPM_ADDR_TYPE = GAPM_ADDR_TYPE.GAPM_CFG_ADDR_PUBLIC,
                 att_cfg: gapm_att_cfg_flag = gapm_att_cfg_flag(),
                 gap_start_hdl: c_uint16 = 0,
                 gatt_start_hdl: c_uint16 = 0,
                 max_mtu: c_uint16 = 23,
                 max_mps: c_uint16 = 23,
                 att_cfg_: c_uint16 = 0,  # Not used
                 max_txoctets: c_uint16 = 27,
                 max_txtime: c_uint16 = 328,
                 priv1_2: c_uint8 = 0
                 ):

        self.operation = operation
        self.role = role
        self.renew_dur = renew_dur
        self.addr = addr
        self.irk = irk
        self.addr_type = addr_type
        self.att_cfg = att_cfg
        self.gap_start_hdl = gap_start_hdl
        self.gatt_start_hdl = gatt_start_hdl
        self.max_mtu = max_mtu
        self.max_mps = max_mps
        self.att_cfg_ = att_cfg_
        self.max_txoctets = max_txoctets
        self.max_txtime = max_txtime
        self.priv1_2 = priv1_2
        super().__init__(operation=self.operation,
                         role=self.role,
                         renew_dur=self.renew_dur,
                         addr=self.addr,
                         irk=self.irk,
                         addr_type=self.addr_type,
                         att_cfg=self.att_cfg,
                         gap_start_hdl=self.gap_start_hdl,
                         gatt_start_hdl=self.gatt_start_hdl,
                         _max_mtu=self._max_mtu,
                         _max_mps=self._max_mps,
                         att_cfg_=self.att_cfg_,
                         _max_txoctets=self._max_txoctets,
                         _max_txtime=self._max_txtime,
                         priv1_2=self.priv1_2,
                         padding=0)

                # GAPM requested operation:
                #  - GAPM_SET_DEV_CONFIG: Set device configuration
                #  - GAPM_SET_SUGGESTED_DFLT_LE_DATA_LEN: Set Suggested Default LE Data Length
    _fields_ = [("operation", c_uint8),
                # Device Role: Central, Peripheral, Observer, Broadcaster or All roles.
                ("role", c_uint8),
                # -------------- Privacy Config -----------------------
                # Duration before regenerate device address when privacy is enabled.
                ("renew_dur", c_uint16),
                # Provided own Random Static Address
                ("addr", bd_addr),
                # Device IRK used for Random Resolvable Private Address generation (LSB first)
                ("irk", gap_sec_key),
                # Device Address Type (@see gapm_addr_type)
                # - GAPM_CFG_ADDR_PUBLIC: Device Address is a Public Static address
                # - GAPM_CFG_ADDR_PRIVATE: Device Address is a Private Static address
                # - GAPM_CFG_ADDR_PRIVACY: Device Address generated using Privacy feature
                # - GAPM_CFG_ADDR_PRIVACY_CNTL: Device Address generated using Privacy feature in
                #                               controller
                ("addr_type", c_uint8),
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
                ("att_cfg", gapm_att_cfg_flag),
                # GAP service start handle
                ("gap_start_hdl", c_uint16),
                # GATT service start handle
                ("gatt_start_hdl", c_uint16),
                # Maximal MTU
                ("_max_mtu", c_uint16),
                # Maximal MPS
                ("_max_mps", c_uint16),
                # Not used
                ("att_cfg_", c_uint16),
                # Maximal Tx octets
                ("_max_txoctets", c_uint16),
                # Maximal Tx time
                ("_max_txtime", c_uint16),
                # Privacy 1.2 Helper
                ("priv1_2", c_uint8),
                # Padding
                ("padding", c_uint8)]

    def get_max_mtu(self):
        return self._max_mtu

    def set_max_mtu(self, new_mtu: c_uint16):
        if new_mtu < 23 or new_mtu > 512:
            raise ValueError("Maximum mtu must be between 23 and 512")
        self._max_mtu = new_mtu

    max_mtu = property(get_max_mtu, set_max_mtu)

    def get_max_mps(self):
        return self._max_mps

    def set_max_mps(self, new_max_mps: c_uint16):
        if new_max_mps < 23 or new_max_mps > 512:
            raise ValueError("Maximum MPS must be between 23 and 512")
        self._max_mps = new_max_mps

    max_mps = property(get_max_mps, set_max_mps)

    def get_max_txoctets(self):
        return self._max_txoctets

    def set_max_txoctets(self, new_txoctets: c_uint16):
        if new_txoctets < 27 or new_txoctets > 251:
            raise ValueError("Maximum TX octets must be between 27 and 251")
        self._max_txoctets = new_txoctets

    max_txoctets = property(get_max_txoctets, set_max_txoctets)

    def get_max_txtime(self):
        return self._max_txtime

    def set_max_txtime(self, new_txtime: c_uint16):
        if new_txtime < 328 or new_txtime > 2120:
            raise ValueError("Maximum TX time must be between 328 and 2120")
        self._max_txtime = new_txtime

    max_txtime = property(get_max_txtime, set_max_txtime)


# Get local device info command
class gapm_get_dev_info_cmd(LittleEndianStructure):
    def __init__(self, operation: GAPM_OPERATION = GAPM_OPERATION.GAPM_GET_DEV_VERSION) -> None:

        self.operation = operation
        super().__init__(operation=self.operation)

                # GAPM requested operation:
                #  - GAPM_GET_DEV_VERSION: Get Local device version
                #  - GAPM_GET_DEV_BDADDR: Get Local device BD Address
                #  - GAPM_GET_DEV_ADV_TX_POWER: Get device advertising power level
                #  - GAPM_DBG_GET_MEM_INFO: Get memory usage (debug only)
                #  - GAPM_GET_SUGGESTED_DFLT_LE_DATA_LEN: Get Suggested Default LE Data Length (valid if RWBLE_SW_VERSION_MAJOR >= 8)
                #  - GAPM_GET_MAX_LE_DATA_LEN: Get Maximum LE Data Length (valid if RWBLE_SW_VERSION_MAJOR >= 8)
    _fields_ = [("operation", c_uint8)]


# Local device version indication event
class gapm_dev_version_ind(LittleEndianStructure):
    def __init__(self,
                 hci_ver: c_uint8 = 0,
                 lmp_ver: c_uint8 = 0,
                 host_ver: c_uint8 = 0,
                 hci_subver: c_uint16 = 0,
                 lmp_subver: c_uint16 = 0,
                 host_subver: c_uint16 = 0,
                 manuf_name: c_uint16 = 0,
                 ) -> None:

        self.hci_ver = hci_ver
        self.lmp_ver = lmp_ver
        self.host_ver = host_ver
        self.hci_subver = hci_subver
        self.lmp_subver = lmp_subver
        self.host_subver = host_subver
        self.manuf_name = manuf_name
        super().__init__(hci_ver=self.hci_ver,
                         lmp_ver=self.lmp_ver,
                         host_ver=self.host_ver,
                         padding=0,
                         hci_subver=self.hci_subver,
                         lmp_subver=self.lmp_subver,
                         host_subver=self.host_subver,
                         manuf_name=self.manuf_name)

                # HCI version
    _fields_ = [("hci_ver", c_uint8),
                # LMP version
                ("lmp_ver", c_uint8),
                # Host version
                ("host_ver", c_uint8),
                ("padding", c_uint8),
                # HCI subversion
                ("hci_subver", c_uint16),
                # LMP subversion
                ("lmp_subver", c_uint16),
                # Host revision
                ("host_subver", c_uint16),
                # Manufacturer name
                ("manuf_name", c_uint16)]


# Local device BD Address indication event
class gapm_dev_bdaddr_ind(LittleEndianStructure):
    def __init__(self,
                 addr: gap_bdaddr = gap_bdaddr()
                 ) -> None:

        self.addr = addr
        super().__init__(addr=self.addr)

                # Local device address information
    _fields_ = [("addr", gap_bdaddr)]


# Cancel ongoing operation
class gapm_cancel_cmd(LittleEndianStructure):
    def __init__(self) -> None:
        self.operation = GAPM_OPERATION.GAPM_CANCEL
        super().__init__(operation=self.operation)

                # GAPM requested operation
                # - GAPM_CANCEL: Cancel running operation
    _fields_ = [("operation", c_uint8)]


class gapm_resolv_addr_cmd(LittleEndianStructure):

    def __init__(self,
                 addr: bd_addr = bd_addr(),
                 irk: Array[gap_sec_key] = None
                 ) -> None:
        self.operation = GAPM_OPERATION.GAPM_RESOLV_ADDR
        self.addr = addr
        self.irk = irk
        super().__init__(operation=self.operation,
                         nb_key=self.nb_key,
                         addr=self.addr,
                         _irk=self._irk)

                # GAPM requested operation:
                #  - GAPM_RESOLV_ADDR: Resolve device address
    _fields_ = [("operation", c_uint8),
                # Number of provided IRK (shall be > 0)
                ("nb_key", c_uint8),
                # Random Resolvable Private Address to solve
                ("addr", bd_addr),
                # Array of IRK used for address resolution (MSB -> LSB)
                ("_irk", POINTER(gap_sec_key))]

    def get_irk(self):
        return cast(self._irk, POINTER(gap_sec_key * self.nb_key)).contents

    def set_irk(self, new_keys: Array[gap_sec_key]):
        self._irk = new_keys if new_keys else (gap_sec_key * 1)()
        self.nb_key = len(new_keys) if new_keys else 1

    irk = property(get_irk, set_irk)


# Indicate that resolvable random address has been solved
class gapm_addr_solved_ind(LittleEndianStructure):

    def __init__(self,
                 addr: bd_addr = bd_addr(),
                 irk: gap_sec_key = gap_sec_key()
                 ) -> None:
        self.addr = addr
        self.irk = irk
        super().__init__(addr=self.addr,
                         irk=self.irk)

                # Random Resolvable Private Address solved
    _fields_ = [("addr", bd_addr),
                # IRK that correctly solved the Random Resolvable Private Address
                ("irk", gap_sec_key)]


# Advertising data that contains information set by host.
class gapm_adv_host(LittleEndianStructure):
    def __init__(self,
                 mode: GAP_ADV_MODE = GAP_ADV_MODE.GAP_NON_DISCOVERABLE,
                 adv_filt_policy: ADV_FILTER_POLICY = ADV_FILTER_POLICY.ADV_ALLOW_SCAN_ANY_CON_ANY,
                 adv_data_len: c_uint8 = 0,
                 adv_data: (c_uint8 * ADV_DATA_LEN) = (c_uint8 * ADV_DATA_LEN)(),
                 scan_rsp_data_len: c_uint8 = 0,
                 scan_rsp_data: (c_uint8 * SCAN_RSP_DATA_LEN) = (c_uint8 * SCAN_RSP_DATA_LEN)(),
                 peer_info: gap_bdaddr = gap_bdaddr()
                 ):

        self.mode = mode
        self.adv_filt_policy = adv_filt_policy
        self.adv_data_len = adv_data_len
        self.adv_data = adv_data
        self.scan_rsp_data_len = scan_rsp_data_len
        self.scan_rsp_data = scan_rsp_data
        self.peer_info = peer_info
        super().__init__(mode=self.mode,
                         adv_filt_policy=self.adv_filt_policy,
                         adv_data_len=self.adv_data_len,
                         adv_data=self.adv_data,
                         scan_rsp_data_len=self.scan_rsp_data_len,
                         scan_rsp_data=self.scan_rsp_data,
                         peer_info=self.peer_info)

                # Advertising mode :
                # - GAP_NON_DISCOVERABLE: Non discoverable mode
                # - GAP_GEN_DISCOVERABLE: General discoverable mode
                # - GAP_LIM_DISCOVERABLE: Limited discoverable mode
                # - GAP_BROADCASTER_MODE: Broadcaster mode
    _fields_ = [("mode", c_uint8),
                # Advertising filter policy:
                # - ADV_ALLOW_SCAN_ANY_CON_ANY: Allow both scan and connection requests from anyone
                # - ADV_ALLOW_SCAN_WLST_CON_ANY: Allow both scan req from White List devices only and
                #   connection req from anyone
                # - ADV_ALLOW_SCAN_ANY_CON_WLST: Allow both scan req from anyone and connection req
                #   from White List devices only
                # - ADV_ALLOW_SCAN_WLST_CON_WLST: Allow scan and connection requests from White List
                #   devices only
                ("adv_filt_policy", c_uint8),
                # Advertising data length - maximum 28 bytes, 3 bytes are reserved to set
                # Advertising AD type flags, shall not be set in advertising data
                ("adv_data_len", c_uint8),
                # Advertising data
                ("adv_data", c_uint8 * ADV_DATA_LEN),
                # Scan response data length- maximum 31 bytes.
                ("scan_rsp_data_len", c_uint8),
                # Scan response data
                ("scan_rsp_data", c_uint8 * SCAN_RSP_DATA_LEN),
                # Peer Info - bdaddr
                ("peer_info", gap_bdaddr)]


# Air operation default parameters
class gapm_air_operation(LittleEndianStructure):
    def __init__(self,
                 code: GAPM_OPERATION = GAPM_OPERATION.GAPM_NO_OP,
                 addr_src: GAPM_OWN_ADDR = GAPM_OWN_ADDR.GAPM_STATIC_ADDR,
                 ):
        self.code = code
        self.addr_src = addr_src
        super().__init__(code=self.code,
                         addr_src=self.addr_src,
                         state=0)

                # Operation code.
    _fields_ = [("code", c_uint8),
                # Own BD address source of the device:
                # - GAPM_STATIC_ADDR: Public or Random Static Address according to device address configuration
                # - GAPM_GEN_RSLV_ADDR: Generated Random Resolvable Private Address
                ("addr_src", c_uint8),
                # Dummy data use to retrieve internal operation state (should be set to 0).
                ("state", c_uint16)]


class gapm_adv_info(Union):
    def __init__(self,
                 host: gapm_adv_host = None,
                 direct: gap_bdaddr = None
                 ):

        if host:
            self.host = host
            super().__init__(host=self.host)
        elif direct:
            self.direct = direct
            super().__init__(direct=self.direct)
        else:
            self.host = gapm_adv_host()
            super().__init__(host=self.host)

                # Host information advertising data (GAPM_ADV_NON_CONN and GAPM_ADV_UNDIRECT)
    _fields_ = [("host", gapm_adv_host),
                #  Direct address information (GAPM_ADV_DIRECT)
                # (used only if reconnection address isn't set or host privacy is disabled)
                ("direct", gap_bdaddr)]


# Set advertising mode Command
class gapm_start_advertise_cmd(LittleEndianStructure):

    def __init__(self,
                 op: gapm_air_operation = gapm_air_operation(),
                 intv_min: c_uint16 = 0,
                 intv_max: c_uint16 = 0,
                 channel_map: ADV_CHANNEL_MAP = ADV_CHANNEL_MAP.ADV_ALL_CHNLS_EN,
                 info: gapm_adv_info = gapm_adv_info()):
        self.op = op
        self.intv_min = intv_min
        self.intv_max = intv_max
        self.channel_map = channel_map
        self.info = info
        super().__init__(op=self.op,
                         intv_min=self.intv_min,
                         intv_max=self.intv_max,
                         channel_map=self.channel_map,
                         info=self.info)

                # GAPM requested operation:
                # - GAPM_ADV_NON_CONN: Start non connectable advertising
                # - GAPM_ADV_UNDIRECT: Start undirected connectable advertising
                # - GAPM_ADV_DIRECT: Start directed connectable advertising
                # - GAPM_ADV_DIRECT_LDC: Start directed connectable advertising using Low Duty Cycle
    _fields_ = [("op", gapm_air_operation),
                # Minimum interval for advertising
                ("intv_min", c_uint16),
                # Maximum interval for advertising
                ("intv_max", c_uint16),
                # Advertising channel map
                ("channel_map", c_uint8),
                # Advertising information
                ("info", gapm_adv_info)]


# Update Advertising Data Command - On fly update when device is advertising
class gapm_update_advertise_data_cmd(LittleEndianStructure):
    def __init__(self,
                 adv_data_len: c_uint8 = 0,
                 adv_data: c_uint8 * ADV_DATA_LEN = (c_uint8 * ADV_DATA_LEN)(),
                 scan_rsp_data_len: c_uint8 = 0,
                 scan_rsp_data: c_uint8 * SCAN_RSP_DATA_LEN = (c_uint8 * SCAN_RSP_DATA_LEN)()
                 ):
        self.operation = GAPM_OPERATION.GAPM_UPDATE_ADVERTISE_DATA
        self.adv_data_len = adv_data_len
        self.adv_data = adv_data
        self.scan_rsp_data_len = scan_rsp_data_len
        self.scan_rsp_data = scan_rsp_data
        super().__init__(operation=self.operation,
                         adv_data_len=self.adv_data_len,
                         adv_data=self.adv_data,
                         scan_rsp_data_len=self.scan_rsp_data_len,
                         scan_rsp_data=self.scan_rsp_data)

                # GAPM requested operation:
                #  - GAPM_UPDATE_ADVERTISE_DATA: Update on the fly advertising data
    _fields_ = [("operation", c_uint8),
                # Advertising data length - maximum 28 bytes, 3 bytes are reserved to set
                # Advertising AD type flags, shall not be set in advertising data
                ("adv_data_len", c_uint8),
                # Advertising data
                ("adv_data", c_uint8 * ADV_DATA_LEN),
                # Scan response data length - maximum 31 bytes
                ("scan_rsp_data_len", c_uint8),
                # Scan response data
                ("scan_rsp_data", c_uint8 * SCAN_RSP_DATA_LEN)]


# Set scan mode Command
class gapm_start_scan_cmd(LittleEndianStructure):

    def __init__(self,
                 op: gapm_air_operation = gapm_air_operation(),
                 interval: c_uint16 = 0,
                 window: c_uint16 = 0,
                 mode: GAP_SCAN_MODE = GAP_SCAN_MODE.GAP_GEN_DISCOVERY,
                 filt_policy: SCAN_FILTER_POLICY = SCAN_FILTER_POLICY.SCAN_ALLOW_ADV_ALL,
                 filter_duplic: SCAN_DUP_FILTER_POLICY = SCAN_DUP_FILTER_POLICY.SCAN_FILT_DUPLIC_DIS):

        self.op = op
        self.interval = interval
        self.window = window
        self.mode = mode
        self.filt_policy = filt_policy
        self.filter_duplic = filter_duplic
        super().__init__(op=self.op,
                         interval=self.interval,
                         window=self.window,
                         mode=self.mode,
                         filt_policy=self.filt_policy,
                         filter_duplic=self.filter_duplic,
                         padding=0)

                # GAPM requested operation:
                # - GAPM_SCAN_ACTIVE: Start active scan operation
                # - GAPM_SCAN_PASSIVE: Start passive scan operation
    _fields_ = [("op", gapm_air_operation),
                # Scan interval
                ("interval", c_uint16),
                # Scan window size
                ("window", c_uint16),
                # Scanning mode :
                # - GAP_GEN_DISCOVERY: General discovery mode
                # - GAP_LIM_DISCOVERY: Limited discovery mode
                # - GAP_OBSERVER_MODE: Observer mode
                ("mode", c_uint8),
                # Scan filter policy:
                # - SCAN_ALLOW_ADV_ALL: Allow advertising packets from anyone
                # - SCAN_ALLOW_ADV_WLST: Allow advertising packets from White List devices only
                ("filt_policy", c_uint8),
                # Scan duplicate filtering policy:
                # - SCAN_FILT_DUPLIC_DIS: Disable filtering of duplicate packets
                # - SCAN_FILT_DUPLIC_EN: Enable filtering of duplicate packets
                ("filter_duplic", c_uint8),
                ("padding", c_uint8)]


# Advertising or scanning report information event
class gapm_adv_report_ind(LittleEndianStructure):
    def __init__(self, report: adv_report = adv_report()) -> None:

        self.report = report
        super().__init__(report=self.report)

                # Advertising report structure
    _fields_ = [("report", adv_report)]


# Set connection initialization Command
class gapm_start_connection_cmd(LittleEndianStructure):
    def __init__(self,
                 op: gapm_air_operation = gapm_air_operation(),
                 scan_interval: c_uint16 = 0,
                 scan_window: c_uint16 = 0,
                 con_intv_min: c_uint16 = 0,
                 con_intv_max: c_uint16 = 0,
                 con_latency: c_uint16 = 0,
                 superv_to: c_uint16 = 0,
                 ce_len_min: c_uint16 = 0,
                 ce_len_max: c_uint16 = 0,
                 peers: Array[gap_bdaddr] = None):

        self.op = op
        self.scan_interval = scan_interval
        self.scan_window = scan_window
        self.con_intv_min = con_intv_min
        self.con_intv_max = con_intv_max
        self.con_latency = con_latency
        self.superv_to = superv_to
        self.ce_len_min = ce_len_min
        self.ce_len_max = ce_len_max
        self.peers = peers
        super().__init__(op=self.op,
                         scan_interval=self.scan_interval,
                         scan_window=self.scan_window,
                         con_intv_min=self.con_intv_min,
                         con_intv_max=self.con_intv_max,
                         con_latency=self.con_latency,
                         superv_to=self.superv_to,
                         e_len_min=self.ce_len_min,
                         ce_len_max=self.ce_len_max,
                         nb_peers=self.nb_peers,
                         _peers=self._peers,
                         padding=0)

                # GAPM requested operation:
                # - GAPM_CONNECTION_DIRECT: Direct connection operation
                # - GAPM_CONNECTION_AUTO: Automatic connection operation
                # - GAPM_CONNECTION_SELECTIVE: Selective connection operation
                # - GAPM_CONNECTION_NAME_REQUEST: Name Request operation (requires to start a direct
                #   connection)
    _fields_ = [("op", gapm_air_operation),
                # Scan interval
                ("scan_interval", c_uint16),
                # Scan window size
                ("scan_window", c_uint16),
                # Minimum of connection interval
                ("con_intv_min", c_uint16),
                # Maximum of connection interval
                ("con_intv_max", c_uint16),
                # Connection latency
                ("con_latency", c_uint16),
                # Link supervision timeout
                ("superv_to", c_uint16),
                # Minimum CE length
                ("ce_len_min", c_uint16),
                # Maximum CE length
                ("ce_len_max", c_uint16),
                # Number of peer device information present in message.
                #  Shall be 1 for GAPM_CONNECTION_DIRECT or GAPM_CONNECTION_NAME_REQUEST operations
                #  Shall be greater than 0 for other operations
                ("nb_peers", c_uint8),
                # Peer device information
                ("_peers", POINTER(gap_bdaddr)),
                # Padding
                ("padding", c_uint8)]

    def get_peers(self):
        # self._atts is a pointer to gattm_att_desc (LP_gattm_att_desc)
        # here we
        # 1. cast to a pointer to an array (LP_gattm_att_desc_Array_x where x is some positive integer)
        # 2. return the contents, providing the underlying array
        return cast(self._peers, POINTER(gap_bdaddr * self.nb_peers)).contents

    def set_peers(self, value: Array[gap_bdaddr]):
        self._peers = value if value else pointer(gap_bdaddr())
        self.nb_peers = len(value) if value else 1

    peers = property(get_peers, set_peers)
