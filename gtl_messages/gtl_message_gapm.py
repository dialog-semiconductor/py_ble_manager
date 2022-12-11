from ctypes import *
from .gtl_message_base import *

class GapmDeviceReadyInd(GtlMessageBase):
     def __init__(self):

        super().__init__(msg_id=GAPM_MSG_ID.GAPM_DEVICE_READY_IND,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=KE_API_ID.TASK_ID_GAPM,
                         par_len=0,
                         parameters=None)

class GapmResetCmd(GtlMessageBase):
    def __init__(self, parameters: gapm_reset_cmd = None):

        params = parameters if parameters else gapm_reset_cmd() 

        super().__init__(msg_id=GAPM_MSG_ID.GAPM_RESET_CMD,
                         dst_id=KE_API_ID.TASK_ID_GAPM,
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=1,
                         parameters=params)
                        
        self.parameters = params

class GapmCmpEvt(GtlMessageBase):
    def __init__(self, parameters: gapm_cmp_evt = None):

        params = parameters if parameters else gapm_cmp_evt()

        super().__init__(msg_id=GAPM_MSG_ID.GAPM_CMP_EVT,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=KE_API_ID.TASK_ID_GAPM,
                         par_len=2,
                         parameters=params)

        self.parameters = params

class GapmSetDevConfigCmd(GtlMessageBase):
    def __init__(self, parameters: gapm_set_dev_config_cmd = None):

        params = parameters if parameters else gapm_set_dev_config_cmd()

        super().__init__(msg_id=GAPM_MSG_ID.GAPM_SET_DEV_CONFIG_CMD,
                         dst_id=KE_API_ID.TASK_ID_GAPM,
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=44,
                         parameters=params)

        self.parameters = params

class GapmStartAdvertiseCmd(GtlMessageBase):
    def __init__(self, parameters: gapm_start_advertise_cmd = None):

        params = parameters if parameters else gapm_start_advertise_cmd()

        super().__init__(msg_id=GAPM_MSG_ID.GAPM_START_ADVERTISE_CMD,
                         dst_id=KE_API_ID.TASK_ID_GAPM,
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=82,
                         parameters=params)

        self.parameters = params

class GapmStartConnectionCmd(GtlMessageBase):
    def __init__(self, parameters: gapm_start_connection_cmd = None):

        self.parameters = parameters if parameters else gapm_start_connection_cmd()

        super().__init__(msg_id=GAPM_MSG_ID.GAPM_START_CONNECTION_CMD,
                         dst_id=KE_API_ID.TASK_ID_GAPM,
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=self.par_len, #  if user updates parameters.nb_peers after construction, par_len automatically updated
                         parameters=self.parameters)

    def get_par_len(self):
        print("getting par_len")
        self._par_len = 21+(self.parameters.nb_peers*7)+1
        return self._par_len

    def set_par_len(self, value):
        print("setting par_len")
        self._par_len = value

    par_len = property(get_par_len, set_par_len)

# TODO next message GAPM_RESOLV_ADDR_CMD, GAPM_ADDR_SOLVED_IND  

