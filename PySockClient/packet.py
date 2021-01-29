
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

import io
import sys
import struct

class Packet(object):
    """Little Endian byte buffer"""

    def __init__(self, data=None):
        self.buff = io.BytesIO()
        if data:
            self.buff.write(data)
        
    def getData(self):
        return self.buff.getvalue()

    def reset(self):
        self.buff.seek(0)

    def release(self):
        self.buff.close()

    def print(self):
        print("[Packet] " + self.get())

    def get(self):
        hex = self.buff.getvalue().hex().upper()
        hex = " ".join(hex[i:i+2] for i in range(0, len(hex), 2))
        return hex
    
    # Encoders
    def decodeChar(self):
        return struct.unpack('<c', self.buff.read(1))[0]

    def decodeByte(self):
        return struct.unpack('<b', self.buff.read(1))[0]

    def decodeUByte(self):
        return struct.unpack('<B', self.buff.read(1))[0]

    def decodeShort(self):
        return struct.unpack('<h', self.buff.read(2))[0]

    def decodeUShort(self):
        return struct.unpack('<H', self.buff.read(2))[0]

    def decodeInt(self):
        return struct.unpack('<i', self.buff.read(4))[0]

    def decodeUInt(self):
        return struct.unpack('<I', self.buff.read(4))[0]

    def decodeLong(self):
        return struct.unpack('<q', self.buff.read(8))[0]

    def decodeULong(self):
        return struct.unpack('<Q', self.buff.read(8))[0]

    def decodeFloat(self):
        return struct.unpack('<f', self.buff.read(4))[0]

    def decodeDouble(self):
        return struct.unpack('<d', self.buff.read(8))[0]

    # Decoders
    def encodeChar(self, value):
        self.buff.write(struct.pack('<c', value))

    def encodeByte(self, value):
        self.buff.write(struct.pack('<b', value))

    def encodeUByte(self, value):
        self.buff.write(struct.pack('<B', value))

    def encodeShort(self, value):
        self.buff.write(struct.pack('<h', value))

    def encodeUShort(self, value):
        self.buff.write(struct.pack('<H', value))

    def encodeInt(self, value):
        self.buff.write(struct.pack('<i', value))

    def encodeUInt(self, value):
        self.buff.write(struct.pack('<I', value))

    def encodeLong(self, value):
        self.buff.write(struct.pack('<q', value))

    def encodeULong(self, value):
        self.buff.write(struct.pack('<Q', value))

    def encodeFloat(self, value):
        self.buff.write(struct.pack('<f', value))

    def encodeDouble(self, value):
        self.buff.write(struct.pack('<d', value))

    def test():
        packet = Packet(b'\x00')
        packet.encodeUShort(2)
        packet.encodeInt(4)
        packet.encodeFloat(1.2)
        packet.encodeInt(-4)
        packet.encodeInt(-1)
        packet.reset()
        assert packet.decodeByte() == 0, "Should be 0"
        assert packet.decodeUShort() == 2, "Should be 2"
        assert packet.decodeInt() == 4, "Should be 4"
        assert packet.decodeFloat() < 2, "Should be <1.2"
        assert packet.decodeInt() == -4, "Should be -4"
        assert packet.decodeInt() == -1, "Should be -1"
        print("[Packet] All Tests Passed")

