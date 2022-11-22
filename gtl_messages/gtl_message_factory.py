from ctypes import *
from .gtl_message_base import *
from .gapm_message_factory import *

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
           
            print("Failed to created")
            raise AssertionError("GtlMessageFactory: Message type is handled or not valid.")
        except AssertionError as e:
            print("Exception")
            print(e)
