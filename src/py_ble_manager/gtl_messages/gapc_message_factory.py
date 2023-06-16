from ..gtl_messages.gtl_message_gapc import GapcConnectionReqInd, GapcConnectionCfm, GapcSecurityCmd, GapcCmpEvt, GapcGetInfoCmd, \
    GapcPeerFeaturesInd, GapcBondReqInd, GapcBondCfm, GapcGetDevInfoReqInd, GapcDisconnectInd, GapcParamUpdateReqInd, \
    GapcParamUpdatedInd, GapcBondInd, GapcPeerVersionInd, GapcEncryptReqInd, GapcEncryptInd, GapcLePktSizeInd
from ..gtl_port.gapc_task import GAPC_MSG_ID, gapc_connection_req_ind, gapc_connection_cfm, gapc_security_cmd, gapc_cmp_evt, gapc_get_info_cmd, \
    gapc_peer_features_ind, gapc_bond_req_ind, gapc_bond_cfm, gapc_get_dev_info_req_ind, gapc_disconnect_ind, \
    gapc_param_update_req_ind, gapc_param_updated_ind, gapc_bond_ind, gapc_peer_version_ind, gapc_encrypt_req_ind, \
    gapc_encrypt_ind, gapc_le_pkt_size_ind
from ..gtl_port.rwip_config import KE_API_ID


class GapcMessageFactory():

    @staticmethod
    def create_message(msg_bytes: bytes):
        msg_id = GAPC_MSG_ID(int.from_bytes(msg_bytes[1:3], "little", signed=False))
        dst_id = KE_API_ID(int.from_bytes(msg_bytes[3:4], "little", signed=False))

        if dst_id != KE_API_ID.TASK_ID_GTL:
            # If task ID is not TASK_ID_GTL, then it has the connection index in the MSB
            conidx = int.from_bytes(msg_bytes[4:5], "little", signed=False)
        else:
            conidx = int.from_bytes(msg_bytes[6:7], "little", signed=False)

        params_buf = msg_bytes[9:]

        try:
            if msg_id == GAPC_MSG_ID.GAPC_CONNECTION_REQ_IND:
                return GapcConnectionReqInd(conidx=conidx, parameters=gapc_connection_req_ind.from_buffer_copy(params_buf))

            elif msg_id == GAPC_MSG_ID.GAPC_CONNECTION_CFM:
                return GapcConnectionCfm(conidx=conidx, parameters=gapc_connection_cfm.from_buffer_copy(params_buf))

            elif msg_id == GAPC_MSG_ID.GAPC_SECURITY_CMD:
                return GapcSecurityCmd(conidx=conidx, parameters=gapc_security_cmd.from_buffer_copy(params_buf))

            elif msg_id == GAPC_MSG_ID.GAPC_CMP_EVT:
                return GapcCmpEvt(conidx=conidx, parameters=gapc_cmp_evt.from_buffer_copy(params_buf))

            elif msg_id == GAPC_MSG_ID.GAPC_GET_INFO_CMD:
                return GapcGetInfoCmd(conidx=conidx, parameters=gapc_get_info_cmd.from_buffer_copy(params_buf))

            elif msg_id == GAPC_MSG_ID.GAPC_PEER_FEATURES_IND:
                return GapcPeerFeaturesInd(conidx=conidx, parameters=gapc_peer_features_ind.from_buffer_copy(params_buf))

            elif msg_id == GAPC_MSG_ID.GAPC_BOND_REQ_IND:
                return GapcBondReqInd(conidx=conidx, parameters=gapc_bond_req_ind.from_buffer_copy(params_buf))

            elif msg_id == GAPC_MSG_ID.GAPC_BOND_CFM:
                return GapcBondCfm(conidx=conidx, parameters=gapc_bond_cfm.from_buffer_copy(params_buf))

            elif msg_id == GAPC_MSG_ID.GAPC_GET_DEV_INFO_REQ_IND:
                return GapcGetDevInfoReqInd(conidx=conidx, parameters=gapc_get_dev_info_req_ind.from_buffer_copy(params_buf))

            elif msg_id == GAPC_MSG_ID.GAPC_DISCONNECT_IND:
                return GapcDisconnectInd(conidx=conidx, parameters=gapc_disconnect_ind.from_buffer_copy(params_buf))

            elif msg_id == GAPC_MSG_ID.GAPC_PARAM_UPDATE_REQ_IND:
                return GapcParamUpdateReqInd(conidx=conidx, parameters=gapc_param_update_req_ind.from_buffer_copy(params_buf))

            elif msg_id == GAPC_MSG_ID.GAPC_PARAM_UPDATED_IND:
                return GapcParamUpdatedInd(conidx=conidx, parameters=gapc_param_updated_ind.from_buffer_copy(params_buf))

            elif msg_id == GAPC_MSG_ID.GAPC_BOND_IND:
                return GapcBondInd(conidx=conidx, parameters=gapc_bond_ind.from_buffer_copy(params_buf))

            elif msg_id == GAPC_MSG_ID.GAPC_PEER_VERSION_IND:
                return GapcPeerVersionInd(conidx=conidx, parameters=gapc_peer_version_ind.from_buffer_copy(params_buf))

            elif msg_id == GAPC_MSG_ID.GAPC_ENCRYPT_REQ_IND:
                return GapcEncryptReqInd(conidx=conidx, parameters=gapc_encrypt_req_ind.from_buffer_copy(params_buf))

            elif msg_id == GAPC_MSG_ID.GAPC_ENCRYPT_IND:
                return GapcEncryptInd(conidx=conidx, parameters=gapc_encrypt_ind.from_buffer_copy(params_buf))

            elif msg_id == GAPC_MSG_ID.GAPC_LE_PKT_SIZE_IND:
                return GapcLePktSizeInd(conidx=conidx, parameters=gapc_le_pkt_size_ind.from_buffer_copy(params_buf))

            else:
                raise AssertionError(f"GapcMessageFactory: Message type is unhandled or not valid. message={msg_bytes.hex()}")
        except AssertionError as e:
            print(e)
            raise e
