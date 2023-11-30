import time
import serial
import re
import matplotlib.pyplot as plt 
import numpy as np

HOLYBRO_PORT = '/dev/ttyUSB2'
HOLYBRO_BAUD = 115200

startSequence = r"11111111 >> ([0-9]*)"
stopSequence = r"([0-9]*) >> ([0-9]*)"

def receive_telem_antenna(telem_device):
    amplitudes = []
    datastream = ""

    if telem_device.is_open:
        
        while True:
            bytes = telem_device.read(telem_device.in_waiting)
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
        else:
            print("No open port...")
            return -1, -1, -1, amplitudes


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

plt.ion() 

print("Requesting data from FPGA...")
now = time.time()
startfreq, endfreq, sampleSize, amplitudes = receive_telem_antenna(holybro)
print("Data received in {} seconds".format(time.time()-now))
# print(amplitudes)
# print("Start Freq: ", startfreq)
# print("Stop Freq: ", endfreq)
# print("Sample Size: ", sampleSize)
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_facecolor('k')
ax.set_ylim(min(amplitudes), max(amplitudes))
bandwidth = list(np.arange(start=startfreq, stop=endfreq, step=((endfreq-startfreq)/sampleSize)))
ax.set_ylabel('Amplitudes (dBm)')
ax.set_xlabel('Frequencies (GHz)')

ax.plot(bandwidth, amplitudes, '-y')
fig.canvas.draw()
fig.canvas.flush_events()
# # plt.show()

while True:
    try:
        now = time.time()
        startfreq, endfreq, sampleSize, amplitudes = receive_telem_antenna(holybro)
        ax.plot(bandwidth, amplitudes, '-y')
        fig.canvas.draw()
        print('Updating data in {}s.'.format(time.time()-now))
        fig.canvas.flush_events()
    except KeyboardInterrupt:
        print("Exiting...")
        break
        