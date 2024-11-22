# gtl_sniffer.py

This is a utility script for sniffing serial GTL communication between a host and DA14xxx BLE device. You can sniff communication from the host to the BLE device,
from the BLE device to the host, or both.

It requires at least one USB-to-UART converter, two if you are sniffing Tx and Rx simultaneously. The Rx pin of your USB-to-UART converter(s) should be connected
to the Host-BLE pin you are intereseted in sniffing:

Host   --  Tx -- > BLE: Connect USB-to-UART Rx pin to the Host Tx pin to sniff GTL messages destined for the BLE device. \
Host < -- Rx  --   BLE: Connect USB-to-UART Rx pin to the Host Rx pin to sniff GTL messages destined for the Host.

You can run it with:

`python gtl_sniffer.py <com_port_1> <baud_rate> <--com_port_2> <--log_file>`

`<com_port_1>` is the COM port associated with your (first) USB-to-UART converter.

`<baud_rate>` is the baud rate of serial communication.

`<--com_port_2>` is the COM port associated with your second USB-to-UART converter if you are sniffing both Tx and Rx.

`<--log_file>` is the path to a log file to log GTL communication to. If no log file is provided, information will be logged to the terminal.

## Running *with* a log file

Once runninng, a message will print to the terminal to indicate sniffing has started:

![terminal](assets/terminal_started.png)

You should see messages printed to the terminal once GTL communication is started:

![terminal](assets/terminal_running.png)

## Running *without* a log file

Once runninng, a message will print to the terminal to indicate sniffing has started:

![terminal](assets/log_started.png)

You should see the messages in your log file once GTL communication is started:

![log_file](assets/log_running.png)
