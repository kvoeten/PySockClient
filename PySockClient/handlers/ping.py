from packet import Packet

class Ping():
    def process(client, inpacket):
        code = inpacket.decodeInt()
        print("[Client] Ping Code ", code)

        outpacket = Packet()
        outpacket.encodeShort(0x01)
        outpacket.encodeInt(code ^ 0x20101010)
        client.encode(outpacket)
