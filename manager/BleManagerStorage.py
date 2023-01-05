import asyncio

from ble_api.BleCommon import bd_address
from ble_api.BleGap import GAP_SEC_LEVEL, BLE_GAP_PHY


class device():
    def __init__(self) -> None:

        self.next = None
        self.addr: bd_address = bd_address()
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
        self.ltk: key_ltk = key_ltk()
        self.remote_ltk: key_ltk = key_ltk()
        self.irk: key_irk = key_irk()
        self.csrk: key_csrk = key_csrk()
        self.remote_csrk: key_csrk = key_csrk()

        # custom values set from application
        self.app_value: asyncio.Queue = asyncio.Queue()
        self.pending_events: asyncio.Queue = asyncio.Queue()

        # disconnection status (disconnection event is pending if other than zero)
        self.discon_reason: int = 0


class key_csrk():
    def __init__(self, key: bytes = None, sign_cnt: int = 0) -> None:
        self.key = key if key else bytes()  # TODO raise error on list size?
        self.sign_cnt = sign_cnt


class key_irk():
    def __init__(self, key: bytes = None) -> None:
        self.key = key if key else bytes  # TODO raise error on list size?


class key_ltk():
    def __init__(self, rand: int = 0, ediv: int = 0, key: bytes = None, key_size: int = 0) -> None:
        self.rand = rand
        self.ediv = ediv
        self.key = key if key else bytes  # TODO raise error on list size?
        self.key_size = key_size
