import asyncio
from Gap import GapController, GapManager
from MessageRouter import MessageRouter
from SerialStreamManager import SerialStreamManager
from gtl_messages.gtl_port.gapm_task import GAPM_OPERATION
from gtl_messages.gtl_message_gapm import * #TODO remove

class BleBase():
    pass

class BleClient(BleBase):
    pass

class BlePeripheral(BleBase):
    def __init__(self, com_port: str):
        
        self.com_port = com_port 
        tx_queue = asyncio.Queue() 
        rx_queue = asyncio.Queue()

        self.message_router = MessageRouter(tx_queue, rx_queue)
        self.gap_manager = GapManager()
        self.gap_controller = GapController()
        self.message_router.register_observer(self.gap_manager.handle_message) 
        self.message_router.register_observer(self.gap_controller.handle_message)
        self.serial_stream_manager = SerialStreamManager(tx_queue, rx_queue)

    async def run(self):
        # TaskGroup is in 3.11
        #async with asyncio.TaskGroup() as tg:
        #    task1 = tg.create_task(coroutine1,)
            #task2 = tg.create_task(another_coroutine(...))

        serial_rx_task = asyncio.create_task(self.message_router.handle_received_message(), name='StreamRx')
        router_tx_task = asyncio.create_task(self.serial_stream_manager.send(), name='StreamTx')
        router_handle_rx_task = asyncio.create_task(self.serial_stream_manager.receive(), name='RouterRx')

        # TODO this should be a call to the gap manager, but it does not currently know about the message router. 
        # Need message router register observer with GAP classes to direct outgoing traffic
        # This assumes 531 running _ext project already. Should wait for a timeout on return message (GapmCmpEvt operation = 1)
        self.message_router.send_message(GapmResetCmd(gapm_reset_cmd(GAPM_OPERATION.GAPM_RESET)))
        # Wait until the port is open before starting any other coroutines
        await asyncio.wait_for(self.serial_stream_manager.open_port(self.com_port), timeout=None)


        await serial_rx_task
        await router_tx_task
        await router_handle_rx_task
