import serial
import time
import re

class HolybroTransmitter():

    def __init__(self, port=None, baud=None):

        self.port = port
        self.baud = baud

    def connect(self):

        print("Connecting to Holybro Transmitter...")
        try:
            self.transmitter = serial.Serial(
            port=self.port,
            baudrate=self.baud,
            parity=serial.PARITY_NONE,
            timeout = None
            )
            time.sleep(1)
        except serial.SerialException:
            print("Error connecting to holybro transmitter.")
        finally:
            print("Holybro Transmitter Connection successfully established.")
            print()
    
    def handshake(self):
        msg = "ready"
        send = "ok"
        acknowledged = False

        while not acknowledged:
            received = self.transmitter.read(self.transmitter.in_waiting)
            if msg in received.decode('utf-8'):
                acknowledged = True
                print("Receiver is ready.")
                self.transmitter.write(send.encode())
                return
            print("Waiting for Receiver...")
            time.sleep(0.5)
    
    def transmit_antenna_data(self, fpga):

        if fpga.is_open:
            command = '\n'
            command = command.encode()
            fpga.write(command)
        
            while True:
                bytes = fpga.read(fpga.in_waiting)
                decoded_bytes = bytes.decode('utf-8')
                if decoded_bytes != "":
                    self.transmitter.write(bytes)
                    if "***" in decoded_bytes:
                        return
                else:
                    continue
    
class HolybroReceiver():
    def __init__(self, port=None, baud=None):
        
        self.port = port
        self.baud = baud

    def connect(self):

        print("Connecting to Holybro Receiver...")
        try:
            self.receiver = serial.Serial(
            port=self.port,
            baudrate=self.baud,
            parity=serial.PARITY_NONE,
            timeout = None
            )
            time.sleep(1)
        except serial.SerialException:
            print("Error connecting to holybro receiver.")
        finally:
            print("Holybro Receiver Connection successfully established.")
            print()
    
    def handshake(self):

        msg = 'ready\n'
        acknowledged = False

        while not acknowledged:
            self.receiver.write(msg.encode())
            bytes = self.receiver.read(self.receiver.in_waiting)
            if 'ok' in bytes.decode('utf-8'):
                acknowledged = True
                print("Handshake complete!")
                return
            print("Waiting...")
            time.sleep(0.5)

    def listen(self):

        startSequence = r"11111111 >> ([0-9]*)"
        stopSequence = r"([0-9]*) >> ([0-9]*)"
        datastream = str("")
        amplitudes = []

        while True:
            bytes = self.receiver.read(self.receiver.in_waiting)
            decoded_bytes = bytes.decode('utf-8')
            if decoded_bytes != "":
                datastream = str(datastream) + decoded_bytes
                print(datastream)
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