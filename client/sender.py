import asyncio
import websockets
import json
from utils.logger import get_logger
from config import Config

logger = get_logger(__name__)

class Sender:
    def __init__(self):
        self.uri = Config.SERVER_WS_URL
        self.websocket = None

    async def connect(self):
        """Connect to server with ping_interval to keep connection alive."""
        try:
            self.websocket = await websockets.connect(
                self.uri,
                ping_interval=10,   # send ping every 10s
                ping_timeout=5      # wait up to 5s for pong
            )
            logger.info("WebSocket connected to server")
        except Exception as e:
            logger.error(f"WebSocket connection error: {e}")
            self.websocket = None

    async def send(self, data):
        """Send data, reconnect if needed."""
        if not data:
            return

        if self.websocket is None or self.websocket.state != websockets.protocol.State.OPEN:
            logger.info("WebSocket not connected, reconnecting...")
            await self.connect()
            if self.websocket is None or self.websocket.state != websockets.protocol.State.OPEN:
                logger.error("Reconnect failed, skipping send")
                return


        try:
            message = json.dumps(data)
            await self.websocket.send(message)
            logger.info(f"Sent: {message}")
        except Exception as e:
            logger.error(f"WebSocket send error: {e}")
            self.websocket = None  # force reconnect next loop
