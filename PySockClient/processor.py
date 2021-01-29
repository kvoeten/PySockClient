
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
        
        print("[Sensor] Packet: " + packet.get())

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



