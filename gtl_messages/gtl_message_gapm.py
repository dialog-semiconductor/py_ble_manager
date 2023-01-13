from .gtl_message_base import GtlMessageBase
from gtl_port.gapm_task import GAPM_MSG_ID, gapm_reset_cmd, gapm_cmp_evt, gapm_set_dev_config_cmd, gapm_start_advertise_cmd, \
    gapm_start_connection_cmd, gapm_start_scan_cmd, gapm_adv_report_ind
from gtl_port.rwip_config import KE_API_ID


class GapmDeviceReadyInd(GtlMessageBase):

    def __init__(self):

        super().__init__(msg_id=GAPM_MSG_ID.GAPM_DEVICE_READY_IND,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=KE_API_ID.TASK_ID_GAPM,
                         par_len=0,
                         parameters=None)


class GapmResetCmd(GtlMessageBase):

    def __init__(self, parameters: gapm_reset_cmd = None):

        self.parameters = parameters if parameters else gapm_reset_cmd()

        super().__init__(msg_id=GAPM_MSG_ID.GAPM_RESET_CMD,
                         dst_id=KE_API_ID.TASK_ID_GAPM,
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=1,
                         parameters=self.parameters)


class GapmCmpEvt(GtlMessageBase):

    def __init__(self, parameters: gapm_cmp_evt = None):

        self.parameters = parameters if parameters else gapm_cmp_evt()

        super().__init__(msg_id=GAPM_MSG_ID.GAPM_CMP_EVT,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=KE_API_ID.TASK_ID_GAPM,
                         par_len=2,
                         parameters=self.parameters)


class GapmSetDevConfigCmd(GtlMessageBase):

    def __init__(self, parameters: gapm_set_dev_config_cmd = None):

        self.parameters = parameters if parameters else gapm_set_dev_config_cmd()

        super().__init__(msg_id=GAPM_MSG_ID.GAPM_SET_DEV_CONFIG_CMD,
                         dst_id=KE_API_ID.TASK_ID_GAPM,
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=44,
                         parameters=self.parameters)


class GapmStartAdvertiseCmd(GtlMessageBase):

    def __init__(self, parameters: gapm_start_advertise_cmd = None):

        self.parameters = parameters if parameters else gapm_start_advertise_cmd()

        super().__init__(msg_id=GAPM_MSG_ID.GAPM_START_ADVERTISE_CMD,
                         dst_id=KE_API_ID.TASK_ID_GAPM,
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=82,
                         parameters=self.parameters)


class GapmStartConnectionCmd(GtlMessageBase):

    def __init__(self, parameters: gapm_start_connection_cmd = None):

        self.parameters = parameters if parameters else gapm_start_connection_cmd()

        super().__init__(msg_id=GAPM_MSG_ID.GAPM_START_CONNECTION_CMD,
                         dst_id=KE_API_ID.TASK_ID_GAPM,
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=self.par_len,
                         parameters=self.parameters)

    def get_par_len(self):
        self._par_len = 21 + (self.parameters.nb_peers * 7) + 1
        return self._par_len

    def set_par_len(self, value):
        self._par_len = value

    par_len = property(get_par_len, set_par_len)


class GapmStartScanCmd(GtlMessageBase):

    def __init__(self, parameters: gapm_start_scan_cmd = None):

        self.parameters = parameters if parameters else gapm_start_scan_cmd()

        super().__init__(msg_id=GAPM_MSG_ID.GAPM_START_SCAN_CMD,
                         dst_id=KE_API_ID.TASK_ID_GAPM,
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=12,
                         parameters=self.parameters)


class GapmAdvReportInd(GtlMessageBase):

    def __init__(self, parameters: gapm_adv_report_ind = None):

        self.parameters = parameters if parameters else gapm_adv_report_ind()

        super().__init__(msg_id=GAPM_MSG_ID.GAPM_ADV_REPORT_IND,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=KE_API_ID.TASK_ID_GAPM,
                         par_len=41,
                         parameters=self.parameters)


# TODO next message GAPM_RESOLV_ADDR_CMD, GAPM_ADDR_SOLVED_IND
