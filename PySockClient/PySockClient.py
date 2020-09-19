from packet import Packet
from sensor import Sensor
from client import ClientSocket
import serial.tools.list_ports
import glob
import serial
import sys
import time

Packet.test()
client = None
BAUDRATE = 9600
TIMEOUT = 0 

def getPorts():
    # Create list of potential ports
    if sys.platform.startswith('win'):
        return ['COM' + str(i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        return glob.glob('/dev/tty[A-Za-z]*')
    else:
        raise EnvironmentError('Unsupported platform: ' + sys.platform)

while True:
    # Check client alive, try connect if not
    if (not client or client.alive == False):
        client = ClientSocket("localhost", 8888)
        client.connect()
    else:
        # Scan for serial ports
        ports = list(serial.tools.list_ports.comports())
        for port in ports:
            if "Arduino" or "Simly" in port.description:
                try:
                    Sensor(client, port.device)
                    print('[Serial] Connected to %s.'%port)
                except Exception as e:
                    print("[Sensor] Failed to connect to sensor: ", e)
    
    # Check connections again after 5 seconds
    time.sleep(5)