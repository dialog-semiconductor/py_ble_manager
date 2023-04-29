import concurrent.futures
import queue
import threading
import serial

from gtl_messages.gtl_message_base import GTL_INITIATOR


class SerialStreamManager():

    def __init__(self, com_port: str, tx_queue: queue.Queue[bytes], rx_queue: queue.Queue[bytes], shutdown_event: threading.Event) -> None:
        self._tx_queue: queue.Queue[bytes] = tx_queue
        self._rx_queue: queue.Queue[bytes] = rx_queue
        self._com_port: str = com_port
        self._shutdown_event = shutdown_event

    def _serial_task(self):

        executor = concurrent.futures.ThreadPoolExecutor(max_workers=2, thread_name_prefix='SerialStream')
        # create task to wait for data on the tx queue (e.g. data from the BLE adapter)
        self._serial_tx_task = executor.submit(self._tx_queue_get)
        # create task to wait for data on the serial port
        self._serial_rx_task = executor.submit(self._receive)

        pending = [self._serial_tx_task, self._serial_rx_task]

        while True:

            if self._shutdown_event.is_set():
                executor.shutdown(wait=False, cancel_futures=True)
                break

            done, pending = concurrent.futures.wait(pending, timeout=1, return_when=concurrent.futures.FIRST_COMPLETED)

            for task in done:
                if task is self._serial_tx_task:
                    # We have received data on the Tx queue, send it and restart the task
                    # TODO need to rethink waiting here. The _receive task should never be
                    # be blocked for a long time or we will miss data
                    if task.result():
                        self._send(task.result())

                    self._serial_tx_task = executor.submit(self._tx_queue_get)
                    pending.add(self._serial_tx_task)

                elif task is self._serial_rx_task:
                    # This is from serial Rx queue
                    if task.result():
                        self._process_received_data(task.result())

                    self._serial_rx_task = executor.submit(self._receive)
                    pending.add(self._serial_rx_task)

    def _process_received_data(self, buffer: bytes):
        if buffer:
            self._rx_queue.put_nowait(buffer)

    def _receive(self):
        buffer = bytes()
        while len(buffer) < 1:
            if self._shutdown_event.is_set():
                break
            # print("waiting for gtl initiator")
            buffer = self._serial_port.read(1)
            if len(buffer) > 0 and (buffer[0] == GTL_INITIATOR):
                # Get msg_id, dst_id, src_id, par_len. Use par_len to read rest of message
                while len(buffer) < (1 + 8):
                    if self._shutdown_event.is_set():
                        break
                    # print("waiting for gtl header")
                    buffer += self._serial_port.read(8)
                    if len(buffer) >= (1 + 8):
                        par_len = int.from_bytes(buffer[7:9], "little", signed=False)
                        if (par_len != 0):
                            while len(buffer) < (1 + 8 + par_len):
                                if self._shutdown_event.is_set():
                                    break
                                # print("waiting for gtl message")
                                buffer += self._serial_port.read(par_len)
            #else:
            # print(f"Returning buffer: {buffer}")
            return buffer

    def _send(self, message: bytes):
        if message:
            # print(f"Sending: {message}")
            self._serial_port.write(message)
            self._serial_port.flush()  # TODO is this needed?

    def _tx_queue_get(self) -> bytes:
        item = None
        while item is None:
            try:
                if self._shutdown_event.is_set():
                    break
                item = self._tx_queue.get(timeout=1)
            except queue.Empty:
                pass
        return item

    def init(self):
        self._task = threading.Thread(target=self._serial_task)
        self._task.start()

    def open_serial_port(self):
        # try:
        self._serial_port = serial.Serial(self._com_port, baudrate=115200, timeout=1)
        # except :
        #    print(f"{type(self)} failed to open {self._com_port}")
