import queue
from ..adapter.BleAdapter import BleAdapter
from ..ble_api.BleCommon import BleEventBase, BLE_ERROR, BLE_HCI_ERROR
from ..ble_api.BleConfig import BleConfigDefault
from ..ble_api.BleGap import BLE_GAP_ROLE, GAP_IO_CAPABILITIES
from ..ble_api.BleGapApi import BleGapApi, GapConnParams
from ..ble_api.BleGattcApi import BleGattcApi
from ..ble_api.BleGattsApi import BleGattsApi
from ..ble_api.BleStorageApi import BleStorageApi
from ..manager.BleManager import BleManager
from ..manager.BleManagerCommonMsgs import BleMgrCommonResetCmd, BleMgrCommonResetRsp
from ..services.BleService import BleServiceBase
from ..serial_manager.SerialStreamManager import SerialStreamManager


class BleDeviceBase():
    """Base BLE device class. Implements functionality common to BLE central and BLE peripheral devices

    :param com_port: COM port of the development kit
    :type com_port: str
    :param ble_config: BLE configuration to use, defaults to BleConfigDefault(BLE_DEVICE_TYPE.CENTRAL)
    :type ble_config: BleConfigDefault, optional
    :param gtl_debug: enable or disable GTL debugging, defaults to False
    :type gtl_debug: bool, optional
    """
    def __init__(self, com_port: str, config: BleConfigDefault = BleConfigDefault(), gtl_debug: bool = False):
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
        self._serial_stream_manager = SerialStreamManager(com_port, serial_tx_q, serial_rx_q)

        # Dialog API
        self._ble_gap = BleGapApi(self._ble_manager)
        self._ble_gattc = BleGattcApi(self._ble_manager)
        self._ble_gatts = BleGattsApi(self._ble_manager)
        self._ble_storage = BleStorageApi(self._ble_manager)

        self._services: list[BleServiceBase] = []

    def _ble_reset(self) -> BLE_ERROR:
        """Reset BLE module

        :return: result code
        :rtype: BLE_ERROR
        """

        command = BleMgrCommonResetCmd()
        response: BleMgrCommonResetRsp = self._ble_manager.cmd_execute(command)
        return response.status

    def conn_param_update(self, conn_idx: int, conn_params: GapConnParams) -> BLE_ERROR:
        """Initiate a connection parameter update

        This call can be used by both the master and the slave of the connection to initiate a connection
        parameter update. For the master of the connection, the new connection parameters will be applied
        immediately. For the slave of the connection, a connection parameter update request will be send
        to the master. If the master accepts the connection parameters, it will be in charge of applying
        them (which will result in a :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_CONN_PARAM_UPDATED`
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
        (:py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_CONN_PARAM_UPDATE_REQ`) message.

        :param conn_idx: connection index
        :type conn_idx: int
        :param accept: accept flag (True to accept, False to reject)
        :type accept: bool
        :return: result code
        :rtype: BLE_ERROR
        """

        return self._ble_gap.conn_param_update_reply(conn_idx, accept)

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
            :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_DISCONNECTED` when the disconnection procedure was successful.
            :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_DISCONNECT_FAILED` with error status when the disconnection procedure
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

    def numeric_reply(self, conn_idx: int, accept: bool) -> BLE_ERROR:
        """Respond to a numeric comparison request

        Respond to a :py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GAP.BLE_EVT_GAP_NUMERIC_REQUEST` event.

        :param conn_idx: connection index
        :type conn_idx: int
        :param accept: accept flag
        :type accept: bool
        :return: result code
        :rtype: BLE_ERROR
        """
        return self._ble_gap.numeric_reply(conn_idx, accept)

    def set_io_cap(self, io_cap: GAP_IO_CAPABILITIES) -> BLE_ERROR:
        """Set the I/O capabilities of the device

        Set the Input/Output Capabilities of the device (combined with the peer's I/O capabilities, this
        will determine which pairing algorithm will be used).

        :param io_cap: new IO capabilities
        :type io_cap: GAP_IO_CAPABILITIES
        :return: result code
        :rtype: BLE_ERROR
        """
        return self._ble_manager.set_io_cap(io_cap)

    def start(self, role: BLE_GAP_ROLE) -> BLE_ERROR:
        """Start the BLE module as a central device

        :param role: GAP role of the device
        :type role: BLE_GAP_ROLE
        :return: result code
        :rtype: BLE_ERROR
        """

        error = self._ble_reset()
        if error == BLE_ERROR.BLE_STATUS_OK:
            error = self._ble_gap.role_set(role)

        return error

    def storage_get_int(self, conn_idx: int, key: int) -> tuple[BLE_ERROR, int]:
        return self._ble_storage.get_int(conn_idx, key)

    def storage_put_int(self, conn_idx: int, key: int, value: int, persistent: bool) -> BLE_ERROR:
        return self._ble_storage.put_int(conn_idx, key, value, persistent)
