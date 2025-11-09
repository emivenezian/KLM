# 📊 COMPREHENSIVE MODEL COMPARISON
## KLM Cargo Loading Optimization Benchmark Models

---

## 🎯 Overview

This document provides a detailed comparison of all benchmark models used in the KLM cargo optimization project. Each model represents a different approach to solving the 3D bin packing problem combined with weight & balance optimization for aircraft loading.

### Model Performance Summary

| Model | Success Rate | Infeasibility | Ranking | Approach |
|-------|--------------|---------------|---------|----------|
| **DelgadoVenezian** (Model) | 89.8% | 10.2% | 1 | Integrated 1D-BPP + W&B + Advanced Objectives |
| **W&B-focused** (Optimized_Actual) | 84.6% | 15.4% | 2 | Direct W&B Only (No Packing) |
| **Sequential** (Baseline) | 77.0% | 23.0% | 3 | 1D-BPP → 3D-BPP → W&B |
| **Puttaert** (Model_Puttaert) | 72.1% | 27.9% | 4 | 1D-BPP + W&B Integral |
| **BAX-fixed** (BAX_Fixed) | 66.8% | 33.2% | 5 | 1D-BPP + W&B with BAX Fixed |
| **Actual** | N/A | N/A | Benchmark | Real KLM Operations |

---

## 📦 MODEL 1: DelgadoVenezian (Your Model)

**File:** `Model.ipynb`  
**Label in Results:** "Model"  
**Authors:** Delgado & Venezian  
**Success Rate:** 89.8% (Best)

### 🔧 Approach
Integrated 1D Bin Packing Problem combined with Weight & Balance optimization in a single model with advanced separation constraints and volume maximization.

### 🎯 Objective Functions (Multi-objective, Hierarchical)

1. **Priority 6 (Highest):** Maximize %MAC ZFW
   - Optimize center of gravity for fuel efficiency
   - Time limit: 60 seconds

2. **Priority 5:** Minimize Number of ULDs
   - Reduce operational costs
   - Time limit: 15 seconds

3. **Priority 4:** Maximize Total Volume Utilization
   - NEW objective: `Σ(volume_i × p_ij)` for all items in ULDs
   - Encourages fuller ULDs
   - Time limit: 15 seconds

4. **Priority 3:** Minimize Booking Separation
   - Uses advanced SP (separation penalty) binary variables
   - Keeps items from same AWB together
   - Mathematical formulation with tight bounds
   - Time limit: 15 seconds

5. **Priority 2:** Minimize BAX Proximity Score
   - Places BAX ULDs in preferred positions
   - Time limit: 15 seconds

### 🔑 Key Features

**Decision Variables:**
- `f[j,t]`: ULD j assigned to position t (binary)
- `u[j]`: ULD j is opened/used (binary)
- `p[i,j]`: Item i assigned to ULD j (binary) - only for regular ULDs
- `z[i,j,t]`: Item i in ULD j at position t (binary)
- `Y[b_i]`: Number of ULDs used by booking b_i (integer)
- `Z[b_i,j]`: Booking b_i uses ULD j (binary)

**Innovative Constraints:**
- **R30-R31:** Advanced separation logic with Y and Z variables
  ```
  p[i,j] ≤ Z[b_i,j]  ∀i ∈ booking b_i, ∀j
  Y[b_i] = Σ_j Z[b_i,j]
  ```
- No minimum volume utilization constraint (commented out)
- Direct weight calculation: `i.weight × z[i,j,t]` (no auxiliary w variables)

**Feedback Loop:**
- Packs ULDs using 3D bin packing between iterations
- Fixes successful packings in next iteration
- Opens new ULDs if needed

### ✅ Advantages
1. Best success rate (89.8%)
2. Mathematically rigorous separation constraints
3. Volume maximization objective promotes efficiency
4. Simplified variable structure (no w variables)
5. Reduced model complexity while maintaining performance

### ⚠️ Disadvantages
1. More complex separation constraints may cause infeasibility in edge cases
2. No volume preference between ULD types (AKE vs PMC/PAG)
3. Requires iterative feedback loop with 3D packing

---

## 📦 MODEL 2: W&B-focused (Optimized_Actual)

**File:** `Optimized_Actual.ipynb`  
**Label in Results:** "W&B-focused"  
**Success Rate:** 84.6% (2nd Best)

### 🔧 Approach
**Direct Weight & Balance optimization ONLY** - completely bypasses 1D and 3D bin packing phases. Uses the actual ULDs that were built in reality.

### 🎯 Objective Functions (Simplest)

1. **Priority 2:** Maximize %MAC ZFW
   - Time limit: 60 seconds

2. **Priority 1:** Minimize BAX Proximity Score
   - Time limit: 15 seconds

### 🔑 Key Features

**Decision Variables:**
- `f[j,t]`: ULD j assigned to position t (binary) - ONLY variable type!

**Key Assumption:**
- Takes pre-packed ULDs from actual flight data
- ULDs already have their weights computed
- Only optimizes WHERE to place ULDs, not WHAT goes in them

**Process:**
1. Read actual ULDs from BuildUpInformationSpotfire.csv
2. Use actual weights from LoadLocationsSpotfire.csv
3. Optimize only position assignment for W&B

### ✅ Advantages
1. Extremely simple and fast (only position assignment)
2. High success rate (84.6%) despite simplicity
3. No packing feasibility issues
4. Closest to actual operational constraints
5. Uses real-world packing solutions

### ⚠️ Disadvantages
1. Cannot improve packing efficiency (items already assigned)
2. Depends entirely on quality of actual packing
3. Cannot optimize number of ULDs used
4. No item-level optimization
5. Limited to scenarios where actual data exists

---

## 📦 MODEL 3: Sequential (Baseline)

**File:** `Baseline.ipynb`  
**Label in Results:** "Sequential"  
**Success Rate:** 77.0%

### 🔧 Approach
Three-stage sequential optimization with feedback loop:
1. **Stage 1:** 1D Bin Packing + Weight & Balance (combined)
2. **Stage 2:** 3D Bin Packing (for each assigned ULD)
3. **Stage 3:** Weight & Balance (final positions)

### 🎯 Objective Functions (Stage 1: 1D-BPP)

1. **Priority 4:** Volume Preference Score
   - Small items (< threshold) prefer AKE ULDs
   - Large items prefer PMC/PAG ULDs
   - Score: `Σ p[i,j] × (threshold - volume_i)` for matching types

2. **Priority 3:** Minimize Number of ULDs

3. **Priority 2:** Minimize Underutilization Penalty
   - Penalizes ULDs with < 20% volume utilization
   - `underutilization[j] ≥ 0.2 - actual_load_factor[j]`

4. **Priority 1:** Minimize Separation Penalty
   - Simple binary penalty per prefix-ULD combination
   - `Σ p[i,j] ≤ |items| × separation_penalty[prefix,j]`

### 🎯 Objective Functions (Stage 3: W&B)

1. **Priority 2:** Maximize %MAC ZFW
2. **Priority 1:** Minimize BAX Proximity Score

### 🔑 Key Features

**Decision Variables (Stage 1):**
- `p[i,j]`: Item i assigned to ULD j (binary) - for ALL ULDs (not just regular)
- `u[j]`: ULD j is opened (binary)
- (No f, z variables in this stage)

**Feedback Loop:**
- After Stage 1: Try 3D packing for each ULD assignment
- If 3D packing fails → mark items as deferred, return to Stage 1
- Iterates until all items successfully packed

**Separation Logic:**
- Simpler than DelgadoVenezian model
- Creates binary variable for each (prefix, ULD) pair
- If any item from prefix goes to ULD → penalty activated

### ✅ Advantages
1. Volume preference logic guides efficient packing
2. Explicit underutilization penalty prevents waste
3. Clear three-stage process
4. Simpler separation constraints

### ⚠️ Disadvantages
1. Sequential approach can miss global optimum
2. 3D packing failures require re-optimization (23% infeasibility)
3. More complex objective function hierarchy
4. Underutilization penalty adds variables and constraints
5. Items can be assigned to BAX/BUP/T in Stage 1 (less restrictive)

---

## 📦 MODEL 4: Puttaert (Model_Puttaert)

**File:** `Model_Puttaert.ipynb`  
**Label in Results:** "Puttaert" (or "Model_Puttaert")  
**Success Rate:** 72.1%

### 🔧 Approach
Integrated 1D-BPP + Weight & Balance similar to DelgadoVenezian, but with older constraint formulation. This is likely the predecessor to the DelgadoVenezian model.

### 🎯 Objective Functions (Similar to DelgadoVenezian)

1. **Priority 6:** Maximize %MAC ZFW
2. **Priority 5:** Volume Preference (AKE vs PMC/PAG)
3. **Priority 4:** Minimize Number of ULDs
4. **Priority 3:** Minimize Underutilization Penalty (like Baseline)
5. **Priority 2:** Minimize Separation Penalty (simple version)
6. **Priority 1:** Minimize BAX Proximity Score

### 🔑 Key Features

**Decision Variables:**
- `f[j,t]`: ULD j assigned to position t
- `w[i,j,t]`: Weight of item i in ULD j at position t (CONTINUOUS)
- `u[j]`: ULD j is opened
- `p[i,j]`: Item i assigned to ULD j
- `z[i,j,t]`: Item i in ULD j at position t

**Key Difference from DelgadoVenezian:**
- Uses auxiliary weight variables `w[i,j,t]`
- Requires linearization constraints: `w[i,j,t] = weight_i × z[i,j,t]`
- Includes underutilization penalty (like Baseline)
- Simpler separation logic

### ✅ Advantages
1. Comprehensive objective function coverage
2. Includes volume preference optimization
3. Penalizes underutilization

### ⚠️ Disadvantages
1. More variables (w variables) increase complexity
2. Requires linearization constraints
3. Lower success rate (72.1%) despite more objectives
4. May over-constrain the problem
5. Older formulation, superseded by DelgadoVenezian

---

## 📦 MODEL 5: BAX-fixed (BAX_Fixed)

**File:** `BAX_Fixed.ipynb`  
**Label in Results:** "BAX-fixed"  
**Success Rate:** 66.8% (Worst)

### 🔧 Approach
Identical to Puttaert model but with **fixed BAX ULD positions** - BAX ULDs must go to their actual positions from real flight data.

### 🎯 Objective Functions
Same as Puttaert model (6 objectives, hierarchical)

### 🔑 Key Features

**Main Difference:**
```python
# BAX ULDs have fixed positions from actual data
for j in cargo.uld:
    if j.isBAX and j.actual_position is not None:
        f[j.index, j.actual_position].lb = 1
        f[j.index, j.actual_position].ub = 1
        # Lock to actual position
```

**Constraint Impact:**
- Removes flexibility in BAX positioning
- BAX positions significantly affect W&B (usually in forward compartments)
- Forces model to work around fixed constraints

### ✅ Advantages
1. More realistic operational constraint
2. Respects actual BAX positioning decisions
3. Tests model robustness with fixed constraints

### ⚠️ Disadvantages
1. Worst success rate (66.8%)
2. Fixed BAX positions severely limit MAC optimization
3. 33.2% infeasibility due to over-constraining
4. Demonstrates importance of BAX positioning flexibility
5. Not practical for optimization purposes

---

## 📦 BASELINE: Actual

**Source:** LoadLocationsSpotfire.csv → `MacZFW` column  
**Label in Results:** "Actual"

### 🔧 Approach
Real-world KLM cargo loading operations. This is NOT a model - it's the ground truth from actual flights.

### 🔑 Key Features

**Data Source:**
```python
aircraft.actual_MAC_ZFW = data['MacZFW'].iloc[0]
```

**What it represents:**
- Actual ULD configurations used in flights
- Actual item assignments made by KLM cargo handlers
- Actual position assignments in aircraft
- Real-world constraints and decisions

**Use Cases:**
1. Performance baseline for all models
2. Fuel consumption reference
3. Validation of model outputs
4. Source data for W&B-focused model

### 📊 Characteristics
- Reflects human decision-making
- Includes operational constraints not in models
- May not be optimal (hence the optimization project)
- Includes real-world inefficiencies and constraints

---

## 🔍 DETAILED COMPARISON

### Decision Variables Comparison

| Model               | f (ULD→Pos) | u (ULD Open) | p (Item→ULD) | z (Item→ULD→Pos) | w (Weight) | Other |
|---------------------|-------------|--------------|--------------|------------------|------------|-------|
| **DelgadoVenezian** | ✅           | ✅ | ✅ (regular only) | ✅ | ❌ | Y, Z (separation) |
| **W&B-focused**     | ✅           | ❌ | ❌ | ❌ | ❌ | None |
| **Sequential**      | Stage 3 only | Stage 1 only | Stage 1 only | ❌ | ❌ | None |
| **Puttaert**        | ✅           | ✅ | ✅ (all ULDs) | ✅ | ✅ | None |
| **BAX-fixed**       | ✅ (BAX fixed)| ✅ | ✅ (all ULDs) | ✅ | ✅ | None |
| **Actual**          | N/A           | N/A | N/A | N/A | N/A | N/A |

### Objective Functions Comparison

| Priority | DelgadoVenezian | Sequential (Stage 1) | Puttaert | BAX-fixed | W&B-focused |
|----------|-----------------|---------------------|----------|-----------|-------------|
| **Highest (6)** | MAC | - | MAC | MAC | - |
| **5** | # ULDs | - | Vol Pref | Vol Pref | - |
| **4** | Total Vol | Vol Pref | # ULDs | # ULDs | - |
| **3** | Separation | # ULDs | Underutil | Underutil | - |
| **2** | BAX Prox | Underutil | Separation | Separation | MAC |
| **Lowest (1)** | - | Separation | BAX Prox | BAX Prox | BAX Prox |

### Constraint Complexity

| Model | Approx # Variables | Approx # Constraints | Complexity |
|-------|-------------------|---------------------|------------|
| **DelgadoVenezian** | O(I×J + I×J×T) | High | ⭐⭐⭐⭐ |
| **W&B-focused** | O(J×T) | Low | ⭐ |
| **Sequential** | Varies by stage | Medium | ⭐⭐⭐ |
| **Puttaert** | O(I×J×T) + w vars | Very High | ⭐⭐⭐⭐⭐ |
| **BAX-fixed** | O(I×J×T) + w vars + fixed | Very High | ⭐⭐⭐⭐⭐ |

Where:
- I = number of cargo items (~20-100 per flight)
- J = number of ULDs (~10-30 per flight)
- T = number of load positions (~15-40 per aircraft)

---

## 🏆 KEY INSIGHTS

### Why DelgadoVenezian Performs Best

1. **Simplified Variables:** Eliminated w variables, reducing complexity
2. **Volume Maximization:** Explicitly promotes better utilization
3. **Advanced Separation:** Tighter mathematical formulation with Y/Z variables
4. **Balanced Priorities:** Right hierarchy of objectives
5. **Flexible Constraints:** Only essential constraints, avoiding over-constraining

### Why W&B-focused Performs Well

1. **Simplicity:** Fewer variables = fewer failure modes
2. **Realistic:** Uses actual packing solutions
3. **Focused:** Optimizes only the most important aspect (W&B)
4. **Fast:** Quick solving time
5. **Practical:** Closest to real operations

### Why Sequential/Puttaert Struggle

1. **Sequential Gaps:** Three stages can miss global optimum
2. **3D Packing Failures:** Major source of infeasibility
3. **Over-complexity:** Too many objectives and constraints
4. **Feedback Loop Iterations:** Multiple solve cycles

### Why BAX-fixed Fails Most

1. **Over-constrained:** Fixed positions remove critical degrees of freedom
2. **BAX Impact:** BAX ULDs are heavy and usually forward → huge MAC impact
3. **Infeasibility:** 33.2% - fixed constraints create impossible scenarios

---

## 📈 PERFORMANCE METRICS

### Infeasibility Analysis

| Model | Infeasible Flights | Main Causes |
|-------|-------------------|-------------|
| **DelgadoVenezian** | 10.2% | Separation constraints, extreme cargo |
| **W&B-focused** | 15.4% | Position conflicts, type mismatches |
| **Sequential** | 23.0% | 3D packing failures, iteration limits |
| **Puttaert** | 27.9% | Over-constrained, w variable conflicts |
| **BAX-fixed** | 33.2% | Fixed BAX positions, over-constrained |

### Solution Quality (When Feasible)

Based on fuel savings potential:

1. **DelgadoVenezian:** Highest MAC optimization, best fuel savings
2. **Sequential:** Good MAC optimization when successful
3. **W&B-focused:** Limited by actual packing, moderate savings
4. **Puttaert:** Similar to Sequential
5. **BAX-fixed:** Limited optimization due to fixed constraints

---

## 🔬 MATHEMATICAL FORMULATIONS

### Core W&B Formulation (All Models)

**Zero Fuel Weight Index:**
```
ZFW_index = DOI + INDEX_PAX + Σ_c (weight_c × Δ_c)

Where:
- DOI: Dry Operating Index
- INDEX_PAX: Passenger moment index
- weight_c: Weight in compartment c
- Δ_c: Delta index for compartment c
```

**%MAC Calculation:**
```
%MAC = ((C × (ZFW_index - K)) / ZFW + ref_arm - lemac) / (mac_formula / 100)

Must satisfy: %MAC_fwd ≤ %MAC_ZFW ≤ %MAC_aft
```

### Separation Constraints

**DelgadoVenezian (Advanced):**
```
p[i,j] ≤ Z[b_i,j]  ∀i ∈ booking b_i, ∀j
Y[b_i] = Σ_j Z[b_i,j]
Minimize: Σ Y[b_i]
```

**Sequential/Puttaert/BAX-fixed (Simple):**
```
Σ_i∈prefix p[i,j] ≤ |items_prefix| × SP[prefix,j]
Minimize: Σ SP[prefix,j]
```

---

## 💡 RECOMMENDATIONS

### For Research/Development:
- **Use DelgadoVenezian** as primary model (best performance)
- Study why W&B-focused performs so well with simplicity
- Investigate hybrid approaches combining both

### For Operations:
- **W&B-focused** might be most practical (uses existing packing)
- DelgadoVenezian requires 3D packing software integration
- Consider two-phase: optimize packing, then optimize positions

### For Further Improvement:
1. Investigate DelgadoVenezian separation constraint relaxation for edge cases
2. Add minimum volume utilization back with tunable parameter
3. Hybrid model: W&B-focused with local packing re-optimization
4. Machine learning to predict infeasibility early

---

## 📚 FILE LOCATIONS

| Model | Implementation | Results | LaTeX Doc |
|-------|---------------|---------|-----------|
| DelgadoVenezian | `Model.ipynb` | `Results/` | N/A (use this as master) |
| W&B-focused | `Optimized_Actual.ipynb` | `Results_Optimized_Actual/` | `latex_models/optimized_actual.tex` |
| Sequential | `Baseline.ipynb` | `Results_Baseline/` | `latex_models/baseline.tex` |
| Puttaert | `Model_Puttaert.ipynb` | `Results Puttaert/` | `latex_models/model_puttaert.tex` |
| BAX-fixed | `BAX_Fixed.ipynb` | `Results_BAX_Fixed/` | `latex_models/bax_fixed.tex` |

---

## 🎓 SUMMARY

### The Five Models Represent Different Philosophies:

1. **DelgadoVenezian:** "Optimize everything with mathematical rigor"
2. **W&B-focused:** "Keep it simple, focus on what matters most"
3. **Sequential:** "Break down the problem into manageable stages"
4. **Puttaert:** "Leave no stone unturned, optimize all aspects"
5. **BAX-fixed:** "Reality has constraints, test robustness"

### The Winner: DelgadoVenezian
- Best success rate (89.8%)
- Balanced complexity
- Smart variable elimination
- Advanced but practical

### The Surprise: W&B-focused
- 84.6% success with simplest approach
- Questions whether complex packing optimization is always necessary
- Suggests operational practicality matters

### The Lesson: BAX-fixed
- Constraints matter - badly
- 33.2% failure shows importance of flexibility
- BAX positioning is critical for W&B

---

**Author:** María Emilia Venezian Juricic  
**Project:** KLM Cargo Optimization  
**Supervisor:** Dr. Felipe Delgado  
**Institution:** Pontificia Universidad Católica de Chile  
**Date:** October 2025

