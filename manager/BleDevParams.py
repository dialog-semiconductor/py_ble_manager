from ctypes import c_uint8

from ble_api.BleCommon import BLE_OWN_ADDR_TYPE, BdAddress, OwnAddress, Irk, BLE_STATUS
from ble_api.BleGap import BLE_GAP_ROLE, BLE_GAP_CONN_MODE, BLE_GAP_APPEARANCE, GapChnlMap, GAP_DISC_MODE, ADV_FILT_POL, \
    GapScanParams, GapConnParams, GAP_IO_CAPABILITIES, GAP_DATA_TYPE
from gtl_port.co_bt import ADV_DATA_LEN, SCAN_RSP_DATA_LEN, ADV_CHANNEL_MAP
from gtl_port.gapm_task import gapm_att_cfg_flag


class BleDevParams():

    def __init__(self) -> None:
        # GAP device information
        # TODO Max len + null char. Should we create property
        # TODO just make a string, convert in dev_params to gtl
        self.dev_name = b""  # (c_uint8 * (BD_NAME_SIZE + 1))()  # GAP device name plus NULL char # TODO F8 seems realy long

        self.appearance = BLE_GAP_APPEARANCE.BLE_GAP_APPEARANCE_UNKNOWN  # GAP device appearance
        # BLE state
        self.status = BLE_STATUS.BLE_IS_DISABLED  # Status of the BLE stack
        # Air operations in progress
        self.advertising = False   # Advertising operation in progress
        self.connecting = False  # Connection operation in progress
        self.scanning = False  # Scanning operation in progress
        self.role = BLE_GAP_ROLE.GAP_NO_ROLE  # Enabled roles for the device

        # Privacy parameters
        self.addr_renew_duration = 0  # Random address renew duration
        # TODO ble_manager seems to redefine own_addr_t
        self.own_addr = OwnAddress()  # Provided own public address
        # TODO redefines irk_t
        self.irk = Irk()  # IRK for device resolvable address
        self.addr_resolv_req_pending = 0  # Pending address resolve requests
        # Attribute database configuration

        self.att_db_cfg = gapm_att_cfg_flag()  # Attribute DB Configuration bitmask
        self.mtu_size = 0  # MTU size
        # Channel map (central only)
        self.channel_map = GapChnlMap()  # Channel map # TODO use ble apis
        # TODO one of GAPM_ADV_NON_CONN, GAPM_ADV_UNDIRECT, GAPM_ADV_DIRECT, GAPM_ADV_DIRECT_LDC
        self.adv_type = BLE_GAP_CONN_MODE.GAP_CONN_MODE_UNDIRECTED  # Advertising type
        self.adv_mode = GAP_DISC_MODE.GAP_DISC_MODE_GEN_DISCOVERABLE  # Discoverability mode for adv. # TODO use ble api
        self.adv_channel_map = ADV_CHANNEL_MAP.ADV_ALL_CHNLS_EN  # Channel map used for advertising  # TODO use ble api
        self.adv_intv_min = 0  # Minimum advertising interval
        self.adv_intv_max = 0  # Maximum advertising interval
        self.adv_filter_policy = ADV_FILT_POL.ADV_ALLOW_SCAN_ANY_CONN_ANY  # Advertising filter policy  # TODO use ble api
        self.adv_direct_address = BdAddress()  # Address used for directed advertising  # TODO use ble api
        self.adv_data_length = 0  # Length of advertising data
        self.adv_data = (c_uint8 * ADV_DATA_LEN)()  # Advertising data  # TODO use ble api
        self.scan_rsp_data_length = 0  # Length of scan response
        self.scan_rsp_data = (c_uint8 * SCAN_RSP_DATA_LEN)()  # Scan response data  # TODO use ble api
        # Scan parameters used for connection procedures
        self.scan_params = GapScanParams()  # Scan parameters # TODO does this struct exist in gtl_port files?  # TODO use ble api
        # Peripheral preferred connection parameters
        self.gap_ppcp = GapConnParams()  # Connection parameters structure  # TODO use ble api
        # IO Capabilities configuration
        self.io_capabilities = GAP_IO_CAPABILITIES.GAP_IO_CAP_NO_INPUT_OUTPUT  # GAP IO capabilities  # TODO use ble api
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
        # self.dev_name[:len(name)] = name
        self.dev_name = name
        self.appearance = BLE_GAP_APPEARANCE.BLE_GAP_APPEARANCE_UNKNOWN
        # BLE state
        self.status = BLE_STATUS.BLE_IS_DISABLED
        self.advertising = False
        self.connecting = False
        self.scanning = False
        self.role = BLE_GAP_ROLE.GAP_NO_ROLE
        self.addr_renew_duration = 900
        self.own_addr.addr_type = BLE_OWN_ADDR_TYPE.PUBLIC_STATIC_ADDRESS
        self.own_addr.addr = bytes([0x01, 0x00, 0xF4, 0x35, 0x23, 0x48])
        self.irk.key = bytes([0xEF, 0xCD, 0xAB, 0x89, 0x67, 0x45, 0x23, 0x01,
                              0xEF, 0xCD, 0xAB, 0x89, 0x67, 0x45, 0x23, 0x01])
        self.addr_resolv_req_pending = 0
        self.att_db_cfg.slv_perf_conn_params_present = True
        self.mtu_size = 23  # TODO 65 for secure connections, 23 otherwise. need to handle
        self.channel_map.map = bytes([0xFF, 0xFF, 0xFF, 0xFF, 0x1F])

        self.adv_type = BLE_GAP_CONN_MODE.GAP_CONN_MODE_UNDIRECTED
        self.adv_mode = GAP_DISC_MODE.GAP_DISC_MODE_GEN_DISCOVERABLE
        self.adv_channel_map = ADV_CHANNEL_MAP.ADV_CHNL_37_EN  # TODO use gap_adv_chnl_t
        self.adv_intv_min = int(((687.5) * 1000 // 625))  # TODO function for this
        self.adv_intv_max = int(((687.5) * 1000 // 625))  # TODO same as above
        self.adv_filter_policy = ADV_FILT_POL.ADV_ALLOW_SCAN_ANY_CONN_ANY
        self.adv_data_length = 28

        self.adv_data[0] = len(name) + 1  # SDK has 0x0C? Should be 0x0B??
        self.adv_data[1] = GAP_DATA_TYPE.GAP_DATA_TYPE_LOCAL_NAME
        self.adv_data[2: (2 + len(name))] = name
        self.scan_rsp_data_length = 0  # Length of scan response
        self.scan_rsp_data = (c_uint8 * SCAN_RSP_DATA_LEN)()
        # Scan parameters used for connection procedures
        self.scan_params.interval = (100) * 1000 // 625  # TODO make function
        self.scan_params.window = (50) * 1000 // 625  # TODO make function
        # Peripheral preferred connection parameters

        self.gap_ppcp.interval_min = ((500) * 100 // 125)
        self.gap_ppcp.interval_max = ((750) * 100 // 125)
        self.gap_ppcp.slave_latency = 0
        self.gap_ppcp.sup_timeout = 6000 // 10
        # IO Capabilities configuration
        self.io_capabilities = GAP_IO_CAPABILITIES.GAP_IO_CAP_NO_INPUT_OUTPUT  # TODO use BLE Enum instead of gtl
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
