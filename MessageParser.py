from gtl_messages.gtl_message_factory import GtlMessageFactory


class MessageParser():

    def decode_from_bytes(self, byte_string):
        return GtlMessageFactory().create_message(byte_string)
