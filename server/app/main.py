import os
import json
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from .api import router as api_router

app = FastAPI(title="IoT Dashboard")

# API routes
app.include_router(api_router, prefix="/api")

# Serve static dashboard
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir, html=True), name="static")

# --- WebSocket support with performance optimizations ---
connected_clients = []
broadcast_queue = asyncio.Queue()
last_broadcast_data = None


async def broadcast_worker():
    """Background worker to handle efficient broadcasting."""
    global last_broadcast_data

    while True:
        try:
            # Wait for data to broadcast
            data = await broadcast_queue.get()

            # Skip if same data was just broadcast (debouncing)
            if data == last_broadcast_data:
                continue

            last_broadcast_data = data

            # Broadcast to all connected clients efficiently
            if connected_clients:
                disconnected_clients = []

                for client in connected_clients:
                    try:
                        await client.send_text(data)
                    except Exception:
                        # Mark for removal if send fails
                        disconnected_clients.append(client)

                # Remove disconnected clients
                for client in disconnected_clients:
                    if client in connected_clients:
                        connected_clients.remove(client)

        except Exception as e:
            print(f"Broadcast worker error: {e}")


# Start the broadcast worker
asyncio.create_task(broadcast_worker())


def process_message(raw_data):
    """Process incoming message and extract latest sensor data."""
    try:
        parsed_data = json.loads(raw_data)

        # Handle batched data
        if parsed_data.get("type") == "batch" and "data" in parsed_data:
            # Extract the latest reading from the batch
            batch_data = parsed_data["data"]
            if batch_data:
                return json.dumps(batch_data[-1])  # Return latest reading
        else:
            # Single reading
            return raw_data

    except json.JSONDecodeError:
        # If not valid JSON, return as-is
        return raw_data

    return None


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    print(f"Client connected. Total clients: {len(connected_clients)}")

    try:
        while True:
            # Receive data from client
            raw_data = await websocket.receive_text()

            # Process the message (handle batching)
            processed_data = process_message(raw_data)

            if processed_data:
                # Add to broadcast queue (non-blocking)
                try:
                    broadcast_queue.put_nowait(processed_data)
                except asyncio.QueueFull:
                    print("Broadcast queue full, skipping message")

    except WebSocketDisconnect:
        if websocket in connected_clients:
            connected_clients.remove(websocket)
        print(f"Client disconnected. Total clients: {len(connected_clients)}")
    except Exception as e:
        print(f"WebSocket error: {e}")
        if websocket in connected_clients:
            connected_clients.remove(websocket)
