
from enum import IntEnum, auto

from ..ble_api.BleAtt import AttUuid, ATT_PERM, ATT_ERROR
from ..ble_api.BleCommon import BLE_ERROR, BLE_EVT_CAT
from ..ble_api.BleGatt import GATT_SERVICE, GATT_PROP, GATT_EVENT
from ..ble_api.BleGatts import GATTS_FLAGS
from ..manager.BleManagerCommonMsgs import BleMgrMsgBase, BleMgrMsgRsp, BLE_CMD_GATTS_OPCODE


class BLE_EVT_GATTS(IntEnum):
    # Read request from ..peer
    BLE_EVT_GATTS_READ_REQ = BLE_EVT_CAT.BLE_EVT_CAT_GATTS << 8
    # Write request from ..peer
    BLE_EVT_GATTS_WRITE_REQ = auto()
    # Prepare write request from ..peer
    BLE_EVT_GATTS_PREPARE_WRITE_REQ = auto()
    # Event (notification or indication) sent
    BLE_EVT_GATTS_EVENT_SENT = auto()


class BleMgrGattsGetValueCmd(BleMgrMsgBase):
    def __init__(self,
                 handle: int = 0,
                 max_len: int = 0,
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_GET_VALUE_CMD)
        self.handle = handle
        self.max_len = max_len


class BleMgrGattsGetValueRsp(BleMgrMsgRsp):
    def __init__(self,
                 status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED,
                 value: bytes = None
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_GET_VALUE_CMD,
                         status=status)
        self.value = value if value else bytes()


class BleMgrGattsPrepareWriteCfmCmd(BleMgrMsgBase):
    def __init__(self,
                 conn_idx: int = 0,
                 handle: int = 0,
                 length: int = 0,
                 status: ATT_ERROR = ATT_ERROR.ATT_ERROR_OK,
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_PREPARE_WRITE_CFM_CMD)
        self.conn_idx = conn_idx
        self.handle = handle
        self.length = length
        self.status = status


class BleMgrGattsPrepareWriteCfmRsp(BleMgrMsgRsp):
    def __init__(self,
                 status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED,
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_PREPARE_WRITE_CFM_CMD,
                         status=status)


class BleMgrGattsReadCfmCmd(BleMgrMsgBase):
    def __init__(self,
                 conn_idx: int = 0,
                 handle: int = 0,
                 status: ATT_ERROR = ATT_ERROR.ATT_ERROR_OK,
                 value: bytes = None
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_READ_CFM_CMD)
        self.conn_idx = conn_idx
        self.handle = handle
        self.status = status
        self.value = value if value else bytes()


class BleMgrGattsReadCfmRsp(BleMgrMsgRsp):
    def __init__(self,
                 status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED,
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_READ_CFM_CMD,
                         status=status)


class BleMgrGattsSendEventCmd(BleMgrMsgBase):
    def __init__(self,
                 conn_idx: int = 0,
                 handle: int = 0,
                 type: GATT_EVENT = GATT_EVENT.GATT_EVENT_NOTIFICATION,
                 value: bytes = None
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_SEND_EVENT_CMD)
        self.conn_idx = conn_idx
        self.handle = handle
        self.type = type
        self.value = value


class BleMgrGattsSendEventRsp(BleMgrMsgRsp):
    def __init__(self,
                 status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED,
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_SEND_EVENT_CMD,
                         status=status)


class BleMgrGattsServiceAddCharacteristicCmd(BleMgrMsgBase):
    def __init__(self,
                 uuid: AttUuid = None,
                 prop: GATT_PROP = GATT_PROP.GATT_PROP_NONE,
                 perm: ATT_PERM = ATT_PERM.ATT_PERM_NONE,
                 max_len: int = 0,
                 flags: GATTS_FLAGS = GATTS_FLAGS.GATTS_FLAG_CHAR_NO_READ_REQ,
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_SERVICE_CHARACTERISTIC_ADD_CMD)
        self.uuid = uuid if uuid else AttUuid()
        self.prop = prop
        self.perm = perm
        self.max_len = max_len
        self.flags = flags


class BleMgrGattsServiceAddCharacteristicRsp(BleMgrMsgRsp):
    def __init__(self,
                 status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED,
                 h_offset: int = 0,
                 h_val_offset: int = 0
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_SERVICE_CHARACTERISTIC_ADD_CMD,
                         status=status)
        self.h_offset = h_offset
        self.h_val_offset = h_val_offset


class BleMgrGattsServiceAddCmd(BleMgrMsgBase):
    def __init__(self,
                 uuid: AttUuid = None,
                 type: GATT_SERVICE = GATT_SERVICE.GATT_SERVICE_PRIMARY,
                 num_attrs: int = 0) -> None:
        super().__init__(opcode=BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_SERVICE_ADD_CMD)
        self.uuid = uuid if uuid else AttUuid()  # TODO raise error is length off
        self.type = type
        self.num_attrs = num_attrs


class BleMgrGattsServiceAddRsp(BleMgrMsgRsp):
    def __init__(self, status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED) -> None:
        super().__init__(opcode=BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_SERVICE_ADD_CMD,
                         status=status)


class BleMgrGattsServiceAddDescriptorCmd(BleMgrMsgBase):
    def __init__(self,
                 uuid: AttUuid = None,
                 perm: ATT_PERM = ATT_PERM.ATT_PERM_NONE,
                 max_len: int = 0,
                 flags: GATTS_FLAGS = GATTS_FLAGS.GATTS_FLAG_CHAR_READ_REQ,
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_SERVICE_DESCRIPTOR_ADD_CMD)
        self.uuid = uuid if uuid else AttUuid()
        self.perm = perm
        self.max_len = max_len
        self.flags = flags


class BleMgrGattsServiceAddDescriptorRsp(BleMgrMsgRsp):
    def __init__(self,
                 status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED,
                 h_offset: int = 0,
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_SERVICE_DESCRIPTOR_ADD_CMD,
                         status=status)
        self.h_offset = h_offset


class BleMgrGattsServiceAddIncludeCmd(BleMgrMsgBase):
    def __init__(self,
                 handle: int = 0,
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_SERVICE_INCLUDE_ADD_CMD)
        self.handle = handle


class BleMgrGattsServiceAddIncludeRsp(BleMgrMsgRsp):
    def __init__(self,
                 status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED,
                 h_offset: int = 0,
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_SERVICE_INCLUDE_ADD_CMD,
                         status=status)
        self.h_offset = h_offset


class BleMgrGattsServiceRegisterCmd(BleMgrMsgBase):
    def __init__(self) -> None:
        super().__init__(opcode=BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_SERVICE_REGISTER_CMD)


class BleMgrGattsServiceRegisterRsp(BleMgrMsgRsp):
    def __init__(self,
                 status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED,
                 handle: int = 0) -> None:
        super().__init__(opcode=BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_SERVICE_REGISTER_CMD,
                         status=status)
        self.handle = handle


class BleMgrGattsSetValueCmd(BleMgrMsgBase):
    def __init__(self,
                 handle: int = 0,
                 value: bytes = None
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_SET_VALUE_CMD)
        self.handle = handle
        self.value = value if value else bytes()


class BleMgrGattsSetValueRsp(BleMgrMsgRsp):
    def __init__(self,
                 status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED,
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_SET_VALUE_CMD,
                         status=status)


class BleMgrGattsWriteCfmCmd(BleMgrMsgBase):
    def __init__(self,
                 conn_idx: int = 0,
                 handle: int = 0,
                 status: ATT_ERROR = ATT_ERROR.ATT_ERROR_OK,
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_WRITE_CFM_CMD)
        self.conn_idx = conn_idx
        self.handle = handle
        self.status = status


class BleMgrGattsWriteCfmRsp(BleMgrMsgRsp):
    def __init__(self,
                 status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED,
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GATTS_OPCODE.BLE_MGR_GATTS_WRITE_CFM_CMD,
                         status=status)
