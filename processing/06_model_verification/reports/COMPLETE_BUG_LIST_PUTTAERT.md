# 🔬 COMPLETE BUG LIST - Model_Puttaert.ipynb vs Model.ipynb

**Systematic Constraint-by-Constraint Comparison**

---

## 🐛 **BUG #1: COMPARTMENT WEIGHT CONSTRAINTS** - CRITICAL! 🔥

**Lines:** ~298-322 in Puttaert

### **The Bug:**
```python
# ❌ PUTTAERT: One constraint PER POSITION
for t in aircraft.loadlocations_C1:
    m.addConstr(...weight_at_t... <= aircraft.max_weight_C1)
```

### **The Fix:**
```python
# ✅ DELGADOVENEZIAN: One constraint for ENTIRE COMPARTMENT
m.addConstr(
    quicksum(...for t in aircraft.loadlocations_C1...) <= aircraft.max_weight_C1
)
```

### **Impact:** CRITICAL - Allows up to N × compartment_limit total weight

**Applies to:** C1, C2, C3, C4, C1+C2, C3+C4 (6 constraint groups)

---

## 🐛 **BUG #2: ITEM ASSIGNMENT CONSTRAINT** - CRITICAL! 🔥

**Line:** ~220 in Puttaert vs ~210 in DelgadoVenezian

### **The Bug:**
```python
# ❌ PUTTAERT: Allows items in ANY ULD (including BAX/BUP/T)
for i in cargo.items:
    m.addConstr(quicksum(p[i.index, j.index] for j in cargo.uld) == 1)
```

### **The Fix:**
```python
# ✅ DELGADOVENEZIAN: Only allows items in regular ULDs
for i in cargo.items:
    m.addConstr(quicksum(p[i.index, j.index] 
                        for j in cargo.uld if j.isNeitherBAXnorBUPnorT) == 1)
```

### **Impact:** 
- CRITICAL! Puttaert could theoretically assign cargo items to BAX/BUP/T ULDs
- Though constraint C_combi_3 (p[i,j] = 0 for BAX) might prevent this, the fundamental constraint is wrong
- **Inconsistent formulation** - relies on another constraint to enforce correctness

---

## 🐛 **BUG #3: CRT/COL COMPARTMENT LOGIC** - CRITICAL! 🔥

**Lines:** ~395-487 in Puttaert

### **The Bug:**
- Creates O(n_COL × n_CRT × n_ULD × n_positions) auxiliary variables
- Complex nested loops with unclear logic
- `quicksum(COL_C1_C2 + CRT_C1_C2 for t in aircraft.loadlocations_C1_C2) == 0`
  - This forces sum = 0, meaning NO COL or CRT items can be placed? Unclear intent.

### **The Fix:**
- Uses 2 compartment-level binary variables (COL_k, CRT_k) per compartment
- Clean big-M formulation: `COL_k + CRT_k <= 1`
- Clear separation of ULD-level and item-level enforcement

### **Impact:** CRITICAL - Complex, inefficient, possibly incorrect logic

---

## 🐛 **BUG #4: LINEARIZATION WITH 'w' VARIABLE** - Inefficiency ⚠️

**Lines:** ~38-273 in Puttaert

### **The Bug:**
```python
# ❌ PUTTAERT: Creates w[i,j,t] continuous variable
w[i.index, j.index, t.index] = m.addVar(vtype=GRB.CONTINUOUS)

# Then uses w in ZFW_index and everywhere else
# Requires 7 linking constraints per (i,j,t)
```

### **The Fix:**
```python
# ✅ DELGADOVENEZIAN: Uses i.weight * z directly
quicksum(i.weight * z[i.index, j.index, t.index] ...)

# Only needs 3 linking constraints for z
```

### **Impact:** 
- Adds O(n_items × n_ULD × n_positions) variables
- Adds 7 × (n_items × n_ULD × n_positions) constraints
- **Slower solve times, more memory**

---

## 🐛 **BUG #5: SEPARATION PENALTY LOGIC** - Suboptimal ⚠️

**Lines:** ~167-187 in Puttaert

### **The Bug:**
```python
# ❌ PUTTAERT: Binary "is prefix in this ULD?"
separation_penalty[prefix, j.index] = m.addVar(vtype=GRB.BINARY)

# Objective: sum of all penalties
obj3 = quicksum(separation_penalty.values())
```

**Issue:** Only tracks IF separated, not HOW MANY ULDs used

### **The Fix:**
```python
# ✅ DELGADOVENEZIAN: Integer Y counts ULDs per booking
Y[b_i] = m.addVar(vtype=GRB.INTEGER)
Z[b_i, j] = m.addVar(vtype=GRB.BINARY)

# Y = count of ULDs used by booking
m.addConstr(Y[b_i] == quicksum(Z[b_i, j] for j in ULDs))

# Objective: minimize total ULDs
obj_separation = quicksum(Y[b_i] for b_i in bookings)
```

### **Impact:** Suboptimal - doesn't minimize ULD count per booking effectively

---

## 🐛 **BUG #6: OBJECTIVE HIERARCHY** - Different Structure

**Puttaert has 6 objectives:**
1. Priority 6: %MAC
2. Priority 5: Volume preference (AKE vs PMC/PAG)
3. Priority 4: Number of ULDs
4. Priority 3: Underutilization penalty
5. Priority 2: Separation penalty
6. Priority 1: BAX proximity

**DelgadoVenezian has 5 objectives:**
1. Priority 6: %MAC
2. Priority 5: Number of ULDs
3. Priority 4: Total volume (maximize)
4. Priority 3: Separation penalty (improved Y/Z)
5. Priority 2: BAX proximity

### **Key Differences:**
- **Eliminated:** Volume preference objective (obj2)
- **Eliminated:** Underutilization penalty objective (obj3 in Puttaert)
- **Added:** Total volume maximization (simpler)
- **Changed:** Separation penalty logic (Y/Z instead of binary per prefix)
- **Changed priorities:** Shifted priorities after removing objectives

### **Impact:**
- Different optimization behavior
- DelgadoVenezian is simpler and more direct
- **This is intentional redesign, not a "bug" but important difference**

---

## 🐛 **BUG #7: BIG-M PARAMETER** - Hardcoded vs Dynamic

**Line:** ~15 in Puttaert

### **Puttaert:**
```python
M = 100000000000  # Hardcoded huge number
```

### **DelgadoVenezian:**
```python
M = max([i.weight for i in cargo.items])  # Dynamic based on data
```

### **Impact:**
- **Minor** - Puttaert's huge M can cause numerical issues
- DelgadoVenezian's dynamic M is more numerically stable
- **Should be fixed** for better solver performance

---

## 🐛 **BUG #8: POSITION WEIGHT CONSTRAINTS** - Redundant Split

**Lines:** ~288-294 in Puttaert

### **Puttaert:**
```python
# Two separate constraints for position weight
for t in aircraft.loadlocations:
    m.addConstr(quicksum(w[i,j,t] ...) <= max_weight(t))  # Items
    m.addConstr(quicksum(j.weight * f[j,t] ...) <= max_weight(t))  # ULDs
```

### **DelgadoVenezian:**
```python
# One combined constraint
for t in aircraft.loadlocations:
    m.addConstr(
        quicksum(i.weight * z[i,j,t] ...) + 
        quicksum(j.weight * f[j,t] ...) 
        <= max_weight(t)
    )
```

### **Impact:**
- **Minor inefficiency** - Puttaert creates 2× constraints
- DelgadoVenezian is cleaner and more direct
- **Should be combined** for efficiency

---

## 🐛 **BUG #9: MULTI-OBJECTIVE ENVIRONMENT SETUP** - Inconsistent

**Lines:** ~492-517 in Puttaert vs ~625-642 in DelgadoVenezian

### **Puttaert:**
```python
WB_env = m.getMultiobjEnv(0)
volume_env = m.getMultiobjEnv(1)
uld_env = m.getMultiobjEnv(2)
underutilization_env = m.getMultiobjEnv(3)
separation_env = m.getMultiobjEnv(4)
bax_env = m.getMultiobjEnv(5)
```

### **DelgadoVenezian:**
```python
envs = [m.getMultiobjEnv(i) for i in range(6)]
envs[0].setParam(GRB.Param.TimeLimit, 60)  # %MAC
envs[1].setParam(GRB.Param.TimeLimit, 15)  # Number of ULDs
# ... etc
```

### **Impact:**
- **Minor** - DelgadoVenezian is cleaner with list comprehension
- Functionally equivalent but Puttaert has **6 objectives** vs **5** in DelgadoVenezian
- Must match the number of actual objectives

---

## 📋 **SUMMARY: ALL BUGS PRIORITIZED**

### **🔥 CRITICAL (MUST FIX):**
1. ✅ **Bug #1:** Compartment weight constraints (per-position → per-compartment)
2. ✅ **Bug #2:** Item assignment (allow BAX/BUP/T → exclude them)
3. ✅ **Bug #3:** CRT/COL compartment logic (complex → clean big-M)

### **⚠️ HIGH PRIORITY (SHOULD FIX):**
4. ⚠️ **Bug #4:** w variable linearization (eliminate for efficiency)
5. ⚠️ **Bug #5:** Separation penalty (upgrade to Y/Z counting)
6. ⚠️ **Bug #7:** Big-M parameter (hardcoded → dynamic)

### **📊 MEDIUM (SHOULD IMPROVE):**
7. ⚠️ **Bug #8:** Position weight constraints (split → combined)
8. ⚠️ **Bug #9:** Multi-objective setup (match objective count)

### **🎯 DESIGN DIFFERENCES (INTENTIONAL):**
- **Bug #6:** Objective hierarchy (different by design - not really a "bug")

---

## 🎯 **NEXT: VERIFY THESE IN OTHER BENCHMARKS**

**For Baseline, Optimized_Actual, BAX_Fixed, check:**

### **Priority 1 (Correctness):**
- [ ] Bug #1: Compartment weights (sum over compartment, not per-position)
- [ ] Bug #2: Item assignment (exclude BAX/BUP/T in constraint)
- [ ] Bug #3: CRT/COL logic (use clean big-M formulation)

### **Priority 2 (Efficiency/Quality):**
- [ ] Bug #4: No w variable (use z directly)
- [ ] Bug #5: Separation penalty (use Y/Z if present)
- [ ] Bug #7: Dynamic big-M (not hardcoded)
- [ ] Bug #8: Combined position weight constraint
- [ ] Bug #9: Correct multi-objective count

### **Also Check:**
- [ ] MAC formula correctness
- [ ] Objective hierarchy matches intent
- [ ] All use same input data/parameters

---

**Total Bugs Found: 9 (3 critical, 3 high priority, 3 medium)**


