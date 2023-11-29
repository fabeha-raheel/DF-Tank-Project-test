import time
import serial
import re
import matplotlib.pyplot as plt 
import numpy as np

startSequence = r"^11111111 >> ([0-9]*)$"
stopSequence = r"^([0-9]*) >> ([0-9]*)$"

def request_antenna_data(device):
    
    amplitudes = []

    if device.is_open:

        command = '\n'
        command = command.encode()
        device.write(command)
        
        while True:
            data = fpga.readline()
            data = data.decode().strip()
            if data=='\n':
                continue
            
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

# Connect to the FPGA over UART
print("Connecting to FPGA...")
try:
    fpga = serial.Serial(
    port='COM7',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    timeout = None
    )
    time.sleep(1)
except serial.SerialException:
    print("Error connecting to port.")
finally:
    print("Connection successfully established.")
    print()

print("Requesting data from FPGA...")
now = time.time()
startfreq, endfreq, sampleSize, amplitudes = request_antenna_data(fpga)
print("Data received in {} seconds".format(time.time()-now))
# print(amplitudes)
# print("Start Freq: ", startfreq)
# print("Stop Freq: ", endfreq)
# print("Sample Size: ", sampleSize)

# plt.ion() 
# fig = plt.figure()
bandwidth = list(np.arange(start=startfreq, stop=endfreq, step=((endfreq-startfreq)/sampleSize)))
plt.plot(bandwidth, amplitudes, '-c')
plt.show()
