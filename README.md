# ✈️ KLM Cargo Optimization - Aviation Fuel Savings Through Strategic Weight Distribution

**Author:** María Emilia Venezian Juricic  
**Supervisor:** Dr. Felipe Delgado  
**Institution:** Pontificia Universidad Católica de Chile  
**Date:** 2025

---

## 🎯 Project Overview

This thesis develops and tests a Mixed Integer Linear Programming (MILP) model to optimize aircraft cargo loading for fuel efficiency on KLM intercontinental flights. The model combines:
- **1D Bin Packing Problem (1D-BPP):** Assigning cargo items to Unit Load Devices (ULDs)
- **Weight & Balance (W&B):** Positioning ULDs in aircraft to maximize %MAC (Mean Aerodynamic Chord)

**Key Result:** Average fuel savings of **0.47%** (~360 kg) per flight, outperforming KLM's current optimization by 145 kg/flight.

---

## 📁 Project Structure

### **🔧 Main Model Files**
- `Model.ipynb` - **DelgadoVenezian Model** (our improved MILP)
- `Model_Puttaert.ipynb` - Puttaert's original model
- `Baseline.ipynb` - Sequential approach (1D-BPP → 3D-BPP → W&B)
- `Optimized_Actual.ipynb` - W&B-focused (no re-packing)
- `BAX_Fixed.ipynb` - Puttaert + fixed BAX positions
- `Classes.ipynb` - Core classes (Aircraft, Cargo_Item, ULD)

### **▶️ Execution Scripts**
- `Run - Model.ipynb` - Run DelgadoVenezian model
- `Run - Baseline.ipynb` - Run Baseline model
- `Run - Optimized_Actual.ipynb` - Run Optimized_Actual model
- `Run - BAX Fixed.ipynb` - Run BAX_Fixed model
- `Run_All_Flights.ipynb` - Batch run all 102 flights

### **📊 Analysis & Results**
- `Read - Model Results.ipynb` - Analyze DelgadoVenezian results
- `Read - Baseline Results.ipynb` - Analyze Baseline results
- `Read - Optimized Actual Results.ipynb` - Analyze Optimized_Actual results
- `Read - BAX Fixed Results.ipynb` - Analyze BAX_Fixed results
- `Read - Results Comparison.ipynb` - **Compare all models** ⭐
- `Map.ipynb` - Visualization of aircraft cargo maps

### **📂 Data & Results Folders**
- `Data/` - Flight data (102 flights)
- `Inputfiles/` - Configuration files (aircraft specs, load locations, etc.)
- `Results/` - DelgadoVenezian model results
- `Results_Baseline/` - Baseline results
- `Results_Optimized_Actual/` - Optimized_Actual results
- `Results_BAX_Fixed/` - BAX_Fixed results
- `Results Puttaert/` - Puttaert model results

### **📚 Documentation & Processing**
- `processing/` - **Organized analysis pipeline** ⭐
  - `01_data_analysis/` - Data exploration and statistics
  - `02_infeasibility_analysis/` - Model feasibility analysis
  - `03_heuristic_development/` - Heuristic improvements
  - `04_visualization/` - Plots and animations
  - `05_documentation/` - General documentation
  - **`06_model_verification/`** - Bug analysis (11 bugs found) ⭐
  - **`07_communications/`** - Emails to advisor
  - `08_analysis_scripts/` - Utility Python scripts
  - `99_archive/` - Old files and superseded docs
- `latex_models/` - Mathematical formulations in LaTeX

---

## 🚀 Quick Start

### **1. Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### **2. Run a Single Flight**
Open and run any of the `Run - [Model].ipynb` notebooks.

### **3. Compare All Models**
Open `Read - Results Comparison.ipynb` to see comparative analysis.

---

## 🐛 Important: Bug Analysis (October 2025)

**11 bugs were discovered** in benchmark models during deep verification. See `processing/06_model_verification/reports/MASTER_BUG_MATRIX.md` for complete analysis.

**Critical bugs affecting all benchmarks:**
- Bug #1: Compartment weight constraints (per-position instead of per-compartment)
- Bug #10: COL/CRT temperature logic (per-position instead of compartment-level)

**Status:**
- ✅ DelgadoVenezian: 0 bugs (all correct)
- ⚠️ Baseline: 4 bugs (3 critical)
- ⚠️ Optimized_Actual: 3 bugs (2 critical)
- ⚠️ BAX_Fixed: 7 bugs (4 critical)
- ⚠️ Puttaert: 8 bugs (4 critical) - not in final comparison

**Action:** Fixing all bugs in Baseline, Optimized_Actual, and BAX_Fixed for fair comparison.

---

## 📖 Model Descriptions

### **DelgadoVenezian Model (Our Model)**
**File:** `Model.ipynb`  
**Type:** Integrated 1D-BPP + W&B MILP  
**Key Features:**
- Aircraft-specific %MAC calculation
- Temperature-sensitive cargo handling (COL/CRT)
- Booking separation optimization (Y/Z variables)
- Overlapping position logic
- Feedback loop for deferred items

### **Baseline (Sequential)**
**File:** `Baseline.ipynb`  
**Type:** 3-stage sequential approach  
**Stages:**
1. 1D-BPP: Assign items to ULDs (minimize ULDs, volume preference)
2. 3D-BPP: Pack items physically using extreme points
3. W&B: Assign ULDs to positions (maximize %MAC)

### **Optimized_Actual (W&B-focused)**
**File:** `Optimized_Actual.ipynb`  
**Type:** W&B only (no re-packing)  
**Logic:** Takes actual ULD configurations and only optimizes positions

### **BAX_Fixed**
**File:** `BAX_Fixed.ipynb`  
**Type:** Puttaert + fixed BAX positions  
**Difference:** Fixes BAX container positions to actual flight data

### **Puttaert**
**File:** `Model_Puttaert.ipynb`  
**Type:** Original integrated MILP  
**Note:** Not included in final comparison (superseded by DelgadoVenezian)

---

## 📊 Results Summary (102 Flights)

| Model | Avg %MAC ZFW | Fuel Savings | Runtime | Bugs |
|-------|--------------|--------------|---------|------|
| **DelgadoVenezian** | Highest | 360 kg | 153s | 0 ✅ |
| KLM Optimization | Baseline | 215 kg | N/A | N/A |
| Baseline | TBD | TBD | TBD | 4 ⚠️ |
| Optimized_Actual | TBD | TBD | TBD | 3 ⚠️ |
| BAX_Fixed | TBD | TBD | TBD | 7 ⚠️ |

*Note: TBD values to be updated after bug fixes applied*

---

## 📧 Contact

**María Emilia Venezian Juricic**  
Pontificia Universidad Católica de Chile  
Email: [your-email]

**Supervisor:**  
Dr. Felipe Delgado  
Department of Transport Engineering and Logistics

---

## 📝 Citation

If you use this work, please cite:
```
Venezian, M.E. (2025). Fuel Optimization in KLM Intercontinental Flights 
through Cargo Palletization and Weight Balance Modeling. 
Undergraduate Thesis, Pontificia Universidad Católica de Chile.
```

---

**Last Updated:** October 2025
