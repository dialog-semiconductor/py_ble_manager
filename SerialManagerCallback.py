import asyncio
import serial_asyncio
from gtl_messages import *

# TODO GAPM message handling should be in a GapManager class

class SerialManagerCallback(asyncio.Protocol):

    def default_handler(self, message):
        print("default handler")

    def handle_gapm_device_ready_ind(self, message):      
        print("Received GapmDeviceReadyInd()", message.msg_id)

        #TODO is this appropriate, should there be some async method? 
        self.transport.serial.write(GapmResetCmd(gapm_reset_cmd(GAPM_OPERATION.GAPM_RESET)).to_bytes())

    def handle_gapm_cmp_evt(self,message):
        print("Received GapmCmpEvt()", message.msg_id)
        self.handle_gapm_reset_completion(message)

    def handle_gapm_reset_completion(self, message: GapmCmpEvt):
        print("handle_gapm_reset_completion", message.msg_id)
        
        if(message.parameters.operation == GAPM_OPERATION.GAPM_RESET):
            self.default_gapm_reset_callback()
        elif(message.parameters.operation == GAPM_OPERATION.GAPM_SET_DEV_CONFIG):
            print("handle_gapm_reset_completion GAPM_SET_DEV_CONFIG")
        

    def default_gapm_reset_callback(self):

        print("default_gapm_reset_callback")
        dev_config = GapmSetDevConfigCmd()
        dev_config.parameters.operation = GAPM_OPERATION.GAPM_SET_DEV_CONFIG
        dev_config.parameters.role = GAP_ROLE.GAP_ROLE_PERIPHERAL
        dev_config.parameters.att_cfg = 0x20 # TODO setup GAPM_MASK_ATT_SVC_CNG_EN
        dev_config.parameters.max_mtu = 512 
        dev_config.parameters.max_txoctets = 251
        dev_config.parameters.max_txtime = 2120

        # TODO 
        self.transport.serial.write(dev_config.to_bytes())

    func_table = {
        GAPM_MSG_ID.GAPM_CMP_EVT: handle_gapm_cmp_evt,
        GAPM_MSG_ID.GAPM_DEVICE_READY_IND: handle_gapm_device_ready_ind,
        GAPM_MSG_ID.GAPM_CANCEL_CMD: default_handler,
    }

    def run(self, message: AbstractGtlMessage):
        #TODO be careful, not clear if you are calling instance func or class method
        return self.func_table[message.msg_id](self, message)

    #def decode_gapm(self, message):
    #    if(message.msg_id == )

    def decode(self, byte_string):

        print("Decode")

        # Assuming all data at once
        #message = AbstractGtlMessage(msg_id = GAPM_MSG_ID(int.from_bytes(byte_string[1:3], "little",signed=False)),
        #                         dst_id=KE_API_ID(int.from_bytes(byte_string[3:5], "little",signed=False)),
        #                         src_id=KE_API_ID(int.from_bytes(byte_string[5:7], "little",signed=False)),
        #                         par_len=int.from_bytes(byte_string[7:9], "little",signed=False))

        # TODO define for 9
        if(len(byte_string) >= 9):
            # Decode the message
            message = GtlMessageFactory().create_message(byte_string)
            print("Message received, handling i")
            # Handle it

            # TODO what is message is not in the table? 
            self.run(message)
            
        else:
            print("Received: ", byte_string)

    
    def connection_made(self, transport):
        #TODO this belongs in a constructure
        #self.gapm_reset_complete_callack = None

        self.transport = transport
        print('port opened', transport)
        transport.serial.rts = False  # You can manipulate Serial object via transport
        transport.write(b'Hello, World!\n')  # Write serial data via transport

    def data_received(self, data):
        print('data received', repr(data))
        
        #TODO  Assumption is whole message received at once, likely it will not be
        self.decode(data)

        if b'\n' in data:
            self.transport.close()

    def connection_lost(self, exc):
        print('port closed')
        self.transport.loop.stop()

    def pause_writing(self):
        print('pause writing')
        print(self.transport.get_write_buffer_size())

    def resume_writing(self):
        print(self.transport.get_write_buffer_size())
        print('resume writing')

loop = asyncio.get_event_loop()
coro = serial_asyncio.create_serial_connection(loop, SerialManagerCallback, 'COM13', baudrate=115200)
transport, protocol = loop.run_until_complete(coro)
loop.run_forever()
loop.close()