import time
import serial
import re
import matplotlib.pyplot as plt 
import numpy as np

# FPGA_PORT = 'COM7'            # port for Windows
FPGA_PORT = '/dev/ttyUSB0'      # port for Linux / Ubuntu
FPGA_BAUD = 115200

startSequence = r"11111111 >> ([0-9]*)"
stopSequence = r"([0-9]*) >> ([0-9]*)"

def request_antenna_data(device):
    
    amplitudes = []
    datastream = ""

    if device.is_open:

        command = '\n'
        command = command.encode()
        device.write(command)
        
        while True:
            bytes = device.read(device.in_waiting)
            decoded_bytes = bytes.decode('utf-8')
            if decoded_bytes != "":
                datastream = datastream + decoded_bytes
                if "*" in datastream:
                    break
            else:
                continue
        datastream = datastream.split("\r\n")

        for line in datastream:
            startresult = re.search(startSequence, line)
            stopresult = re.search(stopSequence, line)

            if line.strip().isnumeric():
                amplitudes.append(int(line))
            elif startresult is not None:
                startfreq = int(startresult.groups()[0])
            elif stopresult is not None:
                endfreq = int(stopresult.groups()[1])
                sampleSize = int(stopresult.groups()[0])
            if "*" in line:
                return startfreq, endfreq, sampleSize, amplitudes

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
else:
    print("Connection successfully established.")
    print()

plt.ion() 
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_facecolor('k')

print("Requesting data from FPGA...")
now = time.time()
startfreq, endfreq, sampleSize, amplitudes = request_antenna_data(fpga)
print("Data received in {} seconds".format(time.time()-now))
# print(amplitudes)
# print("Start Freq: ", startfreq)
# print("Stop Freq: ", endfreq)
# print("Sample Size: ", sampleSize)

ax.set_ylim(min(amplitudes), max(amplitudes))
bandwidth = list(np.arange(start=startfreq, stop=endfreq, step=((endfreq-startfreq)/sampleSize)))
ax.set_ylabel('Amplitudes (dBm)')
ax.set_xlabel('Frequencies (GHz)')

ax.plot(bandwidth, amplitudes, '-y')
fig.canvas.draw()
fig.canvas.flush_events()
# plt.show()

while True:
    try:
        now = time.time()
        startfreq, endfreq, sampleSize, amplitudes = request_antenna_data(fpga)
        ax.plot(bandwidth, amplitudes, '-y')
        fig.canvas.draw()
        print('Updating data in {}s.'.format(time.time()-now))
        fig.canvas.flush_events()
    except KeyboardInterrupt:
        print("Exiting...")
        break
        