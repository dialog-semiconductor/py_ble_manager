from ctypes import c_uint8

from ..gtl_messages.gtl_message_base import GtlMessageBase
from ..gtl_port.gap import GAP_AUTH_MASK, GAP_IO_CAP, GAP_OOB, GAP_SEC_REQ, GAP_KDIST, GAP_TK_TYPE
from ..gtl_port.gapc_task import GAPC_MSG_ID, gapc_connection_req_ind, gapc_connection_cfm, gapc_security_cmd, gapc_cmp_evt, gapc_get_info_cmd, \
    gapc_peer_features_ind, gapc_bond_req_ind, gapc_bond_cfm, gapc_sign_counter_ind, gapc_bond_ind, gapc_encrypt_req_ind, gapc_encrypt_cfm, \
    gapc_encrypt_ind, gapc_param_update_req_ind, gapc_param_update_cfm, gapc_param_update_cmd, gapc_get_dev_info_req_ind, \
    gapc_get_dev_info_cfm, GAPC_DEV_INFO, gapc_disconnect_ind, gapc_param_updated_ind, gapc_disconnect_cmd, gapc_bond_cmd, \
    gapc_peer_version_ind, GAPC_BOND, GAPC_OPERATION, gapc_set_le_pkt_size_cmd, gapc_le_pkt_size_ind, gapc_encrypt_cmd, \
    gapc_security_ind

from ..gtl_port.rwip_config import KE_API_ID


class GapcConnectionReqInd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gapc_connection_req_ind = None):

        self.parameters = parameters if parameters else gapc_connection_req_ind()

        super().__init__(msg_id=GAPC_MSG_ID.GAPC_CONNECTION_REQ_IND,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=((conidx << 8) | KE_API_ID.TASK_ID_GAPC),
                         par_len=16,
                         parameters=self.parameters)


class GapcConnectionCfm(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gapc_connection_cfm = None):

        self.parameters = parameters if parameters else gapc_connection_cfm()

        super().__init__(msg_id=GAPC_MSG_ID.GAPC_CONNECTION_CFM,
                         dst_id=((conidx << 8) | KE_API_ID.TASK_ID_GAPC),
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=44,
                         parameters=self.parameters)


class GapcSecurityCmd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gapc_security_cmd = None):

        self.parameters = parameters if parameters else gapc_security_cmd()

        super().__init__(msg_id=GAPC_MSG_ID.GAPC_SECURITY_CMD,
                         dst_id=((conidx << 8) | KE_API_ID.TASK_ID_GAPC),
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=2,
                         parameters=self.parameters)


class GapcCmpEvt(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gapc_cmp_evt = None):

        self.parameters = parameters if parameters else gapc_cmp_evt()

        super().__init__(msg_id=GAPC_MSG_ID.GAPC_CMP_EVT,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=((conidx << 8) | KE_API_ID.TASK_ID_GAPC),
                         par_len=2,
                         parameters=self.parameters)


class GapcGetInfoCmd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gapc_get_info_cmd = None):

        self.parameters = parameters if parameters else gapc_get_info_cmd()

        super().__init__(msg_id=GAPC_MSG_ID.GAPC_GET_INFO_CMD,
                         dst_id=((conidx << 8) | KE_API_ID.TASK_ID_GAPC),
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=1,
                         parameters=self.parameters)


class GapcPeerFeaturesInd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gapc_peer_features_ind = None):

        self.parameters = parameters if parameters else gapc_peer_features_ind()

        super().__init__(msg_id=GAPC_MSG_ID.GAPC_PEER_FEATURES_IND,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=((conidx << 8) | KE_API_ID.TASK_ID_GAPC),
                         par_len=8,
                         parameters=self.parameters)


class GapcBondReqInd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gapc_bond_req_ind = None):

        self.parameters = parameters if parameters else gapc_bond_req_ind()

        super().__init__(msg_id=GAPC_MSG_ID.GAPC_BOND_REQ_IND,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=((conidx << 8) | KE_API_ID.TASK_ID_GAPC),
                         par_len=18,
                         parameters=self.parameters)

    def _struct_to_str(self, struct: gapc_bond_req_ind):
        param_string = ''

        param_string += f'(request={str(GAPC_BOND(struct.request))}, '
        param_string += 'data=gapc_bond_req_data('

        match struct.request:
            case GAPC_BOND.GAPC_PAIRING_REQ:
                param_string += f'auth_req={str(GAP_AUTH_MASK(struct.data.auth_req))}'
            case GAPC_BOND.GAPC_LTK_EXCH:
                param_string += f'key_size={struct.data.key_size}'
            case GAPC_BOND.GAPC_TK_EXCH:
                param_string += f'tk_type={str(GAP_TK_TYPE(struct.data.tk_type))}'

        param_string += '), '
        param_string += f'tk=gap_sec_key({self._array_to_str("key", struct.tk.key)[:-2]})'
        param_string += '), '  # ,space This will be removed by __repr__ in GtlMessageBase
        return param_string


class GapcBondCfm(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gapc_bond_cfm = None):

        self.parameters = parameters if parameters else gapc_bond_cfm()

        super().__init__(msg_id=GAPC_MSG_ID.GAPC_BOND_CFM,
                         dst_id=((conidx << 8) | KE_API_ID.TASK_ID_GAPC),
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=30,
                         parameters=self.parameters)

    def _struct_to_str(self, struct: gapc_bond_cfm):
        param_string = ''

        param_string += f'(request={str(GAPC_BOND(struct.request))}, '
        param_string += f'accept={struct.accept}, '
        param_string += 'data=gapc_bond_cfm_data('

        match struct.request:
            case GAPC_BOND.GAPC_PAIRING_RSP:
                param_string += 'pairing_feat=gapc_pairing('
                param_string += f'iocap={str(GAP_IO_CAP(struct.data.pairing_feat.iocap))}, '
                param_string += f'oob={str(GAP_OOB(struct.data.pairing_feat.oob))}, '
                param_string += f'auth={str(GAP_AUTH_MASK(struct.data.pairing_feat.auth))}, '
                param_string += f'key_size={struct.data.pairing_feat.key_size}, '
                param_string += f'ikey_dist={str(GAP_KDIST(struct.data.pairing_feat.ikey_dist))}, '
                param_string += f'rkey_dist={str(GAP_KDIST(struct.data.pairing_feat.rkey_dist))}, '
                param_string += f'sec_req={str(GAP_SEC_REQ(struct.data.pairing_feat.sec_req))}'
                param_string += ')'
            case GAPC_BOND.GAPC_LTK_EXCH:
                param_string += 'ltk=gapc_ltk('
                param_string += f'ltk=gap_sec_key({self._array_to_str("key", struct.data.ltk.ltk.key)[:-2]}), '
                param_string += f'ediv={struct.data.ltk.ediv} '
                param_string += f'randnb=rand_nb({self._array_to_str("nb", struct.data.ltk.randnb.nb)[:-2]}), '
                param_string += f'key_size={struct.data.ltk.key_size}'
                param_string += ')'
            case GAPC_BOND.GAPC_CSRK_EXCH:
                param_string += f'csrk=gap_sec_key({self._array_to_str("key", struct.data.csrk.key)[:-2]})'
            case GAPC_BOND.GAPC_TK_EXCH:
                param_string += f'tk=gap_sec_key({self._array_to_str("key", struct.data.tk.key)[:-2]})'

        param_string += ')'
        param_string += '), '  # ,space This will be removed by __repr__ in GtlMessageBase
        return param_string


class GapcBondInd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gapc_bond_ind = None):

        self.parameters = parameters if parameters else gapc_bond_ind()

        super().__init__(msg_id=GAPC_MSG_ID.GAPC_BOND_IND,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=((conidx << 8) | KE_API_ID.TASK_ID_GAPC),
                         par_len=30,
                         parameters=self.parameters)

    def _struct_to_str(self, struct: gapc_bond_ind):
        param_string = ''

        param_string += f'(info={str(GAPC_BOND(struct.info))}, '
        param_string += f'padding={0}, '
        param_string += 'data=gapc_bond_data('

        match struct.info:
            case GAPC_BOND.GAPC_PAIRING_SUCCEED:
                param_string += f'auth={str(GAP_AUTH_MASK(struct.data.auth))}'
            case GAPC_BOND.GAPC_PAIRING_FAILED:
                param_string += f'reason={(struct.data.reason)}'
            case GAPC_BOND.GAPC_LTK_EXCH:
                param_string += 'ltk=gapc_ltk('
                param_string += f'ltk=gap_sec_key({self._array_to_str("key", struct.data.ltk.ltk.key)[:-2]}), '
                param_string += f'ediv={struct.data.ltk.ediv} '
                param_string += f'randnb=rand_nb({self._array_to_str("nb", struct.data.ltk.randnb.nb)[:-2]}), '
                param_string += f'key_size={struct.data.ltk.key_size}'
                param_string += ')'
            case GAPC_BOND.GAPC_IRK_EXCH:
                param_string += 'irk=gapc_irk('
                param_string += f'irk=gap_sec_key({self._array_to_str("key", struct.data.irk.irk.key)[:-2]}, '
                param_string += f'addr=gap_bdaddr=(addr_type={struct.data.irk.addr.addr_type}, '
                param_string += f'addr={self._array_to_str("bd_addr", struct.data.irk.addr.addr.addr)[:-2]}))'
                param_string += ')'
            case GAPC_BOND.GAPC_CSRK_EXCH:
                param_string += f'csrk=gap_sec_key({self._array_to_str("key", struct.data.csrk.key)[:-2]})'

        param_string += ')'
        param_string += '), '  # ,space This will be removed by __repr__ in GtlMessageBase

        return param_string


class GapcEncryptReqInd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gapc_encrypt_req_ind = None):

        self.parameters = parameters if parameters else gapc_encrypt_req_ind()

        super().__init__(msg_id=GAPC_MSG_ID.GAPC_ENCRYPT_REQ_IND,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=((conidx << 8) | KE_API_ID.TASK_ID_GAPC),
                         par_len=10,
                         parameters=self.parameters)


class GapcEncryptCfm(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gapc_encrypt_cfm = None):

        self.parameters = parameters if parameters else gapc_encrypt_cfm()

        super().__init__(msg_id=GAPC_MSG_ID.GAPC_ENCRYPT_CFM,
                         dst_id=((conidx << 8) | KE_API_ID.TASK_ID_GAPC),
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=18,
                         parameters=self.parameters)


class GapcEncryptInd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gapc_encrypt_ind = None):

        self.parameters = parameters if parameters else gapc_encrypt_ind()

        super().__init__(msg_id=GAPC_MSG_ID.GAPC_ENCRYPT_IND,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=((conidx << 8) | KE_API_ID.TASK_ID_GAPC),
                         par_len=1,
                         parameters=self.parameters)


class GapcParamUpdateReqInd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gapc_param_update_req_ind = None):

        self.parameters = parameters if parameters else gapc_param_update_req_ind()

        super().__init__(msg_id=GAPC_MSG_ID.GAPC_PARAM_UPDATE_REQ_IND,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=((conidx << 8) | KE_API_ID.TASK_ID_GAPC),
                         par_len=8,
                         parameters=self.parameters)


class GapcParamUpdateCfm(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gapc_param_update_cfm = None):

        self.parameters = parameters if parameters else gapc_param_update_cfm()

        super().__init__(msg_id=GAPC_MSG_ID.GAPC_PARAM_UPDATE_CFM,
                         dst_id=((conidx << 8) | KE_API_ID.TASK_ID_GAPC),
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=6,
                         parameters=self.parameters)


class GapcParamUpdateCmd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gapc_param_update_cmd = None):

        self.parameters = parameters if parameters else gapc_param_update_cmd()

        super().__init__(msg_id=GAPC_MSG_ID.GAPC_PARAM_UPDATE_CMD,
                         dst_id=((conidx << 8) | KE_API_ID.TASK_ID_GAPC),
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=14,
                         parameters=self.parameters)


class GapcParamUpdatedInd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gapc_param_updated_ind = None):

        self.parameters = parameters if parameters else gapc_param_updated_ind()

        super().__init__(msg_id=GAPC_MSG_ID.GAPC_PARAM_UPDATED_IND,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=((conidx << 8) | KE_API_ID.TASK_ID_GAPC),
                         par_len=6,
                         parameters=self.parameters)


class GapcSignCounterInd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gapc_sign_counter_ind = None):

        self.parameters = parameters if parameters else gapc_sign_counter_ind()

        super().__init__(msg_id=GAPC_MSG_ID.GAPC_SIGN_COUNTER_IND,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=((conidx << 8) | KE_API_ID.TASK_ID_GAPC),
                         par_len=8,
                         parameters=self.parameters)


class GapcDisconnectCmd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gapc_disconnect_cmd = None):

        self.parameters = parameters if parameters else gapc_disconnect_cmd()

        super().__init__(msg_id=GAPC_MSG_ID.GAPC_DISCONNECT_CMD,
                         dst_id=((conidx << 8) | KE_API_ID.TASK_ID_GAPC),
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=2,
                         parameters=self.parameters)


class GapcDisconnectInd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gapc_disconnect_ind = None):

        self.parameters = parameters if parameters else gapc_disconnect_ind()

        super().__init__(msg_id=GAPC_MSG_ID.GAPC_DISCONNECT_IND,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=((conidx << 8) | KE_API_ID.TASK_ID_GAPC),
                         par_len=4,
                         parameters=self.parameters)


class GapcGetDevInfoReqInd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gapc_get_dev_info_req_ind = None):

        self.parameters = parameters if parameters else gapc_get_dev_info_req_ind()

        super().__init__(msg_id=GAPC_MSG_ID.GAPC_GET_DEV_INFO_REQ_IND,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=((conidx << 8) | KE_API_ID.TASK_ID_GAPC),
                         par_len=1,
                         parameters=self.parameters)


class GapcGetDevInfoCfm(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gapc_get_dev_info_cfm = None):

        self.parameters = parameters if parameters else gapc_get_dev_info_cfm()

        super().__init__(msg_id=GAPC_MSG_ID.GAPC_GET_DEV_INFO_CFM,
                         dst_id=((conidx << 8) | KE_API_ID.TASK_ID_GAPC),
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=self.par_len,
                         parameters=self.parameters)

    def get_par_len(self):
        if self.parameters.req == GAPC_DEV_INFO.GAPC_DEV_NAME:
            self._par_len = 10 + self.parameters.info.name.length
        elif self.parameters.req == GAPC_DEV_INFO.GAPC_DEV_APPEARANCE:
            self._par_len = 10 + 2
        elif self.parameters.req == GAPC_DEV_INFO.GAPC_DEV_SLV_PREF_PARAMS:
            self._par_len = 10 + 8
        elif self.parameters.req == GAPC_DEV_INFO.GAPC_DEV_CENTRAL_RPA:
            self._par_len = 10 + 1
        elif self.parameters.req == GAPC_DEV_INFO.GAPC_DEV_RPA_ONLY:
            self._par_len = 10 + 1
        return self._par_len

    def set_par_len(self, value):
        self._par_len = value

    par_len = property(get_par_len, set_par_len)

    def _struct_to_str(self, struct: gapc_get_dev_info_cfm):
        param_string = ''

        param_string += f'(req={str(GAPC_DEV_INFO(struct.req))}, '
        param_string += 'info=gapc_dev_info_val('

        match struct.req:
            case GAPC_DEV_INFO.GAPC_DEV_NAME:
                param_string += f'name=gap_dev_name({self._array_to_str("value", struct.info.name.value)[:-2]})'
            case GAPC_DEV_INFO.GAPC_DEV_APPEARANCE:
                param_string += f'appearance={struct.info.appearance}'
            case GAPC_DEV_INFO.GAPC_DEV_SLV_PREF_PARAMS:
                param_string += 'slv_params=gap_slv_pref('
                param_string += f'con_intv_min={struct.info.slv_params.con_intv_min}, '
                param_string += f'con_intv_max={struct.info.slv_params.con_intv_max}, '
                param_string += f'slave_latency={struct.info.slv_params.slave_latency}, '
                param_string += f'conn_timeout={struct.info.slv_params.conn_timeout})'
            case GAPC_DEV_INFO.GAPC_DEV_CENTRAL_RPA:
                param_string += f'central_rpa={struct.info.central_rpa}'
            case GAPC_DEV_INFO.GAPC_DEV_RPA_ONLY:
                param_string += f'rpa_only={struct.info.rpa_only}'
        param_string += ')'
        param_string += '), '  # ,space This will be removed by __repr__ in GtlMessageBase
        return param_string

    def _struct_to_bytearray(self, struct: gapc_get_dev_info_cfm):

        return_array = bytearray()
        return_array = bytearray(struct.req.to_bytes(length=1, byteorder='little'))
        padding = 0
        return_array += bytearray(padding.to_bytes(length=1, byteorder='little'))  # padding
        return_array += bytearray(struct.info.name.length.to_bytes(length=2, byteorder='little'))

        if struct.req == GAPC_DEV_INFO.GAPC_DEV_NAME:
            return_array += bytearray(struct.info.name.value)
        elif struct.req == GAPC_DEV_INFO.GAPC_DEV_APPEARANCE:
            return_array += bytearray(struct.info.appearance.to_bytes(length=2, byteorder='little'))
        elif struct.req == GAPC_DEV_INFO.GAPC_DEV_SLV_PREF_PARAMS:
            return_array += bytearray(struct.info.slv_params)
        elif struct.req == GAPC_DEV_INFO.GAPC_DEV_CENTRAL_RPA:
            return_array += bytearray(struct.info.central_rpa.to_bytes(length=1, byteorder='little'))
        elif struct.req == GAPC_DEV_INFO.GAPC_DEV_RPA_ONLY:
            return_array += bytearray(struct.info.rpa_only.to_bytes(length=1, byteorder='little'))

        return_array += bytearray((c_uint8 * 6)())  # more padding

        return return_array


# TODO this message not documented in GTL user manual, needs unit test
class GapcBondCmd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gapc_bond_cmd = None):

        self.parameters = parameters if parameters else gapc_bond_cmd()

        super().__init__(msg_id=GAPC_MSG_ID.GAPC_BOND_CMD,
                         dst_id=((conidx << 8) | KE_API_ID.TASK_ID_GAPC),
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=8,
                         parameters=self.parameters)

    def _struct_to_str(self, struct: gapc_bond_cmd):
        param_string = ''

        param_string += f'(info={str(GAPC_OPERATION(struct.operation))}, '
        param_string += 'pair=gapc_pairing('
        param_string += f'iocap={str(GAP_IO_CAP(struct.pairing.iocap))}, '
        param_string += f'oob={str(GAP_OOB(struct.pairing.oob))}, '
        param_string += f'auth={str(GAP_AUTH_MASK(struct.pairing.auth))}, '
        param_string += f'key_size={struct.pairing.key_size}, '
        param_string += f'ikey_dist={str(GAP_KDIST(struct.pairing.ikey_dist))}, '
        param_string += f'rkey_dist={str(GAP_KDIST(struct.pairing.rkey_dist))}, '
        param_string += f'sec_req={str(GAP_SEC_REQ(struct.pairing.sec_req))}'
        param_string += ')'
        param_string += '), '
        return param_string


class GapcPeerVersionInd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gapc_peer_version_ind = None):

        self.parameters = parameters if parameters else gapc_peer_version_ind()

        super().__init__(msg_id=GAPC_MSG_ID.GAPC_PEER_VERSION_IND,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=((conidx << 8) | KE_API_ID.TASK_ID_GAPC),
                         par_len=6,
                         parameters=self.parameters)


class GapcSetLePktSizeCmd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gapc_set_le_pkt_size_cmd = None):

        self.parameters = parameters if parameters else gapc_set_le_pkt_size_cmd()

        super().__init__(msg_id=GAPC_MSG_ID.GAPC_SET_LE_PKT_SIZE_CMD,
                         dst_id=((conidx << 8) | KE_API_ID.TASK_ID_GAPC),
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=6,
                         parameters=self.parameters)


class GapcLePktSizeInd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gapc_le_pkt_size_ind = None):

        self.parameters = parameters if parameters else gapc_le_pkt_size_ind()

        super().__init__(msg_id=GAPC_MSG_ID.GAPC_LE_PKT_SIZE_IND,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=((conidx << 8) | KE_API_ID.TASK_ID_GAPC),
                         par_len=8,
                         parameters=self.parameters)


# TODO need unit test
class GapcEncryptCmd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gapc_encrypt_cmd = None):

        self.parameters = parameters if parameters else gapc_encrypt_cmd()

        super().__init__(msg_id=GAPC_MSG_ID.GAPC_ENCRYPT_CMD,
                         dst_id=((conidx << 8) | KE_API_ID.TASK_ID_GAPC),
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=30,
                         parameters=self.parameters)


# TODO need unit test
class GapcSecurityInd(GtlMessageBase):

    def __init__(self, conidx: c_uint8 = 0, parameters: gapc_security_ind = None):

        self.parameters = parameters if parameters else gapc_security_ind()

        super().__init__(msg_id=GAPC_MSG_ID.GAPC_SECURITY_IND,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=((conidx << 8) | KE_API_ID.TASK_ID_GAPC),
                         par_len=2,
                         parameters=self.parameters)
