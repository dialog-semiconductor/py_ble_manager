# python_gtl

A python library for controlling Renesas BLE devices (DA14xxx) using the Generic Transport Layer (GTL)

For additional information on the GTL please see the [GTL User Manual](https://www.renesas.com/us/en/document/mat/um-b-143-renesas-external-processor-interface-gtl-interface?language=en&r=1564826)

## Purpose

The intent of this library is to provide a python interface similar to [SDK10](http://lpccs-docs.renesas.com/um-b-092-da1469x_software_platform_reference/User_guides/User_guides.html#the-ble-framework) for controlling BLE of DA14xxx devices. This is achieved by communicating with a development kit running GTL supported firmware over a USB port on your PC:

![usb_to_pc](assets/usb_to_pc.png)

The primary intent is for use as a central device for benchtop testing, continuous integration, or as an end-of-line tool.

## Framework Overview

The BLE Framework implemented in SDK10 is depecited below:

![BLE_Framework](assets/BLE_Framework.png)

In SDK10, FreeRTOS is used as an operating system. FreeRTOS provides prioritized scheduling of tasks as well as primitives for communication between tasks such as queues, mutexes, semaphores, etc.

This library provides a python implementation for several layers of the SDK10 BLE Framework (BLE Service Framework, Dialog BLE API Library, BLE Manager, and BLE Adapter) in order to control DA14xxx devices from a python enviornment running on your PC. The python [threading](https://docs.python.org/3/library/threading.html) and [concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html) libraries are used to achieve concurrency between tasks.

The architecture implemented in python is depecited below:

![PythonGtl](assets/PythonGtl.png)

It is largely similar to the original SDK10 architecture, with the addition of the `Serial Manager` layer, whose responsibility it is to communicate serialized GTL messages with the development kit over the serial port.

## Quickstart

1. Clone or download this repository

2. Connect the jumpers on the DA14531 Pro Development kit as depicted below:

![da14531_jumpers](assets/da14531_pro_kit_jumpers.png)

3. Download the GTL enabled [firmware binary](firmware/da14531mod_pro_kit.bin) to the DA14531 Pro Development kit.

4. Open a command prompt or terminal and navigate to the directory for the repository on your PC.

5. Setup a virtual envirornment by calling: `<path_to/python_gtl_thread>$ py -3.10 -m vevn ./venv`. Note this library has been tested with Python v3.10.5. To create
a virtual enviornment that uses Python 3.10.5, you must already have Python 3.10.5 downloaded on your computer. You can download it from the [python website](https://www.python.org/downloads/release/python-3105/).

6. Activate the virtual enviornment. The specific command depends on your operating system. From a windows command prompt call: `<path_to_venv>\Scripts\activate.bat`

7. Call: `pip install -e .` to install the python_gtl_thread package and its dependencies. Note this installs the package in editable mode. This allows changes to the source code to be reflected next time the python interpreter is run.

8. The pacakge is now installed ang you are ready to run one of the [examples](examples)

## Quickstart (VS Code)

1. Follow steps 1-3 in the [Quickstart](#quickstart) section.

2. Open the `python_gtl_thread` repository directory in VS Code.

3. Setup a virtual envirornment by calling: `$ python3.10.5 -m venv ./venv` from the VS Code terminal. Note this library has been tested with Python v3.10.5. To create
a virtual enviornment that uses Python 3.10.5, you must already have Python 3.10.5 downloaded on your computer. You can download it from the [python website](https://www.python.org/downloads/release/python-3105/).

4. Activate the virtual enviornment. Hold CTRL+shift+P to opent he command palette. Select `Python: Select Interpreter`. Select the interpreter in the virtual enviorment you just created (labeled venv). 
Open a new terminal in VS Code and the virtual enviornment will be activated. 

5. Call: `pip install -e .` to install the python_gtl_thread package and its dependencies. Note this installs the package in editable mode. This allows changes to the source code to be reflected next time the python interpreter is run.

6. The pacakge is now installed ang you are ready to run one of the [examples](examples)

## High Level Directory Overview

### ble_devices

The [ble_devices](ble_devices) directory contains the primary classes enabling a user to interact with the python BLE framework, namely the `BleCentral` and `BlePeripheral` classes. These classes provide methods for achieving most of the functionality required by a BLE application.

For example, the `BleCentral` class implement methods for scanning, connecting, browsing, discovering, reading, writing, etc. These methods are typically wrappers for various methods implemented in the `ble_api`.

### services

TODO

### ble_api

The [ble_api](ble_api) directory contains classes that implement the functionality of the `Dialog BLE API Library`. For example, `BleGapApi.py` implements functionality of the `ble_gap.c` API.

### manager

The [manager](manager) directory contains classes that implement the functionality of the `BLE Manager`. For example, `BleManagerGap.py` implements functionality of the `ble_manager_gap.c` API.
It is concerned with:
- Converting commands from the [ble_api](#ble_api) to GTL messages that are passed the [adapter](#adapter).
- Converting GTL messages from the [adapter](#adapter) into responses and events understood by the [ble_api](#ble_api).

### adapter

The [adapter](adapter) directory contains the `BleAdapter` class. Its is concerned with:

- Converting GTL messages from the `BleManager` to byte streams for transmission over the serial port.
- Converting byte streams received on the serial port into Gtl messages for consumption by the `BleManager`

### serial_manager

The [serial_manager](serial_manager) directory contains the `SerialStreamManager` class. It is concerned with
- Transmitting serialized GTL messages from the BLE Adapter over the serial port
- Receiving serialized GTL messages over the serial port (from the development kit) and providing them to the `BleAdapter` for consumption.

### gtl_messages

The [gtl_messages](gtl_messages) directory contains various GTL messages defined in the [GTL User Manual](https://www.renesas.com/us/en/document/mat/um-b-143-renesas-external-processor-interface-gtl-interface?language=en&r=1564826)  

### gtl_port

The [gtl_port](gtl_port) directory is a port of files with GTL structure and enum definitions from their corresponding .h files. Each .h file has a corresponding .py file:

* co_bt.h -> co_bt.py
* co_version.h -> co_version.py
* gap.h -> gap.py
* gapm_task.h -> gapm_task.py
* rwble_hl_error.h -> rwble_hl_error.py
* rwip_config.h -> rwip_config.py
* etc.

## Architecture

Refer to the [architecture](docs/architecture.md) desciption.