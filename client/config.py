from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SERIAL_PORT = os.getenv("SERIAL_PORT", "COM5")
    BAUD_RATE = int(os.getenv("BAUD_RATE", "115200"))
    SERVER_URL = os.getenv("SERVER_URL", "http://localhost:8000/api/data")
    READ_INTERVAL =float(os.getenv("READ_INTERVAL", "0.01"))
