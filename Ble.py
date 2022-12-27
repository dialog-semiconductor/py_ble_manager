import asyncio

# from gtl_messages.gtl_port.gapm_task import GAPM_OPERATION, gapm_reset_cmd  # TODO remove
# from gtl_messages.gtl_message_gapm import GapmResetCmd  # TODO remove
from gtl_messages.gtl_port.gap import GAP_ROLE

from BleManager import BleManager
from BleAdapter import BleAdapter


# common
class BleBase():
    pass


class BleClient(BleBase):
    pass


class BlePeripheral(BleBase):
    def __init__(self, com_port: str):

        app_command_q = asyncio.Queue()
        app_resposne_q = asyncio.Queue()
        app_event_q = asyncio.Queue()

        adapter_command_q = asyncio.Queue()
        adapter_event_q = asyncio.Queue()

        event_signal = asyncio.Event()

        self.ble_manager = BleManager(app_command_q, app_resposne_q, app_event_q, adapter_command_q, adapter_event_q, event_signal)
        self.ble_adapter = BleAdapter(com_port, adapter_command_q, adapter_event_q, event_signal)

    async def init(self):
        try:
            print("Opening serial port")
            # Open the serial port the the 531
            await self.ble_adapter.open_serial_port()
            print("Serial port opened. Starting always running tasks")

            # TODO need to start a BleManager task

            # Start always running BLE tasks
            self.ble_manager.init()
            self.ble_adapter.init()
            print("Tasks started")

        except asyncio.TimeoutError as e:
            raise e

    def start(self):
        pass
        # status = self._enable
        # if (status is True):
        #    self._set_gap_role_set(GAP_ROLE.GAP_ROLE_PERIPHERAL)

    def _enable():
        # send command
        # await for response.
        # need a command and response queue

        pass

    def _gap_role_set(role: GAP_ROLE.GAP_ROLE_NONE):
        pass

    def execute_command():
        pass  # see ble_cmd_execute

# TODO create ble_dev_params for default device ble database
