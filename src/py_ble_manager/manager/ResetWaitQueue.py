
from ctypes import c_uint16
from typing import Callable
from ..gtl_messages.gtl_message_base import GtlMessageBase


class ResetWaitQueueElement():  # TODO repeated from GTlWaitQueue, make a generic base class
    def __init__(self,
                 conn_idx: c_uint16 = 0,
                 msg_id: c_uint16 = 0,
                 ext_id: c_uint16 = 0,
                 cb: Callable = None,
                 param: object = None) -> None:
        self.conn_idx = conn_idx
        self.msg_id = msg_id
        self.ext_id = ext_id
        self.cb = cb
        self.param = param


class ResetWaitQueue():
    def __init__(self) -> None:
        self._queue = []

    def _task_to_connidx(self, task_id):
        return task_id >> 8

    def add(self, elem: ResetWaitQueueElement):
        self.push(elem)

    def match(self, message: GtlMessageBase) -> bool:
        ret = False
        for elem in self._queue:
            elem: ResetWaitQueueElement
            match = elem.msg_id == message.msg_id

            if match:
                callback = elem.cb
                self.remove(elem)
                callback(message, elem.param)
                ret = True
                break

        return ret

    def push(self, elem: ResetWaitQueueElement) -> None:
        if not isinstance(elem, ResetWaitQueueElement):
            raise TypeError(f"Element must be of type ResetWaitQueueElement, was {type(elem)}")
        self._queue.append(elem)

    def remove(self, elem: ResetWaitQueueElement) -> None:
        self._queue.remove(elem)
