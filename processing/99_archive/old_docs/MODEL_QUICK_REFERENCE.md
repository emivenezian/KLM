# 🚀 QUICK REFERENCE: Model Comparison

## Model Names & Mapping

| Code Name | Label in Results | Notebook File | Success Rate |
|-----------|-----------------|---------------|--------------|
| **Model** | DelgadoVenezian / Model | `Model.ipynb` | 89.8% 🥇 |
| **Optimized_Actual** | W&B-focused | `Optimized_Actual.ipynb` | 84.6% 🥈 |
| **Baseline** | Sequential | `Baseline.ipynb` | 77.0% 🥉 |
| **Model_Puttaert** | Puttaert | `Model_Puttaert.ipynb` | 72.1% |
| **BAX_Fixed** | BAX-fixed | `BAX_Fixed.ipynb` | 66.8% |
| **Actual** | Actual | (from data) | N/A ⭐ |

---

## One-Line Summaries

### 🏆 DelgadoVenezian (Model)
**"Your model"** - Integrated 1D-BPP + W&B with advanced separation constraints and volume maximization

### 💡 W&B-focused (Optimized_Actual)
**"Simple is best"** - Direct W&B optimization only, uses actual ULD packing from real flights

### 📦 Sequential (Baseline)
**"Three-stage cascade"** - 1D-BPP → 3D-BPP → W&B with feedback loop and volume preferences

### 🔧 Puttaert
**"Kitchen sink"** - Integrated model with ALL objectives and auxiliary weight variables

### 🔒 BAX-fixed
**"Constrained reality"** - Like Puttaert but BAX ULDs fixed to actual positions (fails often)

### 📊 Actual
**"Ground truth"** - Real KLM flight data from LoadLocationsSpotfire.csv

---

## Key Differences at a Glance

### Optimization Approach

```
DelgadoVenezian:  [1D-BPP + W&B + 3D-Packing Feedback]
W&B-focused:      [W&B ONLY, no packing]
Sequential:       [1D-BPP] → [3D-BPP] → [W&B]
Puttaert:         [1D-BPP + W&B + 3D-Packing Feedback]
BAX-fixed:        [1D-BPP + W&B + 3D-Packing Feedback + Fixed BAX]
```

### Variables Used

| Model | f | u | p | z | w | Other |
|-------|---|---|---|---|---|-------|
| DelgadoVenezian | ✅ | ✅ | ✅* | ✅ | ❌ | Y, Z |
| W&B-focused | ✅ | ❌ | ❌ | ❌ | ❌ | - |
| Sequential | ✅ | ✅ | ✅ | ❌ | ❌ | - |
| Puttaert | ✅ | ✅ | ✅ | ✅ | ✅ | - |
| BAX-fixed | ✅ | ✅ | ✅ | ✅ | ✅ | - |

*Only for regular ULDs (not BAX/BUP/T)

**Legend:**
- `f`: ULD to position assignment
- `u`: ULD opened/used
- `p`: Item to ULD assignment
- `z`: Item to ULD to position assignment
- `w`: Auxiliary weight variables
- `Y/Z`: Advanced separation variables

---

## Objective Functions (Priority Order)

### DelgadoVenezian
1. ⭐⭐⭐⭐⭐⭐ MAC
2. ⭐⭐⭐⭐⭐ Number of ULDs
3. ⭐⭐⭐⭐ Total Volume
4. ⭐⭐⭐ Separation (advanced)
5. ⭐⭐ BAX Proximity

### W&B-focused (Simplest!)
1. ⭐⭐ MAC
2. ⭐ BAX Proximity

### Sequential (Stage 1)
1. ⭐⭐⭐⭐ Volume Preference
2. ⭐⭐⭐ Number of ULDs
3. ⭐⭐ Underutilization Penalty
4. ⭐ Separation

### Puttaert (Most Complex!)
1. ⭐⭐⭐⭐⭐⭐ MAC
2. ⭐⭐⭐⭐⭐ Volume Preference
3. ⭐⭐⭐⭐ Number of ULDs
4. ⭐⭐⭐ Underutilization Penalty
5. ⭐⭐ Separation
6. ⭐ BAX Proximity

### BAX-fixed
Same as Puttaert, but BAX positions are FIXED

---

## Main Differences Explained

### DelgadoVenezian vs Puttaert
- ❌ No `w` variables → simpler
- ❌ No volume preference (AKE vs PMC/PAG)
- ❌ No underutilization penalty
- ✅ Advanced separation constraints (Y, Z variables)
- ✅ Total volume maximization objective
- ✅ Better success rate (89.8% vs 72.1%)

### Sequential vs Integrated (Delgado/Puttaert)
- Sequential: 3 separate optimizations
- Integrated: 1 optimization with all decisions
- Sequential has more 3D packing failures

### W&B-focused vs All Others
- Takes ULD packing as GIVEN (from actual data)
- Only optimizes WHERE to place ULDs
- No item-level decisions
- Surprisingly effective!

### BAX-fixed vs Puttaert
- Identical model
- BAX ULD positions locked to actual values
- 50% more infeasibility (33.2% vs 27.9%)
- Shows BAX flexibility is CRITICAL

---

## When to Use Each Model

### 🏆 DelgadoVenezian - USE FOR:
- ✅ Production optimization
- ✅ Best fuel savings
- ✅ Research baseline
- ✅ When you have 3D packing integration

### 💡 W&B-focused - USE FOR:
- ✅ Quick what-if analysis
- ✅ Position-only optimization
- ✅ When ULD packing is fixed
- ✅ Operational planning with known cargo

### 📦 Sequential - USE FOR:
- ✅ Understanding staged approaches
- ✅ When you need volume preferences
- ✅ Comparing against staged methods

### 🔧 Puttaert - USE FOR:
- ✅ Historical comparison
- ✅ Understanding evolution of DelgadoVenezian
- ⚠️ NOT recommended for production (lower performance)

### 🔒 BAX-fixed - USE FOR:
- ✅ Testing robustness
- ✅ Understanding constraint impact
- ⚠️ NOT for actual optimization (33% failure!)

---

## Results Mapping Table

From `Read - Results Comparison.ipynb`:

```python
model_type_mapping = {
    '%MAC ZFW_model': 'Model',              # DelgadoVenezian
    '%MAC ZFW_baseline': 'Sequential',      # Baseline
    '%MAC ZFW_optimized_actual': 'W&B-focused',  # Optimized_Actual
    '%MAC ZFW_bax_fixed': 'BAX-fixed',      # BAX_Fixed
    'Actual %MAC ZFW': 'Actual'             # Ground truth
}
```

---

## Where Does "Actual" Come From?

**Source:** `LoadLocationsSpotfire.csv`

```python
# In Classes.ipynb, Aircraft class
aircraft.actual_MAC_ZFW = data['MacZFW'].iloc[0]
```

**What it represents:**
- Real KLM flight operations
- What actually happened in the flight
- NOT a model - it's ground truth data
- Used as baseline for comparison
- May include human decisions and operational constraints not in models

**Why compare against it:**
- Validate models produce feasible solutions
- Measure fuel savings potential
- Understand gap between optimal and actual

---

## Folder Structure

```
KLM_Modified/
├── Model.ipynb                    # DelgadoVenezian ⭐
├── Optimized_Actual.ipynb         # W&B-focused
├── Baseline.ipynb                 # Sequential
├── Model_Puttaert.ipynb           # Puttaert
├── BAX_Fixed.ipynb                # BAX-fixed
│
├── Results/                       # DelgadoVenezian results
├── Results_Optimized_Actual/      # W&B-focused results
├── Results_Baseline/              # Sequential results
├── Results Puttaert/              # Puttaert results
├── Results_BAX_Fixed/             # BAX-fixed results
│
└── latex_models/
    ├── baseline.tex               # Sequential LaTeX
    ├── optimized_actual.tex       # W&B-focused LaTeX
    ├── model_puttaert.tex         # Puttaert LaTeX
    └── bax_fixed.tex              # BAX-fixed LaTeX
```

⚠️ **LaTeX Warning:** LaTeX files may have transcription errors from Gurobi → LaTeX. Always trust the .ipynb implementations as source of truth!

---

## Quick Comparison Table

| Feature | DelgadoVenezian | W&B-focused | Sequential | Puttaert | BAX-fixed |
|---------|----------------|-------------|------------|----------|-----------|
| **Success** | 89.8% | 84.6% | 77.0% | 72.1% | 66.8% |
| **Complexity** | Medium-High | Very Low | Medium | Very High | Very High |
| **Speed** | Medium | Fast | Slow (3 stages) | Slow | Slow |
| **Packing** | 1D+3D feedback | Uses actual | 1D+3D staged | 1D+3D feedback | 1D+3D feedback |
| **Variables** | 4 types | 1 type | 2-4 per stage | 5 types | 5 types (fixed) |
| **Best For** | Production | Quick analysis | Understanding | Historical | Testing |

---

## Quick Stats

### Average Solution Times (rough estimates)
- **W&B-focused:** ~60 seconds (just W&B)
- **DelgadoVenezian:** ~180 seconds (including 3D packing)
- **Sequential:** ~240 seconds (3 stages + iterations)
- **Puttaert:** ~200 seconds (more complex)
- **BAX-fixed:** ~250 seconds (often fails)

### Model Sizes (typical flight with 50 items, 20 ULDs, 30 positions)
- **W&B-focused:** ~600 binary variables
- **DelgadoVenezian:** ~32,000 binary + integer variables
- **Sequential:** ~1,000 (Stage 1) + ~600 (Stage 3)
- **Puttaert:** ~62,000 binary + continuous variables
- **BAX-fixed:** ~62,000 variables (more constrained)

---

## Cheat Sheet: What Each Model Optimizes

| Model | Item→ULD | ULD→Position | # ULDs | Volume | Separation | BAX Placement |
|-------|----------|--------------|--------|--------|------------|---------------|
| DelgadoVenezian | ✅ | ✅ | ✅ | ✅ Total | ✅ Advanced | ✅ |
| W&B-focused | ❌ (given) | ✅ | ❌ (given) | ❌ | ❌ | ✅ |
| Sequential | ✅ | ✅ | ✅ | ✅ Pref | ✅ Simple | ✅ |
| Puttaert | ✅ | ✅ | ✅ | ✅ Pref+Util | ✅ Simple | ✅ |
| BAX-fixed | ✅ | ⚠️ (BAX fixed) | ✅ | ✅ Pref+Util | ✅ Simple | ❌ (fixed) |

---

## Common Mistakes to Avoid

1. ❌ Confusing "Model" (DelgadoVenezian) with "Model_Puttaert"
2. ❌ Thinking "Actual" is a model (it's real data!)
3. ❌ Using BAX-fixed for optimization (it's a test case)
4. ❌ Trusting LaTeX without checking .ipynb source
5. ❌ Ignoring infeasibility rates when choosing models

---

## TL;DR

**Best Model:** DelgadoVenezian (89.8% success, your model!)  
**Simplest Model:** W&B-focused (surprisingly good at 84.6%)  
**Don't Use:** BAX-fixed (66.8% success, for testing only)  
**Ground Truth:** Actual (from real KLM data)  
**Historic:** Puttaert (predecessor to DelgadoVenezian)

**The Naming:**
- In code: `Model`, `Optimized_Actual`, `Baseline`, `Model_Puttaert`, `BAX_Fixed`
- In papers/results: "DelgadoVenezian", "W&B-focused", "Sequential", "Puttaert", "BAX-fixed"
- The comparison file maps between them!

---

**Quick Access:**
- Full details: `MODEL_COMPARISON_COMPREHENSIVE.md`
- This reference: `MODEL_QUICK_REFERENCE.md`
- Comparison code: `Read - Results Comparison.ipynb`
- Name mapping: Line 15-21 in Results Comparison notebook

