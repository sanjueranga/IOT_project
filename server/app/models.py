from pydantic import BaseModel
from typing import Literal


class SensorData(BaseModel):
    humidity: float
    temp_c: float
    temp_f: float
    passengers: int
    distance: float
    buzzer: Literal["ON", "OFF"]
