from ctypes import c_uint8
from typing import Tuple
from ..ble_api.BleApiBase import BleApiBase
from ..ble_api.BleAtt import ATT_PERM
from ..ble_api.BleCommon import BLE_ERROR, BdAddress, BLE_HCI_ERROR, OwnAddress
from ..ble_api.BleGap import BLE_GAP_ROLE, GapConnParams, GAP_CONN_MODE, GAP_SCAN_TYPE, GAP_SCAN_MODE, \
    GAP_IO_CAPABILITIES, BLE_NON_CONN_ADV_DATA_LEN_MAX
from ..manager.BleManager import BleManager
from ..manager.BleManagerGapMsgs import BleMgrGapRoleSetCmd, BleMgrGapRoleSetRsp, BleMgrGapConnectCmd, \
    BleMgrGapConnectRsp, BleMgrGapAdvStartCmd, BleMgrGapAdvStartRsp, BleMgrGapScanStartCmd, \
    BleMgrGapScanStartRsp, BleMgrGapDisconnectCmd, BleMgrGapDisconnectRsp, BleMgrGapConnectCancelCmd, \
    BleMgrGapConnectCancelRsp, BleMgrGapConnParamUpdateCmd, BleMgrGapConnParamUpdateRsp, \
    BleMgrGapConnParamUpdateReplyCmd, BleMgrGapConnParamUpdateReplyRsp, BleMgrGapPairCmd, BleMgrGapPairRsp, \
    BleMgrGapPairReplyCmd, BleMgrGapPairReplyRsp, BleMgrGapPasskeyReplyCmd, BleMgrGapPasskeyReplyRsp, \
    BleMgrGapNumericReplyCmd, BleMgrGapNumericReplyRsp, BleMgrGapMtuSizeSetCmd, BleMgrGapMtuSizeSetRsp, \
    BleMgrGapDeviceNameSetCmd, BleMgrGapDeviceNameSetRsp, BleMgrGapAdvStopCmd, BleMgrGapAdvStopRsp, \
    BleMgrGapAdvDataSetCmd, BleMgrGapAdvDataRsp, BleMgrGapScanStopCmd, BleMgrGapScanStopRsp, \
    BleMgrGapDataLengthSetCmd, BleMgrGapDataLengthSetRsp, BleMgrGapAddressSetCmd, BleMgrGapAddressSetRsp


class BleGapApi(BleApiBase):

    def __init__(self, ble_manager: BleManager):
        super().__init__(ble_manager)

    def address_set(self, address: OwnAddress, renew_dur: int) -> BLE_ERROR:

        command = BleMgrGapAddressSetCmd(address, renew_dur)
        response: BleMgrGapAddressSetRsp = self._ble_manager.cmd_execute(command)

        return response.status

    def adv_data_set(self,
                     adv_data_len: int = 0,
                     adv_data: (c_uint8 * BLE_NON_CONN_ADV_DATA_LEN_MAX) = (c_uint8 * BLE_NON_CONN_ADV_DATA_LEN_MAX)(),
                     scan_rsp_data_len: int = 0,
                     scan_rsp_data: (c_uint8 * BLE_NON_CONN_ADV_DATA_LEN_MAX) = (c_uint8 * BLE_NON_CONN_ADV_DATA_LEN_MAX)()
                     ) -> BLE_ERROR:

        if adv_data_len > BLE_NON_CONN_ADV_DATA_LEN_MAX or scan_rsp_data_len > BLE_NON_CONN_ADV_DATA_LEN_MAX:
            return BLE_ERROR.BLE_ERROR_INVALID_PARAM

        command = BleMgrGapAdvDataSetCmd(adv_data_len, adv_data, scan_rsp_data_len, scan_rsp_data)
        response: BleMgrGapAdvDataRsp = self._ble_manager.cmd_execute(command)

        return response.status

    def adv_start(self,
                  adv_type: GAP_CONN_MODE = GAP_CONN_MODE.GAP_CONN_MODE_UNDIRECTED
                  ) -> BLE_ERROR:

        command = BleMgrGapAdvStartCmd(adv_type)
        response: BleMgrGapAdvStartRsp = self._ble_manager.cmd_execute(command)

        return response.status

    def adv_stop(self) -> BLE_ERROR:

        command = BleMgrGapAdvStopCmd()
        response: BleMgrGapAdvStopRsp = self._ble_manager.cmd_execute(command)

        return response.status

    def conn_param_update(self, conn_idx: int, conn_params: GapConnParams):

        command = BleMgrGapConnParamUpdateCmd(conn_idx, conn_params)
        response: BleMgrGapConnParamUpdateRsp = self._ble_manager.cmd_execute(command)

        return response.status

    def conn_param_update_reply(self, conn_idx: int, accept: bool):

        command = BleMgrGapConnParamUpdateReplyCmd(conn_idx, accept)
        response: BleMgrGapConnParamUpdateReplyRsp = self._ble_manager.cmd_execute(command)

        return response.status

    def connect(self, peer_addr: BdAddress, conn_params: GapConnParams) -> BLE_ERROR:

        command = BleMgrGapConnectCmd(peer_addr, conn_params)
        response: BleMgrGapConnectRsp = self._ble_manager.cmd_execute(command)

        return response.status

    def connect_cancel(self) -> BLE_ERROR:

        command = BleMgrGapConnectCancelCmd()
        response: BleMgrGapConnectCancelRsp = self._ble_manager.cmd_execute(command)

        return response.status

    def data_length_set(self,
                        conn_idx: int,
                        tx_length: int,
                        tx_time: int) -> BLE_ERROR:

        command = BleMgrGapDataLengthSetCmd(conn_idx, tx_length, tx_time)
        response: BleMgrGapDataLengthSetRsp = self._ble_manager.cmd_execute(command)

        return response.status

    def device_name_get(self) -> Tuple[bytes, BLE_ERROR]:

        dev_params = self._ble_manager.dev_params_acquire()
        name = dev_params.dev_name
        self._ble_manager.dev_params_release()
        return name, BLE_ERROR.BLE_STATUS_OK

    def device_name_set(self, name: str, perm: ATT_PERM) -> BLE_ERROR:

        command = BleMgrGapDeviceNameSetCmd(name, perm)
        response: BleMgrGapDeviceNameSetRsp = self._ble_manager.cmd_execute(command)

        return response.status

    def disconnect(self, conn_idx: int, reason: BLE_HCI_ERROR) -> BLE_ERROR:

        command = BleMgrGapDisconnectCmd(conn_idx, reason)
        response: BleMgrGapDisconnectRsp = self._ble_manager.cmd_execute(command)

        return response.status

    def mtu_size_get(self) -> Tuple[int, BLE_ERROR]:

        dev_params = self._ble_manager.dev_params_acquire()
        mtu_size = dev_params.mtu_size
        self._ble_manager.dev_params_release()
        return mtu_size, BLE_ERROR.BLE_STATUS_OK

    def mtu_size_set(self, mtu_size: int) -> BLE_ERROR:

        command = BleMgrGapMtuSizeSetCmd(mtu_size)
        response: BleMgrGapMtuSizeSetRsp = self._ble_manager.cmd_execute(command)

        return response.status

    def numeric_reply(self, conn_idx: int, accept: bool):

        command = BleMgrGapNumericReplyCmd(conn_idx, accept)
        response: BleMgrGapNumericReplyRsp = self._ble_manager.cmd_execute(command)

        return response.status

    def pair(self, conn_idx: int, bond: bool) -> BLE_ERROR:

        command = BleMgrGapPairCmd(conn_idx, bond)
        response: BleMgrGapPairRsp = self._ble_manager.cmd_execute(command)

        return response.status

    def passkey_reply(self, conn_idx: int, accept: bool, passkey: int):

        command = BleMgrGapPasskeyReplyCmd(conn_idx, accept, passkey)
        response: BleMgrGapPasskeyReplyRsp = self._ble_manager.cmd_execute(command)

        return response.status

    def pair_reply(self, conn_idx: int, accept: bool, bond: bool) -> BLE_ERROR:

        command = BleMgrGapPairReplyCmd(conn_idx, accept, bond)
        response: BleMgrGapPairReplyRsp = self._ble_manager.cmd_execute(command)

        return response.status

    def role_set(self, role: BLE_GAP_ROLE) -> BLE_ERROR:

        command = BleMgrGapRoleSetCmd(role)
        response: BleMgrGapRoleSetRsp = self._ble_manager.cmd_execute(command)

        return response.status

    def scan_start(self,
                   type: GAP_SCAN_TYPE = GAP_SCAN_TYPE.GAP_SCAN_ACTIVE,
                   mode: GAP_SCAN_MODE = GAP_SCAN_MODE.GAP_SCAN_GEN_DISC_MODE,
                   interval: int = 0,
                   window: int = 0,
                   filt_wlist: bool = False,
                   filt_dupl: bool = False
                   ) -> BLE_ERROR:

        command = BleMgrGapScanStartCmd(type, mode, interval, window, filt_wlist, filt_dupl)
        response: BleMgrGapScanStartRsp = self._ble_manager.cmd_execute(command)

        return response.status

    def scan_stop(self) -> BLE_ERROR:

        command = BleMgrGapScanStopCmd()
        response: BleMgrGapScanStopRsp = self._ble_manager.cmd_execute(command)

        return response.status

    def set_advertising_interval(self, adv_intv_min_ms, adv_intv_max_ms) -> None:
        dev_params = self._ble_manager.dev_params_acquire()
        dev_params.adv_intv_min_ms = adv_intv_min_ms
        dev_params.adv_intv_max_ms = adv_intv_max_ms
        self._ble_manager.dev_params_release()

    def set_io_cap(self, io_cap: GAP_IO_CAPABILITIES) -> BLE_ERROR:
        dev_params = self._ble_manager.dev_params_acquire()
        dev_params.io_capabilities = io_cap
        self._ble_manager.dev_params_release()
        return BLE_ERROR.BLE_STATUS_OK
