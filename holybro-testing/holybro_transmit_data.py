import time
import serial
import re
import matplotlib.pyplot as plt 
import numpy as np
import sys

from holybro_class import HolybroTransmitter

# FPGA_PORT = 'COM7'            # port for Windows
FPGA_PORT = '/dev/ttyUSB0'      # port for Linux / Ubuntu
FPGA_BAUD = 115200

HOLYBRO_TX_PORT = '/dev/ttyUSB2'
HOLYBRO_TX_BAUD = 115200

RE_RUN = False

# Connect to the FPGA over UART
print("Connecting to FPGA...")
try:
    fpga = serial.Serial(
    port=FPGA_PORT,
    baudrate=FPGA_BAUD,
    parity=serial.PARITY_NONE,
    timeout = None
    )
    time.sleep(1)
except serial.SerialException:
    print("Error connecting to port.")
    sys.exit()
finally:
    print("Connection successfully established.")
    print()

holybro_transmitter = HolybroTransmitter(port=HOLYBRO_TX_PORT, baud=HOLYBRO_TX_BAUD)

holybro_transmitter.connect()
print("Waiting for handshake...")
holybro_transmitter.handshake()

if RE_RUN:

    while True:
        try:
            print("Transmitting data from FPGA...")
            now = time.time()
            holybro_transmitter.transmit_antenna_data(fpga)
            print("Data transmitted in {} seconds".format(time.time()-now))

        except KeyboardInterrupt:
            fpga.close()
            holybro_transmitter.transmitter.close()
            print("Exiting...")
            break

else:

    try:
        print("Transmitting data from FPGA...")
        now = time.time()
        holybro_transmitter.transmit_antenna_data(fpga)
        print("Data transmitted in {} seconds".format(time.time()-now))
        
    except KeyboardInterrupt:
        holybro_transmitter.transmitter.close()
        print("Exiting...")