import asyncio
import serial_asyncio
from gtl_messages import *

class MessageParser():

    def decode_from_bytes(self, byte_string):
        #print(f"MessageParser.decode_from_bytes {byte_string}")
        return GtlMessageFactory().create_message(byte_string)

class MessageRouter():

    def __init__(self) -> None:
        self.observers = []
        self.tx_queue = asyncio.Queue() 
        self.message_parser = MessageParser()

    async def handle_received_message(self, byte_string):
        message = self.message_parser.decode_from_bytes(byte_string) 
        #self.rx_queue.put_nowait(message)
        print(f"MessageParser.handle_received_message(). Received: {message}")
        await self.notify(message)
        

    async def notify(self, message):
        for observer in self.observers:
            response = observer(message=message)
            if response:
                print(f"MessageParser.notify. Adding Response to queue: {response}")
                await self.tx_queue.put(response) 

    def register_observer(self, observer: callable):
        self.observers.append(observer)

    async def send(self):
        while True:
            message = await self.tx_queue.get()
            print(f"MessageParser.send(): {message}")
            self.tx_callback(message.to_bytes())

    def register_tx_callback(self, tx_callback):
        self.tx_callback = tx_callback
