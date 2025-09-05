from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    # Serial connection settings
    SERIAL_PORT = os.getenv("SERIAL_PORT", "COM5")
    BAUD_RATE = int(os.getenv("BAUD_RATE", "115200"))
    READ_INTERVAL = float(
        os.getenv("READ_INTERVAL", "0.01")
    )  # Increased from 0.001 for better performance

    # Server connection settings
    SERVER_URL = os.getenv("SERVER_URL", "http://localhost:8000/api/data")
    SERVER_WS_URL = os.getenv("SERVER_WS_URL", "ws://localhost:8000/ws")

    # Performance optimization settings
    BATCH_ENABLED = os.getenv("BATCH_ENABLED", "true").lower() == "true"
    BATCH_SIZE = int(os.getenv("BATCH_SIZE", "5"))  # Send every 5 readings
    BATCH_TIMEOUT = float(os.getenv("BATCH_TIMEOUT", "2.0"))  # Or every 2 seconds

    # WebSocket reconnection settings
    WS_BASE_RECONNECT_DELAY = float(os.getenv("WS_BASE_RECONNECT_DELAY", "1.0"))
    WS_MAX_RECONNECT_DELAY = float(os.getenv("WS_MAX_RECONNECT_DELAY", "30.0"))
    WS_PING_INTERVAL = int(os.getenv("WS_PING_INTERVAL", "10"))
    WS_PING_TIMEOUT = int(os.getenv("WS_PING_TIMEOUT", "5"))
