from ctypes import Array, c_bool, c_uint8, c_uint16, c_uint32, LittleEndianStructure, Union
from enum import auto, IntEnum

from .co_bt import bd_addr, BD_ADDR_LEN, LE_FEATS_LEN, rand_nb
from .co_error import CO_ERROR
from .gap import GAP_AUTH, GAP_IO_CAP, GAP_KDIST, GAP_OOB, GAP_TK_TYPE, gap_sec_key, GAP_SEC_REQ, gap_bdaddr, \
    gap_dev_name, gap_slv_pref
from .rwble_hl_error import HOST_STACK_ERROR_CODE
from .rwip_config import KE_API_ID


# GAP Controller Task messages
class GAPC_MSG_ID(IntEnum):
    # Default event */
    # Command Complete event
    GAPC_CMP_EVT = (KE_API_ID.TASK_ID_GAPC << 8)  # 0x0E00

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
    GAPC_NO_OP = 0x00

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
# ESR10
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


# List of device info that should be provided by application
class GAPC_DEV_INFO(IntEnum):
    # Device Name
    GAPC_DEV_NAME = 0
    # Device Appearance Icon
    GAPC_DEV_APPEARANCE = auto()
    # Device Slave preferred parameters
    GAPC_DEV_SLV_PREF_PARAMS = auto()
    # Device Central Address Resolution parameters
    GAPC_DEV_CENTRAL_RPA = auto()
# ESR10
    # Device Resolvable Private Address Only parameters
    GAPC_DEV_RPA_ONLY = auto()
    # maximum device info parameter
    GAPC_DEV_INFO_MAX = auto()


# Command complete event data structure
class gapc_cmp_evt(LittleEndianStructure):

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
class gapc_connection_req_ind(LittleEndianStructure):
    def __init__(self,
                 conhdl: c_uint16 = 0,
                 con_interval: c_uint16 = 0,
                 con_latency: c_uint16 = 0,
                 sup_to: c_uint16 = 0,
                 clk_accuracy: c_uint8 = 0,
                 peer_addr_type: c_uint8 = 0,
                 peer_addr: bd_addr = bd_addr((c_uint8 * BD_ADDR_LEN)())):

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
class gapc_connection_cfm(LittleEndianStructure):
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


# Request disconnection of current link command.
class gapc_disconnect_cmd(LittleEndianStructure):

    def __init__(self, reason: CO_ERROR = CO_ERROR.CO_ERROR_NO_ERROR) -> None:

        self.operation = GAPC_OPERATION.GAPC_DISCONNECT
        self.reason = reason
        super().__init__(operation=self.operation,
                         reason=self.reason)

                # GAP request type:
                # - GAPC_DISCONNECT: Disconnect link.
    _fields_ = [("operation", c_uint8),
                # Reason of disconnection
                ("reason", c_uint8)]


# Indicate that a link has been disconnected
class gapc_disconnect_ind(LittleEndianStructure):

    def __init__(self,
                 conhdl: c_uint16 = 0,
                 reason: CO_ERROR = CO_ERROR.CO_ERROR_NO_ERROR
                 ) -> None:

        self.conhdl = conhdl
        self.reason = reason
        super().__init__(conhdl=self.conhdl,
                         reason=self.reason,
                         padding=0)

                # Connection handle
    _fields_ = [("conhdl", c_uint16),
                # Reason of disconnection
                ("reason", c_uint8),
                ("padding", c_uint8)]


# Retrieve information command
class gapc_get_info_cmd(LittleEndianStructure):

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


# device information data
class gapc_dev_info_val(Union):

    def __init__(self,
                 name: gap_dev_name = None,
                 appearance: c_uint16 = None,  # TODO is there an ENUM for this? See app_adv_data.h
                 slv_params: gap_slv_pref = None,
                 central_rpa: c_uint8 = None,
                 rpa_only: c_uint8 = None
                 ):

        if name:
            self.name = name
            super().__init__(name=self.name)
        elif appearance:
            self.appearance = appearance
            super().__init__(appearance=self.appearance)
        elif slv_params:
            self.slv_params = slv_params
            super().__init__(slv_params=self.slv_params)
        elif central_rpa:
            self.central_rpa = central_rpa
            super().__init__(central_rpa=self.central_rpa)
        elif rpa_only:
            self.rpa_only = rpa_only
            super().__init__(rpa_only=self.rpa_only)
        else:
            self.name = gap_dev_name()
            super().__init__(name=self.name)

                # Device name
    _fields_ = [("name", gap_dev_name),
                # Appearance Icon
                ("appearance", c_uint16),
                # Slave preferred parameters
                ("slv_params", gap_slv_pref),
                # Central Address Resolution
                ("central_rpa", c_uint8),
                # ESR10
                # Resolvable Private Address Only
                ("rpa_only", c_uint8)]


# Indication of peer version info
class gapc_peer_version_ind(LittleEndianStructure):

    def __init__(self,
                 compid: c_uint16 = 0,
                 lmp_subvers: c_uint16 = 0,
                 lmp_vers: c_uint8 = 0):

        self.compid = compid
        self.lmp_subvers = lmp_subvers
        self.lmp_vers = lmp_vers
        super().__init__(compid=self.compid,
                         lmp_subvers=self.lmp_subvers,
                         lmp_vers=self.lmp_vers,
                         padding=0)

                # Manufacturer name
    _fields_ = [("compid", c_uint16),
                # LMP subversion
                ("lmp_subvers", c_uint16),
                # LMP version
                ("lmp_vers", c_uint8),
                ("padding", c_uint8)]


# Indication of peer features info
class gapc_peer_features_ind(LittleEndianStructure):

    def __init__(self,
                 features: Array = (c_uint8 * LE_FEATS_LEN)()):

        self.features = features
        super().__init__(features=self.features)

                # 8-byte array for LE features
    _fields_ = [("features", c_uint8 * LE_FEATS_LEN)]


# Peer device request local device info such as name, appearance or slave preferred parameters
class gapc_get_dev_info_req_ind(LittleEndianStructure):

    def __init__(self,
                 req: GAPC_DEV_INFO = GAPC_DEV_INFO.GAPC_DEV_NAME):

        self.req = req
        super().__init__(req=self.req)

                # Requested information
                # - GAPC_DEV_NAME: Device Name
                # - GAPC_DEV_APPEARANCE: Device Appearance Icon
                # - GAPC_DEV_SLV_PREF_PARAMS: Device Slave preferred parameters
                # - GAPC_DEV_CENTRAL_RPA: Device Central Address Resolution
                # - GAPC_DEV_RPA_ONLY: Device Resolvable Private Address Only
    _fields_ = [("req", c_uint8)]


# Send requested info to peer device
class gapc_get_dev_info_cfm(LittleEndianStructure):

    def __init__(self,
                 req: GAPC_DEV_INFO = GAPC_DEV_INFO.GAPC_DEV_NAME,
                 info: gapc_dev_info_val = None):

        self.req = req
        self.info = info if info else gapc_dev_info_val()
        super().__init__(req=self.req,
                         padding=0,
                         info=self.info,
                         more_padding=(c_uint8 * 6)())

                # Requested information
                # - GAPC_DEV_NAME: Device Name
                # - GAPC_DEV_APPEARANCE: Device Appearance Icon
                # - GAPC_DEV_SLV_PREF_PARAMS: Device Slave preferred parameters
                # - GAPC_DEV_CENTRAL_RPA: Device Central Address Resolution
                # - GAPC_DEV_RPA_ONLY: Device Resolvable Private Address Only
    _fields_ = [("req", c_uint8),
                ("padding", c_uint8),
                # Peer device information data
                ("info", gapc_dev_info_val),
                ("more_padding", (c_uint8 * 6))]


# Perform update of connection parameters command
class gapc_param_update_cmd(LittleEndianStructure):

    def __init__(self,
                 operation: GAPC_OPERATION = GAPC_OPERATION.GAPC_UPDATE_PARAMS,
                 pkt_id: c_uint8 = 0,
                 intv_min: c_uint16 = 0,
                 intv_max: c_uint16 = 0,
                 latency: c_uint16 = 0,
                 time_out: c_uint16 = 0,
                 ce_len_min: c_uint16 = 0,
                 ce_len_max: c_uint16 = 0):

        self.operation = operation
        self.pkt_id = pkt_id
        self.intv_min = intv_min
        self.intv_max = intv_max
        self.latency = latency
        self.time_out = time_out
        self.ce_len_min = ce_len_min
        self.ce_len_max = ce_len_max
        super().__init__(operation=self.operation,
                         pkt_id=self.pkt_id,
                         intv_min=self.intv_min,
                         intv_max=self.intv_max,
                         latency=self.latency,
                         time_out=self.time_out,
                         ce_len_min=self.ce_len_min,
                         ce_len_max=self.ce_len_max)

                # GAP request type:
                # - GAPC_UPDATE_PARAMS: Perform update of connection parameters.
    _fields_ = [("operation", c_uint8),
                # Internal parameter used to manage internally l2cap packet identifier for signaling
                ("pkt_id", c_uint8),
                # Connection interval minimum
                ("intv_min", c_uint16),
                # Connection interval maximum
                ("intv_max", c_uint16),
                # Latency
                ("latency", c_uint16),
                # Supervision timeout
                ("time_out", c_uint16),
                # Minimum Connection Event Duration
                ("ce_len_min", c_uint16),
                # Maximum Connection Event Duration
                ("ce_len_max", c_uint16)]


# Request of updating connection parameters indication
class gapc_param_update_req_ind(LittleEndianStructure):
    def __init__(self,
                 intv_min: c_uint16 = 0,
                 intv_max: c_uint16 = 0,
                 latency: c_uint16 = 0,
                 time_out: c_uint16 = 0):

        self.intv_min = intv_min
        self.intv_max = intv_max
        self.latency = latency
        self.time_out = time_out
        super().__init__(intv_min=self.intv_min,
                         intv_max=self.intv_max,
                         latency=self.latency,
                         time_out=self.time_out)

                # Connection interval minimum
    _fields_ = [("intv_min", c_uint16),
                # Connection interval maximum
                ("intv_max", c_uint16),
                # Latency
                ("latency", c_uint16),
                # Supervision timeout
                ("time_out", c_uint16)]


# Connection parameters updated indication
class gapc_param_updated_ind(LittleEndianStructure):
    def __init__(self,
                 con_interval: c_uint16 = 0,
                 con_latency: c_uint16 = 0,
                 sup_to: c_uint16 = 0
                 ) -> None:

        self.con_interval = con_interval
        self.con_latency = con_latency
        self.sup_to = sup_to
        super().__init__(con_interval=self.con_interval,
                         con_latency=self.con_latency,
                         sup_to=self.sup_to)

                # Connection interval value
    _fields_ = [("con_interval", c_uint16),
                # Connection latency value
                ("con_latency", c_uint16),
                # Supervision timeout
                ("sup_to", c_uint16)]


# Master confirm or not that parameters proposed by slave are accepted or not
class gapc_param_update_cfm(LittleEndianStructure):

    def __init__(self,
                 accept: c_bool = 0,
                 ce_len_min: c_uint16 = 0,
                 ce_len_max: c_uint16 = 0):

        self.accept = accept
        self.ce_len_min = ce_len_min
        self.ce_len_max = ce_len_max
        super().__init__(accept=self.accept,
                         padding=0,
                         ce_len_min=self.ce_len_min,
                         ce_len_max=self.ce_len_max)

                # True to accept slave connection parameters, False else.
    _fields_ = [("accept", c_bool),
                ("padding", c_uint8),
                # Minimum Connection Event Duration
                ("ce_len_min", c_uint16),
                # Maximum Connection Event Duration
                ("ce_len_max", c_uint16)]


# Pairing parameters
class gapc_pairing(LittleEndianStructure):
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
                # Initiator key distribution (@see gap_kdist)
                ("ikey_dist", c_uint8),
                # Responder key distribution (@see gap_kdist)
                ("rkey_dist", c_uint8),
                # Device security requirements (minimum security level). (@see gap_sec_req)
                ("sec_req", c_uint8)]


# Long Term Key information
class gapc_ltk(LittleEndianStructure):

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
                         key_size=self.key_size,
                         padding=0)

                # Long Term Key
    _fields_ = [("ltk", gap_sec_key),
                # Encryption Diversifier
                ("ediv", c_uint16),
                # Random Number)
                ("randnb", rand_nb),
                # Encryption key size (7 to 16)
                ("key_size", c_uint8),
                ("padding", c_uint8)]


# Identity Resolving Key information
class gapc_irk(LittleEndianStructure):

    def __init__(self,
                 irk: gap_sec_key = gap_sec_key(),
                 addr: gap_bdaddr = gap_bdaddr()):

        self.irk = irk
        self.addr = addr
        super().__init__(irk=self.irk,
                         addr=self.addr)

                # Identity Resolving Key
    _fields_ = [("irk", gap_sec_key),
                # Device BD Address
                ("addr", gap_bdaddr)]


# Start Bonding command procedure
class gapc_bond_cmd(LittleEndianStructure):

    def __init__(self,
                 pairing: gapc_pairing = gapc_pairing()):

        self.operation = GAPC_OPERATION.GAPC_BOND
        self.pairing = pairing
        super().__init__(operation=self.operation,
                         pairing=self.pairing)

                # GAP request type:
                # - GAPC_BOND:  Start bonding procedure.
    _fields_ = [("operation", c_uint8),
                # Pairing information
                ("pairing", gapc_pairing)]


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
class gapc_bond_req_ind(LittleEndianStructure):

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
class gapc_bond_cfm(LittleEndianStructure):

    def __init__(self,
                 request: GAPC_BOND = GAPC_BOND.GAPC_PAIRING_RSP,
                 accept: c_bool = 0,
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
                ("accept", c_bool),
                # Bond procedure information data
                ("data", gapc_bond_cfm_data)]


# Bond procedure information data
class gapc_bond_data(Union):

    def __init__(self,
                 auth: GAP_AUTH = GAP_AUTH.GAP_AUTH_REQ_NO_MITM_NO_BOND,
                 reason: HOST_STACK_ERROR_CODE = HOST_STACK_ERROR_CODE.ATT_ERR_NO_ERROR,
                 ltk: gapc_ltk = gapc_ltk(),
                 irk: gapc_irk = gapc_irk(),
                 csrk: gap_sec_key = gap_sec_key()):

        self.auth = auth
        self.reason = reason
        self.ltk = ltk
        self.irk = irk
        self.csrk = csrk
        super().__init__(auth=self.auth,
                         reason=self.reason,
                         ltk=self.ltk,
                         irk=self.irk,
                         csrk=self.csrk)

                # Authentication information (@see gap_auth)
                # (if info = GAPC_PAIRING_SUCCEED)
    _fields_ = [("auth", c_uint8),
                # Pairing failed reason  (if info = GAPC_PAIRING_FAILED)
                ("reason", c_uint8),
                # Long Term Key information (if info = GAPC_LTK_EXCH)
                ("ltk", gapc_ltk),
                # Identity Resolving Key information (if info = GAPC_IRK_EXCH)
                ("irk", gapc_irk),
                # Connection Signature Resolving Key information (if info = GAPC_CSRK_EXCH)
                ("csrk", gap_sec_key)]


# Bonding information indication message
class gapc_bond_ind(LittleEndianStructure):

    def __init__(self,
                 info: GAPC_BOND = GAPC_BOND.GAPC_PAIRING_RSP,
                 data: gapc_bond_data = gapc_bond_data()):

        self.info = info
        self.data = data
        super().__init__(info=self.info,
                         padding=0,
                         data=self.data)

                # Bond information type (@see gapc_bond)
    _fields_ = [("info", c_uint8),
                ("padding", c_uint8),
                # Bond procedure information data
                ("data", gapc_bond_data)]


# Encryption requested by peer device indication message.
class gapc_encrypt_req_ind(LittleEndianStructure):

    def __init__(self,
                 ediv: c_uint16 = 0,
                 rand_nb: rand_nb = rand_nb()):

        self.ediv = ediv
        self.rand_nb = rand_nb
        super().__init__(ediv=self.ediv,
                         rand_nb=self.rand_nb)

                # Encryption Diversifier
    _fields_ = [("ediv", c_uint16),
                # Random Number
                ("rand_nb", rand_nb)]


# Confirm requested Encryption information.
class gapc_encrypt_cfm(LittleEndianStructure):

    def __init__(self,
                 found: c_bool = 0,
                 ltk: gap_sec_key = gap_sec_key(),
                 key_size: c_uint8 = 0):

        self.found = found
        self.ltk = ltk
        self.key_size = key_size
        super().__init__(found=self.found,
                         ltk=self.ltk,
                         key_size=self.key_size)

                # Indicate if a LTK has been found for the peer device (0x0 = not found, 0x1 found)
    _fields_ = [("found", c_bool),
                # Long Term Key
                ("ltk", gap_sec_key),
                # LTK Key Size
                ("key_size", c_uint8)]


# Encryption information indication message
class gapc_encrypt_ind(LittleEndianStructure):

    def __init__(self,
                 auth: GAP_AUTH = GAP_AUTH.GAP_AUTH_REQ_NO_MITM_NO_BOND):

        self.auth = auth
        super().__init__(auth=self.auth)

                # Authentication  level (@see gap_auth)
    _fields_ = [("auth", c_uint8)]


# Start Security Request command procedure
class gapc_security_cmd(LittleEndianStructure):
    def __init__(self,
                 auth: c_uint16 = GAP_AUTH.GAP_AUTH_REQ_SECURE_CONNECTION,
                 ):

        self.operation = GAPC_OPERATION.GAPC_SECURITY_REQ
        self.auth = auth
        super().__init__(operation=self.operation,
                         auth=self.auth)

                # GAP request type:
                # - GAPC_SECURITY_REQ: Start security request procedure
    _fields_ = [("operation", c_uint8),
                # Authentication level (@see gap_auth)
                ("auth", c_uint8)]


# Parameters of the @ref GAPC_SIGN_COUNTER_IND message
class gapc_sign_counter_ind(LittleEndianStructure):

    def __init__(self,
                 local_sign_counter: c_uint32 = 0,
                 peer_sign_counter: c_uint32 = 0):

        self.local_sign_counter = local_sign_counter
        self.peer_sign_counter = peer_sign_counter
        super().__init__(local_sign_counter=self.local_sign_counter,
                         peer_sign_counter=self.peer_sign_counter)

                # Local SignCounter value
    _fields_ = [("local_sign_counter", c_uint32),
                # Peer SignCounter value
                ("peer_sign_counter", c_uint32)]


class gapc_set_le_pkt_size_cmd(LittleEndianStructure):

    def __init__(self,
                 tx_octets: c_uint16 = 0,
                 tx_time: c_uint16 = 0
                 ):

        self.operation = GAPC_OPERATION.GAPC_SET_LE_PKT_SIZE
        self.tx_octets = tx_octets
        self.tx_time = tx_time
        super().__init__(operation=self.operation,
                         padding=0,
                         tx_octets=self.tx_octets,
                         tx_time=self.tx_time)

                # GAP request type:
                # - GAPC_SET_LE_PKT_SIZE : Set the LE Data length value
    _fields_ = [("operation", c_uint8),
                ("padding", c_uint8),
                # Preferred maximum number of payload octets that the local Controller should include
                # in a single Link Layer Data Channel PDU.
                ("tx_octets", c_uint16),
                # Preferred maximum number of microseconds that the local Controller should use to transmit
                # a single Link Layer Data Channel PDU
                ("tx_time", c_uint16)]


# Parameters of the @ref GAPC_LE_PKT_SIZE_IND message
class gapc_le_pkt_size_ind(LittleEndianStructure):

    def __init__(self,
                 max_tx_octets: c_uint16 = 0,
                 max_tx_time: c_uint16 = 0,
                 max_rx_octets: c_uint16 = 0,
                 max_rx_time: c_uint16 = 0
                 ):

        self.max_tx_octets = max_tx_octets
        self.max_tx_time = max_tx_time
        self.max_rx_octets = max_rx_octets
        self.max_rx_time = max_rx_time
        super().__init__(max_tx_octets=self.max_tx_octets,
                         max_tx_time=self.max_tx_time,
                         max_rx_octets=self.max_rx_octets,
                         max_rx_time=self.max_rx_time)

                # The maximum number of payload octets in TX
    _fields_ = [("max_tx_octets", c_uint16),
                # The maximum time that the local Controller will take to TX
                ("max_tx_time", c_uint16),
                # The maximum number of payload octets in RX
                ("max_rx_octets", c_uint16),
                # The maximum time that the local Controller will take to RX
                ("max_rx_time", c_uint16)]
