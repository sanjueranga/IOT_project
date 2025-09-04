import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .api import router as api_router

app = FastAPI(title="IoT Dashboard")

# API routes
app.include_router(api_router, prefix="/api")

# Serve static dashboard
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")