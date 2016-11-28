import serial
import threading


class PairOfPorts():
    def __init__(self, port, func=(lambda string: print(string))):
        self.WritingPort = serial.Serial(port, timeout=1)
        self.ReadingPort = serial.Serial(port, timeout=1)
        read_thread = threading.Thread(target=self.read, name="reader", args=[func])
        self.need_to_read = True
        read_thread.start()

    def write(self, data):
        message = data.encode("ascii")
        message.replace(b'\x7e', b'\x7d\x5e')
        message.replace(b'\x7d', b'\x7d\x5d')
        message.replace(b'\x7c', b'\x7b\x5c')
        message.replace(b'\x7b', b'\x7b\x5b')
        message = b'\x7e' + message + b'\x7c'
        self.WritingPort.write(message)

    def read(self, func=(lambda string: print(string))):
        while self.need_to_read:
            message = b''
            data = self.ReadingPort.read(1)
            if data != b'\x7e':
                continue
            else:
                data = self.ReadingPort.read(1)
            while data != b'\x7c':
                message += data
                data = self.ReadingPort.read(1)
            if len(message):
                data.replace(b'\x7d\x5e', b'\x7e')
                data.replace(b'\x7d\x5d', b'\x7d')
                data.replace(b'\x7b\x5c', b'\x7c')
                data.replace(b'\x7b\x5b', b'\x7b')
                func(message)

    def stop(self):
        self.need_to_read = False