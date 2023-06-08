import threading
from ..ble_api.BleGap import BLE_CONN_IDX_INVALID
from ..gtl_messages.gtl_message_base import GtlMessageBase
from ..gtl_port.gapc_task import GAPC_MSG_ID, GAPC_OPERATION
from ..gtl_port.gapm_task import GAPM_MSG_ID
from .WaitQueue import WaitQueueElement, WaitQueue


class GtlWaitQueue(WaitQueue):
    def __init__(self) -> None:
        self._wait_queue_lock: threading.Lock = threading.Lock()
        super().__init__()

    def _wait_queue_lock_acquire(self,):
        self._wait_queue_lock.acquire()

    def _wait_queue_lock_release(self,):
        self._wait_queue_lock.release()

    def add(self, elem: WaitQueueElement):
        self._wait_queue_lock_acquire()
        self.push(elem)
        self._wait_queue_lock_release()

    def flush(self, conn_idx):
        elem: WaitQueueElement
        self._wait_queue_lock_acquire()
        for elem in self._queue:
            if elem.conn_idx == conn_idx:
                is_match = False
                match elem.msg_id:
                    case GAPC_MSG_ID.GAPC_CMP_EVT:
                        match elem.ext_id:
                            case GAPC_OPERATION.GAPC_GET_CON_RSSI:
                                is_match = True
                            case GAPC_OPERATION.GAPC_ENCRYPT:
                                is_match = True
                        # if (dg_configBLE_2MBIT_PHY == 1)
                        # case GAPC_LE_SET_PHY:
                        #   is_match  = True
                        # endif /* (dg_configBLE_2MBIT_PHY == 1) */

                        # if (RWBLE_SW_VERSION_MAJOR >= 9)
                        # ifdef F_PCLE
                        #    case GAPC_MSG_ID.GAPC_LE_RD_REM_TX_PWR_LVL:
                        #        is_match = True
                        #    case GAPC_MSG_ID.GAPC_LE_SET_PATH_LOSS_REPORT_PARAMS:
                        #        is_match = True
                        #    case GAPC_MSG_ID.GAPC_LE_SET_PATH_LOSS_REPORT_EN:
                        #        is_match = True
                        #    case GAPC_MSG_ID.GAPC_LE_SET_TX_PWR_REPORT_EN:
                        #        is_match = True
                        # endif // F_PCLE
                        # endif // (RWBLE_SW_VERSION_MAJOR >= 9)
                            case _:
                                is_match = False
                    case _:
                        is_match = False

                if is_match:
                    self.remove(elem)
                    if elem.cb:
                        # Fire associated callback with None gtl message
                        print("Firing callback")
                        elem.cb(None, elem.param)
        self._wait_queue_lock_release()

    def flush_all(self):
        self._wait_queue_lock_acquire()
        elem: WaitQueueElement
        for elem in self._queue:
            self._queue.remove(elem)
        self._wait_queue_lock_release()

    def match(self, message: GtlMessageBase) -> bool:
        ret = False
        self._wait_queue_lock_acquire()
        for item in self._queue:
            item: WaitQueueElement
            if item.conn_idx == BLE_CONN_IDX_INVALID:
                match = item.msg_id == message.msg_id
            else:
                match = (item.conn_idx == self._task_to_connidx(message.src_id)
                         and item.msg_id == message.msg_id)

            if not match:
                continue

            match item.msg_id:
                case GAPM_MSG_ID.GAPM_CMP_EVT:
                    match = item.ext_id == message.parameters.operation
                case GAPC_MSG_ID.GAPC_CMP_EVT:
                    match = item.ext_id == message.parameters.operation
                # Add more events if other commands need more fine-grained matching
                case _:
                    pass

            if match:
                callback = item.cb
                self.remove(item)
                callback(message, item.param)
                ret = True
                break

        self._wait_queue_lock_release()
        return ret
