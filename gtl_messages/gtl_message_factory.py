from .gtl_message_base import GTL_INITIATOR
from .gapc_message_factory import GapcMessageFactory
from .gapm_message_factory import GapmMessageFactory
from .gtl_port.rwip_config import KE_API_ID


class GtlMessageFactory():

    @staticmethod
    def create_message(msg_bytes):
        assert(len(msg_bytes) >= 9)

        #print(len(msg_bytes))
        #TODO figure out what is wrong with this assert
        assert(int.from_bytes(msg_bytes[:1], "little",signed=False) == GTL_INITIATOR)

        dst_id=KE_API_ID(int.from_bytes(msg_bytes[3:5], "little",signed=False))
        src_id = KE_API_ID(int.from_bytes(msg_bytes[5:7], "little",signed=False))
        
        # Message type will be defined under the files associated with the non-GTL task id in the message
        message_task_id = src_id
        if(src_id == KE_API_ID.TASK_ID_GTL):
            message_task_id = dst_id

        try:
            if message_task_id == KE_API_ID.TASK_ID_GAPM:
                return GapmMessageFactory().create_message(msg_bytes)

            elif message_task_id == KE_API_ID.TASK_ID_GAPC:
                return GapcMessageFactory().create_message(msg_bytes)
           
            raise AssertionError(f"{type(__class__).__name__}: Message type is unhandled or not valid. message={msg_bytes}")
        except AssertionError as e:
            print(e)
