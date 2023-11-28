import time
import serial

# Connect to the FPGA over UART
fpga = serial.Serial(
    port='COM13',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    timeout = None
    )
time.sleep(3)

while True:
    data = fpga.readline()
    # data = data.strip()
    print(data)