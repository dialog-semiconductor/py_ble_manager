from ..gtl_messages.gtl_message_base import GtlMessageBase
from .WaitQueue import WaitQueueElement, WaitQueue


class ResetWaitQueue(WaitQueue):
    def __init__(self) -> None:
        super().__init__()

    def match(self, message: GtlMessageBase) -> bool:
        ret = False
        for elem in self._queue:
            elem: WaitQueueElement
            match = elem.msg_id == message.msg_id

            if match:
                callback = elem.cb
                self.remove(elem)
                callback(message, elem.param)
                ret = True
                break

        return ret
