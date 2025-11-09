# LaTeX Models vs Implementation: Discrepancies Found

## Overview
This document lists all discrepancies found between the LaTeX documentation and the actual `.ipynb` implementations.

---

## 1. BAX_Fixed Model

### ❌ ISSUE: BAX Position Parameter
**LaTeX Says:**
```latex
pos_{BAX}(j) ∈ T  ∀j ∈ J_{BAX}  (Posición fija del ULD BAX j)
f_{j,pos_{BAX}(j)} = 1  ∀j ∈ J_{BAX}
```

**Implementation Says:**
```python
# Line 228-229 BAX_Fixed.ipynb
index_position_bax = [t.index for t in aircraft.loadlocations if t.location == j.actual_position_bax][0]
m.addConstr(f[j.index, index_position_bax]  == 1, name = f'C_BAX_fixed_{j.index}')
```

**Fix:** BAX positions come from `j.actual_position_bax` attribute of ULD objects, read from LoadLocationsSpotfire.csv data, not as a model parameter.

---

## 2. Model_Puttaert / BAX_Fixed: Big M Value

### ❌ ISSUE: Inconsistent Big M
**LaTeX Says:**
```latex
M = 100000000000  (Constante Big M)
```

**Implementation Says:**
```python
# Line 22: Initial declaration
M = 100000000000

# Line 242: Actual M used in constraints
M = max([i.weight for i in cargo.items])
```

**Fix:** Big M is actually set to `max(item weights)`, not 100000000000. The initial large value is overwritten.

---

## 3. Baseline Model: No Weight Variables in Stage 1

### ✅ CORRECT in LaTeX
The Baseline LaTeX correctly shows that Stage 1 (1D-BPP) only uses variables `u`, `p`, and auxiliary score/penalty variables. NO `f`, `w`, or `z` variables.

Stage 3 (W&B) only uses `f` variable.

This is correctly documented.

---

## 4. All Models: MAC Formula Division

### ⚠️ CLARIFICATION NEEDED
**LaTeX Shows:**
```latex
MAC = (C × (ZFW_index - K)) / ZFW + reference_arm - lemac
```

**Implementation Shows:**
```python
MAC_obj = (((aircraft.C * (ZFW_index_obj - aircraft.K)) / aircraft.ZFW) + aircraft.reference_arm - aircraft.lemac) / (aircraft.mac_formula / 100)
```

**Fix:** The MAC formula is divided by `(mac_formula / 100)` at the end. LaTeX is missing this final division.

**Correct Formula:**
```latex
MAC = ((C × (ZFW_index - K)) / ZFW + reference_arm - lemac) / (mac_formula / 100)
```

---

## 5. Optimized_Actual: Objective Indexing

### ✅ CORRECT
**LaTeX Says:** Priority 2 for MAC, Priority 1 for BAX
**Implementation Says:**
```python
m.setObjectiveN(MAC_obj, index = 0, priority = 2, weight = -1)
m.setObjectiveN(obj4, index = 5, priority = 1, weight = 1)
```

Index numbering (0 vs 5) doesn't affect priority. Priorities 2 and 1 are correct.

---

## 6. Baseline: Objective Indices in Stage 1

### ❌ ISSUE: Objective Index Numbering
**LaTeX Says:** Objectives 1, 2, 3, 4
**Implementation Says:**
```python
m.setObjectiveN(obj_volume_preference, index = 1, priority = 4, weight = 1)
m.setObjectiveN(obj2, index = 2, priority = 3, weight = 1)
m.setObjectiveN(obj_underutilization, index=3, priority=2, weight=1)
m.setObjectiveN(obj3, index = 4, priority = 1, weight = 1)
```

**Clarification:** Indices 1-4 are used (no index 0). Priorities 4-3-2-1 are correct (higher number = higher priority).

---

## 7. All Integrated Models: Linearization Constraints Order

### ⚠️ ISSUE: w_ijt Constraint Ordering in LaTeX
**LaTeX Shows 4 constraints, but labels them incorrectly**

**Implementation Shows (Puttaert/BAX_Fixed lines 244-274):**
```python
# C_lin_1: w_ijt ≤ M × p_ij
m.addConstr(w[i.index, j.index, t.index] <= M * p[i.index, j.index])

# C_lin_2: w_ijt ≤ M × f_jt  
m.addConstr(w[i.index, j.index, t.index] <= M * f[j.index, t.index])

# C_lin_3: z_ijt ≤ p_ij
m.addConstr(z[i.index, j.index, t.index] <= p[i.index, j.index])

# C_lin_4: z_ijt ≤ f_jt
m.addConstr(z[i.index, j.index, t.index] <= f[j.index, t.index])

# C_lin_5: z_ijt ≥ p_ij + f_jt - 1
m.addConstr(z[i.index, j.index, t.index] >= p[i.index, j.index] + f[j.index, t.index] - 1)

# C_lin_6: w_ijt ≥ w_i - M × (1 - z_ijt)
m.addConstr(w[i.index, j.index, t.index] >= i.weight - M * (1 - z[i.index, j.index, t.index]))

# C_lin_7: w_ijt ≤ w_i
m.addConstr(w[i.index, j.index, t.index] <= i.weight)
```

The LaTeX needs to include ALL 7 linearization constraints, not just 4.

---

## 8. DelgadoVenezian Model (Model.ipynb)

### ⚠️ MISSING: No LaTeX file exists for this model!
The best-performing model (89.8% success) has NO LaTeX documentation.

**Recommendation:** Create `model_delgado_venezian.tex` based on the actual implementation in `Model.ipynb`.

---

## 9. All Models: INDEX_PAX Calculation

### ✅ NOT AN ISSUE
LaTeX shows `INDEX_PAX` as a parameter, which is correct. It's calculated by `aircraft.define_INDEX_PAX()` method in Classes.ipynb and treated as a given value in the optimization.

---

## 10. Baseline WB Stage: Objective Index

### ❌ ISSUE: Missing Index 1-4
**Implementation (Baseline.ipynb lines 438, 445):**
```python
m.setObjectiveN(MAC_obj, index = 0, priority = 2, weight = -1)
m.setObjectiveN(obj4, index = 5, priority = 1, weight = 1)
```

The WB stage skips indices 1-4 (used in Stage 1). This is fine but could be confusing.

---

## Summary of Critical Issues

| Issue | Model(s) | Severity | Fix Required |
|-------|----------|----------|--------------|
| MAC formula missing final division | All | HIGH | Update all LaTeX |
| BAX position source incorrect | BAX_Fixed | MEDIUM | Update LaTeX documentation |
| Big M value incorrect | Puttaert, BAX_Fixed | MEDIUM | Update LaTeX to show dynamic M |
| Missing linearization constraints | Puttaert, BAX_Fixed | MEDIUM | Add constraints C_lin_6 and C_lin_7 |
| No LaTeX for DelgadoVenezian | Model.ipynb | HIGH | Create new LaTeX file |

---

## Recommendations

1. **HIGH PRIORITY:** Fix MAC formula in all LaTeX files
2. **HIGH PRIORITY:** Create LaTeX documentation for DelgadoVenezian model  
3. **MEDIUM PRIORITY:** Update BAX_Fixed LaTeX to correctly document BAX position fixing mechanism
4. **MEDIUM PRIORITY:** Complete linearization constraints in Puttaert and BAX_Fixed LaTeX
5. **LOW PRIORITY:** Add clarification notes about objective index numbering

---

## Files to Update

- [ ] `baseline.tex` - Fix MAC formula
- [ ] `optimized_actual.tex` - Fix MAC formula
- [ ] `bax_fixed.tex` - Fix MAC formula, BAX positions, Big M, linearization
- [ ] `model_puttaert.tex` - Fix MAC formula, Big M, linearization
- [ ] **NEW:** `model_delgado_venezian.tex` - Create from scratch

---

**Date:** October 27, 2025  
**Verified Against:** Model.ipynb, Baseline.ipynb, BAX_Fixed.ipynb, Model_Puttaert.ipynb, Optimized_Actual.ipynb  
**Verified By:** Code inspection and cross-reference

