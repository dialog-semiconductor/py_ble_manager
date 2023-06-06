from enum import IntEnum


# Tasks types definition, this value shall be in [0-254] range
class KE_API_ID(IntEnum):
    # Link Layer Tasks
    TASK_ID_LLM = 0
    TASK_ID_LLC = 1
    TASK_ID_LLD = 2
    TASK_ID_DBG = 3

    # BT Controller Tasks
    TASK_ID_LM = 4
    TASK_ID_LC = 5
    TASK_ID_LB = 6
    TASK_ID_LD = 7

    TASK_ID_HCI = 8
    TASK_ID_DISPLAY = 9

    TASK_ID_L2CC = 10
    TASK_ID_GATTM = 11   # Generic Attribute Profile Manager Task
    TASK_ID_GATTC = 12   # Generic Attribute Profile Controller Task
    TASK_ID_GAPM = 13   # Generic Access Profile Manager
    TASK_ID_GAPC = 14   # Generic Access Profile Controller

    TASK_ID_APP = 15
    TASK_ID_GTL = 16

    # -----------------------------------------------------------------------------------
    # --------------------- BLE Profile TASK API Identifiers ----------------------------
    # -----------------------------------------------------------------------------------
    TASK_ID_DISS = 20   # Device Information Service Server Task
    TASK_ID_DISC = 21   # Device Information Service Client Task

    TASK_ID_PROXM = 22   # Proximity Monitor Task
    TASK_ID_PROXR = 23   # Proximity Reporter Task

    TASK_ID_FINDL = 24   # Find Me Locator Task
    TASK_ID_FINDT = 25   # Find Me Target Task

    TASK_ID_HTPC = 26   # Health Thermometer Collector Task
    TASK_ID_HTPT = 27   # Health Thermometer Sensor Task

    TASK_ID_BLPS = 28   # Blood Pressure Sensor Task
    TASK_ID_BLPC = 29   # Blood Pressure Collector Task

    TASK_ID_HRPS = 30   # Heart Rate Sensor Task
    TASK_ID_HRPC = 31   # Heart Rate Collector Task

    TASK_ID_TIPS = 32   # Time Server Task
    TASK_ID_TIPC = 33   # Time Client Task

    TASK_ID_SCPPS = 34   # Scan Parameter Profile Server Task
    TASK_ID_SCPPC = 35   # Scan Parameter Profile Client Task

    TASK_ID_BASS = 36   # Battery Service Server Task
    TASK_ID_BASC = 37   # Battery Service Client Task

    TASK_ID_HOGPD = 38   # HID Device Task
    TASK_ID_HOGPBH = 39   # HID Boot Host Task
    TASK_ID_HOGPRH = 40   # HID Report Host Task

    TASK_ID_GLPS = 41   # Glucose Profile Sensor Task
    TASK_ID_GLPC = 42   # Glucose Profile Collector Task

    TASK_ID_RSCPS = 43   # Running Speed and Cadence Profile Server Task
    TASK_ID_RSCPC = 44   # Running Speed and Cadence Profile Collector Task

    TASK_ID_CSCPS = 45   # Cycling Speed and Cadence Profile Server Task
    TASK_ID_CSCPC = 46   # Cycling Speed and Cadence Profile Client Task

    TASK_ID_ANPS = 47   # Alert Notification Profile Server Task
    TASK_ID_ANPC = 48   # Alert Notification Profile Client Task

    TASK_ID_PASPS = 49   # Phone Alert Status Profile Server Task
    TASK_ID_PASPC = 50   # Phone Alert Status Profile Client Task

    TASK_ID_CPPS = 51   # Cycling Power Profile Server Task
    TASK_ID_CPPC = 52   # Cycling Power Profile Client Task

    TASK_ID_LANS = 53   # Location and Navigation Profile Server Task
    TASK_ID_LANC = 54   # Location and Navigation Profile Client Task

    TASK_ID_BMSS = 55   # Bond Management Service Server Task
    TASK_ID_BMSC = 56   # Bond Management Service Client Task

    TASK_ID_BCSS = 57   # Body Composition Server
    TASK_ID_BCSC = 58   # Body Composition Client

    TASK_ID_UDSS = 59   # User Data Service Server Task
    TASK_ID_UDSC = 60   # User Data Service Client Task

    TASK_ID_WSSS = 61   # Weight Scale Service Server Task
    TASK_ID_WSSC = 62   # Weight Scale Service Client Task

    TASK_ID_CTSS = 63   # Current Time Service Server Task
    TASK_ID_CTSC = 64   # Current Time Service Client Task

    TASK_ID_ANCC = 65   # Apple Notification Center Service Client Task

    TASK_ID_GATT_CLIENT = 66   # Generic Attribute Profile Service Client Task

    TASK_ID_SUOTAR = 0xFC  # Software Patching Over The Air Receiver

    TASK_ID_CUSTS1 = 0xFD  # Custom1 Task
    TASK_ID_CUSTS2 = 0xFE  # Custom2 Task

    TASK_ID_INVALID = 0xFF  # Invalid Task Identifier
