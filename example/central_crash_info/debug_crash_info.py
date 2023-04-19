
from enum import IntEnum, auto


class DCI_LAST_FAULT_HANDLER(IntEnum):
    HARDFAULT = 0
    NMI = auto()
    PLATFORM_RESET = auto()
    NONE = auto()


class DCI_REST_REASON(IntEnum):
    POR = 0
    HW = auto()
    SW = auto()
    WDOG = auto()
    LAST = auto()
    NONE = auto()


class DCI_SVC_COMMAND(IntEnum):
    DCI_SERVICE_COMMAND_NONE = 0
    DCI_SERVICE_COMMAND_GET_ALL_DATA = auto()
    DCI_SERVICE_COMMAND_GET_NUM_RESETS = auto()


class CortexM0StackFrame():
    def __init__(self, data: bytes = None):
        self.r0 = self.reg_from_bytes(data[0:4]) if data else 0
        self.r1 = self.reg_from_bytes(data[4:8]) if data else 0
        self.r2 = self.reg_from_bytes(data[8:12]) if data else 0
        self.r3 = self.reg_from_bytes(data[12:16]) if data else 0
        self.r12 = self.reg_from_bytes(data[16:20]) if data else 0
        self.LR = self.reg_from_bytes(data[20:24]) if data else 0
        self.return_address = self.reg_from_bytes(data[24:28]) if data else 0
        self.xPSR = self.reg_from_bytes(data[28:32]) if data else 0

    def __repr__(self):
        return_string = f"{type(self).__name__}(r0=0x{self.r0:08x}, r1=0x{self.r1:08x}, " + \
                        f"r2=0x{self.r2:08x}, r3=0x{self.r3:08x}, " + \
                        f"r12=0x{self.r12:08x}, LR=0x{self.LR:08x}, " + \
                        f"return_address=0x{self.return_address:08x}, xPSR=0x{self.xPSR:08x})"

        return return_string

    def reg_from_bytes(self, data: bytes):
        return int.from_bytes(data, 'little')


class DciData():
    def __init__(self):
        self.last_reset_reason: DCI_REST_REASON = DCI_REST_REASON.NONE
        self.num_resets: int = 0
        self.fault_data: list[DciFaultInfo] = []

    def __repr__(self):
        return_string = f"{type(self).__name__}(last_reset_reason={self.last_reset_reason}, num_resets={self.num_resets}, " + \
                        f"fault_data={self.fault_data}"

        return return_string


class DciFaultInfo():
    def __init__(self):
        self.data_valid: bool = False
        self.epoch: int = 0
        self.fault_handler: DCI_LAST_FAULT_HANDLER = DCI_LAST_FAULT_HANDLER.NONE
        self.stack_frame = CortexM0StackFrame()
        self.num_of_call_vals: int = 0
        self.call_trace: list[int] = []

    def __repr__(self):
        return_string = f"{type(self).__name__}(data_valid={self.data_valid}, epoch={self.epoch}, " + \
                        f"fault_handler={self.fault_handler.name}, stack_frame={self.stack_frame}, " + \
                        f"num_of_call_vals={self.num_of_call_vals}, call_trace="
        for i in range(self.num_of_call_vals):
            return_string += f"0x{self.call_trace[i]:08x}, "
        return_string = return_string[:-2]
        return_string += ")"
        return return_string


class ResetData():
    def __init__(self):
        self.command = DCI_SVC_COMMAND.DCI_SERVICE_COMMAND_NONE
        self.len = 0
        self.data = bytes()
