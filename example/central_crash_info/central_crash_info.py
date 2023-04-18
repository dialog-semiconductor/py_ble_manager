import argparse
import asyncio
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.patch_stdout import patch_stdout

# import aiofiles
from enum import IntEnum, auto

# TODO rethink relative import
import sys
from pathlib import Path
HERE = Path(__file__).parent
sys.path.append(str(HERE / '../../'))

import ble_devices as ble

# TODO need to rethink how configuration
ble.dg_configBLE_CENTRAL = 1
ble.dg_configBLE_PERIPHERAL = 0

DEBUG_CRASH_INFO_SVC_UUID_STR = "21ce31fc-da27-11ed-afa1-0242ac120002"
DEBUG_CRASH_INFO_RX_CHAR_UUID_STR = "8a8b791b82f34ecf9ce47d422c371a01"
DEBUG_CRASH_INFO_TX_CHAR_UUID_STR = "17738e0054f94a2ca6ed1ee67e00f323"
CCC_UUID_STR = "2902"
USER_DESC_UUID_STR = "2901"


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
    FETCH_DATA_BROWSE = auto()
    FETCH_DATA_ENABLE_CCC = auto()
    FETCH_DATA_SEND_GET_DATA_COMMAND = auto()
    FETCH_DATA_WAIT_FOR_RESPONSE = auto()
    FETCH_DATA_DISCONNECT = auto()
    FETCH_DATA_ERROR = auto()

#crash_info_uuid: ble.AttUuid = uuid_from_str(DEBUG_CRASH_INFO_SVC_UUID_STR)


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
    def __init__(self):
        self.r0 = 0
        self.r1 = 0
        self.r2 = 0
        self.r3 = 0
        self.r12 = 0
        self.LR = 0
        self.return_address = 0
        self.xPSR = 0



class DCI_REST_REASON(IntEnum):
    NONE = auto()
    POR = auto()
    HW = auto()
    SW = auto()
    WDOG = auto()
    LAST = auto()


class DCI_LAST_FAULT_HANDLER(IntEnum): 
    NONE = auto()
    HARDFAULT = auto()
    NMI = auto()
    PLATFORM_RESET = auto()


class DciFaultInfo():
    def __init__(self):
        self.data_valid: bool = False
        self.epoch: int = 0
        self.fault_handler: DCI_LAST_FAULT_HANDLER = DCI_LAST_FAULT_HANDLER.NONE 
        self.stack_frame = CortexM0StackFrame()
        self.num_of_call_vals: int = 0
        self.call_trace: list[int] = []


class DciData():
    def __init__(self):
        self.last_reset_reason: DCI_REST_REASON = DCI_REST_REASON.NONE
        self.num_resets: int = 0
        self.fault_data: DciFaultInfo = DciFaultInfo()

    
    def __repr__(self):
        return_string = f"last_reset_reason={self.last_reset_reason}"
        
        return return_string
    

async def console(ble_command_q: asyncio.Queue, ble_response_q: asyncio.Queue):
        commands = ['GAPSCAN',
                    'GAPCONNECT',
                    'GAPBROWSE',
                    'GAPDISCONNECT',
                    'GATTWRITE',
                    'GATTREAD',
                    'GETRESETDATA']
        commands.sort()
        word_completer = WordCompleter(commands, ignore_case=True)

        session = PromptSession(completer=word_completer)
        while True:
            with patch_stdout():
                input = await session.prompt_async('>>> ')
                ble_command_q.put_nowait(input)
                response = await ble_response_q.get()
                print(f"<<< {response}")


class BleController():
    def __init__(self, com_port: str, command_q: asyncio.Queue, response_q: asyncio.Queue):
        self.com_port = com_port
        self.command_q = command_q
        self.response_q = response_q
        #                                 name, adv packet, scan rsp packt
        self.scan_dict: dict[bytes, tuple[str, ble.BleEventGapAdvReport, ble.BleEventGapAdvReport]] = {}
        self.crash_info_uuid: ble.AttUuid = uuid_from_str(DEBUG_CRASH_INFO_SVC_UUID_STR)

        self.periph_addr_str = ""
        self.browse_data = []
        self.dci_svc = DebugCrashInfoSvc()
        self.fetch_state = FETCH_DATA_STATE.FETCH_DATA_NONE
        self.response = ResetData()
        self.reset_data = DciData()

        #self.connection_state = CONNECTION_STATE.CONNECTION_STATE_UNCONNECTED  # TODO need to handle multiple connections (use list of connections)
        #self.scanning_state = SCANNING_STATE.SCANNING_STATE_INACTIVE

    def log(self, string: str):
        print(string)
        # TODO create task to write str to file

    async def ble_task(self):
        assert self.com_port
        assert self.command_q
        assert self.response_q

        services = ble.SearchableQueue()

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
                    evt: ble.BleEventBase = task.result()  # TODO how does timeout error affect result
                    await self.handle_ble_event(evt, services)  # TODO services belongs in central??

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

                case "GAPCONNECT":
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
                        periph_bd = str_to_bd_addr(ble.BLE_ADDR_TYPE.PUBLIC_ADDRESS, self.periph_addr_str)
                        periph_conn_params = ble.GapConnParams(50, 70, 0, 420)
                        error = await self.central.connect(periph_bd, periph_conn_params)

                        # move to state machine function
                        if error == ble.BLE_ERROR.BLE_STATUS_OK:
                            self.fetch_state = FETCH_DATA_STATE.FETCH_DATA_CONNECT

                case "GAPBROWSE":
                    if len(args) == 2 or len(args) == 3:
                        if len(args) == 2:
                            conn_idx = int(args[1])
                            uuid = None
                        elif len(args) == 3:
                            conn_idx = int(args[1])
                            print(args[2])
                            uuid = uuid_from_str(args[2])
                        
                        error = await self.central.browse(conn_idx, uuid)

                case "GAPDISCONNECT":
                    if len(args) >= 2:
                        conn_idx = int(args[1])
                        if len(args) == 3:
                            reason = ble.BLE_HCI_ERROR(int(args[2]))
                            if reason == ble.BLE_HCI_ERROR.BLE_HCI_ERROR_NO_ERROR:
                                reason = ble.BLE_HCI_ERROR.BLE_HCI_ERROR_REMOTE_USER_TERM_CON
                        else:
                            reason = ble.BLE_HCI_ERROR.BLE_HCI_ERROR_REMOTE_USER_TERM_CON
                        error = await self.central.disconect(conn_idx, reason)

                case "GATTWRITE":
                    if len(args) == 4:
                        conn_idx = int(args[1])
                        handle = int(args[2])
                        value = bytes.fromhex(args[3])  # TODO requires leading 0 for 0x0-0xF
                        error = await self.central.write(conn_idx, handle, 0, value)
                
                case "GETRESETDATA":
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
                        periph_bd = str_to_bd_addr(ble.BLE_ADDR_TYPE.PUBLIC_ADDRESS, self.periph_addr_str)
                        periph_conn_params = ble.GapConnParams(50, 70, 0, 420)
                        error = await self.central.connect(periph_bd, periph_conn_params)

                case "GATTREAD":  # TODO char handle displayed by browse is acutally the declaration. The value is +1
                    if len(args) == 3:
                        conn_idx = int(args[1])
                        handle = int(args[2])
                        error = await self.central.read(conn_idx, handle, 0)


                case 'GAPPAIR':
                    if len(args) == 3:
                        conn_idx = int(args[1])
                        bond = bool(int(args[2]))
                        error = await self.central.pair(conn_idx, bond)

                case 'PASSKEYENTRY':
                    if len(args) == 4:
                        conn_idx = int(args[1])
                        accept = bool(int(args[2]))
                        passkey = int(args[3])
                        error = await self.central.passkey_reply(conn_idx, accept, passkey)

                case 'YESNOTENTRY':
                    if len(args) == 3:
                        conn_idx = int(args[1])
                        accept = bool(int(args[2]))
                        error = await self.central.numeric_reply(conn_idx, accept)

                case _:
                    pass

        return error

    async def handle_ble_event(self, evt: ble.BleEventBase = None, services: ble.BleServiceBase = None):
        # TODO refactor so central and services not required
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
                    handle_evt_gap_disconnected(evt)
                case ble.BLE_EVT_GATTC.BLE_EVT_GATTC_BROWSE_SVC:
                    self.handle_evt_gattc_browse_svc(evt)
                case ble.BLE_EVT_GATTC.BLE_EVT_GATTC_BROWSE_COMPLETED:
                    self.handle_evt_gattc_browse_completed(evt)
                case ble.BLE_EVT_GATTC.BLE_EVT_GATTC_NOTIFICATION:
                    self.handle_evt_gattc_notification(evt)
                case ble.BLE_EVT_GATTC.BLE_EVT_GATTC_WRITE_COMPLETED:
                    self.handle_evt_gattc_write_completed(evt)
                case ble.BLE_EVT_GATTC.BLE_EVT_GATTC_READ_COMPLETED:
                    handle_evt_gattc_read_completed(evt)

                case _:
                    print(f"Ble Task unhandled event: {evt}")
                    await self.central.handle_event_default(evt)

            self.update_fetch_state(evt)


    def update_fetch_state(self, evt: ble.BleEventBase):
        
        match self.fetch_state:
            
            case FETCH_DATA_STATE.FETCH_DATA_ENABLE_CCC:
                if (evt.evt_code == ble.BLE_EVT_GATTC.BLE_EVT_GATTC_WRITE_COMPLETED
                        and evt.handle == self.dci_svc.tx_ccc.handle):
                    if evt.status == ble.BLE_ERROR.BLE_STATUS_OK:
                        evt: ble.BleEventGattcWriteCompleted
                        self.fetch_state = FETCH_DATA_STATE.FETCH_DATA_WAIT_FOR_RESPONSE
                        # +1 as handle is for char declaration
                        # TODO rx/tx named from perspective of periph. Change to perspective of central
                        # TODO would be nice to handle a rewsponse here
                        
                        self.bg_task = asyncio.create_task(self.central.write(0, (self.dci_svc.rx.handle + 1), 0, bytes(DCI_SVC_COMMAND.DCI_SERVICE_COMMAND_GET_ALL_DATA.to_bytes(1, 'little'))))
                    else:
                        self.fetch_state = FETCH_DATA_STATE.FETCH_DATA_ERROR
                       
            case FETCH_DATA_STATE.FETCH_DATA_WAIT_FOR_RESPONSE:
                if (evt.evt_code == ble.BLE_EVT_GATTC.BLE_EVT_GATTC_NOTIFICATION
                        and evt.handle == self.dci_svc.tx.handle+1):

                    evt: ble.BleEventGattcNotification
                    if self.response.command == 0 and len(evt.value) > 2:
                        self.response.command = evt.value[0]
                        self.response.len = evt.value[1]
                        self.response.data += evt.value[2:]
                    else:
                        self.response.data += evt.value
                        if len(self.response.data) == self.response.len:
                            print("Received all reset data")
                            self.parse_reset_data(self.response.data)
                            self.fetch_state = FETCH_DATA_STATE.FETCH_DATA_DISCONNECT
                        


                    
        if self.fetch_state == FETCH_DATA_STATE.FETCH_DATA_ERROR:
            self.log("Errorrrrr")
            # TODO disconnect is connected
                    
    def parse_reset_data(self, data: bytes):
        length = len(data)
        self.reset_data.last_reset_reason = DCI_REST_REASON(data[0])
        self.reset_data.num_resets = data[1]
        self.reset_data.fault_data.data_valid = bool(data[2])
        self.reset_data.fault_data.epoch = data[3:7]
        self.reset_data.fault_data.fault_handler = data[7:11]
        self.reset_data.fault_data.stack_frame.r0 = data[11:15]

        print(f"reset data: {self.reset_data}")
            

    def handle_evt_gap_adv_report(self, evt: ble.BleEventGapAdvReport):

        # TODO clean this up
        # Parse the advertising structures
        name = "Unknown"
        adv_packet = False  # used to separate adv packets from scan responses
        adv_structs = self.parse_adv_data(evt)
        for adv_struct in adv_structs:
            # This is an advertising packet (vs scan response)  # TODO How to initiate scan request from Central?
            if adv_struct.type == ble.GAP_DATA_TYPE.GAP_DATA_TYPE_FLAGS:
                adv_packet = True
            # device name found
            if (adv_struct.type == ble.GAP_DATA_TYPE.GAP_DATA_TYPE_LOCAL_NAME
                    or adv_struct.type == ble.GAP_DATA_TYPE.GAP_DATA_TYPE_SHORT_LOCAL_NAME):
                # some devices have a null character for the short name, ignore them
                decoded_name = adv_struct.data.decode("utf-8")
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
            for adv_struct in adv_structs:
                # only want devices that advertise Debug Crash Info Service
                if (adv_struct.type == ble.GAP_DATA_TYPE.GAP_DATA_TYPE_UUID128_SVC_DATA 
                        and adv_struct.data[:-1] == self.crash_info_uuid.uuid):
                    # first time seeing this device, add it to dict with an empty scan rsp
                    self.scan_dict[evt.address.addr] = (name, evt, ble.BleEventGapAdvReport())


        '''
        # Set the data in the UI
        self.app_frame.scan_list_ctrl.SetItem(list_index, 0, name)
        self.app_frame.scan_list_ctrl.SetItem(list_index, 1, bd_addr_to_str(evt.address))
        self.app_frame.scan_list_ctrl.SetItem(list_index, 2, str(evt.rssi))
        if adv_packet:
            self.app_frame.scan_list_ctrl.SetItem(list_index, 3, str(adv_structs))
        else:
            self.app_frame.scan_list_ctrl.SetItem(list_index, 4, str(adv_structs))

        # keep track of # of new devices so we can insert them in the list
        if increment_index:
            self.app_frame.scan_list_ctrl_index += 1

        print(f"Advertisment: address={bd_addr_to_str(evt.address)} addr_type={evt.address.addr_type} "
          + f"rssi={evt.rssi}, data={evt.data.hex()}")
        '''

    def parse_adv_data(self, evt: ble.BleEventGapAdvReport) -> list[ble.BleAdvData]:
        data_ptr = 0
        adv_data_structs: ble.BleAdvData = []
        # print(f"Parsing evt.data={list(evt.data)}")
        # print(f"parse_adv_data. address={bd_addr_to_str(evt.address)} evt={evt}")
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
        print(f"Scan complete")
        for key in self.scan_dict:
            name, adv_packet, scan_rsp = self.scan_dict[key]
            print(f"Device name: {name}, addr: {bd_addr_to_str(adv_packet.address)} report: {adv_packet}")
            print("\tAdvertising data:")
            adv_structs = self.parse_adv_data(adv_packet)
            for adv_struct in adv_structs:
                print(f"\tAdv struct: {adv_struct}")
                if adv_struct.type == ble.GAP_DATA_TYPE.GAP_DATA_TYPE_UUID128_SVC_DATA:
                    num_resets = adv_struct.data[-1]
                    print(f"num_resets: {num_resets}")

            print(f"\t Scan Data:")
            adv_structs = self.parse_adv_data(scan_rsp)
            for adv_struct in adv_structs:
                print(f"\Scan struct: {adv_struct}")


       # self.app_frame.scan_spinner.Stop()
       # self.app_frame.scan_spinner.Hide()
       # self.app_frame.scan_btn.SetLabel("Start Scan")
        # TODO status is always coming back BLE_ERROR_TIMEOUT

       # self.app_frame.log(f"Scan completed: status={evt.status.name}")

    def handle_evt_gap_connected(self, evt: ble.BleEventGapConnected):
                #self.app_frame.connect_btn.SetLabel("Disconnect")
        print(f"Connected to: address={bd_addr_to_str(evt.peer_address)}")

    
    def handle_evt_gap_connection_compelted(self, evt: ble.BleEventGapConnectionCompleted):
        print(f"Connection completed: status={evt.status.name}")

        # move this 
        self.fetch_state = FETCH_DATA_STATE.FETCH_DATA_BROWSE
        # start in a background task
        self.bg_task = asyncio.create_task(self.central.browse(0, uuid_from_str(DEBUG_CRASH_INFO_SVC_UUID_STR)))

    def handle_evt_gattc_browse_svc(self, evt: ble.BleEventGattcBrowseSvc):

        self.dci_svc.svc_handle = evt.start_h
        

        for item in evt.items:
            if item.type == ble.GATTC_ITEM_TYPE.GATTC_ITEM_TYPE_CHARACTERISTIC:
                if item.uuid == uuid_from_str(DEBUG_CRASH_INFO_RX_CHAR_UUID_STR):
                    self.dci_svc.rx = item
                elif item.uuid == uuid_from_str(DEBUG_CRASH_INFO_TX_CHAR_UUID_STR):
                    self.dci_svc.tx = item

            elif item.type == ble.GATTC_ITEM_TYPE.GATTC_ITEM_TYPE_DESCRIPTOR:
                if item.handle == self.dci_svc.rx.handle + 2:
                    self.dci_svc.rx_user_desc = item
                elif (item.handle == self.dci_svc.tx.handle + 2
                        or item.handle == self.dci_svc.tx.handle + 3):

                        if uuid_to_str(item.uuid) == CCC_UUID_STR:
                            self.dci_svc.tx_ccc = item
                        elif uuid_to_str(item.uuid) == CCC_UUID_STR:
                            self.dci_svc.tx_user_desc = item
                        #print(f"item handle desc {uuid_to_str(item.uuid)}")
                    
                # TODO format properties function
                print(f"\t\tDescriptor discovered: handle={item.handle}, uuid={uuid_to_str(item.uuid)}")

        print(f"Browse Complete")
        # move this
        self.fetch_state = FETCH_DATA_STATE.FETCH_DATA_ENABLE_CCC
        self.bg_task = asyncio.create_task(self.central.write(0, self.dci_svc.tx_ccc.handle, 0, bytes(GATT_EVENT.GATT_EVENT_NOTIFICATION.to_bytes(2, 'little'))))
        

    def handle_evt_gattc_browse_completed(self, evt: ble.BleEventGattcBrowseCompleted):
        print(f"Browsing complete: conn_idx={evt.conn_idx}, evt={evt.status}")

    def handle_evt_gattc_write_completed(self, evt: ble.BleEventGattcWriteCompleted):
        print(f"Write Complete: conn_idx={evt.conn_idx}, handle={evt.handle}, status={evt.status.name}")


    def handle_evt_gattc_notification(self, evt: ble.BleEventGattcNotification):
        print(f"Received Notification: conn_idx={evt.conn_idx}, handle={evt.handle}, value=0x{evt.value.hex()}")






def handle_evt_gap_disconnected(evt: ble.BleEventGapDisconnected):
    # TODO addr to hex str
    print(f"Disconnected from to: addr={bd_addr_to_str(evt.address)}")




def handle_evt_gattc_read_completed(evt: ble.BleEventGattcReadCompleted):
    print(f"Read Complete: conn_idx={evt.conn_idx}, handle={evt.handle}, status={evt.status.name}, value=0x{evt.value.hex()}")










# TODO move these to a ultility package
def str_to_bd_addr(type: ble.BLE_ADDR_TYPE, bd_addr_str: str) -> ble.BdAddress:
    bd_addr_str = bd_addr_str.replace(":", "")
    bd_addr_list = [int(bd_addr_str[idx:idx + 2], 16) for idx in range(0, len(bd_addr_str), 2)]
    bd_addr_list.reverse()  # mcu is little endian
    return ble.BdAddress(type, bytes(bd_addr_list))


def bd_addr_to_str(bd: ble.BdAddress) -> str:
    return_string = ""
    for byte in bd.addr:
        byte_string = str(hex(byte))[2:]
        if len(byte_string) == 1:  # Add a leading 0
            byte_string = "0" + byte_string
        return_string = byte_string + ":" + return_string
    return return_string[:-1]

def uuid_from_str(uuid_str: str) -> bytes:
    uuid_str = uuid_str.replace("-", "")
    uuid_list = [int(uuid_str[idx:idx + 2], 16) for idx in range(0, len(uuid_str), 2)]
    uuid_list.reverse()  # mcu is little endian
    return ble.AttUuid(bytes(uuid_list))

def uuid_to_str(uuid: ble.AttUuid) -> str:
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


def format_properties(prop: int) -> str:
    propr_str = "BRXWNISE"  # each letter corresponds to single property
    for i in range(0, 8):
        if prop & (1 << i) == 0:
            propr_str = propr_str.replace(propr_str[i], '-')
    return propr_str


async def main(com_port: str):
    ble_command_q = asyncio.Queue()
    ble_response_q = asyncio.Queue()
    ble_handler = BleController(com_port, ble_command_q, ble_response_q)
    # TODO class to handle console interaction
    await asyncio.gather(console(ble_command_q, ble_response_q), ble_handler.ble_task())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='main_central',
                                     description='BLE Central AT Command CLI')

    parser.add_argument("com_port")

    args = parser.parse_args()

    asyncio.run(main(args.com_port))
