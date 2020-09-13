from enum import Enum
from handlers import *

handlers = {
    0x01 : ping.Ping,
}

class PacketProcessor():
    def processPacket(client, packet):
        opcode = packet.decodeShort()
        handlers.get(opcode).process(client, packet)


