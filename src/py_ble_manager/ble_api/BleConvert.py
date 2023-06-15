class BleConvert():
    """Utility class providing convenience methods for often used operations

    1000 / 625 = BLE slot
    1000 // 1250 = BLE double slot
    """

    @staticmethod
    def adv_interval_from_ms(intv_ms: int = 0):
        # Convert time in milliseconds to advertising interval value
        return int(intv_ms * 1000 // 625)

    @staticmethod
    def adv_interval_to_ms(intv: int = 0):
        # Convert advertising interval value to time in milliseconds
        return int(intv * 625 // 1000)

    @staticmethod
    def ble_data_length_to_time(octets: int):
        # Convert Receive/Transmit Data Length to Time
        return ((octets + 11 + 3) * 8)

    @staticmethod
    def conn_event_length_from_ms(intv_ms: int = 0):
        # Convert time in milliseconds to connection event length value
        return int(intv_ms * 1000 // 625)

    @staticmethod
    def conn_event_length_to_ms(intv: int = 0):
        # Convert connection event length value to time in milliseconds
        return int(intv * 625 // 100)

    @staticmethod
    def conn_interval_from_ms(intv_ms: int = 0):
        # Convert time in milliseconds to connection interval value
        return int(intv_ms * 100 // 125)

    @staticmethod
    def conn_interval_to_ms(intv: int = 0):
        # Convert connection interval value to time in milliseconds
        return int(intv * 125 // 100)

    @staticmethod
    def scan_interval_from_ms(intv_ms: int = 0):
        # Convert time in milliseconds to scan interval value
        return int(intv_ms * 1000 // 625)

    @staticmethod
    def scan_interval_to_ms(intv: int = 0):
        # Convert scan interval value to time in milliseconds
        return int(intv * 625 // 100)

    @staticmethod
    def scan_window_from_ms(intv_ms: int = 0):
        # Convert time in milliseconds to scan window value
        return int(intv_ms * 1000 // 625)

    @staticmethod
    def scan_window_to_ms(intv: int = 0):
        # Convert scan window value to time in milliseconds
        return int(intv * 625 // 100)

    @staticmethod
    def supervision_timeout_from_ms(intv_ms: int = 0):
        # Convert time in milliseconds to supervision timeout value
        return int(intv_ms // 10)

    @staticmethod
    def supervision_timeout_to_ms(intv: int = 0):
        # Convert supervision timeout value to time in milliseconds
        return int(intv * 10)
