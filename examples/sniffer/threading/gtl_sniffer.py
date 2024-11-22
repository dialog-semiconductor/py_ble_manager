import argparse
import logging
import sys
import py_ble_manager as ble


def main(com_port_1: str, com_port_2: str, baud_rate: int, log_file: str = None):
    logger = logging.getLogger(__name__)
    if log_file:
        logging.basicConfig(level=logging.INFO,
                            filename=log_file,
                            format='[%(asctime)s.%(msecs)03d] %(message)s',
                            datefmt='%H:%M:%S')
    else:
        logging.basicConfig(level=logging.INFO,
                            stream=sys.stdout,
                            format='[%(asctime)s.%(msecs)03d] %(message)s',
                            datefmt='%H:%M:%S')

    sniffer = ble.GtlSniffer(com_port_1, com_port_2, baud_rate)
    sniffer.init()

    print("Capturing...")

    while True:
        msg = sniffer.get_gtl_msg_str()
        if msg:
            logger.info(msg)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='BLE Central Simple Scan ',
                                     description='A simple example demonstrating scanning for peripherals')

    parser.add_argument("com_port_1", type=str, help='')
    parser.add_argument("baud_rate", type=int, help='')
    parser.add_argument("--com_port_2", type=str, help='')
    parser.add_argument("--log_file", type=str, help='')

    args = parser.parse_args()

    try:
        main(args.com_port_1, args.com_port_2, args.baud_rate, args.log_file)
    except KeyboardInterrupt:
        print("Exiting")
