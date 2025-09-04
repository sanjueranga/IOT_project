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
- They are served at the `/static/` URL endpoint.
- Example: `http://localhost:8000/static/yourfile.png`

---

## API Endpoints

- Main API root: `http://localhost:8000/`
- Documentation (if using FastAPI):  
    - Swagger UI: `http://localhost:8000/docs`  
    - ReDoc: `http://localhost:8000/redoc`
- Access static files: `http://localhost:8000/static/<filename>`


uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
