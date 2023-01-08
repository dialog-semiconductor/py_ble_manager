from ctypes import c_uint16

from gtl_messages.gtl_message_base import GtlMessageBase
from gtl_port.gapc_task import GAPC_MSG_ID, GAPC_OPERATION
from gtl_port.gapm_task import GAPM_MSG_ID


class GtlWaitQueueElement():
    def __init__(self,
                 conn_idx: c_uint16 = 0,  # TODO do these really need to be c_uint16 instead of uint?
                 msg_id: c_uint16 = 0,
                 ext_id: c_uint16 = 0,
                 cb: callable = None,
                 param: object = None) -> None:
        self.conn_idx = conn_idx
        self.msg_id = msg_id
        self.ext_id = ext_id
        self.cb = cb
        self.param = param


class GtlWaitQueue():
    def __init__(self) -> None:
        self.queue = []

    def _task_to_connidx(self, task_id):  # TODO does not seem like an appropriate method for the wait queue to have
        return task_id >> 8

    def add(self, conn_idx, msg_id, ext_id, cb, param):
        item = GtlWaitQueueElement(conn_idx=conn_idx, msg_id=msg_id, ext_id=ext_id, cb=cb, param=param)
        self.push(item)

    def flush(self, conn_idx):
        elem: GtlWaitQueueElement
        for elem in self.queue:
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
                        # Fire associated callback with None gtl message # TODO seems like it could cause issue, verify for two cases where match is true
                        elem.cb(None, elem.param)

    def match(self, message: GtlMessageBase) -> bool:
        ret = False

        for item in self.queue:
            item: GtlWaitQueueElement
            if item.conn_idx == 0XFFFF:  # TODO no magic number
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
                callback(message, item.param)  # TODO use **kwargs for functions that dont use params
                ret = True
                break

        return ret

    def push(self, elem: GtlWaitQueueElement) -> None:
        if not isinstance(elem, GtlWaitQueueElement):
            raise TypeError(f"Element must be of type GtlWaitQueueElement, was {type(elem)}")
        self.queue.append(elem)

    def remove(self, elem: GtlWaitQueueElement) -> None:
        self.queue.remove(elem)
