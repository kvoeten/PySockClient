
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
import _thread
import socket
import struct
import sys

class ClientSocket(object):
    """Simple TCP Socket handler"""
    
    def __init__(self, host, port, sock=None):
        self.alive = False
        self.host = host
        self.port = port
        self.uid = 0x01
        self.sensors = {}
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            sock = sock

    def disconnect(self):
        print("[Socket] Connection closed!")
        self.alive = False

    def connect(self):
        try:
            self.sock.connect((self.host, self.port))
            self.alive = True
            _thread.start_new_thread(ClientSocket.decode ,(self,))
        except Exception as ex:
            print("[Socket] Unable to connect to server at " + self.host + ":" + str(self.port) + ". Err: ", ex)
            self.alive = False

    def decode(self):
        print("[Socket] Connected to server at " + self.host + ":" + str(self.port) + ".")
        while self.alive:
            try:
                length = struct.unpack('<H', self.sock.recv(2))[0]
                PacketProcessor.processPacket(self, Packet(self.sock.recv(length)))
            except Exception as ex:
                print("[Socket] Decoder exception: ", ex)
                self.alive = False
        self.disconnect()

    def encode(self, packet):
        try:
            data = packet.getData()
            outBuffer = Packet()
            outBuffer.encodeUShort(struct.pack('<H', len(data))[0])
            outBuffer.buff.write(data)
            self.sock.sendall(outBuffer.getData())
        except Exception as e:
            print("[Socket] Encoder exception: ", e)
            self.disconnect()