from ..gtl_messages.gtl_message_gapm import GapmDeviceReadyInd, GapmResetCmd, GapmCmpEvt, \
    GapmSetDevConfigCmd, GapmStartAdvertiseCmd, GapmStartConnectionCmd, GapmStartScanCmd, GapmAdvReportInd, \
    GapmCancelCmd, GapmResolvAddrCmd, GapmDevVersionInd, GapmDevBdAddrInd, GapmAddrSolvedInd, GapmUpdateAdvertiseDataCmd, \
    GapmGetDevVersionCmd
from ..gtl_port.gapm_task import GAPM_MSG_ID, gapm_reset_cmd, gapm_cmp_evt, gapm_set_dev_config_cmd, \
    gapm_start_advertise_cmd, gapm_start_connection_cmd, gapm_air_operation, gapm_start_scan_cmd, gapm_adv_report_ind, \
    gapm_cancel_cmd, gapm_resolv_addr_cmd, bd_addr, gap_sec_key, gapm_dev_version_ind, \
    gapm_dev_bdaddr_ind, gapm_addr_solved_ind, gapm_update_advertise_data_cmd, gapm_get_dev_info_cmd, gap_bdaddr


class GapmMessageFactory():

    @staticmethod
    def device_ready_ind(params_buf: bytes):
        return GapmDeviceReadyInd()

    @staticmethod
    def reset_cmd(params_buf: bytes):
        return GapmResetCmd(gapm_reset_cmd.from_buffer_copy(params_buf))

    @staticmethod
    def cmp_evt(params_buf: bytes):
        return GapmCmpEvt(gapm_cmp_evt.from_buffer_copy(params_buf))

    @staticmethod
    def set_dev_config_cmd(params_buf: bytes):
        return GapmSetDevConfigCmd(gapm_set_dev_config_cmd.from_buffer_copy(params_buf))

    @staticmethod
    def start_advertise_cmd(params_buf: bytes):
        return GapmStartAdvertiseCmd(gapm_start_advertise_cmd.from_buffer_copy(params_buf))

    @staticmethod
    def start_connection_cmd(params_buf: bytes):
        # note from_buffer_copy fails due to POINTER in gapm_start_connection_cmd
        parameters = gapm_start_connection_cmd()
        parameters.op = gapm_air_operation.from_buffer_copy(params_buf[0:4])
        parameters.scan_interval = int.from_bytes(params_buf[4:6], "little", signed=False)
        parameters.scan_window = int.from_bytes(params_buf[6:8], "little", signed=False)
        parameters.con_intv_min = int.from_bytes(params_buf[8:10], "little", signed=False)
        parameters.con_intv_max = int.from_bytes(params_buf[10:12], "little", signed=False)
        parameters.con_latency = int.from_bytes(params_buf[12:14], "little", signed=False)
        parameters.superv_to = int.from_bytes(params_buf[14:16], "little", signed=False)
        parameters.ce_len_min = int.from_bytes(params_buf[16:18], "little", signed=False)
        parameters.ce_len_max = int.from_bytes(params_buf[18:20], "little", signed=False)

        # parameters.nb_peers will be set when parameters.peers set
        nb_peers = int.from_bytes(params_buf[20:21], "little", signed=False)

        # peers is list of gap_bdaddr which is 7 bytes
        assert (nb_peers * 7) == len(params_buf[21:-1])  # Check for mismatch in value length and remaining bytes, -1 to account for padding

        parameters.peers = (gap_bdaddr * (len(params_buf[21:-1]) // 7)).from_buffer_copy(params_buf[21:-1])
        return GapmStartConnectionCmd(parameters=parameters)

    @staticmethod
    def start_scan_cmd(params_buf: bytes):
        return GapmStartScanCmd(gapm_start_scan_cmd.from_buffer_copy(params_buf))

    @staticmethod
    def adv_report_ind(params_buf: bytes):
        return GapmAdvReportInd(gapm_adv_report_ind.from_buffer_copy(params_buf))

    @staticmethod
    def cancel_cmd(params_buf: bytes):
        return GapmCancelCmd(gapm_cancel_cmd.from_buffer_copy(params_buf))

    @staticmethod
    def resolv_addr_cmd(params_buf: bytes):
        # note from_buffer_copy fails due to POINTER in gapm_start_connection_cmd
        parameters = gapm_resolv_addr_cmd()
        parameters.operation = int.from_bytes(params_buf[0:1], "little", signed=False)
        # parameters.nb_key will be calculated when irk Array set
        nb_key = int.from_bytes(params_buf[1:2], "little", signed=False)
        parameters.addr = bd_addr.from_buffer_copy(params_buf[2:8])

        # irk is list of gap_sec_key which is 16 bytes
        assert (nb_key * 16) == len(params_buf[8:])  # Check for mismatch in value length and remaining bytes

        parameters.irk = (gap_sec_key * nb_key).from_buffer_copy(params_buf[8:])
        return GapmResolvAddrCmd(parameters=parameters)

    @staticmethod
    def addr_solved_ind(params_buf: bytes):
        return GapmAddrSolvedInd(gapm_addr_solved_ind.from_buffer_copy(params_buf))

    @staticmethod
    def update_advertise_data_cmd(params_buf: bytes):
        # TODO need unit test factory generates GapmUpdateAdvertiseDataCmd correctly
        return GapmUpdateAdvertiseDataCmd(gapm_update_advertise_data_cmd.from_buffer_copy(params_buf))

    @staticmethod
    def get_dev_info_cmd(params_buf: bytes):
        return GapmGetDevVersionCmd(gapm_get_dev_info_cmd.from_buffer_copy(params_buf))

    @staticmethod
    def dev_version_ind(params_buf: bytes):
        return GapmDevVersionInd(gapm_dev_version_ind.from_buffer_copy(params_buf))

    @staticmethod
    def dev_bdaddr_ind(params_buf: bytes):
        return GapmDevBdAddrInd(gapm_dev_bdaddr_ind.from_buffer_copy(params_buf))

    @staticmethod
    def create_message(msg_bytes: bytes):
        msg_id = GAPM_MSG_ID(int.from_bytes(msg_bytes[1:3], "little", signed=False))
        params_buf = msg_bytes[9:]
        handler = GapmMessageFactory.msg_handlers.get(msg_id)
        try:
            if handler:
                return handler(params_buf)
            else:
                raise AssertionError(f"{__class__.__name__}: Message type is unhandled or not valid. msg_id={type(msg_id).__name__}.{msg_id.name}, message={msg_bytes.hex()}")
        except AssertionError as e:
            print(e)
            raise e

    msg_handlers = {
        GAPM_MSG_ID.GAPM_DEVICE_READY_IND: device_ready_ind,
        GAPM_MSG_ID.GAPM_RESET_CMD: reset_cmd,
        GAPM_MSG_ID.GAPM_CMP_EVT: cmp_evt,
        GAPM_MSG_ID.GAPM_SET_DEV_CONFIG_CMD: set_dev_config_cmd,
        GAPM_MSG_ID.GAPM_START_ADVERTISE_CMD: start_advertise_cmd,
        GAPM_MSG_ID.GAPM_START_CONNECTION_CMD: start_connection_cmd,
        GAPM_MSG_ID.GAPM_START_SCAN_CMD: start_scan_cmd,
        GAPM_MSG_ID.GAPM_ADV_REPORT_IND: adv_report_ind,
        GAPM_MSG_ID.GAPM_CANCEL_CMD: cancel_cmd,
        GAPM_MSG_ID.GAPM_RESOLV_ADDR_CMD: resolv_addr_cmd,
        GAPM_MSG_ID.GAPM_ADDR_SOLVED_IND: addr_solved_ind,
        GAPM_MSG_ID.GAPM_UPDATE_ADVERTISE_DATA_CMD: update_advertise_data_cmd,
        GAPM_MSG_ID.GAPM_GET_DEV_INFO_CMD: get_dev_info_cmd,
        GAPM_MSG_ID.GAPM_DEV_VERSION_IND: dev_version_ind,
        GAPM_MSG_ID.GAPM_DEV_BDADDR_IND: dev_bdaddr_ind,
    }
