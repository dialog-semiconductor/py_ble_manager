import queue
from typing import Tuple
from ..adapter.BleAdapter import BleAdapter
from ..ble_api.BleAtt import ATT_PERM
from ..ble_api.BleCommon import BleEventBase, BLE_ERROR, BLE_HCI_ERROR, OwnAddress, BdAddress
from ..ble_api.BleCommonApi import BleCommonApi
from ..ble_api.BleConfig import BleConfigDefault
from ..ble_api.BleGap import BLE_GAP_ROLE, GAP_IO_CAPABILITIES, BLE_GAP_APPEARANCE
from ..ble_api.BleGapApi import BleGapApi, GapConnParams
from ..ble_api.BleGattcApi import BleGattcApi
from ..ble_api.BleGattsApi import BleGattsApi
from ..ble_api.BleStorageApi import BleStorageApi
from ..manager.BleManager import BleManager
from ..services.BleService import BleServiceBase
from ..serial_manager.SerialStreamManager import SerialStreamManager


class BleDeviceBase():
    """Base BLE device class. Implements functionality common to BLE central and BLE peripheral devices

    :param com_port: COM port of the development kit
    :type com_port: str
    :param baud_rate: Baud rate for serial port of the development kit
    :type baud_rate: int
    :param ble_config: BLE configuration to use, defaults to BleConfigDefault(BLE_DEVICE_TYPE.CENTRAL)
    :type ble_config: BleConfigDefault, optional
    :param gtl_debug: enable or disable GTL debugging, defaults to False
    :type gtl_debug: bool, optional
    """
    def __init__(self, com_port: str, baud_rate: int = 1000000, config: BleConfigDefault = BleConfigDefault(), gtl_debug: bool = False):
        """Constructor
        """
        app_command_q = queue.Queue()
        app_response_q = queue.Queue()
        app_event_q = queue.Queue()

        adapter_command_q = queue.Queue()
        adapter_event_q = queue.Queue()
        serial_tx_q = queue.Queue()
        serial_rx_q = queue.Queue()
        self._config = config
        # Internal BLE framework layers
        self._ble_manager = BleManager(app_command_q, app_response_q, app_event_q, adapter_command_q, adapter_event_q, config)
        self._ble_adapter = BleAdapter(adapter_command_q, adapter_event_q, serial_tx_q, serial_rx_q, gtl_debug)
        self._serial_stream_manager = SerialStreamManager(com_port, baud_rate, serial_tx_q, serial_rx_q)

        # Dialog API
        self._ble_gap = BleGapApi(self._ble_manager)
        self._ble_gattc = BleGattcApi(self._ble_manager)
        self._ble_gatts = BleGattsApi(self._ble_manager)
        self._ble_storage = BleStorageApi(self._ble_manager)
        self._ble_common = BleCommonApi(self._ble_manager)

        self._services: list[BleServiceBase] = []

    def _ble_reset(self) -> BLE_ERROR:
        """Reset BLE module

        :return: result code
        :rtype: BLE_ERROR
        """

        return self._ble_common.ble_reset()

    def _get_dev_version(self) -> Tuple[BleConfigDefault, BLE_ERROR]:
        """Get Device Version, used to determine whihc development kit in use

        :return: result code
        :rtype: BLE_ERROR
        """

        return self._ble_common.get_dev_version()

    def address_set(self, address: OwnAddress, renew_dur: int) -> BLE_ERROR:
        """Set the address of the device

        This API call is used to set the BD address of the device. If the address type is not
        :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_OWN_ADDR_TYPE.PRIVATE_STATIC_ADDRESS`
        the address passed is ignored (public static is set using
        :py:data:`~py_ble_manager.ble_api.BleConfig.defaultBLE_STATIC_ADDRESS`
        and private random addresses are automatically generated by the BLE stack every `renew_dur` seconds).

        ..note:
            When the address of a peripheral device is set to be non-resolvable, then the advertising type
            has to be non-connectable.

        ..note:
            This API function has to be called prior to creating the attribute database of the device. This
            is because the device configuration is going to be modified, which will result in clearing the
            current attribute database (if it exists).

        :param address: address to be set
        :type address: OwnAddress
        :param renew_dur: random address renew duration in seconds (valid range is 1 to 3600 seconds)
        :type renew_dur: int
        :return: result code
        :rtype: BLE_ERROR
        """

        return self._ble_gap.address_set(address, renew_dur)

    def appearance_set(self, appearance: BLE_GAP_APPEARANCE, perm: ATT_PERM) -> BLE_ERROR:
        """Set the appearance used for GAP service

        ..note:
            This API function has to be called prior to creating the attribute database of the device. This
            is because the device configuration is going to be modified, which will result in clearing the
            current attribute database (if it exists).

        :param appearance: appearance value
        :type appearance: BLE_GAP_APPEARANCE
        :param perm: appearance attribute write permission
        :type perm: ATT_PERM
        :return: result code
        :rtype: BLE_ERROR
        """

        return self._ble_gap.appearance_set(appearance, perm)

    def conn_param_update(self, conn_idx: int, conn_params: GapConnParams) -> BLE_ERROR:
        """Initiate a connection parameter update

        This call can be used by both the master and the slave of the connection to initiate a connection
        parameter update. For the master of the connection, the new connection parameters will be applied
        immediately. For the slave of the connection, a connection parameter update request will be send
        to the master. If the master accepts the connection parameters, it will be in charge of applying
        them (which will result in a :py:class:`~py_ble_manager.ble_api.BleGap.BleEventGapConnParamUpdated`
        event message to the slave that initiated the connection parameter update process). If 40s elapse without a response from the
        master, the connection will be terminated.

        :param conn_idx: connection index
        :type conn_idx: int
        :param conn_params: connection parameters
        :type conn_params: GapConnParams
        :return: result code
        :rtype: BLE_ERROR
        """

        return self._ble_gap.conn_param_update(conn_idx, conn_params)

    def conn_param_update_reply(self, conn_idx: int, accept: bool) -> BLE_ERROR:
        """Reply to a connection parameter update request

        This call should be used to reply to a connection parameter update request event
        (:py:class:`~py_ble_manager.ble_api.BleGap.BleEventGapConnParamUpdateReq`) message.

        :param conn_idx: connection index
        :type conn_idx: int
        :param accept: accept flag (True to accept, False to reject)
        :type accept: bool
        :return: result code
        :rtype: BLE_ERROR
        """

        return self._ble_gap.conn_param_update_reply(conn_idx, accept)

    def data_length_set(self,
                        conn_idx: int,
                        tx_length: int,
                        tx_time: int) -> BLE_ERROR:
        """Set the data length used for TX

        This function will set the maximum transmit data channel PDU payload length and time depending
        on the `conn_idx` provided. If `conn_idx` is set to
        :py:data`~py_ble_manager.ble_api.BleGap.BLE_CONN_IDX_INVALID` then this API sets
        the preferred TX data length and time for subsequent connections. If `conn_idx` corresponds to
        an existing connection, it will set the TX data length and time for the specific connection (and
        possibly will initiate a Data Length Update procedure as defined in Bluetooth Core v_4.2).

        ..note:
          The application will receive one of the following events as response to this API:
          :py:class:`~py_ble_manager.ble_api.BleGap.BleEventGapDataLengthChanged`
          if data length has been changed
          :py:class:`~py_ble_manager.ble_api.BleGap.BleEventGapDataLengthSetFailed`
          with error code if data length could not be set

        ..note:
          If data length is not changed (i.e. if it is set by application to a value larger than the
          peer's previously reported RX length) no event will be sent to application. Even though
          :py:meth:`~py_ble_manager.ble_devices.BleDeviceBase.data_length_set()` be successfully completed,
          the data length has not changed.

        :param conn_idx: connection index (if set to :py:data`~py_ble_manager.ble_api.BleGap.BLE_CONN_IDX_INVALID`
                         then the API will set the preferred data length for new connections)
        :type conn_idx: int
        :param tx_length: length for TX data channel PDU payload in octets
        :type tx_length: int
        :param tx_time: time for TX data channel PDU payload (if set to 0 it will be
                                calculated based on the tx_length (with regard to Bluetooth Core v_4.2)
        :type tx_time: int
        :return: result code
        :rtype: BLE_ERROR
        """

        return self._ble_gap.data_length_set(conn_idx, tx_length, tx_time)

    def device_name_get(self) -> Tuple[str, BLE_ERROR]:
        """Get the device name used for GAP service

        :return: device name, result code
        :rtype: Tuple[str, BLE_ERROR]
        """

        return self._ble_gap.device_name_get()

    def device_name_set(self, name: str, perm: ATT_PERM = ATT_PERM.ATT_PERM_NONE) -> BLE_ERROR:
        """Set the device name used for GAP service

        ..note:
            This API function has to be called prior to creating the attribute database of the device. This
            is because the device configuration is going to be modified, which will result in clearing the
            current attribute database (if it exists).

        :param name: device name
        :type name: str
        :param perm: device name attribute write permission, defaults to ATT_PERM.ATT_PERM_NONE
        :type perm: ATT_PERM, optional
        :return: result code
        :rtype: BLE_ERROR
        """

        return self._ble_gap.device_name_set(name, perm)

    def disconnect(self, conn_idx: int, reason: BLE_HCI_ERROR = BLE_HCI_ERROR.BLE_HCI_ERROR_REMOTE_USER_TERM_CON) -> BLE_ERROR:
        """Terminate a connection

        This call initiates a disconnection procedure on an established link.

        :param conn_idx: connection index
        :type conn_idx: int
        :param reason: reason for disconnection, defaults to BLE_HCI_ERROR.BLE_HCI_ERROR_REMOTE_USER_TERM_CON
        :type reason: BLE_HCI_ERROR, optional
        :return: result code
        :rtype: BLE_ERROR

    .. note::
        Valid reasons for initiating a disconnection are:
            * :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_HCI_ERROR.BLE_HCI_ERROR_AUTH_FAILURE`
            * :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_HCI_ERROR.BLE_HCI_ERROR_REMOTE_USER_TERM_CON`
            * :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_HCI_ERROR.BLE_HCI_ERROR_REMOTE_DEV_TERM_LOW_RESOURCES`
            * :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_HCI_ERROR.BLE_HCI_ERROR_REMOTE_DEV_POWER_OFF`
            * :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_HCI_ERROR.BLE_HCI_ERROR_UNSUPPORTED_REMOTE_FEATURE`
            * :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_HCI_ERROR.BLE_HCI_ERROR_PAIRING_WITH_UNIT_KEY_NOT_SUP`
            * :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_HCI_ERROR.BLE_HCI_ERROR_UNACCEPTABLE_CONN_INT`

        If API is called with a different reason, disconnection will fail with return status
            :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_ERROR.BLE_ERROR_INVALID_PARAM`.

    .. note:: After calling this function, the application will receive one of the following messages:
            :py:class:`~py_ble_manager.ble_api.BleGap.BleEventGapDisconnected` when the disconnection procedure was successful.
            :py:class:`~py_ble_manager.ble_api.BleGap.BleEventGapDisconnectFailed` with error status when the disconnection procedure
            failed.
        """

        return self._ble_gap.disconnect(conn_idx, reason)

    def init(self) -> None:
        self._serial_stream_manager.open_serial_port()

        # Start always running BLE tasks
        self._ble_manager.init()
        self._ble_adapter.init()
        self._serial_stream_manager.init()

    def get_event(self, timeout: int = None) -> BleEventBase:
        """Get event from BLE event queue

        :param timeout: time (in seconds) to wait for an event on the queue, defaults to None
        :type timeout: int, optional
        :return: an event from the queue. `None` if queue empty when `timeout` is exceeded
        :rtype: BleEventBase
        """

        return self._ble_manager.mgr_event_queue_get(timeout)

    def mtu_size_get(self) -> Tuple[int, BLE_ERROR]:
        """Get MTU size

        This call retrieves the Maximum Protocol Unit size that is used in exchange MTU transactions
        with peers.

        :return: result code, mtu size
        :rtype: Tuple[BLE_ERROR, int]
        """
        return self._ble_gap.mtu_size_get()

    def mtu_size_set(self, mtu_size: int) -> BLE_ERROR:
        """Set MTU size

        This call sets the Maximum Protocol Unit size that will be used in exchange MTU transactions
        with peers.

        .. note::
            This API function has to be called prior to creating the attribute database of the device. This
            is because the device configuration is going to be modified, which will result in clearing the
            current attribute database (if it exists).

        :param mtu_size: MTU size
        :type mtu_size: int
        :return: result code
        :rtype: BLE_ERROR
        """
        return self._ble_gap.mtu_size_set(mtu_size)

    def numeric_reply(self, conn_idx: int, accept: bool) -> BLE_ERROR:
        """Respond to a numeric comparison request

        Respond to a :py:class:`~py_ble_manager.ble_api.BleGap.BleEventGapNumericRequest` event.

        :param conn_idx: connection index
        :type conn_idx: int
        :param accept: accept flag
        :type accept: bool
        :return: result code
        :rtype: BLE_ERROR
        """
        return self._ble_gap.numeric_reply(conn_idx, accept)

    def peer_features_get(self, conn_idx: int) -> BLE_ERROR:
        """Get peer's features

        This call initiates a Feature Exchange procedure or retrieves the already exchanged peer's
        features on an established connection. Peer's features will be delivered to the application via
        :py:class:`~py_ble_manager.ble_api.BleGap.BleEventGapPeerFeatures` event.

        ..note:
            For a mapping between bit values and features, see [Vol 6] Part B, Section 4.6 in Bluetooth
            Core_v5.0.pdf, or look under "BLE supported features" in co_bt.h.

        :param conn_idx: connection index
        :type conn_idx: int
        :return: result code
        :rtype: BLE_ERROR
        """

        return self._ble_gap.peer_features_get(conn_idx)

    def peer_version_get(self, conn_idx: int) -> BLE_ERROR:
        """Get peer's features

        This call initiates a Feature Exchange procedure or retrieves the already exchanged peer's
        features on an established connection. Peer's features will be delivered to the application via
        :py:class:`~py_ble_manager.ble_api.BleGap.BleEventGapPeerVersion` event.

        ..note:
            For a mapping between bit values and features, see [Vol 6] Part B, Section 4.6 in Bluetooth
            Core_v5.0.pdf, or look under "BLE supported features" in co_bt.h.

        :param conn_idx: connection index
        :type conn_idx: int
        :return: result code
        :rtype: BLE_ERROR
        """

        return self._ble_gap.peer_version_get(conn_idx)

    def set_io_cap(self, io_cap: GAP_IO_CAPABILITIES) -> BLE_ERROR:
        """Set the I/O capabilities of the device

        Set the Input/Output Capabilities of the device (combined with the peer's I/O capabilities, this
        will determine which pairing algorithm will be used).

        :param io_cap: new IO capabilities
        :type io_cap: GAP_IO_CAPABILITIES
        :return: result code
        :rtype: BLE_ERROR
        """
        return self._ble_gap.set_io_cap(io_cap)

    def start(self, role: BLE_GAP_ROLE) -> BLE_ERROR:
        """Start the BLE module as a central device

        :param role: GAP role of the device
        :type role: BLE_GAP_ROLE
        :return: result code
        :rtype: BLE_ERROR
        """

        error = self._ble_reset()
        if error == BLE_ERROR.BLE_STATUS_OK:
            ble_config, error = self._get_dev_version()
            if error == BLE_ERROR.BLE_STATUS_OK:
                self._config = ble_config
                self._ble_manager.update_ble_config(ble_config)
                error = self._ble_gap.role_set(role)

        return error

    def storage_get_int(self, conn_idx: int, key: int) -> tuple[int, BLE_ERROR]:
        return self._ble_storage.get_int(conn_idx, key)

    def storage_put_int(self, conn_idx: int, key: int, value: int, persistent: bool) -> BLE_ERROR:
        return self._ble_storage.put_int(conn_idx, key, value, persistent)

    def unpair(self, addr: BdAddress) -> BLE_ERROR:
        """Unpair command

        Use this function to unpair a device. This will also remove the device bond data from BLE storage.

        :param addr: remote device address
        :type addr: BdAddress
        :return: result code
        :rtype: BLE_ERROR
        """

        return self._ble_gap.unpair(addr)
