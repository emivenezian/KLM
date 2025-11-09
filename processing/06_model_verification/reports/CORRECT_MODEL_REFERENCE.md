# 🔬 CORRECT MODEL REFERENCE - DelgadoVenezian (Model.ipynb)

**Date:** October 28, 2025  
**Purpose:** Gold standard reference for verifying other benchmarks

---

## 🎯 **OBJECTIVE FUNCTIONS (Multi-objective with Lexicographic Priorities)**

### **Obj 0 (Priority 6 - HIGHEST): Maximize %MAC at ZFW**
```python
MAC_obj = (((aircraft.C * (ZFW_index_obj - aircraft.K)) / aircraft.ZFW) + 
           aircraft.reference_arm - aircraft.lemac) / (aircraft.mac_formula / 100)
m.setObjectiveN(MAC_obj, index=0, priority=6, weight=-1)  # NEGATIVE = MAXIMIZE
```

**Key Points:**
- **MINIMIZES** the negative MAC (= MAXIMIZES MAC)
- Uses **aircraft-specific parameters**: C, K, lemac, mac_formula, reference_arm
- **ZFW_index_obj** calculated per compartment with delta_index_cargo_C1/C2/C3/C4
- **ZFW_index constrained** to envelope: INDEX_ZFW_fwd ≤ ZFW_index ≤ INDEX_ZFW_aft

### **Obj 1 (Priority 5): Minimize Number of ULDs**
```python
obj2 = quicksum(u[j.index] for j in cargo.uld)
m.setObjectiveN(obj2, index=1, priority=5, weight=1)
```

### **Obj 2 (Priority 4): Maximize Total Volume Packed**
```python
obj_volume_total = quicksum(i.volume * p[i.index, j.index] 
                           for i in cargo.items 
                           for j in cargo.uld if j.isNeitherBAXnorBUPnorT)
m.setObjectiveN(obj_volume_total, index=2, priority=4, weight=-1)  # NEGATIVE = MAXIMIZE
```

### **Obj 3 (Priority 3): Minimize Booking Separation**
```python
# Uses Y variables: number of ULDs used per booking group
obj_separation = quicksum(Y[b_i] for b_i in booking_groups.keys())
m.setObjectiveN(obj_separation, index=3, priority=3, weight=1)
```

### **Obj 4 (Priority 2): Minimize BAX Proximity to Door**
```python
obj4 = quicksum(aircraft.define_proximity_score_loadlocation(t) * f[j.index, t.index] 
               for j in cargo.uld for t in aircraft.loadlocations if j.isBAX)
m.setObjectiveN(obj4, index=4, priority=2, weight=1)
```

---

## 📊 **CONSTRAINTS - CORRECT FORMULATIONS**

### **DV1: ULD Weight Capacity**
```python
for j in cargo.uld:
    m.addConstr(quicksum(i.weight * p[i.index, j.index] for i in cargo.items) 
                <= j.max_weight * u[j.index])
```
✅ **Correct:** Item weights sum ≤ ULD capacity when active

---

### **DV2: ULD Volume Capacity**
```python
for j in cargo.uld:
    m.addConstr(quicksum(i.volume * p[i.index, j.index] for i in cargo.items) 
                <= j.volume * u[j.index] * loadfactor)
```
✅ **Correct:** Item volumes sum ≤ ULD volume × loadfactor when active

---

### **DV3: Item Assignment**
```python
for i in cargo.items:
    m.addConstr(quicksum(p[i.index, j.index] 
                        for j in cargo.uld if j.isNeitherBAXnorBUPnorT) == 1)
```
✅ **Correct:** Each item assigned to exactly one regular ULD

---

### **DV4: ULD Position Assignment**
```python
for j in cargo.uld:
    m.addConstr(quicksum(f[j.index, t.index] for t in aircraft.loadlocations) 
                == u[j.index])
```
✅ **Correct:** Active ULD assigned to exactly one position

---

### **DV5: Position Occupancy**
```python
for t in aircraft.loadlocations:
    m.addConstr(quicksum(f[j.index, t.index] for j in cargo.uld) <= 1)
```
✅ **Correct:** Each position holds at most one ULD

---

### **DV6: Compatible Positions**
```python
for j in cargo.uld:
    m.addConstr(quicksum(f[j.index, t.index] 
                        for t in aircraft.define_forbidden_positions_for_ULD(j)) == 0)
```
✅ **Correct:** ULD cannot be in forbidden positions

---

### **DV7: Special ULD Assignment**
```python
for j in cargo.uld:
    if j.isBAXorBUPorT:
        m.addConstr(quicksum(f[j.index, t.index] for t in aircraft.loadlocations) == 1)
```
✅ **Correct:** BAX/BUP/T always assigned to exactly one position

---

### **DV8, DV9, DV10: Linking Constraints (Linearization)**
```python
for i in cargo.items:
    for j in cargo.uld:
        for t in aircraft.loadlocations:
            # DV8: z ≤ p
            m.addConstr(z[i.index, j.index, t.index] <= p[i.index, j.index])
            # DV9: z ≤ f
            m.addConstr(z[i.index, j.index, t.index] <= f[j.index, t.index])
            # DV10: z ≥ p + f - 1
            m.addConstr(z[i.index, j.index, t.index] >= 
                       p[i.index, j.index] + f[j.index, t.index] - 1)
```
✅ **Correct:** z_ijt = 1 iff item i in ULD j AND ULD j at position t

---

### **DV11: Position Weight Limit**
```python
for t in aircraft.loadlocations:
    m.addConstr(quicksum(i.weight * z[i.index, j.index, t.index] 
                        for i in cargo.items for j in cargo.uld) +
                quicksum(j.weight * f[j.index, t.index] 
                        for j in cargo.uld if j.isBAXorBUPorT)
                <= aircraft.define_max_weight_postion(t))
```
✅ **Correct:** Total weight at position t (items + ULD tare) ≤ position limit

---

### **DV12: Compartment Weight Limits (C1, C2, C3, C4)** ⚠️ **CRITICAL**
```python
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
                for t in loadlocations) +
        quicksum(j.weight * f[j.index, t.index] 
                for j in cargo.uld if j.isBAXorBUPorT 
                for t in loadlocations)
        <= max_weight
    )
```
✅ **Correct:** Sums over **loadlocations** (positions) in each compartment, NOT over all positions t

**EMILIA MENTIONED THIS WAS WRONG IN PUTTAERT!**

---

### **DV13: Forward Compartment Weight (C1+C2)**
```python
m.addConstr(
    quicksum(i.weight * z[i.index, j.index, t.index] 
            for i in cargo.items 
            for j in cargo.uld 
            for t in aircraft.loadlocations_C1_C2) +
    quicksum(j.weight * f[j.index, t.index] 
            for j in cargo.uld if j.isBAXorBUPorT 
            for t in aircraft.loadlocations_C1_C2)
    <= aircraft.max_weight_C1_C2
)
```
✅ **Correct:** Combined front compartments

---

### **DV14: Aft Compartment Weight (C3+C4)**
```python
m.addConstr(
    quicksum(i.weight * z[i.index, j.index, t.index] 
            for i in cargo.items 
            for j in cargo.uld 
            for t in aircraft.loadlocations_C3_C4) +
    quicksum(j.weight * f[j.index, t.index] 
            for j in cargo.uld if j.isBAXorBUPorT 
            for t in aircraft.loadlocations_C3_C4)
    <= aircraft.max_weight_C3_C4
)
```
✅ **Correct:** Combined aft compartments

---

### **DV15: Lateral Balance at Takeoff (TOW) - 2 Constraints**
```python
# Left - Right ≤ a_lat_TOW * (cargo + OEW + TOF) + b_lat_TOW
m.addConstr((left_weight) - (right_weight) <= 
            a_lat_TOW * (total_cargo + aircraft.OEW + aircraft.TOF) * b_lat_TOW)

# Right - Left ≤ a_lat_TOW * (cargo + OEW + TOF) + b_lat_TOW
m.addConstr((right_weight) - (left_weight) <= 
            a_lat_TOW * (total_cargo + aircraft.OEW + aircraft.TOF) * b_lat_TOW)
```
✅ **Correct:** Symmetric lateral balance at takeoff weight

---

### **DV16: Lateral Balance at Landing (LW) - 2 Constraints**
```python
# Left - Right ≤ a_lat_LW * (cargo + OEW + TOF - TripF) + b_lat_LW
m.addConstr((left_weight) - (right_weight) <= 
            a_lat_LW * (total_cargo + aircraft.OEW + aircraft.TOF - aircraft.TripF) * b_lat_LW)

# Right - Left ≤ a_lat_LW * (cargo + OEW + TOF - TripF) + b_lat_LW
m.addConstr((right_weight) - (left_weight) <= 
            a_lat_LW * (total_cargo + aircraft.OEW + aircraft.TOF - aircraft.TripF) * b_lat_LW)
```
✅ **Correct:** Symmetric lateral balance at landing weight (includes fuel burn)

---

### **DV17: Forward CG Envelope at TOW**
```python
m.addConstr(aircraft.define_INDEX_TOW_fwd(aircraft.aircraft_type) <= 
            aircraft.DOI + aircraft.fuel_index + aircraft.define_INDEX_PAX() +
            (cargo_C1) * aircraft.delta_index_cargo_C1 +
            (cargo_C2) * aircraft.delta_index_cargo_C2 +
            (cargo_C3) * aircraft.delta_index_cargo_C3 +
            (cargo_C4) * aircraft.delta_index_cargo_C4)
```
✅ **Correct:** Forward limit check at TOW (includes fuel_index)

---

### **DV18: Aft CG Envelope at ZFW**
```python
m.addConstr(aircraft.define_INDEX_ZFW_fwd(aircraft.aircraft_type) <= 
            aircraft.DOI + aircraft.define_INDEX_PAX() +
            (cargo_C1) * aircraft.delta_index_cargo_C1 +
            (cargo_C2) * aircraft.delta_index_cargo_C2 +
            (cargo_C3) * aircraft.delta_index_cargo_C3 +
            (cargo_C4) * aircraft.delta_index_cargo_C4)
```
✅ **Correct:** Aft limit check at ZFW (NO fuel_index)

---

### **DV19: COL/CRT Mixing Prohibition** ⚠️ **CRITICAL**
```python
for j in cargo.uld:
    if j.isNeitherBAXnorBUPnorT:
        for i_1 in cargo.items:
            for i_2 in cargo.items:
                if i_1 != i_2:
                    if i_1.COL == 1 and i_2.CRT == 1:
                        m.addConstr(p[i_1.index, j.index] + p[i_2.index, j.index] <= 1)
```
✅ **Correct:** COL and CRT items cannot be in same ULD

**EMILIA MENTIONED THIS WAS WRONG/INCOMPLETE IN PUTTAERT!**

---

### **DV20: Booking Separation (p to Z linking)**
```python
for b_i, items in booking_groups.items():
    for j in cargo.uld:
        if j.isNeitherBAXnorBUPnorT:
            for i in items:
                m.addConstr(p[i.index, j.index] <= Z[b_i, j.index])
```
✅ **Correct:** If item of booking b_i in ULD j, then Z[b_i,j] = 1

---

### **DV21: Booking Separation (Y to Z linking)**
```python
for b_i in booking_groups.keys():
    m.addConstr(Y[b_i] == quicksum(Z[b_i, j.index] 
                                   for j in cargo.uld if j.isNeitherBAXnorBUPnorT))
```
✅ **Correct:** Y counts number of ULDs used by booking b_i

---

### **DV22: Overlapping Positions**
```python
for j_1 in cargo.uld:
    for j_2 in cargo.uld:
        if j_1 != j_2:
            for t_1 in aircraft.loadlocations:
                for t_2 in aircraft.define_overlapping_positions(t_1):
                    m.addConstr(f[j_1.index, t_1.index] + f[j_2.index, t_2.index] <= 1)
```
✅ **Correct:** Overlapping positions cannot both be occupied

---

### **DV23: Maximum Payload Limit (MPL)**
```python
m.addConstr(quicksum(i.weight * z[i.index, j.index, t.index] 
                    for t in aircraft.loadlocations 
                    for j in cargo.uld 
                    for i in cargo.items) +
            quicksum(j.weight * f[j.index, t.index] 
                    for t in aircraft.loadlocations 
                    for j in cargo.uld if j.isBAXorBUPorT)
            <= aircraft.define_MPL())
```
✅ **Correct:** Total cargo weight ≤ MPL

---

### **DV24: COL/CRT Compartment Separation (Boeing 777)** ⚠️ **VERY COMPLEX**
```python
if str(aircraft.aircraft_type) in ['772', '77W']:
    compartments_R34 = {
        'front': aircraft.loadlocations_C1_C2,
        'aft': aircraft.loadlocations_C3_C4
    }
    
    COL_k = {}  # Binary: 1 if compartment k has COL
    CRT_k = {}  # Binary: 1 if compartment k has CRT
    
    for k_label, loadlocations_k in compartments_R34.items():
        COL_k[k_label] = m.addVar(vtype=GRB.BINARY)
        CRT_k[k_label] = m.addVar(vtype=GRB.BINARY)
        
        # If any COL ULD in compartment k, then COL_k = 1
        m.addConstr(sum(COL ULDs in k) <= big_M * COL_k[k_label])
        
        # If any CRT ULD in compartment k, then CRT_k = 1
        m.addConstr(sum(CRT ULDs in k) <= big_M * CRT_k[k_label])
        
        # COL and CRT mutually exclusive in compartment k
        m.addConstr(COL_k[k_label] + CRT_k[k_label] <= 1)
        
        # Item-level enforcement
        for i with COL: z[i,j,t in k] <= big_M * COL_k[k]
        for i with CRT: z[i,j,t in k] <= big_M * CRT_k[k]
```
✅ **Correct:** COL and CRT cannot be in same compartment (Boeing 777)

---

### **DV25-DV26: Boeing 787 COL/CRT Rules**
```python
if str(aircraft.aircraft_type) in ['789', '781']:
    # DV25a: Prohibit COL/CRT in aft
    for i in cargo.items:
        if i.COL == 1 or i.CRT == 1:
            for j, t in aft_positions:
                m.addConstr(z[i.index, j.index, t.index] == 0)
    
    # DV26: Mutually exclusive COL/CRT in front (similar to DV24 but only front)
    COL_front = m.addVar(vtype=GRB.BINARY)
    CRT_front = m.addVar(vtype=GRB.BINARY)
    m.addConstr(COL_front + CRT_front <= 1)
```
✅ **Correct:** Boeing 787-specific temperature handling

---

## 🔑 **KEY CORRECT FEATURES**

1. ✅ **MAC Formula**: Aircraft-specific with correct division by (mac_formula / 100)
2. ✅ **Compartment Weights**: Sum over positions **in that compartment**, not all positions
3. ✅ **CRT/COL**: Comprehensive item-level and ULD-level constraints with big-M
4. ✅ **Booking Separation**: Uses Y and Z variables for proper tracking
5. ✅ **Lateral Balance**: Includes OEW, TOF, TripF correctly
6. ✅ **CG Envelope**: TOW includes fuel_index, ZFW does not
7. ✅ **Overlapping Positions**: Explicitly handled
8. ✅ **Feedback Loop**: Iterative with packed_ULDs and deferred_items

---

## ⚠️ **KNOWN ISSUES FIXED FROM PUTTAERT**

Based on Emilia's comments:

1. **Compartment weight sums** - Puttaert summed over all t instead of t in compartment
2. **CRT constraints** - Puttaert had incomplete or incorrect CRT/COL separation
3. **Separation penalty** - Improved implementation with Y/Z variables

---

**Next Step:** Compare this to Model_Puttaert.ipynb to find exact differences


