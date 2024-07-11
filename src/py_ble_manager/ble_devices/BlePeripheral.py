from ctypes import c_uint8
from typing import Tuple
from ..ble_api.BleAtt import ATT_ERROR
from ..ble_api.BleCommon import BleEventBase, BLE_ERROR, BLE_EVT_GAP, BLE_EVT_GATTS
from ..ble_api.BleConfig import BleConfigDefault, BLE_DEVICE_TYPE
from ..ble_api.BleGap import GAP_ROLE, GAP_CONN_MODE, BleEventGapConnected, \
    BleEventGapDisconnected, BleEventGapConnParamUpdateReq, BleEventGapPairReq, \
    BleAdvData, BLE_NON_CONN_ADV_DATA_LEN_MAX, GapConnParams, GAP_DISC_MODE
from ..ble_api.BleGatt import GATT_EVENT
from ..ble_api.BleGatts import BleEventGattsReadReq, BleEventGattsWriteReq, \
    BleEventGattsPrepareWriteReq, BleEventGattsEventSent
from ..ble_api.BleUtil import BleUtils
from ..ble_devices.BleDeviceBase import BleDeviceBase
from ..services.BleService import BleServiceBase


class BlePeripheral(BleDeviceBase):

    def __init__(self,
                 com_port: str,
                 baud_rate: int = 1000000,
                 ble_config: BleConfigDefault = BleConfigDefault(BLE_DEVICE_TYPE.PERIPHERAL)
                 ) -> None:
        super().__init__(com_port, baud_rate, ble_config)

    def _find_service_by_handle(self, handle: int) -> BleServiceBase:
        for service in self._services:
            if service and handle >= service.start_h and handle <= service.end_h:
                return service
        return None

    def _handle_connected_evt(self, evt: BleEventGapConnected) -> None:
        for service in self._services:
            if service and service.connected_evt:
                service.connected_evt(evt)

    def _handle_disconnected_evt(self, evt: BleEventGapDisconnected) -> None:
        for service in self._services:
            if service and service.disconnected_evt:
                service.disconnected_evt(evt)

    def _handle_event_sent_evt(self, evt: BleEventGattsEventSent) -> bool:
        service = self._find_service_by_handle(evt.handle)
        if service:
            if service.event_sent:
                service.event_sent(evt)
            return True
        return False

    def _handle_prepare_write_req_evt(self, evt: BleEventGattsPrepareWriteReq) -> bool:
        service = self._find_service_by_handle(evt.handle)
        if service:
            if service.prepare_write_req:
                service.prepare_write_req(evt)
            return True
        return False

    def _handle_read_req_evt(self, evt: BleEventGattsReadReq) -> bool:
        service = self._find_service_by_handle(evt.handle)
        if service:
            if service.read_req:
                service.read_req(evt)
            return True
        return False

    def _handle_write_req_evt(self, evt: BleEventGattsWriteReq) -> bool:
        service = self._find_service_by_handle(evt.handle)
        if service:
            if service.write_req:
                service.write_req(evt)
            return True
        return False

    def advertising_channel_map_get(self) -> Tuple[int, BLE_ERROR]:
        """Get the advertising channel map currently set

        .. note::
            Resposne will be constructed using the members of :py:class:`~py_ble_manager.ble_api.BleGap.GAP_ADV_CHANNEL`:
            :py:class:`~py_ble_manager.ble_api.BleGap.GAP_ADV_CHANNEL.GAP_ADV_CHANNEL_37`,
            :py:class:`~py_ble_manager.ble_api.BleGap.GAP_ADV_CHANNEL.GAP_ADV_CHANNEL_38`,
            :py:class:`~py_ble_manager.ble_api.BleGap.GAP_ADV_CHANNEL.GAP_ADV_CHANNEL_39`.

        :return: channel map currently used for advertising, result code
        :rtype: Tuple[int, BLE_ERROR]
        """

        return self._ble_gap.adv_chnl_map_get()

    def advertising_channel_map_set(self, chnl_map: int) -> BLE_ERROR:
        """Set the advertising channel map

        .. note::
            This function has to be called prior to an advertising start and
            it will not modify the channel map of an ongoing advertising operation.

        .. note:
            ``chnl_map`` must be constructed using the members of :py:class:`~py_ble_manager.ble_api.BleGap.GAP_ADV_CHANNEL`:
            :py:class:`~py_ble_manager.ble_api.BleGap.GAP_ADV_CHANNEL.GAP_ADV_CHANNEL_37`,
            :py:class:`~py_ble_manager.ble_api.BleGap.GAP_ADV_CHANNEL.GAP_ADV_CHANNEL_38`,
            :py:class:`~py_ble_manager.ble_api.BleGap.GAP_ADV_CHANNEL.GAP_ADV_CHANNEL_39`.

        :param chnl_map: channel map used for advertising
        :type chnl_map: int
        :return: result code
        :rtype: BLE_ERROR
        """

        return self._ble_gap.adv_chnl_map_set(chnl_map)

    def advertising_data_get(self) -> Tuple[list[BleAdvData], list[BleAdvData], BLE_ERROR]:
        """Get currently used Advertising Data and Scan Response Data

        Get the Advertising Data and Scan Response Data currently used. This can be used while an
        advertising operation is in progress.

        :return: list of AD Structures used for advertising, list AD Structures used for scan response, result code
        :rtype: Tuple[list[BleAdvData], list[BleAdvData], BLE_ERROR]
        """

        adv_data, scan_rsp_data, error = self._ble_gap.adv_data_get()
        adv_data_structs: list[BleAdvData] = BleUtils.parse_adv_data_from_bytes(adv_data)
        scan_rsp_data_structs: list[BleAdvData] = BleUtils.parse_adv_data_from_bytes(scan_rsp_data)
        return adv_data_structs, scan_rsp_data_structs, error

    def advertising_data_set(self,
                             adv_data_ad_list: list[BleAdvData] = [],
                             scan_rsp_ad_list: list[BleAdvData] = []
                             ) -> BLE_ERROR:
        """Set advertising Data and scan response data

        This API call is used to modify the advertising data and scan response data used. It can be used
        while an advertising operation is in progress. If an advertising operation is not in progress,
        the new Advertising Data and/or new Scan Response Data will be used the next time function
        :py:meth:`~py_ble_manager.ble_devices.BlePeripheral.advertising_start`. is called.
        The maximum Advertising Data length for undirected connectable
        advertising is :py:const:`~py_ble_manager.ble_api.BleGap.BLE_ADV_DATA_LEN_MAX` bytes (31 minus 3 that are reserved to set the Advertising Data
        type flags - which shall not be set in Advertising Data using this function). The equivalent max
        length for non-connectable advertising is :py:const:`~py_ble_manager.ble_api.BleGap.BLE_NON_CONN_ADV_DATA_LEN_MAX` bytes.

        :param adv_data_ad_list: list of AD Structures used for advertising, defaults to []
        :type adv_data_ad_list: list[BleAdvData], optional
        :param scan_rsp_ad_list: list of AD Structures used for scan response, defaults to []
        :type scan_rsp_ad_list: list[BleAdvData], optional
        :return: result code
        :rtype: BLE_ERROR
        """
        adv_data_len = 0
        adv_data = (c_uint8 * BLE_NON_CONN_ADV_DATA_LEN_MAX)()
        for ad in adv_data_ad_list:
            adv_data[adv_data_len] = c_uint8(ad.len)
            adv_data[adv_data_len + 1] = c_uint8(ad.type)
            adv_data[adv_data_len + 2:adv_data_len + len(ad.data) + 2] = ad.data
            adv_data_len += ad.len + 1  # +1 to account for AD len byte

        scan_rsp_data_len = 0
        scan_rsp_data = (c_uint8 * BLE_NON_CONN_ADV_DATA_LEN_MAX)()
        for ad in scan_rsp_ad_list:
            scan_rsp_data[scan_rsp_data_len] = c_uint8(ad.len)
            scan_rsp_data[scan_rsp_data_len + 1] = c_uint8(ad.type)
            scan_rsp_data[scan_rsp_data_len + 2:len(ad.data) + 2] = ad.data
            scan_rsp_data_len += ad.len + 1  # +1 to account for AD len byte

        return self._ble_gap.adv_data_set(adv_data_len, adv_data, scan_rsp_data_len, scan_rsp_data)

    def advertising_interval_get(self) -> Tuple[int, int, BLE_ERROR]:
        """Get the currently set advertising interval

        Get the minimum and maximum advertising intervals currently set.

        :return: minimum interval (ms), maximum interval (ms), result code
        :rtype: Tuple[int, int, BLE_ERROR]
        """

        return self._ble_gap.adv_intv_get()

    def advertising_interval_set(self, adv_intv_min_ms: int, adv_intv_max_ms: int) -> None:
        """Set the advertising interval

        Set the minimum and maximum interval to be used for advertising.
        Allowed values for intervals span from 20ms to 10.24s, while for
        non-connectable advertising the range is 100ms to 10.24s.

        .. note::
            This function has to be called prior to an advertising start and
            it will not modify the advertising interval of an ongoing advertising operation.

        :param adv_intv_min_ms: minimum interval (ms)
        :type adv_intv_min_ms: int
        :param adv_intv_max_ms: maximum interval (ms)
        :type adv_intv_max_ms: int
        """
        self._ble_gap.adv_intv_set(adv_intv_min_ms, adv_intv_max_ms)

    def advertising_mode_get(self) -> Tuple[GAP_DISC_MODE, BLE_ERROR]:
        """Get the discoverability mode used for advertising

        :return: discoverability mode, result code
        :rtype: Tuple[GAP_DISC_MODE, BLE_ERROR]
        """
        return self._ble_gap.adv_mode_get()

    def advertising_mode_set(self, mode: GAP_DISC_MODE) -> BLE_ERROR:
        """Set the discoverability mode used for advertising

        .. note::
            This function has to be called prior to an advertising start and
            it will not modify the discoverability mode of an ongoing advertising operation.

        :param mode: discoverability mode used for advertising
        :type mode: GAP_DISC_MODE
        :return: result code
        :rtype: BLE_ERROR
        """
        return self._ble_gap.adv_mode_set(mode)

    def advertising_start(self,
                          adv_type: GAP_CONN_MODE = GAP_CONN_MODE.GAP_CONN_MODE_UNDIRECTED
                          ) -> BLE_ERROR:
        """Start advertising

        This API call is used to start an advertising air operation. If ``adv_type`` is set to be
        :py:class:`~py_ble_manager.ble_api.BleGap.GAP_CONN_MODE.GAP_CONN_MODE_NON_CONN` or
        :py:class:`~py_ble_manager.ble_api.BleGap.GAP_CONN_MODE.GAP_CONN_MODE_UNDIRECTED`,
        the air operation will go on until it is
        stopped using :py:meth:`~py_ble_manager.ble_devices.BlePeripheral.advertising_stop`.
        If ``adv_type`` is set to be :py:class:`~py_ble_manager.ble_api.BleGap.GAP_CONN_MODE.GAP_CONN_MODE_DIRECTED` or
        :py:class:`~py_ble_manager.ble_api.BleGap.GAP_CONN_MODE.GAP_CONN_MODE_DIRECTED_LDC`
        (low duty cycle advertising), the air operation will automatically
        stop after 1.28s. In both cases, upon advertising completion, a :py:class:`~py_ble_manager.ble_api.BleGap.BleEventGapAdvCompleted` event
        will be sent to the application.

        :param adv_type: type of advertising, defaults to GAP_CONN_MODE.GAP_CONN_MODE_UNDIRECTED
        :type adv_type: GAP_CONN_MODE, optional
        :return: result code
        :rtype: BLE_ERROR
        """

        return self._ble_gap.adv_start(adv_type)

    def advertising_stop(self) -> BLE_ERROR:
        """Stop advertising

        This API call is used to stop a previously started advertising air operation. If advertising is
        successfully stopped, the application will receive a :py:class:`~py_ble_manager.ble_api.BleGap.BleEventGapAdvCompleted`
        with status set to :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_ERROR.BLE_ERROR_CANCELED`

        :return: result code
        :rtype: BLE_ERROR
        """

        return self._ble_gap.adv_stop()

    def get_value(self, handle: int, max_len: int) -> Tuple[bytes, BLE_ERROR]:
        """Get attribute value

        This retrieves an attribute's value from the database. Up to ``max_len`` size bytes are returned
        buffer.

        :param handle: handle attribute handle
        :type handle: int
        :param max_len: attribute value length
        :type max_len: int
        :return: buffer to store attribute value, result code
        :rtype: Tuple[bytes,BLE_ERROR]
        """
        service = self._find_service_by_handle(handle)
        if service:
            value, error = self._ble_gatts.get_value(handle, max_len)
            return value, error
        return bytes(), BLE_ERROR.BLE_ERROR_FAILED

    def handle_event_default(self, evt: BleEventBase):
        """Execute default event handler

        It's recommended for application to call this for any event it does not handle. This avoids
        situation when BLE stack is waiting for response on event which application does not handle.

        :param evt: event to handle
        :type evt: BleEventBase
        """

        match evt.evt_code:
            case BLE_EVT_GAP.BLE_EVT_GAP_CONN_PARAM_UPDATE_REQ:
                evt: BleEventGapConnParamUpdateReq = evt
                self.conn_param_update_reply(evt.conn_idx, True)
            case BLE_EVT_GAP.BLE_EVT_GAP_PAIR_REQ:
                evt: BleEventGapPairReq = evt
                self.pair_reply(evt.conn_idx, False, False)
            case BLE_EVT_GATTS.BLE_EVT_GATTS_READ_REQ:
                evt: BleEventGattsReadReq = evt
                self.read_cfm(evt.conn_idx, evt.handle, ATT_ERROR.ATT_ERROR_READ_NOT_PERMITTED, None)
            case BLE_EVT_GATTS.BLE_EVT_GATTS_WRITE_REQ:
                evt: BleEventGattsWriteReq = evt
                self.write_cfm(evt.conn_idx, evt.handle, ATT_ERROR.ATT_ERROR_WRITE_NOT_PERMITTED)
            case BLE_EVT_GATTS.BLE_EVT_GATTS_PREPARE_WRITE_REQ:
                evt: BleEventGattsPrepareWriteReq = evt
                self.prepare_write_cfm(evt.conn_idx, evt.handle, 0, ATT_ERROR.ATT_ERROR_WRITE_NOT_PERMITTED)

    def pair_reply(self, conn_idx: int, accept: bool, bond: bool) -> BLE_ERROR:
        """Respond to a pairing request

        The application should use this function to respond to a :py:class:`~py_ble_manager.ble_api.BleGap.BleEventGapPairReq` event.

        :param conn_idx: connection index
        :type conn_idx: int
        :param accept: accept flag
        :type accept: bool
        :param bond: bonding flag
        :type bond: bool
        :return: result code,
        :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_ERROR.BLE_STATUS_OK` if reply has been send successfully
        :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_ERROR.BLE_ERROR_FAILED` if reply hasn't been send successfully
        :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_ERROR.BLE_ERROR_INS_RESOURCES` if there is BLE_GAP_MAX_BONDED number of bonded devices
        :rtype: BLE_ERROR
        """

        return self._ble_gap.pair_reply(conn_idx, accept, bond)

    def per_pref_conn_params_get(self) -> Tuple[GapConnParams, BLE_ERROR]:
        """Get the peripheral preferred connection parameters currently set for GAP service

        :return: preferred connection params, result code
        :rtype: Tuple[GapConnParams, BLE_ERROR]
        """
        return self._ble_gap.per_pref_conn_params_get()

    def per_pref_conn_params_set(self, conn_params: GapConnParams) -> BLE_ERROR:
        """Set the peripheral preferred connection parameters used for GAP service

        .. note::
            This API function has to be called prior to creating the attribute database of the device. This
            is because the device configuration is going to be modified, which will result in clearing the
            current attribute database (if it exists).

        :param conn_params: preferred connection parameters
        :type conn_params: GapConnParams
        :return: result code
        :rtype: BLE_ERROR
        """
        return self._ble_gap.per_pref_conn_params_set(conn_params)

    def prepare_write_cfm(self,
                          conn_idx: int,
                          handle: int,
                          length: int,
                          status: ATT_ERROR
                          ) -> BLE_ERROR:
        """Respond to an attribute prepare write request

        The application should use this function to respond to a :py:class:`~py_ble_manager.ble_api.BleGatts.BleEventGattsPrepareWriteReq` event.

        :param conn_idx: connection index
        :type conn_idx: int
        :param handle: attribute handle
        :type handle: int
        :param length: attribute value length
        :type length: int
        :param status: operation status
        :type status: ATT_ERROR
        :return: result code
        :rtype: BLE_ERROR
        """

        return self._ble_gatts.prepare_write_cfm(conn_idx, handle, length, status)

    def read_cfm(self,
                 conn_idx: int,
                 handle: int,
                 status: ATT_ERROR,
                 data: bytes
                 ) -> BLE_ERROR:
        """Respond to an attribute read request

        The application should use this function to respond to a :py:class:`~py_ble_manager.ble_api.BleGatts.BleEventGattsReadReq` event.

        :param conn_idx: connection index
        :type conn_idx: int
        :param handle: attribute handle
        :type handle: int
        :param status: operation status
        :type status: ATT_ERROR
        :param data: attribute value
        :type data: bytes
        :return: result code
        :rtype: BLE_ERROR
        """

        return self._ble_gatts.read_cfm(conn_idx, handle, status, data)

    def register_service(self, svc: BleServiceBase) -> BLE_ERROR:
        """Register service in database

        Adds all attributes previously added to the ``svc```` to the attribute database.

        :param svc: service to register
        :type svc: BleServiceBase
        :return: result code
        :rtype: BLE_ERROR
        """

        error = self._ble_gatts.add_service(svc.service_defs.uuid,
                                            svc.service_defs.type,
                                            svc.service_defs.num_attrs)

        if error == BLE_ERROR.BLE_STATUS_OK:
            for i in range(0, len(svc.incl_svc_defs)):
                error, _ = self._ble_gatts.add_include(svc.incl_svc_defs[i].start_h)
                if error != BLE_ERROR.BLE_STATUS_OK:
                    break

            for i in range(0, len(svc.gatt_char_defs)):
                gatt_char_def = svc.gatt_char_defs[i]
                char_def = gatt_char_def.char_def
                # ignoring ( _ ) char declaration handle offset (h_offset)
                _, char_def.handle.value, error = self._ble_gatts.add_characteristic(char_def.uuid,
                                                                                     char_def.prop,
                                                                                     char_def.perm,
                                                                                     char_def.max_len,
                                                                                     char_def.flags)
                if error == BLE_ERROR.BLE_STATUS_OK:
                    for j in range(0, len(gatt_char_def.desc_defs)):
                        desc = gatt_char_def.desc_defs[j]
                        desc.handle.value, error = self._ble_gatts.add_descriptor(desc.uuid,
                                                                                  desc.perm,
                                                                                  desc.max_len,
                                                                                  desc.flags)
                        if error != BLE_ERROR.BLE_STATUS_OK:
                            break
                    # Break out of both loops
                    if error != BLE_ERROR.BLE_STATUS_OK:
                        break
                else:
                    break

            if error == BLE_ERROR.BLE_STATUS_OK:

                error = self._ble_gatts.register_service(svc)
                if error == BLE_ERROR.BLE_STATUS_OK:
                    self._services.append(svc)
                    # Set this BlePeripheral with the service so service can make calls to set, notify, read_cfm, etc
                    svc.register_peripheral(self)

        return error

    def send_event(self,
                   conn_idx: int,
                   handle: int,
                   type: GATT_EVENT,
                   value: bytes) -> BLE_ERROR:
        """Send a characteristic value notification or indication

        Send an indication or a notification of an attribute's value to a connected peer.

        The application will receive a :py:class:`~py_ble_manager.ble_api.BleGatts.BleEventGattsEventSent` event when the notification is
        successfully sent over the air.

        .. note::
            The characteristic must have either the :py:class:`~py_ble_manager.ble_api.BleGatt.GATT_PROP.GATT_PROP_NOTIFY` or the
            :py:class:`~py_ble_manager.ble_api.BleGatt.GATT_PROP.GATT_PROP_INDICATE` property.

        .. note::
            If a disconnection happens after calling this function or the notification cannot be
            successfully sent over the air due to e.g. a bad connection, the :py:class:`~py_ble_manager.ble_api.BleGatts.BleEventGattsEventSent`
            event may not be received.

        :param conn_idx: connection index
        :type conn_idx: int
        :param handle: characteristic value handle
        :type handle: int
        :param type: indication or notification
        :type type: GATT_EVENT
        :param value: characteristic value
        :type value: bytes
        :return: result code
        :rtype: BLE_ERROR
        """

        error = BLE_ERROR.BLE_ERROR_FAILED
        service = self._find_service_by_handle(handle)
        if service:
            error = self._ble_gatts.send_event(conn_idx, handle, type, value)
        return error

    def service_handle_event(self, evt: BleEventBase) -> bool:
        """Handle BLE event

        This function handles BLE events and passes them to services.

        :param evt: BLE event
        :type evt: BleEventBase
        :return: True if event was handled, False otherwise
        :rtype: bool
        """
        handled = False

        match evt.evt_code:
            case BLE_EVT_GAP.BLE_EVT_GAP_CONNECTED:
                self._handle_connected_evt(evt)
                # Connected event always marked as unhandled so app can handle
            case BLE_EVT_GAP.BLE_EVT_GAP_DISCONNECTED:
                self._handle_disconnected_evt(evt)
                # Disconnected event always marked as unhandled so app can handle
            case BLE_EVT_GATTS.BLE_EVT_GATTS_READ_REQ:
                handled = self._handle_read_req_evt(evt)
            case BLE_EVT_GATTS.BLE_EVT_GATTS_WRITE_REQ:
                handled = self._handle_write_req_evt(evt)
            case BLE_EVT_GATTS.BLE_EVT_GATTS_PREPARE_WRITE_REQ:
                handled = self._handle_prepare_write_req_evt(evt)
            case BLE_EVT_GATTS.BLE_EVT_GATTS_EVENT_SENT:
                handled = self._handle_event_sent_evt(evt)

        return handled

    def set_value(self, handle: int, value: bytes) -> BLE_ERROR:
        """Set attribute value

        This sets an attribute's value in the internal database. Any read request from any peer will have
        this value returned. In order for an attribute to have different values for each peer, the
        application should store them locally and use :py:class:`~py_ble_manager.ble_api.BleGatts.BleEventGattsReadReq` to handle read requests
        for a given attribute.

        :param handle: attribute handle
        :type handle: int
        :param value: attribute value
        :type value: bytes
        :return: result code
        :rtype: BLE_ERROR
        """
        error = BLE_ERROR.BLE_ERROR_FAILED
        service = self._find_service_by_handle(handle)
        if service:
            error = self._ble_gatts.set_value(handle, value)
        return error

    def start(self) -> BLE_ERROR:
        """Start the BLE module as a peripheral device

        :return: result code
        :rtype: BLE_ERROR
        """
        return super().start(GAP_ROLE.GAP_PERIPHERAL_ROLE)

    def write_cfm(self,
                  conn_idx: int,
                  handle: int,
                  status: ATT_ERROR
                  ) -> BLE_ERROR:
        """Respond to an attribute write request

        The application should use this function to respond to a :py:class:`~py_ble_manager.ble_api.BleGatts.BleEventGattsWriteReq` event.

        .. note::
            The application shall also use this to confirm write requests for characteristics with
            the "Write Without Response" property set.


        :param conn_idx: connection index
        :type conn_idx: int
        :param handle: attribute handle
        :type handle: int
        :param status: operation status
        :type status: ATT_ERROR
        :return: result code
        :rtype: BLE_ERROR
        """
        return self._ble_gatts.write_cfm(conn_idx, handle, status)
