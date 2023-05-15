from ..ble_api.BleAtt import AttUuid
from ..ble_api.BleConfig import BleConfigDefault, BLE_DEVICE_TYPE
from ..ble_devices.BleDeviceBase import BleDeviceBase
from ..ble_api.BleCommon import BLE_ERROR, BdAddress, BleEventBase, BLE_EVT_GAP
from ..ble_api.BleGap import BLE_GAP_ROLE, GapConnParams, GAP_SCAN_TYPE, GAP_SCAN_MODE, \
    BleEventGapConnParamUpdateReq


class BleCentral(BleDeviceBase):
    """A BLE central device

    :param com_port: COM port of the development kit
    :type com_port: str
    :param ble_config: BLE configuration to use, defaults to BleConfigDefault(BLE_DEVICE_TYPE.CENTRAL)
    :type ble_config: BleConfigDefault, optional
    :param gtl_debug: enable or disable GTL debugging, defaults to False
    :type gtl_debug: bool, optional
    """
    def __init__(self,
                 com_port: str,
                 ble_config: BleConfigDefault = BleConfigDefault(BLE_DEVICE_TYPE.CENTRAL),
                 gtl_debug: bool = False
                 ) -> None:
        """Constructor
        """
        super().__init__(com_port, ble_config, gtl_debug)

    def browse(self, conn_idx: int, uuid: AttUuid) -> BLE_ERROR:
        """Browse services on remote GATT server in a given range

        This will automatically discover all characteristics and descriptors of a service. To discover
        services only, use ble_gattc_discover_svc() instead.

        :py:class:`~python_gtl_thread.ble_api.BleCommon.BLE_EVT_GATTC.BLE_EVT_GATTC_BROWSE_SVC` will be sent for each service found. Once completed
        :py:class:`~python_gtl_thread.ble_api.BleCommon.BLE_EVT_GATTC.BLE_EVT_GATTC_BROWSE_COMPLETED` will be sent.

        :param conn_idx: connection index
        :type conn_idx: int
        :param uuid: optional service UUID
        :type uuid: AttUuid
        :return: result code
        :rtype: BLE_ERROR
        """

        return self._ble_gattc.browse(conn_idx, uuid)

    def connect(self, peer_addr: BdAddress, conn_params: GapConnParams) -> BLE_ERROR:
        """Connect to a device

        This call initiates a direct connection procedure to a specified device. The application will get
        a :py:class:`~python_gtl_thread.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_CONNECTED` event when the connection is established and a
        :py:class:`~python_gtl_thread.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_CONNECTION_COMPLETED` event when the connection procedure is completed either
        successfully or with error (in the second case, :py:class:`~python_gtl_thread.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_CONNECTED` will not be received).

        :param peer_addr: BD address of the peer device
        :type peer_addr: BdAddress
        :param conn_params: connection parameters to be used
        :type conn_params: GapConnParams
        :return: result code
        :rtype: BLE_ERROR
        """

        return self._ble_gap.connect(peer_addr, conn_params)

    def connect_cancel(self) -> BLE_ERROR:
        """Cancel an initiated connection

        This call cancels a previously started connection procedure using connect(). The
        application will receive a :py:class:`~python_gtl_thread.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP.BLE_EVT_GAP_CONNECTION_COMPLETED` event with status set to
        :py:class:`~python_gtl_thread.ble_api.BleCommon.BLE_EVT_GAP.BLE_ERROR.BLE_ERROR_CANCELED` if the connection procedure is successfully canceled.

        :return: result code
        :rtype: BLE_ERROR
        """

        return self._ble_gap.connect_cancel()

    def discover_characteristics(self,
                                 conn_idx: int,
                                 start_h: int,
                                 end_h: int,
                                 uuid: AttUuid
                                 ) -> BLE_ERROR:
        """Discover characteristics on remote GATT server

        :py:class:`~python_gtl_thread.ble_api.BleCommon.BLE_EVT_GATTC.BLE_EVT_GATTC_DISCOVER_CHAR` will be sent for each characteristic found. Once completed
        :py:class:`~python_gtl_thread.ble_api.BleCommon.BLE_EVT_GATTC.BLE_EVT_GATTC_DISCOVER_COMPLETED` will be sent.

        If `uuid` is `None`, all characteristics are returned.

        :param conn_idx: connection index
        :type conn_idx: int
        :param start_h: start handle of service to discover
        :type start_h: int
        :param end_h: end handle of service to discover
        :type end_h: int
        :param uuid: optional characteristic UUID
        :type uuid: AttUuid
        :return: result code
        :rtype: BLE_ERROR
        """

        return self._ble_gattc.discover_characteristics(conn_idx, start_h, end_h, uuid)

    def discover_descriptors(self,
                             conn_idx: int,
                             start_h: int,
                             end_h: int
                             ) -> BLE_ERROR:
        """Discover descriptors on remote GATT server

        :py:class:`~python_gtl_thread.ble_api.BleCommon.BLE_EVT_GATTC.BLE_EVT_GATTC_DISCOVER_DESC` will be sent for each descriptor found. Once completed
        :py:class:`~python_gtl_thread.ble_api.BleCommon..BLE_EVT_GATTC.BLE_EVT_GATTC_DISCOVER_COMPLETED` will be sent.

        :param conn_idx: connection index
        :type conn_idx: int
        :param start_h: start handle of characteristic to discover
        :type start_h: int
        :param end_h: end handle of characteristic to discover
        :type end_h: int
        :return: result code
        :rtype: BLE_ERROR
        """

        return self._ble_gattc.discover_descriptors(conn_idx, start_h, end_h)

    def discover_services(self, conn_idx: int, uuid: AttUuid) -> BLE_ERROR:
        """Discover services on remote GATT server

        :py:class:`~python_gtl_thread.ble_api.BleCommon.BLE_EVT_GATTC.BLE_EVT_GATTC_DISCOVER_SVC` will be sent for each service found. Once completed
        :py:class:`~python_gtl_thread.ble_api.BleCommon.BLE_EVT_GATTC.BLE_EVT_GATTC_DISCOVER_COMPLETED` will be sent.

        If `uuid` is None, all services are returned.

        :param conn_idx: connection index
        :type conn_idx: int
        :param uuid: optional service UUID
        :type uuid: AttUuid
        :return: result code
        :rtype: BLE_ERROR
        """

        return self._ble_gattc.discover_services(conn_idx, uuid)

    def handle_event_default(self, evt: BleEventBase) -> None:
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

    def pair(self, conn_idx: int, bond: bool) -> BLE_ERROR:
        """Start pairing

        This call starts a pairing or bonding procedure. Depending on whether the device is master or
        slave on the connection, it will send a pairing or a security request respectively.

        :param conn_idx: connection index
        :type conn_idx: int
        :param bond: whether it starts pairing or bonding procedure
        :type bond: bool
        :return:
            :py:class:`~python_gtl_thread.ble_api.BleCommon.BLE_ERROR.BLE_STATUS_OK` if request has been send successfully.
            :py:class:`~python_gtl_thread.ble_api.BleCommon.BLE_ERROR.BLE_ERROR_FAILED` if request hasn't been send successfully
            :py:class:`~python_gtl_thread.ble_api.BleCommon.BLE_ERROR.BLE_ERROR_ALREADY_DONE` if device is already paired or bonded respectively
            :py:class:`~python_gtl_thread.ble_api.BleCommon.BLE_ERROR.BLE_ERROR_INS_RESOURCES` if there is
              :py:const:`~python_gtl_thread.ble_api.BleGap.BLE_GAP_MAX_BONDED` number of bonded devices
        :rtype: BLE_ERROR
        """

        return self._ble_gap.pair(conn_idx, bond)

    def passkey_reply(self, conn_idx: int, accept: bool, passkey: int) -> BLE_ERROR:
        """Respond to a passkey request

        Respond to a :py:class:`~python_gtl_thread.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_PASSKEY_REQUEST` event.

        :param conn_idx: connection index
        :type conn_idx: int
        :param accept: accept flag
        :type accept: bool
        :param passkey: passkey entered by user
        :type passkey: int
        :return: result code
        :rtype: BLE_ERROR
        """

        return self._ble_gap.passkey_reply(conn_idx, accept, passkey)

    def read(self, conn_idx: int, handle: int, offset: int) -> BLE_ERROR:
        """Read attribute from remote GATT server

        This uses either the "Read Characteristic Value" procedure or the "Read Characteristic Descriptor"
        procedure, depending on the attribute `handle`. If `offset` is non-zero or the
        attribute length is larger than the MTU, the "Read Long Characteristic Value" procedure or the
        "Read Long Characteristic Descriptor" procedure will be used respectively. The complete attribute
        value will be returned in the :py:class:`~python_gtl_thread.ble_api.BleCommon.BLE_EVT_GATTC.BLE_EVT_GATTC_READ_COMPLETED` event.

        :param conn_idx: connection index
        :type conn_idx: int
        :param handle: attribute handle
        :type handle: int
        :param offset: value offset to start with
        :type offset: int
        :return: result code
        :rtype: BLE_ERROR
        """
        return self._ble_gattc.read(conn_idx, handle, offset)

    def scan_start(self,
                   type: GAP_SCAN_TYPE,
                   mode: GAP_SCAN_MODE,
                   interval: int,
                   window: int,
                   filt_wlist: bool,
                   filt_dupl: bool
                   ) -> BLE_ERROR:
        """Start scanning for devices

        This call initiates a scan procedure. The scan duration depends on the scan mode selected.
        In General-discoverable and Limited-discoverable modes, the scan will stop after 10s of activity.
        In Observer mode, the scan operation will continue until it is stopped using ble_gap_scan_stop().
        The scan `interval` and `window` can be set in steps of 0.625ms. Allowed values for `interval`
        span in the range of 0x4 (2.5ms) to 0x4000 (10.24s).

        :param type: active or passive scanning
        :type type: GAP_SCAN_TYPE
        :param mode: scan for General-discoverable, Limited-discoverable or for all devices
        :type mode: GAP_SCAN_MODE
        :param interval: scan interval in steps of 0.625ms
        :type interval: int
        :param window: _description_
        :type window: int
        :param filt_wlist: enable or disable white list filtering, defaults to False
        :type filt_wlist: bool
        :param filt_dupl: nable or disable filtering of duplicates
        :type filt_dupl: bool
        :return: result code
        :rtype: BLE_ERROR
        """

        return self._ble_gap.scan_start(type, mode, interval, window, filt_wlist, filt_dupl)

    def start(self) -> BLE_ERROR:
        """Start the BLE module as a central device

        :return: result code
        :rtype: BLE_ERROR
        """
        return super().start(BLE_GAP_ROLE.GAP_CENTRAL_ROLE)

    def write(self, conn_idx: int, handle: int, offset: int, value: bytes) -> BLE_ERROR:
        """Write attribute to remote GATT server

        This uses either the "Write Characteristic Value" procedure or the "Write Characteristic
        Descriptor" procedure, depending on the attribute `handle`. If `offset` is non-zero
        or the attribute length is larger than the MTU, the "Write Long Characteristic Value" procedure
        or the "Write Long Characteristic Descriptor" procedure will be used respectively.

        The application will receive a :py:class:`~python_gtl_thread.ble_api.BleCommon.BLE_EVT_GATTC.BLE_EVT_GATTC_WRITE_COMPLETED`
        event when the write operation is completed.

        :param conn_idx: connection index
        :type conn_idx: int
        :param handle: attribute handle
        :type handle: int
        :param offset: value offset to start with
        :type offset: int
        :param value: value data
        :type value: bytes
        :return: result code
        :rtype: BLE_ERROR
        """

        return self._ble_gattc.write(conn_idx, handle, offset, value)

    def write_no_resp(self, conn_idx: int, handle: int, signed_write: bool, value: bytes) -> BLE_ERROR:
        """Write attribute to remote GATT server (without response)

        If `signed_write` is set to `False`, the "Write Without Response" procedure will be used.
        If `signed_write` is set to `True`, the "Signed Write Without Response" procedure will be used on
        a link which is not encrypted or will fall back to the "Write Without Response" procedure on a
        link that is already encrypted.

        The application will receive a :py:class:`~python_gtl_thread.ble_api.BleCommon.BLE_EVT_GATTC.BLE_EVT_GATTC_WRITE_COMPLETED` event
        when the write operation is performed.

        :param conn_idx: connection index
        :type conn_idx: int
        :param handle: attribute handle
        :type handle: int
        :param signed_write: true if signed write should be used if possible/applicable
        :type signed_write: bool
        :param value: value data
        :type value: bytes
        :return: result code
        :rtype: BLE_ERROR
        """
        return self._ble_gattc.write_no_resp(conn_idx, handle, signed_write, value)

    def write_prepare(self, conn_idx: int, handle: int, offset: int, value: bytes) -> BLE_ERROR:
        """Prepare long/reliable write to remote GATT server

        The application will receive a :py:class:`~python_gtl_thread.ble_api.BleCommon.BLE_EVT_GATTC.BLE_EVT_GATTC_WRITE_COMPLETED` event when
        the write operation is queued.

        :param conn_idx: connection index
        :type conn_idx: int
        :param handle: attribute handle
        :type handle: int
        :param offset: value offset
        :type offset: int
        :param value: value data
        :type value: bytes
        :return: result code
        :rtype: BLE_ERROR
        """
        return self._ble_gattc.write_prepare(conn_idx, handle, offset, value)

    def write_execute(self, conn_idx: int, commit: bool) -> BLE_ERROR:
        """Execute reliable/long write to remote GATT server

        In order to cancel prepared requests, `commit` shall be set to `False`.

        The application will receive a :py:class:`~python_gtl_thread.ble_api.BleCommon.BLE_EVT_GATTC.BLE_EVT_GATTC_WRITE_COMPLETED`
        event when write queue is executed. The `handle` parameter of this event will be set to 0.

        :param conn_idx: connection index
        :type conn_idx: int
        :param commit: true if data shall be written, false otherwise
        :type commit: bool
        :return: result code
        :rtype: BLE_ERROR
        """
        return self._ble_gattc.write_execute(conn_idx, commit)
