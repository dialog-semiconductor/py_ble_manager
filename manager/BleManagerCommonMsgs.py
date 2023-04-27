from enum import IntEnum, auto

from ble_api.BleCommon import BLE_ERROR


class BLE_MGR_CMD_CAT(IntEnum):
    BLE_MGR_COMMON_CMD_CAT = 0x00
    BLE_MGR_GAP_CMD_CAT = 0x01
    BLE_MGR_GATTS_CMD_CAT = 0x02
    BLE_MGR_GATTC_CMD_CAT = 0x03
    BLE_MGR_L2CAP_CMD_CAT = 0x04
    BLE_MGR_LAST_CMD_CAT = auto()


class BLE_MGR_COMMON_CMD_OPCODE(IntEnum):
    BLE_MGR_COMMON_STACK_MSG = BLE_MGR_CMD_CAT.BLE_MGR_COMMON_CMD_CAT << 8
    BLE_MGR_COMMON_REGISTER_CMD = auto()
    BLE_MGR_COMMON_ENABLE_CMD = auto()
    BLE_MGR_COMMON_RESET_CMD = auto()
    BLE_MGR_COMMON_READ_TX_POWER_CMD = auto()
    # Dummy command opcode, needs to be always defined after all commands
    BLE_MGR_COMMON_LAST_CMD = auto()


class BLE_CMD_GAP_OPCODE(IntEnum):
    BLE_MGR_GAP_ADDRESS_SET_CMD = BLE_MGR_CMD_CAT.BLE_MGR_GAP_CMD_CAT << 8
    BLE_MGR_GAP_DEVICE_NAME_SET_CMD = auto()
    BLE_MGR_GAP_APPEARANCE_SET_CMD = auto()
    BLE_MGR_GAP_PPCP_SET_CMD = auto()
    BLE_MGR_GAP_ADV_START_CMD = auto()
    BLE_MGR_GAP_ADV_STOP_CMD = auto()
    BLE_MGR_GAP_ADV_DATA_SET_CMD = auto()
    BLE_MGR_GAP_ADV_SET_PERMUTATION_CMD = auto()
    BLE_MGR_GAP_SCAN_START_CMD = auto()
    BLE_MGR_GAP_SCAN_STOP_CMD = auto()
    BLE_MGR_GAP_CONNECT_CMD = auto()
    BLE_MGR_GAP_CONNECT_CANCEL_CMD = auto()
    BLE_MGR_GAP_DISCONNECT_CMD = auto()
    BLE_MGR_GAP_PEER_VERSION_GET_CMD = auto()
    BLE_MGR_GAP_PEER_FEATURES_GET_CMD = auto()
    BLE_MGR_GAP_CONN_RSSI_GET_CMD = auto()
    BLE_MGR_GAP_ROLE_SET_CMD = auto()
    BLE_MGR_GAP_MTU_SIZE_SET_CMD = auto()
    BLE_MGR_GAP_CHANNEL_MAP_SET_CMD = auto()
    BLE_MGR_GAP_CONN_PARAM_UPDATE_CMD = auto()
    BLE_MGR_GAP_CONN_PARAM_UPDATE_REPLY_CMD = auto()
    BLE_MGR_GAP_PAIR_CMD = auto()
    BLE_MGR_GAP_PAIR_REPLY_CMD = auto()
    BLE_MGR_GAP_PASSKEY_REPLY_CMD = auto()
    BLE_MGR_GAP_UNPAIR_CMD = auto()
    BLE_MGR_GAP_SET_SEC_LEVEL_CMD = auto()
# if (dg_configBLE_SKIP_LATENCY_API == 1) # TODO need to handle these defines
    BLE_MGR_GAP_SKIP_LATENCY_CMD = auto()
# endif /* (dg_configBLE_SKIP_LATENCY_API == 1)
    BLE_MGR_GAP_DATA_LENGTH_SET_CMD = auto()
# if (dg_configBLE_SECURE_CONNECTIONS == 1)
    BLE_MGR_GAP_NUMERIC_REPLY_CMD = auto()
# endif /* (dg_configBLE_SECURE_CONNECTIONS == 1)
    BLE_MGR_GAP_ADDRESS_RESOLVE_CMD = auto()
# if (dg_configBLE_2MBIT_PHY == 1)
    BLE_MGR_GAP_PHY_SET_CMD = auto()
# endif /* (dg_configBLE_2MBIT_PHY == 1)
    BLE_MGR_GAP_TX_POWER_SET_CMD = auto()
    BLE_MGR_GAP_CONN_TX_POWER_SET_CMD = auto()
    BLE_MGR_GAP_LOCAL_TX_POWER_GET_CMD = auto()
    BLE_MGR_GAP_REMOTE_TX_POWER_GET_CMD = auto()
    BLE_MGR_GAP_PATH_LOSS_REPORT_PARAMS_SET_CMD = auto()
    BLE_MGR_GAP_PATH_LOSS_REPORT_EN_CMD = auto()
    BLE_MGR_GAP_TX_PWR_REPORT_EN_CMD = auto()
    BLE_MGR_GAP_RF_PATH_COMPENSATION_SET_CMD = auto()
    BLE_MGR_GAP_LAST_CMD = auto()


class BLE_CMD_GATTC_OPCODE(IntEnum):
    BLE_MGR_GATTC_BROWSE_CMD = BLE_MGR_CMD_CAT.BLE_MGR_GATTC_CMD_CAT << 8
    BLE_MGR_GATTC_BROWSE_RANGE_CMD = auto()
    BLE_MGR_GATTC_DISCOVER_SVC_CMD = auto()
    BLE_MGR_GATTC_DISCOVER_INCLUDE_CMD = auto()
    BLE_MGR_GATTC_DISCOVER_CHAR_CMD = auto()
    BLE_MGR_GATTC_DISCOVER_DESC_CMD = auto()
    BLE_MGR_GATTC_READ_CMD = auto()
    BLE_MGR_GATTC_WRITE_GENERIC_CMD = auto()
    BLE_MGR_GATTC_WRITE_EXECUTE_CMD = auto()
    BLE_MGR_GATTC_EXCHANGE_MTU_CMD = auto()
    BLE_MGR_GATTC_LAST_CMD = auto()


class BLE_CMD_GATTS_OPCODE(IntEnum):
    BLE_MGR_GATTS_SERVICE_ADD_CMD = BLE_MGR_CMD_CAT.BLE_MGR_GATTS_CMD_CAT << 8
    BLE_MGR_GATTS_SERVICE_INCLUDE_ADD_CMD = auto()
    BLE_MGR_GATTS_SERVICE_CHARACTERISTIC_ADD_CMD = auto()
    BLE_MGR_GATTS_SERVICE_DESCRIPTOR_ADD_CMD = auto()
    BLE_MGR_GATTS_SERVICE_REGISTER_CMD = auto()
    BLE_MGR_GATTS_SERVICE_ENABLE_CMD = auto()
    BLE_MGR_GATTS_SERVICE_DISABLE_CMD = auto()
    BLE_MGR_GATTS_SERVICE_CHARACTERISTIC_GET_PROP_CMD = auto()
    BLE_MGR_GATTS_SERVICE_CHARACTERISTIC_SET_PROP_CMD = auto()
    BLE_MGR_GATTS_GET_VALUE_CMD = auto()
    BLE_MGR_GATTS_SET_VALUE_CMD = auto()
    BLE_MGR_GATTS_READ_CFM_CMD = auto()
    BLE_MGR_GATTS_WRITE_CFM_CMD = auto()
    BLE_MGR_GATTS_PREPARE_WRITE_CFM_CMD = auto()
    BLE_MGR_GATTS_SEND_EVENT_CMD = auto()
    BLE_MGR_GATTS_SERVICE_CHANGED_IND_CMD = auto()
    BLE_MGR_GATTS_LAST_CMD = auto()


# OP codes for L2CAP commands
class BLE_CMD_L2CAP_OPCODE(IntEnum):
    BLE_MGR_L2CAP_LISTEN_CMD = BLE_MGR_CMD_CAT.BLE_MGR_L2CAP_CMD_CAT << 8
    BLE_MGR_L2CAP_STOP_LISTEN_CMD = 1
    BLE_MGR_L2CAP_CONNECTION_CFM_CMD = 2
    BLE_MGR_L2CAP_CONNECT_CMD = 3
    BLE_MGR_L2CAP_DISCONNECT_CMD = 4
    BLE_MGR_L2CAP_ADD_CREDITS_CMD = 5
    BLE_MGR_L2CAP_SEND_CMD = 6
    BLE_MGR_L2CAP_LAST_CMD = 7


class BleMgrMsgBase():
    def __init__(self,
                 opcode: (BLE_MGR_COMMON_CMD_OPCODE
                          | BLE_CMD_GAP_OPCODE
                          | BLE_CMD_GATTS_OPCODE
                          | BLE_CMD_GATTC_OPCODE
                          | BLE_CMD_L2CAP_OPCODE),
                 ) -> None:
        self.opcode = opcode


class BleMgrMsgRsp(BleMgrMsgBase):  # TODO reponses should inherit fromm this class instead of BleMgrMsgBase
    def __init__(self,
                 opcode: (BLE_MGR_COMMON_CMD_OPCODE
                          | BLE_CMD_GAP_OPCODE
                          | BLE_CMD_GATTS_OPCODE
                          | BLE_CMD_GATTC_OPCODE
                          | BLE_CMD_L2CAP_OPCODE),
                 status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED) -> None:
        self.status = status
        super().__init__(opcode=opcode)


class BleMgrCommonResetCmd(BleMgrMsgBase):
    def __init__(self) -> None:
        super().__init__(opcode=BLE_MGR_COMMON_CMD_OPCODE.BLE_MGR_COMMON_RESET_CMD)


class BleMgrCommonResetRsp(BleMgrMsgRsp):
    def __init__(self, status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED) -> None:
        super().__init__(opcode=BLE_MGR_COMMON_CMD_OPCODE.BLE_MGR_COMMON_RESET_CMD,
                         status=status)
