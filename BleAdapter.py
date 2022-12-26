import asyncio
from Gap import GapController, GapManager
from MessageRouter import MessageRouter
from SerialStreamManager import SerialStreamManager
from MessageRouter import MessageParser
from gtl_messages.gtl_port.gapm_task import GAPM_MSG_ID


class BleAdapter():

    def __init__(self, com_port: str, command_q: asyncio.Queue(), event_q: asyncio.Queue(), event_signal: asyncio.Event()) -> None:

        self.event_observers = []
        self.message_parser = MessageParser()
        self.command_q = command_q
        self.event_q = event_q if event_q else asyncio.Queue()
        self.event_signal = event_signal if event_signal else asyncio.Event()
        self.ble_stack_initialized = False

        self.com_port = com_port
        self.serial_tx_queue = asyncio.Queue()
        self.serial_rx_queue = asyncio.Queue()

        self.message_router = MessageRouter(self.serial_tx_queue, self.serial_rx_queue)
        self.serial_stream_manager = SerialStreamManager(self.serial_tx_queue, self.serial_rx_queue)
        self.gap_manager = GapManager()
        self.gap_controller = GapController()
        self.message_router.register_observer(self.gap_manager.handle_message)
        self.message_router.register_observer(self.gap_controller.handle_message)

    def init(self):
        # TaskGroup is in 3.11
        # async with asyncio.TaskGroup() as tg:
        #    task1 = tg.create_task(coroutine1,)
        #    task2 = tg.create_task(another_coroutine(...))

        # TODO move these below open port???

        # TODO this should be a call to the gap manager, but it does not currently know about the message router.
        # Need message router register observer with GAP classes to direct outgoing traffic
        # This assumes 531 running _ext project already. Should wait for a timeout on return message (GapmCmpEvt operation = 1)
        # self.message_router.send_message(GapmResetCmd(gapm_reset_cmd(GAPM_OPERATION.GAPM_RESET)))
        # Wait until the port is open before starting any other coroutines

        # TODO keeping handles so these can be cancelled somehow
        self.handle_rx_task = asyncio.create_task(self.handle_received_serial_message(), name='BleAdapterRx')
        self.serial_tx_task = asyncio.create_task(self.serial_stream_manager.send(), name='SerialStreamTx')
        self.serial_rx_task = asyncio.create_task(self.serial_stream_manager.receive(), name='SerialStreamRx')

        print(f"{type(self)} Exiting init")

    async def open_serial_port(self):
        try:
            await asyncio.wait_for(self.serial_stream_manager.open_port(self.com_port), timeout=5)
            print(f"{type(self)} We are exiting open_serial_port")

        except asyncio.TimeoutError:
            print(f"{type(self)} failed to open {self.com_port}")

    def register_event_observer():
        pass

    async def handle_received_serial_message(self):
        while True:  # TODO instead of infinite loop, could we instead schedule this coroutine when an item is put on the queue?
            byte_string = await self.serial_rx_queue.get()
            msg = self.message_parser.decode_from_bytes(byte_string)
            print(f"<-- Rx: {msg}\n")
            # self.notify(message)

            # TODO these two if clauses are adapter messages (vs stack messages)
            # this should match up with ad_ble_stack_write()?
            # TODO GAPM_CMP_EVT should be sent to BleManager so it knows BleStack ready
            if msg.msg_id == GAPM_MSG_ID.GAPM_DEVICE_READY_IND:
                # This will reset stack
                response = self.gap_manager.handle_message(msg)  # GapManager seems unecessary
                # print(f"response from GapManager: {response}")
                if response is not None:
                    self.serial_tx_queue.put_nowait(response)
                    
            elif msg.msg_id == GAPM_MSG_ID.GAPM_CMP_EVT:
                self.ble_stack_initialized = True
                self.event_q.put_nowait(msg)  # Not making an adapter msg, just forwarding to manager
                self.event_signal.set()

                # TODO send AD_BLE_OP_CMP_EVT to BleManager
            if msg.msg_id != GAPM_MSG_ID.GAPM_CMP_EVT and msg.msg_id != GAPM_MSG_ID.GAPM_DEVICE_READY_IND:
                self.event_q.put_nowait(msg)  # seems this could be combined with above elif. TODO combine adding to queue with setting event
                self.event_signal.set()
                
    def notify():
        pass

# TODO get rid of message router? Send things to this class? Handle default events here. If cannot, send to BleManager to handle