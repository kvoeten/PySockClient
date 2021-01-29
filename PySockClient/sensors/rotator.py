
#   This file is part of the Simly project by Kaz Voeten at the Eindhoven University of Technology.
#   Copyright (C) 2020 Eindhoven University of Technology
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

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