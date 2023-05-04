'''
/* Services UUIDs */
#define UUID_SERVICE_GAS                        (0x1800) // Generic Access Service
#define UUID_SERVICE_GATT                       (0x1801) // Generic Attribute
#define UUID_SERVICE_IAS                        (0x1802) // Immediate Alert Service
#define UUID_SERVICE_LLS                        (0x1803) // Link Loss Service
#define UUID_SERVICE_TPS                        (0x1804) // Tx Power Service
#define UUID_SERVICE_CTS                        (0x1805) // Current Time Service
#define UUID_SERVICE_RTUS                       (0x1806) // Reference Time Update Service
#define UUID_SERVICE_NDCS                       (0x1807) // Next DST Change Service
#define UUID_SERVICE_GLS                        (0x1808) // Glucose Service
#define UUID_SERVICE_HTS                        (0x1809) // Health Thermometer Service
#define UUID_SERVICE_DIS                        (0x180A) // Device Information Service
#define UUID_SERVICE_HRS                        (0x180D) // Heart Rate Service
#define UUID_SERVICE_PASS                       (0x180E) // Phone Alert Status Service
#define UUID_SERVICE_BAS                        (0x180F) // Battery Service
#define UUID_SERVICE_BLS                        (0x1810) // Blood Pressure Service
#define UUID_SERVICE_AND                        (0x1811) // Alert Notification Service
#define UUID_SERVICE_HIDS                       (0x1812) // Human Interface Device Service
#define UUID_SERVICE_SCPS                       (0x1813) // Scan Parameters Service
#define UUID_SERVICE_RSCS                       (0x1814) // Running Speed and Cadence Service
#define UUID_SERVICE_CSCS                       (0x1816) // Cycling Speed and Cadence Service
#define UUID_SERVICE_CPS                        (0x1818) // Cycling Power Service
#define UUID_SERVICE_LNS                        (0x1819) // Location and Navigation Service
#define UUID_SERVICE_ESS                        (0x181A) // Environmental Sensing Service
#define UUID_SERVICE_BCS                        (0x181B) // Body Composition Service
#define UUID_SERVICE_UDS                        (0x181C) // User Data Service
#define UUID_SERVICE_WSS                        (0x181D) // Weight Scale Service
#define UUID_SERVICE_BMS                        (0x181E) // Bond Management Service
#define UUID_SERVICE_CGMS                       (0x181F) // Continuous Glucose Monitoring Service
#define UUID_SERVICE_IPSS                       (0x1820) // Internet Protocol Support Service
#define UUID_SERVICE_IPS                        (0x1821) // Indoor Positioning Service

/* GATT UUIDs */
#define UUID_GATT_PRIMARY_SERVICE               (0x2800)
#define UUID_GATT_SECONDARY_SERVICE             (0x2801)
#define UUID_GATT_INCLUDE                       (0x2802)
#define UUID_GATT_CHARACTERISTIC                (0x2803)

/* GATT descriptors UUIDs */
'''

UUID_GATT_CHAR_EXT_PROPERTIES = (0x2900)
UUID_GATT_CHAR_USER_DESCRIPTION = (0x2901)
# define UUID_GATT_CLIENT_CHAR_CONFIGURATION     (0x2902)
# define UUID_GATT_SERVER_CHAR_CONFIGURATION     (0x2903)
# define UUID_GATT_CHAR_PRESENTATION_FORMAT      (0x2904)
# define UUID_GATT_CHAR_AGGREGATE_FORMAT         (0x2905)


# def ble_uuid_create16(uuid16, uuid: att_uuid):
#        uuid->type = ATT_UUID_TYPE.ATT_UUID_16;
#        uuid->uuid16 = uuid16;
# }
