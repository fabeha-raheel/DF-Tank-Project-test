import serial
import time

from holybro_class import HolybroReceiver

HOLYBRO_RX_PORT = '/dev/ttyUSB2'
HOLYBRO_RX_BAUD = 115200

holybro_receiver = HolybroReceiver(port=HOLYBRO_RX_PORT, baud=HOLYBRO_RX_BAUD)

try:
    holybro_receiver.connect()
    print("Waiting for handshake...")
    holybro_receiver.handshake()
    
except KeyboardInterrupt:
    holybro_receiver.transmitter.close()
    print("Exiting...")