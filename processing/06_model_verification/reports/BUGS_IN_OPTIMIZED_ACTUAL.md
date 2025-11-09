# 🐛 BUGS FOUND IN OPTIMIZED_ACTUAL.IPYNB

**Model Type:** W&B-focused (Weight & Balance only, no packing stage)

---

## 🔥 **CRITICAL BUGS (MUST FIX)**

### **BUG #1: COMPARTMENT WEIGHT CONSTRAINTS** - CRITICAL! 🔥

**Lines:** ~98-123 (O6a-O6f)

```python
# ❌ OPTIMIZED_ACTUAL: One constraint PER POSITION
# O6a: Peso Compartimento C1
for t in aircraft.loadlocations_C1:
    m.addConstr(quicksum(j.weight * f[j.index, t.index] for j in cargo.uld)
                <= aircraft.max_weight_C1, name=f'C_Added_1_{t.index}')

# O6b, O6c, O6d, O6e, O6f: Same pattern for C2, C3, C4, C1+C2, C3+C4
```

**Should be:**
```python
# ✅ CORRECT: One constraint for ENTIRE COMPARTMENT
m.addConstr(
    quicksum(j.weight * f[j.index, t.index] 
            for j in cargo.uld 
            for t in aircraft.loadlocations_C1)
    <= aircraft.max_weight_C1
)
```

**Impact:** CRITICAL - Same as Baseline and Puttaert, allows N × compartment_limit

**Applies to:** O6a (C1), O6b (C2), O6c (C3), O6d (C4), O6e (C1+C2), O6f (C3+C4)

---

### **BUG #10: COL/CRT PER-POSITION LOGIC** - CRITICAL! 🔥

**Lines:** ~163-175 (O12)

```python
# ❌ OPTIMIZED_ACTUAL: Per-POSITION constraint
if str(aircraft.aircraft_type) in ['772', '77W']:
    for t in aircraft.loadlocations_C1_C2:
        m.addConstr(quicksum(f[j, t.index] for j in uld_with_COL) + 
                   quicksum(f[k, t.index] for k in uld_with_CRT) <= 1,
                   name=f'C_special_COL_CRT_C1_C2_{t.index}')
    for t in aircraft.loadlocations_C3_C4:
        m.addConstr(quicksum(f[j, t.index] for j in uld_with_COL) + 
                   quicksum(f[k, t.index] for k in uld_with_CRT) <= 1,
                   name=f'C_special_COL_CRT_C3_C4_{t.index}')
```

**Problem:**
- Creates one constraint per position
- Allows COL at position 11L and CRT at position 12L (both in C1+C2 front) - WRONG!
- Should prevent COL and CRT in same **compartment** (front or aft)

**Should be:**
```python
# ✅ CORRECT: Compartment-level with big-M
COL_front = m.addVar(vtype=GRB.BINARY)
CRT_front = m.addVar(vtype=GRB.BINARY)

m.addConstr(
    quicksum(f[j, t.index] for j in uld_with_COL for t in aircraft.loadlocations_C1_C2)
    <= big_M * COL_front
)
m.addConstr(
    quicksum(f[k, t.index] for k in uld_with_CRT for t in aircraft.loadlocations_C1_C2)
    <= big_M * CRT_front
)
m.addConstr(COL_front + CRT_front <= 1)
```

**Impact:** CRITICAL - Allows COL and CRT in same compartment!

---

### **BUG #11: MULTI-OBJECTIVE INDEX MISMATCH** - HIGH! 🔥

**Lines:** ~53, ~61, ~176-177

```python
# ❌ OPTIMIZED_ACTUAL: Only 2 objectives but uses index 5
m.setObjectiveN(MAC_obj, index=0, priority=2, weight=-1)
m.setObjectiveN(obj4, index=5, priority=1, weight=1)  # ❌ index 5!

# Then tries to access environment 5
WB_env = m.getMultiobjEnv(0)  # ✅ OK
bax_env = m.getMultiobjEnv(5)  # ❌ ERROR - only indices 0-1 exist!
```

**Should be:**
```python
# ✅ CORRECT: Sequential indices 0, 1
m.setObjectiveN(MAC_obj, index=0, priority=2, weight=-1)
m.setObjectiveN(obj4, index=1, priority=1, weight=1)

WB_env = m.getMultiobjEnv(0)
bax_env = m.getMultiobjEnv(1)
```

**Impact:** HIGH - Potential runtime error or undefined behavior

---

## ✅ **CORRECT FEATURES (No Bugs)**

### **✅ No Bug #2 (Item Assignment)**
- N/A - This model has no packing stage, only W&B

### **✅ No Bug #3 (Puttaert CRT/COL complexity)**
- Simpler than Puttaert (no nested item-level variables)
- But still has **Bug #10** (per-position instead of per-compartment)

### **✅ No Bug #4 (w variable)**
- ✅ Correctly uses j.weight directly (no linearization needed)

### **✅ No Bug #5 (Separation)**
- N/A - No separation penalty in W&B-only model

### **✅ No Bug #7 (Big-M)**
- N/A - No Big-M needed for this simpler model

### **✅ No Bug #8 (Position Weight Split)**
- ✅ Correctly uses single combined constraint (O5)

### **✅ MAC Formula Correct**
```python
MAC_obj = (((aircraft.C * (ZFW_index_obj - aircraft.K)) / aircraft.ZFW) + 
           aircraft.reference_arm - aircraft.lemac) / (aircraft.mac_formula / 100)
```
✅ Same as DelgadoVenezian - CORRECT!

### **✅ Lateral Balance Correct**
- Includes OEW, TOF, TripF correctly
- TOW and LW both correct

### **✅ CG Envelope Correct**
- TOW includes fuel_index ✅
- ZFW excludes fuel_index ✅

### **✅ Overlapping Positions**
- Handled correctly (O4)

---

## 📋 **SUMMARY FOR OPTIMIZED_ACTUAL**

### **🔥 CRITICAL (2 bugs):**
1. ✅ **Bug #1:** Compartment weights (per-position → per-compartment) - **SAME AS BASELINE & PUTTAERT**
2. ✅ **Bug #10:** COL/CRT logic (per-position → compartment-level) - **SAME AS BASELINE**

### **⚠️ HIGH PRIORITY (1 bug):**
3. ⚠️ **Bug #11:** Multi-objective indexing (index 5 → index 1) - **SAME AS BASELINE**

### **✅ N/A or CORRECT (8 features):**
- N/A: Bugs #2, #5 (no packing stage)
- N/A: Bugs #7 (no Big-M needed)
- ✅ No Bug #3 (simpler than Puttaert, though still has #10)
- ✅ No Bug #4 (no w variable)
- ✅ No Bug #6 (objective structure appropriate for W&B-only)
- ✅ No Bug #8 (combined position weight)
- ✅ No Bug #9 (objective count matches environments used)
- ✅ MAC formula correct
- ✅ Lateral balance correct
- ✅ CG envelope correct

---

## 🎯 **FIXES REQUIRED FOR OPTIMIZED_ACTUAL**

### **Priority 1 (Correctness):**
1. Fix compartment weight constraints (O6a-O6f): 6 constraint groups
2. Fix COL/CRT logic (O12): Compartment-level with big-M
3. Fix multi-objective indexing: index 5 → index 1

---

**Total Bugs in Optimized_Actual: 3 (2 critical, 1 high priority)**

**This is cleaner than Baseline and Puttaert!**
- No w variable linearization
- No packing stage bugs
- Simpler structure overall


