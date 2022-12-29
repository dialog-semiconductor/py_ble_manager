from ctypes import c_uint8, c_uint16, LittleEndianStructure
from enum import IntEnum
from gtl_messages.gtl_port.co_bt import le_chnl_map, ADV_FILTER_POLICY, ADV_DATA_LEN, SCAN_RSP_DATA_LEN, \
    BD_ADDR_LEN, ADV_CHANNEL_MAP, BD_NAME_SIZE
from gtl_messages.gtl_port.gap import GAP_ROLE, gap_bdaddr, gap_sec_key, GAP_IO_CAP, gap_slv_pref, GAP_AD_TYPE
from gtl_messages.gtl_port.gapm_task import GAPM_OPERATION, GAP_ADV_MODE, gapm_att_cfg_flag, GAPM_ADDR_TYPE


# TODO belong in ble_common.h
# BLE stack status
class BLE_STATUS(IntEnum):
    BLE_IS_DISABLED = 0x00,
    BLE_IS_ENABLED = 0x01,
    BLE_IS_BUSY = 0x02,
    BLE_IS_RESET = 0x03,
# end ble_common.h


# TODO belong in ble_gap.h
# GAP roles
# TODO why is this seprate def needed ?
'''
class GAP_ROLE(IntEnum):
        GAP_NO_ROLE = 0x00,  # No role
        GAP_OBSERVER_ROLE = 0x01,  # Observer role
        GAP_BROADCASTER_ROLE = 0x02,  # Broadcaster role
        GAP_CENTRAL_ROLE = 0x04,  # Central role
        GAP_PERIPHERAL_ROLE = 0x08,  # Peripheral role
        GAP_ALL_ROLES = (GAP_OBSERVER_ROLE|GAP_BROADCASTER_ROLE|GAP_CENTRAL_ROLE|GAP_PERIPHERAL_ROLE),  # All roles
'''


# GAP scan parameters
class gap_scan_params(LittleEndianStructure):

    def __init__(self,
                 interval: c_uint16 = 0,
                 window: c_uint16 = 0):
        self.interval = interval
        self.window = window
        super().__init__(interval=self.interval, window=self.window)

    _fields_ = [("interval", c_uint16),
                ("window", c_uint16)]


# end ble_gap.h
# TODO make this a structure so dont need to convert
class BleDevParams():

    def __init__(self) -> None:
        # GAP device information
        # TODO Max len + null char. Should we create property
        self.dev_name = (c_uint8 * (BD_NAME_SIZE + 1))()  # GAP device name plus NULL char # TODO F8 seems realy long

        # TODO do we need this gap_appearance_t   appearance;                                  # GAP device appearance
        # BLE state
        self.status = BLE_STATUS.BLE_IS_DISABLED  # Status of the BLE stack
        # Air operations in progress
        self.advertising = False   # Advertising operation in progress
        self.connecting = False  # Connection operation in progress
        self.scanning = False  # Scanning operation in progress
        self.role = GAP_ROLE.GAP_ROLE_NONE  # Enabled roles for the device # TODO redef of role_t in ble_manager

        # Privacy parameters
        self.addr_renew_duration = 0  # Random address renew duration
        # TODO ble_manager seems to redefine own_addr_t
        self.own_addr = gap_bdaddr()  # Provided own public address
        # TODO redefines irk_t
        self.irk = gap_sec_key()  # IRK for device resolvable address
        self.addr_resolv_req_pending = 0  # Pending address resolve requests
        # Attribute database configuration

        self.att_db_cfg = gapm_att_cfg_flag()  # Attribute DB Configuration bitmask
        self.mtu_size = 0  # MTU size
        # Channel map (central only)
        self.channel_map = le_chnl_map()  # Channel map
        # TODO one of GAPM_ADV_NON_CONN, GAPM_ADV_UNDIRECT, GAPM_ADV_DIRECT, GAPM_ADV_DIRECT_LDC
        self.adv_type = GAPM_OPERATION.GAPM_ADV_UNDIRECT  # Advertising type
        self.adv_mode = GAP_ADV_MODE.GAP_GEN_DISCOVERABLE  # Discoverability mode for adv.
        self.adv_channel_map = ADV_CHANNEL_MAP.ADV_ALL_CHNLS_EN  # Channel map used for advertising
        self.adv_intv_min = 0  # Minimum advertising interval
        self.adv_intv_max = 0  # Maximum advertising interval
        self.adv_filter_policy = ADV_FILTER_POLICY.ADV_ALLOW_SCAN_ANY_CON_ANY  # Advertising filter policy
        self.adv_direct_address = gap_bdaddr()  # Address used for directed advertising
        self.adv_data_length = 0  # Length of advertising data
        self.adv_data = (c_uint8 * ADV_DATA_LEN)()  # Advertising data
        self.scan_rsp_data_length = 0  # Length of scan response
        self.scan_rsp_data = (c_uint8 * SCAN_RSP_DATA_LEN)()  # Scan response data
        # Scan parameters used for connection procedures
        self.scan_params = gap_scan_params()  # Scan parameters # TODO does this struct exist in gtl_port files?
        # Peripheral preferred connection parameters
        self.gap_ppcp = gap_slv_pref()  # Connection parameters structure
        # IO Capabilities configuration
        self.io_capabilities = GAP_IO_CAP.GAP_IO_CAP_NO_INPUT_NO_OUTPUT  # GAP IO capabilities
# if (dg_configBLE_PRIVACY_1_2 == 1) # TODO add privacy
        # ble_mgr_ral_op_t  prev_privacy_operation;  # TODO add privacy enum
# endif /* (dg_configBLE_PRIVACY_1_2 == 1)
# if (dg_configBLE_2MBIT_PHY == 1) # TODO 2M PHY??
        # self.tx_phy_pref_default = 0  # GAP default TX PHY preference
        # self.rx_phy_pref_default = 0  # GAP default RX PHY preference
        # self.phy_set_pending = False  # GAP PHY set operation pending
        # self.phy_change_req = False  # GAP PHY change requested
# endif /* (dg_configBLE_2MBIT_PHY == 1)
        self.conn_rssi = 0  # The RSSI reading reported by GAPC_CON_RSSI_IND


# TODO any reason not to set these in BleDevParams??
class BleDevParamsDefault(BleDevParams):
    def __init__(self) -> None:
        super().__init__()
        # GAP device information
        name = b"Dialog BLE"
        self.dev_name[:len(name)] = name
        # TODO do we need this gap_appearance_t   appearance;  #    GAP device appearance
        # BLE state
        self.status = BLE_STATUS.BLE_IS_DISABLED
        self.advertising = False
        self.connecting = False
        self.scanning = False
        self.role = GAP_ROLE.GAP_ROLE_NONE
        self.own_addr.addr_type = GAPM_ADDR_TYPE.GAPM_CFG_ADDR_PUBLIC
        self.own_addr.addr.addr[:] = [0x01, 0x00, 0xF4, 0x35, 0x23, 0x48]
        self.irk.key[:] = [0xEF, 0xCD, 0xAB, 0x89, 0x67, 0x45, 0x23, 0x01,
                           0xEF, 0xCD, 0xAB, 0x89, 0x67, 0x45, 0x23, 0x01]
        self.addr_resolv_req_pending = 0
        self.att_db_cfg.slv_perf_conn_params_present = True
        self.mtu_size = 65  # TODO 65 for secure connections, 23 otherwise. need to handle
        self.channel_map.map[:] = [0xFF, 0xFF, 0xFF, 0xFF, 0x1F]

        self.adv_type = GAPM_OPERATION.GAPM_ADV_UNDIRECT
        self.adv_mode = GAP_ADV_MODE.GAP_GEN_DISCOVERABLE
        self.adv_channel_map = ADV_CHANNEL_MAP.ADV_CHNL_37_EN
        self.adv_intv_min = ((687.5) * 1000 // 625)  # TODO function for this
        self.adv_intv_max = ((687.5) * 1000 // 625)  # TODO same as above
        self.adv_filter_policy = ADV_FILTER_POLICY.ADV_ALLOW_SCAN_ANY_CON_ANY  # Advertising filter policy
        self.adv_data_length = 28

        self.adv_data[0] = len(name) + 2
        self.adv_data[1] = GAP_AD_TYPE.GAP_AD_TYPE_COMPLETE_NAME
        self.adv_data[2: (2 + len(name))] = name
        self.scan_rsp_data_length = 31  # Length of scan response
        self.scan_rsp_data = (c_uint8 * SCAN_RSP_DATA_LEN)()
        # Scan parameters used for connection procedures
        self.scan_params.interval = (100) * 1000 // 625  # TODO make function
        self.scan_params.window = (50) * 1000 // 625  # TODO make function
        # Peripheral preferred connection parameters

        self.gap_ppcp.con_intv_min = ((10) * 100 // 125)
        self.gap_ppcp.con_intv_max = ((20) * 100 // 125)
        self.gap_ppcp.con_intv_min = 1000 // 10
        # IO Capabilities configuration
        self.io_capabilities = GAP_IO_CAP.GAP_IO_CAP_NO_INPUT_NO_OUTPUT
# if (dg_configBLE_PRIVACY_1_2 == 1) # TODO add privacy
        # ble_mgr_ral_op_t  prev_privacy_operation;  # TODO add privacy enum
# endif /* (dg_configBLE_PRIVACY_1_2 == 1)
# if (dg_configBLE_2MBIT_PHY == 1) # TODO 2M PHY??
        # self.tx_phy_pref_default = 0  # GAP default TX PHY preference
        # self.rx_phy_pref_default = 0  # GAP default RX PHY preference
        # self.phy_set_pending = False  # GAP PHY set operation pending
        # self.phy_change_req = False  # GAP PHY change requested
# endif /* (dg_configBLE_2MBIT_PHY == 1)
        self.conn_rssi = 0


'''
static const ble_dev_params_t default_ble_dev_params = {
        /** GAP device information */
        .dev_name              = defaultBLE_DEVICE_NAME,
        .appearance            = defaultBLE_APPEARANCE,
        /** BLE state */
        .status                = BLE_IS_DISABLED,
        /** Air operations in progress */
        .advertising           = false,
        .connecting            = false,
        .scanning              = false,
        .role                  = defaultBLE_GAP_ROLE,
        /** Privacy  parameters */
        .addr_renew_duration   = defaultBLE_ADDRESS_RENEW_DURATION,
        .own_addr = {
                .addr_type     = PUBLIC_STATIC_ADDRESS,
                .addr          = defaultBLE_STATIC_ADDRESS
        },
        .irk.key               = defaultBLE_IRK,
        .addr_resolv_req_pending = 0,
        /** Attribute database configuration */
        .att_db_cfg            = defaultBLE_ATT_DB_CONFIGURATION,
        .mtu_size              = defaultBLE_MTU_SIZE,
        /** Channel map (central only) */
        .channel_map = {
                .map           = defaultBLE_CHANNEL_MAP
        },
        /** Advertising mode configuration */
        .adv_mode              = defaultBLE_ADVERTISE_MODE,
        .adv_channel_map       = defaultBLE_ADVERTISE_CHANNEL_MAP,
        .adv_intv_min          = defaultBLE_ADVERTISE_INTERVAL_MIN,
        .adv_intv_max          = defaultBLE_ADVERTISE_INTERVAL_MAX,
        .adv_filter_policy     = defaultBLE_ADVERTISE_FILTER_POLICY,
        .adv_data_length       = defaultBLE_ADVERTISE_DATA_LENGTH,
        .adv_data              = defaultBLE_ADVERTISE_DATA,
        .scan_rsp_data_length  = defaultBLE_SCAN_RESPONSE_DATA_LENGTH,
        .scan_rsp_data         = defaultBLE_SCAN_RESPONSE_DATA,
        /** Scan parameters used for connection procedures */
        .scan_params = {
                .interval = defaultBLE_SCAN_INTERVAL,
                .window   = defaultBLE_SCAN_WINDOW
        },
        /** Peripheral preferred connection parameters */
        .gap_ppcp = {
                .interval_min  = defaultBLE_PPCP_INTERVAL_MIN,
                .interval_max  = defaultBLE_PPCP_INTERVAL_MAX,
                .slave_latency = defaultBLE_PPCP_SLAVE_LATENCY,
                .sup_timeout   = defaultBLE_PPCP_SUP_TIMEOUT
        },
        /** IO Capabilities configuration */
        .io_capabilities       = defaultBLE_GAP_IO_CAP,
#if (dg_configBLE_PRIVACY_1_2 == 1)
        .prev_privacy_operation= BLE_MGR_RAL_OP_NO_PRIVACY,
#endif /* (dg_configBLE_PRIVACY_1_2 == 1) */
#if (dg_configBLE_2MBIT_PHY == 1)
        .tx_phy_pref_default   = BLE_GAP_PHY_PREF_AUTO,
        .rx_phy_pref_default   = BLE_GAP_PHY_PREF_AUTO,
#endif /* (dg_configBLE_2MBIT_PHY == 1) */
};
'''