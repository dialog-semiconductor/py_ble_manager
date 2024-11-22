from ctypes import c_uint8

from ..gtl_messages.gtl_message_gapc import GapcConnectionReqInd, GapcConnectionCfm, GapcSecurityCmd, GapcCmpEvt, GapcGetInfoCmd, \
    GapcPeerFeaturesInd, GapcBondReqInd, GapcBondCfm, GapcGetDevInfoReqInd, GapcDisconnectInd, GapcParamUpdateReqInd, \
    GapcParamUpdatedInd, GapcBondInd, GapcPeerVersionInd, GapcEncryptReqInd, GapcEncryptCfm, GapcEncryptInd, GapcLePktSizeInd, \
    GapcSecurityInd, GapcSignCounterInd, GapcSetDevInfoReqInd, GapcLePhyInd, GapcParamUpdateCfm, GapcParamUpdateCmd, \
    GapcDisconnectCmd, GapcGetDevInfoCfm, GapcBondCmd, GapcSetLePktSizeCmd, GapcEncryptCmd, GapcSetDevInfoCfm
from ..gtl_port.gapc_task import GAPC_MSG_ID, gapc_connection_req_ind, gapc_connection_cfm, gapc_security_cmd, gapc_cmp_evt, gapc_get_info_cmd, \
    gapc_peer_features_ind, gapc_bond_req_ind, gapc_bond_cfm, gapc_get_dev_info_req_ind, gapc_disconnect_ind, \
    gapc_param_update_req_ind, gapc_param_updated_ind, gapc_bond_ind, gapc_peer_version_ind, gapc_encrypt_req_ind, \
    gapc_encrypt_ind, gapc_le_pkt_size_ind, gapc_security_ind, gapc_sign_counter_ind, gapc_set_dev_info_req_ind, GAPC_DEV_INFO, \
    gapc_le_phy_ind, gapc_encrypt_cfm, gapc_param_update_cfm, gapc_param_update_cmd, gapc_disconnect_cmd, gapc_get_dev_info_cfm, \
    gapc_bond_cmd, gapc_set_le_pkt_size_cmd, gapc_encrypt_cmd, gapc_set_dev_info_cfm, gap_slv_pref
from ..gtl_port.rwip_config import KE_API_ID


class GapcMessageFactory():

    @staticmethod
    def connection_req_ind(conidx: int, params_buf: bytes):
        return GapcConnectionReqInd(conidx=conidx, parameters=gapc_connection_req_ind.from_buffer_copy(params_buf))

    @staticmethod
    def connection_cfm(conidx: int, params_buf: bytes):
        return GapcConnectionCfm(conidx=conidx, parameters=gapc_connection_cfm.from_buffer_copy(params_buf))

    @staticmethod
    def security_cmd(conidx: int, params_buf: bytes):
        return GapcSecurityCmd(conidx=conidx, parameters=gapc_security_cmd.from_buffer_copy(params_buf))

    @staticmethod
    def cmp_evt(conidx: int, params_buf: bytes):
        return GapcCmpEvt(conidx=conidx, parameters=gapc_cmp_evt.from_buffer_copy(params_buf))

    @staticmethod
    def get_info_cmd(conidx: int, params_buf: bytes):
        return GapcGetInfoCmd(conidx=conidx, parameters=gapc_get_info_cmd.from_buffer_copy(params_buf))

    @staticmethod
    def peer_features_ind(conidx: int, params_buf: bytes):
        return GapcPeerFeaturesInd(conidx=conidx, parameters=gapc_peer_features_ind.from_buffer_copy(params_buf))

    @staticmethod
    def bond_req_ind(conidx: int, params_buf: bytes):
        return GapcBondReqInd(conidx=conidx, parameters=gapc_bond_req_ind.from_buffer_copy(params_buf))

    @staticmethod
    def bond_cfm(conidx: int, params_buf: bytes):
        return GapcBondCfm(conidx=conidx, parameters=gapc_bond_cfm.from_buffer_copy(params_buf))

    @staticmethod
    def bond_ind(conidx: int, params_buf: bytes):
        return GapcBondInd(conidx=conidx, parameters=gapc_bond_ind.from_buffer_copy(params_buf))

    @staticmethod
    def encrypt_req_ind(conidx: int, params_buf: bytes):
        return GapcEncryptReqInd(conidx=conidx, parameters=gapc_encrypt_req_ind.from_buffer_copy(params_buf))

    @staticmethod
    def encrypt_cfm(conidx: int, params_buf: bytes):
        return GapcEncryptCfm(conidx=conidx, parameters=gapc_encrypt_cfm.from_buffer_copy(params_buf))

    @staticmethod
    def encrypt_ind(conidx: int, params_buf: bytes):
        return GapcEncryptInd(conidx=conidx, parameters=gapc_encrypt_ind.from_buffer_copy(params_buf))

    @staticmethod
    def param_update_req_ind(conidx: int, params_buf: bytes):
        return GapcParamUpdateReqInd(conidx=conidx, parameters=gapc_param_update_req_ind.from_buffer_copy(params_buf))

    @staticmethod
    def param_update_cfm(conidx: int, params_buf: bytes):
        return GapcParamUpdateCfm(conidx=conidx, parameters=gapc_param_update_cfm.from_buffer_copy(params_buf))

    @staticmethod
    def param_update_cmd(conidx: int, params_buf: bytes):
        return GapcParamUpdateCmd(conidx=conidx, parameters=gapc_param_update_cmd.from_buffer_copy(params_buf))

    @staticmethod
    def param_updated_ind(conidx: int, params_buf: bytes):
        return GapcParamUpdatedInd(conidx=conidx, parameters=gapc_param_updated_ind.from_buffer_copy(params_buf))

    @staticmethod
    def sign_counter_ind(conidx: int, params_buf: bytes):
        return GapcSignCounterInd(conidx=conidx, parameters=gapc_sign_counter_ind.from_buffer_copy(params_buf))

    @staticmethod
    def disconnect_cmd(conidx: int, params_buf: bytes):
        return GapcDisconnectCmd(conidx=conidx, parameters=gapc_disconnect_cmd.from_buffer_copy(params_buf))

    @staticmethod
    def disconnect_ind(conidx: int, params_buf: bytes):
        return GapcDisconnectInd(conidx=conidx, parameters=gapc_disconnect_ind.from_buffer_copy(params_buf))

    @staticmethod
    def get_dev_info_req_ind(conidx: int, params_buf: bytes):
        return GapcGetDevInfoReqInd(conidx=conidx, parameters=gapc_get_dev_info_req_ind.from_buffer_copy(params_buf))

    @staticmethod
    def get_dev_info_cfm(conidx: int, params_buf: bytes):
        # TODO unit test for dev_name only, need test for other req types
        parameters = gapc_get_dev_info_cfm()
        parameters.req = params_buf[0]
        # padding = params_buf[1]
        if parameters.req == GAPC_DEV_INFO.GAPC_DEV_NAME:
            # parameters.info.name.length will be set when parameters.info.name.value set
            length = int.from_bytes(params_buf[2:4], "little", signed=False)
            # -6 to account for additional padding in gapc_get_dev_info_cfm
            assert (length) == len(params_buf[4:-6]), f"length={length}, params_buf[4:]={len(params_buf[4:-6])}"  # Check for mismatch in value length and remaining bytes
            parameters.info.name.value = (length * c_uint8).from_buffer_copy(params_buf[4:-6])
        elif parameters.req == GAPC_DEV_INFO.GAPC_DEV_APPEARANCE:
            assert len(params_buf[2:-6] == 2)
            parameters.info.appearance = params_buf[2:]
        elif parameters.req == GAPC_DEV_INFO.GAPC_DEV_SLV_PREF_PARAMS:
            parameters.info.slv_params = gap_slv_pref.from_buffer_copy(params_buf[2:-6])
        elif parameters.req == GAPC_DEV_INFO.GAPC_DEV_CENTRAL_RPA:
            assert len(params_buf[2:-6] == 1)
            parameters.info.central_rpa = params_buf[2:-6]
        else:
            # req = GAPC_DEV_INFO.GAPC_DEV_RPA_ONLY
            assert len(params_buf[2:-6] == 1)
            parameters.info.rpa_only = params_buf[2:-6]

        return GapcGetDevInfoCfm(conidx=conidx, parameters=parameters)

    @staticmethod
    def bond_cmd(conidx: int, params_buf: bytes):
        # TODO has no unit test
        return GapcBondCmd(conidx=conidx, parameters=gapc_bond_cmd.from_buffer_copy(params_buf))

    @staticmethod
    def peer_version_ind(conidx: int, params_buf: bytes):
        return GapcPeerVersionInd(conidx=conidx, parameters=gapc_peer_version_ind.from_buffer_copy(params_buf))

    @staticmethod
    def set_le_pkt_size_cmd(conidx: int, params_buf: bytes):
        return GapcSetLePktSizeCmd(conidx=conidx, parameters=gapc_set_le_pkt_size_cmd.from_buffer_copy(params_buf))

    @staticmethod
    def le_pkt_size_ind(conidx: int, params_buf: bytes):
        return GapcLePktSizeInd(conidx=conidx, parameters=gapc_le_pkt_size_ind.from_buffer_copy(params_buf))

    @staticmethod
    def encrypt_cmd(conidx: int, params_buf: bytes):
        # TODO has no unit test
        return GapcEncryptCmd(conidx=conidx, parameters=gapc_encrypt_cmd.from_buffer_copy(params_buf))

    @staticmethod
    def security_ind(conidx: int, params_buf: bytes):
        # TODO has no unit test
        return GapcSecurityInd(conidx=conidx, parameters=gapc_security_ind.from_buffer_copy(params_buf))

    @staticmethod
    def set_dev_info_req_ind(conidx: int, params_buf: bytes):
        parameters = gapc_set_dev_info_req_ind()
        parameters.req = params_buf[0]
        # padding = params_buf[1]
        if parameters.req == GAPC_DEV_INFO.GAPC_DEV_NAME:
            # parameters.info.name.length will be set when parameters.info.name.value set
            length = int.from_bytes(params_buf[2:4], "little", signed=False)
            assert (length) == len(params_buf[4:])  # Check for mismatch in value length and remaining bytes
            parameters.info.name.value = (length * c_uint8).from_buffer_copy(params_buf[4:])
        else:
            # req = GAPC_DEV_INFO.GAPC_DEV_APPEARANCE
            assert len(params_buf[2:] == 2)
            parameters.info.appearance = params_buf[2:]

        return GapcSetDevInfoReqInd(conidx=conidx, parameters=parameters)

    @staticmethod
    def set_dev_info_cfm(conidx: int, params_buf: bytes):
        return GapcSetDevInfoCfm(conidx=conidx, parameters=gapc_set_dev_info_cfm.from_buffer_copy(params_buf))

    @staticmethod
    def le_phy_ind(conidx: int, params_buf: bytes):
        # TODO has no unit test
        return GapcLePhyInd(conidx=conidx, parameters=gapc_le_phy_ind.from_buffer_copy(params_buf))

    @classmethod
    def create_message(cls, msg_bytes: bytes):
        msg_id = GAPC_MSG_ID(int.from_bytes(msg_bytes[1:3], "little", signed=False))
        dst_id = KE_API_ID(int.from_bytes(msg_bytes[3:4], "little", signed=False))

        if dst_id != KE_API_ID.TASK_ID_GTL:
            # If task ID is not TASK_ID_GTL, then it has the connection index in the MSB
            conidx = int.from_bytes(msg_bytes[4:5], "little", signed=False)
        else:
            conidx = int.from_bytes(msg_bytes[6:7], "little", signed=False)

        params_buf = msg_bytes[9:]
        handler = cls.msg_handlers.get(msg_id)
        try:
            if handler:
                return handler(conidx, params_buf)
            else:
                raise AssertionError(f"{__class__.__name__}: Message type is unhandled or not valid. msg_id={type(msg_id).__name__}.{msg_id.name}, message={msg_bytes.hex()}")
        except AssertionError as e:
            print(e)
            raise e

    msg_handlers = {
        GAPC_MSG_ID.GAPC_CONNECTION_REQ_IND: connection_req_ind,
        GAPC_MSG_ID.GAPC_CONNECTION_CFM: connection_cfm,
        GAPC_MSG_ID.GAPC_SECURITY_CMD: security_cmd,
        GAPC_MSG_ID.GAPC_CMP_EVT: cmp_evt,
        GAPC_MSG_ID.GAPC_GET_INFO_CMD: get_info_cmd,
        GAPC_MSG_ID.GAPC_PEER_FEATURES_IND: peer_features_ind,
        GAPC_MSG_ID.GAPC_BOND_REQ_IND: bond_req_ind,
        GAPC_MSG_ID.GAPC_BOND_CFM: bond_cfm,
        GAPC_MSG_ID.GAPC_BOND_IND: bond_ind,
        GAPC_MSG_ID.GAPC_ENCRYPT_REQ_IND: encrypt_req_ind,
        GAPC_MSG_ID.GAPC_ENCRYPT_CFM: encrypt_cfm,
        GAPC_MSG_ID.GAPC_ENCRYPT_IND: encrypt_ind,
        GAPC_MSG_ID.GAPC_PARAM_UPDATE_REQ_IND: param_update_req_ind,
        GAPC_MSG_ID.GAPC_PARAM_UPDATE_CFM: param_update_cfm,
        GAPC_MSG_ID.GAPC_PARAM_UPDATE_CMD: param_update_cmd,
        GAPC_MSG_ID.GAPC_PARAM_UPDATED_IND: param_updated_ind,
        GAPC_MSG_ID.GAPC_SIGN_COUNTER_IND: sign_counter_ind,
        GAPC_MSG_ID.GAPC_DISCONNECT_CMD: disconnect_cmd,
        GAPC_MSG_ID.GAPC_DISCONNECT_IND: disconnect_ind,
        GAPC_MSG_ID.GAPC_GET_DEV_INFO_REQ_IND: get_dev_info_req_ind,
        GAPC_MSG_ID.GAPC_GET_DEV_INFO_CFM: get_dev_info_cfm,
        GAPC_MSG_ID.GAPC_BOND_CMD: bond_cmd,
        GAPC_MSG_ID.GAPC_PEER_VERSION_IND: peer_version_ind,
        GAPC_MSG_ID.GAPC_SET_LE_PKT_SIZE_CMD: set_le_pkt_size_cmd,
        GAPC_MSG_ID.GAPC_LE_PKT_SIZE_IND: le_pkt_size_ind,
        GAPC_MSG_ID.GAPC_ENCRYPT_CMD: encrypt_cmd,
        GAPC_MSG_ID.GAPC_SECURITY_IND: security_ind,
        GAPC_MSG_ID.GAPC_SET_DEV_INFO_REQ_IND: set_dev_info_req_ind,
        GAPC_MSG_ID.GAPC_SET_DEV_INFO_CFM: set_dev_info_cfm,
        GAPC_MSG_ID.GAPC_LE_PHY_IND: le_phy_ind,
    }
