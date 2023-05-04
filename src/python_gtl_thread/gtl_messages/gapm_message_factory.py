from ..gtl_messages.gtl_message_base import GTL_INITIATOR
from ..gtl_messages.gtl_message_gapm import GapmDeviceReadyInd, GapmCmpEvt, \
    GapmStartAdvertiseCmd, GapmAdvReportInd
from ..gtl_port.gapm_task import GAPM_MSG_ID, gapm_cmp_evt, \
    gapm_start_advertise_cmd, gapm_adv_report_ind


class GapmMessageFactory():

    @staticmethod
    def create_message(msg_bytes: bytes):

        # TODO this section will be same for each factory except for the msg_id enum, dont rewrite it everytime
        assert (len(msg_bytes) >= 9)
        assert (int.from_bytes(msg_bytes[:1], "little", signed=False) == GTL_INITIATOR)

        # First byte is GTL header
        msg_id = GAPM_MSG_ID(int.from_bytes(msg_bytes[1:3], "little", signed=False))

        # par_len=int.from_bytes(msg_bytes[7:9], "little", signed=False)
        params_buf = msg_bytes[9:]

        # TODO do we need these? Verify them?
        # dst_id=KE_API_ID(int.from_bytes(msg_bytes[3:5], "little",signed=False))
        # src_id=KE_API_ID(int.from_bytes(msg_bytes[5:7], "little",signed=False))

        # TODO for each case add a check to ensure params_buf not too long for parameters variablee
        try:
            if msg_id == GAPM_MSG_ID.GAPM_DEVICE_READY_IND:
                return GapmDeviceReadyInd()

            # TODO remove? Right now these are handlng messages rx'd from 531, would we ever want to
            # convert messages destined for the 531?
            # elif msg_id == GAPM_MSG_ID.GAPM_RESET_CMD:
            #     return GapmResetCmd(gapm_reset_cmd.from_buffer_copy(params_buf))

            elif msg_id == GAPM_MSG_ID.GAPM_CMP_EVT:
                return GapmCmpEvt(gapm_cmp_evt.from_buffer_copy(params_buf))

            # elif msg_id == GAPM_MSG_ID.GAPM_SET_DEV_CONFIG_CMD:
            #    return GapmSetDevConfigCmd(gapm_set_dev_config_cmd.from_buffer_copy(params_buf))

            elif msg_id == GAPM_MSG_ID.GAPM_START_ADVERTISE_CMD:
                return GapmStartAdvertiseCmd(gapm_start_advertise_cmd.from_buffer_copy(params_buf))

            elif msg_id == GAPM_MSG_ID.GAPM_ADV_REPORT_IND:
                return GapmAdvReportInd(gapm_adv_report_ind.from_buffer_copy(params_buf))

            else:
                raise AssertionError(f"GapmMessageFactory: Message type is unhandled or not valid. message={msg_bytes.hex()}")
        except AssertionError as e:
            print(e)
            raise e
