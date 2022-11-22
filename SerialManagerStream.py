import asyncio
import serial_asyncio
from gtl_messages import *

# TODO GAPM message handling should be in a GapManager class


class GapManager():

    def default_handler(self, message):
        print("default handler")
        return None

    def handle_gapm_device_ready_ind(self, message):      
        #print("Received GapmDeviceReadyInd()", message.msg_id)
        return GapmResetCmd(gapm_reset_cmd(GAPM_OPERATION.GAPM_RESET))

    def handle_gapm_cmp_evt(self,message):
        #print("Received GapmCmpEvt()", message.msg_id)
        return self.handle_gapm_reset_completion(message)

    def handle_gapm_reset_completion(self, message: GapmCmpEvt):
        #print("handle_gapm_reset_completion", message.msg_id)
        
        response = GtlMessageBase()
        if(message.parameters.operation == GAPM_OPERATION.GAPM_RESET):
            response = self.default_gapm_reset_callback()
        elif(message.parameters.operation == GAPM_OPERATION.GAPM_SET_DEV_CONFIG):
            pass
            # Because this is not handled we add a GtlBaseMessage to the queue
            #print("handle_gapm_reset_completion GAPM_SET_DEV_CONFIG")
        
        return response

    def default_gapm_reset_callback(self):

        #print("default_gapm_reset_callback")
        response = GapmSetDevConfigCmd()
        response.parameters.operation = GAPM_OPERATION.GAPM_SET_DEV_CONFIG
        response.parameters.role = GAP_ROLE.GAP_ROLE_PERIPHERAL
        response.parameters.att_cfg = 0x20 # TODO setup GAPM_MASK_ATT_SVC_CNG_EN
        response.parameters.max_mtu = 512 
        response.parameters.max_txoctets = 251
        response.parameters.max_txtime = 2120
        return response

    func_table = {
        GAPM_MSG_ID.GAPM_CMP_EVT: handle_gapm_cmp_evt,
        GAPM_MSG_ID.GAPM_DEVICE_READY_IND: handle_gapm_device_ready_ind,
        GAPM_MSG_ID.GAPM_CANCEL_CMD: default_handler,
    }

    def handle_gap_message(self, message: GtlMessageBase):
        #print("GapManager.handle_gap_message Calling function table")
        #TODO be careful, not clear if you are calling instance func or class method
        return self.func_table[message.msg_id](self, message)

class GapController():
        pass

class MessageParser():

    def __init__(self) -> None:
        self.observers = []
        self.tx_queue = asyncio.Queue() 

    def run(self, message: GtlMessageBase):
        pass
    #Put on queue? Traverse list of observers? Call specific callback? 

    def decode_from_bytes(self, byte_string):
        #print(f"MessageParser.decode_from_bytes {byte_string}")
        return GtlMessageFactory().create_message(byte_string)

    async def handle_received_message(self, byte_string):
        message = self.decode_from_bytes(byte_string) 
        #self.rx_queue.put_nowait(message)
        print(f"MessageParser.handle_received_message(). Received: {message}")
        for observer in self.observers:
            response = observer(message=message)
            if response:
                print(f"MessageParser.handle_received_message. Adding Response to queue: {response}")
                await self.tx_queue.put(response) 


    #async def handle_received_message(self, byte_string):
    #    message = self.decode_from_bytes(byte_string) 
    #    #self.rx_queue.put_nowait(message)
    #    for observer in self.observers:
    #        observer(await self.rx_queue.get())


    def register_observer(self, observer: callable):
        self.observers.append(observer)

    #async def notify_rx(self):
    #    for observer in self.observers:
    #        observer(await self.rx_queue.get())

    async def send(self):
        while True:
            message = await self.tx_queue.get()
            print(f"MessageParser.send(): {message}")
            self.tx_callback(message.to_bytes())

    def register_tx_callback(self, tx_callback):
        self.tx_callback = tx_callback


class SerialManagerStream(asyncio.Protocol):

    async def open_port(self):
        self.reader, self.writer = await serial_asyncio.open_serial_connection(url='COM13', baudrate=115200)
        #print("SerialManagerStream.open_port Port has been opened")
    
    def register_rx_callback(self, rx_callback):
        self.rx_callback = rx_callback

    async def notify(self, byte_string):
        await self.rx_callback(byte_string)

    async def receive(self):
        while True:
            buffer = bytes()
            #print(f"buffer: {buffer}")
            #print("Waiting for GTL_INITIATOR")
            buffer = await self.reader.readexactly(1)
            if(buffer[0] == GTL_INITIATOR):
                #print("Waiting for message header")
                buffer += await self.reader.readexactly(8)
                par_len = int.from_bytes(buffer[7:9], "little",signed=False)
                if(par_len != 0):
                    #print("Waiting for message params")
                    buffer += await self.reader.readexactly(par_len)
                
                #print(f"SerialManagerStream.receive Sending: {buffer}")

                # Handle it
                # TODO awaiting here makes is so buffer is not reset and enter endless loop
                await self.notify(buffer)

                #print('Tasks count: ', len(asyncio.all_tasks()))
                #print('Tasks: ', asyncio.all_tasks())
            else:
                print("Received some garbage")

    def send(self, byte_string):
        #print(f"SerialManagerStream.send: {byte_string}")
        self.writer.write(byte_string)


async def main(coro1, coro2, coro3):
    # TaskGroup is in 3.11
    #async with asyncio.TaskGroup() as tg:
    #    task1 = tg.create_task(coro1,)
        #task2 = tg.create_task(another_coro(...))

    #task1 = asyncio.create_task(coro1, name='OpenPort')
    task2 = asyncio.create_task(coro2, name='StreamRx')
    task3 = asyncio.create_task(coro3, name='ParserTx')

    #print("Waiting to open port")
    await asyncio.wait_for(coro1, timeout=None)

    #print("Port should be open????????")
    await task2
    await task3

    print("Waiting for Reset")

    # fails to catch serial port data 
    #await forever(task1,task2)

async def forever(task1, task2):
    while True:
        await task1
        await task2

message_router = MessageParser()
gap_manager = GapManager()
gap_controller = GapController()
message_router.register_observer(gap_manager.handle_gap_message)
serial_stream_manager = SerialManagerStream()
serial_stream_manager.register_rx_callback(message_router.handle_received_message)
message_router.register_tx_callback(serial_stream_manager.send)

loop = asyncio.get_event_loop()
loop.run_until_complete(main(serial_stream_manager.open_port(), serial_stream_manager.receive(), message_router.send()))
loop.close()