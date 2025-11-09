# Model Selection Guide

## How Model Selection Works

The dashboard allows you to select which optimization model to run. Here's how it maps to your notebooks:

### Model Type → Notebook Mapping

| Frontend Selection | `model_type` Parameter | Notebook File | Description |
|-------------------|------------------------|---------------|-------------|
| **DelgadoVenezian** | `delgado_venezian` | `Model.ipynb` | Your best model (89.8% success rate) |
| **Baseline** | `baseline` | `Baseline.ipynb` | Sequential approach (77.0% success rate) |
| **Optimized Actual** | `optimized_actual` | `Optimized_Actual.ipynb` | W&B-focused (84.6% success rate) |
| **BAX Fixed** | `bax_fixed` | `BAX_Fixed.ipynb` | Fixed BAX positions (66.8% success rate) |

## Flow Diagram

```
User selects model in dropdown
        ↓
Frontend sends: { model_type: "delgado_venezian" }
        ↓
Backend receives model_type
        ↓
model_runner.py maps:
  - "delgado_venezian" → loads Model.ipynb
  - "baseline" → loads Baseline.ipynb
  - "optimized_actual" → loads Optimized_Actual.ipynb
  - "bax_fixed" → loads BAX_Fixed.ipynb
        ↓
ProjectSetup.setup_project() called with flags:
  - baseline=False, optimized_actual=False, BAX_fixed=False (for delgado_venezian)
  - baseline=True, optimized_actual=False, BAX_fixed=False (for baseline)
  - baseline=False, optimized_actual=True, BAX_fixed=False (for optimized_actual)
  - baseline=False, optimized_actual=False, BAX_fixed=True (for bax_fixed)
        ↓
Extracts Python code from selected notebook
        ↓
Executes feedback_loop() function
        ↓
feedback_loop() calls:
  - solve_1D_BPP_WB() (MILP optimization)
  - solve_3D_BPP() (3D packing)
        ↓
Results saved to appropriate Results folder:
  - Results/ (for delgado_venezian)
  - Results_Baseline/ (for baseline)
  - Results_Optimized_Actual/ (for optimized_actual)
  - Results_BAX_Fixed/ (for bax_fixed)
```

## Code Location

- **Frontend selection**: `app/frontend/src/components/OptimizationControls.tsx`
- **Backend mapping**: `app/backend/services/model_runner.py` (lines 86-95)
- **ProjectSetup flags**: `app/backend/services/model_runner.py` (lines 67-82)

## Important Notes

1. **Each model uses the same input data** from `Data/` folder
2. **Results are saved separately** in different Results folders
3. **The model_type parameter controls**:
   - Which notebook code is executed
   - Which Results folder is used
   - Which ProjectSetup flags are set

## Default Model

The default selection is **DelgadoVenezian** (`Model.ipynb`), which is your best-performing model.

