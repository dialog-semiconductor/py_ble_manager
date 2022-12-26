import asyncio
from gtl_messages.gtl_message_base import GtlMessageBase
from gtl_messages.gtl_message_factory import GtlMessageFactory


class MessageParser():

    def decode_from_bytes(self, byte_string):
        return GtlMessageFactory().create_message(byte_string)


class MessageRouter():

    def __init__(self, tx_queue: asyncio.Queue(), rx_queue: asyncio.Queue()) -> None:
        self.observers = []
        # TODO error check queues are asyncio.Queue
        # if(not tx_queue or not rx_queue):
            # throw error
        self.tx_queue = tx_queue
        self.rx_queue = rx_queue
        self.message_parser = MessageParser()

    async def handle_received_message(self):
        while True:  # TODO instead of infinite loop, could we instead schedule this coroutine when an item is put on the queue?
            byte_string = await self.rx_queue.get()
            message = self.message_parser.decode_from_bytes(byte_string)
            print(f"<-- Rx: {message}\n")
            self.notify(message)

    def notify(self, message):
        for observer in self.observers:
            response = observer(message)
            if response:
                self.tx_queue.put_nowait(response)
                break  # message handled, no need to send to other observers

    def register_observer(self, observer: callable):
        self.observers.append(observer)

    def send_message(self, message: GtlMessageBase):
        self.tx_queue.put_nowait(message)
