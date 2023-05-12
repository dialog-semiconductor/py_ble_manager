import argparse
import threading
import time
import queue
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.patch_stdout import patch_stdout
import python_gtl_thread as ble


class CLIHandler():
    def __init__(self, ble_command_q: queue.Queue, ble_response_q: queue.Queue):
        self.ble_command_q = ble_command_q
        self.ble_response_q = ble_response_q
        self.exit = threading.Event()

    def start_prompt(self):
        # Accepted commands
        commands = ['GAPSCAN',
                    'GAPCONNECT',
                    'GAPBROWSE',
                    'GAPDISCONNECT',
                    'GATTWRITE',
                    'GATTREAD',
                    'GATTWRITENORESP',
                    'GAPPAIR',
                    'GAPSETCONNPARAM',
                    'PASSKEYENTRY',
                    'YESNOENTRY',
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
                 response_q: queue.Queue):

        self.com_port = com_port
        self.command_q = command_q
        self.response_q = response_q
        self._exit = threading.Event()

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

        self.services = ble.SearchableQueue()

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

    def format_properties(self, prop: int) -> str:
        propr_str = "BRXWNISE"  # each letter corresponds to single property
        for i in range(0, 8):
            if prop & (1 << i) == 0:
                propr_str = propr_str.replace(propr_str[i], '-')
        return propr_str

    def handle_console_command(self, command: str) -> ble.BLE_ERROR:
        error = ble.BLE_ERROR.BLE_ERROR_FAILED
        args = command.split()
        if len(args) > 0:
            ble_func = args[0]
            match ble_func:
                case 'GAPSCAN':
                    error = self.central.scan_start(ble.GAP_SCAN_TYPE.GAP_SCAN_ACTIVE,
                                                    ble.GAP_SCAN_MODE.GAP_SCAN_GEN_DISC_MODE,
                                                    160,
                                                    80,
                                                    False,
                                                    True)

                case "GAPCONNECT":
                    if len(args) == 2:
                        periph_bd = ble.BleUtils.str_to_bd_addr(args[1])
                        periph_conn_params = ble.GapConnParams(50, 70, 0, 420)
                        error = self.central.connect(periph_bd, periph_conn_params)

                case "GAPBROWSE":
                    if len(args) == 2:
                        conn_idx = int(args[1])
                        error = self.central.browse(conn_idx, None)

                case "GAPDISCONNECT":
                    if len(args) >= 2:
                        conn_idx = int(args[1])
                        if len(args) == 3:
                            reason = ble.BLE_HCI_ERROR(int(args[2]))
                            if reason == ble.BLE_HCI_ERROR.BLE_HCI_ERROR_NO_ERROR:
                                reason = ble.BLE_HCI_ERROR.BLE_HCI_ERROR_REMOTE_USER_TERM_CON
                        else:
                            reason = ble.BLE_HCI_ERROR.BLE_HCI_ERROR_REMOTE_USER_TERM_CON
                        error = self.central.disconect(conn_idx, reason)

                case "GATTWRITE":
                    if len(args) == 4:
                        conn_idx = int(args[1])
                        handle = int(args[2])
                        value = bytes.fromhex(args[3])  # TODO requires leading 0 for 0x0-0xF
                        error = self.central.write(conn_idx, handle, 0, value)

                case "GATTWRITENORESP":
                    if len(args) == 5:
                        conn_idx = int(args[1])
                        handle = int(args[2])
                        signed = bool(int(args[3]))
                        value = bytes.fromhex(args[4])  # TODO requires leading 0 for 0x0-0xF
                        error = self.central.write_no_resp(conn_idx, handle, signed, value)

                case "GATTWRITEPREPARE":
                    # TODO not receiving GATTC_CMP_EVT after sending GattcWriteCmd
                    if len(args) == 4:
                        conn_idx = int(args[1])
                        handle = int(args[2])
                        value = bytes.fromhex(args[3])
                        error = self.central.write_prepare(conn_idx, handle, 0, value)

                case "GATTWRITEEXECUTE":
                    if len(args) == 3:
                        conn_idx = int(args[1])
                        execute = bool(int(args[2]))
                        error = self.central.write_execute(conn_idx, execute)

                case "GATTREAD":  # TODO char handle displayed by browse is acutally the declaration. The value is +1
                    if len(args) == 3:
                        conn_idx = int(args[1])
                        handle = int(args[2])
                        error = self.central.read(conn_idx, handle, 0)

                case 'GAPSETCONNPARAM':
                    if len(args) == 6:
                        conn_idx = int(args[1])
                        conn_params = ble.GapConnParams()
                        conn_params.interval_min = int(args[2])
                        conn_params.interval_max = int(args[3])
                        conn_params.slave_latency = int(args[4])
                        conn_params.sup_timeout = int(args[5])
                        error = self.central.conn_param_update(conn_idx, conn_params)

                case 'GAPPAIR':
                    if len(args) == 3:
                        conn_idx = int(args[1])
                        bond = bool(int(args[2]))
                        error = self.central.pair(conn_idx, bond)

                case 'PASSKEYENTRY':
                    if len(args) == 4:
                        conn_idx = int(args[1])
                        accept = bool(int(args[2]))
                        passkey = int(args[3])
                        error = self.central.passkey_reply(conn_idx, accept, passkey)

                case 'YESNOENTRY':
                    if len(args) == 3:
                        conn_idx = int(args[1])
                        accept = bool(int(args[2]))
                        error = self.central.numeric_reply(conn_idx, accept)

                case 'EXIT':
                    # Expected command format: EXIT
                    self.shutdown()
                    error = ble.BLE_ERROR.BLE_STATUS_OK

                case _:
                    pass

        return error

    def handle_ble_event(self, evt: ble.BleEventBase):
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
            case ble.BLE_EVT_GATTC.BLE_EVT_GATTC_DISCOVER_SVC:
                self.handle_evt_gattc_discover_svc(evt)
            case ble.BLE_EVT_GATTC.BLE_EVT_GATTC_DISCOVER_COMPLETED:
                if evt.type == ble.GATTC_DISCOVERY_TYPE.GATTC_DISCOVERY_TYPE_SVC:
                    self.handle_evt_gattc_discover_completed(evt)
            case ble.BLE_EVT_GATTC.BLE_EVT_GATTC_DISCOVER_CHAR:
                self.handle_evt_gattc_discover_char(evt)
            case ble.BLE_EVT_GATTC.BLE_EVT_GATTC_DISCOVER_CHAR:
                self.handle_evt_gattc_discover_char(evt)
            case ble.BLE_EVT_GATTC.BLE_EVT_GATTC_DISCOVER_DESC:
                self.handle_evt_gattc_discover_desc(evt)
            case ble.BLE_EVT_GATTC.BLE_EVT_GATTC_BROWSE_SVC:
                self.handle_evt_gattc_browse_svc(evt)
            case ble.BLE_EVT_GATTC.BLE_EVT_GATTC_BROWSE_COMPLETED:
                self.handle_evt_gattc_browse_completed(evt)
            case ble.BLE_EVT_GATTC.BLE_EVT_GATTC_NOTIFICATION:
                self.handle_evt_gattc_notification(evt)
            case ble.BLE_EVT_GATTC.BLE_EVT_GATTC_READ_COMPLETED:
                self.handle_evt_gattc_read_completed(evt)
            case ble.BLE_EVT_GATTC.BLE_EVT_GATTC_WRITE_COMPLETED:
                self.handle_evt_gattc_write_completed(evt)
            case ble.BLE_EVT_GAP.BLE_EVT_GAP_CONN_PARAM_UPDATED:
                self.handle_evt_gap_conn_param_updated(evt)
            case ble.BLE_EVT_GAP.BLE_EVT_GAP_CONN_PARAM_UPDATE_COMPLETED:
                self.handle_evt_gap_conn_param_update_compelted(evt)
            case ble.BLE_EVT_GAP.BLE_EVT_GAP_PAIR_REQ:
                self.handle_evt_gap_pair_req(evt)
            case ble.BLE_EVT_GAP.BLE_EVT_GAP_PAIR_COMPLETED:
                self.handle_evt_gap_pair_completed(evt)
            case ble.BLE_EVT_GAP.BLE_EVT_GAP_SEC_LEVEL_CHANGED:
                self.handle_evt_gap_sec_level_changed(evt)
            case ble.BLE_EVT_GAP.BLE_EVT_GAP_PEER_FEATURES:
                self.handle_evt_gap_peer_features(evt)
            case ble.BLE_EVT_GAP.BLE_EVT_GAP_PEER_VERSION:
                self.handle_evt_gap_peer_version(evt)
            case ble.BLE_EVT_GAP.BLE_EVT_GAP_PASSKEY_NOTIFY:
                self.handle_evt_gap_passkey_notify(evt)
            case ble.BLE_EVT_GAP.BLE_EVT_GAP_ADDRESS_RESOLVED:
                self.handle_evt_gap_address_resolved(evt)
            case ble.BLE_EVT_GAP.BLE_EVT_GAP_NUMERIC_REQUEST:
                self.handle_evt_gap_numeric_request(evt)
            case _:
                print(f"Ble Task unhandled event: {evt}")
                self.central.handle_event_default(evt)

    def handle_evt_gap_address_resolved(self, evt: ble.BleEventGapAddressResolved):
        print(f"Address resolved: conn_idx={evt.conn_idx}, resolved_address={ble.BleUtils.bd_addr_to_str(evt.resolved_address)}")

    def handle_evt_gap_adv_report(self, evt: ble.BleEventGapAdvReport):
        

        print(f"Advertisment: address={ble.BleUtils.bd_addr_to_str(evt.address)} "
              + f"rssi={evt.rssi}, data={evt.data.hex()}")
        # adv_structs = self.parse_adv_data(evt)
        # print("AD Structs:")
        # for struct in adv_structs:
        #    print(f"\t{struct}")
        # print("")

    def handle_evt_gap_connected(self, evt: ble.BleEventGapConnected):
        print(f"Connected to: addr={ble.BleUtils.bd_addr_to_str(evt.peer_address)}, conn_idx={evt.conn_idx}")

    def handle_evt_gap_connection_compelted(self, evt: ble.BleEventGapConnectionCompleted):
        print(f"Connection completed: status={evt.status.name}")

    def handle_evt_gap_conn_param_updated(self, evt: ble.BleEventGapConnParamUpdated):
        print(f"Connection Parameters updated: conn_idx={evt.conn_idx}, conn_params={evt.conn_params}")

    def handle_evt_gap_conn_param_update_compelted(self, evt: ble.BleEventGapConnParamUpdateCompleted):
        print(f"Connection Parameters update completed: status={evt.status.name}")

    def handle_evt_gap_disconnected(self, evt: ble.BleEventGapDisconnected):
        print(f"Disconnected from: addr={ble.BleUtils.bd_addr_to_str(evt.address)}")

    def handle_evt_gap_numeric_request(central: ble.BleCentral, evt: ble.BleEventGapNumericRequest):
        print(f"Numeric Request: conn_idx={evt.conn_idx}, num_key={evt.num_key}")

    def handle_evt_gap_pair_completed(self, evt: ble.BleEventGapPairCompleted):
        print(f"Pairing compelte: conn_idx={evt.conn_idx}, bond={evt.bond}, mitm={evt.mitm}, status={evt.status.name}")

    def handle_evt_gap_pair_req(self, evt: ble.BleEventGapPairReq):
        print(f"Pair Request: evt={evt}")

    def handle_evt_gap_passkey_notify(self, evt: ble.BleEventGapPasskeyNotify):
        print(f"Passkey notify: conn_idx={evt.conn_idx}, passkey={evt.passkey}")

    def handle_evt_gap_peer_features(self, evt: ble.BleEventGapPeerFeatures):
        print(f"Peer features: conn_idx={evt.conn_idx}, features={evt.le_features.hex()}")

    def handle_evt_gap_peer_version(self, evt: ble.BleEventGapPeerVersion):
        print(f"Peer version: conn_idx={evt.conn_idx}, lmp_version={evt.lmp_version} "
              + f"company_id={evt.company_id}, lmp_subversion={evt.lmp_subversion}")

    def handle_evt_gap_scan_completed(central: ble.BleCentral, evt: ble.BleEventGapScanCompleted):
        # TODO status is always coming back BLE_ERROR_TIMEOUT. Is that correct?
        print(f"Scan completed: status={evt.status.name}")

    def handle_evt_gap_sec_level_changed(self, evt: ble.BleEventGapSecLevelChanged):
        print(f"Security level changed: sec_level={evt.level.name}")

    def handle_evt_gattc_browse_completed(self, evt: ble.BleEventGattcBrowseCompleted):
        print(f"Browsing complete: conn_idx={evt.conn_idx}, evt={evt.status}")

    def handle_evt_gattc_browse_svc(self, evt: ble.BleEventGattcBrowseSvc):

        print(f"Service discovered: uuid={ble.BleUtils.uuid_to_str(evt.uuid)}. handle={evt.start_h}")
        for item in evt.items:
            if item.type == ble.GATTC_ITEM_TYPE.GATTC_ITEM_TYPE_INCLUDE:
                print(f"\tIncluded service discovered: handle={item.handle}, uuid={ble.BleUtils.uuid_to_str(item.uuid)}")
            elif item.type == ble.GATTC_ITEM_TYPE.GATTC_ITEM_TYPE_CHARACTERISTIC:
                print(f"\tCharacteristic discovered: handle={item.handle}, uuid={ble.BleUtils.uuid_to_str(item.uuid)}, prop={item.char_data.properties} "
                      + f"{self.format_properties(item.char_data.properties)}")
            elif item.type == ble.GATTC_ITEM_TYPE.GATTC_ITEM_TYPE_DESCRIPTOR:
                print(f"\t\tDescriptor discovered: handle={item.handle}, uuid={ble.BleUtils.uuid_to_str(item.uuid)}")

    def handle_evt_gattc_discover_char(self, evt: ble.BleEventGattcDiscoverChar):
        print(f"main_central handle_evt_gattc_discover_char unimplemented. evt={evt}")

    def handle_evt_gattc_discover_desc(self, evt: ble.BleEventGattcDiscoverDesc):
        print(f"main_central handle_evt_gattc_discover_desc unimplemented. evt={evt}")

    def handle_evt_gattc_discover_completed(self, evt: ble.BleEventGattcDiscoverCompleted):
        print(f"main_central handle_evt_gattc_discover_completed unimplemented. evt={evt}")

        if evt.type == ble.GATTC_DISCOVERY_TYPE.GATTC_DISCOVERY_TYPE_SVC:
            service: ble.BleServiceBase = self.services.peek_back()
            self.central.discover_characteristics(evt.conn_idx, service.start_h, service.end_h, None)

        # TODO discover included services

        elif evt.type == ble.GATTC_DISCOVERY_TYPE.GATTC_DISCOVERY_TYPE_CHARACTERISTICS:
            # self.central.discover_descriptors(evt.conn_idx. )
            pass

    def handle_evt_gattc_discover_svc(self, evt: ble.BleEventGattcDiscoverSvc):
        service = ble.BleServiceBase()
        service.start_h = evt.start_h
        service.end_h = evt.end_h
        self.services.push(service)

    def handle_evt_gattc_notification(self, evt: ble.BleEventGattcNotification):
        print(f"Received Notification: conn_idx={evt.conn_idx}, handle={evt.handle}, value={evt.value.hex()}")

    def handle_evt_gattc_read_completed(self, evt: ble.BleEventGattcReadCompleted):
        print(f"Read Complete: conn_idx={evt.conn_idx}, handle={evt.handle}, status={evt.status.name}, value={evt.value.hex()}")

    def handle_evt_gattc_write_completed(self, evt: ble.BleEventGattcWriteCompleted):
        print(f"Write Complete: conn_idx={evt.conn_idx}, handle={evt.handle}, status={evt.status.name}")

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

    def shutdown(self):
        self._exit.set()


def main(com_port: str):
    ble_command_q = queue.Queue()
    ble_response_q = queue.Queue()
    ble_handler = BleController(com_port, ble_command_q, ble_response_q)
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
    parser = argparse.ArgumentParser(prog='BLE Central CLI',
                                     description='A command line interface for controlling a BLE Central device')

    parser.add_argument("com_port", type=str, help='COM port for your development kit')

    args = parser.parse_args()

    try:
        main(args.com_port)
    except KeyboardInterrupt:
        print("Keyborard")
