import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from .api import router as api_router

app = FastAPI(title="IoT Dashboard")

# API routes
app.include_router(api_router, prefix="/api")

# Serve static dashboard
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir, html=True), name="static")

# --- WebSocket support ---
connected_clients = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            # Receive data from client
            data = await websocket.receive_text()
            
            # Optional: print data server-side
            print("Received from client:", data)

            # Broadcast to all connected clients (e.g., frontend)
            for client in connected_clients:
                await client.send_text(data)

    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        print("Client disconnected")
