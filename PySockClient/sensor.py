
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

from processor import PacketProcessor
from threading import Thread
from packet import Packet
import bluetooth as bl
import _thread
import serial
import struct
import sys

class Sensor(object):
    """Simple Serial USB Reading"""
    
    def __init__(self, client, port, mac = None, bluetooth = False):
        self.bluetooth = bluetooth
        self.port = port
        self.type = 0x00
        self.uid = 0x00
        self.client = client
        self.decode = -1
        if not bluetooth:
            self.serial = serial.Serial(port, 9600, timeout = 1, rtscts = 0)
            self.sock = None
        else:
            self.sock = bl.BluetoothSocket(bl.RFCOMM)
            self.sock.connect((mac, port))
            self.serial = None
            self.alive = True
        _thread.start_new_thread(Sensor.read ,(self,))

    def disconnect(self):
        print("[Sensor] Connection closed!")
        self.alive = False
        if self.serial:
            self.serial.close()
        if self.sock:
            self.sock.close()

    def read(self):
        print("[Sensor] Connected to sensor at " + self.port + ".")
        if not self.bluetooth:
            while self.serial.isOpen() and self.client and self.client.alive:
                try:
                    if self.decode is -1 and self.serial.in_waiting >= 2:
                        self.decode = struct.unpack('<H', self.serial.read(2))[0]
                        print("[Sensor] Received packet of length: " + str(self.decode))
                    if self.decode is not -1 and self.serial.in_waiting >= self.decode:
                        PacketProcessor.processSensor(self, Packet(self.serial.read(self.decode)))
                        self.decode = -1
                except Exception as e:
                    print("[Sensor] Read exception: ", e)
        else:
            while self.alive and self.client and self.client.alive:
                try:
                    length = struct.unpack('<H', self.sock.recv(2))[0]
                    print("[Sensor] Received packet of length: " + str(length))
                    PacketProcessor.processSensor(self, Packet(self.sock.recv(length)))
                except Exception as ex:
                    print("[Sensor] Decoder exception: ", ex)
                    self.alive = False
        self.disconnect()

    def write(self, packet):
        try:
            data = packet.getData()
            outBuffer = Packet()
            outBuffer.encodeUShort(struct.pack('<H', len(data))[0])
            outBuffer.buff.write(data)
            self.serial.write(outBuffer.getData())
            print("[Sensor] Sent packet ", outBuffer.get())
        except Exception as e:
            print("[Sensor] Write exception: ", e)
            self.disconnect()

