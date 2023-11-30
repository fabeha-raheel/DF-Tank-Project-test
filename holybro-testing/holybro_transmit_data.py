import time
import serial
import re
import matplotlib.pyplot as plt 
import numpy as np

# FPGA_PORT = 'COM7'            # port for Windows
FPGA_PORT = '/dev/ttyUSB0'      # port for Linux / Ubuntu
FPGA_BAUD = 115200

HOLYBRO_PORT = '/dev/ttyUSB1'
HOLYBRO_BAUD = 115200

RE_RUN = True

startSequence = r"11111111 >> ([0-9]*)"
stopSequence = r"([0-9]*) >> ([0-9]*)"

def transmit_telem_antenna(fpga_device, telem_device):
    
    datastream = ""

    if fpga_device.is_open:

        command = '\n'
        command = command.encode()
        fpga_device.write(command)
        
        while True:
            bytes = fpga_device.read(fpga_device.in_waiting)
            decoded_bytes = bytes.decode('utf-8')
            if decoded_bytes != "":
                telem_device.write(bytes)
                datastream = datastream + decoded_bytes
                if "*" in datastream:
                    return
            else:
                continue

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
finally:
    print("Connection successfully established.")
    print()

# Connect to the Holybro Module over UART
print("Connecting to Holybro Module...")
try:
    holybro = serial.Serial(
    port=HOLYBRO_PORT,
    baudrate=HOLYBRO_BAUD,
    parity=serial.PARITY_NONE,
    timeout = None
    )
    time.sleep(1)
except serial.SerialException:
    print("Error connecting to holybro port.")
finally:
    print("Holybro Connection successfully established.")
    print()

if RE_RUN:

    while True:
        try:
            print("Requesting data from FPGA...")
            now = time.time()
            # startfreq, endfreq, sampleSize, amplitudes = request_antenna_data(fpga, holybro)
            transmit_telem_antenna(fpga, holybro)
            print("Data transmitted in {} seconds".format(time.time()-now))
        except KeyboardInterrupt:
            fpga.close()
            holybro.close()
            print("Exiting ...")
            break

else:

    print("Requesting data from FPGA...")
    now = time.time()
    # startfreq, endfreq, sampleSize, amplitudes = request_antenna_data(fpga, holybro)
    transmit_telem_antenna(fpga, holybro)
    print("Data transmitted in {} seconds".format(time.time()-now))