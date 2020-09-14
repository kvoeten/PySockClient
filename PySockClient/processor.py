from enum import Enum
from packet import Packet
from handlers import ping

handlers = {
    0x01 : ping.Ping,
}

class PacketProcessor():
    def processPacket(client, packet):
        packet.reset()
        opcode = packet.decodeUShort()
        print("[Client] InPacket (", opcode, ") ", packet.get())
        handlers.get(opcode).process(client, packet)

    def handshake(client):
        outpacket = Packet()
        outpacket.encodeUShort(0xF0)
        outpacket.writeLong(client.uid)



