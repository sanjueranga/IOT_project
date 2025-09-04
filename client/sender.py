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
        self.websocket = await websockets.connect(self.uri)
        logger.info("WebSocket connected to server")

    async def send(self, data):
        if self.websocket and data:
            try:
                message = json.dumps(data)
                await self.websocket.send(message)
                logger.info(f"Sent: {message}")
            except Exception as e:
                logger.error(f"WebSocket send error: {e}")
