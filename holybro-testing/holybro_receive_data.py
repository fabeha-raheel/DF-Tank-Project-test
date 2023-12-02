import time
import serial
import re
import matplotlib.pyplot as plt 
import numpy as np

from holybro_class import HolybroReceiver

HOLYBRO_RX_PORT = '/dev/ttyUSB2'
HOLYBRO_RX_BAUD = 115200

RE_RUN = False

holybro_receiver = HolybroReceiver(port=HOLYBRO_RX_PORT, baud=HOLYBRO_RX_BAUD)

holybro_receiver.connect()
print("Waiting for handshake...")
holybro_receiver.handshake()

if RE_RUN:

    while True:
        try:
            print("Requesting data from FPGA...")
            now = time.time()
            startfreq, endfreq, sampleSize, amplitudes = holybro_receiver.listen()
            print("Data transmitted in {} seconds".format(time.time()-now))
            print("Amplitudes gotten: ", len(amplitudes))
            print("Start Freq: ", startfreq)
            print("Stop Freq: ", endfreq)
            print("Sample Size: ", sampleSize)

        except KeyboardInterrupt:
            holybro_receiver.receiver.close()
            print("Exiting...")
            break

else:

    try:
        print("Receiving data from FPGA...")
        now = time.time()
        startfreq, endfreq, sampleSize, amplitudes = holybro_receiver.listen()
        print("Data received in {} seconds".format(time.time()-now))
        print("Amplitudes gotten: ", len(amplitudes))
        print("Start Freq: ", startfreq)
        print("Stop Freq: ", endfreq)
        print("Sample Size: ", sampleSize)

    except KeyboardInterrupt:
        holybro_receiver.transmitter.close()
        print("Exiting...")