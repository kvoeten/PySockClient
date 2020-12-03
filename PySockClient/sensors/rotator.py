from packet import Packet

class Rotation():
    # Write the current received angle to unreal
    def process(sensor, inpacket):
        # Read current angle
        angle = inpacket.decodeInt()

        # Construct packet with opcode 0x03
        outpacket = Packet()
        outpacket.encodeUShort(0x03)

        # Encode type and uid for callbacks from unreal
        outpacket.encodeUShort(sensor.type)
        outpacket.encodeUShort(sensor.uid)

        # Encode angle and send to unreal
        outpacket.encodeUInt(angle)
        sensor.client.encode(outpacket)

class Angle():
    # Handle unreal request for rotation to a desired angle
    def process(client, inpacket):
        # Get sensor identifier and angle request
        sensor.type = inpacket.decodeUShort()
        sensor.uid = inpacket.decodeUShort()
        angle = inpacket.decodeInt()

        # Construct sensor identifier
        key = str(sensor.type) + ":" + str(sensor.uid)
        existing = sensor.client.sensors.get(key)

        # Check if sensor is also connected over serial
        if existing and sensor.bluetooth and not existing.bluetooth:
            sensor.disconnect()
        else:
            sensor.client.sensors[key] = sensor

        # Write desired angle to sensor (arduino)
        outpacket = Packet()
        outpacket.encodeInt(angle)
        sensor.write(outpacket)