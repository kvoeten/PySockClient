from packet import Packet
from processor import PacketProcessor
import threading
import socket
import struct
import sys

class ClientSocket(object):
    """Simple TCP Socket handler"""
    
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.alive = True
        else:
            sock = sock

    def disconnect(self):
        self.alive = False
        print("[Socket] Connection closed!")

    def connect(self, host, port):
        try:
            self.sock.connect((host, port))
            decodeThread == threading.thread(target = decode, args = (self))
        except:
            self.alive = False
            print("[Socket] Unable to connect to server!")

    def decode(self):
        while alive:
            try:
                length = struct.unpack('<h', self.sock.receive(2))
                print("[Socket] Awaiting packet of length: " + length)
                PacketProcessor.processPacket(Packet(self.sock.receive(length)))
            except:
                disconnect(self)

    def encode(self, packet):
        try:
            data = packet.getData()
            length = struct.pack('<h', len(data))
            self.sock.sendall(length + data)
            print("[Socket] Sent packet of length: " + length)
        except:
            disconnect(self)

