
from enum import IntEnum, auto
from ble_api.BleAtt import AttUuid
from ble_api.BleCommon import BLE_ERROR
from manager.BleManagerCommonMsgs import BLE_MGR_CMD_CAT, BleMgrMsgBase, BleMgrMsgRsp, BLE_CMD_GATTC_OPCODE


class BleMgrGattcBrowseCmd(BleMgrMsgBase):
    def __init__(self,
                 conn_idx: int = 0,
                 uuid: AttUuid = None) -> None:
        super().__init__(opcode=BLE_CMD_GATTC_OPCODE.BLE_MGR_GATTC_BROWSE_CMD)
        self.conn_idx = conn_idx
        self.uuid = uuid


class BleMgrGattcBrowseRsp(BleMgrMsgRsp):
    def __init__(self, status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED) -> None:
        super().__init__(opcode=BLE_CMD_GATTC_OPCODE.BLE_MGR_GATTC_BROWSE_CMD,
                         status=status)


class BleMgrGattcDiscoverCharCmd(BleMgrMsgBase):
    def __init__(self,
                 conn_idx: int = 0,
                 start_h: int = 0,
                 end_h: int = 0,
                 uuid: AttUuid = None) -> None:
        super().__init__(opcode=BLE_CMD_GATTC_OPCODE.BLE_MGR_GATTC_DISCOVER_CHAR_CMD)
        self.conn_idx = conn_idx
        self.start_h = start_h
        self.end_h = end_h
        self.uuid = uuid


class BleMgrGattcDiscoverCharRsp(BleMgrMsgRsp):
    def __init__(self, status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED) -> None:
        super().__init__(opcode=BLE_CMD_GATTC_OPCODE.BLE_MGR_GATTC_DISCOVER_CHAR_CMD,
                         status=status)


class BleMgrGattcDiscoverDescCmd(BleMgrMsgBase):
    def __init__(self,
                 conn_idx: int = 0,
                 start_h: int = 0,
                 end_h: int = 0) -> None:
        super().__init__(opcode=BLE_CMD_GATTC_OPCODE.BLE_MGR_GATTC_DISCOVER_DESC_CMD)
        self.conn_idx = conn_idx
        self.start_h = start_h
        self.end_h = end_h


class BleMgrGattcDiscoverDescRsp(BleMgrMsgRsp):
    def __init__(self, status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED) -> None:
        super().__init__(opcode=BLE_CMD_GATTC_OPCODE.BLE_MGR_GATTC_DISCOVER_DESC_CMD,
                         status=status)


class BleMgrGattcDiscoverSvcCmd(BleMgrMsgBase):
    def __init__(self, conn_idx: int = 0, uuid: AttUuid = None) -> None:
        super().__init__(opcode=BLE_CMD_GATTC_OPCODE.BLE_MGR_GATTC_DISCOVER_SVC_CMD)
        self.conn_idx = conn_idx
        self.uuid = uuid


class BleMgrGattcDiscoverSvcRsp(BleMgrMsgRsp):
    def __init__(self, status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED) -> None:
        super().__init__(opcode=BLE_CMD_GATTC_OPCODE.BLE_MGR_GATTC_DISCOVER_SVC_CMD,
                         status=status)


class BleMgrGattcReadCmd(BleMgrMsgBase):
    def __init__(self, conn_idx: int = 0, handle: int = 0, offset: int = 0) -> None:
        super().__init__(opcode=BLE_CMD_GATTC_OPCODE.BLE_MGR_GATTC_READ_CMD)
        self.conn_idx = conn_idx
        self.handle = handle
        self.offset = offset


class BleMgrGattcReadRsp(BleMgrMsgRsp):
    def __init__(self, status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED) -> None:
        super().__init__(opcode=BLE_CMD_GATTC_OPCODE.BLE_MGR_GATTC_READ_CMD,
                         status=status)


class BleMgrGattcWriteExecuteCmd(BleMgrMsgBase):
    def __init__(self,
                 conn_idx: int = 0,
                 commit: bool = False
                 ) -> None:
        super().__init__(opcode=BLE_CMD_GATTC_OPCODE.BLE_MGR_GATTC_WRITE_EXECUTE_CMD)
        self.conn_idx = conn_idx
        self.commit = commit


class BleMgrGattcWriteExecuteRsp(BleMgrMsgRsp):
    def __init__(self, status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED) -> None:
        super().__init__(opcode=BLE_CMD_GATTC_OPCODE.BLE_MGR_GATTC_WRITE_EXECUTE_CMD,
                         status=status)


class BleMgrGattcWriteGenericCmd(BleMgrMsgBase):
    def __init__(self,
                 conn_idx: int = 0,
                 handle: int = 0,
                 no_response: bool = False,
                 signed_write: bool = False,
                 prepare: bool = False,
                 offset: int = 0,
                 value: bytes = None) -> None:
        super().__init__(opcode=BLE_CMD_GATTC_OPCODE.BLE_MGR_GATTC_WRITE_GENERIC_CMD)
        self.conn_idx = conn_idx
        self.handle = handle
        self.no_response = no_response
        self.signed_write = signed_write
        self.prepare = prepare
        self.offset = offset
        self.value = value if value else None


class BleMgrGattcWriteGenericRsp(BleMgrMsgRsp):
    def __init__(self, status: BLE_ERROR = BLE_ERROR.BLE_ERROR_FAILED) -> None:
        super().__init__(opcode=BLE_CMD_GATTC_OPCODE.BLE_MGR_GATTC_WRITE_GENERIC_CMD,
                         status=status)
