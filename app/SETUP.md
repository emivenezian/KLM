# 🚀 Setup Instructions

## Prerequisites

- **Python 3.8+** (check with `python --version`)
- **Node.js 16+** (check with `node --version`)
- **npm** (comes with Node.js)
- **Gurobi license** (local installation)

## Quick Start

### 1. Backend Setup

```bash
# Navigate to backend directory
cd app/backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the backend server
uvicorn main:app --reload --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 2. Frontend Setup

**In a new terminal:**

```bash
# Navigate to frontend directory
cd app/frontend

# Install dependencies (this may take a few minutes)
npm install

# Start the development server
npm start
```

The dashboard will automatically open at:
- **Dashboard**: http://localhost:3000

## Testing with Synthetic Data

You can generate synthetic flight data for testing:

```python
# In Python console or script
from app.backend.services.synthetic_data import generate_synthetic_flight

# Generate synthetic data
files = generate_synthetic_flight(
    num_items=50,
    num_ulds=10,
    weight_range=(100, 1000),
    flight_number="SYN001",
    departure_airport="AMS",
    arrival_airport="SIN"
)

print(f"Generated files in: {files['output_directory']}")
```

Then use the flight path in the dashboard: `app/data/synthetic`

## Configuration

### Backend Configuration

Edit `app/backend/config.py` to customize:
- Data paths
- CORS origins
- Model settings

### Frontend Configuration

Edit `app/frontend/src/config.ts` to change:
- API base URL (if backend runs on different port)

## Google Sheets Export (Optional)

1. Create a Google Cloud Project
2. Enable Google Sheets API
3. Create service account credentials
4. Download JSON credentials file
5. Update `app/backend/config.py`:
   ```python
   GOOGLE_SHEETS_CREDENTIALS_PATH = "path/to/credentials.json"
   GOOGLE_SHEETS_ENABLED = True
   ```
6. Share your target Google Sheet with the service account email

## Troubleshooting

### Backend Issues

**Import errors:**
- Make sure you're in the `app/backend` directory
- Activate the virtual environment
- Check that all dependencies are installed: `pip list`

**Port already in use:**
- Change port: `uvicorn main:app --reload --port 8001`

**Gurobi errors:**
- Verify Gurobi license is installed
- Check environment variables are set correctly

### Frontend Issues

**npm install fails:**
- Clear npm cache: `npm cache clean --force`
- Delete `node_modules` and `package-lock.json`, then `npm install` again

**Port 3000 in use:**
- React will automatically use port 3001, 3002, etc.

**API connection errors:**
- Verify backend is running on port 8000
- Check CORS settings in `backend/config.py`
- Verify API URL in `frontend/src/config.ts`

## Next Steps

1. **Test with real flight data**: Use flights from `Data/` folder
2. **Generate synthetic data**: Test edge cases and bottlenecks
3. **Integrate actual model**: Replace mock data in `model_executor.py` with real model execution
4. **Add features**: Historical analysis, batch processing, etc.

## Development Notes

- Backend uses FastAPI with automatic API documentation
- Frontend uses React with TypeScript
- All visualization data comes from backend API
- Current MVP uses mock data - integrate actual model execution in Phase 2

