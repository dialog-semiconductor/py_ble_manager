import argparse
import threading
import queue
import time
import python_gtl_thread as ble

from CustomBleService import CustomBleService, CustomBleServiceCallbacks


def app_char1_read_callback(svc: CustomBleService, conn_idx: int):
    print("app_char1_read_callback")
    data = 0x05
    svc.send_char1_read_cfm(conn_idx,
                            ble.ATT_ERROR.ATT_ERROR_OK,
                            data.to_bytes(1, byteorder='little'))


def app_char1_write_callback(svc: CustomBleService, conn_idx: int, value: int):
    print(f"app_char1_write_callback. conn_idx={conn_idx}, value={value}")
    svc.send_char1_write_cfm(conn_idx, ble.ATT_ERROR.ATT_ERROR_OK)


def app_char2_write_callback(svc: CustomBleService, conn_idx: int, value: int):
    print(f"app_char2_write_callback. conn_idx={conn_idx}, value={value}")
    svc.send_char2_write_cfm(conn_idx, ble.ATT_ERROR.ATT_ERROR_OK)
    svc.set_char2_value(value.to_bytes(2, byteorder='little'))


def app_char3_ccc_changed_callback(svc: CustomBleService, conn_idx: int, value: int):
    print(f"app_char3_ccc_changed_callback. conn_idx={conn_idx}, value={value}")


class BleController():
    def __init__(self,
                 com_port: str,
                 command_q: queue.Queue,
                 response_q: queue.Queue):

        self.com_port = com_port
        self.command_q = command_q
        self.response_q = response_q
        self._exit = threading.Event()

    def bd_addr_to_str(self, bd: ble.BdAddress) -> str:
        return_string = ""
        for byte in bd.addr:
            byte_string = str(hex(byte))[2:]
            if len(byte_string) == 1:  # Add a leading 0
                byte_string = "0" + byte_string
            return_string = byte_string + ":" + return_string
        return return_string[:-1]

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
            self.handle_ble_event(evt)

    def ble_task(self):

        periph = ble.BlePeripheral(self.com_port, gtl_debug=True)
        periph.init()
        periph.start()

        periph.set_io_cap(ble.GAP_IO_CAPABILITIES.GAP_IO_CAP_DISP_YES_NO)

        my_service_callbacks = CustomBleServiceCallbacks(app_char1_read_callback,
                                                         app_char1_write_callback,
                                                         app_char2_write_callback)
        my_service = CustomBleService(my_service_callbacks)
        my_service.init()

        periph.register_service(my_service)
        my_service.set_char2_value((0x8692).to_bytes(2, 'little'))
        my_service.set_char3_user_desc_value(b"Hello")

        periph.set_advertising_interval(20, 30)
        periph.start_advertising()

        while True:

            evt = periph.get_event()

            if evt is not None:
                handled = periph.service_handle_event(evt)
                if not handled:
                    match evt.evt_code:
                        case ble.BLE_EVT_GAP.BLE_EVT_GAP_DISCONNECTED:
                            periph.start_advertising()
                        case ble.BLE_EVT_GAP.BLE_EVT_GAP_PAIR_REQ:
                            evt: ble.BleEventGapPairReq
                            print(f"BleEventGapPairReq. evt={evt}")
                            periph.pair_reply(evt.conn_idx, True, evt.bond)
                        case ble.BLE_EVT_GAP.BLE_EVT_GAP_NUMERIC_REQUEST:
                            print(f"BLE_EVT_GAP_NUMERIC_REQUEST. evt={evt}")
                            periph.numeric_reply(evt.conn_idx, True)
                        case ble.BLE_EVT_GAP.BLE_EVT_GAP_PASSKEY_REQUEST:
                            print(f"Passkey {evt}")
                        case ble.BLE_EVT_GAP.BLE_EVT_GAP_PASSKEY_NOTIFY:
                            print(f"Passkey2 {evt}")
                        case _:
                            periph.handle_event_default(evt)

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
                        self.periph_addr_str, addr_type_str = args[1].split(',')
                        addr_type = ble.BLE_ADDR_TYPE.PUBLIC_ADDRESS if addr_type_str == 'P' else ble.BLE_ADDR_TYPE.PRIVATE_ADDRESS
                        periph_bd = self.str_to_bd_addr(addr_type, self.periph_addr_str)
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

                case 'YESNOTENTRY':
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
        print(f"Address resolved: conn_idx={evt.conn_idx}, evt={evt}")

    def handle_evt_gap_adv_report(self, evt: ble.BleEventGapAdvReport):
        addr_type_str = "P" if evt.address.addr_type == ble.BLE_ADDR_TYPE.PUBLIC_ADDRESS else "R"

        print(f"Advertisment: address={self.bd_addr_to_str(evt.address)},{addr_type_str} "
              + f"rssi={evt.rssi}, data={evt.data.hex()}")

        # adv_structs = self.parse_adv_data(evt)
        # print("AD Structs:")
        # for struct in adv_structs:
        #    print(f"\t{struct}")
        # print("")

    def handle_evt_gap_connected(self, evt: ble.BleEventGapConnected):
        print(f"Connected to: addr={self.bd_addr_to_str(evt.peer_address)}, conn_idx={evt.conn_idx}")

    def handle_evt_gap_connection_compelted(self, evt: ble.BleEventGapConnectionCompleted):
        print(f"Connection completed: status={evt.status.name}")

    def handle_evt_gap_conn_param_updated(self, evt: ble.BleEventGapConnParamUpdated):
        print(f"Connection Parameters updated: evt={evt}")

    def handle_evt_gap_conn_param_update_compelted(self, evt: ble.BleEventGapConnParamUpdateCompleted):
        print(f"Connection Parameters update completed: evt={evt}")

    def handle_evt_gap_disconnected(self, evt: ble.BleEventGapDisconnected):
        print(f"Disconnected from to: addr={self.bd_addr_to_str(evt.address)}")

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

        print(f"Service discovered: uuid={self.uuid_to_str(evt.uuid)}. handle={evt.start_h}")
        for item in evt.items:
            if item.type == ble.GATTC_ITEM_TYPE.GATTC_ITEM_TYPE_INCLUDE:
                print(f"\tIncluded service discovered: handle={item.handle}, uuid={self.uuid_to_str(item.uuid)}")
            elif item.type == ble.GATTC_ITEM_TYPE.GATTC_ITEM_TYPE_CHARACTERISTIC:
                # TODO format properties function
                print(f"\tCharacteristic discovered: handle={item.handle}, uuid={self.uuid_to_str(item.uuid)}, prop={item.char_data.properties} "
                      + f"{self.format_properties(item.char_data.properties)}")
            elif item.type == ble.GATTC_ITEM_TYPE.GATTC_ITEM_TYPE_DESCRIPTOR:
                # TODO format properties function
                print(f"\t\tDescriptor discovered: handle={item.handle}, uuid={self.uuid_to_str(item.uuid)}")

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

    def str_to_bd_addr(self, type: ble.BLE_ADDR_TYPE, bd_addr_str: str) -> ble.BdAddress:
        bd_addr_str = bd_addr_str.replace(":", "")
        bd_addr_list = [int(bd_addr_str[idx:idx + 2], 16) for idx in range(0, len(bd_addr_str), 2)]
        bd_addr_list.reverse()  # mcu is little endian
        return ble.BdAddress(type, bytes(bd_addr_list))

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

'''
def user_main(sample_q: queue.Queue):
    elapsed = 0
    delay = 1
    while True:
        time.sleep(delay)
        elapsed += delay
        sample_q.put_nowait(elapsed)
'''


def main(com_port: str):
    ble_command_q = queue.Queue()
    ble_response_q = queue.Queue()
    ble_handler = BleController(com_port, ble_command_q, ble_response_q)
    ble_task = threading.Thread(target=ble_handler.ble_task)
    ble_task.daemon = True
    ble_task.start()

    while True:
        if ble_task.is_alive():
            time.sleep(1)
        else:
            if ble_task.is_alive():
                ble_handler.shutdown()
            return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='main_central',
                                     description='BLE Central AT Command CLI')

    parser.add_argument("com_port")

    args = parser.parse_args()

    try:
        main(args.com_port)
    except KeyboardInterrupt:
        print("Keyborard")
