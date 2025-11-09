# 🐛 BUGS: CODE COMPARISON - Buggy vs Correct Implementation

**Purpose:** Side-by-side comparison of each bug with correct implementation  
**Date:** November 3, 2025

---

## 🔥 **CRITICAL BUG #1: Compartment Weight Per-Position (Instead of Per-Compartment)**

**Present in:** ALL 4 models (Puttaert, Baseline, Optimized_Actual, BAX_Fixed)

### ❌ **BUGGY IMPLEMENTATION** (Puttaert, BAX_Fixed)

```python
# P13: Peso Compartimento C1 - Total weight in compartment 1 limit
for t in aircraft.loadlocations_C1:  # ❌ WRONG: Loop over positions
    m.addConstr(quicksum(w[i.index, j.index, t.index]  for i in cargo.items for j in cargo.uld) +
                quicksum(j.weight * f[j.index, t.index] for j in cargo.uld if j.isBAXorBUPorT)
                <= aircraft.max_weight_C1, name = f'C_Added_1_{t.index}')

# P14: Peso Compartimento C2 - Total weight in compartment 2 limit
for t in aircraft.loadlocations_C2:  # ❌ WRONG: Loop over positions
    m.addConstr(quicksum(w[i.index, j.index, t.index]  for i in cargo.items for j in cargo.uld) +
                quicksum(j.weight * f[j.index, t.index] for j in cargo.uld if j.isBAXorBUPorT)
                <= aircraft.max_weight_C2, name = f'C_Added_2_{t.index}')

# P15: Peso Compartimento C3 - Total weight in compartment 3 limit
for t in aircraft.loadlocations_C3:  # ❌ WRONG: Loop over positions
    m.addConstr(quicksum(w[i.index, j.index, t.index]  for i in cargo.items for j in cargo.uld) +
                quicksum(j.weight * f[j.index, t.index] for j in cargo.uld if j.isBAXorBUPorT)
                <= aircraft.max_weight_C3, name = f'C_Added_3_{t.index}')

# P16: Peso Compartimento C4 - Total weight in compartment 4 limit
for t in aircraft.loadlocations_C4:  # ❌ WRONG: Loop over positions
    m.addConstr(quicksum(w[i.index, j.index, t.index]  for i in cargo.items for j in cargo.uld) +
                quicksum(j.weight * f[j.index, t.index] for j in cargo.uld if j.isBAXorBUPorT)
                <= aircraft.max_weight_C4, name = f'C_Added_4_{t.index}')
```

**Why is this wrong?**
- Creates **N constraints** (one per position) instead of 1 per compartment
- Each constraint applies the **same compartment limit** to each position individually
- **Example:** If C1 has 5 positions with limit 10,000 kg:
  - ❌ Buggy: Each of 5 positions ≤ 10,000 kg → Total can be 50,000 kg!
  - ✅ Correct: Sum of all 5 positions ≤ 10,000 kg

---

### ✅ **CORRECT IMPLEMENTATION** (DelgadoVenezian - Model.ipynb)

```python
# DV12: Compartment weight limits - Weight in each compartment (C1-C4) cannot exceed limit
compartments = [
    ('C1', aircraft.max_weight_C1, aircraft.loadlocations_C1),
    ('C2', aircraft.max_weight_C2, aircraft.loadlocations_C2),
    ('C3', aircraft.max_weight_C3, aircraft.loadlocations_C3),
    ('C4', aircraft.max_weight_C4, aircraft.loadlocations_C4)
]

for compartment, max_weight, loadlocations in compartments:
    m.addConstr(
        # ✅ CORRECT: Sum over ALL positions in compartment
        quicksum(i.weight * z[i.index, j.index, t.index] for i in cargo.items for j in cargo.uld for t in loadlocations) +
        quicksum(j.weight * f[j.index, t.index] for j in cargo.uld if j.isBAXorBUPorT for t in loadlocations)
        <= max_weight,
        name=f'C_Added_{compartment}'
    )
```

**Key difference:**
- ✅ **ONE constraint per compartment** (not per position)
- ✅ The sum includes **`for t in loadlocations`** INSIDE the quicksum
- ✅ Properly enforces compartment weight limit across all positions

---

## 🔥 **CRITICAL BUG #2: Item Assignment Includes BAX/BUP/T**

**Present in:** Puttaert, Baseline, BAX_Fixed (Not applicable to Optimized_Actual)

### ❌ **BUGGY IMPLEMENTATION** (Puttaert)

```python
# P3: Asignación Items - Every item must be placed in exactly one ULD
for i in cargo.items:
    m.addConstr(quicksum(p[i.index, j.index] for j in cargo.uld) == 1, 
                name = f'C3_{i.index}')
    # ❌ WRONG: Sum includes ALL ULDs (even BAX/BUP/T)
```

**Why is this wrong?**
- BAX/BUP/T ULDs are **pre-built containers** that cannot receive items from optimization
- Items cannot be packed in these special ULDs
- The model should only assign items to regular ULDs
- This creates **infeasible solutions** or forces items into BAX containers

---

### ✅ **CORRECT IMPLEMENTATION** (DelgadoVenezian - Model.ipynb)

```python
# DV3: Item assignment - Every item must be placed in exactly one ULD
for i in cargo.items:
    m.addConstr(quicksum(p[i.index, j.index] for j in cargo.uld if j.isNeitherBAXnorBUPnorT) == 1, 
                name=f'C3_{i.index}')
    # ✅ CORRECT: Only sum over regular ULDs (exclude BAX/BUP/T)
```

**Key difference:**
- ✅ Filter `if j.isNeitherBAXnorBUPnorT` excludes special ULDs
- ✅ Items can only go to regular containers
- ✅ Prevents infeasibility and incorrect assignments

---

## 🔥 **CRITICAL BUG #10: COL/CRT Per-Position Logic (Not Compartment-Level)**

**Present in:** ALL 4 models (Puttaert, Baseline, Optimized_Actual, BAX_Fixed)

### ❌ **BUGGY IMPLEMENTATION** (Baseline, Optimized_Actual)

```python
# Simpler per-position logic (still wrong)
if str(aircraft.aircraft_type) in ['772', '77W']:
    for t in aircraft.loadlocations_C1_C2:  # ❌ WRONG: Loop per position
        m.addConstr(
            quicksum(f[j, t.index] for j in uld_with_COL) + 
            quicksum(f[k, t.index] for k in uld_with_CRT) <= 1, 
            name=f'C_special_COL_CRT_C1_C2_{t.index}'
        )
    for t in aircraft.loadlocations_C3_C4:  # ❌ WRONG: Loop per position
        m.addConstr(
            quicksum(f[j, t.index] for j in uld_with_COL) + 
            quicksum(f[k, t.index] for k in uld_with_CRT) <= 1, 
            name=f'C_special_COL_CRT_C3_C4_{t.index}'
        )
```

**Why is this wrong?**
- COL and CRT are **temperature-controlled cargo** that cannot share the **same compartment**
- The constraint is per-position, not per-compartment
- **Example:** In C1_C2 (front) with 10 positions:
  - ❌ Buggy: COL can be at position 1, CRT at position 2 (both in C1_C2!)
  - ✅ Correct: COL and CRT mutually exclusive across entire C1_C2 compartment

---

### ✅ **CORRECT IMPLEMENTATION** (DelgadoVenezian - Model.ipynb)

```python
# DV24: COL/CRT compartment separation - COL and CRT cannot be in same compartment (Boeing 777)
if str(aircraft.aircraft_type) in ['772', '77W']:
    # Define compartment groups
    compartment_groups = [
        ('C1_C2', aircraft.loadlocations_C1_C2),
        ('C3_C4', aircraft.loadlocations_C3_C4)
    ]
    
    COL_k = {}
    CRT_k = {}
    
    for k_label, loadlocations_k in compartment_groups:
        # Binary variables: 1 if COL/CRT present in entire compartment k
        COL_k[k_label] = m.addVar(vtype=GRB.BINARY, name=f'COL_{k_label}')
        CRT_k[k_label] = m.addVar(vtype=GRB.BINARY, name=f'CRT_{k_label}')
        
        # Identify ULDs with COL/CRT
        U_COL = [j for j in cargo.uld if j.COL == 1 or 
                 (j.isNeitherBAXnorBUPnorT and any(i.COL == 1 for i in cargo.items))]
        U_CRT = [j for j in cargo.uld if j.CRT == 1 or 
                 (j.isNeitherBAXnorBUPnorT and any(i.CRT == 1 for i in cargo.items))]
        
        big_M_COL = len(U_COL)
        big_M_CRT = len(U_CRT)
        
        # Link: If any COL ULD in compartment k → COL_k = 1
        if U_COL:
            m.addConstr(
                quicksum(f[j.index, t.index] for j in U_COL for t in loadlocations_k) <= big_M_COL * COL_k[k_label],
                name=f'C_R34_COL_{k_label}'
            )
        
        # Link: If any CRT ULD in compartment k → CRT_k = 1
        if U_CRT:
            m.addConstr(
                quicksum(f[j.index, t.index] for j in U_CRT for t in loadlocations_k) <= big_M_CRT * CRT_k[k_label],
                name=f'C_R34_CRT_{k_label}'
            )
        
        # ✅ CRITICAL: Mutual exclusion at COMPARTMENT level
        m.addConstr(
            COL_k[k_label] + CRT_k[k_label] <= 1,
            name=f'C_R34_COL_CRT_conflict_{k_label}'
        )
        
        # Link items to compartment binary
        for j in cargo.uld:
            if j.isNeitherBAXnorBUPnorT:
                for i in cargo.items:
                    if i.COL == 1:
                        m.addConstr(
                            quicksum(z[i.index, j.index, t.index] for t in loadlocations_k) <= big_M_COL * COL_k[k_label],
                            name=f'C_R34_COL_item_{i.index}_{j.index}_{k_label}'
                        )
                    if i.CRT == 1:
                        m.addConstr(
                            quicksum(z[i.index, j.index, t.index] for t in loadlocations_k) <= big_M_CRT * CRT_k[k_label],
                            name=f'C_R34_CRT_item_{i.index}_{j.index}_{k_label}'
                        )
```

**Key differences:**
- ✅ **Compartment-level binary variables** (COL_k, CRT_k) for C1_C2 and C3_C4
- ✅ Big-M formulation links ULD placement to compartment presence
- ✅ **Mutual exclusion:** `COL_k + CRT_k ≤ 1` at compartment level
- ✅ If COL is anywhere in C1_C2, no CRT allowed anywhere in C1_C2

---

## 🔥 **CRITICAL BUG #3: COL/CRT Complex Nested Logic**

**Present in:** Puttaert, BAX_Fixed (Not in Baseline/Optimized_Actual)

### ❌ **BUGGY IMPLEMENTATION** (Puttaert)

```python
# Overly complex nested variable creation (from Puttaert model)
if COL_items_present and CRT_items_present:
    for j in cargo.uld:
        if j.isNeitherBAXnorBUPnorT:
            for i in COL_items_indices:
                for k in CRT_items_indices:
                    # ❌ WRONG: Creates auxiliary variable for EACH combination (i, k, j, t)
                    for t in aircraft.loadlocations_C1_C2:
                        COL_C1_C2 = m.addVar(vtype=GRB.BINARY, name=f'COL_C1_C2_{i}_{j.index}_{t.index}')
                        CRT_C1_C2 = m.addVar(vtype=GRB.BINARY, name=f'CRT_C1_C2_{k}_{j.index}_{t.index}')
                        
                        # Linking constraints for COL
                        m.addConstr(COL_C1_C2 <= p[i, j.index])
                        m.addConstr(COL_C1_C2 <= f[j.index, t.index])
                        m.addConstr(COL_C1_C2 >= p[i, j.index] + f[j.index, t.index] - 1)
                        
                        # Linking constraints for CRT
                        m.addConstr(CRT_C1_C2 <= p[k, j.index])
                        m.addConstr(CRT_C1_C2 <= f[j.index, t.index])
                        m.addConstr(CRT_C1_C2 >= p[k, j.index] + f[j.index, t.index] - 1)
                    
                    # Sum over all positions = 0 (trying to prohibit)
                    m.addConstr(quicksum(COL_C1_C2 + CRT_C1_C2 for t in aircraft.loadlocations_C1_C2) == 0, 
                                name=f'C_special_COL_CRT_C1_C2_{i}_{k}_{j.index}')
```

**Why is this wrong?**
- **Exponential variable explosion:** Creates variables for every (COL_item, CRT_item, ULD, position) combination
- **Example:** 3 COL items × 5 CRT items × 20 ULDs × 10 positions = **3,000 binary variables** + linking constraints!
- **Incorrect logic:** The constraint `sum(COL_C1_C2 + CRT_C1_C2) == 0` tries to force both to 0, but doesn't properly enforce mutual exclusion
- **Performance:** Massive solver slowdown
- **Conceptual error:** Tries to use item-level logic for compartment-level restriction

---

### ✅ **CORRECT IMPLEMENTATION** (DelgadoVenezian - Model.ipynb)

See Bug #10 correct implementation above - same solution applies!

**Key advantages:**
- ✅ **Only 4 binary variables** (2 compartments × 2 cargo types) instead of thousands
- ✅ Clean compartment-level logic
- ✅ Proper big-M formulation
- ✅ Fast solver performance
- ✅ Conceptually correct: compartment restriction using compartment variables

---

## ⚠️ **HIGH PRIORITY BUG #4: w Variable Unnecessary Linearization**

**Present in:** Puttaert, BAX_Fixed (Not in Baseline/Optimized_Actual)

### ❌ **BUGGY IMPLEMENTATION** (Puttaert)

```python
# Create w variable (weight linearization)
w = {}
for i in cargo.items:
    for j in cargo.uld:
        for t in aircraft.loadlocations:
            w[i.index, j.index, t.index] = m.addVar(lb=0, vtype=GRB.CONTINUOUS, 
                                                     name=f'w_{i.index}_{j.index}_{t.index}')

# Linearization constraints (L1-L5 in Puttaert latex)
M = 10000  # ❌ Hardcoded Big-M

# L1: w_ijt ≤ weight_i * p_ij
for i in cargo.items:
    for j in cargo.uld:
        for t in aircraft.loadlocations:
            m.addConstr(w[i.index, j.index, t.index] <= i.weight * p[i.index, j.index], 
                        name=f'C_lin_1_{i.index}_{j.index}_{t.index}')

# L2: w_ijt ≤ M * f_jt
for i in cargo.items:
    for j in cargo.uld:
        for t in aircraft.loadlocations:
            m.addConstr(w[i.index, j.index, t.index] <= M * f[j.index, t.index], 
                        name=f'C_lin_2_{i.index}_{j.index}_{t.index}')

# Then use w[i,j,t] in constraints like:
m.addConstr(quicksum(w[i.index, j.index, t.index] for ...) <= max_weight)
```

**Why is this suboptimal?**
- **Unnecessary variable:** Creates |I| × |J| × |T| continuous variables
- **Unnecessary constraints:** 2 × |I| × |J| × |T| linking constraints
- **Example:** 100 items × 30 ULDs × 20 positions = **60,000 extra variables + 120,000 constraints!**
- **Not needed:** Gurobi handles `i.weight * z[i,j,t]` natively without linearization (z is binary)

---

### ✅ **CORRECT IMPLEMENTATION** (DelgadoVenezian - Model.ipynb)

```python
# NO w variable needed! Just use i.weight * z directly

# DV11: Position weight limit
for t in aircraft.loadlocations:
    m.addConstr(
        # ✅ CORRECT: Use i.weight * z[i,j,t] directly (no linearization needed)
        quicksum(i.weight * z[i.index, j.index, t.index] for i in cargo.items for j in cargo.uld) +
        quicksum(j.weight * f[j.index, t.index] for j in cargo.uld if j.isBAXorBUPorT)
        <= aircraft.define_max_weight_postion(t), 
        name=f'C7_{t.index}'
    )
```

**Key advantages:**
- ✅ **No w variable** → 60,000 fewer variables
- ✅ **No linearization constraints** → 120,000 fewer constraints
- ✅ **Faster solve times**
- ✅ **More readable code**
- ✅ Gurobi handles this automatically (z is binary, weight is parameter)

---

## ⚠️ **HIGH PRIORITY BUG #5: Separation Penalty Suboptimal**

**Present in:** Puttaert, Baseline, BAX_Fixed (Not applicable to Optimized_Actual)

### ❌ **BUGGY IMPLEMENTATION** (Puttaert)

```python
# Simple binary penalty (0 or 1 per ULD)
separation_penalty = {}
for prefix, items in prefix_groups.items():
    for j in cargo.uld:
        separation_penalty[prefix, j.index] = m.addVar(vtype=GRB.BINARY, 
                                                       name=f'separation_penalty_{prefix}_{j.index}')

# Constraint: If items from booking in ULD j, penalty = 1
for prefix, items in prefix_groups.items():
    for j in cargo.uld:
        m.addConstr(
            quicksum(p[i.index, j.index] for i in items) <= len(items) * separation_penalty[prefix, j.index], 
            name=f'C_separation_{prefix}_{j.index}'
        )

# Objective: Minimize total penalties
obj_separation = quicksum(separation_penalty.values())
m.setObjectiveN(obj_separation, index=2, priority=3, weight=1)
```

**Why is this suboptimal?**
- **Binary penalty:** Only counts "ULD used or not" (0 or 1)
- **Doesn't count number of ULDs:** If booking split across 5 ULDs, penalty = 5 (same as split across 2)
- **Example:** Booking with 10 pieces
  - ❌ Buggy: Split [8, 1, 1] pieces → penalty = 3 (3 ULDs used)
  - ❌ Buggy: Split [5, 5] pieces → penalty = 2 (2 ULDs used)
  - ✅ Correct system should prefer [5, 5] less strongly than keeping all 10 together

---

### ✅ **CORRECT IMPLEMENTATION** (DelgadoVenezian - Model.ipynb)

```python
# Y-Z counting system: Y counts number of ULDs used by each booking
Y = {}  # Y[b_i] = number of ULDs used by booking b_i
Z = {}  # Z[b_i, j] = 1 if booking b_i uses ULD j

for b_i, items in booking_groups.items():
    Y[b_i] = m.addVar(vtype=GRB.INTEGER, lb=0, ub=len(cargo.uld), name=f'Y_{b_i}')
    for j in cargo.uld:
        if j.isNeitherBAXnorBUPnorT:
            Z[b_i, j.index] = m.addVar(vtype=GRB.BINARY, name=f'Z_{b_i}_{j.index}')

# DV20: Link p to Z (if any item from booking in ULD j, Z = 1)
for b_i, items in booking_groups.items():
    for j in cargo.uld:
        if j.isNeitherBAXnorBUPnorT:
            for i in items:
                m.addConstr(
                    p[i.index, j.index] <= Z[b_i, j.index],
                    name=f'C_p_Z_{b_i}_{i.index}_{j.index}'
                )

# DV21: Y = sum of Z (count how many ULDs booking uses)
for b_i in booking_groups.keys():
    m.addConstr(
        Y[b_i] == quicksum(Z[b_i, j.index] for j in cargo.uld if j.isNeitherBAXnorBUPnorT),
        name=f'C_Y_Z_{b_i}'
    )

# Objective: Minimize Y (directly minimize number of ULDs per booking)
obj_separation = quicksum(Y.values())
m.setObjectiveN(obj_separation, index=2, priority=3, weight=1)
```

**Key advantages:**
- ✅ **Y counts exact number of ULDs** used per booking
- ✅ **Direct optimization:** Minimize total Y across all bookings
- ✅ **Better solution quality:** Strongly prefers keeping bookings together
- ✅ Example: Y=1 (all in one ULD) is penalized less than Y=3 (split across 3 ULDs)

---

## ⚠️ **HIGH PRIORITY BUG #7: Hardcoded Big-M**

**Present in:** Puttaert, BAX_Fixed (Not in Baseline/Optimized_Actual)

### ❌ **BUGGY IMPLEMENTATION** (Puttaert)

```python
# Hardcoded Big-M value
M = 10000  # ❌ WRONG: Arbitrary constant

# Used in constraints like:
m.addConstr(w[i.index, j.index, t.index] <= M * f[j.index, t.index], 
            name=f'C_lin_2_{i.index}_{j.index}_{t.index}')
```

**Why is this wrong?**
- **Too large:** Can cause numerical instability in solver
- **Too small:** Can make constraint ineffective if actual weights > 10,000 kg
- **Not adaptive:** Same value used regardless of actual cargo weights
- **Example:** If max item weight is 50 kg, M=10,000 is 200× larger than needed!

---

### ✅ **CORRECT IMPLEMENTATION** (DelgadoVenezian - Model.ipynb)

```python
# Calculate Big-M based on actual data
M = max([i.weight for i in cargo.items])  # ✅ CORRECT: Tightest possible M

# Used in DV8-DV10 linking constraints (if needed)
# But actually, DelgadoVenezian doesn't use w variable at all!
```

**Key advantages:**
- ✅ **Data-driven:** M adapts to actual cargo weights
- ✅ **Tighter bounds:** Helps solver performance
- ✅ **No numerical issues:** Avoids very large coefficients
- ✅ Example: If max weight = 2,000 kg, M = 2,000 (not 10,000)

---

## 📊 **MEDIUM PRIORITY BUG #8: Position Weight Split**

**Present in:** Puttaert, BAX_Fixed (Not in Baseline/Optimized_Actual)

### ❌ **BUGGY IMPLEMENTATION** (Puttaert)

```python
# P12a: Peso Posición (Items) - Weight of items at position limit
for t in aircraft.loadlocations:
    m.addConstr(
        quicksum(w[i.index, j.index, t.index] for i in cargo.items for j in cargo.uld) 
        <= aircraft.define_max_weight_postion(t), 
        name=f'C7_A_{t.index}'
    )

# P12b: Peso Posición (ULDs) - Weight of ULD at position limit  
for t in aircraft.loadlocations:
    m.addConstr(
        quicksum(j.weight * f[j.index, t.index] for j in cargo.uld if j.isBAXorBUPorT) 
        <= aircraft.define_max_weight_postion(t), 
        name=f'C7_B_{t.index}'
    )
```

**Why is this suboptimal?**
- **Redundant:** Two separate constraints for same position limit
- **Weaker:** Each constraint allows up to max_weight independently
- **Example:** Position limit = 1,000 kg
  - ❌ Buggy: Items ≤ 1,000 AND ULDs ≤ 1,000 (could total 2,000 kg if both active!)
  - ✅ Correct: Items + ULDs ≤ 1,000

---

### ✅ **CORRECT IMPLEMENTATION** (DelgadoVenezian - Model.ipynb)

```python
# DV11: Position weight limit - Single combined constraint
for t in aircraft.loadlocations:
    m.addConstr(
        # ✅ CORRECT: Single constraint for total weight at position
        quicksum(i.weight * z[i.index, j.index, t.index] for i in cargo.items for j in cargo.uld) +
        quicksum(j.weight * f[j.index, t.index] for j in cargo.uld if j.isBAXorBUPorT)
        <= aircraft.define_max_weight_postion(t), 
        name=f'C7_{t.index}'
    )
```

**Key advantages:**
- ✅ **Single constraint** per position (cleaner)
- ✅ **Correct enforcement** of total weight limit
- ✅ Matches LaTeX formulation in thesis

---

## ⚠️ **HIGH PRIORITY BUG #11: Multi-Objective Index Wrong**

**Present in:** Baseline, Optimized_Actual (Not in Puttaert/BAX_Fixed)

### ❌ **BUGGY IMPLEMENTATION** (Baseline, Optimized_Actual)

```python
# Multiple objectives with non-sequential indices
m.setObjectiveN(obj_MAC, index=0, priority=6, weight=-1)          # OK
m.setObjectiveN(obj_volume_pref, index=1, priority=5, weight=-1)  # OK
m.setObjectiveN(obj_separation, index=2, priority=3, weight=1)    # OK
m.setObjectiveN(obj_underutilization, index=3, priority=2, weight=1)  # ❌ WRONG: index=3 but should be next
m.setObjectiveN(obj_num_uld, index=5, priority=1, weight=1)       # ❌ WRONG: index=5 skips 4!
```

**Why is this wrong?**
- **Gurobi expects sequential indices:** 0, 1, 2, 3, 4, 5...
- **Skipped index (4):** Can cause undefined behavior
- **Not critical** but bad practice and may cause issues in future Gurobi versions

---

### ✅ **CORRECT IMPLEMENTATION** (DelgadoVenezian - Model.ipynb)

```python
# Sequential objective indices
m.setObjectiveN(MAC_obj, index=0, priority=6, weight=-1)               # Highest priority
m.setObjectiveN(obj_volume_pref, index=1, priority=5, weight=-1)
m.setObjectiveN(obj_separation, index=2, priority=4, weight=1)
m.setObjectiveN(obj_priority_underutil, index=3, priority=3, weight=1)
m.setObjectiveN(obj_uld_open, index=4, priority=2, weight=1)
m.setObjectiveN(obj_num_uld_opened, index=5, priority=1, weight=1)
# ✅ CORRECT: Indices 0, 1, 2, 3, 4, 5 (sequential)
```

**Key advantages:**
- ✅ **Sequential indices** (no gaps)
- ✅ **Best practice** for Gurobi
- ✅ **No undefined behavior**

---

## 📊 **DESIGN DIFFERENCE BUG #6: Objective Hierarchy**

**Present in:** Puttaert, Baseline, BAX_Fixed (Optimized_Actual is W&B only)

### 🤔 **DIFFERENT IMPLEMENTATION** (Puttaert)

```python
# Puttaert objective priorities:
m.setObjectiveN(obj_num_uld, index=0, priority=6, weight=1)        # Priority 6: Minimize ULDs (HIGHEST)
m.setObjectiveN(obj_volume_pref, index=1, priority=5, weight=-1)   # Priority 5: Volume preference
m.setObjectiveN(obj_priority, index=2, priority=4, weight=-1)      # Priority 4: Priority cargo
m.setObjectiveN(obj_separation, index=3, priority=3, weight=1)     # Priority 3: Separation
m.setObjectiveN(MAC_obj, index=4, priority=2, weight=-1)           # Priority 2: MAC (LOW!)
m.setObjectiveN(obj_uld_open, index=5, priority=1, weight=1)       # Priority 1: Underutilization
```

**Why is this different?**
- **MAC is only Priority 2** (low priority)
- **Number of ULDs is Priority 6** (highest)
- This is a **design choice** (not necessarily a bug), but:
  - Fuel efficiency (MAC) should be higher priority
  - Operational constraints vs optimization goals

---

### ✅ **CORRECT IMPLEMENTATION** (DelgadoVenezian - Model.ipynb)

```python
# DelgadoVenezian objective priorities:
m.setObjectiveN(MAC_obj, index=0, priority=6, weight=-1)               # Priority 6: MAC (HIGHEST)
m.setObjectiveN(obj_volume_pref, index=1, priority=5, weight=-1)       # Priority 5: Volume preference
m.setObjectiveN(obj_separation, index=2, priority=4, weight=1)         # Priority 4: Separation
m.setObjectiveN(obj_priority_underutil, index=3, priority=3, weight=1) # Priority 3: Priority cargo
m.setObjectiveN(obj_uld_open, index=4, priority=2, weight=1)           # Priority 2: Underutilization
m.setObjectiveN(obj_num_uld_opened, index=5, priority=1, weight=1)     # Priority 1: Minimize ULDs (LOW)
```

**Key differences:**
- ✅ **MAC is Priority 6** (highest) → fuel efficiency first
- ✅ **Number of ULDs is Priority 1** (lowest) → minimize only after other goals met
- ✅ **Better alignment** with aviation priorities (safety + efficiency first, then cost)

---

## 📊 **SUMMARY TABLE**

| Bug # | Description | Puttaert | Baseline | Opt_Actual | BAX_Fixed | Criticality |
|-------|-------------|----------|----------|------------|-----------|-------------|
| **#1** | Compartment weight per-position | ❌ | ❌ | ❌ | ❌ | 🔥 CRITICAL |
| **#2** | Item assignment includes BAX | ❌ | ❌ | N/A | ❌ | 🔥 CRITICAL |
| **#3** | COL/CRT complex nested | ❌ | ✅ | ✅ | ❌ | 🔥 CRITICAL |
| **#10** | COL/CRT per-position | ❌ | ❌ | ❌ | ❌ | 🔥 CRITICAL |
| **#4** | w variable linearization | ❌ | ✅ | ✅ | ❌ | ⚠️ HIGH |
| **#5** | Separation penalty suboptimal | ❌ | ❌ | N/A | ❌ | ⚠️ HIGH |
| **#7** | Hardcoded Big-M | ❌ | N/A | N/A | ❌ | ⚠️ HIGH |
| **#8** | Position weight split | ❌ | ✅ | ✅ | ❌ | 📊 MEDIUM |
| **#11** | Multi-objective index wrong | ✅ | ❌ | ❌ | ✅ | ⚠️ HIGH |
| **#6** | Objective hierarchy different | ❌ | ❌ | OK | ❌ | 📊 DESIGN |
| **#9** | Multi-obj count mismatch | Maybe | ✅ | ✅ | ✅ | 📊 MEDIUM |

**Total bugs per model:**
- **Puttaert:** 9 bugs
- **Baseline:** 4 bugs  
- **Optimized_Actual:** 3 bugs
- **BAX_Fixed:** 8 bugs (based on Puttaert)
- **DelgadoVenezian:** 0 bugs ✅

---

## 🎯 **NEXT STEPS**

1. **Fix all bugs** in benchmark models (recommended: fix all 11 where applicable)
2. **Test on subset** (e.g., 10 flights) to verify fixes
3. **Run full comparison** (102 complete flights) with corrected models
4. **Document performance impact** of fixes

---

**Legend:**
- ❌ = Bug present  
- ✅ = Correct or not applicable
- N/A = Constraint not in this model
- 🔥 = Critical (correctness)
- ⚠️ = High priority (performance/quality)
- 📊 = Design difference or medium priority

