from ctypes import *
from .gtl_message_base import *

class GattmAddSvcReq(GtlMessageBase):
    def __init__(self, parameters: gattm_add_svc_req = None):

        params = parameters if parameters else gattm_add_svc_req()
        p_len = 24*(params.svc_desc.nb_att+1)

        super().__init__(msg_id=GATTM_MSG_ID.GATTM_ADD_SVC_REQ,
                         dst_id=KE_API_ID.TASK_ID_GATTM,
                         src_id=KE_API_ID.TASK_ID_GTL,
                         par_len=p_len, # TODO if user updates parameters.nb_att after construction, par_len automatically updated
                         parameters=params)

        self.parameters = params 
        self.par_len = p_len

    def get_par_len(self):
        self._par_len = 24*(self.parameters.svc_desc.nb_att+1)
        print(f"GattmAddSvcReq getting _par_len = {self._par_len}")
        return self._par_len

    def set_par_len(self, value):
        self._par_len = value

    par_len = property(get_par_len, set_par_len)

    def to_bytes(self):

        message = bytearray()
        message.append(GTL_INITIATOR)
        members = self.__dict__.keys()
        for member in members:
            if(member != 'parameters'):
                #TODO  _par_len used in some messages to dynamically update par_len when length of parameters can change.
                # If GtlMessageBase to_bytes used for these classes, For some reason first call to to_bytes uses initial value of par_len and second call has correct updated value
                # Here to_bytes method has been overridden. But perhaps there is someway to handle in GtlMessageBase
                if(member == '_par_len'):
                    message.extend(self.par_len.to_bytes(length=2, byteorder='little'))
                else:
                    message.extend(getattr(self, member).to_bytes(length=2, byteorder='little'))

            elif(member == 'parameters' and getattr(self, 'par_len') > 0):
                # TODO need to detect if pointer type and get contents. Look at __repr__ for parsing. Make Struct to bytearray?
                #message.extend(bytearray(self.parameters)) # TODO revisit this for big endian machine

                print(f"message before: {message[:10]}")
                message.extend(self.struct_to_bytearray(self.parameters))
                #print(f"message before: {message[:10]}")
                #message.extend(self.serialize(self.parameters))
        
        return message

# TODO need to add to_bytes method for any class that dynamically updates par_len
# TODO try using little endinan stucture to prevent endian issues