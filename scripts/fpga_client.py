import socket
import json
import time
import re
import serial

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5555

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

def run_client(fpga):
    # create a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = SERVER_IP  # replace with the server's IP address
    server_port = SERVER_PORT  # replace with the server's port number
    # establish connection with server
    client.connect((server_ip, server_port))

    try:
        while True:
            # Get Antenna Data
            startfreq, endfreq, sampleSize, amplitudes = request_antenna_data(fpga)
            print("Start Freq: ", startfreq)
            print("Stop Freq: ", endfreq)
            print("Sample Size: ", sampleSize)

            # Packetize Data to Transmit wirelessly
            sensor_data = {
                "starting_frequency" : startfreq,
                "ending_frequency" : endfreq,
                "sample_size" : sampleSize
                # "amplitudes" : amplitudes
            }

            # Convert data to JSON format
            payload = json.dumps(sensor_data)

            # Send data to the server
            try:
                client.sendall(payload.encode())
                time.sleep(1)
            except:
                print("Problem sending data to client")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # close client socket (connection to the server)
        client.close()
        print("Connection to server closed")

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
    print("Starting Data Transmission Client...")
    run_client(fpga)
except serial.SerialException:
    print("Error connecting to port.")
finally:
    print("Connection successfully established.")
    print()