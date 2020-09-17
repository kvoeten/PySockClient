from enum import Enum
from packet import Packet
from handlers import ping
from sensors import forceplane

handlers = {
    0x01 : ping.Ping,
}

sensors = {
    0x01 : forceplane.ForcePlane    
}

class PacketProcessor():
    def processPacket(client, packet):
        packet.reset() # Reset reader index
        opcode = packet.decodeUShort()
        handlers.get(opcode).process(client, packet)

    def processSensor(sensor, packet):
        packet.reset() # Reset reader index
        sensor.type = packet.decodeUShort()
        sensors.get(sensor.type).process(sensor, packet)

    def handshake(client):
        outpacket = Packet()
        outpacket.encodeUShort(0xF0)
        outpacket.writeLong(client.uid)



