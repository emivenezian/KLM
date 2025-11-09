# 🔑 KEY CORRECT IMPLEMENTATIONS - What to Check in Other Models

**Purpose:** Focus on the 3 main areas Emilia fixed from Puttaert

---

## 1️⃣ **MAC FORMULA** ✅

### **Correct Implementation (Model.ipynb):**
```python
MAC_obj = (((aircraft.C * (ZFW_index_obj - aircraft.K)) / aircraft.ZFW) + 
           aircraft.reference_arm - aircraft.lemac) / (aircraft.mac_formula / 100)
```

### **What to Check:**
- [ ] Aircraft-specific parameters: `C`, `K`, `lemac`, `mac_formula`, `reference_arm`
- [ ] Final division by `(aircraft.mac_formula / 100)` is present
- [ ] `ZFW_index_obj` calculated correctly per compartment
- [ ] Objective uses `weight=-1` (MAXIMIZE MAC)

---

## 2️⃣ **COMPARTMENT WEIGHT CONSTRAINTS** ✅ ⚠️ **CRITICAL - EMILIA'S FIX**

### **Correct Implementation (Model.ipynb):**
```python
# DV12: Individual compartments
compartments = [
    ('C1', aircraft.max_weight_C1, aircraft.loadlocations_C1),
    ('C2', aircraft.max_weight_C2, aircraft.loadlocations_C2),
    ('C3', aircraft.max_weight_C3, aircraft.loadlocations_C3),
    ('C4', aircraft.max_weight_C4, aircraft.loadlocations_C4),
]

for compartment, max_weight, loadlocations in compartments:
    m.addConstr(
        quicksum(i.weight * z[i.index, j.index, t.index] 
                for i in cargo.items 
                for j in cargo.uld 
                for t in loadlocations) +  # ← CORRECT: sum over loadlocations IN compartment
        quicksum(j.weight * f[j.index, t.index] 
                for j in cargo.uld if j.isBAXorBUPorT 
                for t in loadlocations)    # ← CORRECT: sum over loadlocations IN compartment
        <= max_weight
    )
```

### **WRONG Implementation (Puttaert had this):**
```python
# ❌ WRONG: Summing over ALL t in aircraft.loadlocations
for t in aircraft.loadlocations:  # ← WRONG: should be "for t in loadlocations_C1"
    m.addConstr(
        quicksum(i.weight * z[i.index, j.index, t.index] ...) <= max_weight_C1
    )
```

### **What to Check:**
- [ ] **For C1**: Sum over `t in aircraft.loadlocations_C1` (NOT all loadlocations)
- [ ] **For C2**: Sum over `t in aircraft.loadlocations_C2`
- [ ] **For C3**: Sum over `t in aircraft.loadlocations_C3`
- [ ] **For C4**: Sum over `t in aircraft.loadlocations_C4`
- [ ] **For C1+C2**: Sum over `t in aircraft.loadlocations_C1_C2`
- [ ] **For C3+C4**: Sum over `t in aircraft.loadlocations_C3_C4`
- [ ] Includes both item weights AND ULD tare weights (j.weight for BAX/BUP/T)

---

## 3️⃣ **CRT/COL CONSTRAINTS** ✅ ⚠️ **CRITICAL - EMILIA'S FIX**

### **Correct Implementation (Model.ipynb):**

#### **3A. Item-Level Mixing Prohibition (DV19)**
```python
# COL and CRT items cannot be in same ULD
for j in cargo.uld:
    if j.isNeitherBAXnorBUPnorT:
        for i_1 in cargo.items:
            for i_2 in cargo.items:
                if i_1 != i_2:
                    if i_1.COL == 1 and i_2.CRT == 1:
                        m.addConstr(p[i_1.index, j.index] + p[i_2.index, j.index] <= 1)
```

#### **3B. Compartment-Level Separation (Boeing 777 - DV24)**
```python
if str(aircraft.aircraft_type) in ['772', '77W']:
    for k_label in ['front', 'aft']:  # front=C1+C2, aft=C3+C4
        COL_k[k_label] = m.addVar(vtype=GRB.BINARY)  # 1 if k has COL
        CRT_k[k_label] = m.addVar(vtype=GRB.BINARY)  # 1 if k has CRT
        
        # Big-M constraints to detect presence
        m.addConstr(sum(COL ULDs in k) <= big_M * COL_k[k_label])
        m.addConstr(sum(CRT ULDs in k) <= big_M * CRT_k[k_label])
        
        # Mutual exclusion
        m.addConstr(COL_k[k_label] + CRT_k[k_label] <= 1)
        
        # Item-level enforcement
        for i with COL:
            m.addConstr(sum(z[i,j,t] for t in k) <= big_M * COL_k[k])
        for i with CRT:
            m.addConstr(sum(z[i,j,t] for t in k) <= big_M * CRT_k[k])
```

#### **3C. Boeing 787 Rules (DV25-DV26)**
```python
if str(aircraft.aircraft_type) in ['789', '781']:
    # Prohibit COL/CRT in aft (C3+C4)
    for i with COL or CRT:
        for j, t in aft_positions:
            m.addConstr(z[i.index, j.index, t.index] == 0)
    
    # Mutually exclusive in front (C1+C2)
    COL_front = m.addVar(vtype=GRB.BINARY)
    CRT_front = m.addVar(vtype=GRB.BINARY)
    m.addConstr(COL_front + CRT_front <= 1)
```

### **What to Check:**
- [ ] **Item-level**: COL and CRT items cannot be in same ULD
- [ ] **ULD-level**: COL and CRT ULDs tracked correctly
- [ ] **Boeing 777**: COL and CRT cannot be in same compartment (front or aft)
- [ ] **Boeing 787**: COL/CRT prohibited in aft, mutually exclusive in front
- [ ] **Big-M values**: Correctly calculated (e.g., `len(U_COL) * len(loadlocations_k)`)
- [ ] Both `i.COL` (item property) and `j.COL` (ULD property) handled

---

## 4️⃣ **SEPARATION PENALTY** ✅ (Improved from Puttaert)

### **Correct Implementation (Model.ipynb):**
```python
# Uses Y and Z variables
Y = {}  # Number of ULDs used for booking b_i
Z = {}  # Binary: 1 if booking b_i has items in ULD j

for b_i in booking_groups.keys():
    Y[b_i] = m.addVar(vtype=GRB.INTEGER, lb=0)
    for j in cargo.uld:
        if j.isNeitherBAXnorBUPnorT:
            Z[b_i, j.index] = m.addVar(vtype=GRB.BINARY)

# Objective: Minimize sum of Y (total ULDs used across all bookings)
obj_separation = quicksum(Y[b_i] for b_i in booking_groups.keys())

# Constraints:
# DV20: If item of booking b_i in ULD j, then Z[b_i,j] = 1
for b_i, items in booking_groups.items():
    for j in cargo.uld if j.isNeitherBAXnorBUPnorT:
        for i in items:
            m.addConstr(p[i.index, j.index] <= Z[b_i, j.index])

# DV21: Y counts number of ULDs used by booking b_i
for b_i in booking_groups.keys():
    m.addConstr(Y[b_i] == quicksum(Z[b_i, j.index] 
                                   for j in cargo.uld if j.isNeitherBAXnorBUPnorT))
```

### **What to Check:**
- [ ] Uses Y (integer) and Z (binary) variables
- [ ] Objective minimizes `sum(Y[b_i])`
- [ ] Linking constraint: `p[i,j] <= Z[b_i,j]`
- [ ] Counting constraint: `Y[b_i] = sum(Z[b_i,j])`

---

## 5️⃣ **ADDITIONAL CORRECT FEATURES**

### **5A. Objective Hierarchy**
```python
# Priority 6 (highest): %MAC
m.setObjectiveN(MAC_obj, index=0, priority=6, weight=-1)

# Priority 5: Minimize ULDs
m.setObjectiveN(obj2, index=1, priority=5, weight=1)

# Priority 4: Maximize volume
m.setObjectiveN(obj_volume_total, index=2, priority=4, weight=-1)

# Priority 3: Minimize separation
m.setObjectiveN(obj_separation, index=3, priority=3, weight=1)

# Priority 2: Minimize BAX proximity
m.setObjectiveN(obj4, index=4, priority=2, weight=1)
```

### **5B. Overlapping Positions**
```python
for j_1 in cargo.uld:
    for j_2 in cargo.uld:
        if j_1 != j_2:
            for t_1 in aircraft.loadlocations:
                for t_2 in aircraft.define_overlapping_positions(t_1):
                    m.addConstr(f[j_1.index, t_1.index] + f[j_2.index, t_2.index] <= 1)
```

### **5C. Lateral Balance**
```python
# Includes OEW, TOF, TripF correctly
# TOW: cargo + OEW + TOF
# LW: cargo + OEW + TOF - TripF
```

---

## 📋 **VERIFICATION CHECKLIST FOR OTHER MODELS**

When checking Baseline, Optimized_Actual, BAX_Fixed:

### **Priority 1 (MUST FIX):**
- [ ] **Compartment weights**: Sum over positions in that compartment ONLY
- [ ] **CRT/COL mixing**: Proper constraints at item and compartment levels
- [ ] **MAC formula**: Correct with all parameters and final division

### **Priority 2 (IMPORTANT):**
- [ ] **Objective**: Minimizes negative MAC (= maximizes)
- [ ] **Separation penalty**: Uses Y/Z or equivalent correct logic
- [ ] **Lateral balance**: Includes OEW, TOF, TripF correctly

### **Priority 3 (CHECK):**
- [ ] **CG envelope**: TOW has fuel_index, ZFW doesn't
- [ ] **Overlapping positions**: Handled explicitly
- [ ] **Input data**: Same aircraft/cargo parameters

---

**Next:** Compare Model.ipynb vs Model_Puttaert.ipynb to find exact bugs Emilia fixed


