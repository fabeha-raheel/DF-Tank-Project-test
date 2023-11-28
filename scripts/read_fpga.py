import time
import serial
import re

startSequence = r"^11111111 >> ([0-9]*)$"
stopSequence = r"^([0-9]*) >> ([0-9]*)$"

def request_antenna_data(device):
    startfreq = 0
    endfreq = 0
    sampleSize = 0

    command = '\n'
    command = command.encode()
    device.write(command)

    while True:
        data = fpga.readline()
        data = data.decode('utf-8')
        data = data.strip()
        print(data)

        startresult = re.search(startSequence, data)
        stopresult = re.search(stopSequence, data)

        if startresult is not None:
            startfreq = int(startresult.groups()[0])
        elif stopresult is not None:
            stopfreq = int(stopresult.groups()[1])
            sampleSize = int(stopresult.groups()[0])
        elif data == "*******************************************************************************":
            print("Data complete.")
            print("Start Freq: ", startfreq)
            print("Stop Freq: ", stopfreq)
            print("Sample Size: ", sampleSize)
            break

# Connect to the FPGA over UART
fpga = serial.Serial(
    port='COM7',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    timeout = None
    )
time.sleep(3)

print("Sending data to FPGA...")
request_antenna_data(fpga)