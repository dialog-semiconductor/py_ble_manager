from serial_manager.SerialStreamManager import SerialStreamManager
from gtl_messages.gtl_message_base import *
from gtl_messages.gtl_message_gapm import *
import queue
import time

com_port = "COM54"
tx_queue = queue.Queue()
rx_queue = queue.Queue()
print("Opening serial stream manager")
stream = SerialStreamManager(com_port, tx_queue, rx_queue)
stream.open_serial_port()
stream.init()

print("Put item on q")
tx_queue.put_nowait(GapmResetCmd().to_bytes())

count = 0
while True:
    count += 1
    print(f"Running {count}")
    time.sleep(1)
