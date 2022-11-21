import asyncio
import serial_asyncio
from gtl_messages import *

# TODO GAPM message handling should be in a GapManager class

class SerialManagerStream(asyncio.Protocol):

    def default_handler(self, message):
        print("default handler")

    def handle_gapm_device_ready_ind(self, message):      
        print("Received GapmDeviceReadyInd()", message.msg_id)

        #TODO is this appropriate, should there be some async method? 
        self.writer.write(GapmResetCmd(gapm_reset_cmd(GAPM_OPERATION.GAPM_RESET)).to_bytes())

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
        self.writer.write(dev_config.to_bytes())

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

    async def receive(self):
        self.reader, self.writer = await serial_asyncio.open_serial_connection(url='COM13', baudrate=115200)
        print("Reader created")

        while True:
            buffer = bytes()
            buffer = await self.reader.readexactly(1)
            if(buffer[0] == GTL_INITIATOR):
                buffer += await self.reader.readexactly(8)
                par_len = int.from_bytes(buffer[7:9], "little",signed=False)
                if(par_len != 0):
                    buffer += await self.reader.readexactly(par_len)
                message = GtlMessageFactory().create_message(buffer)
                print("Message received, handling it")
                # Handle it

                # TODO what is message is not in the table? 
                self.run(message)



loop = asyncio.get_event_loop()
serial_stream_manager = SerialManagerStream()
loop.run_until_complete(serial_stream_manager.receive())
loop.close()