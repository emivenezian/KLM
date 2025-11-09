# 🐛 CRITICAL BUGS FOUND IN MODEL_PUTTAERT.IPYNB

**Date:** October 28, 2025  
**Comparison:** Model_Puttaert.ipynb (BUGGY) vs Model.ipynb (CORRECT - DelgadoVenezian)

---

## ⚠️ **BUG #1: COMPARTMENT WEIGHT CONSTRAINTS** - CRITICAL! 🔥

### **The Bug (Puttaert):**
```python
# ❌ WRONG: Creates one constraint PER POSITION in C1
for t in aircraft.loadlocations_C1:
    m.addConstr(quicksum(w[i.index, j.index, t.index] for i in cargo.items for j in cargo.uld) +
                quicksum(j.weight * f[j.index, t.index] for j in cargo.uld if j.isBAXorBUPorT)
                <= aircraft.max_weight_C1, name=f'C_Added_1_{t.index}')
```

### **Why It's Wrong:**
- **Creates multiple constraints**: One for EACH position `t` in C1
- **Each constraint checks**: weight at position `t` ≤ max_weight_C1
- **But max_weight_C1 is the COMPARTMENT limit**, not the position limit!
- **Result**: Each individual position is constrained to the entire compartment capacity
- This is **overly restrictive** and doesn't match the intended logic

**Example:** If C1 has 3 positions (11L, 12L, 13L) and max_weight_C1 = 5000 kg:
- Puttaert creates 3 constraints:
  - weight_at_11L ≤ 5000
  - weight_at_12L ≤ 5000  
  - weight_at_13L ≤ 5000
- This allows up to 15,000 kg total in C1! (3 × 5000)

### **The Fix (DelgadoVenezian):**
```python
# ✅ CORRECT: Creates ONE constraint for entire compartment C1
compartments = [
    ('C1', aircraft.max_weight_C1, aircraft.loadlocations_C1),
    # ...
]

for compartment, max_weight, loadlocations in compartments:
    m.addConstr(
        quicksum(i.weight * z[i.index, j.index, t.index] 
                for i in cargo.items 
                for j in cargo.uld 
                for t in loadlocations) +  # ← Sum over ALL t in compartment
        quicksum(j.weight * f[j.index, t.index] 
                for j in cargo.uld if j.isBAXorBUPorT 
                for t in loadlocations)    # ← Sum over ALL t in compartment
        <= max_weight  # ← ONE constraint: total weight ≤ limit
    )
```

### **Impact:**
- **CRITICAL** - This fundamentally changes the feasible region
- Puttaert's model is **less constrained** than intended
- Could allow overweight compartments in practice
- **MUST BE FIXED** in all benchmark models

### **Same Bug Applies To:**
- C1 weight (line ~272)
- C2 weight (line ~277)
- C3 weight (line ~282)
- C4 weight (line ~287)
- C1+C2 combined (line ~292)
- C3+C4 combined (line ~297)

---

## ⚠️ **BUG #2: CRT/COL COMPARTMENT CONSTRAINTS** - CRITICAL! 🔥

### **The Bug (Puttaert - Boeing 777 version):**
```python
# ❌ WRONG: Overly complex with too many variables
if str(aircraft.aircraft_type) in ['772', '77W']:
    # Per-position constraints (questionable)
    for t in aircraft.loadlocations_C1_C2:
        m.addConstr(quicksum(f[j, t.index] for j in T_with_COL) + 
                   quicksum(f[k, t.index] for k in T_with_CRT) <= 1)
    
    # Then creates NEW variables for every i, k, j, t combination!
    for j in cargo.uld:
        for i in COL_items_indices:
            for k in CRT_items_indices:
                for t in aircraft.loadlocations_C1_C2:
                    COL_C1_C2 = m.addVar(...)  # New variable!
                    CRT_C1_C2 = m.addVar(...)  # New variable!
                    # ... many linking constraints ...
                
                # Then forces sum == 0 across all positions
                m.addConstr(quicksum(COL_C1_C2 + CRT_C1_C2 for t in ...) == 0)
```

### **Issues:**
1. **Too many variables**: Creates variables for every (i, k, j, t) combination
2. **Inefficient**: O(n_COL × n_CRT × n_ULD × n_positions) variables
3. **Logic questionable**: The `sum == 0` constraint forces NO COL or CRT in those positions?
4. **Not compartment-level**: Works at position level, then sums, which is convoluted

### **The Fix (DelgadoVenezian):**
```python
# ✅ CORRECT: Compartment-level binary variables with big-M
if str(aircraft.aircraft_type) in ['772', '77W']:
    compartments_R34 = {
        'front': aircraft.loadlocations_C1_C2,
        'aft': aircraft.loadlocations_C3_C4
    }
    
    COL_k = {}  # ONE binary per compartment
    CRT_k = {}  # ONE binary per compartment
    
    for k_label, loadlocations_k in compartments_R34.items():
        COL_k[k_label] = m.addVar(vtype=GRB.BINARY)  # 1 if k has COL
        CRT_k[k_label] = m.addVar(vtype=GRB.BINARY)  # 1 if k has CRT
        
        # Big-M: If any COL ULD in k, then COL_k = 1
        big_M_COL = len(U_COL) * len(loadlocations_k)
        m.addConstr(
            quicksum(f[j.index, t.index] for j in U_COL for t in loadlocations_k) 
            <= big_M_COL * COL_k[k_label]
        )
        
        # Big-M: If any CRT ULD in k, then CRT_k = 1
        big_M_CRT = len(U_CRT) * len(loadlocations_k)
        m.addConstr(
            quicksum(f[j.index, t.index] for j in U_CRT for t in loadlocations_k) 
            <= big_M_CRT * CRT_k[k_label]
        )
        
        # Mutual exclusion at compartment level
        m.addConstr(COL_k[k_label] + CRT_k[k_label] <= 1)
        
        # Item-level enforcement using same binary
        for j, i with COL:
            m.addConstr(
                quicksum(z[i.index, j.index, t.index] for t in loadlocations_k) 
                <= big_M_COL * COL_k[k_label]
            )
        for j, i with CRT:
            m.addConstr(
                quicksum(z[i.index, j.index, t.index] for t in loadlocations_k) 
                <= big_M_CRT * CRT_k[k_label]
            )
```

### **Why DelgadoVenezian's Version Is Better:**
1. **O(2 × n_compartments)** variables instead of O(n_COL × n_CRT × n_ULD × n_positions)
2. **Clear logic**: COL_k and CRT_k are indicator variables for compartment occupancy
3. **Efficient big-M formulation**: Standard technique for mutual exclusion
4. **Compartment-level**: Directly models the requirement "COL and CRT cannot be in same compartment"

### **Impact:**
- **CRITICAL** - Affects feasibility and correctness
- Puttaert's version may be too restrictive or have unintended behavior
- **MUST BE FIXED** for correct COL/CRT handling

---

## ⚠️ **BUG #3: LINEARIZATION WITH 'w' VARIABLE** - Inefficiency

### **Puttaert's Approach:**
```python
# Creates continuous variable w[i,j,t] for item weight at position
w[i.index, j.index, t.index] = m.addVar(lb=0, vtype=GRB.CONTINUOUS)

# Then uses 7 linearization constraints to make w = i.weight when z = 1
# L1: w <= M * p
# L2: w <= M * f
# L6: w >= i.weight - M*(1-z)
# L7: w <= i.weight
# ... etc
```

**Variables:** O(n_items × n_ULD × n_positions) continuous variables

### **DelgadoVenezian's Approach:**
```python
# Uses z directly with i.weight (no w variable needed)
quicksum(i.weight * z[i.index, j.index, t.index] ...)

# Only needs 3 linking constraints for z:
# z <= p
# z <= f  
# z >= p + f - 1
```

**Variables:** No additional continuous variables

### **Impact:**
- **Medium Priority** - Doesn't affect correctness, but:
  - Puttaert has O(n_items × n_ULD × n_positions) extra variables
  - Puttaert has 7 × (n_items × n_ULD × n_positions) extra constraints
  - **Slower solve times**, more memory
- **Should be simplified** in other models if they use Puttaert's approach

---

## ⚠️ **BUG #4: SEPARATION PENALTY** - Suboptimal

### **Puttaert's Approach:**
```python
# Binary variable per (prefix, ULD)
separation_penalty[prefix, j.index] = m.addVar(vtype=GRB.BINARY)

# Constraint: if any item of prefix in j, then penalty = 1
m.addConstr(quicksum(p[i.index, j.index] for i in items) 
           <= len(items) * separation_penalty[prefix, j.index])

# Objective: minimize sum of penalties
obj3 = quicksum(separation_penalty.values())
```

**Issue:** Only tracks IF a prefix uses a ULD, not HOW MANY ULDs it uses

### **DelgadoVenezian's Approach:**
```python
# Integer variable: number of ULDs used by booking
Y[b_i] = m.addVar(vtype=GRB.INTEGER, lb=0)

# Binary: 1 if booking b_i uses ULD j
Z[b_i, j.index] = m.addVar(vtype=GRB.BINARY)

# Link p to Z
for i in booking:
    m.addConstr(p[i.index, j.index] <= Z[b_i, j.index])

# Count ULDs
m.addConstr(Y[b_i] == quicksum(Z[b_i, j.index] for j in ULDs))

# Objective: minimize total ULDs across all bookings
obj_separation = quicksum(Y[b_i] for b_i in bookings)
```

### **Why DelgadoVenezian's Is Better:**
- **Counts ULDs used per booking**: Y = 1 (good), Y = 3 (bad)
- **More accurate penalty**: Minimizes total ULD count, not just "is separated"
- **Better separation**: Keeps bookings together more effectively

### **Impact:**
- **Medium Priority** - Affects solution quality
- Puttaert's version works but is less effective at minimizing separation
- **Should be improved** in other models

---

## 📋 **SUMMARY OF BUGS TO FIX IN OTHER BENCHMARKS**

### **Priority 1: MUST FIX (Correctness)**
1. ✅ **Compartment weight constraints**: Change from `for t in loadlocations` to ONE constraint summing over all t
2. ✅ **CRT/COL compartment logic**: Simplify to compartment-level binary variables with big-M

### **Priority 2: SHOULD FIX (Efficiency/Quality)**
3. ⚠️ **w variable linearization**: Eliminate if present, use z directly
4. ⚠️ **Separation penalty**: Upgrade to Y/Z counting if present

### **Additional Checks:**
- ✅ MAC formula: Same in both (correct)
- ✅ Lateral balance: Same in both (correct)
- ✅ CG envelope: Same in both (correct)
- ✅ Overlapping positions: Same in both (correct)
- ✅ Item-level COL/CRT mixing: Same in both (correct)

---

## 🎯 **NEXT STEPS**

**Phase 3:** Check Baseline.ipynb for these bugs  
**Phase 4:** Check Optimized_Actual.ipynb for these bugs  
**Phase 5:** Check BAX_Fixed.ipynb for these bugs  

**For each model, verify:**
1. Compartment weight constraints (sum over all t in compartment, NOT per-position)
2. CRT/COL logic (simplified compartment-level version)
3. MAC formula (correct with all parameters)
4. Separation penalty (Y/Z version preferred)


