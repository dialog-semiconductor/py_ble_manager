'''
#*
 ****************************************************************************************
 *
 * @file gattc_task.h
 *
 * @brief Header file - GATTCTASK.
 *
 * Copyright (C) RivieraWaves 2009-2014
 *
 *
 ****************************************************************************************


#ifndef GATTC_TASK_H_
#define GATTC_TASK_H_

#*
 ****************************************************************************************
 * @addtogroup GATTCTASK Task
 * @ingroup GATTC
 * @brief Handles ALL messages to/from GATT Controller block.
 *
 * The GATTCTASK is responsible for managing the messages coming from
 * the attribute layer and host-level layers for dedicated connection.
 * The task includes services and characteristic discovery, configuration exchanges
 * and attribute value access operations (reading, writing, notification and indication).
 *
 * Messages may originate from @ref ATTC "ATTC", @ref ATTS "ATTS", @ref GAP "GAP"
 * and Application.
 *
 * @{
 ****************************************************************************************

#
 * INCLUDE FILES
 ****************************************************************************************

#include "rwip_config.h"
#if (BLE_CENTRAL || BLE_PERIPHERAL)
#include "attm.h"
#include "gatt.h"
#include "co_utils.h"
'''

from ctypes import Array, cast, c_bool, c_uint8, c_uint16, LittleEndianStructure, memmove, pointer, POINTER, Union
from enum import auto, IntEnum

from .att import ATT_CHAR_PROP, ATT_UUID_128_LEN
from .rwble_hl_error import HOST_STACK_ERROR_CODE
from .rwip_config import KE_API_ID

'''

#
 * DEFINES
 ****************************************************************************************


# number of GATT Controller Process
#define GATTC_IDX_MAX                                 BLE_CONNECTION_MAX

#if defined (__DA14531__)
# PDU Opcode Command Flag - indicates that ATT PDU is a Command and NOT a Request
#define CMD_FLAG
#endif

# Operation type
enum gattc_op_type
{
    #if (BLE_ATTS)
    # Operation used to Server Request operations
    GATTC_OP_SERVER,
    #endif // (BLE_ATTS)

    #if (BLE_ATTC)
    # Operation used to Client Request operations
    GATTC_OP_CLIENT,
    # Service Discovery Procedure operation
    GATTC_OP_SDP,
    #endif // (BLE_ATTC)

    # Max number of operations
    GATTC_OP_MAX
};


# states of GATT Controller task
enum gattc_state_id
{
    # Connection ready state
    GATTC_READY = 0,
    #if (BLE_ATTC)
    # Client operation on-going
    GATTC_CLIENT_BUSY       = (1 << GATTC_OP_CLIENT),
    # Service Discovery Procedure operation on-going
    GATTC_SDP_BUSY          = (1 << GATTC_OP_SDP),
    #endif // (BLE_ATTC)
    #if (BLE_ATTS)
    # Server operation on-going
    GATTC_SERVER_BUSY       = (1 << GATTC_OP_SERVER),
    GATTC_ATTS_BUSY         = (1 << GATTC_OP_MAX),
    #endif // (BLE_ATTS)
    # Connection started but ATTS not ready
    GATTC_CONNECTED         = (1 << (GATTC_OP_MAX + 1)),

    # Free state
    GATTC_FREE              = (1 << (GATTC_OP_MAX + 2)),
    # Number of defined states.
    GATTC_STATE_MAX
};
'''


# GATT Task messages
class GATTC_MSG_ID(IntEnum):

    # Default event
    # Command Complete event
    GATTC_CMP_EVT = (KE_API_ID.TASK_ID_GATTC << 8)  # 0C00

    # ATTRIBUTE CLIENT
    # Server configuration request
    GATTC_EXC_MTU_CMD = auto()
    # Indicate that the ATT MTU has been updated (negotiated)
    GATTC_MTU_CHANGED_IND = auto()

    # Discover All Services
    # Discover Services by Service UUID
    # Find Included Services
    # Discover Characteristics by UUID
    # Discover All Characteristics of a Service
    # Discover All Characteristic Descriptors
    # Discovery command
    GATTC_DISC_CMD = auto()
    # GATT -> HL: Events to Upper layer
    # Discover All Services
    # Discovery services indication
    GATTC_DISC_SVC_IND = auto()
    # Find Included Services
    # Discover included services indication
    GATTC_DISC_SVC_INCL_IND = auto()
    # Discover All Characteristics of a Service
    # Discover characteristic indication
    GATTC_DISC_CHAR_IND = auto()
    # Discover All Characteristic Descriptors
    # Discovery characteristic descriptor indication
    GATTC_DISC_CHAR_DESC_IND = auto()

    # Read Value
    # Read Using UUID
    # Read Long Value
    # Read Multiple Values
    # Read command
    GATTC_READ_CMD = auto()
    # Read response
    GATTC_READ_IND = auto()

    # Write without response
    # Write without response with Authentication
    # Write Characteristic Value
    # Signed Write Characteristic Value
    # Write Long Characteristic Value
    # Characteristic Value Reliable Write
    # Write Characteristic Descriptors
    # Write Long Characteristic Descriptors
    # Characteristic Value Reliable Write
    # Write command request
    GATTC_WRITE_CMD = auto()

    # Cancel / Execute pending write operations
    # Execute write characteristic request
    GATTC_EXECUTE_WRITE_CMD = auto()

    # Reception of an indication or notification from peer device.
    # peer device triggers an event (notification)
    GATTC_EVENT_IND = auto()
    # peer device triggers an event that requires a confirmation (indication)
    GATTC_EVENT_REQ_IND = auto()
    # Confirm reception of event (trigger a confirmation message)
    GATTC_EVENT_CFM = auto()

    # Registration to peer device events (Indication/Notification).
    GATTC_REG_TO_PEER_EVT_CMD = auto()

    # -------------------------- ATTRIBUTE SERVER ------------------------------- \
    # Notify Characteristic
    # Indicate Characteristic
    # send an event to peer device
    GATTC_SEND_EVT_CMD = auto()

    # Service Changed Characteristic Indication
    # *
    # * Send a Service Changed indication to a device
    # * (message structure is struct gattc_send_svc_changed_cmd)

    GATTC_SEND_SVC_CHANGED_CMD = auto()
    # *
    # * Inform the application when sending of Service Changed indications has been
    # * enabled or disabled

    GATTC_SVC_CHANGED_CFG_IND = auto()

    # Indicate that read operation is requested.
    # Read command indicated to upper layers.
    GATTC_READ_REQ_IND = auto()
    # REad command confirmation from upper layers.
    GATTC_READ_CFM = auto()

    # Indicate that write operation is requested.
    # Write command indicated to upper layers.
    GATTC_WRITE_REQ_IND = auto()
    # Write command confirmation from upper layers.
    GATTC_WRITE_CFM = auto()

    # Indicate that write operation is requested.
    # Request Attribute info to upper layer - could be trigger during prepare write
    GATTC_ATT_INFO_REQ_IND = auto()
    # Attribute info from upper layer confirmation
    GATTC_ATT_INFO_CFM = auto()

    # ----------------------- SERVICE DISCOVERY PROCEDURE  ---------------------------
    # Service Discovery command
    GATTC_SDP_SVC_DISC_CMD = auto()
    # Service Discovery indicate that a service has been found.
    GATTC_SDP_SVC_IND = auto()

    # -------------------------- TRANSACTION ERROR EVENT -----------------------------
    # Transaction Timeout Error Event no more transaction will be accepted
    GATTC_TRANSACTION_TO_ERROR_IND = auto()

    # ------------------------------- Internal API -----------------------------------
    # Client Response timeout indication
    GATTC_CLIENT_RTX_IND = auto()
    # Server indication confirmation timeout indication
    GATTC_SERVER_RTX_IND = auto()


# request operation type - application interface
class GATTC_OPERATION(IntEnum):

    #              Attribute Client Flags
    # No Operation (if nothing has been requested)
    # ************************************************
    # No operation
    GATTC_NO_OP = 0x00,

    # Operation flags for MTU Exchange
    # ************************************************
    # Perform MTU exchange
    GATTC_MTU_EXCH = auto()

    #      Operation flags for discovery operation
    # ************************************************
    # Discover all services
    GATTC_DISC_ALL_SVC = auto()
    # Discover services by UUID
    GATTC_DISC_BY_UUID_SVC = auto()
    # Discover included services
    GATTC_DISC_INCLUDED_SVC = auto()
    # Discover all characteristics
    GATTC_DISC_ALL_CHAR = auto()
    # Discover characteristic by UUID
    GATTC_DISC_BY_UUID_CHAR = auto()
    # Discover characteristic descriptor
    GATTC_DISC_DESC_CHAR = auto()

    # Operation flags for reading attributes
    # ************************************************
    # Read attribute
    GATTC_READ = auto()
    # Read long attribute
    GATTC_READ_LONG = auto()
    # Read attribute by UUID
    GATTC_READ_BY_UUID = auto()
    # Read multiple attribute
    GATTC_READ_MULTIPLE = auto()

    # Operation flags for writing/modifying attributes
    # ************************************************
    # Write attribute
    GATTC_WRITE = auto()
    # Write no response
    GATTC_WRITE_NO_RESPONSE = auto()
    # Write signed
    GATTC_WRITE_SIGNED = auto()
    # Execute write
    GATTC_EXEC_WRITE = auto()

    # Operation flags for registering to peer device
    # events
    # ************************************************
    # Register to peer device events
    GATTC_REGISTER = auto()
    # Unregister from peer device events
    GATTC_UNREGISTER = auto()

    # Operation flags for sending events to peer device
    # ************************************************
    # Send an attribute notification
    GATTC_NOTIFY = auto()
    # Send an attribute indication
    GATTC_INDICATE = auto()
    # Send a service changed indication
    GATTC_SVC_CHANGED = auto()

    # Service Discovery Procedure
    # ************************************************
    # Search specific service
    GATTC_SDP_DISC_SVC = auto()
    # Search for all services
    GATTC_SDP_DISC_SVC_ALL = auto()
    # Cancel Service Discovery Procedure
    GATTC_SDP_DISC_CANCEL = auto()

    # Last GATT flag
    GATTC_LAST = auto()


# Servic Discovery Attribute type
class GATTC_SDP_ATT_TYPE(IntEnum):
    # No Attribute Information
    GATTC_SDP_NONE = 0
    # Included Service Information
    GATTC_SDP_INC_SVC = auto()
    # Characteristic Declaration
    GATTC_SDP_ATT_CHAR = auto()
    # Attribute Value
    GATTC_SDP_ATT_VAL = auto()
    # Attribute Descriptor
    GATTC_SDP_ATT_DESC = auto()


'''
# Command complete event data structure
struct gattc_op_cmd
{
    # GATT request type
    uint8_t operation;
    # operation sequence number
    uint16_t seq_num;
};
'''


# Command complete event data structure
class gattc_cmp_evt(LittleEndianStructure):

    def __init__(self,
                 operation: GATTC_OPERATION = GATTC_OPERATION.GATTC_NO_OP,
                 status: HOST_STACK_ERROR_CODE = HOST_STACK_ERROR_CODE.ATT_ERR_NO_ERROR,
                 seq_num: c_uint16 = 0):

        self.operation = operation
        self.status = status
        self.seq_num = seq_num
        super().__init__(operation=self.operation,
                         status=self.status,
                         seq_num=self.seq_num)

                # GATT request type
    _fields_ = [("operation", c_uint8),
                # Status of the request
                ("status", c_uint8),
                # operation sequence number - provided when operation is started
                ("seq_num", c_uint16)]


# Service Discovery Command LittleEndianStructure
class gattc_exc_mtu_cmd(LittleEndianStructure):

    def __init__(self,
                 operation: GATTC_OPERATION = GATTC_OPERATION.GATTC_NO_OP,
                 seq_num: c_uint16 = 0):

        self.operation = operation
        self.seq_num = seq_num
        super().__init__(operation=self.operation,
                         padding=0,
                         seq_num=self.seq_num)

                # GATT request type
    _fields_ = [("operation", c_uint8),
                ("padding", c_uint8),
                # operation sequence number
                ("seq_num", c_uint16)]


# Indicate that the ATT MTU has been updated (negotiated)
class gattc_mtu_changed_ind(LittleEndianStructure):

    def __init__(self,
                 mtu: c_uint16 = 0,
                 seq_num: c_uint16 = 0):

        self.mtu = mtu
        self.seq_num = seq_num
        super().__init__(_mtu=self._mtu,
                         seq_num=self.seq_num)

                # Exchanged MTU value
    _fields_ = [("_mtu", c_uint16),
                # operation sequence number
                ("seq_num", c_uint16)]

    def get_mtu(self):
        return self._mtu

    def set_mtu(self, new_mtu: c_uint16):
        if new_mtu > 512:
            raise ValueError("Maximum mtu is 512")
        self._mtu = new_mtu

    mtu = property(get_mtu, set_mtu)


# Service Discovery Command
class gattc_disc_cmd(LittleEndianStructure):

    def __init__(self,
                 operation: GATTC_OPERATION = GATTC_OPERATION.GATTC_NO_OP,
                 seq_num: c_uint16 = 0,
                 start_hdl: c_uint16 = 0,
                 end_hdl: c_uint16 = 0,
                 uuid: Array[c_uint8] = None):

        self.operation = operation
        self.seq_num = seq_num
        self.start_hdl = start_hdl
        self.end_hdl = end_hdl
        self.uuid = uuid if uuid else (c_uint8 * 2)(0, 0)
        super().__init__(operation=self.operation,
                         uuid_len=self.uuid_len,
                         seq_num=self.seq_num,
                         start_hdl=self.start_hdl,
                         end_hdl=self.end_hdl,
                         _uuid=self._uuid)

                # GATT request type
    _fields_ = [("operation", c_uint8),
                # UUID length
                ("uuid_len", c_uint8),
                # operation sequence number
                ("seq_num", c_uint16),
                # start handle range
                ("start_hdl", c_uint16),
                # end handle range
                ("end_hdl", c_uint16),
                # UUID
                ("_uuid", POINTER(c_uint8))]

    def get_uuid(self):
        return cast(self._uuid, POINTER(c_uint8 * self.uuid_len)).contents

    def set_uuid(self, new_uuid: Array[c_uint8]):
        if len(new_uuid) == 2 or len(new_uuid) == 16:
            self._uuid = new_uuid
            self.uuid_len = len(new_uuid)
        else:
            raise ValueError("UUID length must be 2 or 16")

    uuid = property(get_uuid, set_uuid)


# Discover Service indication LittleEndianStructure
class gattc_disc_svc_ind(LittleEndianStructure):

    def __init__(self,
                 start_hdl: c_uint16 = 0,
                 end_hdl: c_uint16 = 0,
                 uuid: Array[c_uint8] = None):

        self.start_hdl = start_hdl
        self.end_hdl = end_hdl
        self.uuid = uuid if uuid else (c_uint8 * 2)(0, 0)
        super().__init__(start_hdl=self.start_hdl,
                         end_hdl=self.end_hdl,
                         uuid_len=self.uuid_len,
                         _uuid=self._uuid,
                         padding=0)

                # start handle
    _fields_ = [("start_hdl", c_uint16),
                # end handle
                ("end_hdl", c_uint16),
                # UUID length
                ("uuid_len", c_uint8),
                # UUID
                ("_uuid", POINTER(c_uint8)),
                ("padding", c_uint8)]

    def get_uuid(self):
        return cast(self._uuid, POINTER(c_uint8 * self.uuid_len)).contents

    def set_uuid(self, new_uuid: Array[c_uint8]):
        if len(new_uuid) == 2 or len(new_uuid) == 16:
            self._uuid = new_uuid
            self.uuid_len = len(new_uuid)
        else:
            raise ValueError("UUID length must be 2 or 16")

    uuid = property(get_uuid, set_uuid)


# Discover Service indication LittleEndianStructure
class gattc_disc_svc_incl_ind(LittleEndianStructure):

    def __init__(self,
                 attr_hdl: c_uint16 = 0,
                 start_hdl: c_uint16 = 0,
                 end_hdl: c_uint16 = 0,
                 uuid: Array[c_uint8] = None):

        self.attr_hdl = attr_hdl
        self.start_hdl = start_hdl
        self.end_hdl = end_hdl
        self.uuid = uuid if uuid else (c_uint8 * 2)(0, 0)
        super().__init__(attr_hdl=self.attr_hdl,
                         start_hdl=self.start_hdl,
                         end_hdl=self.end_hdl,
                         uuid_len=self.uuid_len,
                         _uuid=self._uuid,
                         padding=0)

                # element handle
    _fields_ = [("attr_hdl", c_uint16),
                # start handle
                ("start_hdl", c_uint16),
                # end handle
                ("end_hdl", c_uint16),
                # UUID length
                ("uuid_len", c_uint8),
                # included service UUID
                ("_uuid", POINTER(c_uint8)),
                ("padding", c_uint8)]

    def get_uuid(self):
        return cast(self._uuid, POINTER(c_uint8 * self.uuid_len)).contents

    def set_uuid(self, new_uuid: Array[c_uint8]):
        if len(new_uuid) == 2 or len(new_uuid) == 16:
            self._uuid = new_uuid
            self.uuid_len = len(new_uuid)
        else:
            raise ValueError("UUID length must be 2 or 16")

    uuid = property(get_uuid, set_uuid)


# Discovery All Characteristic indication LittleEndianStructure
class gattc_disc_char_ind(LittleEndianStructure):

    def __init__(self,
                 attr_hdl: c_uint16 = 0,
                 pointer_hdl: c_uint16 = 0,
                 prop: ATT_CHAR_PROP = ATT_CHAR_PROP.READ,  # TODO difference between attribute prop and permissons
                 uuid: Array[c_uint8] = None):

        self.attr_hdl = attr_hdl
        self.pointer_hdl = pointer_hdl
        self.prop = prop
        self.uuid = uuid if uuid else (c_uint8 * 2)(0, 0)
        super().__init__(attr_hdl=self.attr_hdl,
                         pointer_hdl=self.pointer_hdl,
                         prop=self.prop,
                         uuid_len=self.uuid_len,
                         _uuid=self._uuid)

                # database element handle
    _fields_ = [("attr_hdl", c_uint16),
                # pointer attribute handle to UUID
                ("pointer_hdl", c_uint16),
                # properties
                ("prop", c_uint8),
                # UUID length
                ("uuid_len", c_uint8),
                # characteristic UUID
                ("_uuid", POINTER(c_uint8))]

    def get_uuid(self):
        return cast(self._uuid, POINTER(c_uint8 * self.uuid_len)).contents

    def set_uuid(self, new_uuid: Array[c_uint8]):
        if len(new_uuid) == 2 or len(new_uuid) == 16:
            self._uuid = new_uuid
            self.uuid_len = len(new_uuid)
        else:
            raise ValueError("UUID length must be 2 or 16")

    uuid = property(get_uuid, set_uuid)


# Discovery Characteristic Descriptor indication LittleEndianStructure
class gattc_disc_char_desc_ind(LittleEndianStructure):

    def __init__(self,
                 attr_hdl: c_uint16 = 0,
                 uuid: Array[c_uint8] = None):

        self.attr_hdl = attr_hdl
        self.uuid = uuid if uuid else (c_uint8 * 2)(0, 0)
        super().__init__(attr_hdl=self.attr_hdl,
                         uuid_len=self.uuid_len,
                         _uuid=self._uuid,
                         padding=0)

                # database element handle
    _fields_ = [("attr_hdl", c_uint16),
                # UUID length
                ("uuid_len", c_uint8),
                # UUID
                ("_uuid", POINTER(c_uint8)),
                ("padding", c_uint8)]

    def get_uuid(self):
        return cast(self._uuid, POINTER(c_uint8 * self.uuid_len)).contents

    def set_uuid(self, new_uuid: Array[c_uint8]):
        if len(new_uuid) == 2 or len(new_uuid) == 16:
            self._uuid = new_uuid
            self.uuid_len = len(new_uuid)
        else:
            raise ValueError("UUID length must be 2 or 16")

    uuid = property(get_uuid, set_uuid)


# Simple Read (GATTC_READ or GATTC_READ_LONG)
class gattc_read_simple(LittleEndianStructure):

    def __init__(self,
                 handle: c_uint16 = 0,
                 offset: c_uint16 = 0,
                 length: c_uint16 = 0):

        self.handle = handle
        self.offset = offset
        self.length = length
        super().__init__(handle=self.handle,
                         offset=self.offset,
                         length=self.length)

                # attribute handle
    _fields_ = [("handle", c_uint16),
                # start offset in data payload
                ("offset", c_uint8),
                # Length of data to read (0 = read all)
                ("length", c_uint16)]


# Read by UUID: search UUID and read it's characteristic value (GATTC_READ_BY_UUID)
# Note: it doesn't perform an automatic read long.
class gattc_read_by_uuid(LittleEndianStructure):

    def __init__(self,
                 start_hdl: c_uint16 = 0,
                 end_hdl: c_uint16 = 0,
                 uuid: Array[c_uint8] = None):

        self.start_hdl = start_hdl
        self.end_hdl = end_hdl
        self.uuid = uuid if uuid else (c_uint8 * 2)(0, 0)
        super().__init__(start_hdl=self.start_hdl,
                         end_hdl=self.end_hdl,
                         uuid_len=self.uuid_len,
                         _uuid=self._uuid)

                # Start handle
    _fields_ = [("start_hdl", c_uint16),
                # End handle
                ("end_hdl", c_uint16),
                # Size of UUID
                ("uuid_len", c_uint8),
                # UUID value
                ("_uuid", POINTER(c_uint8))]

    def get_uuid(self):
        return cast(self._uuid, POINTER(c_uint8 * self.uuid_len)).contents

    def set_uuid(self, new_uuid: Array[c_uint8]):
        if len(new_uuid) == 2 or len(new_uuid) == 16:
            self._uuid = new_uuid
            self.uuid_len = len(new_uuid)
        else:
            raise ValueError("UUID length must be 2 or 16")

    uuid = property(get_uuid, set_uuid)


# Read Multiple short characteristic (GATTC_READ_MULTIPLE)
class gattc_read_multiple(LittleEndianStructure):
    def __init__(self,
                 handle: c_uint16 = 0,
                 len: c_uint16 = 1):

        self.handle = handle
        self.len = len
        super().__init__(handle=self.handle,
                         _len=self._len)

                # attribute handle
    _fields_ = [("handle", c_uint16),
                # Known Handle length (shall be != 0)
                ("_len", c_uint16)]

    def get_len(self):
        return self._len

    def set_len(self, new_len: c_uint16):
        if new_len == 0:
            raise ValueError("Length cannot be 0")
        self._len = new_len

    len = property(get_len, set_len)


# request union according to read type
class gattc_read_req(Union):

    def __init__(self,
                 simple: gattc_read_simple = None,
                 by_uuid: gattc_read_by_uuid = None,
                 multiple: Array[gattc_read_multiple] = None):

        if simple:
            self.simple = simple
            super().__init__(simple=self.simple)
        elif by_uuid:
            self.by_uuid = by_uuid
            super().__init__(by_uuid=self.by_uuid)
        elif multiple:
            self.multiple = multiple
            super().__init__(_multiple=self._multiple,
                             _multiple_len=self._multiple_len)
        else:
            super().__init__(simple=self.simple)

                # Simple Read (GATTC_READ or GATTC_READ_LONG)
    _fields_ = [("simple", gattc_read_simple),
                # Read by UUID (GATTC_READ_BY_UUID)
                ("by_uuid", gattc_read_by_uuid),
                # Read Multiple short characteristic (GATTC_READ_MULTIPLE)
                # ("_multiple", POINTER(gattc_read_multiple))]
                ("_multiple", POINTER(gattc_read_multiple)),
                ("_multiple_len", c_uint16)]  # This field is not included in original struct, but is required to keep track of _multiple length

    def get_multiple(self):
        return cast(self._multiple, POINTER(gattc_read_multiple * self._multiple_len)).contents

    def set_multiple(self, new_value: Array[gattc_read_multiple]):
        self._multiple = new_value if new_value else pointer(gattc_read_multiple)
        self._multiple_len = len(new_value) if new_value else 1

    multiple = property(get_multiple, set_multiple)


# Read command (Simple, Long, Multiple, or by UUID)
class gattc_read_cmd(LittleEndianStructure):

    def __init__(self,
                 operation: GATTC_OPERATION = GATTC_OPERATION.GATTC_READ,
                 seq_num: c_uint16 = 0,
                 req: gattc_read_req = None):

        self.operation = operation
        self.nb = 0
        self.seq_num = seq_num
        self.req = req if req else gattc_read_req()
        super().__init__(operation=self.operation,
                         _nb=self._nb,
                         seq_num=self.seq_num,
                         req=self.req)

                # request type
    _fields_ = [("operation", c_uint8),
                # number of read (only used for multiple read)
                ("_nb", c_uint8),
                # operation sequence number
                ("seq_num", c_uint16),
                # request union according to read type
                ("req", gattc_read_req)]

    def get_nb(self):
        if self.operation == GATTC_OPERATION.GATTC_READ_MULTIPLE:
            return self.req._multiple_len
        return 0

    def set_nb(self, new_value):
        self._nb = new_value

    nb = property(get_nb, set_nb)


# Attribute value read indication
class gattc_read_ind(LittleEndianStructure):

    def __init__(self,
                 handle: c_uint16 = 0,
                 offset: c_uint16 = 0,
                 value: Array[c_uint8] = None):

        self.handle = handle
        self.offset = offset
        self.value = value
        super().__init__(handle=self.handle,
                         offset=self.offset,
                         length=self.length,
                         _value=self._value)

                # Attribute handle
    _fields_ = [("handle", c_uint16),
                # Read offset
                ("offset", c_uint16),
                # Read length
                ("length", c_uint16),
                # Handle value
                ("_value", POINTER(c_uint8))]

    def get_value(self):
        return cast(self._value, POINTER(c_uint8 * self.length)).contents

    def set_value(self, new_value: Array[c_uint8]):
        self._value = new_value if new_value else pointer(c_uint8(0))
        self.length = len(new_value) if new_value else 1

    value = property(get_value, set_value)


# Write peer attribute value command
class gattc_write_cmd(LittleEndianStructure):
    def __init__(self,
                 operation: GATTC_OPERATION = GATTC_OPERATION.GATTC_NO_OP,
                 auto_execute: c_bool = False,
                 seq_num: c_uint16 = 0,
                 handle: c_uint16 = 0,
                 offset: c_uint16 = 0,
                 cursor: c_uint16 = 0,
                 value: Array[c_uint8] = None):

        self.operation = operation
        self.auto_execute = auto_execute
        self.seq_num = seq_num
        self.handle = handle
        self.offset = offset
        self.cursor = cursor
        self.value = value
        super().__init__(operation=self.operation,
                         auto_execute=self.auto_execute,
                         seq_num=self.seq_num,
                         handle=self.handle,
                         offset=self.offset,
                         length=self.length,
                         cursor=self.cursor,
                         _value=self._value)

                # Request type
    _fields_ = [("operation", c_uint8),
                # Perform automatic execution
                # (if false, an ATT Prepare Write will be used this shall be use for reliable write)
                ("auto_execute", c_bool),
                # operation sequence number
                ("seq_num", c_uint16),
                # Attribute handle
                ("handle", c_uint16),
                # Write offset
                ("offset", c_uint16),
                # Write length
                ("length", c_uint16),
                # Internal write cursor shall be initialized to 0
                ("cursor", c_uint16),
                # Handle value
                ("_value", POINTER(c_uint8))]

    def get_value(self):
        return cast(self._value, POINTER(c_uint8 * self.length)).contents

    def set_value(self, new_value: Array[c_uint8]):
        self._value = new_value if new_value else pointer(c_uint8(0))
        self.length = len(new_value) if new_value else 1

    value = property(get_value, set_value)


# Write peer attribute value command
class gattc_execute_write_cmd(LittleEndianStructure):
    def __init__(self,
                 execute: c_bool = False,
                 seq_num: c_uint16 = 0):

        self.operation = GATTC_OPERATION.GATTC_EXEC_WRITE
        self.execute = execute
        self.seq_num = seq_num
        super().__init__(operation=self.operation,
                         execute=self.execute,
                         seq_num=self.seq_num)

                # Request type
    _fields_ = [("operation", c_uint8),
                # [True = perform/False cancel] pending write operations
                ("execute", c_bool),
                # operation sequence number
                ("seq_num", c_uint16)]


# peer device triggers an event (notification)
class gattc_event_ind(LittleEndianStructure):

    def __init__(self,
                 handle: c_uint16 = 0,
                 value: Array[c_uint8] = None):

        self.type = GATTC_OPERATION.GATTC_NOTIFY
        self.handle = handle
        self.value = value
        super().__init__(type=self.type,
                         padding=0,
                         length=self.length,
                         handle=self.handle,
                         _value=self._value)

                # Event Type
    _fields_ = [("type", c_uint8),
                ("padding", c_uint8),
                # Data length
                ("length", c_uint16),
                # Attribute handle
                ("handle", c_uint16),
                # Event Value
                ("_value", POINTER(c_uint8))]

    def get_value(self):
        return cast(self._value, POINTER(c_uint8 * self.length)).contents

    def set_value(self, new_value: Array[c_uint8]):
        self._value = new_value if new_value else pointer(c_uint8(0))
        self.length = len(new_value) if new_value else 1

    value = property(get_value, set_value)


# peer device triggers an event that requires a confirmation (indication)
class gattc_event_req_ind(LittleEndianStructure):

    def __init__(self,
                 handle: c_uint16 = 0,
                 value: Array[c_uint8] = None):

        self.type = GATTC_OPERATION.GATTC_INDICATE
        self.handle = handle
        self.value = value
        super().__init__(type=self.type,
                         padding=0,
                         length=self.length,
                         handle=self.handle,
                         _value=self._value)

                # Event Type
    _fields_ = [("type", c_uint8),
                ("padding", c_uint8),
                # Data length
                ("length", c_uint16),
                # Attribute handle
                ("handle", c_uint16),
                # Event Value
                ("_value", POINTER(c_uint8))]

    def get_value(self):
        return cast(self._value, POINTER(c_uint8 * self.length)).contents

    def set_value(self, new_value: Array[c_uint8]):
        self._value = new_value if new_value else pointer(c_uint8(0))
        self.length = len(new_value) if new_value else 1

    value = property(get_value, set_value)


# Confirm reception of event (trigger a confirmation message)
class gattc_event_cfm(LittleEndianStructure):

    def __init__(self,
                 handle: c_uint16 = 0):

        self.handle = handle
        super().__init__(handle=self.handle)

                # Attribute handle
    _fields_ = [("handle", c_uint16)]


'''
# Register to peer device events command
struct gattc_reg_to_peer_evt_cmd
{
    # Request type
    uint8_t operation;
    # operation sequence number
    uint16_t seq_num;
    # attribute start handle
    uint16_t start_hdl;
    # attribute end handle
    uint16_t end_hdl;
};
'''


# Send an event to peer device
class gattc_send_evt_cmd(LittleEndianStructure):

    def __init__(self,
                 operation: GATTC_OPERATION = GATTC_OPERATION.GATTC_NO_OP,
                 seq_num: c_uint16 = 0,
                 handle: c_uint16 = 0,
                 value: Array[c_uint8] = None):

        self.operation = operation
        self.seq_num = seq_num
        self.handle = handle
        self.value = value
        super().__init__(operation=self.operation,
                         padding=0,
                         seq_num=self.seq_num,
                         handle=self.handle,
                         length=self.length,
                         _value=self._value,)

                # Request type (notification / indication)
    _fields_ = [("operation", c_uint8),
                ("padding", c_uint8),
                # operation sequence number
                ("seq_num", c_uint16),
                # characteristic handle
                ("handle", c_uint16),
                # length of packet to send
                ("length", c_uint16),
                # data value
                ("_value", POINTER(c_uint8))]

    def get_value(self):
        return cast(self._value, POINTER(c_uint8 * self.length)).contents

    def set_value(self, new_value: Array[c_uint8]):
        self._value = new_value if new_value else pointer(c_uint8(0))
        self.length = len(new_value) if new_value else 1

    value = property(get_value, set_value)


# Inform that attribute value is requested by lower layers.
class gattc_read_req_ind(LittleEndianStructure):

    def __init__(self,
                 handle: c_uint16 = 0):

        self.handle = handle
        super().__init__(handle=self.handle)

                # Handle of the attribute that has to be read
    _fields_ = [("handle", c_uint16)]


# Confirm Read Request requested by GATT to profile
class gattc_read_cfm(LittleEndianStructure):

    def __init__(self,
                 handle: c_uint16 = 0,
                 status: HOST_STACK_ERROR_CODE = HOST_STACK_ERROR_CODE.ATT_ERR_NO_ERROR,
                 value: Array[c_uint8] = None):

        self.handle = handle
        self.status = status
        self.value = value
        super().__init__(handle=self.handle,
                         length=self.length,
                         status=self.status,
                         _value=self._value,
                         padding=0)

                # Handle of the attribute read
    _fields_ = [("handle", c_uint16),
                # Data length read
                ("length", c_uint16),
                # Status of read command execution by upper layers
                ("status", c_uint8),
                # attribute data value
                ("_value", POINTER(c_uint8)),
                ("padding", c_uint8)]

    def get_value(self):
        return cast(self._value, POINTER(c_uint8 * self.length)).contents

    def set_value(self, new_value: Array[c_uint8]):
        self._value = new_value if new_value else pointer(c_uint8(0))
        self.length = len(new_value) if new_value else 1

    value = property(get_value, set_value)


# Inform that a modification of database has been requested by peer device.
class gattc_write_req_ind(LittleEndianStructure):

    def __init__(self,
                 handle: c_uint16 = 0,
                 offset: c_uint16 = 0,
                 value: Array[c_uint8] = None
                 ):

        self.handle = handle
        self.offset = offset
        self.value = value
        super().__init__(handle=self.handle,
                         offset=self.offset,
                         length=self.length,
                         _value=self._value)

                # Handle of the attribute that has to be written
    _fields_ = [("handle", c_uint16),
                # offset at which the data has to be written
                ("offset", c_uint16),
                # Data length to be written
                ("length", c_uint16),
                # Data to be written in attribute database
                ("_value", POINTER(c_uint8))]

    def get_value(self):
        return cast(self._value, POINTER(c_uint8 * self.length)).contents

    def set_value(self, new_value: Array[c_uint8]):
        self._value = new_value if new_value else pointer(c_uint8(0))
        self.length = len(new_value) if new_value else 1

    value = property(get_value, set_value)


# Confirm modification of database from upper layer when requested by peer device.
class gattc_write_cfm(LittleEndianStructure):

    def __init__(self,
                 handle: c_uint16 = 0,
                 status: HOST_STACK_ERROR_CODE = HOST_STACK_ERROR_CODE.ATT_ERR_NO_ERROR,
                 ):

        self.handle = handle
        self.status = status
        super().__init__(handle=self.handle,
                         status=self.status,
                         padding=0)

                # Handle of the attribute written
    _fields_ = [("handle", c_uint16),
                # Status of write command execution by upper layers
                ("status", c_uint8),
                ("padding", c_uint8)]


'''
# Parameters for @ref GATTC_SEND_SVC_CHANGED_CMD message
struct gattc_send_svc_changed_cmd
{
    # Request Type
    uint8_t operation;
    # operation sequence number
    uint16_t seq_num;
    # Start of Affected Attribute Handle Range
    uint16_t svc_shdl;
    # End of Affected Attribute Handle Range
    uint16_t svc_ehdl;
};

# Parameters for @ref GATTC_SVC_CHANGED_CFG_IND message
struct gattc_svc_changed_cfg
{
    #*
     * Current value of the Client Characteristic Configuration descriptor for the Service
     * Changed characteristic

    uint16_t ind_cfg;
};
'''


# Request Attribute info to upper layer - could be trigger during prepare write
class gattc_att_info_req_ind(LittleEndianStructure):

    def __init__(self,
                 handle: c_uint16 = 0,
                 ) -> None:

        self.handle = handle
        super().__init__(handle=self.handle)

                # Handle of the attribute for which info are requested
    _fields_ = [("handle", c_uint16)]


# Attribute info from upper layer confirmation
class gattc_att_info_cfm(LittleEndianStructure):

    def __init__(self,
                 handle: c_uint16 = 0,
                 length: c_uint16 = 0,
                 status: HOST_STACK_ERROR_CODE = HOST_STACK_ERROR_CODE.ATT_ERR_NO_ERROR,
                 ) -> None:

        self.handle = handle
        self.length = length
        self.status = status
        super().__init__(handle=self.handle,
                         length=self.length,
                         status=self.status,
                         padding=0)

                # Handle of the attribute
    _fields_ = [("handle", c_uint16),
                # Current length of the attribute
                ("length", c_uint16),
                # use to know if it's possible to modify the attribute
                # can contains authorization or application error code.
                ("status", c_uint8),
                ("padding", c_uint8)]


# Service Discovery command
class gattc_sdp_svc_disc_cmd(LittleEndianStructure):

    def __init__(self,
                 operation: GATTC_OPERATION = GATTC_OPERATION.GATTC_NO_OP,
                 seq_num: c_uint16 = 0,
                 start_hdl: c_uint16 = 0,
                 end_hdl: c_uint16 = 0,
                 uuid: Array[c_uint8] = None
                 ):

        self.operation = operation
        self.seq_num = seq_num
        self.start_hdl = start_hdl
        self.end_hdl = end_hdl
        self.uuid = uuid
        super().__init__(operation=self.operation,
                         uuid_len=self.uuid_len,
                         seq_num=self.seq_num,
                         start_hdl=self.start_hdl,
                         end_hdl=self.end_hdl,
                         _uuid=self._uuid)

                # GATT Request Type
                # - GATTC_SDP_DISC_SVC Search specific service
                # - GATTC_SDP_DISC_SVC_ALL Search for all services
                # - GATTC_SDP_DISC_CANCEL Cancel Service Discovery Procedure
    _fields_ = [("operation", c_uint8),
                # Service UUID Length
                ("uuid_len", c_uint8),
                # operation sequence number
                ("seq_num", c_uint16),
                # Search start handle
                ("start_hdl", c_uint16),
                # Search end handle
                ("end_hdl", c_uint16),
                # Service UUID
                ("_uuid", (c_uint8 * ATT_UUID_128_LEN))]

    def get_uuid(self):
        return self._uuid

    def set_uuid(self, new_uuid: Array[c_uint8]):
        if not self._uuid:
            self._uuid = (c_uint8 * ATT_UUID_128_LEN)()
        set_value = new_uuid if new_uuid else (c_uint8 * ATT_UUID_128_LEN)()
        if len(set_value) != 2 and len(set_value) != 4 and len(set_value) != 16:
            raise ValueError("UUID length must be 2, 4, or 16")
        self.uuid_len = len(set_value)
        memmove(self._uuid, set_value, self.uuid_len)

    uuid = property(get_uuid, set_uuid)


# Information about included service
class gattc_sdp_include_svc(LittleEndianStructure):

    def __init__(self,
                 uuid: c_uint8 * ATT_UUID_128_LEN = (c_uint8 * ATT_UUID_128_LEN)(),
                 start_hdl: c_uint16 = 0,
                 end_hdl: c_uint16 = 0
                 ) -> None:

        self.att_type = GATTC_SDP_ATT_TYPE.GATTC_SDP_INC_SVC
        self.uuid = uuid
        self.start_hdl = start_hdl
        self.end_hdl = end_hdl
        super().__init__(att_type=self.att_type,
                         uuid_len=self.uuid_len,
                         _uuid=self._uuid,
                         # padding=(c_uint8 * 4)(), # TODO manual says there is padding here, but I think it may be wrong
                         start_hdl=self.start_hdl,
                         end_hdl=self.end_hdl)

                # Attribute Type
                # - GATTC_SDP_INC_SVC: Included Service Information
    _fields_ = [("att_type", c_uint8),
                # Included service UUID Length
                ("uuid_len", c_uint8),
                # Included Service UUID
                ("_uuid", c_uint8 * ATT_UUID_128_LEN),
                # ("padding", c_uint8 * 4),
                # Included service Start Handle
                ("start_hdl", c_uint16),
                # Included service End Handle
                ("end_hdl", c_uint16)]

    def get_uuid(self):
        return self._uuid  # TODO could return self._uuid[:self.uuid_len]

    def set_uuid(self, uuid: Array[c_uint8]):
        if len(uuid) == 2 or len(uuid) == 4 or len(uuid) == 16:
            self._uuid = (c_uint8 * ATT_UUID_128_LEN)()
            self._uuid[:len(uuid)] = uuid
            self.uuid_len = len(uuid)
        else:
            raise TypeError("uuid length must be 2, 4, or 16")

    uuid = property(get_uuid, set_uuid)


# Information about attribute characteristic
class gattc_sdp_att_char(LittleEndianStructure):
    def __init__(self,
                 prop: c_uint16 = 0,
                 handle: c_uint16 = 0,
                 ) -> None:

        self.att_type = GATTC_SDP_ATT_TYPE.GATTC_SDP_ATT_CHAR
        self.prop = prop
        self.handle = handle
        super().__init__(att_type=self.att_type,
                         prop=self.prop,
                         handle=self.handle,
                         padding=(c_uint8 * 18)())

                # Attribute Type
                # - GATTC_SDP_ATT_CHAR: Characteristic Declaration
    _fields_ = [("att_type", c_uint8),
                #  Value property
                ("prop", c_uint8),
                # Value Handle
                ("handle", c_uint16),
                ("padding", c_uint8 * 18)]


# Information about attribute
class gattc_sdp_att(LittleEndianStructure):

    def __init__(self,
                 att_type: GATTC_SDP_ATT_TYPE = GATTC_SDP_ATT_TYPE.GATTC_SDP_ATT_VAL,
                 uuid_len: c_uint8 = 0,
                 uuid: c_uint8 * ATT_UUID_128_LEN = (c_uint8 * ATT_UUID_128_LEN)(),
                 ) -> None:

        self.att_type = att_type
        self.uuid_len = uuid_len
        self.uuid = uuid

        super().__init__(_att_type=self.att_type,
                         uuid_len=self.uuid_len,
                         _uuid=self._uuid,
                         padding=(c_uint8 * 4)())

                # Attribute Type
                # - GATTC_SDP_ATT_VAL: Attribute Value
                # - GATTC_SDP_ATT_DESC: Attribute Descriptor
    _fields_ = [("_att_type", c_uint8),
                # Attribute UUID Length
                ("uuid_len", c_uint8),
                # Attribute UUID
                ("_uuid", c_uint8 * ATT_UUID_128_LEN),
                ("padding", c_uint8 * 4)]

    def get_att_type(self):
        return self._att_type

    def set_att_type(self, new_att_type: GATTC_SDP_ATT_TYPE):
        if new_att_type != GATTC_SDP_ATT_TYPE.GATTC_SDP_ATT_VAL and new_att_type != GATTC_SDP_ATT_TYPE.GATTC_SDP_ATT_DESC:
            raise TypeError("att_type must be GATTC_SDP_ATT_TYPE.GATTC_SDP_ATT_VAL or GATTC_SDP_ATT_TYPE.GATTC_SDP_ATT_DESC")
        self._att_type = new_att_type

    att_type = property(get_att_type, set_att_type)

    def get_uuid(self):
        return self._uuid  # TODO could return self._uuid[:self.uuid_len]

    def set_uuid(self, uuid: Array[c_uint8]):
        if len(uuid) == 2 or len(uuid) == 4 or len(uuid) == 16:
            self._uuid = (c_uint8 * ATT_UUID_128_LEN)()
            self._uuid[:len(uuid)] = uuid
            self.uuid_len = len(uuid)

        else:
            raise TypeError("uuid length must be 2, 4, or 16")

    uuid = property(get_uuid, set_uuid)


# Attribute information
class gattc_sdp_att_info(Union):

    def __init__(self,
                 att_type: GATTC_SDP_ATT_TYPE = GATTC_SDP_ATT_TYPE.GATTC_SDP_NONE,
                 att_char: gattc_sdp_att_char = gattc_sdp_att_char(),
                 inc_svc: gattc_sdp_include_svc = gattc_sdp_include_svc(),
                 att: gattc_sdp_att = gattc_sdp_att()):

        if att_type:
            self.att_type = att_type
            super().__init__(att_type=self.att_type)
        elif att_char:
            self.att_char = att_char
            super().__init__(att_char=self.att_char)
        elif inc_svc:
            self.inc_svc = inc_svc
            super().__init__(inc_svc=self.inc_svc)
        elif att:
            self.att = att
            super().__init__(att=self.att)
        else:
            self.att_type = att_type
            super().__init__(simple=self.att_type)

                # Attribute Type
    _fields_ = [("att_type", c_uint8),
                # Information about attribute characteristic
                ("att_char", gattc_sdp_att_char),
                # Information about included service
                ("inc_svc", gattc_sdp_include_svc),
                # Information about attribute
                ("att", gattc_sdp_att)]  # This field is not included in original struct, but is required to keep track of _multiple length


# Service Discovery indicate that a service has been found.
class gattc_sdp_svc_ind(LittleEndianStructure):

    def __init__(self,
                 uuid_len: c_uint8 = 0,
                 uuid: c_uint8 * ATT_UUID_128_LEN = (c_uint8 * ATT_UUID_128_LEN)(),
                 start_hdl: c_uint16 = 0,
                 end_hdl: c_uint16 = 0,
                 info: Array[gattc_sdp_att_info] = None
                 ) -> None:

        self.uuid_len = uuid_len
        self.uuid = uuid
        self.start_hdl = start_hdl
        self.end_hdl = end_hdl
        self.info = info
        super().__init__(uuid_len=self.uuid_len,
                         _uuid=self._uuid,
                         padding=0,
                         start_hdl=self.start_hdl,
                         end_hdl=self.end_hdl,
                         _info=self._info)

                # Service UUID Length
    _fields_ = [("uuid_len", c_uint8),
                # Service UUID
                ("_uuid", c_uint8 * ATT_UUID_128_LEN),
                ("padding", c_uint8),
                # Service start handle
                ("start_hdl", c_uint16),
                # Service end handle
                ("end_hdl", c_uint16),
                # attribute information present in the service
                # (length = end_hdl - start_hdl)
                ("_info", POINTER(gattc_sdp_att_info))]

    def get_info(self):
        return cast(self._info, POINTER(gattc_sdp_att_info * (self.end_hdl - self.start_hdl))).contents

    def set_info(self, new_info: Array[gattc_sdp_att_info]):
        self._info = new_info if new_info else pointer(gattc_sdp_att_info())

    info = property(get_info, set_info)

    def get_uuid(self):
        return self._uuid  # TODO could return self._uuid[:self.uuid_len]

    def set_uuid(self, uuid: Array[c_uint8]):
        if len(uuid) == 2 or len(uuid) == 4 or len(uuid) == 16:  # TODO raise error
            self._uuid = (c_uint8 * ATT_UUID_128_LEN)()
            self._uuid[:len(uuid)] = uuid
            self.uuid_len = len(uuid)

        else:
            raise TypeError("uuid length must be 2, 4, or 16")

    uuid = property(get_uuid, set_uuid)


'''
#
 * FUNCTION DECLARATIONS
 ****************************************************************************************

extern const struct ke_state_handler gattc_default_handler;
extern ke_state_t gattc_state[GATTC_IDX_MAX];

#endif # (BLE_CENTRAL || BLE_PERIPHERAL)
# @} GATTCTASK
#endif // GATTC_TASK_H_
'''
