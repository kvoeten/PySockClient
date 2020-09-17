from processor import PacketProcessor
from threading import Thread
from packet import Packet
import _thread
import serial
import struct
import sys

class Sensor(object):
    """Simple TCP Socket handler"""
    
    def __init__(self, client, port):
        self.port = port
        self.type = 0x00
        self.client = client
        self.decode = -1
        self.serial = serial.Serial(port, 9600, timeout = 1, rtscts = 0)
        _thread.start_new_thread(Sensor.read ,(self,))

    def disconnect(self):
        print("[Sensor] Connection closed!")
        if self.serial:
            self.serial.close()

    def read(self):
        print("[Sensor] Connected to sensor at " + self.port + ".")
        while self.serial.isOpen() and self.client and self.client.alive:
            try:
                if self.decode is -1 and self.serial.in_waiting >= 2:
                    self.decode = struct.unpack('<H', self.serial.read(2))[0]
                if self.decode is not -1 and self.serial.in_waiting >= self.decode:
                    PacketProcessor.processSensor(self, Packet(self.serial.read(self.decode)))
                    self.decode = -1
            except Exception as e:
                print("[Sensor] Read exception: ", e)
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

