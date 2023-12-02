import serial
import time

from holybro_class import HolybroTransmitter


FPGA_PORT = '/dev/ttyUSB0'      # port for Linux / Ubuntu
FPGA_BAUD = 115200

HOLYBRO_TX_PORT = '/dev/ttyUSB1'
HOLYBRO_TX_BAUD = 115200

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

holybro_transmitter = HolybroTransmitter(port=HOLYBRO_TX_PORT, baud=HOLYBRO_TX_BAUD)

try:
    holybro_transmitter.connect()
    print("Waiting for handshake...")
    holybro_transmitter.handshake()
    
except KeyboardInterrupt:
    holybro_transmitter.transmitter.close()
    print("Exiting...")