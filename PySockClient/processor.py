from enum import Enum
from packet import Packet
from handlers import ping

handlers = {
    0x01 : ping.Ping,
}

class PacketProcessor():
    def processPacket(client, packet):
        opcode = packet.decodeShort()
        handlers.get(opcode).process(client, packet)

    def handshake(client):
        outpacket = Packet()
        outpacket.encodeUShort(0xF0)
        outpacket.writeLong(client.uid)



