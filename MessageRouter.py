import asyncio
import serial_asyncio
from gtl_messages import *

class MessageParser():

    def decode_from_bytes(self, byte_string):
        #print(f"MessageParser.decode_from_bytes {byte_string}")
        return GtlMessageFactory().create_message(byte_string)

class MessageRouter():

    def __init__(self, tx_queue: asyncio.Queue(), rx_queue: asyncio.Queue()) -> None:
        self.observers = []
        # TODO error check queues are asyncio.Queue
        #if(not tx_queue or not rx_queue):
            # throw error
        self.tx_queue = tx_queue 
        self.rx_queue = rx_queue
        self.message_parser = MessageParser()
    
    async def handle_received_message(self):
        while True: # TODO instead of infinite loop, could we instead schedule this coroutine when an item is put on the queue? 
            byte_string = await self.rx_queue.get()
            message = self.message_parser.decode_from_bytes(byte_string) 
            #self.rx_queue.put_nowait(message)
            print(f"<-- {message}")
            await self.notify(message)
        
    async def notify(self, message):
        for observer in self.observers:
            response = observer(message=message)
            if response:
                #print(f"MessageParser.notify. Adding Response to queue: {response}")
                await self.tx_queue.put(response) 

    def register_observer(self, observer: callable):
        self.observers.append(observer)
