# python_gtl

A python library for controlling Renesas BLE devices (DA14xxx) using the Generic Transport Layer (GTL)

For additional information on the GTL please see the [GTL User Manual](https://www.renesas.com/us/en/document/mat/um-b-143-renesas-external-processor-interface-gtl-interface?language=en&r=1564826)

## Purpose

The intent of this library is to provide a python interface similar to [SDK10](http://lpccs-docs.renesas.com/um-b-092-da1469x_software_platform_reference/User_guides/User_guides.html#the-ble-framework) for controlling BLE of DA14xxx devices. This is achieved by communicating with a development kit running GTL supported firmware over a USB port on your PC.

![usb_to_pc](assets/usb_to_pc.png)

The primary intent is for use as a central device for benchtop testing, continuous integration, or as an end-of-line tool.

## Framework Overview

The BLE Framework implemented in SDK10 is depecited below:

![BLE_Framework](assets/BLE_Framework.png)

In SDK10, FreeRTOS is used as an operating system. FreeRTOS provides prioritized scheduling of tasks as well as primitives for communication between tasks such as queues, mutexes, semaphores, etc.

This library provides a python implementation for several layers of the SDK10 BLE Framework (BLE Service Framework, Dialog BLE API Library, BLE Manager, and BLE Adapter) in order to control DA14xxx devices from a python enviornment running on your PC. The python [asyncio](https://docs.python.org/3/library/asyncio.html) library is used to achieve concurrency between tasks.

The architecture implemented in python is depecited below:

![PythonGtl](assets/PythonGtl.png)

It is largely similar to the original SDK10 architecture, with the addition of the `Serial Manager` layer, whose responsibility it is to communicate serialized GTL messages with the development kit over the serial port.

## Getting Started

To use the library, the DA14xxx device must be running firmware that supports GTL commands. 

For DA14585/DA14531 devices, SDK6 includes projects which support GTL commands. Specifically the  `empty_template_ext` project, located in `projects\target_apps\template\empty_template_ext`, is a good starting point for a GTL based application.

In addition the `prox_reporter_ext` and `prox_monitor_ext` projects, located in the `projects\target_apps\ble_examples\prox_reporter_ext` and
`projects\target_apps\ble_examples\prox_monitor_ext` folders respectively, are available.

To communicate with a DA145xx running GTL supported firmware from python, you must setup your development kit as described in [here](http://lpccs-docs.renesas.com/UM-140-DA145x-CodeLess/howToUse.html#hardware-setup). Please note, you may need to modify the UART pin definitions defined in `user_periph_setup.h` of the firmware project you use (e.g. `empty_template_ext`) depending on which daughterboard you are using.

Once you have programmed the development kit with GTL supported firmware, you are ready to communicate with it from python.

The [central_at_command](example/central_at_command/central_at_command_cli.py) is the most developed example. It provides a AT Command like interface to control a BLE central deivce. 

## High Level Directory Overview

### ble_devices

The [ble_devices](ble_devices) directory contains the primary classes enabling a user to interact with the python BLE framework, namely the `BleCentral` and `BlePeripheral` classes. These classes provide methods for achieving most of the functionality required by a BLE application.

For example, the `BleCentral` class implement methods for scanning, connecting, browsing, discovering, reading, writing, etc. These methods are typically wrappers for various methods implemented in the `ble_api`.

### services

TODO

### ble_api

The [ble_api](ble_api) directory contains classes that implement the functionality of the `Dialog BLE API Library`. For example, `BleGap.py` implements functionality of the `ble_gap.c` API.

### manager

The [manager](manager) directory contains classes that implement the functionality of the `BLE Manager`.

### adapter
The [adapter](adapter) directory contains classes that implement the functionality of the `BLE Adapater`

### serial_manager

The [serial_manager](serial_manager) directory contains the `SerialStreamManager` class. It is responsible for transmitting serialized GTL messages from the BLE Adapter over the serial port. In addition, it receives serialized GTL messages over the serial port (from the development kit) and provides them to the `BleAdapter` for consumption.

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