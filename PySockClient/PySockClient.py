from packet import Packet
from client import ClientSocket
import struct

Packet.test()

client = ClientSocket()
client.connect("127.0.0.1", "8888")

while (client.alive):
    packet = Packet(b'')
    packet.encodeByte(1)
    client.encode(packet)