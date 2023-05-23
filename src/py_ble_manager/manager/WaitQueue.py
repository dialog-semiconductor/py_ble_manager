from ctypes import c_uint16
from typing import Callable


class WaitQueueElement():
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


class WaitQueue():
    def __init__(self) -> None:
        self._queue = []

    def _task_to_connidx(self, task_id):
        return task_id >> 8

    def add(self, elem: WaitQueueElement):
        self.push(elem)

    def push(self, elem: WaitQueueElement) -> None:
        if not isinstance(elem, WaitQueueElement):
            raise TypeError(f"Element must be of type WaitQueueElement, was {type(elem)}")
        self._queue.append(elem)

    def remove(self, elem: WaitQueueElement) -> None:
        self._queue.remove(elem)
