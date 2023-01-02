from ctypes import c_uint16
from gtl_messages.gtl_message_base import GtlMessageBase
from gtl_messages.gtl_message_gapm import GAPM_MSG_ID
from gtl_messages.gtl_message_gapc import GAPC_MSG_ID


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
        self.len = 0

    def _task_to_connidx(self, task_id):  # TODO does not seem like an appropriate method for the wait queue to have
        return task_id >> 8

    # TODO does this method belong in BleManagerBase ??
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
        self.len += 1

    def remove(self, elem) -> None:
        self.len -= 1
        self.queue.remove(elem)
