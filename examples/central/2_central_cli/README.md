# central_cli

This example provides a command line interface to control a BLE central deivce. It supports scanning, connecting, reading, writing, etc.

You can run it with:

`python central_cli.py <com_port>`

where `<com_port>` is the COM port associated with your development kit. Note, in the case of the Pro development kit there will be two COM ports associated with your development kit. You should use the lower of the two.

Once running, you will be provided with a prompt:

![terminal](assets/terminal.png)

Here you can enter various commands. The prompt will provide auto-complete for commands available:

![autocomplete](assets/autocomplete.png)

For example, to scan for peripheral devices the `GAPSCAN` command can be used. When a command is entered, a response will be immediately returned indicating if the command was processed correctly:

![command_response](assets/command_response.png)

Once the command is processed, data from the BLE interaction will be returned. In the case of the `GAPSCAN` command, advertising packets recevied from any peripheral devices are printed to the terminal:

![scan](assets/scan.png)

## Command Usage

### SCAN

Scan for peripheral devices.

`SCAN`

Advertisement data will print to the terminal. Once the scan is finished, a message indicating the scan is complete will be printed to the terminal:

![scan](assets/scan.png)

### SCAN_CANCEL

Cancel a scan for peripheral devices.

`SCAN_CANCEL`

Once the scan is canceled, a message indicating the scan is canceled will be printed to the terminal:

![scan_cancel](assets/scan_cancel.png)

### CONNECT

Connect to a peripheral.

`CONNECT <address>`

For example:

`CONNECT 48:23:35:00:1b:53,P`

When the procedure is complete, a message indicationg so will be printed to the terminal:

![connect](assets/connect.png)

### CONNECT_CANCEL

Cancel connecting to a peripheral.

`CONNECT_CANCEL`

For example:

`CONNECT_CANCEL`

When the procedure is complete, a message indicationg so will be printed to the terminal:

![connect_cancel](assets/connect_cancel.png)

### BROWSE

Browse a peripheral's attributes.

`BROWSE <connection_index>`

For example, to browse the attributes of the peripheral at connection index 0:

`BROWSE 0`

When the procedure is complete, a message indicationg so will be printed to the terminal:

![browse](assets/browse.png)

### DISCONNECT

`DISCONNECT <connection_index>`

For example, to disconnect from the peripheral at connection index 0:

`DISCONNECT 0`

When the procedure is complete, a message indicationg you have disconnected will be printed to the terminal:

![disconnect](assets/disconnect.png)

You may also pass a reason for diconnectiong. The reason should correspond to a `BLE_HCI_ERROR`:

`DISCONNECT <connection_index> <reason>`

For example, to disconnect from a peripheral at connection index 0 with the reason `BLE_HCI_ERROR_REMOTE_USER_TERM_CON`:

`DISCONNECT 0 19`

### PAIR

`PAIR <connection_index> <bond>`

For example, to pair to the peripheral at connection index 0:

`PAIR 0 0`

When the procedure is complete, a message indicationg so will be printed to the terminal:

![pair](assets/pair.png)

### READ

`READ <connection_index> <handle>`

For example, to read handle 13 from the peripheral at connection index 0:

`READ 0 13`

When the procedure is complete, a message indicationg so will be printed to the terminal:

![read](assets/read.png)

Note the data returned is little endian.

Note the Characteristic handle returned by the `BROWSE` command is that of the characteristic declaration. To read the value of the characteristic, add 1 to the handle returned by the `BROWSE` command. For example, if the `BROWSE` command identifies a characteristic handle as 12:

![browse](assets/browse_char_handle.png)

You would use handle 13 to read the characteristic value.

### WRITE

`WRITE <connection_index> <handle> <data>`

For example, to write 0x3412 to handle 13 of the peripheral at connection index 0:

`WRITE 0 13 1234`

Note the data should be written little endian. When the procedure is complete, a message indicationg so will be printed to the terminal:

![write](assets/write.png)

Again note the Characteristic handle returned by the `BROWSE` command is that of the characteristic declaration. To write the value of the characteristic, add 1 to the handle returned by the `BROWSE` command. For example, if the `BROWSE` command identifies a characteristic handle as 12:

![browse](assets/browse_char_handle.png)

You would use handle 13 to write the characteristic value.

### WRITE_NO_RESP

`WRITE_NO_RESP <connection_index> <handle> <signed> <data>`

For example, to perform a signed write or 0x3412 to handle 13 of the peripheral at connection index 0:

`WRITE_NO_RESP 0 13 1 1234`

### SET_CONN_PARAM

`SET_CONN_PARAM <connection_index> <interval_min> <interval_max> <slave_latency> <sup_timeout>`

For example:

`SET_CONN_PARAM 0 50 70 0 420`

When the procedure is complete, a message indicationg so will be printed to the terminal:

![setconnparam](assets/setconnparams.png)

### PASSKEY_ENTRY

`PASSKEY_ENTRY <connection_index> <accept> <passkey>`

For example, to accept pairing at connection index 0 with passkey 945553:

`PASSKEY_ENTRY 0 1 945553`

Note the passkey to enter is presented on the display of the Peripheral.

When the procedure is complete, a message indicationg so will be printed to the terminal:

![passkeyentry](assets/passkeyentry.png)

### YES_NO_ENTRY

`YES_NO_ENTRY <connection_index> <accept>`

For example, to accept a secure connection at connection index 0:

`YESNOENTRY 0 1`

When the procedure is complete, a message indicationg so will be printed to the terminal:

![yesnoentry](assets/yesnoentry.png)
