import serial
import time
from config import Config

class SerialReader:
    def __init__(self):
        self.ser = serial.Serial(Config.SERIAL_PORT, Config.BAUD_RATE, timeout=1)
        time.sleep(2)  # allow ESP32 reset

    def read_line(self):
        if self.ser.in_waiting > 0:
            line = self.ser.readline().decode("utf-8").strip()
            return line
        return None
