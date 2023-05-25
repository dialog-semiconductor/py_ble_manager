from enum import IntEnum, auto
from ..gtl_port.gap import GAP_KDIST


class BLE_DEVICE_TYPE(IntEnum):
    NONE = 0
    CENTRAL = auto()
    PERIPHERAL = auto()
    OBSERVER = auto()
    BROADCASTER = auto()


class BleConfigDefault():
    """Default configuration for various BLE parameters
    """
    def __init__(self, ble_device_type: BLE_DEVICE_TYPE = BLE_DEVICE_TYPE.CENTRAL):

        self.dg_configBLE_SECURE_CONNECTIONS = (1)
        self.dg_configBLE_PAIR_INIT_KEY_DIST = (GAP_KDIST.GAP_KDIST_ENCKEY | GAP_KDIST.GAP_KDIST_IDKEY | GAP_KDIST.GAP_KDIST_SIGNKEY)
        self.dg_configBLE_PAIR_RESP_KEY_DIST = (GAP_KDIST.GAP_KDIST_ENCKEY | GAP_KDIST.GAP_KDIST_IDKEY | GAP_KDIST.GAP_KDIST_SIGNKEY)
        self.dg_configBLE_PRIVACY_1_2 = (0)

        self.dg_configBLE_CENTRAL = 1 if ble_device_type == BLE_DEVICE_TYPE.CENTRAL else 0
        self.dg_configBLE_PERIPHERAL = 1 if ble_device_type == BLE_DEVICE_TYPE.PERIPHERAL else 0
        self.dg_configBLE_OBSERVER = 1 if ble_device_type == BLE_DEVICE_TYPE.OBSERVER else 0
        self.dg_configBLE_BROADCASTER = 1 if ble_device_type == BLE_DEVICE_TYPE.BROADCASTER else 0

        self.dg_configBLE_DATA_LENGTH_RX_MAX = 251
        self.dg_configBLE_DATA_LENGTH_TX_MAX = 251
        self.defaultBLE_STATIC_ADDRESS = bytes([0x01, 0x00, 0xF4, 0x35, 0x23, 0x48])

        assert ((self.dg_configBLE_DATA_LENGTH_RX_MAX < 251) or (self.dg_configBLE_DATA_LENGTH_RX_MAX > 27))
        assert ((self.dg_configBLE_DATA_LENGTH_TX_MAX < 251) or (self.dg_configBLE_DATA_LENGTH_TX_MAX > 27))


# define dg_configBLE_OBSERVER                (1)
# define dg_configBLE_BROADCASTER             (1)
# define dg_configBLE_CENTRAL                 (1)
# define dg_configBLE_PERIPHERAL              (1)
# define dg_configBLE_GATT_CLIENT             (1)
# define dg_configBLE_GATT_SERVER             (1)
# define dg_configBLE_L2CAP_COC               (1)

# define dg_configBLE_EVENT_COUNTER_ENABLE    (0)
# define dg_configBLE_ADV_STOP_DELAY_ENABLE   (0)
# define dg_configBLE_SKIP_LATENCY_API        (0)
# define dg_configBLE_PRIVACY_1_2             (0)
# define dg_configBLE_DATA_LENGTH_RX_MAX      (251)
# define dg_configBLE_DATA_LENGTH_TX_MAX      (251)

# define dg_configBLE_DATA_LENGTH_REQ_UPON_CONN  (0)

# define dg_configBLE_CONN_EVENT_LENGTH_MIN \
#        ( (BLE_DATA_LENGTH_TO_TIME(dg_configBLE_DATA_LENGTH_RX_MAX) \
#         + BLE_DATA_LENGTH_TO_TIME(dg_configBLE_DATA_LENGTH_TX_MAX) + 150 + 624) / 625)

# if (dg_configBLE_CONN_EVENT_LENGTH_MIN > 8)
        # undef dg_configBLE_CONN_EVENT_LENGTH_MIN
        # define dg_configBLE_CONN_EVENT_LENGTH_MIN (8)
# endif
# elif defined(dg_configBLE_CONN_EVENT_LENGTH_MAX) \
#        && (dg_configBLE_CONN_EVENT_LENGTH_MIN > dg_configBLE_CONN_EVENT_LENGTH_MAX)
# error "dg_configBLE_CONN_EVENT_LENGTH_MIN must be lower or equal to dg_configBLE_CONN_EVENT_LENGTH_MAX."
# endif


# define dg_configBLE_CONN_EVENT_LENGTH_MAX   (0xFFFF)

# define dg_configBLE_DUPLICATE_FILTER_MAX    (10)
# elif ((dg_configBLE_DUPLICATE_FILTER_MAX < 10) || (dg_configBLE_DUPLICATE_FILTER_MAX > 255))
# error "dg_configBLE_DUPLICATE_FILTER_MAX value must be between 10 and 255."
# endif

# define dg_configBLE_PAIR_INIT_KEY_DIST      (GAP_KDIST_ENCKEY | GAP_KDIST_IDKEY | GAP_KDIST_SIGNKEY)

# define dg_configBLE_PAIR_RESP_KEY_DIST      (GAP_KDIST_ENCKEY | GAP_KDIST_IDKEY | GAP_KDIST_SIGNKEY)

# define dg_configBLE_SECURE_CONNECTIONS      (1)

# define dg_configBLE_USE_HIGH_PERFORMANCE_1M    (1)
# define dg_configBLE_USE_HIGH_PERFORMANCE_2M    (1)

# define dg_configBLE_GOLDEN_RANGE_LOW        (-70)
# define dg_configBLE_GOLDEN_RANGE_UP         (-40)
# define dg_configBLE_GOLDEN_RANGE_PREF       (-55)
# define dg_configBLE_PCLE_MIN_TX_PWR_IDX     (GAP_TX_POWER_MINUS_26_dBm)
# define dg_configBLE_PCLE_MAX_TX_PWR_IDX     (GAP_TX_POWER_MAX)
# define dg_configBLE_INITIAL_TX_POWER        (GAP_TX_POWER_0_dBm)

# define dg_configRF_CALIB_TEMP_DIFF          (8)
# define dg_configRF_CALIB_TEMP_POLL_INTV     (1000)


# define defaultBLE_DEVICE_NAME               "Dialog BLE"
# define defaultBLE_APPEARANCE                (0)

# define defaultBLE_MAX_CONNECTIONS           (CFG_CON)
# elif ( (DEVICE_FAMILY == DA1469X) && (defaultBLE_MAX_CONNECTIONS != CFG_CON) )
# error "Values different than the BLE stack library default (CFG_CON) are not currently supported."
# endif

# define defaultBLE_MAX_BONDED                (8)

# define defaultBLE_GAP_ROLE                  GAP_NO_ROLE

'''
/**
 * \brief Default random address renew duration
 *
 * Default duration for random address generation when a random resolvable or a random
 * non-resolvable address has been set using ble_gap_address_set().
 *
 * \note Value is in seconds (valid range is 1 to 3600 seconds. Out of range values will be ignored)
 *
 * \bsp_default_note{\bsp_config_option_app,}
 */
# ifndef defaultBLE_ADDRESS_RENEW_DURATION
# define defaultBLE_ADDRESS_RENEW_DURATION    (900)    // 900 seconds (15 minutes)
# endif

/**
 * \brief Default static BD address
 *
 * Default static BD address set if one is not retrieved from the non-volatile storage.
 *
 * \bsp_default_note{\bsp_config_option_app,}
 */
# ifndef defaultBLE_STATIC_ADDRESS
# define defaultBLE_STATIC_ADDRESS            { 0x01, 0x00, 0xF4, 0x35, 0x23, 0x48 }
# endif

/**
 * \brief Default BD address type
 *
 * Default BD address type used if one is not set using ble_gap_address_set().
 *
 * \bsp_default_note{\bsp_config_option_app,}
 */
# ifndef defaultBLE_ADDRESS_TYPE
# define defaultBLE_ADDRESS_TYPE              PUBLIC_ADDRESS
# endif

/**
 * \brief Default Identity Resolution Key
 *
 * Default Identity Resolution Key to be used upon IRK exchange.
 *
 * \bsp_default_note{\bsp_config_option_app,}
 */
# ifndef defaultBLE_IRK
# define defaultBLE_IRK                       { 0xEF, 0xCD, 0xAB, 0x89, 0x67, 0x45, 0x23, 0x01, \
                                               0xEF, 0xCD, 0xAB, 0x89, 0x67, 0x45, 0x23, 0x01 }
# endif

/**
 * \brief Default attribute database configuration
 *
 * \verbatim
 * Default attribute database configuration:
 *     7     6    5     4     3    2    1    0
 * +-----+-----+----+-----+-----+----+----+----+
 * | DBG | RFU | SC | PCP | APP_PERM |NAME_PERM|
 * +-----+-----+----+-----+-----+----+----+----+
 * - Bit [0-1]: Device Name write permission requirements for peer device (see gapm_write_att_perm)
 * - Bit [2-3]: Device Appearance write permission requirements for peer device (see gapm_write_att_perm)
 * - Bit [4]  : Slave Preferred Connection Parameters present
 * - Bit [5]  : Service change feature present in GATT attribute database.
 * - Bit [6]  : Reserved
 * - Bit [7]  : Enable Debug Mode
 * endverbatim
 *
 * \bsp_default_note{\bsp_config_option_app, \bsp_config_option_expert_only}
 */
# ifndef defaultBLE_ATT_DB_CONFIGURATION
# define defaultBLE_ATT_DB_CONFIGURATION      (0x10)     // Peripheral Pref. Conn. Parameters present
# endif

/**
 * \brief Maximum MTU size
 *
 * Maximum supported MTU size.
 *
 * \bsp_default_note{\bsp_config_option_app, \bsp_config_option_expert_only}
 */
# ifndef defaultBLE_MAX_MTU_SIZE
# define defaultBLE_MAX_MTU_SIZE              (512)
# endif

/**
 * \brief Minimum MTU size
 *
 * Minimum supported MTU size as defined by Bluetooth SIG:
 * - 23 when LE Secure Connections are not used.
 * - 65 when LE Secure Connections are used.
 *
 * \bsp_default_note{\bsp_config_option_app, \bsp_config_option_expert_only}
 */
# ifndef defaultBLE_MIN_MTU_SIZE
# if (dg_configBLE_SECURE_CONNECTIONS == 1)
# define defaultBLE_MIN_MTU_SIZE              (65)
#else
# define defaultBLE_MIN_MTU_SIZE              (23)
# endif
#elif (((dg_configBLE_SECURE_CONNECTIONS == 1) \
                && (defaultBLE_MIN_MTU_SIZE < 65)) \
        || ((dg_configBLE_SECURE_CONNECTIONS == 0) \
                && (defaultBLE_MIN_MTU_SIZE < 23)) \
        || (defaultBLE_MIN_MTU_SIZE > defaultBLE_MAX_MTU_SIZE))
# error "defaultBLE_MIN_MTU_SIZE set out of supported range!"
# endif

/**
 * \brief Default MTU size
 *
 * Default MTU size used on MTU exchange negotiations if one is not set using ble_gap_mtu_size_set().
 *
 * \bsp_default_note{\bsp_config_option_app,}
 */
# ifndef defaultBLE_MTU_SIZE
# define defaultBLE_MTU_SIZE                  (defaultBLE_MIN_MTU_SIZE)
#elif ((defaultBLE_MTU_SIZE < defaultBLE_MIN_MTU_SIZE) \
        || (defaultBLE_MTU_SIZE > defaultBLE_MAX_MTU_SIZE))
# error "defaultBLE_MTU_SIZE set out of supported range!"
# endif

/**
 * \brief Default channel map (for central role only)
 *
 * Default channel map used when device is configured with the central role if one is not set using
 * ble_gap_channel_map_set().
 *
 * \bsp_default_note{\bsp_config_option_app,}
 */
# ifndef defaultBLE_CHANNEL_MAP
# define defaultBLE_CHANNEL_MAP               {0xFF, 0xFF, 0xFF, 0xFF, 0x1F}  // All channels enabled
# endif

/**
 * \brief Default advertising mode
 *
 * Default mode used for advertising if one is not set using ble_gap_adv_mode_set().
 *
 * \bsp_default_note{\bsp_config_option_app,}
 */
# ifndef defaultBLE_ADVERTISE_MODE
# define defaultBLE_ADVERTISE_MODE            GAP_DISC_MODE_GEN_DISCOVERABLE
# endif

/**
 * \brief Default channels used for advertising
 *
 * Default channel used for advertising if they are not set using ble_gap_adv_chnl_map_set().
 *
 * \bsp_default_note{\bsp_config_option_app,}
 */
# ifndef defaultBLE_ADVERTISE_CHANNEL_MAP
# define defaultBLE_ADVERTISE_CHANNEL_MAP     (GAP_ADV_CHANNEL_37 | GAP_ADV_CHANNEL_38 | GAP_ADV_CHANNEL_39)
# endif

/**
 * \brief Default minimum interval used for advertising
 *
 * Default minimum interval used for advertising in steps of 0.625ms if one is not set using
 * ble_gap_adv_intv_set().
 *
 * \bsp_default_note{\bsp_config_option_app,}
 */
# ifndef defaultBLE_ADVERTISE_INTERVAL_MIN
# define defaultBLE_ADVERTISE_INTERVAL_MIN    (BLE_ADV_INTERVAL_FROM_MS(687.5))  // 687.5ms
# endif

/**
 * \brief Default maximum interval used for advertising
 *
 * Default maximum interval used for advertising in steps of 0.625ms if one is not set using
 * ble_gap_adv_intv_set().
 *
 * \bsp_default_note{\bsp_config_option_app,}
 */
# ifndef defaultBLE_ADVERTISE_INTERVAL_MAX
# define defaultBLE_ADVERTISE_INTERVAL_MAX    (BLE_ADV_INTERVAL_FROM_MS(687.5))  // 687.5ms
# endif

/**
 * \brief Default filtering policy used for advertising
 *
 * Default filtering policy used for advertising if one is not set using ble_gap_adv_filt_policy_set().
 *
 * \note Whitelist management API is not present in this release, so setting a filtering policy for
 *       advertising is not possible.
 *
 * \bsp_default_note{\bsp_config_option_app,}
 */
# ifndef defaultBLE_ADVERTISE_FILTER_POLICY
# define defaultBLE_ADVERTISE_FILTER_POLICY   ADV_ALLOW_SCAN_ANY_CONN_ANY
# endif

/**
 * \brief Default advertising data length
 *
 * Default length of advertising data. This is set to the maximum value allowed by the stack, which
 * is 28 bytes.
 *
 * \bsp_default_note{\bsp_config_option_app,}
 */
# ifndef defaultBLE_ADVERTISE_DATA_LENGTH
# define defaultBLE_ADVERTISE_DATA_LENGTH     (28)
# endif

/**
 * \brief Default advertising Data
 *
 * Default advertising data are set to advertise the device name. If the application
 * should have specific advertising data, these should be set using the ble_gap_adv_data_set().
 *
 * \note Changing #defaultBLE_DEVICE_NAME won't change the device name included by default in the
 *       advertising data.
 *
 * \bsp_default_note{\bsp_config_option_app,}
 */
# ifndef defaultBLE_ADVERTISE_DATA
# define defaultBLE_ADVERTISE_DATA            { 0x0C, GAP_DATA_TYPE_LOCAL_NAME, \
                                               'D', 'i', 'a', 'l', 'o', 'g', ' ', 'B', 'L', 'E' }
# endif

/**
 * \brief Default scan response data length
 *
 * Default length of scan response data. This is set to the maximum value allowed by the stack,
 * which is 31 bytes.
 *
 * \bsp_default_note{\bsp_config_option_app,}
 */
# ifndef defaultBLE_SCAN_RESPONSE_DATA_LENGTH
# define defaultBLE_SCAN_RESPONSE_DATA_LENGTH (31)
# endif

/**
 * \brief Default scan response Data
 *
 * Default scan response data are set to zero. If the application should have specific scan response
 * data, these should be set using the ble_gap_adv_data_set().
 *
 * \note Changing #defaultBLE_DEVICE_NAME won't change the device name included by default in the
 *       scan response data.
 *
 * \bsp_default_note{\bsp_config_option_app,}
 */
# ifndef defaultBLE_SCAN_RESPONSE_DATA
# define defaultBLE_SCAN_RESPONSE_DATA        { }
# endif

/**
 * \brief Default scan interval
 *
 * Default interval used for scanning in steps of 0.625ms if one is not set using
 * ble_gap_scan_params_set().
 *
 * \bsp_default_note{\bsp_config_option_app, \bsp_config_option_expert_only}
 */
# ifndef defaultBLE_SCAN_INTERVAL
# define defaultBLE_SCAN_INTERVAL             (BLE_SCAN_INTERVAL_FROM_MS(100))   // 100ms
# endif

/**
 * \brief Default scan window
 *
 * Default window used for scanning in steps of 0.625ms if one is not set using
 * ble_gap_scan_params_set().
 *
 * \bsp_default_note{\bsp_config_option_app, \bsp_config_option_expert_only}
 */
# ifndef defaultBLE_SCAN_WINDOW
# define defaultBLE_SCAN_WINDOW               (BLE_SCAN_WINDOW_FROM_MS(50))      // 50ms
# endif

/**
 * \brief Default peripheral preferred minimum connection interval
 *
 * Default minimum connection interval set in the peripheral preferred connection parameters
 * attribute in steps of 1.25ms if one is not set using ble_gap_per_pref_conn_params_set().
 *
 * \bsp_default_note{\bsp_config_option_app, \bsp_config_option_expert_only}
 */
# ifndef defaultBLE_PPCP_INTERVAL_MIN
# define defaultBLE_PPCP_INTERVAL_MIN         (BLE_CONN_INTERVAL_FROM_MS(10))    // 10ms
# endif

/**
 * \brief Default peripheral preferred maximum connection interval
 *
 * Default maximum connection interval set in the peripheral preferred connection parameters
 * attribute in steps of 1.25ms if one is not set using ble_gap_per_pref_conn_params_set().
 *
 * \bsp_default_note{\bsp_config_option_app, \bsp_config_option_expert_only}
 */
# ifndef defaultBLE_PPCP_INTERVAL_MAX
# define defaultBLE_PPCP_INTERVAL_MAX         (BLE_CONN_INTERVAL_FROM_MS(20))    // 20ms
# endif

/**
 * \brief Default peripheral preferred slave latency
 *
 * Default slave latency set in the peripheral preferred connection parameters attribute in number
 * of events if one is not set using ble_gap_per_pref_conn_params_set().
 *
 * \bsp_default_note{\bsp_config_option_app, \bsp_config_option_expert_only}
 */
# ifndef defaultBLE_PPCP_SLAVE_LATENCY
# define defaultBLE_PPCP_SLAVE_LATENCY        (0)          // number of events
# endif

/**
 * \brief Default peripheral preferred supervision timeout
 *
 * Default supervision timeout set in the peripheral preferred connection parameters attribute in
 * steps of 10ms if one is not set using ble_gap_per_pref_conn_params_set().
 *
 * \bsp_default_note{\bsp_config_option_app, \bsp_config_option_expert_only}
 */
# ifndef defaultBLE_PPCP_SUP_TIMEOUT
# define defaultBLE_PPCP_SUP_TIMEOUT          (BLE_SUPERVISION_TMO_FROM_MS(1000)) // 1s
# endif

/**
 * \brief Default Input/Output capabilities
 *
 * Default input/output capabilities set for pairing procedures if they are not set using the
 * ble_gap_set_io_cap().
 *
 * \bsp_default_note{\bsp_config_option_app,}
 */
# ifndef defaultBLE_GAP_IO_CAP
# define defaultBLE_GAP_IO_CAP                GAP_IO_CAP_NO_INPUT_OUTPUT
# endif

/**
 * \brief Device Information Service default data
 *
 * \bsp_default_note{\bsp_config_option_app,}
 */
# ifndef defaultBLE_DIS_MANUFACTURER
# define defaultBLE_DIS_MANUFACTURER          "Dialog Semiconductor"
# endif

# ifndef defaultBLE_DIS_MODEL_NUMBER
# define defaultBLE_DIS_MODEL_NUMBER          "Dialog BLE"
# endif

# ifndef defaultBLE_DIS_SERIAL_NUMBER
# define defaultBLE_DIS_SERIAL_NUMBER         "SN123456"
# endif

# ifndef defaultBLE_DIS_HW_REVISION
# define defaultBLE_DIS_HW_REVISION           "Rev.D"
# endif

# ifndef defaultBLE_DIS_FW_REVISION
# define defaultBLE_DIS_FW_REVISION           "1.0"
# endif

# ifndef defaultBLE_DIS_SW_REVISION
# define defaultBLE_DIS_SW_REVISION           "1.1"
# endif

# ifndef defaultBLE_DIS_PNP_VID_SOURCE
# define defaultBLE_DIS_PNP_VID_SOURCE        (0x01)
# endif

# ifndef defaultBLE_DIS_PNP_VID
# define defaultBLE_DIS_PNP_VID               (0x00D2)
# endif

# ifndef defaultBLE_DIS_PNP_PID
# define defaultBLE_DIS_PNP_PID               (0x0001)
# endif

# ifndef defaultBLE_DIS_PNP_VERSION
# define defaultBLE_DIS_PNP_VERSION           (0x0001)
# endif

/* IEEE 11073-20601 Regulatory Certification Data List Characteristic */
# ifndef defaultBLE_DIS_REGULATORY_CERT
# define defaultBLE_DIS_REGULATORY_CERT       { 0x00, 0x02, 0x00, 0x12, 0x02, 0x01, 0x00, 0x08, 0x01, \
                                               0x05, 0x00, 0x01, 0x00, 0x02, 0x80, 0x08, 0x02, 0x02, \
                                               0x00, 0x02, 0x00, 0x00 }
# endif

# ifndef defaultBLE_DIS_SYSTEM_ID_OUI
# define defaultBLE_DIS_SYSTEM_ID_OUI         { 0x48, 0x23, 0x35 }
# endif

# ifndef defaultBLE_DIS_SYSTEM_ID_MANUFACTURER
# define defaultBLE_DIS_SYSTEM_ID_MANUFACTURER  { 0x0A, 0x0B, 0x0C, 0x0D, 0x0E }
# endif

/**
 * \brief Use passthrough mode
 *
 * If application has enabled the external host configuration, BLE stack is configured for
 * pass-through mode.
 *
 */
# ifdef BLE_EXTERNAL_HOST
# define BLE_STACK_PASSTHROUGH_MODE
# define BLE_MGR_DIRECT_ACCESS   0
# endif

/**
 * \brief Use BLE sleep mode
 *
 * Macro #USE_BLE_SLEEP controls whether BLE will be set to sleep when it is not needed to be
 * active.
 *
 * \bsp_default_note{\bsp_config_option_app, \bsp_config_option_expert_only}
 */
# ifndef USE_BLE_SLEEP
#               define USE_BLE_SLEEP           1
# endif

/**
 * \brief Wake Up Latency
 *
 * Defines the Wake Up Latency expressed in Low Power clock cycles, that is
 * the number of LP clock cycles needed for the BLE to be fully operational
 * (calculations and BLE timer synchronization)
 *
 * \bsp_default_note{\bsp_config_option_app, \bsp_config_option_expert_only}
 */
# ifndef BLE_WUP_LATENCY
# if ((dg_configUSE_LP_CLK == LP_CLK_32000) || (dg_configUSE_LP_CLK == LP_CLK_32768))
# ifdef RELEASE_BUILD
        # if (dg_configCODE_LOCATION != NON_VOLATILE_IS_FLASH)   // RAM, OTP
                # define BLE_WUP_LATENCY        8
        #else                                                   // Flash
                # define BLE_WUP_LATENCY        9
        # endif
#else                                                           // !RELEASE_BUILD
        # if (dg_configCODE_LOCATION != NON_VOLATILE_IS_FLASH)
                # define BLE_WUP_LATENCY        16
        #else
                # define BLE_WUP_LATENCY        32
        # endif
# endif // RELEASE_BUILD

#elif (dg_configUSE_LP_CLK == LP_CLK_RCX) // RCX

# ifdef RELEASE_BUILD
        # if (dg_configCODE_LOCATION != NON_VOLATILE_IS_FLASH)
                # define BLE_WUP_LATENCY        cm_rcx_us_2_lpcycles(300)
        #else
                # define BLE_WUP_LATENCY        cm_rcx_us_2_lpcycles(300)
        # endif
#else // !RELEASE_BUILD
        # if (dg_configCODE_LOCATION != NON_VOLATILE_IS_FLASH)
                # define BLE_WUP_LATENCY        cm_rcx_us_2_lpcycles(500)
        #else
                # define BLE_WUP_LATENCY        cm_rcx_us_2_lpcycles(1000)
        # endif
# endif // RELEASE_BUILD

# endif
# endif

/**
 * \addtogroup BLE_EVENT_NOTIFICATIONS
 *
 * \brief Doxygen documentation is not yet available for this module.
 *        Please check the source code file(s)
 *
 * \bsp_default_note{\bsp_config_option_app, \bsp_config_option_expert_only}
 *
 * {
 */
/* -----------------------------------BLE event notifications configuration --------------------- */

/*
 * BLE ISR event Notifications
 *
 * This facility enables the user app to receive notifications for BLE
 * ISR events. These events can be received either directly from inside
 * the BLE ISR, or as task notifications to the Application Task
 * registered to the BLE manager.
 *
 * To enable, define dg_configBLE_EVENT_NOTIF_TYPE to either
 * BLE_EVENT_NOTIF_USER_ISR or BLE_EVENT_NOTIF_USER_TASK.
 *
 * - When dg_configBLE_EVENT_NOTIF_TYPE == BLE_EVENT_NOTIF_USER_ISR, the user
 *   can define the following macros on his app configuration:
 *
 *   dg_configBLE_EVENT_NOTIF_HOOK_END_EVENT    : The BLE End Event
 *   dg_configBLE_EVENT_NOTIF_HOOK_CSCNT_EVENT  : The BLE CSCNT Event
 *   dg_configBLE_EVENT_NOTIF_HOOK_FINE_EVENT   : The BLE FINE Event
 *
 *   These macros must be actually set to the names of functions defined inside
 *   the user application, having a prototype of
 *
 *     void func(void);
 *
 *   (The user app does not need to explicitly define the prototype).
 *
 *   If one of these macros is not defined, the respective notification
 *   will be suppressed.
 *
 *   Note that these functions will be called in ISR context, directly from the
 *   BLE ISR. They should therefore be very fast and should NEVER block.
 *
 * - When dg_configBLE_EVENT_NOTIF_TYPE == BLE_EVENT_NOTIF_USER_TASK, the user
 *   app will receive task notifications on the task registered to the BLE
 *   manager.
 *
 *   Notifications will be received using the following bit masks:
 *
 *   - dg_configBLE_EVENT_NOTIF_MASK_END_EVENT: End Event Mask (Def: bit 24)
 *   - dg_configBLE_EVENT_NOTIF_MASK_CSCNT_EVENT: CSCNT Event Mask (Def: bit 25)
 *   - dg_configBLE_EVENT_NOTIF_MASK_FINE_EVENT: FINE Event Mask (Def: bit 26)
 *
 *   These macros, defining the task notification bit masks, can be redefined as
 *   needed.
 *
 *   If one of the macros for callback functions presented in the previous
 *   section (for direct ISR notifications) is defined, while in this mode,
 *   the function with the same name will be called directly from the isr
 *   instead of sending a task notification for this particular event to
 *   the app task.
 *
 *   Macro dg_configBLE_EVENT_NOTIF_RUNTIME_CONTROL (Default: 1) enables/disables
 *   runtime control/masking of notifications.
 *
 *   If dg_configBLE_EVENT_NOTIF_RUNTIME_CONTROL == 1, then task notifications
 *   must be enabled/disabled using the
 *   ble_event_notif_[enable|disable]_[end|cscnt|fine]_event() functions.
 *   By default all notifications are disabled.
 *
 *   If dg_configBLE_EVENT_NOTIF_RUNTIME_CONTROL == 0, all notifications will
 *   be sent unconditionally to the application task.
 *
 */
# ifndef dg_configBLE_EVENT_NOTIF_TYPE
# define dg_configBLE_EVENT_NOTIF_TYPE BLE_EVENT_NOTIF_USER_ISR
# endif

# if dg_configBLE_EVENT_NOTIF_TYPE == BLE_EVENT_NOTIF_USER_TASK

/* Default implementation of BLE event task notifications. This
 * implementation allows a user task to register for notifications,
 * and to get task notifications for the available events
 */

/* Default task notification masks for the various events for which
 * the framework provides notifications
 */
# ifndef dg_configBLE_EVENT_NOTIF_MASK_END_EVENT
# define dg_configBLE_EVENT_NOTIF_MASK_END_EVENT         (1 << 24)
# endif

# ifndef dg_configBLE_EVENT_NOTIF_MASK_CSCNT_EVENT
# define dg_configBLE_EVENT_NOTIF_MASK_CSCNT_EVENT       (1 << 25)
# endif

# ifndef dg_configBLE_EVENT_NOTIF_MASK_FINE_EVENT
# define dg_configBLE_EVENT_NOTIF_MASK_FINE_EVENT        (1 << 26)
# endif

/* Implement event hook functions */
# ifndef dg_configBLE_EVENT_NOTIF_HOOK_END_EVENT
# define dg_configBLE_EVENT_NOTIF_HOOK_END_EVENT         ble_event_notif_app_task_end_event
# endif

# ifndef dg_configBLE_EVENT_NOTIF_HOOK_CSCNT_EVENT
# define dg_configBLE_EVENT_NOTIF_HOOK_CSCNT_EVENT       ble_event_notif_app_task_cscnt_event
# endif

# ifndef dg_configBLE_EVENT_NOTIF_HOOK_FINE_EVENT
# define dg_configBLE_EVENT_NOTIF_HOOK_FINE_EVENT        ble_event_notif_app_task_fine_event
# endif

/*
 * Allow runtime control of (un)masking notifications
 */
# ifndef dg_configBLE_EVENT_NOTIF_RUNTIME_CONTROL
# define dg_configBLE_EVENT_NOTIF_RUNTIME_CONTROL        1
# endif

# endif
/* ---------------------------------------------------------------------------------------------- */

/**
 * }
 */

/**
 * }
 */

/**
 * \brief Enable 2MBIT PHY
 *
 * This is defined by default to 1 to enable LE 2MBIT PHY.
 */
# define dg_configBLE_2MBIT_PHY               (1)

# endif /* _BLE_CONFIG_H_ */
/**
 }
 }
 */
'''
