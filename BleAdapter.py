import asyncio
from Gap import GapController, GapManager
from MessageRouter import MessageRouter
from SerialStreamManager import SerialStreamManager
from MessageRouter import MessageParser
from gtl_messages.gtl_port.gapm_task import GAPM_MSG_ID
# from ctypes import LittleEndianStructure, c_uint16, c_uint8, Array, pointer, POINTER, cast
# from enum import IntEnum, auto


'''
# from ad_ble.h
# Operations for BLE adapter messages
class AD_BLE_OPCODES(IntEnum):
    AD_BLE_OP_CODE_STACK_MSG = 0x00
    AD_BLE_OP_CODE_ADAPTER_MSG = 0x01
    AD_BLE_OP_CODE_LAST = auto()


class AD_BLE_OPERATION(IntEnum):
    AD_BLE_OP_CMP_EVT = 0x00
    AD_BLE_OP_INIT_CMD = 0x01
    AD_BLE_OP_RESET_CMD = 0x02
    AD_BLE_OP_LAST = auto()


# BLE adapter message structure
class ad_ble_msg(LittleEndianStructure):
    def __init__(self,
                 operation: AD_BLE_OPERATION = AD_BLE_OPERATION.AD_BLE_OP_LAST,
                 msg_len: c_uint16 = 0
                 ):

        self.op_code = AD_BLE_OPCODES.AD_BLE_OP_CODE_ADAPTER_MSG
        self.operation = operation
        self.param = (c_uint8 * msg_len)()
        super().__init__(op_code=self.op_code,
                         msg_size=self.msg_size,
                         operation=self.operation,
                         _param=self._param)

    _fields_ = [("op_code", c_uint16),
                ("msg_size", c_uint16),
                ("operation", c_uint8),
                ("_param", POINTER(c_uint8))]

    def get_param(self):
        return cast(self._param, POINTER(c_uint8 * self.msg_size)).contents

    def set_param(self, new_param: Array[c_uint8]):
        self._param = new_param if new_param else pointer(c_uint8(0))
        self.msg_size = len(new_param) if new_param else 0

    value = property(get_param, set_param)

# end ad_ble.h
'''


class BleAdapter():

    def __init__(self, com_port: str, command_q: asyncio.Queue(), event_q: asyncio.Queue(), event_signal: asyncio.Event()) -> None:

        self.event_observers = []
        self.message_parser = MessageParser()
        self.command_q = command_q if command_q else asyncio.Queue()
        self.event_q = event_q if event_q else asyncio.Queue()
        self.event_signal = event_signal if event_signal else asyncio.Event()
        self.ble_stack_initialized = False
        self.reset_signal = asyncio.Event()

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
        self.handle_rx_task = asyncio.create_task(self.adapter_task(), name='BleAdapterTx')
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

    async def adapter_task(self):
        # TODO any setup needed
        while True:
            command = await self.command_q.get()
            self.serial_tx_queue.put_nowait(command)

            while not self.command_q.empty():
                command = self.command_q.get_nowait()
                self.serial_tx_queue.put_nowait(command)

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

    def notify(self):
        pass

    def ble_reset(self):
        self.serial_tx_queue.put_nowait(self.gap_manager.create_reset_command())

# TODO get rid of message router? Send things to this class? Handle default events here. If cannot, send to BleManager to handle
