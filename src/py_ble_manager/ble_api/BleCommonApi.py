from .BleApiBase import BleApiBase
from .BleCommon import BLE_ERROR
from ..manager.BleManager import BleManager
from ..manager.BleManagerCommonMsgs import BleMgrCommonResetCmd, BleMgrCommonResetRsp, BleMgrCommonGetDevVersionCmd, BleMgrCommonGetDevVersionRsp


class BleCommonApi(BleApiBase):

    def __init__(self, ble_manager: BleManager):
        super().__init__(ble_manager)

    def ble_reset(self) -> BLE_ERROR:

        command = BleMgrCommonResetCmd()
        response: BleMgrCommonResetRsp = self._ble_manager.cmd_execute(command, 5)  # timeout after 5 seconds
        if not response:
            raise TimeoutError("Failed to reset BLE stack. Check your development kit hardware setup"
                               " and confirm the development kit is programmed with py_ble_manager firmware")
        return response.status

    def get_dev_version(self) -> BLE_ERROR:

        command = BleMgrCommonGetDevVersionCmd()
        response: BleMgrCommonGetDevVersionRsp = self._ble_manager.cmd_execute(command)

        return response.config, response.status
