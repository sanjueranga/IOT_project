## Getting Started

### 1. Create and Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

### 3. Run the Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## Static Files

- Static files are located in the `app/static/` directory.

---

## API Endpoints

Visit:
👉 http://localhost:8000 → Dashboard

👉 http://localhost:8000/api/data → JSON


uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
