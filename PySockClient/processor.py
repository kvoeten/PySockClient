from enum import Enum
from packet import Packet
from handlers import ping
from sensors import forceplane, rotator

handlers = {
    0x01 : ping.Ping,
    0x02 : rotator.Angle
}

sensors = {
    0x01 : forceplane.ForcePlane,
    0x02 : rotator.Rotation
}

class PacketProcessor():
    # Process unreal requests
    def processPacket(client, packet):
        packet.reset() # Reset reader index
        opcode = packet.decodeUShort()
        handlers.get(opcode).process(client, packet)

    # Process sensor data reports
    def processSensor(sensor, packet):
        # Reset reader index
        packet.reset() 

        # Get sensor identifier
        sensor.type = packet.decodeUShort()
        sensor.uid = packet.decodeUShort()

        # Construct sensor identifier
        key = str(sensor.type) + ":" + str(sensor.uid)
        existing = sensor.client.sensors.get(key)

        # Check if sensor is also connected over serial
        if existing and sensor.bluetooth and not existing.bluetooth:
            sensor.disconnect()
        else:
            sensor.client.sensors[key] = sensor

        # Finally handle sensor
        sensors.get(sensor.type).process(sensor, packet)

    # Send hello to unreal
    def handshake(client):
        outpacket = Packet()
        outpacket.encodeUShort(0xF0)
        outpacket.writeLong(client.uid)



