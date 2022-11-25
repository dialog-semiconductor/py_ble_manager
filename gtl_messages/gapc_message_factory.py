from ctypes import *
from .gtl_message_gapc import *


class GapcMessageFactory():
    
    @staticmethod
    def create_message(msg_bytes):
        assert(len(msg_bytes) >= 9)

        #TODO figure out what is wrong with this assert
        assert(int.from_bytes(msg_bytes[:1], "little",signed=False) == GTL_INITIATOR)

        # First byte is GTL header
        msg_id = GAPC_MSG_ID(int.from_bytes(msg_bytes[1:3], "little",signed=False))

        # cannot pass these direct, need to pull conidx out
        dst_id = KE_API_ID(int.from_bytes(msg_bytes[4:5], "little",signed=False))
        src_id = KE_API_ID(int.from_bytes(msg_bytes[6:7], "little",signed=False))

        if dst_id != KE_API_ID.TASK_ID_GTL:
            conidx = int.from_bytes(msg_bytes[3:4], "little",signed=False)
        else:
            conidx = int.from_bytes(msg_bytes[5:6], "little",signed=False)

        par_len=int.from_bytes(msg_bytes[7:9], "little",signed=False)
        params_buf = msg_bytes[9:]


        #TODO for each case add a check to ensure params_buf not too long for parameters variable
        try:
            if msg_id == GAPC_MSG_ID.GAPC_CONNECTION_REQ_IND:
                return GapcConnectionReqInd(conidx=conidx, parameters=gapc_connection_req_ind.from_buffer_copy(params_buf))

            elif msg_id == GAPC_MSG_ID.GAPC_CONNECTION_CFM:
                return GapcConnectionCfm(conidx=conidx, parameters=gapc_connection_req_ind.from_buffer_copy(params_buf))

            elif msg_id == GAPC_MSG_ID.GAPC_SECURITY_CMD:
                return GapcSecurityCmd(conidx=conidx, parameters=gapc_security_cmd.from_buffer_copy(params_buf))

            elif msg_id == GAPC_MSG_ID.GAPC_CMP_EVT:
                return GapcCmpEvt(conidx=conidx, parameters=gapc_cmp_evt().from_buffer_copy(params_buf))

            elif msg_id == GAPC_MSG_ID.GAPC_GET_INFO_CMD:
                return GapcGetInfoCmd(conidx=conidx, parameters=gapc_get_info_cmd().from_buffer_copy(params_buf))

            elif msg_id == GAPC_MSG_ID.GAPC_PEER_FEATURES_IND:
                return GapcPeerFeaturesInd(conidx=conidx, parameters=gapc_peer_features_ind().from_buffer_copy(params_buf))

            elif msg_id == GAPC_MSG_ID.GAPC_BOND_REQ_IND:
                return GapcBondReqInd(conidx=conidx, parameters=gapc_bond_req_ind().from_buffer_copy(params_buf))

            elif msg_id == GAPC_MSG_ID.GAPC_BOND_REQ_IND:
                return GapcBondReqInd(conidx=conidx, parameters=gapc_bond_req_ind().from_buffer_copy(params_buf))

            elif msg_id == GAPC_MSG_ID.GAPC_BOND_CFM:
                return GapcBondCfm(conidx=conidx, parameters=gapc_bond_cfm().from_buffer_copy(params_buf))

            raise AssertionError("GapcMessageFactory: Message type is unhandled or not valid")
        except AssertionError as e:
            print(e)

