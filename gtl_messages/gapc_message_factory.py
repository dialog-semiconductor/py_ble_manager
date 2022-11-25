from ctypes import *
from .gtl_message_gapc import *


class GapcMessageFactory():
    
    @staticmethod
    def create_message(msg_bytes):
        assert(len(msg_bytes) >= 9)

        print(len(msg_bytes))
        #TODO figure out what is wrong with this assert
        assert(int.from_bytes(msg_bytes[:1], "little",signed=False) == GTL_INITIATOR)

        # First byte is GTL header
        msg_id = GAPC_MSG_ID(int.from_bytes(msg_bytes[1:3], "little",signed=False))
       
        par_len=int.from_bytes(msg_bytes[7:9], "little",signed=False)
        params_buf = msg_bytes[9:]


        #TODO for each case add a check to ensure params_buf not too long for parameters variablee
        try:
            if msg_id == GAPC_MSG_ID.GAPC_CONNECTION_REQ_IND:
                return GapcConnectionReqInd(gapc_connection_req_ind.from_buffer_copy(params_buf))

            elif msg_id == GAPC_MSG_ID.GAPC_CONNECTION_CFM:
                return GapcConnectionCfm(gapc_connection_req_ind.from_buffer_copy(params_buf))

            elif msg_id == GAPC_MSG_ID.GAPC_SECURITY_CMD:
                return GapcSecurityCmd(gapc_security_cmd.from_buffer_copy(params_buf))

            raise AssertionError("GapcMessageFactory: Message type is unhandled or not valid")
        except AssertionError as e:
            print(e)

