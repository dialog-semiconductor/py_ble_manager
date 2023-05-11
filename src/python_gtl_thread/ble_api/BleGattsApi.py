from ..adapter.BleAdapter import BleAdapter
from ..ble_api.BleApiBase import BleApiBase
from ..ble_api.BleAtt import AttUuid, ATT_PERM, ATT_ERROR
from ..ble_api.BleCommon import BLE_ERROR
from ..ble_api.BleGatt import GATT_SERVICE, GATT_PROP, GATT_EVENT
from ..ble_api.BleGatts import GATTS_FLAG
from ..manager.BleManager import BleManager
from ..manager.BleManagerGattsMsgs import BleMgrGattsServiceAddCmd, BleMgrGattsServiceAddRsp, \
    BleMgrGattsServiceAddCharacteristicCmd, BleMgrGattsServiceAddCharacteristicRsp, \
    BleMgrGattsServiceAddDescriptorCmd, BleMgrGattsServiceAddDescriptorRsp, \
    BleMgrGattsServiceRegisterCmd, BleMgrGattsServiceRegisterRsp, BleMgrGattsReadCfmCmd, BleMgrGattsReadCfmRsp, \
    BleMgrGattsSetValueCmd, BleMgrGattsSetValueRsp, BleMgrGattsWriteCfmCmd, BleMgrGattsWriteCfmRsp, \
    BleMgrGattsSendEventCmd, BleMgrGattsSendEventRsp, BleMgrGattsGetValueCmd, BleMgrGattsGetValueRsp, \
    BleMgrGattsServiceAddIncludeCmd, BleMgrGattsServiceAddIncludeRsp, BleMgrGattsPrepareWriteCfmCmd, BleMgrGattsPrepareWriteCfmRsp

from python_gtl_thread.services.BleService import BleServiceBase


class BleGattsApi(BleApiBase):

    def __init__(self, ble_manager: BleManager, ble_adapter: BleAdapter):
        super().__init__(ble_manager, ble_adapter)

    def add_characteristic(self,
                           uuid: AttUuid = None,
                           prop: GATT_PROP = GATT_PROP.GATT_PROP_NONE,
                           perm: ATT_PERM = ATT_PERM.ATT_PERM_NONE,
                           max_len: int = 0,
                           flags: GATTS_FLAG = GATTS_FLAG.GATTS_FLAG_CHAR_READ_REQ,
                           ) -> tuple[BLE_ERROR, int, int]:

        command = BleMgrGattsServiceAddCharacteristicCmd(uuid, prop, perm, max_len, flags)
        response: BleMgrGattsServiceAddCharacteristicRsp = self._ble_manager.cmd_execute(command)
        if response.status is BLE_ERROR.BLE_STATUS_OK:
            return response.status, response.h_offset, response.h_val_offset
        else:
            return response.status, 0, 0

    def add_descriptor(self,
                       uuid: AttUuid = None,
                       perm: ATT_PERM = ATT_PERM.ATT_PERM_NONE,
                       max_len: int = 0,
                       flags: GATTS_FLAG = GATTS_FLAG.GATTS_FLAG_CHAR_READ_REQ,
                       ) -> tuple[BLE_ERROR, int]:

        command = BleMgrGattsServiceAddDescriptorCmd(uuid, perm, max_len, flags)
        response: BleMgrGattsServiceAddDescriptorRsp = self._ble_manager.cmd_execute(command)
        if response.status is BLE_ERROR.BLE_STATUS_OK:
            return response.status, response.h_offset
        else:
            return response.status, 0

    # TODO need to add to register service in Ble.py. Need to find example with included service
    def add_include(self,
                    handle: int = 0
                    ) -> BLE_ERROR:

        command = BleMgrGattsServiceAddIncludeCmd(handle)
        response: BleMgrGattsServiceAddIncludeRsp = self._ble_manager.cmd_execute(command)
        if response.status is BLE_ERROR.BLE_STATUS_OK:
            return response.status, response.h_offset
        else:
            return response.status, 0

    def add_service(self,
                    uuid: AttUuid = None,
                    type: GATT_SERVICE = GATT_SERVICE.GATT_SERVICE_PRIMARY,
                    num_attrs: int = 0
                    ) -> BLE_ERROR:

        command = BleMgrGattsServiceAddCmd(uuid, type, num_attrs)
        response: BleMgrGattsServiceAddRsp = self._ble_manager.cmd_execute(command)

        return response.status

    def get_value(self,
                  handle: int = 0,
                  max_len: int = 0
                  ) -> BLE_ERROR:

        command = BleMgrGattsGetValueCmd(handle, max_len)
        response: BleMgrGattsGetValueRsp = self._ble_manager.cmd_execute(command)

        return response.status

    def register_service(self, svc: BleServiceBase) -> BLE_ERROR:

        command = BleMgrGattsServiceRegisterCmd()
        response: BleMgrGattsServiceRegisterRsp = self._ble_manager.cmd_execute(command)
        if response.status is BLE_ERROR.BLE_STATUS_OK:
            if svc:
                svc.start_h = response.handle
                for gatt_char in svc.gatt_char_defs:
                    gatt_char.char_def.handle.value += response.handle
                    for desc in gatt_char.desc_defs:
                        desc.handle.value += response.handle

                svc.end_h = svc.start_h + svc.service_defs.num_attrs

        return response.status

    def prepare_write_cfm(self,
                          conn_idx: int = 0,
                          handle: int = 0,
                          length: int = 0,
                          status: ATT_ERROR = ATT_ERROR.ATT_ERROR_OK
                          ) -> BLE_ERROR:

        command = BleMgrGattsPrepareWriteCfmCmd(conn_idx, handle, length, status)
        response: BleMgrGattsPrepareWriteCfmRsp = self._ble_manager.cmd_execute(command)

        return response.status

    def send_event(self,
                   conn_idx: int = 0,
                   handle: int = 0,
                   type: GATT_EVENT = GATT_EVENT.GATT_EVENT_NOTIFICATION,
                   value: bytes = None
                   ) -> BLE_ERROR:

        command = BleMgrGattsSendEventCmd(conn_idx, handle, type, value)
        response: BleMgrGattsSendEventRsp = self._ble_manager.cmd_execute(command)

        return response.status

    def read_cfm(self,
                 conn_idx: int = 0,
                 handle: int = 0,
                 status: ATT_ERROR = ATT_ERROR.ATT_ERROR_OK,
                 value: bytes = None
                 ) -> BLE_ERROR:

        command = BleMgrGattsReadCfmCmd(conn_idx, handle, status, value)
        response: BleMgrGattsReadCfmRsp = self._ble_manager.cmd_execute(command)

        return response.status

    def write_cfm(self,
                  conn_idx: int = 0,
                  handle: int = 0,
                  status: ATT_ERROR = ATT_ERROR.ATT_ERROR_OK
                  ) -> BLE_ERROR:

        command = BleMgrGattsWriteCfmCmd(conn_idx, handle, status)
        response: BleMgrGattsWriteCfmRsp = self._ble_manager.cmd_execute(command)

        return response.status

    def set_value(self,
                  handle: int = 0,
                  value: bytes = None
                  ) -> BLE_ERROR:

        command = BleMgrGattsSetValueCmd(handle, value)
        response: BleMgrGattsSetValueRsp = self._ble_manager.cmd_execute(command)

        return response.status
