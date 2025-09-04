from fastapi import APIRouter
from .storage import Storage
from .models import SensorData

router = APIRouter()
storage = Storage()


@router.post("/data")
def receive_data(data: SensorData):
    storage.add_data(data.dict())
    return {"status": "ok"}


@router.get("/data")
def get_data():
    return {"values": storage.get_all()}
