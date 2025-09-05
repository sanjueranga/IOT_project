import asyncio
import websockets
import json
import time
from utils.logger import get_logger
from config import Config

logger = get_logger(__name__)


class Sender:
    def __init__(self):
        self.uri = Config.SERVER_WS_URL
        self.websocket = None
        self.reconnect_attempts = 0
        self.max_reconnect_delay = Config.WS_MAX_RECONNECT_DELAY
        self.base_reconnect_delay = Config.WS_BASE_RECONNECT_DELAY

        # Batching configuration from config
        self.batch_enabled = Config.BATCH_ENABLED
        self.batch_size = Config.BATCH_SIZE
        self.batch_timeout = Config.BATCH_TIMEOUT
        self.batch_buffer = []
        self.last_batch_time = time.time()

    async def connect(self):
        """Connect to server with exponential backoff."""
        while True:
            try:
                self.websocket = await websockets.connect(
                    self.uri,
                    ping_interval=Config.WS_PING_INTERVAL,
                    ping_timeout=Config.WS_PING_TIMEOUT,
                )
                logger.info("WebSocket connected to server")
                self.reconnect_attempts = 0  # Reset on successful connection
                return

            except Exception as e:
                # Exponential backoff with jitter
                delay = min(
                    self.base_reconnect_delay * (2**self.reconnect_attempts),
                    self.max_reconnect_delay,
                )
                jitter = (
                    delay * 0.1 * (2 * asyncio.get_event_loop().time() - 1)
                )  # ±10% jitter
                total_delay = delay + jitter

                self.reconnect_attempts += 1
                logger.error(
                    f"WebSocket connection error (attempt {self.reconnect_attempts}): {e}"
                )
                logger.info(f"Retrying in {total_delay:.2f} seconds...")

                await asyncio.sleep(total_delay)

    async def send_batch(self, force=False):
        """Send batched data if conditions are met."""
        current_time = time.time()
        time_since_last = current_time - self.last_batch_time

        should_send = (
            force
            or len(self.batch_buffer) >= self.batch_size
            or time_since_last >= self.batch_timeout
        )

        if should_send and self.batch_buffer:
            try:
                # Prepare batch message
                batch_data = {
                    "type": "batch",
                    "timestamp": current_time,
                    "count": len(self.batch_buffer),
                    "data": self.batch_buffer,
                }

                if await self._send_raw(json.dumps(batch_data)):
                    logger.info(f"Sent batch of {len(self.batch_buffer)} readings")
                    self.batch_buffer.clear()
                    self.last_batch_time = current_time

            except Exception as e:
                logger.error(f"Error sending batch: {e}")

    async def _send_raw(self, message):
        """Internal method to send raw message."""
        if (
            self.websocket is None
            or self.websocket.state != websockets.protocol.State.OPEN
        ):
            await self.connect()
            if (
                self.websocket is None
                or self.websocket.state != websockets.protocol.State.OPEN
            ):
                logger.error("Failed to establish connection, skipping send")
                return False

        try:
            await self.websocket.send(message)
            return True
        except Exception as e:
            logger.error(f"WebSocket send error: {e}")
            self.websocket = None  # force reconnect next time
            return False

    async def send(self, data):
        """Send data, with optional batching."""
        if not data:
            return

        if self.batch_enabled:
            # Add to batch
            self.batch_buffer.append({"timestamp": time.time(), **data})

            # Send batch if conditions are met
            await self.send_batch()

        else:
            # Send immediately (legacy mode)
            message = json.dumps(data)
            if await self._send_raw(message):
                logger.info(f"Sent: {message}")

    async def flush(self):
        """Force send any pending batched data."""
        if self.batch_enabled and self.batch_buffer:
            await self.send_batch(force=True)
