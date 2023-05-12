import argparse
# import logging
import threading
import queue
from enum import IntEnum, auto
import os
from pathlib import Path
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.patch_stdout import patch_stdout
import time

from debug_crash_info import DciData, DciFaultInfo, CortexM0StackFrame, DciSvcResponse, DCI_LAST_FAULT_HANDLER, DCI_REST_REASON, DCI_SVC_COMMAND
import python_gtl_thread as ble


FILE_PATH = Path(__file__).parent

DEBUG_CRASH_INFO_SVC_UUID_STR = "21ce31fc-da27-11ed-afa1-0242ac120002"
DEBUG_CRASH_INFO_RX_CHAR_UUID_STR = "8a8b791b-82f3-4ecf-9ce4-7d422c371a01"
DEBUG_CRASH_INFO_TX_CHAR_UUID_STR = "17738e00-54f9-4a2c-a6ed-1ee67e00f323"
CCC_UUID_STR = "2902"
USER_DESC_UUID_STR = "2901"

DEVICE_NAME_HANDLE = 3


class FETCH_DATA_STATE(IntEnum):
    FETCH_DATA_NONE = auto()
    FETCH_DATA_CONNECT = auto()
    FETCH_DATA_WAIT_FOR_NAME = auto()
    FETCH_DATA_BROWSE_DCI = auto()
    FETCH_DATA_ENABLE_CCC = auto()
    FETCH_DATA_SEND_GET_DATA_COMMAND = auto()
    FETCH_DATA_WAIT_FOR_RESPONSE = auto()
    FETCH_DATA_DISCONNECT = auto()
    FETCH_DATA_DONE = auto()
    FETCH_DATA_ERROR = auto()


class GATT_EVENT(IntEnum):
    GATT_EVENT_NONE = 0x0000
    GATT_EVENT_NOTIFICATION = 0x0001
    GATT_EVENT_INDICATION = 0x0002


class DebugCrashInfoSvc():
    def __init__(self):
        self.svc_handle = 0
        self.rx = ble.GattcItem()
        self.rx_user_desc = ble.GattcItem()
        self.tx = ble.GattcItem()
        self.tx_user_desc = ble.GattcItem()
        self.tx_ccc = ble.GattcItem()


class CLIHandler():
    def __init__(self, ble_command_q: queue.Queue, ble_response_q: queue.Queue):
        self.ble_command_q = ble_command_q
        self.ble_response_q = ble_response_q
        self.exit = threading.Event()

    def start_prompt(self):
        # Accepted commands
        commands = ['GAPSCAN',
                    'GETALLRESETDATA',
                    'EXIT']
        commands.sort()
        word_completer = WordCompleter(commands, ignore_case=True)

        self.session = PromptSession(completer=word_completer)
        while True:
            with patch_stdout():
                try:
                    if self.exit.is_set():
                        return
                    input: str = self.session.prompt('>>> ')
                    if input:
                        args = input.split()
                        # Ensure we have a valid command
                        if input and args[0] in commands:
                            self.ble_command_q.put_nowait(input)
                            response = self.ble_response_q.get()
                        else:
                            response = "ERROR Invalid Command"
                        print(f"<<< {response}")
                except KeyboardInterrupt:
                    print("Session Keyboard Interrupt")
                    return

                # TODO wait for event from ble_task before accepting additional input (eg scan done)?

    def shutdown(self):
        try:
            if self.session and self.session.app.is_running:
                self.session.app.exit()
                self.exit.set()
        finally:
            pass


class BleController():
    def __init__(self,
                 com_port: str,
                 command_q: queue.Queue,
                 response_q: queue.Queue,
                 log: object = None):  # TODO correct type hint for file handle

        self.com_port = com_port
        self.command_q = command_q
        self.response_q = response_q
        self._exit = threading.Event()
        #                                 name, adv packet, scan rsp packet
        self.scan_dict: dict[bytes, tuple[str, ble.BleEventGapAdvReport, ble.BleEventGapAdvReport]] = {}
        self.crash_info_uuid: ble.AttUuid = ble.BleUtils.uuid_from_str(DEBUG_CRASH_INFO_SVC_UUID_STR)

        self.connected_addr: ble.BdAddress = ble.BdAddress()
        self.browse_data = []
        self.dci_svc = DebugCrashInfoSvc()
        self.fetch_state = FETCH_DATA_STATE.FETCH_DATA_NONE
        self.response = DciSvcResponse()
        self.reset_data = DciData()
        self.connected_name = "Unknown"
        self.device_name_char = ble.GattcItem()
        self.log_file_handle = log

    def _command_queue_task(self):
        while True:
            command = self.command_queue_get()
            error = self.handle_console_command(command)
            if error == ble.BLE_ERROR.BLE_STATUS_OK:
                response = "OK"
            else:
                response = f"ERROR {error}"
            self.response_q.put_nowait(str(response))

    def _event_queue_task(self):
        while True:
            evt = self.central.get_event()
            if evt:
                self.handle_ble_event(evt)

    def ble_task(self):
        assert self.com_port
        assert self.command_q
        assert self.response_q

        # initalize central device
        self.central = ble.BleCentral(self.com_port, gtl_debug=False)
        self.central.init()
        self.central.start()
        self.central.set_io_cap(ble.GAP_IO_CAPABILITIES.GAP_IO_CAP_KEYBOARD_DISP)

        self._command_task = threading.Thread(target=self._command_queue_task)
        self._command_task.daemon = True
        self._command_task.start()

        self._evnt_task = threading.Thread(target=self._event_queue_task)
        self._evnt_task.daemon = True
        self._evnt_task.start()

        self._exit.wait()

    def command_queue_get(self):
        return self.command_q.get()

    def handle_ble_event(self, evt: ble.BleEventBase = None):
        if evt:
            match evt.evt_code:
                case ble.BLE_EVT_GAP.BLE_EVT_GAP_ADV_REPORT:
                    self.handle_evt_gap_adv_report(evt)
                case ble.BLE_EVT_GAP.BLE_EVT_GAP_SCAN_COMPLETED:
                    self.handle_evt_gap_scan_completed(evt)
                case ble.BLE_EVT_GAP.BLE_EVT_GAP_CONNECTED:
                    self.handle_evt_gap_connected(evt)
                case ble.BLE_EVT_GAP.BLE_EVT_GAP_CONNECTION_COMPLETED:
                    self.handle_evt_gap_connection_compelted(evt)
                case ble.BLE_EVT_GAP.BLE_EVT_GAP_DISCONNECTED:
                    self.handle_evt_gap_disconnected(evt)
                case ble.BLE_EVT_GATTC.BLE_EVT_GATTC_BROWSE_SVC:
                    self.handle_evt_gattc_browse_svc(evt)
                case ble.BLE_EVT_GATTC.BLE_EVT_GATTC_BROWSE_COMPLETED:
                    self.handle_evt_gattc_browse_completed(evt)
                case ble.BLE_EVT_GATTC.BLE_EVT_GATTC_NOTIFICATION:
                    self.handle_evt_gattc_notification(evt)
                case ble.BLE_EVT_GATTC.BLE_EVT_GATTC_WRITE_COMPLETED:
                    self.handle_evt_gattc_write_completed(evt)
                case ble.BLE_EVT_GATTC.BLE_EVT_GATTC_READ_COMPLETED:
                    self.handle_evt_gattc_read_completed(evt)

                case _:
                    self.central.handle_event_default(evt)

            self.process_fetch_state(evt)

    def handle_console_command(self, command: str) -> ble.BLE_ERROR:
        error = ble.BLE_ERROR.BLE_ERROR_FAILED
        args = command.split()
        if len(args) > 0:
            ble_func = args[0]
            match ble_func:
                case 'GAPSCAN':
                    # Expected command format: >>>GAPSCAN
                    self.scan_dict: dict[bytes, tuple[str, ble.BleEventGapAdvReport]] = {}
                    self.log("Starting scan...")
                    error = self.central.scan_start(ble.GAP_SCAN_TYPE.GAP_SCAN_ACTIVE,
                                                    ble.GAP_SCAN_MODE.GAP_SCAN_GEN_DISC_MODE,
                                                    160,
                                                    80,
                                                    False,
                                                    True)

                case "GETALLRESETDATA":
                    # Expected command format: >>>GETALLRESETDATA 48:23:35:00:1b:53,P
                    if len(args) == 2:
                        periph_bd = ble.BleUtils.str_to_bd_addr(args[1])
                        periph_conn_params = ble.GapConnParams(50, 70, 0, 420)
                        error = self.central.connect(periph_bd, periph_conn_params)

                    # move to state machine function
                    if error == ble.BLE_ERROR.BLE_STATUS_OK:
                        self.fetch_state = FETCH_DATA_STATE.FETCH_DATA_CONNECT

                case "EXIT":
                    # Expected command format: EXIT
                    self.shutdown()
                    error = ble.BLE_ERROR.BLE_STATUS_OK

                case _:
                    pass

        return error

    def handle_evt_gap_adv_report(self, evt: ble.BleEventGapAdvReport):

        name = "Unknown"
        adv_packet = False  # used to separate adv packets from scan responses

        # Parse the advertising structures
        ad_structs = self.parse_adv_data(evt)
        for ad_struct in ad_structs:
            if ad_struct.type == ble.GAP_DATA_TYPE.GAP_DATA_TYPE_FLAGS:
                # This is an advertising packet (vs scan response)  # TODO How to initiate scan request from Central?
                adv_packet = True

            if (ad_struct.type == ble.GAP_DATA_TYPE.GAP_DATA_TYPE_LOCAL_NAME
                    or ad_struct.type == ble.GAP_DATA_TYPE.GAP_DATA_TYPE_SHORT_LOCAL_NAME):
                # device name found
                decoded_name = ad_struct.data.decode("utf-8")
                if decoded_name != '\x00':  # some devices have a null character for the short name, ignore them
                    name = decoded_name

        if adv_report := self.scan_dict.get(evt.address.addr):
            # Item exists in the scan dict, update it
            # if we have a name for this device, do not overwrite it with Unknown
            if adv_report[0] != "Unknown":
                name = adv_report[0]
            if adv_packet:
                self.scan_dict[evt.address.addr] = (name, evt, adv_report[2])
            else:
                self.scan_dict[evt.address.addr] = (name, adv_report[1], evt)
        else:
            # Item does not exist in the scan dict, add it to the dict
            for ad_struct in ad_structs:
                # only want devices that advertise Debug Crash Info Service
                if (ad_struct.type == ble.GAP_DATA_TYPE.GAP_DATA_TYPE_UUID128_SVC_DATA
                        and ad_struct.data[:-1] == self.crash_info_uuid.uuid):
                    # first time seeing this device, add it to dict with an empty scan rsp
                    self.scan_dict[evt.address.addr] = (name, evt, ble.BleEventGapAdvReport())

    def handle_evt_gap_connected(self, evt: ble.BleEventGapConnected):
        self.connected_addr = evt.peer_address
        self.log(f"Connected to: address={ble.BleUtils.bd_addr_to_str(evt.peer_address)}")

    def handle_evt_gap_connection_compelted(self, evt: ble.BleEventGapConnectionCompleted):
        self.log(f"Connection completed: status={evt.status.name}")

    def handle_evt_gap_disconnected(self, evt: ble.BleEventGapDisconnected):
        self.log(f"Disconnected from addr={ble.BleUtils.bd_addr_to_str(evt.address)}")

    def handle_evt_gap_scan_completed(self, evt: ble.BleEventGapScanCompleted):
        self.log("Scan complete")
        device_info = ""
        # Display information for all devices advertising with the Debug Crash Info Service
        for key in self.scan_dict:
            name, adv_packet, scan_rsp = self.scan_dict[key]
            device_info += f"Device name: {name}, addr: {ble.BleUtils.bd_addr_to_str(adv_packet.address)}"

            ad_structs = self.parse_adv_data(adv_packet)
            for ad_struct in ad_structs:
                if ad_struct.type == ble.GAP_DATA_TYPE.GAP_DATA_TYPE_UUID128_SVC_DATA:
                    num_resets = ad_struct.data[-1]
                    device_info += f", number of resets: {num_resets}"

            self.log(device_info)

    def handle_evt_gattc_browse_completed(self, evt: ble.BleEventGattcBrowseCompleted):
        self.log(f"Browsing complete: conn_idx={evt.conn_idx}, evt={evt.status.name}")

    def handle_evt_gattc_browse_svc(self, evt: ble.BleEventGattcBrowseSvc):

        # If browse info is for Debug Crash Info Service,  store attribute handles so we can access attributes via read/write/etc.
        if (ble.BleUtils.uuid_from_str(DEBUG_CRASH_INFO_SVC_UUID_STR) == evt.uuid):
            self.dci_svc.svc_handle = evt.start_h
            for item in evt.items:
                if item.type == ble.GATTC_ITEM_TYPE.GATTC_ITEM_TYPE_CHARACTERISTIC:
                    if item.uuid == ble.BleUtils.uuid_from_str(DEBUG_CRASH_INFO_RX_CHAR_UUID_STR):
                        self.dci_svc.rx = item
                    elif item.uuid == ble.BleUtils.uuid_from_str(DEBUG_CRASH_INFO_TX_CHAR_UUID_STR):
                        self.dci_svc.tx = item

                elif item.type == ble.GATTC_ITEM_TYPE.GATTC_ITEM_TYPE_DESCRIPTOR:
                    if item.handle == self.dci_svc.rx.handle + 2:
                        self.dci_svc.rx_user_desc = item
                    elif (item.handle == self.dci_svc.tx.handle + 2
                            or item.handle == self.dci_svc.tx.handle + 3):

                        if ble.BleUtils.uuid_to_str(item.uuid) == CCC_UUID_STR:
                            self.dci_svc.tx_ccc = item
                        elif ble.BleUtils.uuid_to_str(item.uuid) == CCC_UUID_STR:
                            self.dci_svc.tx_user_desc = item

    def handle_evt_gattc_notification(self, evt: ble.BleEventGattcNotification):
        self.log(f"Received Notification: conn_idx={evt.conn_idx}, handle={evt.handle}, value={evt.value.hex()}")

    def handle_evt_gattc_read_completed(self, evt: ble.BleEventGattcReadCompleted):
        self.log(f"Read Complete: conn_idx={evt.conn_idx}, handle={evt.handle}, status={evt.status.name}, value={evt.value.hex()}")

    def handle_evt_gattc_write_completed(self, evt: ble.BleEventGattcWriteCompleted):
        self.log(f"Write Complete: conn_idx={evt.conn_idx}, handle={evt.handle}, status={evt.status.name}")

    def log(self, string):
        print(string)
        if self.log_file_handle:
            self.log_file_handle.write(string + "\n")
        # logging.info(string)

    def log_reset_data(self):
        self.log("*******************Debug Crash Info*******************")
        self.log(f"Device name: {self.connected_name}")
        self.log(f"Device address: {ble.BleUtils.bd_addr_to_str(self.connected_addr)}")
        self.log(f"Last reset reason: {self.reset_data.last_reset_reason.name}")
        self.log(f"Number of resets: {self.reset_data.num_resets}")

        for i in range(self.reset_data.num_resets):
            if self.reset_data.fault_data[i].data_valid:
                self.log(f"Fault Data #{i}:")
                self.log(f"\t Epoch: {self.reset_data.fault_data[i].epoch}")
                self.log(f"\t Fault Type: {self.reset_data.fault_data[i].fault_handler.name}")
                self.log("\t Last stack frame: ")
                self.log(f"\t\t r0:  0x{self.reset_data.fault_data[i].stack_frame.r0:08x}")
                self.log(f"\t\t r1:  0x{self.reset_data.fault_data[i].stack_frame.r1:08x}")
                self.log(f"\t\t r2:  0x{self.reset_data.fault_data[i].stack_frame.r2:08x}")
                self.log(f"\t\t r3:  0x{self.reset_data.fault_data[i].stack_frame.r3:08x}")
                self.log(f"\t\t r12: 0x{self.reset_data.fault_data[i].stack_frame.r12:08x}")
                self.log(f"\t\t LR:  0x{self.reset_data.fault_data[i].stack_frame.LR:08x}")
                self.log(f"\t\t return_address: 0x{self.reset_data.fault_data[i].stack_frame.return_address:08x}")
                self.log(f"\t\t xPSR: 0x{self.reset_data.fault_data[i].stack_frame.xPSR:08x}")

                self.log("\t Call trace: ")
                for j in range(self.reset_data.fault_data[i].num_of_call_vals):
                    self.log(f"\t\t Call address {j}: 0x{self.reset_data.fault_data[i].call_trace[j]:08x}")

        self.log("*****************Debug Crash Info End*****************")

    def parse_adv_data(self, evt: ble.BleEventGapAdvReport) -> list[ble.BleAdvData]:
        data_ptr = 0
        adv_data_structs: ble.BleAdvData = []
        if evt.length > 0:
            while data_ptr < 31 and data_ptr < evt.length:
                struct = ble.BleAdvData(len=evt.data[data_ptr], type=evt.data[data_ptr + 1])

                if struct.len == 0 or struct.type == ble.GAP_DATA_TYPE.GAP_DATA_TYPE_NONE:
                    break

                data_ptr += 2
                struct.data = evt.data[data_ptr:(data_ptr + struct.len - 1)]  # -1 as calc includes AD Type
                data_ptr += struct.len - 1  # -1 as calc includes AD Type
                adv_data_structs.append(struct)

        return adv_data_structs

    def parse_reset_data(self, data: bytes):

        self.reset_data.last_reset_reason = DCI_REST_REASON(data[0])
        self.reset_data.num_resets = data[1]

        # Parsing assumes data is the appropriate length
        fault_data = data[2:]
        for i in range(self.reset_data.num_resets):
            fault_data = fault_data[(i * 63):]
            self.reset_data.fault_data.append(DciFaultInfo())
            self.reset_data.fault_data[i].data_valid = bool(fault_data[0])
            self.reset_data.fault_data[i].epoch = int.from_bytes(fault_data[1:5], 'little')
            self.reset_data.fault_data[i].fault_handler = DCI_LAST_FAULT_HANDLER(fault_data[5])
            self.reset_data.fault_data[i].stack_frame = CortexM0StackFrame(fault_data[6:38])
            self.reset_data.fault_data[i].num_of_call_vals = int(fault_data[38])
            index = 39
            for _ in range(6):
                self.reset_data.fault_data[i].call_trace.append(int.from_bytes(fault_data[index:(index + 4)], 'little'))
                index = index + 4

    def process_fetch_state(self, evt: ble.BleEventBase):
        '''
        Fetch Process:
        1. Connect to the device on interest
        2. Read the device name
        3. Browse the Device Crash Info Service to determine characteristic/descriptor handles
        4. Enable TX Characteristic CCC to receive data from peripheral
        5. Send Get All Reset Data command
        6. Receive notifications with data
        7. When all data received, disconnect
        8. Parse reset data and log reset data
        9. Exit the application
        '''

        match self.fetch_state:

            case FETCH_DATA_STATE.FETCH_DATA_CONNECT:
                if (evt.evt_code == ble.BLE_EVT_GAP.BLE_EVT_GAP_CONNECTION_COMPLETED):
                    self.fetch_state = FETCH_DATA_STATE.FETCH_DATA_WAIT_FOR_NAME
                    self.central.read(0, DEVICE_NAME_HANDLE, 0)

            case FETCH_DATA_STATE.FETCH_DATA_WAIT_FOR_NAME:

                if (evt.evt_code == ble.BLE_EVT_GATTC.BLE_EVT_GATTC_READ_COMPLETED
                        and evt.handle == DEVICE_NAME_HANDLE):
                    evt: ble.BleEventGattcReadCompleted
                    self.connected_name = evt.value.decode("utf-8")
                    self.fetch_state = FETCH_DATA_STATE.FETCH_DATA_BROWSE_DCI
                    self.central.browse(0, ble.BleUtils.uuid_from_str(DEBUG_CRASH_INFO_SVC_UUID_STR))

            case FETCH_DATA_STATE.FETCH_DATA_BROWSE_DCI:
                evt: ble.BleEventGattcBrowseCompleted
                if (evt.evt_code == ble.BLE_EVT_GATTC.BLE_EVT_GATTC_BROWSE_COMPLETED
                        and self.dci_svc.svc_handle != 0):
                    self.fetch_state = FETCH_DATA_STATE.FETCH_DATA_ENABLE_CCC
                    self.central.write(0,
                                       self.dci_svc.tx_ccc.handle,
                                       0,
                                       bytes(GATT_EVENT.GATT_EVENT_NOTIFICATION.to_bytes(2, 'little'))
                                       )

            case FETCH_DATA_STATE.FETCH_DATA_ENABLE_CCC:
                if (evt.evt_code == ble.BLE_EVT_GATTC.BLE_EVT_GATTC_WRITE_COMPLETED
                        and evt.handle == self.dci_svc.tx_ccc.handle):
                    if evt.status == ble.BLE_ERROR.BLE_STATUS_OK:
                        evt: ble.BleEventGattcWriteCompleted
                        self.fetch_state = FETCH_DATA_STATE.FETCH_DATA_WAIT_FOR_RESPONSE
                        # +1 as handle is for char declaration
                        # TODO rx/tx named from perspective of periph. Change to perspective of central
                        self.central.write(0,
                                           (self.dci_svc.rx.handle + 1),  # saved handle is the char declaration, +1 to write to the char value
                                           0,
                                           bytes(DCI_SVC_COMMAND.GET_ALL_RESET_DATA.to_bytes(1, 'little'))
                                           )
                    else:
                        self.fetch_state = FETCH_DATA_STATE.FETCH_DATA_ERROR

            case FETCH_DATA_STATE.FETCH_DATA_WAIT_FOR_RESPONSE:
                if (evt.evt_code == ble.BLE_EVT_GATTC.BLE_EVT_GATTC_NOTIFICATION
                        and evt.handle == self.dci_svc.tx.handle + 1):

                    # TODO need to know what response waiting for
                    evt: ble.BleEventGattcNotification
                    if self.response.command == DCI_SVC_COMMAND.NONE and len(evt.value) > 2:
                        self.response.command = evt.value[0]
                        self.response.len = evt.value[1]
                        self.response.data += evt.value[2:]
                    else:
                        self.response.data += evt.value
                        if len(self.response.data) == self.response.len:
                            self.parse_reset_data(self.response.data)
                            self.log_reset_data()
                            self.fetch_state = FETCH_DATA_STATE.FETCH_DATA_DISCONNECT
                            self.central.disconect(0, ble.BLE_HCI_ERROR.BLE_HCI_ERROR_REMOTE_USER_TERM_CON)

            case FETCH_DATA_STATE.FETCH_DATA_DISCONNECT:
                if (evt.evt_code == ble.BLE_EVT_GAP.BLE_EVT_GAP_DISCONNECTED):
                    self.fetch_state = FETCH_DATA_STATE.FETCH_DATA_NONE
                    self.shutdown()

        if self.fetch_state == FETCH_DATA_STATE.FETCH_DATA_ERROR:
            # TODO disconnect if connected
            pass

    def shutdown(self):
        self.log_file_handle.close()
        # self.response_q.put("EXIT")
        self._exit.set()

def create_log():

    # Create the log directory if nec
    # yessary
    logs_directory = f"{FILE_PATH}\\logs"
    if not os.path.exists(logs_directory):
        os.makedirs(logs_directory)

    log_file = open(f"{logs_directory}\\DCI_log_{time.strftime('%Y%m%d-%H%M%S')}.txt", 'w')

    return log_file

    # TODO logging is preventing prompt_toolkit from patching stdout
    # open a file for writing
    # logging.basicConfig(level=logging.INFO,
    #                    format='%(asctime)s - %(message)s',
    #                    handlers=[logging.FileHandler(f"{logs_directory}\\DCI_log_{time.strftime('%Y%m%d-%H%M%S')}.txt"),
    #                              logging.StreamHandler()],)


def main(com_port: str):

    logfile = create_log()
    ble_command_q = queue.Queue()
    ble_response_q = queue.Queue()
    ble_handler = BleController(com_port, ble_command_q, ble_response_q, logfile)
    console = CLIHandler(ble_command_q, ble_response_q)

    # start 2 tasks:
    #   one for handling command line input
    #   one for handling BLE

    cli_task = threading.Thread(target=console.start_prompt)
    cli_task.daemon = True
    cli_task.start()

    ble_task = threading.Thread(target=ble_handler.ble_task)
    ble_task.daemon = True
    ble_task.start()

    while True:
        # If one of the tasks exits, clean up and exit the application
        if cli_task.is_alive() and ble_task.is_alive():
            time.sleep(1)
        else:
            if cli_task.is_alive():
                console.shutdown()
            if ble_task.is_alive():
                ble_handler.shutdown()
            return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='BLE Central Crash Info CLI',
                                     description='A command line interface for retreiving crash information from a peripheral running the Debug Crash Info ' \
                                     + 'Service')

    parser.add_argument("com_port", type=str, help='COM port for your development kit')

    args = parser.parse_args()

    try:
        main(args.com_port)
    except KeyboardInterrupt:
        print("Keyborard")
