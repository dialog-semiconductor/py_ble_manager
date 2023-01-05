
from enum import IntEnum, auto

from ble_api.BleAtt import att_uuid, ATT_PERM
from ble_api.BleCommon import BLE_ERROR, BLE_EVT_CAT
from ble_api.BleGatt import GATT_SERVICE, GATT_PROP
from ble_api.BleGatts import GATTS_FLAGS
from manager.BleManagerCommonMsgs import BleMgrMsgBase, BLE_MGR_CMD_CAT


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


class BLE_EVT_GATTS(IntEnum):
    # Read request from peer
    BLE_EVT_GATTS_READ_REQ = BLE_EVT_CAT.BLE_EVT_CAT_GATTS << 8
    # Write request from peer
    BLE_EVT_GATTS_WRITE_REQ = auto()
    # Prepare write request from peer
    BLE_EVT_GATTS_PREPARE_WRITE_REQ = auto()
    # Event (notification or indication) sent
    BLE_EVT_GATTS_EVENT_SENT = auto()


class BleMgrGattsServiceAddCharacteristicCmd(BleMgrMsgBase):
    def __init__(self,
                 uuid: att_uuid = att_uuid(),
                 prop: GATT_PROP = GATT_PROP.GATT_PROP_NONE,
                 perm: ATT_PERM = ATT_PERM.ATT_PERM_NONE,
                 max_len: int = 0,
                 flags: GATTS_FLAGS = GATTS_FLAGS.GATTS_FLAG_CHAR_NO_READ_REQ,
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_SERVICE_CHARACTERISTIC_ADD_CMD)
        self.uuid = uuid
        self.prop = prop
        self.perm = perm
        self.max_len = max_len
        self.flags = flags


class BleMgrGattsServiceAddCharacteristicRsp(BleMgrMsgBase):
    def __init__(self,
                 status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED,
                 h_offset: int = 0,
                 h_val_offset: int = 0
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_SERVICE_CHARACTERISTIC_ADD_CMD)
        self.status = status
        self.h_offset = h_offset
        self.h_val_offset = h_val_offset


class BleMgrGattsServiceAddCmd(BleMgrMsgBase):
    def __init__(self,
                 uuid: att_uuid = None,
                 type: GATT_SERVICE = GATT_SERVICE.GATT_SERVICE_PRIMARY,
                 num_attrs: int = 0) -> None:
        super().__init__(opcode=BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_SERVICE_ADD_CMD)
        self.uuid = uuid if uuid else []  # TODO raise error is length off
        self.type = type
        self.num_attrs = num_attrs


class BleMgrGattsServiceAddRsp(BleMgrMsgBase):
    def __init__(self, status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED) -> None:
        super().__init__(opcode=BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_SERVICE_ADD_CMD)
        self.status = status


class BleMgrGattsServiceAddDescriptorCmd(BleMgrMsgBase):
    def __init__(self,
                 uuid: att_uuid = att_uuid(),
                 perm: ATT_PERM = ATT_PERM.ATT_PERM_NONE,
                 max_len: int = 0,
                 flags: GATTS_FLAGS = GATTS_FLAGS.GATTS_FLAG_CHAR_READ_REQ,
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_SERVICE_DESCRIPTOR_ADD_CMD)
        self.uuid = uuid
        self.perm = perm
        self.max_len = max_len
        self.flags = flags


class BleMgrGattsServiceAddDescriptorRsp(BleMgrMsgBase):
    def __init__(self,
                 status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED,
                 h_offset: int = 0,
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_SERVICE_DESCRIPTOR_ADD_CMD)
        self.status = status
        self.h_offset = h_offset


class BleMgrGattsServiceRegisterCmd(BleMgrMsgBase):
    def __init__(self) -> None:
        super().__init__(opcode=BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_SERVICE_REGISTER_CMD)


class BleMgrGattsServiceRegisterRsp(BleMgrMsgBase):
    def __init__(self,
                 status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED,
                 handle: int = 0) -> None:
        super().__init__(opcode=BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_SERVICE_REGISTER_CMD)
        self.status = status
        self.handle = handle


class BleMgrGattsReadCfmCmd(BleMgrMsgBase):
    def __init__(self,
                 conn_idx: int = 0,
                 handle: int = 0,
                 status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED,
                 value: list[int] = None
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_READ_CFM_CMD)
        self.conn_idx = conn_idx
        self.handle = handle
        self.status = status
        self.value = value


class BleMgrGattsReadCfmRsp(BleMgrMsgBase):
    def __init__(self,
                 status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED,
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_READ_CFM_CMD)
        self.status = status


class BleMgrGattsSetValueCmd(BleMgrMsgBase):
    def __init__(self,
                 handle: int = 0,
                 value: bytes = None
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_SET_VALUE_CMD)
        self.handle = handle
        self.value = value


class BleMgrGattsSetValueRsp(BleMgrMsgBase):
    def __init__(self,
                 status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED,
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_SET_VALUE_CMD)
        self.status = status
