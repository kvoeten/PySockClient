from packet import Packet
from client import ClientSocket
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

    # Scan for serial ports
    ports = getPorts()

    # Purge dead ones
    port_exceptions = ['dev/ttyprintk']
    for port in port_exceptions:
        if port in ports:
            ports.remove(port)
            print('[Serial] Removed %s.'%port)

    # Scan again!
    for port in ports:
        try:
            s = serial.Serial(port, 9600, timeout = TIMEOUT, rtscts = 0)
            print('[Serial] Connected to %s.'%port)
        except:
            pass
    
    # Check connections again after 5 seconds
    time.sleep(5)