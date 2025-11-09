# Constraint Verification Report
## Thesis Quality Control - LaTeX vs Implementation

**Date:** October 27, 2025  
**Purpose:** Verify all LaTeX constraints match actual .ipynb implementations  
**Status:** IN PROGRESS

---

## Model 1: BASELINE (Sequential) - Stage 1 (1D-BPP)

### Implementation File: `Baseline.ipynb` lines 134-170

| # | LaTeX Section | Implementation Line | Match? | Notes |
|---|---------------|---------------------|--------|-------|
| R1 | Apertura de ULDs | 137 | ✅ | Correct: `sum(u[j]) >= number_of_opened_uld` for j in J_reg |
| R2 | Uso de ULD | 140-142 | ✅ | Correct: `sum(p[i,j]) >= u[j]` for j in J_reg |
| R3 | Capacidad de Peso | 145-146 | ✅ | Correct: `sum(w_i * p[i,j]) <= W_j * u[j]` for ALL j |
| R4 | Capacidad Volumétrica | 149-150 | ✅ | Correct: `sum(v_i * p[i,j]) <= V_j * u[j] * loadfactor` for ALL j |
| R5 | Asignación Única | 153-154 | ✅ | Correct: `sum(p[i,j]) == 1` for all i, ALL j |
| R6 | Prohibición BAX/BUP/T | 157-160 | ✅ | Correct: `p[i,j] = 0` for all i, j in BAX∪BUP∪T |
| R7 | Manejo Especial COL/CRT | 163-169 | ✅ | Correct: `p[i1,j] + p[i2,j] <= 1` for COL+CRT pairs in J_reg |

**Stage 1 Status: ✅ ALL CORRECT**

---

## Model 1: BASELINE (Sequential) - Stage 3 (W&B)

### Implementation File: `Baseline.ipynb` lines 448-620

| # | LaTeX Section | Implementation Line | Match? | Notes |
|---|---------------|---------------------|--------|-------|
| W1 | Asignación de ULD | 450 | ✅ | Correct: `sum(f[j,t]) == 1` for all j |
| W2 | Posición Única | 454 | ✅ | Correct: `sum(f[j,t]) <= 1` for all t |
| W3 | Posiciones Prohibidas | 458 | ✅ | Correct: `sum(f[j,t_forbidden]) == 0` |
| W4 | Posiciones Superpuestas | 463-467 | ✅ | Correct: `f[j1,t1] + f[j2,t2] <= 1` for overlapping |
| W5 | Peso por Posición | 470-472 | ✅ | Correct: `sum(w_j * f[j,t]) <= W_max(t)` |
| W6a-d | Peso por Compartimento | 475-494 | ✅ | Correct: C1, C2, C3, C4 individual limits |
| W6e-f | Peso Compartimentos 1+2, 3+4 | 497-503 | ✅ | Correct: Combined C1+C2, C3+C4 limits |
| W7 | Peso Total (MPL) | 506-507 | ✅ | Correct: Total weight <= MPL |
| W8 | Balance Lateral TOW | 510-516 | ✅ | Correct: Two constraints for left-right balance |
| W9 | Balance Lateral LW | 519-524 | ✅ | Correct: Two constraints for landing weight balance |
| W10 | Envelope CG TOW | 527-539 | ✅ | Correct: Forward and aft TOW index limits |
| W11 | Envelope CG ZFW | 542-554 | ✅ | Correct: Forward and aft ZFW index limits |
| W12 | COL/CRT Compartimentos | 557-564 | ✅ | Correct: Aircraft-specific (772/77W vs 789/781) |

**Stage 3 Status: ✅ ALL CORRECT**

---

## Model 2: OPTIMIZED_ACTUAL (W&B-focused)

### Implementation File: `Optimized_Actual.ipynb` lines 63-196

**Checking against `optimized_actual.tex`...**

| # | LaTeX Section | Implementation Line | Match? | Notes |
|---|---------------|---------------------|--------|-------|
| O1 | Asignación de ULD | 66 | ✅ | `sum(f[j,t]) == 1` for all j |
| O2 | Posición Única | 70 | ✅ | `sum(f[j,t]) <= 1` for all t |
| O3 | Posiciones Prohibidas | 74 | ✅ | `sum(f[j,t_forbidden]) == 0` |
| O4 | Posiciones Superpuestas | 78-84 | ✅ | `f[j1,t1] + f[j2,t2] <= 1` |
| O5 | Peso por Posición | 88-89 | ✅ | `sum(w_j * f[j,t]) <= W_max(t)` |
| O6a-d | Peso por Compartimento | 93-107 | ✅ | Individual C1-C4 |
| O6e-f | Peso Compartimentos 1+2, 3+4 | 109-115 | ✅ | Combined limits |
| O7 | Peso Total | 118-119 | ✅ | Total <= MPL |
| O8 | Balance Lateral TOW | 122-130 | ✅ | Two-sided constraint |
| O9 | Balance Lateral LW | 133-141 | ✅ | Two-sided constraint |
| O10 | Envelope CG TOW | 144-154 | ✅ | Forward & aft |
| O11 | Envelope CG ZFW | 157-167 | ✅ | Forward & aft |
| O12 | COL/CRT Especial | 170-183 | ✅ | Aircraft-specific |

**Status: ✅ ALL CORRECT**

---

## Model 3: MODEL_PUTTAERT

### Implementation File: `Model_Puttaert.ipynb` lines 191-490

Checking comprehensive integrated model with w variables...

| # | LaTeX Section | Implementation Line | Match? | Notes |
|---|---------------|---------------------|--------|-------|
| P1 | Apertura de ULDs | 194 | ✅ | `sum(u[j]) >= number_of_opened_uld` for J_reg |
| P2 | Uso de ULD | 197-199 | ✅ | `sum(p[i,j]) >= u[j]` for J_reg |
| P3 | Capacidad de Peso | 202-203 | ✅ | `sum(w_i * p[i,j]) <= W_j * u[j]` |
| P4 | Capacidad Volumétrica | 206-207 | ✅ | `sum(v_i * p[i,j]) <= V_j * u[j] * loadfactor` |
| P5 | Asignación Única | 210-211 | ✅ | `sum(p[i,j]) == 1` for all i |
| P6 | Combinatorial ULD-Position | 225 | ✅ | `sum(f[j,t]) == u[j]` for all j |
| P7 | Posición Única | 228-229 | ✅ | `sum(f[j,t]) <= 1` for all t |
| P8 | BAX/BUP/T Asignación | 232-234 | ✅ | `sum(f[j,t]) == 1` for special ULDs |
| P9 | Prohibición en BAX/BUP/T | 237-240 | ✅ | `p[i,j] = 0` for special ULDs |
| L1 | Linearización w <= M*p | 244-247 | ✅ | `w[i,j,t] <= M * p[i,j]` |
| L2 | Linearización w <= M*f | 250-253 | ✅ | `w[i,j,t] <= M * f[j,t]` |
| L3 | Linearización z <= p | 256-260 (line 259) | ✅ | `z[i,j,t] <= p[i,j]` |
| L4 | Linearización z <= f | 256-260 (line 260) | ✅ | `z[i,j,t] <= f[j,t]` |
| L5 | Linearización z >= p+f-1 | 256-261 (line 261) | ✅ | `z[i,j,t] >= p[i,j] + f[j,t] - 1` |
| L6 | Linearización w >= w_i - M*(1-z) | 264-267 | ⚠️ MISSING IN LATEX | **NEED TO ADD** |
| L7 | Linearización w <= w_i | 271-274 | ⚠️ MISSING IN LATEX | **NEED TO ADD** |
| P10 | Posiciones Prohibidas | 277-278 | ✅ | `sum(f[j,t_forbidden]) == 0` |
| P11 | Posiciones Superpuestas | 281-286 | ✅ | `f[j1,t1] + f[j2,t2] <= 1` |
| P12 | Peso por Posición | 289-290 | ✅ | Weight limits per position |
| P13-18 | Peso por Compartimento | 294-307 | ✅ | All 6 constraints |
| P19 | Peso Total | 310-311 | ✅ | Total weight <= MPL |
| P20-21 | Balance Lateral TOW | 314-325 | ✅ | Two-sided |
| P22-23 | Balance Lateral LW | 328-339 | ✅ | Two-sided |
| P24-25 | Envelope CG TOW | 343-356 | ✅ | Forward & aft |
| P26-27 | Envelope CG ZFW | 360-373 | ✅ | Forward & aft |
| P28 | COL/CRT en ULD | 377-382 | ✅ | Item-level constraint |
| P29-30 | COL/CRT Compartimentos | 385-404 | ✅ | Aircraft-specific |

**Status: ⚠️ MISSING 2 LINEARIZATION CONSTRAINTS (L6, L7)**

---

## Model 4: BAX_FIXED

### Implementation File: `BAX_Fixed.ipynb` lines 191-282

**Same as Puttaert PLUS BAX position fixing (lines 226-229)**

All constraints same as Puttaert, PLUS:

| # | LaTeX Section | Implementation Line | Match? | Notes |
|---|---------------|---------------------|--------|-------|
| BF1 | BAX Position Fixed | 227-229 | ✅ UPDATED | `f[j, actual_position] == 1` for BAX |

**Status: ⚠️ MISSING 2 LINEARIZATION CONSTRAINTS (L6, L7) - same as Puttaert**

---

## SUMMARY

| Model | Total Constraints | Verified | Issues | Status |
|-------|------------------|----------|--------|--------|
| **Baseline Stage 1** | 7 | 7 | 0 | ✅ COMPLETE |
| **Baseline Stage 3** | 12 | 12 | 0 | ✅ COMPLETE |
| **Optimized_Actual** | 12 | 12 | 0 | ✅ COMPLETE |
| **Puttaert** | 30 | 28 | 2 missing | ⚠️ NEEDS FIX |
| **BAX_Fixed** | 31 | 29 | 2 missing | ⚠️ NEEDS FIX |

---

## FIXES REQUIRED

### Puttaert & BAX_Fixed LaTeX Files

Need to add these two linearization constraints:

**L6: Ensuring w_ijt equals w_i when z_ijt = 1**
```latex
w_{ijt} \geq w_i - M \cdot (1 - z_{ijt}) \quad \forall i \in I, \forall j \in J, \forall t \in T
```

**L7: Upper bound on w_ijt**
```latex
w_{ijt} \leq w_i \quad \forall i \in I, \forall j \in J, \forall t \in T
```

These exist in implementation but are missing from LaTeX documentation.

---

**Verified By:** Line-by-line code inspection  
**Next Step:** Update LaTeX files with missing constraints + Add comments to code

