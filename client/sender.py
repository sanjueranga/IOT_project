import requests
from config import Config
from utils.logger import get_logger

logger = get_logger(__name__)


class Sender:
    def __init__(self):
        self.url = Config.SERVER_URL

    def send(self, data):
        if not data:
            return
        try:
            response = requests.post(self.url, json=data, timeout=5)
            logger.info(f"Sent: {data}, Response: {response.status_code}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending to server: {e}")
