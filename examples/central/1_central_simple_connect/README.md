# central_simple_connect

This example demonstrates creating/initializing a BleCentral object, connecting to and disconnecting from a peripheral.

You can run it with:

`python central_simple_connect.py <com_port> <peripheral_addr> <timeout_s>`

`<com_port>` is the COM port associated with your development kit. Note, in the case of the Pro development kit there will be two COM ports associated with your development kit. You should use the lower of the two.

`<peripheral_addr>` is the address of the peripheral you want to connect to. \
The address should be of the form 48:23:35:00:1b:53,P: \
&emsp; where 48:23:35:00:1b:53 is the BLE device address and last letter indicates the address type: \
&emsp;&emsp; P indicates a public address \
&emsp;&emsp; R indicates a random address

`<timeout_s>` is the length of time (in seconds) to wait for a connection to be established before cancelling the connection.

Once running, you should see messages indicating you have connected to your peripheral:

![connection](assets/connection.png)

About 3 seconds after a successful connection, you should see a message indicating you have disconnected from your peripheral and the application will exit:

![disconnection](assets/disconnection.png)

If a connection is not established to the peripheral before the timeout, the connection will be cancelled and the application will exit:

![timeout](assets/timeout.png)
