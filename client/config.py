from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SERIAL_PORT = os.getenv("SERIAL_PORT", "COM3")
    BAUD_RATE = int(os.getenv("BAUD_RATE", "115200"))
    SERVER_URL = os.getenv("SERVER_URL", "http://localhost:5000/api/data")
    READ_INTERVAL = int(os.getenv("READ_INTERVAL", "1"))
