import asyncio
from serial_reader import SerialReader
from sender import Sender
from utils.logger import get_logger

logger = get_logger("Client")

async def main():
    reader = SerialReader()
    sender = Sender()
    await sender.connect()  # persistent connection

    logger.info("Client started, listening to ESP32...")

    while True:
        line = reader.read_line()
        if line:
            await sender.send(line)  # send over persistent WS
        await asyncio.sleep(0.001)  # tiny sleep to avoid CPU overload

if __name__ == "__main__":
    asyncio.run(main())
