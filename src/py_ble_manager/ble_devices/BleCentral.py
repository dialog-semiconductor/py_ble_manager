from ..ble_api.BleAtt import AttUuid
from ..ble_api.BleConfig import BleConfigDefault, BLE_DEVICE_TYPE
from ..ble_api.BleConvert import BleConvert
from ..ble_devices.BleDeviceBase import BleDeviceBase
from ..ble_api.BleCommon import BLE_ERROR, BdAddress, BleEventBase, BLE_EVT_GAP
from ..ble_api.BleGap import BLE_GAP_ROLE, GapConnParams, GAP_SCAN_TYPE, GAP_SCAN_MODE, \
    BleEventGapConnParamUpdateReq


class BleCentral(BleDeviceBase):
    """A BLE central device

    :param com_port: COM port of the development kit
    :type com_port: str
    :param baud_rate: Baud rate for serial port of the development kit
    :type baud_rate: int
    :param ble_config: BLE configuration to use, defaults to BleConfigDefault(BLE_DEVICE_TYPE.CENTRAL)
    :type ble_config: BleConfigDefault, optional
    """

    def __init__(self,
                 com_port: str,
                 baud_rate: int = 1000000,
                 ble_config: BleConfigDefault = BleConfigDefault(BLE_DEVICE_TYPE.CENTRAL),
                 ) -> None:
        """Constructor
        """
        super().__init__(com_port, baud_rate, ble_config)

    def browse(self, conn_idx: int, uuid: AttUuid) -> BLE_ERROR:
        """Browse services on remote GATT server

        This will automatically discover all characteristics and descriptors of a service. To discover
        services only, use :py:meth:`~py_ble_manager.ble_devices.BleCentral.BleCentral.discover_services`. instead.

        :py:class:`~py_ble_manager.ble_api.BleGattc.BleEventGattcBrowseSvc` will be sent for each service found. Once completed
        :py:class:`~py_ble_manager.ble_api.BleGattc.BleEventGattcBrowseCompleted` will be sent.

        If ``uuid`` is ``None``, all services are returned.

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
        a :py:class:`~py_ble_manager.ble_api.BleGap.BleEventGapConnected` event when the connection is established and a
        :py:class:`~py_ble_manager.ble_api.BleGap.BleEventGapConnectionCompleted` event when the connection procedure is completed either
        successfully or with error (in the second case,
        :py:class:`~py_ble_manager.ble_api.BleGap.BleEventGapConnected` will not be received).

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
        application will receive a :py:class:`~py_ble_manager.ble_api.BleGap.BleEventGapConnectionCompleted` event
        with status set to :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_ERROR.BLE_ERROR_CANCELED`
        if the connection procedure is successfully canceled.

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

        :py:class:`~py_ble_manager.ble_api.BleGattc.BleEventGattcDiscoverChar` will be sent for each characteristic found. Once completed
        :py:class:`~py_ble_manager.ble_api.BleGattc.BleEventGattcDiscoverCompleted` will be sent.

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

        :py:class:`~py_ble_manager.ble_api.BleGattc.BleEventGattcDiscoverDesc` will be sent for each descriptor found. Once completed
        :py:class:`~py_ble_manager.ble_api.BleGattc.BleEventGattcDiscoverCompleted` will be sent.

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

        :py:class:`~py_ble_manager.ble_api.BleGattc.BLE_EVT_GATTC.BleEventGattcDiscoverSvc` will be sent for each service found. Once completed
        :py:class:`~py_ble_manager.ble_api.BleGattc.BleEventGattcDiscoverCompleted` will be sent.

        If `uuid` is None, all services are returned.

        :param conn_idx: connection index
        :type conn_idx: int
        :param uuid: optional service UUID
        :type uuid: AttUuid
        :return: result code
        :rtype: BLE_ERROR
        """

        return self._ble_gattc.discover_services(conn_idx, uuid)

    def exchange_mtu(self, conn_idx: int) -> BLE_ERROR:
        """Exchange MTU

        This call will start an MTU exchange procedure with the MTU previously set using
        :py:meth:`~py_ble_manager.ble_devices.BleCentral.mtu_size_set`.
        If the MTU has been changed during the negotiation, a
        :py:class:`~py_ble_manager.ble_api.BleGattc.BleEventGattcMtuChanged` event will be sent to the application

        :param conn_idx: connection index
        :type conn_idx: int
        :return: result code
        :rtype: BLE_ERROR
        """

        return self._ble_gattc.exchange_mtu(conn_idx)

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
            * :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_ERROR.BLE_STATUS_OK` if request has been send successfully.
            * :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_ERROR.BLE_ERROR_FAILED` if request hasn't been sent successfully
            * :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_ERROR.BLE_ERROR_ALREADY_DONE` if device is already paired or bonded respectively
            * :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_ERROR.BLE_ERROR_INS_RESOURCES` if there is 
              :py:const:`~py_ble_manager.ble_api.BleConfig.defaultBLE_MAX_BONDED` number of bonded devices
        :rtype: BLE_ERROR
        """

        return self._ble_gap.pair(conn_idx, bond)

    def passkey_reply(self, conn_idx: int, accept: bool, passkey: int) -> BLE_ERROR:
        """Respond to a passkey request

        Respond to a :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_PASSKEY_REQUEST` event.

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
        value will be returned in the :py:class:`~py_ble_manager.ble_api.BleGattc.BleEventGattcReadCompleted` event.

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
                   interval_ms: int,
                   window_ms: int,
                   filt_wlist: bool,
                   filt_dupl: bool
                   ) -> BLE_ERROR:
        """Start scanning for devices

        This call initiates a scan procedure. The scan duration depends on the scan mode selected.
        In General-discoverable and Limited-discoverable modes, the scan will stop after 10s of activity.
        In Observer mode, the scan operation will continue until it is stopped using :py:meth:`~py_ble_manager.ble_devices.BleCentral.BleCentral.scan_stop`.
        Allowed values for `interval_ms` span in the range of 2.5ms to 10.24s.

        :param type: active or passive scanning
        :type type: GAP_SCAN_TYPE
        :param mode: scan for General-discoverable, Limited-discoverable or for all devices
        :type mode: GAP_SCAN_MODE
        :param interval_ms: scan interval in milliseconds
        :type interval_ms: int
        :param window_ms: scan window in milliseconds
        :type window_ms: int
        :param filt_wlist: enable or disable white list filtering, defaults to False
        :type filt_wlist: bool
        :param filt_dupl: enable or disable filtering of duplicates
        :type filt_dupl: bool
        :return: result code
        :rtype: BLE_ERROR
        """
        interval = BleConvert.scan_interval_from_ms(interval_ms)
        window = BleConvert.scan_window_from_ms(window_ms)
        return self._ble_gap.scan_start(type, mode, interval, window, filt_wlist, filt_dupl)

    def scan_stop(self) -> BLE_ERROR:
        """Stop scanning for devices

        This call stops a scan procedure previously started using :py:meth:`~py_ble_manager.ble_devices.BleCentral.BleCentral.scan_start`

        :return: result code
        :rtype: BLE_ERROR
        """
        return self._ble_gap.scan_stop()

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

        The application will receive a :py:class:`~py_ble_manager.ble_api.BleGattc.BleEventGattcWriteCompleted`
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

        The application will receive a :py:class:`~py_ble_manager.ble_api.BleGattc.BleEventGattcWriteCompleted` event
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

        The application will receive a :py:class:`~py_ble_manager.ble_api.BleGattc.BleEventGattcWriteCompleted` event when
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

        The application will receive a :py:class:`~py_ble_manager.ble_api.BleGattc.BleEventGattcWriteCompleted`
        event when write queue is executed. The `handle` parameter of this event will be set to 0.

        :param conn_idx: connection index
        :type conn_idx: int
        :param commit: true if data shall be written, false otherwise
        :type commit: bool
        :return: result code
        :rtype: BLE_ERROR
        """
        return self._ble_gattc.write_execute(conn_idx, commit)
