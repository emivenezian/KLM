# ✈️ Aviation Cargo Optimization Dashboard

**Enterprise Web Application for Cargo Loading Optimization and Visualization**

## 💰 Business Value

- **Annual Savings**: **$10-20M USD** for KLM, **$8-15M USD** for LATAM
- **ROI**: 355-809% in Year 1, 567-1,233% Year 2+
- **Payback Period**: < 1 month
- **Environmental Impact**: 45,000-75,000 tons CO₂ reduction annually

📊 **See [VALUE_PROPOSITION.md](./VALUE_PROPOSITION.md) for detailed business case and ROI analysis**

## 🚀 Current Status

**✅ MVP Complete** - Ready for pilot testing with airlines.

**Fully Implemented:**
- ✅ Real-time optimization (Gurobi MILP)
- ✅ Comprehensive metrics (50+ KPIs)
- ✅ KLM actual data comparison
- ✅ Annual impact projections ($10-20M/year)
- ✅ Beautiful dashboard with visualization
- ✅ Three-tier fallback system (real-time → pre-computed → CSV)

📋 **See [NEXT_STEPS.md](./NEXT_STEPS.md) for development roadmap and unimplemented features**

## 🎯 Overview

This dashboard application provides a user-friendly interface for:
- Running cargo loading optimizations (DelgadoVenezian MILP model)
- Visualizing weight distribution (by compartment, left/right, position)
- Analyzing ULD utilization and cargo plans
- Exporting results to Google Sheets
- Testing with synthetic data to identify bottlenecks

## 📁 Structure

```
app/
├── backend/          # FastAPI backend service
│   ├── api/         # API endpoints
│   ├── services/    # Business logic (model execution, data processing)
│   ├── models/      # Data models/schemas
│   ├── utils/       # Helper functions
│   └── main.py      # FastAPI app entry point
│
├── frontend/        # React dashboard
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── pages/       # Dashboard pages
│   │   ├── services/    # API client
│   │   └── App.jsx
│   └── package.json
│
├── data/            # Data handling
│   └── synthetic/   # Synthetic data generator
│
└── README.md        # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Gurobi license (local)
- Google API credentials (for Sheets export - optional)

### Backend Setup

```bash
cd app/backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend Setup

```bash
cd app/frontend
npm install
npm start
```

The dashboard will be available at `http://localhost:3000`

## 📊 Features

### MVP (Week 1)
- ✅ Run optimization on flight data
- ✅ Visualize weight distribution:
  - By compartment (C1, C2, C3, C4)
  - Left vs Right side
  - By position
- ✅ ULD type analysis:
  - Proportion of ULD types used
  - ULD utilization metrics
- ✅ Cargo item details:
  - Items per ULD
  - Weight distribution
- ✅ Synthetic data generator for testing

### Phase 2 (Future)
- Historical flight analysis
- Batch processing
- Advanced analytics
- User authentication
- Email notifications

## 🔧 Configuration

### Backend Configuration
Edit `backend/config.py` for:
- Data paths (pointing to parent `Data/` folder)
- Gurobi settings
- Google Sheets API credentials

### Frontend Configuration
Edit `frontend/src/config.js` for:
- API endpoint URLs
- Default settings

## 📝 API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🔐 Google Sheets Export

1. Create a Google Cloud Project
2. Enable Google Sheets API
3. Create service account credentials
4. Place credentials file in `backend/config/`
5. Share target Google Sheet with service account email

## 🧪 Testing with Synthetic Data

Use the synthetic data generator to test edge cases:

```python
from app.backend.services.synthetic_data import generate_synthetic_flight

flight_data = generate_synthetic_flight(
    num_items=50,
    num_ulds=10,
    weight_range=(100, 1000)
)
```

## 📧 Support

For issues or questions, contact: [Your Email]

---

**Built for KLM Operations - Thesis Project 2025**

