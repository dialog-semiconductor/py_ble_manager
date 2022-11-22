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

        parms = parameters if parameters else gapm_reset_cmd() 

        super().__init__(msg_id=GAPM_MSG_ID.GAPM_RESET_CMD,
                         dst_id=KE_API_ID.TASK_ID_GAPM,
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=1,
                         parameters=parms)
                        
        self.parameters = parms

class GapmCmpEvt(GtlMessageBase):
    def __init__(self, parameters: gapm_cmp_evt = None):

        parms = parameters if parameters else gapm_cmp_evt()

        super().__init__(msg_id=GAPM_MSG_ID.GAPM_CMP_EVT,
                         dst_id=KE_API_ID.TASK_ID_GTL,
                         src_id=KE_API_ID.TASK_ID_GAPM,
                         par_len=2,
                         parameters=parms)

        self.parameters = parms

class GapmSetDevConfigCmd(GtlMessageBase):
    def __init__(self, parameters: gapm_set_dev_config_cmd = None):

        parms = parameters if parameters else gapm_set_dev_config_cmd()

        super().__init__(msg_id=GAPM_MSG_ID.GAPM_SET_DEV_CONFIG_CMD,
                         dst_id=KE_API_ID.TASK_ID_GAPM,
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=44,
                         parameters=parms)

        self.parameters = parms

class GapmStartAdvertiseCmd(GtlMessageBase):
    def __init__(self, parameters: gapm_start_advertise_cmd = None):

        parms = parameters if parameters else gapm_start_advertise_cmd()

        super().__init__(msg_id=GAPM_MSG_ID.GAPM_START_ADVERTISE_CMD,
                         dst_id=KE_API_ID.TASK_ID_GAPM,
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=82,
                         parameters=parms)

        self.parameters = parms

# TODO need unit test case
class GapmStartConnectionCmd(GtlMessageBase):
    def __init__(self, parameters: gapm_start_connection_cmd = None):

        parms = parameters if parameters else gapm_start_connection_cmd()

        super().__init__(msg_id=GAPM_MSG_ID.GAPM_START_ADVERTISE_CMD,
                         dst_id=KE_API_ID.TASK_ID_GAPM,
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=21+parameters.nb_peers*7,
                         parameters=parms)

        self.parameters = parms




