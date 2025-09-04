from fastapi import APIRouter
from pydantic import BaseModel
from .storage import Storage

router = APIRouter()
storage = Storage()

class SensorData(BaseModel):
    value: float

@router.post("/data")
def receive_data(data: SensorData):
    storage.add_data(data.value)
    return {"status": "ok"}

@router.get("/data")
def get_data():
    return {"values": storage.get_all()}
