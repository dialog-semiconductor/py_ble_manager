from ..gtl_messages.gtl_message_gapm import GapmDeviceReadyInd, GapmCmpEvt, \
    GapmStartAdvertiseCmd, GapmAdvReportInd, GapmDevVersionInd, GapmDevBdAddrInd, \
    GapmAddrSolvedInd
from ..gtl_port.gapm_task import GAPM_MSG_ID, gapm_cmp_evt, \
    gapm_start_advertise_cmd, gapm_adv_report_ind, gapm_dev_version_ind, \
    gapm_dev_bdaddr_ind, gapm_addr_solved_ind


class GapmMessageFactory():

    @staticmethod
    def create_message(msg_bytes: bytes):
        msg_id = GAPM_MSG_ID(int.from_bytes(msg_bytes[1:3], "little", signed=False))
        params_buf = msg_bytes[9:]

        try:
            if msg_id == GAPM_MSG_ID.GAPM_DEVICE_READY_IND:
                return GapmDeviceReadyInd()

            elif msg_id == GAPM_MSG_ID.GAPM_CMP_EVT:
                return GapmCmpEvt(gapm_cmp_evt.from_buffer_copy(params_buf))

            elif msg_id == GAPM_MSG_ID.GAPM_START_ADVERTISE_CMD:
                return GapmStartAdvertiseCmd(gapm_start_advertise_cmd.from_buffer_copy(params_buf))

            elif msg_id == GAPM_MSG_ID.GAPM_ADV_REPORT_IND:
                return GapmAdvReportInd(gapm_adv_report_ind.from_buffer_copy(params_buf))

            elif msg_id == GAPM_MSG_ID.GAPM_DEV_VERSION_IND:
                return GapmDevVersionInd(gapm_dev_version_ind.from_buffer_copy(params_buf))

            elif msg_id == GAPM_MSG_ID.GAPM_DEV_BDADDR_IND:
                return GapmDevBdAddrInd(gapm_dev_bdaddr_ind.from_buffer_copy(params_buf))

            elif msg_id == GAPM_MSG_ID.GAPM_ADDR_SOLVED_IND:
                return GapmAddrSolvedInd(gapm_addr_solved_ind.from_buffer_copy(params_buf))

            else:
                raise AssertionError(f"GapmMessageFactory: Message type is unhandled or not valid. message={msg_bytes.hex()}")
        except AssertionError as e:
            print(e)
            raise e
