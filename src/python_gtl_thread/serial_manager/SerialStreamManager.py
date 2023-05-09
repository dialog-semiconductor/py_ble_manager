import concurrent.futures
import queue
import threading
import serial

from ..gtl_messages.gtl_message_base import GTL_INITIATOR


class SerialStreamManager():

    def __init__(self, com_port: str, tx_queue: queue.Queue[bytes], rx_queue: queue.Queue[bytes]) -> None:
        self._tx_queue: queue.Queue[bytes] = tx_queue
        self._rx_queue: queue.Queue[bytes] = rx_queue
        self._com_port: str = com_port

    def _process_received_data(self, buffer: bytes):
        if buffer:
            self._rx_queue.put_nowait(buffer)

    def _receive(self):
        buffer = bytes()
        buffer = self._serial_port.read(1)
        if (buffer[0] == GTL_INITIATOR):
            # Get msg_id, dst_id, src_id, par_len. Use par_len to read rest of message
            buffer += self._serial_port.read(8)
            par_len = int.from_bytes(buffer[7:9], "little", signed=False)
            if (par_len != 0):
                buffer += self._serial_port.read(par_len)
        else:
            # print("Received some garbage")
            pass
        return buffer
    
    def _receive_task(self):
        while True:
            serial_message = self._receive()
            self._process_received_data(serial_message)
    
    def _send(self, message: bytes):
        if message:
            # print(f"Sending: {message}")
            self._serial_port.write(message)
            self._serial_port.flush()  # TODO is this needed?

    def _tx_queue_get(self) -> bytes:
        return self._tx_queue.get()
    
    def _tx_queue_task(self):
        while True:
            serial_message = self._tx_queue_get()
            self._send(serial_message)

    def init(self):
        self._tx_task = threading.Thread(target=self._tx_queue_task)
        self._tx_task.daemon = True
        self._tx_task.start()

        self._rx_task = threading.Thread(target=self._receive_task)
        self._rx_task.daemon = True
        self._rx_task.start()

    def open_serial_port(self):
        # try:
        # TODO timeout opening port
        self._serial_port = serial.Serial(self._com_port, baudrate=115200)

        # except :
        #    print(f"{type(self)} failed to open {self._com_port}")
