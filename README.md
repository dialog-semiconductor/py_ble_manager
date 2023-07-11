# py_ble_manager

A python library for controlling Renesas BLE devices.

## Purpose

The intent of this library is to provide a python interface similar to [SDK10](http://lpccs-docs.renesas.com/um-b-092-da1469x_software_platform_reference/User_guides/User_guides.html#the-ble-framework) for controlling BLE of DA14xxx devices. This is achieved by communicating with a development kit running Generic Transport Layer (GTL) supported firmware over a USB port on your PC:

![](https://raw.githubusercontent.com/dialog-semiconductor/py_ble_manager/blob/main/assets/usb_to_pc.png)

The primary intent is for use as a central device for benchtop testing, continuous integration, or as an end-of-line tool. For additional information on the GTL please see the [GTL User Manual](https://www.renesas.com/us/en/document/mat/um-b-143-renesas-external-processor-interface-gtl-interface?language=en&r=1564826).

## Quick Start

1. Refer to the [hardware setup](https://github.com/dialog-semiconductor/py_ble_manager/blob/main/docs/source/hardware_setup.rst) to setup the jumpers on your development kit.

2. Call: `pip install "py_ble_manager[dev] @ git+https://github.com/dialog-semiconductor/py_ble_manager.git"` to install the `py_ble_manager` package and its dependencies.

    > **_NOTE:_**
      Specifying [dev] will install optional dependency: [prompt_toolkit](https://pypi.org/project/prompt-toolkit/).
      `prompt_toolkit` is used in some of the examples to provide a command line interface.

    > **_NOTE:_**
      This library requires Python v3.10.5 or later.

3. [Download](https://github.com/dialog-semiconductor/py_ble_manager/tree/main/src/py_ble_manager/util) the py_ble_manager compatible firmware binary to the development kit by calling the `py_ble_manager_programmer`
utility from the terminal.

4. The package is now installed and you are ready to run one of the [examples](https://github.com/dialog-semiconductor/py_ble_manager/tree/main/examples)!

## Basic Usage

### Create a BLE Central object and perform initialization

```Python
import py_ble_manager as ble

central = ble.BleCentral("COM54")

# Initialize the Python BLE Framework
central.init()

# Start operating as a BLE Central 
central.start()

# Set the IO capabilities
central.set_io_cap(ble.GAP_IO_CAPABILITIES.GAP_IO_CAP_KEYBOARD_DISP)
```

### Initiate a BLE Operation

Some examples include:

Scanning:

```Python
central.scan_start(type=ble.GAP_SCAN_TYPE.GAP_SCAN_ACTIVE,
                   mode=ble.GAP_SCAN_MODE.GAP_SCAN_GEN_DISC_MODE,
                   interval_ms=100,
                   window_ms=50,
                   filt_wlist=False,
                   filt_dupl=True)
```

Connecting:

```Python
peripheral_addr: ble.BdAddress = ble.BleUtils.str_to_bd_addr("48:23:35:00:1b:53,P") 
connection_params = ble.GapConnParams(interval_min_ms=50, interval_max_ms=70, slave_latency=0, sup_timeout_ms=420)
central.connect(peripheral_addr, connection_params)
```

Read a characteristic value

```Python
central.read(conn_idx=0, handle=24, offset=0) 
```

Write a characteristic value

```Python
central.write(conn_idx=0, handle=24, offset=0, value=1234) 
```

Disconnect

```Python
central.disconnect(conn_idx=0) 
```

### Handle asynchronous events

The framework returns asynchronous events to the application through an event queue. Calling `BleCentral.get_event()` will get an event from the queue. All of the events returned by `BleCentral.get_event()` are a subclass of `BleEventBase`.
A variety of different events occur throughout the life a BLE application. Some example events include `BleEventGapConnectionCompleted`, `BleEventGapDisconnected`, `BleEventGattcReadCompleted`, `BleEventGattcWriteCompleted`.
Each event has an `evt_code` to identify the type of event.  

For example, after you initiate a write you will receive a `BleEventGattcWriteCompleted` event which has an `evt_code` of `BLE_EVT_GATTC.BLE_EVT_GATTC_WRITE_COMPLETED`. Your application can
handle the event however it sees fit. If your application does not handle the event, call `BleCentral.handle_event_default()` to have the BLE framework process the event for you.

```Python
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
```

## Architecture

Refer to the [architecture](https://github.com/dialog-semiconductor/py_ble_manager/blob/main/docs/architecture.md) description.
