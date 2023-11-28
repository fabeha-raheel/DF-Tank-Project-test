import time
import serial
import re
import matplotlib.pyplot as plt 
import numpy as np


startSequence = r"^11111111 >> ([0-9]*)$"
stopSequence = r"^([0-9]*) >> ([0-9]*)$"


def request_antenna_data(device):
    
    amplitudes = []

    command = '\n'
    command = command.encode()
    device.write(command)
    
    # now = time.time()
    while True:
        data = fpga.readline()
        data = data.decode().strip()
        # data = data.strip()
        # print(data)
        
        startresult = re.search(startSequence, data)
        stopresult = re.search(stopSequence, data)

        if data.isnumeric():
            amplitudes.append(int(data))
        elif startresult is not None:
            startfreq = int(startresult.groups()[0])
        elif stopresult is not None:
            endfreq = int(stopresult.groups()[1])
            sampleSize = int(stopresult.groups()[0])
        elif data == "*******************************************************************************":
            
            return startfreq, endfreq, sampleSize, amplitudes
        # print("Time taken by if block: ", time.time()-now)

# Connect to the FPGA over UART
fpga = serial.Serial(
    port='COM7',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    timeout = None
    )
time.sleep(3)

print("Requesting data from FPGA...")
now = time.time()
startfreq, endfreq, sampleSize, amplitudes = request_antenna_data(fpga)
print("Data received in {} seconds".format(time.time()-now))
# print("Received Data")
# print(amplitudes)
# print("Start Freq: ", startfreq)
# print("Stop Freq: ", endfreq)
# print("Sample Size: ", sampleSize)

# plt.ion() 
# fig = plt.figure()
# now = time.time()
x = list(np.arange(start=startfreq, stop=endfreq, step=((endfreq-startfreq)/sampleSize)))
y = amplitudes
plt.plot(x, y, '-b')
# print("Data displayed in {} seconds.".format(time.time()-now))
plt.show()
