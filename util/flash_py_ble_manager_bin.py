import argparse
from io import TextIOWrapper
import json
import os
import sys


import ezFlashCLI.cli
from ezFlashCLI.ezFlash.smartbond.smartbondDevices import da14xxx, da14531


def flash(bin_path: TextIOWrapper, mcu: str):

    mcu: da14xxx
    # create appropriate device object
    match mcu:
        case "DA14531":
            mcu = da14531()
        case _:
            print("MCU not supported")
            sys.exit(1)

    with open(os.path.join(os.path.dirname(os.path.abspath(ezFlashCLI.__file__)), 'flash_database.json')) as json_file:
        flash_db = json.load(json_file)
        json_file.close()

    # open binary and load data
    bin_file = open(bin_path, 'rb')
    bin_data = bin_file.read()

    # connect thru Jlink.
    # If only one JLink device is attached to PC, it will automatically be connected to.
    # If multiple are connected, you will be prompted to select which to perform operation on
    mcu.connect(None)

    # get the flash ID
    flash_id = mcu.flash_probe()

    # erase
    print("Erasing flash...")
    mcu.flash_erase()

    # program
    print("Programming binary...")
    flash = mcu.get_flash(flash_id, flash_db)
    mcu.flash_program_image(bin_data, flash)
    print("Finished programming.")

    # reset the device to start the application
    print("Resetting device...")
    mcu.link.resetNoHalt()
    print("Firmware is running and the serial port is available for communication with py_ble_manager!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Py BLE Manager Flash Utility',
                                     description='Program your development kit flash with a compatibile firmware binary')

    parser.add_argument("bin", type=str, help='Binary file to download to development kit')
    parser.add_argument("mcu", type=str, help='BLE MCU on your development kit')

    args = parser.parse_args()

    try:
        flash(args.bin, args.mcu)
    except KeyboardInterrupt:
        pass
