from ..ble_api.BleAtt import AttUuid, ATT_UUID_TYPE
from ..ble_api.BleCommon import BdAddress, BLE_ADDR_TYPE


class BleUtils():

    @staticmethod
    def bd_addr_to_str(bd: BdAddress) -> str:
        return_string = ""
        for byte in bd.addr:
            byte_string = str(hex(byte))[2:]
            if len(byte_string) == 1:  # Add a leading 0
                byte_string = "0" + byte_string
            return_string = byte_string + ":" + return_string
        return_string = return_string[:-1]
        return_string += ",P" if bd.addr_type == BLE_ADDR_TYPE.PUBLIC_ADDRESS else ",R"
        return return_string

    @staticmethod
    def str_to_bd_addr(bd_addr_str: str) -> BdAddress:
        '''
        Expect string of form "48:23:35:00:1b:53,P"
        where 48:23:35:00:1b:53 is the address
        and last letter indiactes the address type:
            P indiactes a BLE_ADDR_TYPE.PUBLIC_ADDRESS
            R indicates a BLE_ADDR_TYPE.PRIVATE_ADDRESS
        '''
        periph_addr_str, addr_type_str = bd_addr_str.split(',')
        addr_type = BLE_ADDR_TYPE.PUBLIC_ADDRESS if addr_type_str == 'P' else BLE_ADDR_TYPE.PRIVATE_ADDRESS
        periph_addr_str_stripped = periph_addr_str.replace(":", "")
        bd_addr_list = [int(periph_addr_str_stripped[idx:idx + 2], 16) for idx in range(0, len(periph_addr_str_stripped), 2)]
        bd_addr_list.reverse()  # mcu is little endian
        return BdAddress(addr_type, bytes(bd_addr_list))

    @staticmethod
    def uuid_from_str(uuid_str: str) -> AttUuid:
        '''
        Expect UUID of form: 21ce31fc-da27-11ed-afa1-0242ac120002
        '''
        uuid_str = uuid_str.replace("-", "")
        uuid_list = [int(uuid_str[idx:idx + 2], 16) for idx in range(0, len(uuid_str), 2)]
        uuid_list.reverse()  # mcu is little endian
        return AttUuid(bytes(uuid_list))

    @staticmethod
    def uuid_to_str(uuid: AttUuid) -> str:
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
