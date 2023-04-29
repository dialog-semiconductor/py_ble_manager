from serial_manager.SerialStreamManager import SerialStreamManager
from gtl_messages.gtl_message_base import *
from gtl_messages.gtl_message_gapm import *
import queue
import time


buf = bytes()
if len(buf) > 0 and buf[0] == 1:
    print(buf[0])
