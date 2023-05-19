Basic Usage
===========

The primary interface to the library is the :py:class:`~py_ble_manager.ble_devices.BleCentral` class, which provides methods to initiate BLE operations
and handle asynchronous BLE events.

Create a BLE Central object and perform initialization
------------------------------------------------------

.. code-block:: python

    import py_ble_manager as ble

    central = ble.BleCentral("COM54")
   
    # Initialize the Python BLE Framework
    central.init()

    # Start operating as a BLE Central 
    central.start()

    # Set the IO capabilities
    central.set_io_cap(ble.GAP_IO_CAPABILITIES.GAP_IO_CAP_KEYBOARD_DISP)

Initiate a BLE Operation
------------------------

Scanning
^^^^^^^^
.. code-block:: python

    central.scan_start(type=ble.GAP_SCAN_TYPE.GAP_SCAN_ACTIVE,
                       mode=ble.GAP_SCAN_MODE.GAP_SCAN_GEN_DISC_MODE,
                       interval=160,
                       window=80,
                       filt_wlist=False,
                       filt_dupl=True)

Connecting
^^^^^^^^^^

.. code-block:: python

    peripheral_addr: ble.BdAddress = ble.BleUtils.str_to_bd_addr("48:23:35:00:1b:53,P") 
    connection_params = ble.GapConnParams(interval_min_ms=50, interval_max_ms=70, slave_latency=0, sup_timeout_ms=420)
    central.connect(peripheral_addr, connection_params)


Read a characteristic value
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    central.read(conn_idx=0, handle=24, offset=0) 


Write a characteristic value
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    central.write(conn_idx=0, handle=24, offset=0, value=1234) 


Disconnect
^^^^^^^^^^

.. code-block:: python

    central.disconnect(conn_idx=0) 

Handle asynchronous events
--------------------------

The framework returns asynchronous events to the application through an event queue. Calling ``BleCentral.get_event()`` will get an event from the queue. 
All of the events returned by ``BleCentral.get_event()`` are a subclass of :py:class:`~py_ble_manager.ble_api.BleCommon.BleEventBase`.
A variety of different events occur throughout the life a BLE application. Some example events include 
:py:class:`~py_ble_manager.ble_api.BleGap.BleEventGapConnectionCompleted`, :py:class:`~py_ble_manager.ble_api.BleGap.BleEventGapDisconnected`, 
:py:class:`~py_ble_manager.ble_api.BleGattc.BleEventGattcReadCompleted`, :py:class:`~py_ble_manager.ble_api.BleGattc.BleEventGattcWriteCompleted`.
Each event has an ``evt_code`` to identify the type of event.  

For example, after you initiate a write you will receive a :py:class:`~py_ble_manager.ble_api.BleGattc.BleEventGattcWriteCompleted` event which has an ``evt_code`` of 
:py:class:`~py_ble_manager.ble_api.BleCommon.BLE_EVT_GATTC.BLE_EVT_GATTC_WRITE_COMPLETED`. Your application can
handle the event however it sees fit. If your application does not handle the event, call ``BleCentral.handle_event_default()`` to have the BLE framework process the event for you.

.. code-block:: python

    # This call will block until an event is available. Use the timeout parameter to block for a specified period of time
    evt = central.get_event()
        
        # Determine which event occurred. It will be of type BLE_EVT_GAP, BLE_EVT_GATTC, or BLE_EVT_GATTS
        match evt.evt_code:

            # Handle the event
            case ble.BLE_EVT_GAP.BLE_EVT_GAP_ADV_REPORT:
                # Define your own handling function to process the event
                handle_evt_gap_adv_report(evt)
            case ble.BLE_EVT_GAP.BLE_EVT_GAP_SCAN_COMPLETED:
                handle_evt_gap_scan_completed(evt)
            case ble.BLE_EVT_GAP.BLE_EVT_GAP_CONNECTED:
                handle_evt_gap_connected(evt)
            case ble.BLE_EVT_GAP.BLE_EVT_GAP_CONNECTION_COMPLETED:
                handle_evt_gap_connection_completed(evt)
            case ble.BLE_EVT_GAP.BLE_EVT_GAP_DISCONNECTED:
                handle_evt_gap_disconnected(evt)
            case ble.BLE_EVT_GATTC.BLE_EVT_GATTC_BROWSE_SVC:
                handle_evt_gattc_browse_svc(evt)
            case ble.BLE_EVT_GATTC.BLE_EVT_GATTC_BROWSE_COMPLETED:
                handle_evt_gattc_browse_completed(evt)
            case ble.BLE_EVT_GATTC.BLE_EVT_GATTC_NOTIFICATION:
                handle_evt_gattc_notification(evt)
            case ble.BLE_EVT_GATTC.BLE_EVT_GATTC_WRITE_COMPLETED:
                handle_evt_gattc_write_completed(evt)
            case ble.BLE_EVT_GATTC.BLE_EVT_GATTC_READ_COMPLETED:
                handle_evt_gattc_read_completed(evt)

            case _:
                # For any events not handled by your application, call the BleCentral default handler to process the event
                central.handle_event_default(evt)
