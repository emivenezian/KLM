# 🐛 BUGS FOUND IN BASELINE.IPYNB

**Model Structure:** Sequential (Stage 1: 1D-BPP, Stage 2: 3D-BPP, Stage 3: W&B)

---

## 🔥 **CRITICAL BUGS (MUST FIX)**

### **BUG #1: COMPARTMENT WEIGHT CONSTRAINTS** - CRITICAL! 🔥

**Lines:** ~465-485 (W6a-W6f in Stage 3)

```python
# ❌ BASELINE: One constraint PER POSITION
# W6a: Peso Compartimento C1
for t in aircraft.loadlocations_C1:
    m.addConstr(quicksum(j.weight * f[j.index, t.index] for j in cargo.uld)
                <= aircraft.max_weight_C1, name=f'C_Added_1_{t.index}')
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

**Impact:** CRITICAL - Same as Puttaert, allows N × compartment_limit

**Applies to:** W6a (C1), W6b (C2), W6c (C3), W6d (C4), W6e (C1+C2), W6f (C3+C4)

---

### **BUG #2: ITEM ASSIGNMENT CONSTRAINT** - CRITICAL! 🔥

**Line:** ~154 (R5 in Stage 1)

```python
# ❌ BASELINE: Includes BAX/BUP/T in sum
# R5: Asignación Única
for i in cargo.items:
    m.addConstr(quicksum(p[i.index, j.index] for j in cargo.uld) == 1)
```

**Should be:**
```python
# ✅ CORRECT: Exclude BAX/BUP/T
for i in cargo.items:
    m.addConstr(quicksum(p[i.index, j.index] 
                        for j in cargo.uld if j.isNeitherBAXnorBUPnorT) == 1)
```

**Impact:** CRITICAL - Fundamental constraint is wrong (though R6 prevents it)

---

### **🆕 BUG #10: COL/CRT LOGIC INCORRECT** - CRITICAL! 🔥

**Lines:** ~553-560 (W12 in Stage 3)

```python
# ❌ BASELINE: Per-POSITION constraint
if str(aircraft.aircraft_type) in ['772', '77W']:
    for t in aircraft.loadlocations_C1_C2:
        m.addConstr(quicksum(f[j, t.index] for j in uld_with_COL) + 
                   quicksum(f[k, t.index] for k in uld_with_CRT) <= 1)
```

**Problem:**
- Creates one constraint PER POSITION
- Allows COL at position 11L and CRT at position 12L (both in C1) - WRONG!
- Should be COMPARTMENT-level: COL and CRT cannot be in same compartment

**Should be:**
```python
# ✅ CORRECT: Compartment-level with big-M
COL_front = m.addVar(vtype=GRB.BINARY)  # 1 if COL in C1+C2
CRT_front = m.addVar(vtype=GRB.BINARY)  # 1 if CRT in C1+C2

m.addConstr(
    quicksum(f[j, t.index] for j in uld_with_COL for t in aircraft.loadlocations_C1_C2)
    <= big_M * COL_front
)
m.addConstr(
    quicksum(f[k, t.index] for k in uld_with_CRT for t in aircraft.loadlocations_C1_C2)
    <= big_M * CRT_front
)
m.addConstr(COL_front + CRT_front <= 1)  # Mutual exclusion at compartment level
```

**Impact:** CRITICAL - Allows COL and CRT in same compartment at different positions!

---

## ⚠️ **HIGH PRIORITY BUGS**

### **BUG #5: SEPARATION PENALTY** - Suboptimal

**Lines:** ~112-118 (Stage 1)

Same as Puttaert - uses binary penalty, not Y/Z counting.

**Impact:** Suboptimal separation minimization

---

### **🆕 BUG #11: MULTI-OBJECTIVE ENVIRONMENT MISMATCH** - Bug! 🔥

**Lines:** ~186-195 (Stage 1) and ~563-566 (Stage 3)

**Stage 1:**
```python
# Defines 4 objectives with indices 1, 2, 3, 4
m.setObjectiveN(obj_volume_preference, index=1, priority=4, weight=1)
m.setObjectiveN(obj2, index=2, priority=3, weight=1)
m.setObjectiveN(obj_underutilization, index=3, priority=2, weight=1)
m.setObjectiveN(obj3, index=4, priority=1, weight=1)

# But tries to access 4 environments (indices 1-4)
volume_env = m.getMultiobjEnv(1)
uld_env = m.getMultiobjEnv(2)
underutilization_env = m.getMultiobjEnv(3)
separation_env = m.getMultiobjEnv(4)
```

**Stage 3:**
```python
# Defines 2 objectives with indices 0 and 5
m.setObjectiveN(MAC_obj, index=0, priority=2, weight=-1)
m.setObjectiveN(obj4, index=5, priority=1, weight=1)

# But tries to access environments 0 and 5
WB_env = m.getMultiobjEnv(0)
bax_env = m.getMultiobjEnv(5)  # ❌ This is index 5 but only 2 objectives!
```

**Problems:**
1. **Index 0 missing** in Stage 1 (starts at 1)
2. **Index 5 invalid** in Stage 3 (only 2 objectives: should be indices 0 and 1)
3. **Inconsistent indexing** across stages

**Should be:**
```python
# Stage 1: Use indices 0-3
m.setObjectiveN(obj_volume_preference, index=0, priority=4, weight=1)
m.setObjectiveN(obj2, index=1, priority=3, weight=1)
# ...

# Stage 3: Use indices 0-1
m.setObjectiveN(MAC_obj, index=0, priority=2, weight=-1)
m.setObjectiveN(obj4, index=1, priority=1, weight=1)  # NOT index 5!

bax_env = m.getMultiobjEnv(1)  # Access index 1
```

**Impact:** Potential runtime error or undefined behavior

---

## 📊 **MEDIUM PRIORITY (Improvements)**

### **Design Differences (Not Bugs)**

**No Bug #4 (w variable):**
- ✅ Baseline correctly uses j.weight directly (no w variable)
- Stage 3 only has f variables, much simpler than Puttaert

**No Bug #7 (Big-M):**
- N/A - Baseline doesn't use Big-M in Stage 1
- Stage 3 doesn't need it either

**No Bug #8 (Position Weight Split):**
- ✅ Baseline correctly has one combined constraint (W5)

---

## 📋 **SUMMARY FOR BASELINE**

### **🔥 CRITICAL (3 bugs):**
1. ✅ **Bug #1:** Compartment weights (per-position → per-compartment) - **SAME AS PUTTAERT**
2. ✅ **Bug #2:** Item assignment (includes BAX/BUP/T) - **SAME AS PUTTAERT**
3. ✅ **Bug #10:** COL/CRT logic (per-position → compartment-level) - **NEW BUG!**

### **⚠️ HIGH PRIORITY (2 bugs):**
4. ⚠️ **Bug #5:** Separation penalty (binary vs Y/Z) - **SAME AS PUTTAERT**
5. ⚠️ **Bug #11:** Multi-objective indexing (0, 5 → 0, 1) - **NEW BUG!**

### **✅ CORRECT (3 features):**
- ✅ No w variable linearization (simpler than Puttaert)
- ✅ Combined position weight constraint
- ✅ MAC formula correct

---

## 🆕 **NEW BUGS DISCOVERED (Not in Original List)**

### **Bug #10: COL/CRT Per-Position Instead of Per-Compartment**
- Creates `f[COL] + f[CRT] <= 1` for each position
- Should be compartment-level mutual exclusion
- **Critical logic error**

### **Bug #11: Multi-Objective Index Mismatch**
- Stage 1 uses indices 1-4 (skips 0)
- Stage 3 uses indices 0, 5 (5 is invalid for 2 objectives)
- **Runtime error risk**

---

## 🎯 **FIXES REQUIRED**

### **Priority 1 (Correctness):**
1. Fix compartment weight constraints (W6a-W6f)
2. Fix item assignment (R5)
3. Fix COL/CRT logic (W12) - use compartment-level with big-M
4. Fix multi-objective indexing

### **Priority 2 (Quality):**
5. Improve separation penalty if desired

---

**Total New Bugs: 2 (Bug #10, Bug #11)**
**Total Bugs in Baseline: 5 (3 critical, 2 high priority)**


