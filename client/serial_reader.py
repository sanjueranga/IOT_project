import serial
import time
import json
import logging
import re
from config import Config

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

class SerialReader:
    def __init__(self):
        try:
            self.ser = serial.Serial(Config.SERIAL_PORT, Config.BAUD_RATE, timeout=1)
            logger.info(f"Connected to {Config.SERIAL_PORT} at {Config.BAUD_RATE} baud")
            time.sleep(2)  # allow ESP32 reset
            self.ser.reset_input_buffer()  # flush old serial data
        except Exception as e:
            logger.error(f"Failed to connect to serial port: {e}")
            self.ser = None

    def read_line(self):
        """Read and parse data from ESP32."""
        if not self.ser or not self.ser.is_open:
            logger.warning("Serial connection not available")
            return None

        try:
            if self.ser.in_waiting > 0:
                line = self.ser.readline().decode("utf-8").strip()
                if line:
                    logger.debug(f"Raw data: {line}")
                    return self.parse_line(line)
        except Exception as e:
            logger.error(f"Serial read error: {e}")
        return None

    def parse_line(self, line):
        """Parse ESP32 data format into JSON structure."""
        try:
            # Try JSON parsing first (in case ESP32 sends JSON)
            data = json.loads(line)
            logger.info(f"Parsed JSON data: {data}")
            return data
        except json.JSONDecodeError:
            # Parse the ESP32 human-readable format
            return self.parse_esp32_format(line)

    def parse_esp32_format(self, line):
        """Parse ESP32 human-readable format."""
        try:
            data = {}

            # Extract humidity: "Humidity: 51.00%"
            humidity_match = re.search(r"Humidity:\s*([\d.]+)%", line)
            if humidity_match:
                data["humidity"] = float(humidity_match.group(1))

            # Extract temperature: "Temp: 29.40C/84.92F"
            temp_match = re.search(r"Temp:\s*([\d.]+)C/([\d.]+)F", line)
            if temp_match:
                data["temp_c"] = float(temp_match.group(1))
                data["temp_f"] = float(temp_match.group(2))

            # Extract passengers: "Passengers: 96"
            passengers_match = re.search(r"Passengers:\s*(\d+)", line)
            if passengers_match:
                data["passengers"] = int(passengers_match.group(1))

            # Extract distance: "Distance: 22.29 cm"
            distance_match = re.search(r"Distance:\s*([\d.]+)\s*cm", line)
            if distance_match:
                data["distance"] = float(distance_match.group(1))

            # Extract GPS: "GPS: 6.927100, 79.861200"
            gps_match = re.search(r"GPS:\s*([\d.-]+),\s*([\d.-]+)", line)
            if gps_match:
                data["latitude"] = float(gps_match.group(1))
                data["longitude"] = float(gps_match.group(2))

            # Extract buzzer status: "Buzzer OFF" or "Buzzer ON"
            if "Buzzer OFF" in line:
                data["buzzer"] = "OFF"
            elif "Buzzer ON" in line:
                data["buzzer"] = "ON"
            else:
                data["buzzer"] = "OFF"  # Default

            # Add timestamp
            data["timestamp"] = time.time()

            # Extract status message if present
            status_match = re.search(r"Status:\s*(.+?)(?:\s*Buzzer|$)", line)
            if status_match:
                data["status"] = status_match.group(1).strip()

            if data:
                logger.debug(f"Parsed ESP32 data: {data}")
                return data
            else:
                logger.warning(f"Could not parse any data from: {line}")
                return None

        except Exception as e:
            logger.error(f"Error parsing ESP32 format: {e}")
            return None
