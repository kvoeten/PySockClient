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
        outpacket.encodeInt(angle)
        sensor.client.encode(outpacket)

class Angle():
    # Handle unreal request for rotation to a desired angle
    def process(client, inpacket):
        # Get sensor identifier and angle request
        type = inpacket.decodeUShort()
        uid = inpacket.decodeUShort()
        angle = inpacket.decodeInt()

        # Construct sensor identifier
        key = str(type) + ":" + str(uid)
        sensor = client.sensors.get(key)

        if (sensor):
            # Write desired angle to sensor (arduino)
            outpacket = Packet()
            outpacket.encodeInt(angle)
            sensor.write(outpacket)
            print("[Rotator] Requested angle: " + str(angle))
        else:
            print("[Rotator] Invalid sensor request: " + str(uid))