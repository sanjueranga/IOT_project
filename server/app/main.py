from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .api import router as api_router

app = FastAPI(title="IoT Dashboard")

# API routes
app.include_router(api_router, prefix="/api")

# Serve static dashboard
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")
