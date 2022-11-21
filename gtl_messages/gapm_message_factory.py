from ctypes import *
from .gtl_message_gapm import *


class GapmMessageFactory():
    
    @staticmethod
    def create_message(msg_bytes):
        assert(len(msg_bytes) >= 9)

        print(len(msg_bytes))
        #TODO figure out what is wrong with this assert
        assert(int.from_bytes(msg_bytes[:1], "little",signed=False) == GTL_INITIATOR)

        # First byte is GTL header
        msg_id = GAPM_MSG_ID(int.from_bytes(msg_bytes[1:3], "little",signed=False))
       
        par_len=int.from_bytes(msg_bytes[7:9], "little",signed=False)
        params_buf = msg_bytes[9:]

        # TODO do we need these? Verify them?
        #dst_id=KE_API_ID(int.from_bytes(msg_bytes[3:5], "little",signed=False))
        #src_id=KE_API_ID(int.from_bytes(msg_bytes[5:7], "little",signed=False))

        #TODO for each case add a check to ensure params_buf not too long for parameters variablee
        try:
            if msg_id == GAPM_MSG_ID.GAPM_DEVICE_READY_IND:
                print("Creating GapmDeviceReadyInd")
                return GapmDeviceReadyInd()

            elif msg_id == GAPM_MSG_ID.GAPM_RESET_CMD:
                return GapmResetCmd(gapm_reset_cmd.from_buffer_copy(params_buf))

            elif msg_id == GAPM_MSG_ID.GAPM_CMP_EVT:
                print("Creating GapmCmpEvt")
                return GapmCmpEvt(gapm_cmp_evt.from_buffer_copy(params_buf))

            elif GAPM_MSG_ID.GAPM_SET_DEV_CONFIG_CMD:
                return GapmSetDevConfigCmd(gapm_set_dev_config_cmd.from_buffer_copy(params_buf))

            elif msg_id==GAPM_MSG_ID.GAPM_START_ADVERTISE_CMD:
                return GapmStartAdvertiseCmd(gapm_start_advertise_cmd.from_buffer_copy(params_buf))

            raise AssertionError("GapmMessageFactory: Message type is handled or not valid")
        except AssertionError as e:
            print("Exception")
            print(e)
