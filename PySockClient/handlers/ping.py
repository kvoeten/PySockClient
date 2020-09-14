from packet import Packet

class Ping():
    def process(client, inpacket):
        code = inpacket.readInt()
        outpacket = Packet()
        outpacket.encodeShort(0x01)
        outpacket.enocdeInt(code ^ 0x20101010)
        client.encode(outpacket)
