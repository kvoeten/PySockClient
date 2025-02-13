
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
from sensor import Sensor
from client import ClientSocket
import serial.tools.list_ports
import bluetooth as bl
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
        client = ClientSocket("127.0.0.1", 8888)
        client.connect()
    else:
        # Scan for serial ports
        ports = list(serial.tools.list_ports.comports())
        for port in ports:
            if "Arduino" in port.description:

                # Attempt to connect sensor via serial
                try:
                    Sensor(client, port.device)
                    print('[Serial] Connected to %s.'%port)
                except Exception as e:
                    #print("[Sensor] Failed to connect to sensor: ", e)
                    pass

        # Scan for bluetooth:
        devices = bl.discover_devices(duration=5, flush_cache=True, lookup_names=True)
        if (devices):
            for device in devices:
                if "Simly" in device[1]:

                    # Construct sensor identifier
                    key = int(device[1][-4:])
                    if "FS-01" in device[1]:
                        key = "1:" + key;

                    # Check if sensor is already connected
                    if client.sensors.get(key):
                        continue

                    # Attempt to connect sensor via bluetooth
                    try:
                        Sensor(client, 0, device[0], True)
                    except Exception as e:
                        pass
    
    # Check connections again after 5 seconds
    time.sleep(5)