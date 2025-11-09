# ⚡ Quick Start Guide

## What Was Built

✅ **Complete MVP Dashboard Application** with:
- FastAPI backend API
- React TypeScript frontend
- Visualization components for weight distribution, ULD utilization
- Synthetic data generator for testing
- Google Sheets export capability

## Start the Application

### Terminal 1 - Backend
```bash
cd app/backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Terminal 2 - Frontend
```bash
cd app/frontend
npm install
npm start
```

Then open: **http://localhost:3000**

## Current Status

### ✅ What Works
- Flight selection from `Data/` folder
- API endpoints for optimization
- Visualization components (charts, metrics)
- Synthetic data generation
- Google Sheets export (if configured)

### ⚠️ What Needs Integration (Phase 2)
- **Actual model execution**: Currently `model_executor.py` returns mock data
  - Replace with real calls to your `Model.ipynb` logic
  - Import classes from `Classes.ipynb`
  - Execute actual Gurobi optimization
  
### 📝 Next Steps

1. **Integrate Real Model Execution**
   - Open `app/backend/services/model_executor.py`
   - Replace mock data with actual model calls
   - Import your existing classes (Cargo, Aircraft, ULD, etc.)
   - Execute the optimization and parse results

2. **Test with Real Data**
   - Use a flight from `Data/Flights AMSBLR FEB 2024/`
   - Verify results match notebook outputs

3. **Enhance Visualizations**
   - Add 3D cargo loading visualization
   - Add position-level weight distribution
   - Add fuel savings calculations

## File Structure

```
app/
├── backend/          # FastAPI API
│   ├── services/
│   │   └── model_executor.py  # ⚠️ Needs real model integration
│   └── main.py
├── frontend/        # React dashboard
│   └── src/
│       └── components/  # All visualization components
└── README.md        # Full documentation
```

## Need Help?

- **Backend API Docs**: http://localhost:8000/docs
- **See**: `app/SETUP.md` for detailed setup
- **See**: `app/README.md` for full documentation

---

**Status**: MVP Complete ✅ | Model Integration Pending ⚠️

