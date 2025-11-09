# Backend API

FastAPI backend for KLM Cargo Optimization.

## Structure

```
backend/
├── api/              # API endpoints
│   ├── optimization.py  # Optimization endpoints
│   └── export.py        # Export endpoints
├── services/         # Business logic
│   ├── model_executor.py      # Model execution
│   ├── visualization_data.py  # Visualization prep
│   ├── synthetic_data.py      # Synthetic data generator
│   └── google_sheets.py        # Google Sheets export
├── models/          # Data models/schemas
│   └── schemas.py   # Pydantic models
├── utils/           # Utilities
│   └── path_utils.py # Path helpers
├── config.py        # Configuration
└── main.py          # FastAPI app
```

## API Endpoints

### Optimization

- `POST /api/v1/optimization/run` - Run optimization
- `GET /api/v1/optimization/flights` - List available flights
- `POST /api/v1/optimization/synthetic/generate` - Generate synthetic data
- `POST /api/v1/optimization/visualization/prepare` - Prepare visualization data

### Export

- `POST /api/v1/export/sheets` - Export to Google Sheets
- `GET /api/v1/export/sheets/status` - Check Google Sheets status

## Running

```bash
cd app/backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

