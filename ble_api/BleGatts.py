from enum import IntEnum, auto
from .BleAtt import att_uuid, ATT_PERM  # ATT_ERROR, ATT_UUID_TYPE
from .BleGatt import GATT_SERVICE, GATT_PROP, GATT_EVENT
from manager.BleManagerGatts import BleMgrGattsServiceAddCmd, BleMgrGattsServiceAddRsp, \
    BleMgrGattsServiceAddCharacteristicCmd, BleMgrGattsServiceAddCharacteristicRsp, \
    BleMgrGattsServiceAddDescriptorCmd, BleMgrGattsServiceAddDescriptorRsp, \
    BleMgrGattsServiceRegisterCmd, BleMgrGattsServiceRegisterRsp
from manager.BleManager import BLE_ERROR  # BleManager
from manager.BleManagerGatts import GATTS_FLAGS
# from adapter.BleAdapter import BleAdapter
from .BleCommon import BleEventBase, BLE_EVT_CAT
from .BleApiBase import BleApiBase
from manager.BleManager import BleManager
from adapter.BleAdapter import BleAdapter


class BLE_EVT_GATTS(IntEnum):
    # Read request from peer
    BLE_EVT_GATTS_READ_REQ = BLE_EVT_CAT.BLE_EVT_CAT_GATTS << 8
    # Write request from peer
    BLE_EVT_GATTS_WRITE_REQ = auto()
    # Prepare write request from peer
    BLE_EVT_GATTS_PREPARE_WRITE_REQ = auto()
    # Event (notification or indication) sent
    BLE_EVT_GATTS_EVENT_SENT = auto()


class BleEventGattsReadReq(BleEventBase):
    def __init__(self,
                 conn_idx: int = 0,
                 handle: int = 0,
                 offset: int = 0,
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GATTS.BLE_EVT_GATTS_READ_REQ)
        self.conn_idx = conn_idx
        self.handle = handle
        self.offset = offset


class BleEventGattsWriteReq(BleEventBase):
    def __init__(self,
                 conn_idx: int = 0,
                 handle: int = 0,
                 offset: int = 0,
                 length: int = 0,
                 value: list = 0,
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GATTS.BLE_EVT_GATTS_WRITE_REQ)
        self.conn_idx = conn_idx
        self.handle = handle
        self.offset = offset
        self.length = length
        self.value = value if value else []


class BleEventGattsPrepareWriteReq(BleEventBase):
    def __init__(self,
                 conn_idx: int = 0,
                 handle: int = 0,
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GATTS.BLE_EVT_GATTS_PREPARE_WRITE_REQ)
        self.conn_idx = conn_idx
        self.handle = handle


class BleEventGattsEventSent(BleEventBase):
    def __init__(self,
                 conn_idx: int = 0,
                 handle: int = 0,
                 type: GATT_EVENT = GATT_EVENT.GATT_EVENT_NOTIFICATION,
                 status: bool = False
                 ) -> None:
        super().__init__(evt_code=BLE_EVT_GATTS.BLE_EVT_GATTS_EVENT_SENT)
        self.conn_idx = conn_idx
        self.handle = handle
        self.type = type
        self.status = status


class BleGatts(BleApiBase):

    def __init__(self, ble_manager: BleManager, ble_adapter: BleAdapter):
        super().__init__(ble_manager, ble_adapter)

    async def add_characteristic(self,
                                 uuid: att_uuid = att_uuid(),
                                 prop: GATT_PROP = GATT_PROP.GATT_PROP_NONE,
                                 perm: ATT_PERM = ATT_PERM.ATT_PERM_NONE,
                                 max_len: int = 0,
                                 flags: GATTS_FLAGS = GATTS_FLAGS.GATTS_FLAG_CHAR_READ_REQ,
                                 ) -> tuple[BLE_ERROR, int, int]:

        response = BLE_ERROR.BLE_ERROR_FAILED

        command = BleMgrGattsServiceAddCharacteristicCmd(uuid, prop, perm, max_len, flags)

        response: BleMgrGattsServiceAddCharacteristicRsp = await self.ble_manager.cmd_execute(command)

        # TODO just return response instead?
        return response.status, response.h_offset, response.h_val_offset

    async def add_descriptor(self,
                             uuid: att_uuid = att_uuid(),
                             prop: GATT_PROP = GATT_PROP.GATT_PROP_NONE,
                             perm: ATT_PERM = ATT_PERM.ATT_PERM_NONE,
                             max_len: int = 0,
                             flags: GATTS_FLAGS = GATTS_FLAGS.GATTS_FLAG_CHAR_READ_REQ,
                             ) -> tuple[BLE_ERROR, int]:

        response = BLE_ERROR.BLE_ERROR_FAILED

        command = BleMgrGattsServiceAddDescriptorCmd(uuid, prop, perm, max_len, flags)

        response: BleMgrGattsServiceAddDescriptorRsp = await self.ble_manager.cmd_execute(command)

        return response.status, response.h_offset

    async def add_service(self,
                          uuid: att_uuid = None,
                          type: GATT_SERVICE = GATT_SERVICE.GATT_SERVICE_PRIMARY,
                          num_attrs: int = 0
                          ) -> BLE_ERROR:

        response = BLE_ERROR.BLE_ERROR_FAILED

        command = BleMgrGattsServiceAddCmd(uuid, type, num_attrs)

        response: BleMgrGattsServiceAddRsp = await self.ble_manager.cmd_execute(command)

        return response.status

    def get_num_attr(num_included_svcs: int = 0, num_chars: int = 0, num_descriptors: int = 0) -> int:
        return (1 * num_included_svcs) + (2 * num_chars) + (1 * num_descriptors)

    async def register_service(self, *handles) -> BLE_ERROR:

        response = BLE_ERROR.BLE_ERROR_FAILED

        command = BleMgrGattsServiceRegisterCmd()

        response: BleMgrGattsServiceRegisterRsp = await self.ble_manager.cmd_execute(command)

        if handles:
            handles[0] = response.handle
            for i in range(1, len(handles)):
                handles[i] = handles[i] + response.handle

        return response.status
