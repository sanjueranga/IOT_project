import serial
import time
from config import Config

import re


class SerialReader:
    def __init__(self):
        self.ser = serial.Serial(Config.SERIAL_PORT, Config.BAUD_RATE, timeout=0) # non-blocking
        time.sleep(2)  # allow ESP32 reset
        self.ser.reset_input_buffer()  # <-- flush old serial data

    def read_line(self):
        try:
            line = self.ser.readline().decode("utf-8").strip()
            if line:
                return self.parse_line(line)
        except Exception as e:
            print("Serial read error:", e)
        return None

    def parse_line(self, line):
        # Example: Humidity: 61.00% | Temp: 27.00C/80.60F | Passengers: 19 | Distance: 29.43 cm | GPS: 6.927100, 79.861200 | Buzzer: OFF
        pattern = (
            r"Humidity: ([\d.]+)% \| "
            r"Temp: ([\d.]+)C/([\d.]+)F \| "
            r"Passengers: (\d+) \| "
            r"Distance: ([\d.]+) cm \| "
            r"GPS: ([\d.-]+), ([\d.-]+) \| "
            r"Buzzer: (ON|OFF)"
        )
        match = re.match(pattern, line)
        if match:
            return {
                "humidity": float(match.group(1)),
                "temp_c": float(match.group(2)),
                "temp_f": float(match.group(3)),
                "passengers": int(match.group(4)),
                "distance": float(match.group(5)),
                "latitude": float(match.group(6)),
                "longitude": float(match.group(7)),
                "buzzer": match.group(8),
            }
        return None
