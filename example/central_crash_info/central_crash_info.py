import argparse
import aiofiles
import asyncio
from enum import IntEnum, auto
import os
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.patch_stdout import patch_stdout
import time

# TODO rethink relative import
import sys
from pathlib import Path
FILE_PATH = Path(__file__).parent
sys.path.append(str(FILE_PATH / '../../'))

import ble_devices as ble

# TODO need to rethink how configuration
ble.dg_configBLE_CENTRAL = 1
ble.dg_configBLE_PERIPHERAL = 0

DEBUG_CRASH_INFO_SVC_UUID_STR = "21ce31fc-da27-11ed-afa1-0242ac120002"
DEBUG_CRASH_INFO_RX_CHAR_UUID_STR = "8a8b791b82f34ecf9ce47d422c371a01"
DEBUG_CRASH_INFO_TX_CHAR_UUID_STR = "17738e0054f94a2ca6ed1ee67e00f323"
CCC_UUID_STR = "2902"
USER_DESC_UUID_STR = "2901"

# TODO is this always 3?
DEVICE_NAME_HANDLE = 3


class GATT_EVENT(IntEnum):
    GATT_EVENT_NONE = 0x0000
    GATT_EVENT_NOTIFICATION = 0x0001
    GATT_EVENT_INDICATION = 0x0002


class DCI_SVC_COMMAND(IntEnum):
    DCI_SERVICE_COMMAND_NONE = 0
    DCI_SERVICE_COMMAND_GET_ALL_DATA = auto()
    DCI_SERVICE_COMMAND_GET_NUM_RESETS = auto()


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

#crash_info_uuid: ble.AttUuid = self.uuid_from_str(DEBUG_CRASH_INFO_SVC_UUID_STR)


class ResetData():
    def __init__(self):
        self.command = DCI_SVC_COMMAND.DCI_SERVICE_COMMAND_NONE
        self.len = 0
        self.data = bytes()


class DebugCrashInfoSvc():
    def __init__(self):
        self.svc_handle = 0
        self.rx = ble.GattcItem()
        self.rx_user_desc = ble.GattcItem()
        self.tx = ble.GattcItem()
        self.tx_user_desc = ble.GattcItem()
        self.tx_ccc = ble.GattcItem()


class CortexM0StackFrame():
    def __init__(self, data: bytes = None):
        self.r0 = self.reg_from_bytes(data[0:4]) if data else 0
        self.r1 = self.reg_from_bytes(data[4:8]) if data else 0
        self.r2 = self.reg_from_bytes(data[8:12]) if data else 0
        self.r3 = self.reg_from_bytes(data[12:16]) if data else 0
        self.r12 = self.reg_from_bytes(data[16:20]) if data else 0
        self.LR = self.reg_from_bytes(data[20:24]) if data else 0
        self.return_address = self.reg_from_bytes(data[24:28]) if data else 0
        self.xPSR = self.reg_from_bytes(data[28:32]) if data else 0

    def reg_from_bytes(self, data: bytes):
        return int.from_bytes(data, 'little')
    

    # TODO ensure print in hex
    def __repr__(self):
        return_string = f"{type(self).__name__}(r0=0x{self.r0:08x}, r1=0x{self.r1:08x}, " + \
                        f"r2=0x{self.r2:08x}, r3=0x{self.r3:08x}, " + \
                        f"r12=0x{self.r12:08x}, LR=0x{self.LR:08x}, " + \
                        f"return_address=0x{self.return_address:08x}, xPSR=0x{self.xPSR:08x})"

        return return_string


class DCI_REST_REASON(IntEnum):
    POR = 0
    HW = auto()
    SW = auto()
    WDOG = auto()
    LAST = auto()
    NONE = auto()


class DCI_LAST_FAULT_HANDLER(IntEnum):
    HARDFAULT = 0
    NMI = auto()
    PLATFORM_RESET = auto()
    NONE = auto()


class DciFaultInfo():
    def __init__(self):
        self.data_valid: bool = False
        self.epoch: int = 0
        self.fault_handler: DCI_LAST_FAULT_HANDLER = DCI_LAST_FAULT_HANDLER.NONE 
        self.stack_frame = CortexM0StackFrame()
        self.num_of_call_vals: int = 0
        self.call_trace: list[int] = []

    def __repr__(self):
        return_string = f"{type(self).__name__}(data_valid={self.data_valid}, epoch={self.epoch}, " + \
                        f"fault_handler={self.fault_handler.name}, stack_frame={self.stack_frame}, " + \
                        f"num_of_call_vals={self.num_of_call_vals}, call_trace="
        for i in range(self.num_of_call_vals):
            return_string += f"0x{self.call_trace[i]:08x}, "
        return_string = return_string[:-2]
        return_string += ")"
        return return_string


class DciData():
    def __init__(self):
        self.last_reset_reason: DCI_REST_REASON = DCI_REST_REASON.NONE
        self.num_resets: int = 0
        self.fault_data: list[DciFaultInfo] = []

    def __repr__(self):
        return_string = f"{type(self).__name__}(last_reset_reason={self.last_reset_reason}, num_resets={self.num_resets}, " + \
                        f"fault_data={self.fault_data}"

        return return_string


async def console(ble_command_q: asyncio.Queue, ble_response_q: asyncio.Queue):
        commands = ['GAPSCAN',
                    'GETALLRESETDATA']
        commands.sort()
        word_completer = WordCompleter(commands, ignore_case=True)

        session = PromptSession(completer=word_completer)
        while True:
            with patch_stdout():
                input = await session.prompt_async('>>> ')
                ble_command_q.put_nowait(input)
                response = await ble_response_q.get()
                print(f"<<< {response}")
                #if input == 'GAPSCAN' and response == "OK":
                #    await scan_complete_evt.wait()
                # TODO wait for EVENT from ble_task before accepting additional input (eg scan done)


class BleController():
    def __init__(self, com_port: str, command_q: asyncio.Queue, response_q: asyncio.Queue):
        self.com_port = com_port
        self.command_q = command_q
        self.response_q = response_q
        #                                 name, adv packet, scan rsp packt
        self.scan_dict: dict[bytes, tuple[str, ble.BleEventGapAdvReport, ble.BleEventGapAdvReport]] = {}
        self.crash_info_uuid: ble.AttUuid = self.uuid_from_str(DEBUG_CRASH_INFO_SVC_UUID_STR)

        self.connected_addr: ble.BdAddress = ble.BdAddress()
        self.periph_addr_str = ""
        self.browse_data = []
        self.dci_svc = DebugCrashInfoSvc()
        self.fetch_state = FETCH_DATA_STATE.FETCH_DATA_NONE
        self.response = ResetData()
        self.reset_data = DciData()
        self.connected_name = "Unknown"
        self.device_name_char = ble.GattcItem()

    async def init(self):
        await self.create_log_file()
        await self.ble_task()

    async def create_log_file(self):

        self.log_tasks = set()
        # TODO move directory
        logs_directory = f"{FILE_PATH}\logs"
        if not os.path.exists(logs_directory):
            os.makedirs(logs_directory)
        self.log_file = await aiofiles.open(f'{logs_directory}\DCI_log_{time.strftime("%Y%m%d-%H%M%S")}.txt', mode='w')

    def log(self, string: str):
        print(string)
        log_to_file_task = asyncio.create_task(self.log_file.write(string + "\r"))
        self.log_tasks.add(log_to_file_task)
        log_to_file_task.add_done_callback(self.log_tasks.discard)
        # TODO create task to write str to file

    def bd_addr_to_str(self, bd: ble.BdAddress) -> str:
        return_string = ""
        for byte in bd.addr:
            byte_string = str(hex(byte))[2:]
            if len(byte_string) == 1:  # Add a leading 0
                byte_string = "0" + byte_string
            return_string = byte_string + ":" + return_string
        return return_string[:-1]

    async def ble_task(self):
        assert self.com_port
        assert self.command_q
        assert self.response_q

        # initalize central device
        self.central = ble.BleCentral(self.com_port, gtl_debug=False)
        await self.central.init()
        await self.central.start()
        self.central.set_io_cap(ble.GAP_IO_CAPABILITIES.GAP_IO_CAP_KEYBOARD_DISP)

        # create tasks for:
        #   hanlding commands from the console
        #   responding to BLE events
        self.console_command_task = asyncio.create_task(self.command_q.get(), name='GetConsoleCommand')
        self.ble_event_task = asyncio.create_task(self.central.get_event(), name='GetBleEvent')
        pending = [self.ble_event_task, self.console_command_task]

        while True:
            # Wait for a console command or BLE event to occur
            done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)

            for task in done:
                # Handle command line input
                if task is self.console_command_task:
                    command: str = task.result()
                    error = await self.handle_console_command(command)

                    if error == ble.BLE_ERROR.BLE_STATUS_OK:
                        response = "OK"
                    else:
                        response = f"ERROR {error}"
                    self.response_q.put_nowait(str(response))

                    # restart console command task
                    self.console_command_task = asyncio.create_task(self.command_q.get(), name='GetConsoleCommand')
                    pending.add(self.console_command_task)

                # Handle and BLE events that have occurred
                if task is self.ble_event_task:
                    evt: ble.BleEventBase = task.result()
                    await self.handle_ble_event(evt)

                    # restart ble event task
                    self.ble_event_task = asyncio.create_task(self.central.get_event(), name='GetBleEvent')
                    pending.add(self.ble_event_task)

    async def handle_console_command(self, command: str) -> ble.BLE_ERROR:
        error = ble.BLE_ERROR.BLE_ERROR_FAILED
        args = command.split()
        if len(args) > 0:
            ble_func = args[0]
            match ble_func:
                case 'GAPSCAN':
                    self.scan_dict: dict[bytes, tuple[str, ble.BleEventGapAdvReport]] = {}
                    self.log("Starting scan...")
                    error = await self.central.scan_start(ble.GAP_SCAN_TYPE.GAP_SCAN_ACTIVE,
                                                          ble.GAP_SCAN_MODE.GAP_SCAN_GEN_DISC_MODE,
                                                          160,
                                                          80,
                                                          False,
                                                          True)

                case "GETALLRESETDATA":
                    if len(args) == 1:  # TODO this case just to avoid having to enter bd addr  # 531B00352348 964700352348
                        periph_bd = ble.BdAddress(ble.BLE_ADDR_TYPE.PUBLIC_ADDRESS, bytes.fromhex("531B00352348"))  # addr is backwards
                        periph_conn_params = ble.GapConnParams(50, 70, 0, 420)
                        error = await self.central.connect(periph_bd, periph_conn_params)
                        # TODO using hardcoded address, Peer Features and Version returned
                        # Passin address, Peer Features and Version not returned

                    if len(args) == 2:  # TODO pass in addr 48:23:35:00:1b:53
                        # bd_info = args[1].strip(',')
                        # bd_type =  if bd_info[1] == 'P' else BLE_ADDR_TYPE.PRIVATE_ADDRESS

                        # TODO need to enter private vs public type
                        self.periph_addr_str = args[1]
                        periph_bd = self.str_to_bd_addr(ble.BLE_ADDR_TYPE.PUBLIC_ADDRESS, self.periph_addr_str)
                        periph_conn_params = ble.GapConnParams(50, 70, 0, 420)
                        error = await self.central.connect(periph_bd, periph_conn_params)

                    # move to state machine function
                    if error == ble.BLE_ERROR.BLE_STATUS_OK:
                        self.fetch_state = FETCH_DATA_STATE.FETCH_DATA_CONNECT

                case _:
                    pass

        return error

    async def handle_ble_event(self, evt: ble.BleEventBase = None):
        if evt:
            match evt.evt_code:
                case ble.BLE_EVT_GAP.BLE_EVT_GAP_ADV_REPORT:
                    self.handle_evt_gap_adv_report(evt)
                case ble.BLE_EVT_GAP.BLE_EVT_GAP_SCAN_COMPLETED:
                    self.handle_evt_scan_completed(evt)
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
                    await self.central.handle_event_default(evt)

            self.process_fetch_state(evt)


    def process_fetch_state(self, evt: ble.BleEventBase):

        match self.fetch_state:

            case FETCH_DATA_STATE.FETCH_DATA_CONNECT:
                if (evt.evt_code == ble.BLE_EVT_GAP.BLE_EVT_GAP_CONNECTION_COMPLETED):
                    self.fetch_state = FETCH_DATA_STATE.FETCH_DATA_WAIT_FOR_NAME
                    self.bg_task = asyncio.create_task(self.central.read(0, DEVICE_NAME_HANDLE, 0))

            case FETCH_DATA_STATE.FETCH_DATA_WAIT_FOR_NAME:
                
                if(evt.evt_code == ble.BLE_EVT_GATTC.BLE_EVT_GATTC_READ_COMPLETED
                    and evt.handle == DEVICE_NAME_HANDLE):
                    evt: ble.BleEventGattcReadCompleted
                    self.connected_name = evt.value.decode("utf-8")
                    self.fetch_state = FETCH_DATA_STATE.FETCH_DATA_BROWSE_DCI
                    self.bg_task = asyncio.create_task(self.central.browse(0, self.uuid_from_str(DEBUG_CRASH_INFO_SVC_UUID_STR)))
                

            case FETCH_DATA_STATE.FETCH_DATA_BROWSE_DCI:
                evt: ble.BleEventGattcBrowseCompleted
                if (evt.evt_code == ble.BLE_EVT_GATTC.BLE_EVT_GATTC_BROWSE_COMPLETED
                        and self.dci_svc.svc_handle != 0):
                    self.fetch_state = FETCH_DATA_STATE.FETCH_DATA_ENABLE_CCC
                    self.bg_task = asyncio.create_task(self.central.write(0, self.dci_svc.tx_ccc.handle, 0, bytes(GATT_EVENT.GATT_EVENT_NOTIFICATION.to_bytes(2, 'little'))))

            case FETCH_DATA_STATE.FETCH_DATA_ENABLE_CCC:
                if (evt.evt_code == ble.BLE_EVT_GATTC.BLE_EVT_GATTC_WRITE_COMPLETED
                        and evt.handle == self.dci_svc.tx_ccc.handle):
                    if evt.status == ble.BLE_ERROR.BLE_STATUS_OK:
                        evt: ble.BleEventGattcWriteCompleted
                        self.fetch_state = FETCH_DATA_STATE.FETCH_DATA_WAIT_FOR_RESPONSE
                        # +1 as handle is for char declaration
                        # TODO rx/tx named from perspective of periph. Change to perspective of central
                        # TODO would be nice to handle a rewsponse FILE_PATH
                        self.bg_task = asyncio.create_task(self.central.write(0, (self.dci_svc.rx.handle + 1), 0, bytes(DCI_SVC_COMMAND.DCI_SERVICE_COMMAND_GET_ALL_DATA.to_bytes(1, 'little'))))
                    else:
                        self.fetch_state = FETCH_DATA_STATE.FETCH_DATA_ERROR
                       
            case FETCH_DATA_STATE.FETCH_DATA_WAIT_FOR_RESPONSE:
                if (evt.evt_code == ble.BLE_EVT_GATTC.BLE_EVT_GATTC_NOTIFICATION
                        and evt.handle == self.dci_svc.tx.handle + 1):

                    # TODO need to know what response waiting for
                    evt: ble.BleEventGattcNotification
                    if self.response.command == 0 and len(evt.value) > 2:
                        self.response.command = evt.value[0]
                        self.response.len = evt.value[1]
                        self.response.data += evt.value[2:]
                    else:
                        self.response.data += evt.value
                        if len(self.response.data) == self.response.len:
                            # TODO assert length is 128
                            self.parse_reset_data(self.response.data)
                            self.log_reset_data()
                            self.fetch_state = FETCH_DATA_STATE.FETCH_DATA_DISCONNECT
                            self.bg_task = asyncio.create_task(self.central.disconect(0, ble.BLE_HCI_ERROR.BLE_HCI_ERROR_REMOTE_USER_TERM_CON))

            case FETCH_DATA_STATE.FETCH_DATA_DISCONNECT:
                if (evt.evt_code == ble.BLE_EVT_GAP.BLE_EVT_GAP_DISCONNECTED):
                    self.log("Disconnected")
                    self.log_file.close()
                    self.fetch_state = FETCH_DATA_STATE.FETCH_DATA_NONE

        if self.fetch_state == FETCH_DATA_STATE.FETCH_DATA_ERROR:
            self.log("Errorrrrr")
            # TODO disconnect if connected

    def log_reset_data(self):
        self.log("*******************Debug Crash Info*******************")
        self.log(f"Device name: {self.connected_name}")
        self.log(f"Device address: {self.bd_addr_to_str(self.connected_addr)}")
        self.log(f"Last reset reason: {self.reset_data.last_reset_reason.name}")
        self.log(f"Number of resets: {self.reset_data.num_resets}")

        for i in range(self.reset_data.num_resets):
            if self.reset_data.fault_data[i].data_valid:
                self.log(f"Fault Data #{i}:")
                self.log(f"\t Epoch: {self.reset_data.fault_data[i].epoch}")
                self.log(f"\t Fault Type: {self.reset_data.fault_data[i].fault_handler.name}")
                self.log(f"\t Last stack frame: ")
                self.log(f"\t\t r0:  0x{self.reset_data.fault_data[i].stack_frame.r0:08x}")
                self.log(f"\t\t r1:  0x{self.reset_data.fault_data[i].stack_frame.r1:08x}")
                self.log(f"\t\t r2:  0x{self.reset_data.fault_data[i].stack_frame.r2:08x}")
                self.log(f"\t\t r3:  0x{self.reset_data.fault_data[i].stack_frame.r3:08x}")
                self.log(f"\t\t r12: 0x{self.reset_data.fault_data[i].stack_frame.r12:08x}")
                self.log(f"\t\t LR:  0x{self.reset_data.fault_data[i].stack_frame.LR:08x}")
                self.log(f"\t\t return_address: 0x{self.reset_data.fault_data[i].stack_frame.return_address:08x}")
                self.log(f"\t\t xPSR: 0x{self.reset_data.fault_data[i].stack_frame.xPSR:08x}")

                self.log(f"\t Call trace: ")
                for j in range(self.reset_data.fault_data[i].num_of_call_vals):
                    self.log(f"\t\t Call address {j}: 0x{self.reset_data.fault_data[i].call_trace[j]:08x}")


    def parse_reset_data(self, data: bytes):

        self.reset_data.last_reset_reason = DCI_REST_REASON(data[0])
        self.reset_data.num_resets = data[1]

        # TODO this is assuming data is the appropriate length

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

    def handle_evt_gap_adv_report(self, evt: ble.BleEventGapAdvReport):

        name = "Unknown"
        adv_packet = False  # used to separate adv packets from scan responses

        # Parse the advertising structures
        ad_structs = self.parse_adv_data(evt)
        for ad_struct in ad_structs:
            # This is an advertising packet (vs scan response)  # TODO How to initiate scan request from Central?
            if ad_struct.type == ble.GAP_DATA_TYPE.GAP_DATA_TYPE_FLAGS:
                adv_packet = True
            # device name found
            if (ad_struct.type == ble.GAP_DATA_TYPE.GAP_DATA_TYPE_LOCAL_NAME
                    or ad_struct.type == ble.GAP_DATA_TYPE.GAP_DATA_TYPE_SHORT_LOCAL_NAME):
                # some devices have a null character for the short name, ignore them
                decoded_name = ad_struct.data.decode("utf-8")
                if decoded_name != '\x00':
                    name = decoded_name

        if adv_report := self.scan_dict.get(evt.address.addr):
            # Item exists in dict, update it
            # if we have a name for this device, do not overwrite it with Unknown
            if adv_report[0] != "Unknown":
                name = adv_report[0]
            if adv_packet:
                self.scan_dict[evt.address.addr] = (name, evt, adv_report[2])
            else:
                self.scan_dict[evt.address.addr] = (name, adv_report[1], evt)
        else:
            for ad_struct in ad_structs:
                # only want devices that advertise Debug Crash Info Service
                if (ad_struct.type == ble.GAP_DATA_TYPE.GAP_DATA_TYPE_UUID128_SVC_DATA 
                        and ad_struct.data[:-1] == self.crash_info_uuid.uuid):
                    # first time seeing this device, add it to dict with an empty scan rsp
                    self.scan_dict[evt.address.addr] = (name, evt, ble.BleEventGapAdvReport())

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

    def handle_evt_scan_completed(self, evt: ble.BleEventGapScanCompleted):
        self.log("Scan complete")
        device_info = ""
        for key in self.scan_dict:
            name, adv_packet, scan_rsp = self.scan_dict[key]
            device_info += f"Device name: {name}, addr: {self.bd_addr_to_str(adv_packet.address)}"

            ad_structs = self.parse_adv_data(adv_packet)
            for ad_struct in ad_structs:
                if ad_struct.type == ble.GAP_DATA_TYPE.GAP_DATA_TYPE_UUID128_SVC_DATA:
                    num_resets = ad_struct.data[-1]
                    device_info += f", number of resets: {num_resets}"

            self.log(device_info)

    def handle_evt_gap_connected(self, evt: ble.BleEventGapConnected):
        self.connected_addr = evt.peer_address
        self.log(f"Connected to: address={self.bd_addr_to_str(evt.peer_address)}")

    def handle_evt_gap_connection_compelted(self, evt: ble.BleEventGapConnectionCompleted):
        self.log(f"Connection completed: status={evt.status.name}")

    def handle_evt_gattc_browse_svc(self, evt: ble.BleEventGattcBrowseSvc):

        if (self.uuid_from_str(DEBUG_CRASH_INFO_SVC_UUID_STR) == evt.uuid):
            self.dci_svc.svc_handle = evt.start_h
            for item in evt.items:
                if item.type == ble.GATTC_ITEM_TYPE.GATTC_ITEM_TYPE_CHARACTERISTIC:
                    if item.uuid == self.uuid_from_str(DEBUG_CRASH_INFO_RX_CHAR_UUID_STR):
                        self.dci_svc.rx = item
                    elif item.uuid == self.uuid_from_str(DEBUG_CRASH_INFO_TX_CHAR_UUID_STR):
                        self.dci_svc.tx = item

                elif item.type == ble.GATTC_ITEM_TYPE.GATTC_ITEM_TYPE_DESCRIPTOR:
                    if item.handle == self.dci_svc.rx.handle + 2:
                        self.dci_svc.rx_user_desc = item
                    elif (item.handle == self.dci_svc.tx.handle + 2
                            or item.handle == self.dci_svc.tx.handle + 3):

                        if self.uuid_to_str(item.uuid) == CCC_UUID_STR:
                            self.dci_svc.tx_ccc = item
                        elif self.uuid_to_str(item.uuid) == CCC_UUID_STR:
                            self.dci_svc.tx_user_desc = item

    def handle_evt_gattc_browse_completed(self, evt: ble.BleEventGattcBrowseCompleted):
        self.log(f"Browsing complete: conn_idx={evt.conn_idx}, evt={evt.status.name}")

    def handle_evt_gattc_write_completed(self, evt: ble.BleEventGattcWriteCompleted):
        self.log(f"Write Complete: conn_idx={evt.conn_idx}, handle={evt.handle}, status={evt.status.name}")

    def handle_evt_gattc_notification(self, evt: ble.BleEventGattcNotification):
        self.log(f"Received Notification: conn_idx={evt.conn_idx}, handle={evt.handle}, value=0x{evt.value.hex()}")

    def handle_evt_gap_disconnected(self, evt: ble.BleEventGapDisconnected):
        # TODO addr to hex str
        self.log(f"Disconnected from to: addr={self.bd_addr_to_str(evt.address)}")

    def handle_evt_gattc_read_completed(self, evt: ble.BleEventGattcReadCompleted):
        self.log(f"Read Complete: conn_idx={evt.conn_idx}, handle={evt.handle}, status={evt.status.name}, value=0x{evt.value.hex()}")

    def str_to_bd_addr(self, type: ble.BLE_ADDR_TYPE, bd_addr_str: str) -> ble.BdAddress:
        bd_addr_str = bd_addr_str.replace(":", "")
        bd_addr_list = [int(bd_addr_str[idx:idx + 2], 16) for idx in range(0, len(bd_addr_str), 2)]
        bd_addr_list.reverse()  # mcu is little endian
        return ble.BdAddress(type, bytes(bd_addr_list))

    def uuid_from_str(self, uuid_str: str) -> ble.AttUuid:
        uuid_str = uuid_str.replace("-", "")
        uuid_list = [int(uuid_str[idx:idx + 2], 16) for idx in range(0, len(uuid_str), 2)]
        uuid_list.reverse()  # mcu is little endian
        return ble.AttUuid(bytes(uuid_list))

    def uuid_to_str(self, uuid: ble.AttUuid) -> str:
        data = uuid.uuid
        return_string = ""
        if uuid.type == ble.ATT_UUID_TYPE.ATT_UUID_128:
            for byte in data:
                byte_string = str(hex(byte))[2:]
                if len(byte_string) == 1:  # Add a leading 0
                    byte_string = "0" + byte_string
                return_string = byte_string + return_string
        else:
            for i in range(1, -1, -1):
                byte_string = str(hex(data[i]))[2:]
                if len(byte_string) == 1:
                    byte_string = "0" + byte_string
                return_string += byte_string

        return return_string


async def main(com_port: str):
    ble_command_q = asyncio.Queue()
    ble_response_q = asyncio.Queue()
    ble_handler = BleController(com_port, ble_command_q, ble_response_q)
    
    # TODO class to handle console interaction

    # return_exceptions: https://stackoverflow.com/questions/65147823/python-asyncio-task-exception-was-never-retrieved
    # suppresses "Task exception was never retrieved" when using KeyboardInterrupt
    await asyncio.gather(console(ble_command_q, ble_response_q), ble_handler.init(), return_exceptions=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='main_central',
                                     description='BLE Central AT Command CLI')

    parser.add_argument("com_port")

    args = parser.parse_args()

    try:
        asyncio.run(main(args.com_port))
    except KeyboardInterrupt:
        pass
    finally:
        print("Exiting")
