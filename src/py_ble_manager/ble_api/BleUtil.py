from ..ble_api.BleAtt import AttUuid, ATT_UUID_TYPE
from ..ble_api.BleCommon import BdAddress, ADDR_TYPE
from ..ble_api.BleGap import BleAdvData, GAP_DATA_TYPE


class BleUtils():
    """Utility class providing convenience methods for often used operations
    """

    @staticmethod
    def bd_addr_to_str(bd: BdAddress) -> str:
        """Convert BD address to string of form "48:23:35:00:1b:53,P", where P is a public address and R is a random address

        :param bd: BD address to convert to string
        :type bd: BdAddress
        :return: string of the form "48:23:35:00:1b:53,P"
        :rtype: str
        """

        return_string = ""
        for byte in bd.addr:
            byte_string = str(hex(byte))[2:]
            if len(byte_string) == 1:  # Add a leading 0
                byte_string = "0" + byte_string
            return_string = byte_string + ":" + return_string
        return_string = return_string[:-1]
        return_string += ",P" if bd.addr_type == ADDR_TYPE.PUBLIC_ADDRESS else ",R"
        return return_string

    @staticmethod
    def parse_adv_data_from_bytes(data: bytes) -> list[BleAdvData]:
        """"Generate AD structures from bytes

        :param data: advertising data
        :type data: bytes
        :return: list of AD structures
        :rtype: list[BleAdvData]
        """
        data_ptr = 0
        adv_data_structs: list[BleAdvData] = []
        data_len = len(data)
        if data_len > 0:
            while data_ptr < 31 and data_ptr < data_len:
                length = data[data_ptr]
                struct = BleAdvData(type=data[data_ptr + 1])

                if length == 0 or struct.type == GAP_DATA_TYPE.GAP_DATA_TYPE_NONE:
                    break

                data_ptr += 2
                struct.data = data[data_ptr:(data_ptr + length - 1)]  # -1 as calc includes AD Type
                data_ptr += struct.len - 1  # -1 as calc includes AD Type
                adv_data_structs.append(struct)

        return adv_data_structs

    @staticmethod
    def str_to_bd_addr(bd_addr_str: str) -> BdAddress:
        """Convert a string to a BD address

    .. note:
        Expect string of form "48:23:35:00:1b:53,P"
        where 48:23:35:00:1b:53 is the address
        and last letter indiactes the address type:
            P indiactes a public address
            R indicates a random address

        :param bd_addr_str: string to convert
        :type bd_addr_str: str
        :return: BD address corresponding to the input string
        :rtype: BdAddress
        """

        periph_addr_str, addr_type_str = bd_addr_str.split(',')
        addr_type = ADDR_TYPE.PUBLIC_ADDRESS if addr_type_str == 'P' else ADDR_TYPE.PRIVATE_ADDRESS
        periph_addr_str_stripped = periph_addr_str.replace(":", "")
        bd_addr_list = [int(periph_addr_str_stripped[idx:idx + 2], 16) for idx in range(0, len(periph_addr_str_stripped), 2)]
        bd_addr_list.reverse()  # mcu is little endian
        return BdAddress(addr_type, bytes(bd_addr_list))

    @staticmethod
    def uuid_from_str(uuid_str: str) -> AttUuid:
        """Convert a string to a AttUuid

    ..note:
        Expect UUID of form: 21ce31fc-da27-11ed-afa1-0242ac120002

        :param uuid_str: string to convert
        :type uuid_str: str
        :return: AttUuid corresponding to the input string
        :rtype: AttUuid
        """
        uuid_str = uuid_str.replace("-", "")
        uuid_list = [int(uuid_str[idx:idx + 2], 16) for idx in range(0, len(uuid_str), 2)]
        uuid_list.reverse()  # mcu is little endian
        return AttUuid(bytes(uuid_list))

    @staticmethod
    def uuid_to_str(uuid: AttUuid) -> str:
        """Convert a AttUuid to a string

        :param uuid: uuid to convert
        :type uuid: AttUuid
        :return: string corresponding to the input AttUuid
        :rtype: str
        """
        data = uuid.uuid
        return_string = ""
        if uuid.type == ATT_UUID_TYPE.ATT_UUID_128:
            for byte in data:
                byte_string = str(hex(byte))[2:]
                if len(byte_string) == 1:  # Add a leading 0
                    byte_string = "0" + byte_string
                return_string = byte_string + return_string
        else:
            for i in range(1, -1, -1):
                byte_string = str(hex(data[i]))[2:]
                if len(byte_string) == 1:
                    byte_string = "0" + byte_string
                return_string += byte_string

        return return_string
