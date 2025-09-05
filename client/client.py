import asyncio
import signal
import sys
from serial_reader import SerialReader
from sender import Sender
from utils.logger import get_logger

logger = get_logger("Client")


class IoTClient:
    def __init__(self):
        self.reader = SerialReader()
        self.sender = Sender()
        self.running = False

    async def start(self):
        """Start the IoT client with proper error handling."""
        self.running = True

        # Setup graceful shutdown
        def signal_handler():
            logger.info("Shutdown signal received, cleaning up...")
            self.running = False

        signal.signal(signal.SIGINT, lambda s, f: signal_handler())
        signal.signal(signal.SIGTERM, lambda s, f: signal_handler())

        await self.sender.connect()  # initial connection
        logger.info("IoT Client started, listening to ESP32...")

        try:
            while self.running:
                line = self.reader.read_line()
                if line:
                    await self.sender.send(line)  # send via persistent WS with batching

                # Small sleep to prevent excessive CPU usage
                await asyncio.sleep(0.01)  # 10ms sleep for better performance

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
