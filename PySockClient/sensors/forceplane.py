
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
