from ctypes import c_uint8

from ..ble_api.BleCommon import BLE_OWN_ADDR_TYPE, BdAddress, OwnAddress, Irk, BLE_STATUS
from ..ble_api.BleGap import BLE_GAP_ROLE, GAP_CONN_MODE, GAP_APPEARANCE, GapChnlMap, GAP_DISC_MODE, ADV_FILT_POL, \
    GapScanParams, GapConnParams, GAP_IO_CAPABILITIES, GAP_DATA_TYPE, BLE_NON_CONN_ADV_DATA_LEN_MAX, SCAN_RSP_DATA_LEN, GAP_ADV_CHANNEL, BLE_GAP_PHY
from ..gtl_port.gapm_task import gapm_att_cfg_flag
from ..manager.BleManagerGapMsgs import BLE_MGR_RAL_OP


class BleDevParams():

    def __init__(self) -> None:
        # GAP device information
        self.dev_name = b""  # GAP device name

        self.appearance = GAP_APPEARANCE.BLE_GAP_APPEARANCE_UNKNOWN  # GAP device appearance
        # BLE state
        self.status = BLE_STATUS.BLE_IS_DISABLED  # Status of the BLE stack
        # Air operations in progress
        self.advertising = False   # Advertising operation in progress
        self.connecting = False  # Connection operation in progress
        self.scanning = False  # Scanning operation in progress
        self.role = BLE_GAP_ROLE.GAP_NO_ROLE  # Enabled roles for the device

        # Privacy parameters
        self.addr_renew_duration = 0  # Random address renew duration
        self.own_addr = OwnAddress()  # Provided own public address
        self.irk = Irk()  # IRK for device resolvable address
        self.addr_resolv_req_pending = 0  # Pending address resolve requests
        # Attribute database configuration

        self.att_db_cfg = gapm_att_cfg_flag()
        self.mtu_size = 0  # MTU size
        # Channel map (central only)
        self.channel_map = GapChnlMap()  # Channel map #
        self.adv_type = GAP_CONN_MODE.GAP_CONN_MODE_UNDIRECTED  # Advertising type
        self.adv_mode = GAP_DISC_MODE.GAP_DISC_MODE_GEN_DISCOVERABLE  # Discoverability mode for adv.=
        self.adv_channel_map = (GAP_ADV_CHANNEL.GAP_ADV_CHANNEL_37
                                | GAP_ADV_CHANNEL.GAP_ADV_CHANNEL_38
                                | GAP_ADV_CHANNEL.GAP_ADV_CHANNEL_39)  # Channel map used for advertising
        self.adv_intv_min_ms = 0  # Minimum advertising interval
        self.adv_intv_max_ms = 0  # Maximum advertising interval
        self.adv_filter_policy = ADV_FILT_POL.ADV_ALLOW_SCAN_ANY_CONN_ANY  # Advertising filter policy
        self.adv_direct_address = BdAddress()  # Address used for directed advertising
        self.adv_data_length = 0  # Length of advertising data
        self.adv_data = (c_uint8 * BLE_NON_CONN_ADV_DATA_LEN_MAX)()  # Advertising data
        self.scan_rsp_data_length = 0  # Length of scan response
        self.scan_rsp_data = (c_uint8 * SCAN_RSP_DATA_LEN)()  # Scan response data
        # Scan parameters used for connection procedures
        self.scan_params = GapScanParams()  # Scan parameters
        # Peripheral preferred connection parameters
        self.gap_ppcp = GapConnParams()  # Connection parameters structure
        # IO Capabilities configuration
        self.io_capabilities = GAP_IO_CAPABILITIES.GAP_IO_CAP_NO_INPUT_OUTPUT  # GAP IO capabilities

        # Only relevant for dg_configBLE_PRIVACY_1_2 == 1
        self.prev_privacy_operation = BLE_MGR_RAL_OP.BLE_MGR_RAL_OP_NO_PRIVACY
        # end (dg_configBLE_PRIVACY_1_2 == 1)
        # Only relevant for dg_configBLE_2MBIT_PHY == 1
        self.tx_phy_pref_default = BLE_GAP_PHY.BLE_GAP_PHY_PREF_AUTO  # GAP default TX PHY preference
        self.rx_phy_pref_default = BLE_GAP_PHY.BLE_GAP_PHY_PREF_AUTO  # GAP default RX PHY preference
        self.phy_set_pending = False  # GAP PHY set operation pending
        self.phy_change_req = False  # GAP PHY change requested
        # end (dg_configBLE_2MBIT_PHY == 1)
        self.conn_rssi = 0  # The RSSI reading reported by GAPC_CON_RSSI_IND


# defined in ble_mgr.c
class BleDevParamsDefault(BleDevParams):
    def __init__(self) -> None:
        super().__init__()
        # GAP device information
        self.dev_name = b"Dialog BLE"
        self.appearance = GAP_APPEARANCE.BLE_GAP_APPEARANCE_UNKNOWN
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

        # TODO Any issue always setting to 65 even if dg_configBLE_SECURE_CONNECTIONS = 0?
        self.mtu_size = 65  # 23  # 65 for secure connections, 23 otherwise
        self.channel_map.map = bytes([0xFF, 0xFF, 0xFF, 0xFF, 0x1F])

        self.adv_type = GAP_CONN_MODE.GAP_CONN_MODE_UNDIRECTED
        self.adv_mode = GAP_DISC_MODE.GAP_DISC_MODE_GEN_DISCOVERABLE
        self.adv_channel_map = (GAP_ADV_CHANNEL.GAP_ADV_CHANNEL_37
                                | GAP_ADV_CHANNEL.GAP_ADV_CHANNEL_38
                                | GAP_ADV_CHANNEL.GAP_ADV_CHANNEL_39)
        self.adv_intv_min_ms = 687.5
        self.adv_intv_max_ms = 687.5
        self.adv_filter_policy = ADV_FILT_POL.ADV_ALLOW_SCAN_ANY_CONN_ANY
        self.adv_data_length = 28

        self.adv_data[0] = len(self.dev_name) + 1  # SDK has 0x0C? Should be 0x0B??
        self.adv_data[1] = GAP_DATA_TYPE.GAP_DATA_TYPE_LOCAL_NAME
        self.adv_data[2:(2 + len(self.dev_name))] = self.dev_name
        self.scan_rsp_data_length = 0  # Length of scan response
        self.scan_rsp_data = (c_uint8 * SCAN_RSP_DATA_LEN)()

        # Scan parameters used for connection procedures
        self.scan_params.interval_ms = 100
        self.scan_params.window_ms = 50

        # Peripheral preferred connection parameters
        self.gap_ppcp.interval_min_ms = 500
        self.gap_ppcp.interval_max_ms = 750
        self.gap_ppcp.slave_latency = 0
        self.gap_ppcp.sup_timeout_ms = 6000
        # IO Capabilities configuration
        self.io_capabilities = GAP_IO_CAPABILITIES.GAP_IO_CAP_NO_INPUT_OUTPUT
        # Only relevant for dg_configBLE_PRIVACY_1_2 == 1
        self.prev_privacy_operation = BLE_MGR_RAL_OP.BLE_MGR_RAL_OP_NO_PRIVACY
        # end (dg_configBLE_PRIVACY_1_2 == 1)
        # Only relevant for dg_configBLE_2MBIT_PHY == 1
        self.tx_phy_pref_default = BLE_GAP_PHY.BLE_GAP_PHY_PREF_AUTO  # GAP default TX PHY preference
        self.rx_phy_pref_default = BLE_GAP_PHY.BLE_GAP_PHY_PREF_AUTO  # GAP default RX PHY preference
        self.phy_set_pending = False  # GAP PHY set operation pending
        self.phy_change_req = False
        # end (dg_configBLE_2MBIT_PHY == 1)
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
