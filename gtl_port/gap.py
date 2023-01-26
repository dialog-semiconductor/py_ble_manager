'''
 ****************************************************************************************
 *
 * @file gap.h
 *
 * @brief Header file - GAP.
 *
 * Copyright (C) RivieraWaves 2009-2014
 *
 *
 ****************************************************************************************
 */

/**
 ****************************************************************************************
 * @addtogroup HOST
 * @ingroup ROOT
 * @brief Bluetooth Low Energy Host
 *
 * The HOST layer of the stack contains the higher layer protocols (@ref ATT "ATT",
 * @ref SMP "SMP") and transport module (@ref L2C "L2C"). It also includes the Generic
 * Access Profile (@ref GAP "GAP"), used for scanning/connection operations.
 ****************************************************************************************
 */
/**
 ****************************************************************************************
 * @addtogroup GAP Generic Access Profile
 * @ingroup HOST
 * @brief Generic Access Profile.
 *
 * The GAP module is responsible for providing an API to the application in order to
 * configure the device in the desired mode (discoverable, connectable, etc.) and perform
 * required actions (scanning, connection, pairing, etc.). To achieve this, the GAP
 * interfaces with both the @ref SMP "SMP", @ref L2C "L2C" and the @ref CONTROLLER "CONTROLLER"
 *
 * @{
 ****************************************************************************************
 */
'''

from ctypes import Array, c_uint8, c_uint16, LittleEndianStructure, pointer, POINTER, cast
from enum import auto, IntEnum, IntFlag
from .co_bt import BD_ADDR_LEN, KEY_LEN, bd_addr


# GAP Advertising Flags
class GAP_AD_TYPE(IntEnum):

    # Flag
    GAP_AD_TYPE_FLAGS = 0x01
    # Use of more than 16 bits UUID
    GAP_AD_TYPE_MORE_16_BIT_UUID = 0x02
    # Complete list of 16 bit UUID
    GAP_AD_TYPE_COMPLETE_LIST_16_BIT_UUID = 0x03
    # Use of more than 32 bit UUD
    GAP_AD_TYPE_MORE_32_BIT_UUID = 0x04
    # Complete list of 32 bit UUID
    GAP_AD_TYPE_COMPLETE_LIST_32_BIT_UUID = 0x05
    # Use of more than 128 bit UUID
    GAP_AD_TYPE_MORE_128_BIT_UUID = 0x06
    # Complete list of 128 bit UUID
    GAP_AD_TYPE_COMPLETE_LIST_128_BIT_UUID = 0x07
    # Shortened device name
    GAP_AD_TYPE_SHORTENED_NAME = 0x08
    # Complete device name
    GAP_AD_TYPE_COMPLETE_NAME = 0x09
    # Transmit power
    GAP_AD_TYPE_TRANSMIT_POWER = 0x0A
    # Class of device
    GAP_AD_TYPE_CLASS_OF_DEVICE = 0x0D
    # Simple Pairing Hash C
    GAP_AD_TYPE_SP_HASH_C = 0x0E
    # Simple Pairing Randomizer
    GAP_AD_TYPE_SP_RANDOMIZER_R = 0x0F
    # Temporary key value
    GAP_AD_TYPE_TK_VALUE = 0x10
    # Out of Band Flag
    GAP_AD_TYPE_OOB_FLAGS = 0x11
    # Slave connection interval range
    GAP_AD_TYPE_SLAVE_CONN_INT_RANGE = 0x12
    # Require 16 bit service UUID
    GAP_AD_TYPE_RQRD_16_BIT_SVC_UUID = 0x14
    # Require 128 bit service UUID
    GAP_AD_TYPE_RQRD_128_BIT_SVC_UUID = 0x15
    # Service data 16-bit UUID
    GAP_AD_TYPE_SERVICE_16_BIT_DATA = 0x16
    # Public Target Address
    GAP_AD_TYPE_PUB_TGT_ADDR = 0x17
    # Random Target Address
    GAP_AD_TYPE_RAND_TGT_ADDR = 0x18
    # Appearance
    GAP_AD_TYPE_APPEARANCE = 0x19
    # Advertising Interval
    GAP_AD_TYPE_ADV_INTV = 0x1A
    # LE Bluetooth Device Address
    GAP_AD_TYPE_LE_BT_ADDR = 0x1B
    # LE Role
    GAP_AD_TYPE_LE_ROLE = 0x1C
    # Simple Pairing Hash C-256
    GAP_AD_TYPE_SPAIR_HASH = 0x1D
    # Simple Pairing Randomizer R-256
    GAP_AD_TYPE_SPAIR_RAND = 0x1E
    # Require 32 bit service UUID
    GAP_AD_TYPE_RQRD_32_BIT_SVC_UUID = 0x1F
    # Service data 32-bit UUID
    GAP_AD_TYPE_SERVICE_32_BIT_DATA = 0x20
    # Service data 128-bit UUID
    GAP_AD_TYPE_SERVICE_128_BIT_DATA = 0x21
    # LE Secure Connections Confirmation Value
    GAP_AD_TYPE_LE_SEC_CONN_CFM_VALUE = 0x22
    # LE Secure Connections Random Value
    GAP_AD_TYPE_LE_SEC_CONN_RAND_VALUE = 0x23
    # URI
    GAP_AD_TYPE_URI = 0x24
    # Indoor Positioning
    GAP_AD_TYPE_INDOOR_POSITIONING = 0x25
    # Transport Discovery Data
    GAP_AD_TYPE_TRANSPORT_DISC_DATA = 0x26
    # LE Supported Features
    GAP_AD_TYPE_LE_SUPP_FEATURES = 0x27
    # Channel Map Update Indication
    GAP_AD_TYPE_CHNL_MAP_UPD_IND = 0x28
    # PB-ADV
    GAP_AD_TYPE_PB_ADV = 0x29
    # Mesh Message
    GAP_AD_TYPE_MESH_MESSAGE = 0x2A
    # Mesh Beacon
    GAP_AD_TYPE_MESH_BEACON = 0x2B
    # 3D Information Data
    GAP_AD_TYPE_3D_INFO = 0x3D
    # Manufacturer specific data
    GAP_AD_TYPE_MANU_SPECIFIC_DATA = 0xFF


# Random Address type
class GAP_RND_ADDR_TYPE(IntEnum):

    # Random Static Address           - 11 (MSB->LSB)
    GAP_STATIC_ADDR = 0xC0
    # non-Resolvable Private Address  - 01 (MSB->LSB)
    GAP_NON_RSLV_ADDR = 0x00
    # Resolvable Private Address      - 01 (MSB->LSB)
    GAP_RSLV_ADDR = 0x40


# Boolean value set
class GAP_ENABLE_TYPE(IntEnum):
    # Disable
    GAP_DISABLE = 0x00
    # Enable
    GAP_ENABLE = auto()


# if (BLE_ATTS)
# GAP Attribute database handles
# Generic Access Profile Service
'''
enum
{
    GAP_IDX_PRIM_SVC
    GAP_IDX_CHAR_DEVNAME
    GAP_IDX_DEVNAME
    GAP_IDX_CHAR_ICON
    GAP_IDX_ICON
    GAP_IDX_CHAR_SLAVE_PREF_PARAM
    GAP_IDX_SLAVE_PREF_PARAM
    GAP_IDX_CHAR_CENTRAL_RPA
    GAP_IDX_CENTRAL_RPA
    /// ESR10
    GAP_IDX_CHAR_RPA_ONLY
    GAP_IDX_RPA_ONLY
    GAP_IDX_NUMBER
};


// GAP database default features
#define GAP_DB_DEFAULT_FEAT         0x001F
// GAP database features in peripheral role
#define GAP_DB_PERIPH_FEAT          0x0060

// GAP database features in central role
#define GAP_DB_CENTRAL_FEAT         0x0180
// GAP database features in for RPA Only  (ESR10)
#define GAP_DB_RPA_ONLY_FEAT        0x0600


#endif /* (BLE_ATTS)*/

'''


# GAP Role
class GAP_ROLE(IntEnum):
    # No role set yet
    GAP_ROLE_NONE = 0x00

    # Observer role
    GAP_ROLE_OBSERVER = 0x01

    # Broadcaster role
    GAP_ROLE_BROADCASTER = 0x02

    # Master/Central role
    GAP_ROLE_CENTRAL = (0x04 | GAP_ROLE_OBSERVER)

    # Peripheral/Slave role
    GAP_ROLE_PERIPHERAL = (0x08 | GAP_ROLE_BROADCASTER)

    # Device has all role both peripheral and central
    GAP_ROLE_ALL = (GAP_ROLE_CENTRAL | GAP_ROLE_PERIPHERAL)

    # if BLE_DEBUG
    # Debug mode used to force LL configuration on BLE 4.0
    GAP_ROLE_DBG_LE_4_0 = 0x80
    # endif // BLE_DEBUG


# Advertising mode
class GAP_ADV_MODE(IntEnum):
    # Mode in non-discoverable
    GAP_NON_DISCOVERABLE = 0
    # Mode in general discoverable
    GAP_GEN_DISCOVERABLE = auto()
    # Mode in limited discoverable
    GAP_LIM_DISCOVERABLE = auto()
    # Broadcaster mode which is a non discoverable and non connectable mode.
    GAP_BROADCASTER_MODE = auto()


# Scan mode
class GAP_SCAN_MODE(IntEnum):
    # Mode in general discovery
    GAP_GEN_DISCOVERY = 0
    # Mode in limited discovery
    GAP_LIM_DISCOVERY = auto()
    # Observer mode
    GAP_OBSERVER_MODE = auto()
    # Invalid mode
    GAP_INVALID_MODE = auto()


# IO Capability Values
class GAP_IO_CAP(IntEnum):
    # Display Only
    GAP_IO_CAP_DISPLAY_ONLY = 0x00
    # Display Yes No
    GAP_IO_CAP_DISPLAY_YES_NO = auto()
    # Keyboard Only
    GAP_IO_CAP_KB_ONLY = auto()
    # No Input No Output
    GAP_IO_CAP_NO_INPUT_NO_OUTPUT = auto()
    # Keyboard Display
    GAP_IO_CAP_KB_DISPLAY = auto()
    GAP_IO_CAP_LAST = auto()


# TK Type
class GAP_TK_TYPE(IntEnum):

    #  TK get from out of band method
    GAP_TK_OOB = 0x00
    # TK generated and shall be displayed by local device
    GAP_TK_DISPLAY = auto()
    # TK shall be entered by user using device keyboard
    GAP_TK_KEY_ENTRY = auto()
    # TK shall be displayed and confirmed
    GAP_TK_KEY_CONFIRM = auto()


# OOB Data Present Flag Values
class GAP_OOB(IntEnum):
    # OOB Data not present
    GAP_OOB_AUTH_DATA_NOT_PRESENT = 0x00
    # OOB data present
    GAP_OOB_AUTH_DATA_PRESENT = auto()
    GAP_OOB_AUTH_DATA_LAST = auto()


# Authentication mask
class GAP_AUTH_MASK(IntFlag):
    # No Flag set
    GAP_AUTH_NONE = 0
    # Bond authentication
    GAP_AUTH_BOND = (1 << 0)
    # Man In the middle protection
    GAP_AUTH_MITM = (1 << 2)
    # Secure Connections
    GAP_AUTH_SEC = (1 << 3)
    # Keypress Notifications
    GAP_AUTH_KEY = (1 << 4)


# define GAP_AUTH_REQ_MASK   0x1F

# Authentication Requirements
class GAP_AUTH(IntFlag):

    # No MITM No Bonding
    GAP_AUTH_REQ_NO_MITM_NO_BOND = (GAP_AUTH_MASK.GAP_AUTH_NONE)
    # No MITM Bonding
    GAP_AUTH_REQ_NO_MITM_BOND = (GAP_AUTH_MASK.GAP_AUTH_BOND)
    # MITM No Bonding
    GAP_AUTH_REQ_MITM_NO_BOND = (GAP_AUTH_MASK.GAP_AUTH_MITM)
    # MITM and Bonding
    GAP_AUTH_REQ_MITM_BOND = (GAP_AUTH_MASK.GAP_AUTH_MITM | GAP_AUTH_MASK.GAP_AUTH_BOND)
    # Secure Connection
    GAP_AUTH_REQ_SECURE_CONNECTION = (GAP_AUTH_MASK.GAP_AUTH_SEC)
    # Keypress Notification
    GAP_AUTH_REQ_KEYPRESS_NOTIFICATIONS = (GAP_AUTH_MASK.GAP_AUTH_KEY)

    GAP_AUTH_REQ_LAST = auto()


# Key Distribution Flags
class GAP_KDIST(IntFlag):

    # No Keys to distribute
    GAP_KDIST_NONE = 0x00,
    # Encryption key in distribution
    GAP_KDIST_ENCKEY = (1 << 0)
    # IRK (ID key)in distribution
    GAP_KDIST_IDKEY = (1 << 1)
    # CSRK(Signature key) in distribution
    GAP_KDIST_SIGNKEY = (1 << 2)
    # TODO add missing comment (This is from the original file, what does it mean???)
    GAP_KDIST_BR_EDR = (1 << 3)

    GAP_KDIST_LAST = (1 << 4)


# Security Defines
class GAP_SEC_REQ(IntEnum):

    # No security (no authentication and encryption)
    GAP_NO_SEC = 0x00,
    # Unauthenticated pairing with encryption
    GAP_SEC1_NOAUTH_PAIR_ENC = auto()
    # Authenticated pairing with encryption
    GAP_SEC1_AUTH_PAIR_ENC = auto()
    # Unauthenticated pairing with data signing
    GAP_SEC2_NOAUTH_DATA_SGN = auto()
    # Authentication pairing with data signing
    GAP_SEC2_AUTH_DATA_SGN = auto()
    # Authenticated LE Secure Connections pairing with encryption
    GAP_SEC1_SEC_PAIR_ENC = auto()
    # Unrecognized security
    GAP_SEC_UNDEFINED = auto()


# device name
class gap_dev_name(LittleEndianStructure):

    def __init__(self, value: Array[c_uint8] = None) -> None:
        self.value = value
        super().__init__(_value=self._value)

                # name length
    _fields_ = [("length", c_uint16),
                # name value
                ("_value", POINTER(c_uint8))]

    def get_value(self):
        return cast(self._value, POINTER(c_uint8 * self.length)).contents

    def set_value(self, new_value: Array[c_uint8]):
        self._value = new_value if new_value else pointer(c_uint8())
        self.length = len(new_value) if new_value else 1

    value = property(get_value, set_value)


# Slave preferred connection parameters
class gap_slv_pref(LittleEndianStructure):

    def __init__(self,
                 con_intv_min: c_uint16 = 0,
                 con_intv_max: c_uint16 = 0,
                 slave_latency: c_uint16 = 0,
                 conn_timeout: c_uint16 = 0):

        self.con_intv_min = con_intv_min
        self.con_intv_max = con_intv_max
        self.slave_latency = slave_latency
        self.conn_timeout = conn_timeout
        super().__init__(con_intv_min=self.con_intv_min,
                         con_intv_max=self.con_intv_max,
                         slave_latency=self.slave_latency,
                         conn_timeout=self.conn_timeout)

                # Connection interval minimum
    _fields_ = [("con_intv_min", c_uint16),
                # Connection interval maximum
                ("con_intv_max", c_uint16),
                # Slave latency
                ("slave_latency", c_uint16),
                # Connection supervision timeout multiplier
                ("conn_timeout", c_uint16)]


'''
///***** AD Type Flag - Bit set *******/
/// Limited discovery flag - AD Flag
#define GAP_LE_LIM_DISCOVERABLE_FLG             0x01
/// General discovery flag - AD Flag
#define GAP_LE_GEN_DISCOVERABLE_FLG             0x02
/// Legacy BT not supported - AD Flag
#define GAP_BR_EDR_NOT_SUPPORTED                0x04
/// Dual mode for controller supported (BR/EDR/LE) - AD Flag
#define GAP_SIMUL_BR_EDR_LE_CONTROLLER          0x08
/// Dual mode for host supported (BR/EDR/LE) - AD Flag
#define GAP_SIMUL_BR_EDR_LE_HOST                0x10

/*********** GAP Miscellaneous Defines *************/
/// Invalid connection index
#define GAP_INVALID_CONIDX                      0xFF

/// Invalid connection handle
#define GAP_INVALID_CONHDL                      0xFFFF

/// Connection interval min (N*1.250ms)
#define GAP_CNX_INTERVAL_MIN            6       //(0x06)
/// Connection interval Max (N*1.250ms)
#define GAP_CNX_INTERVAL_MAX            3200    //(0xC80)
/// Connection latency min (N*cnx evt)
#define GAP_CNX_LATENCY_MIN             0       //(0x00)
/// Connection latency Max (N*cnx evt
#define GAP_CNX_LATENCY_MAX             499     //(0x1F3)
/// Supervision TO min (N*10ms)
#define GAP_CNX_SUP_TO_MIN              10      //(0x0A)
/// Supervision TO Max (N*10ms)
#define GAP_CNX_SUP_TO_MAX              3200    //(0xC80)

/// maximum number of LECB connection per BLE link
#define GAP_LECB_CNX_MAX                rom_cfg_table[gap_lecb_cnx_max_pos] //10
'''
# *************** GAP LittleEndianStructures ********************


# Address information about a device address
class gap_bdaddr(LittleEndianStructure):
    def __init__(self,
                 addr: bd_addr = bd_addr(),
                 # TODO: NOTE 1 Was below:
                 # addr_type: GAPM_ADDR_TYPE = GAPM_ADDR_TYPE.GAPM_CFG_ADDR_PUBLIC):
                 # Changed to generic c_types to avoid moving enum into this file or creating circular ref.
                 # When creating a gap_bdaddr assure it is a GAPM_ADDR_TYPE in the file using it??? Is there a different kind of gap_bdaddr?
                 addr_type: c_uint8 = 0  # TODO is there an enum for this addr_type? 0 = public, 1 = random
                 ):
        self.addr = addr
        self.addr_type = addr_type
        super().__init__(addr=self.addr, addr_type=self.addr_type)

                # BD Address of device
    _fields_ = [("addr", bd_addr),
                # BD Address type of the device
                ("addr_type", c_uint8)]


# Generic Security key structure
class gap_sec_key(LittleEndianStructure):

    def __init__(self,
                 key: Array = (c_uint8 * KEY_LEN)()):
        assert len(key) == KEY_LEN
        self.key = key
        super().__init__(key=self.key)

                # Key value MSB -> LSB
    _fields_ = [("key", c_uint8 * KEY_LEN)]


# Resolving list device information
class gap_ral_dev_info:

    # TODO: See NOTE 1
    def __init__(self,
                 addr_type: c_uint8 = 0,
                 addr: Array = (c_uint8 * BD_ADDR_LEN)(),
                 peer_irk: Array = (c_uint8 * KEY_LEN)(),
                 local_irk: Array = (c_uint8 * KEY_LEN)()):
        assert len(addr) == BD_ADDR_LEN
        assert len(peer_irk) == KEY_LEN
        assert len(local_irk) == KEY_LEN

        self.addr_type = addr_type
        self.addr = addr
        self.peer_irk = peer_irk
        self.local_irk = local_irk
        super().__init__(addr_type=self.addr_type,
                         addr=self.addr,
                         peer_irk=self.peer_irk,
                         local_irk=self.local_irk)

                # Identity type of the device 0: Public, 1: Random Static
    _fields_ = [("addr_type", c_uint8),
                # Identity Address of the device
                ("addr", c_uint8 * BD_ADDR_LEN),
                # Peer IRK
                ("peer_irk", c_uint8 * KEY_LEN),
                # Local IRK
                ("local_irk", c_uint8 * KEY_LEN)]

# @} GAP
