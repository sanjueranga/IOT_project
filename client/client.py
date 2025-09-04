import time
from serial_reader import SerialReader
from sender import Sender
from config import Config
from utils.logger import get_logger

logger = get_logger("Client")


def main():
    reader = SerialReader()
    sender = Sender()

    logger.info("Client started, listening to ESP32...")

    while True:
        line = reader.read_line()
        if line:
            logger.info(f"Received: {line}")
            sender.send(line)
        time.sleep(Config.READ_INTERVAL)


if __name__ == "__main__":
    main()
