import serial
import time
from config import Config

import re


class SerialReader:
    def __init__(self):
        self.ser = serial.Serial(Config.SERIAL_PORT, Config.BAUD_RATE, timeout=1)
        time.sleep(2)  # allow ESP32 reset

    def read_line(self):
        if self.ser.in_waiting > 0:
            line = self.ser.readline().decode("utf-8").strip()
            return self.parse_line(line)
        return None

    def parse_line(self, line):
        # Example: Humidity: 55.00% | Temp: 28.40C/83.12F | Passengers: 43 | Distance: 18.72 cm | Buzzer: OFF
        pattern = r"Humidity: ([\d.]+)% \| Temp: ([\d.]+)C/([\d.]+)F \| Passengers: (\d+) \| Distance: ([\d.]+) cm \| Buzzer: (ON|OFF)"
        match = re.match(pattern, line)
        if match:
            return {
                "humidity": float(match.group(1)),
                "temp_c": float(match.group(2)),
                "temp_f": float(match.group(3)),
                "passengers": int(match.group(4)),
                "distance": float(match.group(5)),
                "buzzer": match.group(6),
            }
        return None
