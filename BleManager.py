import asyncio
from gtl_messages.gtl_message_base import GtlMessageBase
from gtl_messages.gtl_port.gapm_task import GAPM_MSG_ID
from gtl_messages.gtl_port.gapc_task import GAPC_MSG_ID
from gtl_messages.gtl_port.gattc_task import GATTC_MSG_ID
from BleDevParams import BleDevParamsDefault


class BleManager():

    def __init__(self,
                 app_command_q: asyncio.Queue(),
                 app_response_q: asyncio.Queue(),
                 app_event_q: asyncio.Queue(),
                 adapter_command_q: asyncio.Queue(),
                 adapter_event_q: asyncio.Queue(),
                 event_notif: asyncio.Event()) -> None:

        # TODO if x else y is so vscode will treat variable as that item for auto complete
        self.app_command_q = app_command_q if app_command_q else asyncio.Queue()
        self.app_response_q = app_response_q if app_response_q else asyncio.Queue()
        self.app_event_q = app_event_q if app_event_q else asyncio.Queue()
        self.adapter_commnand_q = adapter_command_q if adapter_command_q else asyncio.Queue()
        self.adapter_event_q = adapter_event_q if adapter_event_q else asyncio.Queue()
        self.event_notif = event_notif if event_notif else asyncio.Event()
        self.wait_q = asyncio.Queue()
        self.dev_params = BleDevParamsDefault()

    def init(self):

        # TODO keeping handles so these can be cancelled somehow
        self._task = asyncio.create_task(self.manager_task(), name='BleManagerTask')

        print(f"{type(self)} Exiting init")

    async def manager_task(self):
        # TODO any setup needed
        while True:
            await self.event_notif.wait()  # Need to be careful with multiple events happening before switch to this func
            self.event_notif.clear()
            # get an item from the queue
            if not self.adapter_event_q.empty():
                item = self.adapter_event_q.get_nowait()

            # if item not None:
            print(f" Ble Manager Received event signal {item}")

            # TODO check if more messages in adapter event q

    def handle_evt_or_ind(message: GtlMessageBase):

        match message.msg_id:
            case GAPM_MSG_ID.GAPM_CMP_EVT:
                pass
            case GAPC_MSG_ID.GAPC_PARAM_UPDATE_CMD:
                pass
            case GATTC_MSG_ID.GATTC_CMP_EVT:
                pass
