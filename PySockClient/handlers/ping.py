from packet import Packet

class Ping():
    def process(client, inpacket):
        code = inpacket.readInt()
        outpacket = Packet()
        outpacket.writeShort(0x01)
        outpacket.writeShort(code ^ 0x20101010)
        client.encode(outpacket)
