# py_ble_manager_programmer

A utility for programming DA14xxx development kit flash with py_ble_manager compatible firmware.

If you have installed py_ble_manager, you can call the executable in your *<Python install dir/Scripts>*:

`py_ble_manager_programmer`

> **_NOTE:_** If py_ble_manager_programmer is not found in your terminal, ensure *<Python install dir/Scripts>* is in your path.

To run the python script directly call:

`python py_ble_manager_programmer.py`

Once running the script will:

1. identify J-Link devices connected to your PC
2. prompt you for which J-Link device to program
3. connect to your development kit over J-Link
4. erase the flash
5. program the appropriate py_ble_manager compatible binary
6. reset the device to start the firmware application

J-Link selection prompt:

![prompt](assets/prompt.png)

Progress with erasing/programming/resetting will be printed to the terminal:

![terminal](assets/terminal.png)

Once the script is complete, your development kit is ready to communicate with the py_ble_manager library.

> **_NOTE:_** Occasionally the script fails to reset the target to start the firmware. Simply press the reset button or remove and re-apply power to your development kit to reset the device.

If the LED on the development kit is illuminated, the application is running. Below shows the LED for various development kits:

* The DA14531 Pro Development kit: <br> ![da14531_pro_kit](assets/da14531_pro_kit_jumpers_led_on.png)

* The DA14531MOD Pro Development kit: <br> ![da14531mod_pro_kit](assets/da14531mod_pro_kit_jumpers_led_on.png)

* DA1469x Pro Development kit: <br> ![da1469x_pro_kit](assets/da1469x_pro_kit_jumpers_led_on.png)

* DA1469x USB Development kit: <br> ![da1469x_usb_kit](assets/da1469x_usb_kit_jumpers_led_on.png)

In the case of the DA1469x, you will be prompted which kit to use:

![terminal_69x_kit_type](assets/terminal_69x_kit_type.png)

For the Pro kit, you will be prompted which baud rate to use:

![terminal](assets/terminal_baud.png)

> **_NOTE:_** the default `baud_rate` used by a `BleCentral` object is 1M. If you select the 3M baud option, ensure you pass in the `baud_rate` parameter when creating a `BleCentral` object:

```Python
import py_ble_manager as ble

central = ble.BleCentral("COM54", baud_rate=3000000)
```

For the UBS Kit, firmware supporting a baud rate of 115200 will automatically be downloaded:

![terminal_69x_usb](assets/terminal_69x_usb.png)

> **_NOTE:_** the default `baud_rate` used by a `BleCentral` object is 1M. If you are using the USB kit, ensure you pass in the `baud_rate` parameter when creating a `BleCentral` object:

```Python
import py_ble_manager as ble

central = ble.BleCentral("COM54", baud_rate=115200)
```
