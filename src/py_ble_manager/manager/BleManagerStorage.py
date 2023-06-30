from enum import IntEnum
from typing import Callable

from ..ble_api.BleCommon import BdAddress
from ..ble_api.BleGap import GAP_SEC_LEVEL, BLE_GAP_PHY
from ..gtl_port.gap import gap_sec_key


class INTERNAL_STORAGE_KEY(IntEnum):
    STORAGE_KEY_SVC_CHANGED_CCC = 0xF0000000


class SearchableQueue():  # TODO move to queue files
    def __init__(self) -> None:
        self.queue = []

    def push(self, elem) -> None:
        self.queue.append(elem)

    def remove(self, elem) -> None:
        self.queue.remove(elem)

    def peek(self):
        if len(self.queue) >= 1:
            return self.queue[0]
        else:
            return None

    def peek_back(self):
        if len(self.queue) >= 1:
            return self.queue[-1]
        else:
            return None


class PendingEvent():
    def __init__(self, handle: int = 0) -> None:
        self.handle = handle


class PendingEventQueue(SearchableQueue):
    def __init__(self) -> None:
        self.queue: list[PendingEvent] = []

    def push(self, elem: PendingEvent) -> None:
        if not isinstance(elem, PendingEvent):
            raise TypeError(f"Element must be of type PendingEvent, was {type(elem)}")
        self.queue.append(elem)


class AppValue():
    # TODO add agrs/return type to Callable
    def __init__(self, key: int = 0, persistent: bool = False, value: bytes = None, length: int = 0, free_cb: Callable = None) -> None:
        self.key = key  # TODO storage key type?
        self.persistent = persistent
        self.value = value
        # self.length = length
        # self.free_cb = free_cb  # TODO not sure we need this


class AppValueQueue(SearchableQueue):
    def __init__(self) -> None:
        self.queue: list[AppValue] = []

    def push(self, elem: AppValue) -> None:

        if not isinstance(elem, AppValue):
            raise TypeError(f"Element must be of type AppValue, was {type(elem)}")
        self.queue.append(elem)

    def find_app_value_by_key(self, key: int = None, create: bool = False) -> AppValue:

        found = None
        if key is not None:
            app_value: AppValue
            for app_value in self.queue:
                found = app_value if app_value.key == key else None

            if found is None and create:
                new_app_value = AppValue()
                new_app_value.key = key
                self.push(new_app_value)
                found = new_app_value

        return found


class StoredDevice():
    def __init__(self) -> None:

        self.next = None
        self.addr: BdAddress = BdAddress()
        self.conn_idx: int = 0

        # state flags
        self.connecting: bool = False
        self.connected: bool = False
        self.master: bool = False
        self.paired: bool = False
        self.bonded: bool = False

# if (dg_configBLE_PERIPHERAL == 1)
        self.security_req_pending: bool = False
# endif /* (dg_configBLE_PERIPHERAL == 1) */
        self.encrypted: bool = False
        self.mitm: bool = False
        self.resolving: bool = False
# if (dg_configBLE_SECURE_CONNECTIONS == 1)
        self.secure: bool = False
# endif /* (dg_configBLE_SECURE_CONNECTIONS == 1) */
        self.updating: bool = False

        # parameters
        self.mtu: int = 0
        self.sec_level: GAP_SEC_LEVEL = GAP_SEC_LEVEL.GAP_SEC_LEVEL_1
        self.sec_level_req: GAP_SEC_LEVEL = GAP_SEC_LEVEL.GAP_SEC_LEVEL_1
        self.ce_len_min: int = 0
        self.ce_len_max: int = 0
# if (dg_configBLE_2MBIT_PHY == 1)
        self.tx_phy: BLE_GAP_PHY = BLE_GAP_PHY.BLE_GAP_PHY_1M
        self.rx_phy: BLE_GAP_PHY = BLE_GAP_PHY.BLE_GAP_PHY_1M
# endif /* (dg_configBLE_2MBIT_PHY == 1) */

        # pairing information
        self.ltk: key_ltk = None
        self.remote_ltk: key_ltk = None
        self.irk: key_irk = None
        self.csrk: key_csrk = None
        self.remote_csrk: key_csrk = None

        # custom values set from ..application
        self.app_values: AppValueQueue = AppValueQueue()
        self.pending_events: PendingEventQueue = PendingEventQueue()

        # disconnection status (disconnection event is pending if other than zero)
        self.discon_reason: int = 0

    def app_value_get(self, key: int) -> bytes:
        app_value = self.app_values.find_app_value_by_key(key, False)
        return app_value.value if app_value else None

    def app_value_put(self, key: int, value: bytes, persistent: bool) -> None:

        self.app_value_remove_by_key(key)  # TODO This may be unnecessary as we can reassign dynamically
        app_value = self.app_values.find_app_value_by_key(key, True)
        app_value.persistent = persistent
        app_value.key = key
        app_value.value = value

        # storage_mark_dirty(true);  # TODO want to save these value to disk somewhere?

    def app_value_remove_by_key(self, key: int):
        if key is not None:
            app_value: AppValue
            for app_value in self.app_values.queue:
                if app_value.key == key:
                    self.app_values.remove(app_value)

    def app_value_remove_by_elem(self, elem: AppValue):
        if elem is not None:
            for app_value in self.app_values.queue:
                if elem == app_value:
                    self.app_values.remove(app_value)

    def app_value_remove_not_persistent(self):
        app_value: AppValue
        for app_value in self.app_values.queue:
            if not app_value.persistent:
                self.app_values.remove(app_value)
                # if app_value.free_cb:
                #    app_value.free_cb()  # TODO passing a ptr arg, but not sure what it is yet

    def pending_events_clear_handles(self) -> None:
        self.pending_events = PendingEventQueue()

    def pending_events_has_handle(self, handle: int) -> PendingEvent:
        event: PendingEvent
        for event in self.pending_events.queue:
            if event.handle == handle:
                return event
        return None

    def pending_events_put_handle(self, handle: int) -> None:
        evt = PendingEvent(handle)
        self.pending_events.push(evt)

    def pending_events_clear_handle(self, handle: int) -> None:
        event: PendingEvent
        for event in self.pending_events.queue:
            if event.handle == handle:
                self.pending_events.remove(event)


class StoredDeviceQueue(SearchableQueue):
    def __init__(self) -> None:
        self.queue: list[StoredDevice] = []

    def count_bonded(self):
        count = 0
        for dev in self.queue:
            if dev.bonded:
                count += 1
        return count

    def get_irk_count(self) -> int:
        count = 0
        for dev in self.queue:
            if dev.irk:
                count += 1
        return count

    def find_device_by_connenting(self):
        found = None
        device: StoredDevice
        for device in self.queue:
            found = device if device.connecting else None
            if found:
                break

        return found

    def find_device_by_address(self, addr: BdAddress = None, create: bool = False) -> StoredDevice:

        found = None
        if addr is not None:
            device: StoredDevice
            for device in self.queue:
                found = device if device.addr.addr == addr.addr else None
                if found:
                    break

            if found is None and create:
                new_device = StoredDevice()
                new_device.addr = addr
                new_device.mtu = 23
                self.push(new_device)
                found = new_device

        return found

    def find_device_by_conn_idx(self, conn_idx):
        found = None
        device: StoredDevice
        for device in self.queue:
            found = device if (device.connected and device.conn_idx == conn_idx) else None
            if found:
                break

        return found

    def find_device_by_irk(self, irk: gap_sec_key) -> StoredDevice:
        found = None
        device: StoredDevice
        for device in self.queue:
            if device.irk:
                found = device if (device.irk.key == bytes(irk.key)) else None
                if found:
                    break

        return found

    def for_each(self, callback: Callable, param: object):
        for device in self.queue:
            callback(device, param)

    def move_to_front(self, elem: StoredDevice):
        device: StoredDevice
        for device in self.queue:
            # if device == elem: # TODO method for comparing devices
            if device.conn_idx == elem.conn_idx:
                self.queue.remove(device)
                self.push_front(device)

    def push(self, elem: StoredDevice) -> None:
        if not isinstance(elem, StoredDevice):
            raise TypeError(f"Element must be of type StoredDevice, was {type(elem)}")
        self.queue.append(elem)

    def push_front(self, elem: StoredDevice) -> None:
        self.queue.insert(0, elem)

    def remove_device(self, device: StoredDevice):
        self.queue.remove(device)
        device.app_values = None
        device.pending_events = None

        '''
        device.app_value = SearchableQueue()  # TODO Is this necessary, will no longer be a reference to device
        device.pending_events_clear_handles()

        device.ltk = key_ltk()
        device.remote_ltk = key_ltk()
        device.irk = key_irk()
        device.csrk = key_csrk()
        device.remote_csrk = key_csrk()
        '''

        # TODO storage mark dirty???
        # storage_mark_dirty(true);

    def remove_pairing(self, device: StoredDevice):
        device.bonded = False
        device.paired = False
        device.mitm = False

        # device_free_pairing
        if device.ltk:
            device.ltk = key_ltk()
        if device.remote_ltk:
            device.remote_ltk = key_ltk()
        if device.irk:
            device.irk = key_irk()
        if device.csrk:
            device.csrk = key_csrk()
        if device.remote_csrk:
            device.remote_csrk = key_csrk()

        # TODO STORAGE
        # storage_mark_dirty(true)


class key_csrk():
    def __init__(self, key: bytes = None, sign_cnt: int = 0) -> None:
        self.key = key if key else bytes()
        self.sign_cnt = sign_cnt


class key_irk():
    def __init__(self, key: bytes = None) -> None:
        self.key = key if key else bytes()


class key_ltk():
    def __init__(self, rand: int = 0, ediv: int = 0, key: bytes = None, key_size: int = 0) -> None:
        self.rand = rand
        self.ediv = ediv
        self.key = key if key else bytes()
        self.key_size = key_size
