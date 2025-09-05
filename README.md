# IoT Project

A real-time IoT monitoring system with a Python client for data collection and a FastAPI server for data visualization.

## Project Structure
```
├── client/               # Client application
│   ├── utils/           # Utility functions
│   ├── client.py        # Main client application
│   ├── config.py        # Client configuration
│   ├── sender.py        # Data sender module
│   └── serial_reader.py # Serial port reader
├── server/              # Server application
│   └── app/            
│       ├── static/      # Static files (HTML, CSS, JS)
│       ├── api.py       # API endpoints
│       └── main.py      # Main server application
└── requirements.txt     # Project dependencies
```

## Prerequisites

- Python 3.10 or higher
- Virtual environment
- Serial device (ESP32) connected to your computer

## Installation

1. Clone the repository:
```bash
git clone https://github.com/sanjueranga/IOT_project.git
cd IOT_project
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
.\.venv\Scripts\activate  # Windows
source .venv/bin/activate # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

### Client
Create a `.env` file in the client directory with:
```env
SERIAL_PORT=COM3  # Replace with your device's port
BAUD_RATE=115200
READ_INTERVAL=0.001
SERVER_URL=http://localhost:8000/api/data
```

## Running the Application

1. Start the server:
```bash
uvicorn server.app.main:app --reload
```
Server will be available at http://localhost:8000

2. In a new terminal, start the client:
```bash
python client/client.py
```

## Features

- Real-time data collection from IoT device
- WebSocket communication for live updates
- Dashboard for data visualization
- REST API endpoints for data access
- Configurable sampling rates and connection parameters

## API Endpoints

- `GET /api/data` - Get collected data
- `POST /api/data` - Submit new data point
- `WS /ws` - WebSocket endpoint for real-time updates