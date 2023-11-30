import time
import serial
import re
import matplotlib.pyplot as plt 
import numpy as np

startSequence = r"11111111 >> ([0-9]*)"
stopSequence = r"([0-9]*) >> ([0-9]*)"

def request_antenna_data(fpga_device, telem_device):
    
    amplitudes = []
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
    port='COM7',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    timeout = None
    )
    time.sleep(1)
except serial.SerialException:
    print("Error connecting to fpga port.")
finally:
    print("FPGA Connection successfully established.")
    print()

# Connect to the Holybro Module over UART
print("Connecting to Holybro Module...")
try:
    holybro = serial.Serial(
    port='COM8',
    baudrate=57600,
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
startfreq, endfreq, sampleSize, amplitudes = request_antenna_data(fpga, holybro)
print("Data received in {} seconds".format(time.time()-now))
# print(amplitudes)
# print("Start Freq: ", startfreq)
# print("Stop Freq: ", endfreq)
# print("Sample Size: ", sampleSize)
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.set_facecolor('k')
# ax.set_ylim(min(amplitudes), max(amplitudes))
# bandwidth = list(np.arange(start=startfreq, stop=endfreq, step=((endfreq-startfreq)/sampleSize)))
# ax.set_ylabel('Amplitudes (dBm)')
# ax.set_xlabel('Frequencies (GHz)')

# ax.plot(bandwidth, amplitudes, '-y')
# fig.canvas.draw()
# fig.canvas.flush_events()
# # plt.show()

# while True:
#     try:
#         now = time.time()
#         startfreq, endfreq, sampleSize, amplitudes = request_antenna_data(fpga)
#         ax.plot(bandwidth, amplitudes, '-y')
#         fig.canvas.draw()
#         print('Updating data in {}s.'.format(time.time()-now))
#         fig.canvas.flush_events()
#     except KeyboardInterrupt:
#         print("Exiting...")
#         break
        