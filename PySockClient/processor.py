from enum import Enum

class PacketProcessor():
    def processPacket(client, packet):
        sensor = packet.decodeShort()

