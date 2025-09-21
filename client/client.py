import asyncio
import signal
import sys
import logging
import time
from serial_reader import SerialReader
from sender import Sender
from config import Config

# Set up detailed logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("iot_client.log"), logging.StreamHandler()],
)
logger = logging.getLogger("Client")


class IoTClient:
    def __init__(self):
        self.reader = SerialReader()
        self.sender = Sender()
        self.running = False
        self.data_count = 0
        self.last_data_time = time.time()

    async def start(self):
        """Start the IoT client with proper error handling."""
        self.running = True

        # Setup graceful shutdown
        def signal_handler():
            logger.info("Shutdown signal received, cleaning up...")
            self.running = False

        signal.signal(signal.SIGINT, lambda s, f: signal_handler())
        signal.signal(signal.SIGTERM, lambda s, f: signal_handler())

        # Check serial connection
        if not self.reader.ser:
            logger.error("Failed to connect to ESP32. Check COM port and cable.")
            return

        # Connect to WebSocket server
        await self.sender.connect()
        logger.info("IoT Client started, listening to ESP32...")

        try:
            while self.running:
                # Read from ESP32
                data = self.reader.read_line()

                if data:
                    self.data_count += 1
                    self.last_data_time = time.time()
                    logger.info(f"Data #{self.data_count} received: {data}")

                    # Send to server
                    await self.sender.send(data)
                else:
                    # Check if we haven't received data for a while
                    if time.time() - self.last_data_time > 10:  # 10 seconds
                        logger.warning("No data received from ESP32 for 10 seconds")
                        self.last_data_time = time.time()  # Reset timer

                # Sleep according to config
                await asyncio.sleep(Config.READ_INTERVAL)

        except KeyboardInterrupt:
            logger.info("KeyboardInterrupt received")
        except Exception as e:
            logger.error(f"Unexpected error in main loop: {e}")
        finally:
            await self.cleanup()

    async def cleanup(self):
        """Clean up resources."""
        logger.info("Cleaning up...")
        try:
            # Flush any pending batched data
            await self.sender.flush()

            # Close WebSocket connection gracefully
            if self.sender.websocket and not self.sender.websocket.closed:
                await self.sender.websocket.close()

            # Close serial connection
            if self.reader.ser and self.reader.ser.is_open:
                self.reader.ser.close()
                logger.info("Serial connection closed")

        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

        logger.info("Cleanup complete")


async def main():
    """Main entry point with improved error handling."""
    client = IoTClient()

    try:
        await client.start()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutdown complete.")
    except Exception as e:
        logger.error(f"Failed to start client: {e}")
        sys.exit(1)
