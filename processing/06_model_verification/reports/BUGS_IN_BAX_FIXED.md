# 🐛 BUGS FOUND IN BAX_FIXED.IPYNB

**Model Type:** Based on Puttaert + BAX positions fixed to actual

---

## 🔥 **CRITICAL BUGS (MUST FIX)**

### **BUG #1: COMPARTMENT WEIGHT CONSTRAINTS** - CRITICAL! 🔥

**Lines:** ~168-193 (P13-P18)

```python
# ❌ BAX_FIXED: One constraint PER POSITION (same as Puttaert)
for t in aircraft.loadlocations_C1:
    m.addConstr(quicksum(w[i.index, j.index, t.index] for i in cargo.items for j in cargo.uld) +
                quicksum(j.weight * f[j.index, t.index] for j in cargo.uld if j.isBAXorBUPorT)
                <= aircraft.max_weight_C1, name=f'C_Added_1_{t.index}')
```

**Should be:**
```python
# ✅ CORRECT: One constraint for ENTIRE COMPARTMENT
m.addConstr(
    quicksum(i.weight * z[i.index, j.index, t.index] 
            for i in cargo.items for j in cargo.uld 
            for t in aircraft.loadlocations_C1) +
    quicksum(j.weight * f[j.index, t.index] 
            for j in cargo.uld if j.isBAXorBUPorT 
            for t in aircraft.loadlocations_C1)
    <= aircraft.max_weight_C1
)
```

**Impact:** CRITICAL - Same as all others, allows N × compartment_limit

**Applies to:** P13 (C1), P14 (C2), P15 (C3), P16 (C4), P17 (C1+C2), P18 (C3+C4)

---

### **BUG #2: ITEM ASSIGNMENT CONSTRAINT** - CRITICAL! 🔥

**Line:** ~125 (P5)

```python
# ❌ BAX_FIXED: Includes BAX/BUP/T in sum
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

**Impact:** CRITICAL - Same as Puttaert, fundamental constraint wrong

---

### **BUG #3: CRT/COL COMPARTMENT LOGIC** — ✅ FIXED

*Lines corregidas:* `BAX_Fixed.ipynb` (~236-345)

- Se reemplazó la lógica explosiva por un esquema Big-M compacto por compartimento.
- Nuevas binarias `COL_k` y `CRT_k` controlan presencia de carga especial por sección (front/aft).
- Se consideran tanto items reasignados (`z`) como ULDs pre-etiquetados (`f`), replicando el enfoque de `Model.ipynb`.

> **Estado:** corregido (abril 2025)

**Impact:** CRITICAL - Same as Puttaert

---

## ⚠️ **HIGH PRIORITY BUGS**

### **BUG #4: LINEARIZATION WITH 'w' VARIABLE** - Inefficiency

**Lines:** ~38-148 (creates w variables and L1-L7 constraints)

Same as Puttaert:
- Extra w[i,j,t] continuous variables
- 7 linearization constraints instead of 3

**Impact:** Slower solve times, more memory

---

### **BUG #5: SEPARATION PENALTY** - Suboptimal

**Lines:** ~150-165

Same as Puttaert - uses binary penalty, not Y/Z counting

**Impact:** Suboptimal separation minimization

---

### **BUG #7: BIG-M HARDCODED** - Numerical Issues

**Line:** ~15

```python
M = 100000000000  # Hardcoded
```

Should be:
```python
M = max([i.weight for i in cargo.items])  # Dynamic
```

**Impact:** Numerical instability

---

### **BUG #8: POSITION WEIGHT SPLIT** - Inefficiency

**Lines:** ~156-162 (P12)

Same as Puttaert - splits into 2 constraints instead of combining

**Impact:** 2× constraints created

---

### **BUG #10: COL/CRT PER-POSITION** — ✅ FIXED

*Lines corregidas:* `BAX_Fixed.ipynb` (~236-420)

- Las restricciones ahora agregan por compartimento (no por posición individual).
- Para 772/77W se impone exclusión mutua COL/CRT por sección (`front`, `aft`).
- Para 789/781 se bloquea cualquier COL/CRT en compartimentos traseros y se mantiene exclusión en el frente.

> **Estado:** corregido junto con BUG #3 (abril 2025)

---

## ✅ **CORRECT FEATURES**

### **✅ BF1: BAX Position Fixed** - Special Feature
```python
for j in cargo.uld:
    if j.isBAX:
        index_position_bax = [t.index for t in aircraft.loadlocations 
                             if t.location == j.actual_position_bax][0]
        m.addConstr(f[j.index, index_position_bax] == 1)
```
✅ This is the unique feature of this model - correctly implemented!

### **✅ MAC Formula**
✅ Same as DelgadoVenezian - CORRECT!

### **✅ Lateral Balance**
✅ Includes OEW, TOF, TripF correctly

### **✅ CG Envelope**
✅ TOW includes fuel_index, ZFW excludes it - CORRECT!

### **✅ Overlapping Positions**
✅ Handled correctly (P11)

---

## 📋 **SUMMARY FOR BAX_FIXED**

### **🔥 CRITICAL (4 bugs):**
1. ✅ **Bug #1:** Compartment weights (per-position → per-compartment) lo cambie 
2. ✅ **Bug #2:** Item assignment (includes BAX/BUP/T) no por ahora
3. ✅ **Bug #3:** CRT/COL complex logic (needs big-M simplification) 
4. ✅ **Bug #10:** COL/CRT per-position (needs compartment-level) lo cambie. 

### **⚠️ HIGH PRIORITY (4 bugs):**
5. ⚠️ **Bug #4:** w variable linearization
6. ⚠️ **Bug #5:** Separation penalty
7. ⚠️ **Bug #7:** Big-M hardcoded
8. ⚠️ **Bug #8:** Position weight split

### **✅ CORRECT (Special Feature):**
- ✅ BF1: BAX position fixed constraint (unique to this model)
- ✅ MAC formula
- ✅ Lateral balance
- ✅ CG envelope
- ✅ Overlapping positions

---

**Total Bugs in BAX_Fixed: 8 (4 critical, 4 high priority)**

**This is essentially Puttaert + BAX fixed, so inherits all Puttaert bugs!**


