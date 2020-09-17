from packet import Packet

class ForcePlane():
    def process(sensor, inpacket):
        front = inpacket.decodeUInt()
        back = inpacket.decodeUInt()
        left = inpacket.decodeUInt()
        right = inpacket.decodeUInt()

        outpacket = Packet()
        outpacket.encodeUShort(0x02)
        outpacket.encodeUShort(sensor.type)
        outpacket.encodeUInt(front)
        outpacket.encodeUInt(back)
        outpacket.encodeUInt(left)
        outpacket.encodeUInt(right)
        sensor.client.encode(outpacket)
