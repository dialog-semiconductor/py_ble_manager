import argparse
import json
import os
import sys
import ezFlashCLI.cli
from ezFlashCLI.ezFlash.smartbond.smartbondDevices import da14xxx, da14531, SMARTBOND_IDENTIFIER
from ezFlashCLI.ezFlash.pyjlink import pyjlink
import py_ble_manager


def create_mcu(device_id_str):

    match device_id_str:
        case 'da14531':
            mcu = da14531()
        case _:
            print("MCU not supported")
            sys.exit(1)
    return mcu


def get_jlink_devices() -> list[str]:
    link = pyjlink()
    link.init()
    raw_device_list = link.browse()
    device_list = []
    for device in raw_device_list:
        if device.SerialNumber != 0:
            device_list.append(device.SerialNumber)
    return device_list


def identify_hardware_type(serial_number: str):
    # identify hardware type
    mcu = da14xxx()
    id = mcu.connect(serial_number)
    device_id_str = SMARTBOND_IDENTIFIER[id]
    # close the link
    mcu.link.close()
    return device_id_str


def load_binary_data(device_id_str: str):
    match device_id_str:
        case 'da14531':
            with open(os.path.join(os.path.dirname(os.path.abspath(py_ble_manager.__file__)), 'firmware/da14531mod_pro_kit_921600.bin'), 'rb') as bin_file:
                # open binary and load data
                bin_data = bin_file.read()
        case _:
            print("MCU not supported")
            sys.exit(1)
    return bin_data


def load_flash_db():
    with open(os.path.join(os.path.dirname(os.path.abspath(ezFlashCLI.__file__)), 'flash_database.json')) as json_file:
        flash_db = json.load(json_file)
        json_file.close()
    return flash_db


def program_binary(mcu: da14xxx, bin_data: bytes, flash_db):
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
    mcu.link.close()

    print("Firmware is running and the serial port is available for communication with py_ble_manager!")


def prompt_for_jlink_to_use(device_list: list[str]) -> int:
    # Have user select appropriate device
    print("Available JLink devices:")
    for i in range(0, len(device_list)):
        print(f"\t {i}. {device_list[i]}")
    return int(input("Select JLink device (0, 1, 2, etc): "))


def main():

    try:
        # Get a list of Jlink devices
        device_list = get_jlink_devices()

        # Have the user identify which jlink to use
        serial_num_index = prompt_for_jlink_to_use(device_list)

        # identify hardware type
        device_id_str = identify_hardware_type(device_list[serial_num_index])

        # create the appropriate mcu object and connect to it
        mcu = create_mcu(device_id_str)
        mcu.connect(device_list[serial_num_index])

        # load the appropriate binary
        bin_data = load_binary_data(device_id_str)

        # load the flash database
        flash_db = load_flash_db()

        # program the binary
        program_binary(mcu, bin_data, flash_db)

    except Exception as ex:
        print(f"Exception: {ex}")
        print("Failed to program device.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Py BLE Manager Flash Utility',
                                     description='Program your development kit flash with a compatibile firmware binary')

    try:
        main()
    except KeyboardInterrupt:
        pass