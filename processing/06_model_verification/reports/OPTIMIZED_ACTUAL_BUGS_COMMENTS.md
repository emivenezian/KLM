# COMENTARIOS DE BUGS PARA OPTIMIZED_ACTUAL.IPYNB

**Formato:** Español, sin emojis  
**Total de bugs:** 3 (Bug #1, #10, #11)  
**Nota:** Optimized_Actual es W&B only (no tiene 1D-BPP), por lo que solo tiene bugs relacionados con W&B

---

## BUG 1: Peso de Compartimento Por Posicion (CRITICO)

**Ubicacion:** Celda principal del modelo, antes de las restricciones de compartimento

**Comentario a agregar ANTES de O7a:**

```python
# BUG 1: Peso de compartimento por posicion (deberia ser por compartimento) - Crea N restricciones (una por posicion).
# Cada restriccion aplica el MISMO limite de compartimento a cada posicion individualmente.
# Ejemplo: Si C1 tiene 5 posiciones con limite 10,000 kg:
#   - BUGGY: Cada una de 5 posiciones <= 10,000 kg -> Total puede ser 50,000 kg!
#   - CORRECTO: Suma de todas las 5 posiciones <= 10,000 kg
# CORRECCION: UNA restriccion por compartimento con sum sobre TODAS las posiciones (for t in loadlocations DENTRO del quicksum)
# Ver Model.ipynb lineas 260-277 (DV12): quicksum(...for t in loadlocations) <= max_weight
```

**Comentarios inline a agregar:**

```python
# O7a: Peso Compartimento C1 - Total weight in compartment 1 limit
for t in aircraft.loadlocations_C1:  # BUG 1: Loop por posicion, no por compartimento
    m.addConstr(quicksum(j.weight * f[j.index, t.index] for j in cargo.uld)
                <= aircraft.max_weight_C1, name = f'C_Added_1_{t.index}')

# O7b: Peso Compartimento C2 - Total weight in compartment 2 limit
for t in aircraft.loadlocations_C2:  # BUG 1: Loop por posicion, no por compartimento
    m.addConstr(quicksum(j.weight * f[j.index, t.index] for j in cargo.uld)
                <= aircraft.max_weight_C2, name = f'C_Added_2_{t.index}')

# O7c: Peso Compartimento C3 - Total weight in compartment 3 limit
for t in aircraft.loadlocations_C3:  # BUG 1: Loop por posicion, no por compartimento
    m.addConstr(quicksum(j.weight * f[j.index, t.index] for j in cargo.uld)
                <= aircraft.max_weight_C3, name = f'C_Added_3_{t.index}')

# O7d: Peso Compartimento C4 - Total weight in compartment 4 limit
for t in aircraft.loadlocations_C4:  # BUG 1: Loop por posicion, no por compartimento
    m.addConstr(quicksum(j.weight * f[j.index, t.index] for j in cargo.uld)
                <= aircraft.max_weight_C4, name = f'C_Added_4_{t.index}')
```

---

## BUG 10: COL/CRT Por Posicion (CRITICO)

**Ubicacion:** Cerca del final del modelo, restricciones COL/CRT

**Comentario a agregar ANTES de las restricciones COL/CRT:**

```python
# BUG 10: Logica COL/CRT por posicion (no por compartimento) - Restriccion es PER-POSITION, no per-compartment.
# COL y CRT son carga con control de temperatura que no pueden compartir MISMO COMPARTIMENTO (no posicion).
# Ejemplo: En C1_C2 (frente) con 10 posiciones: COL en posicion 1, CRT en posicion 2 -> AMBOS en C1_C2! (malo)
# CORRECCION: Usar variables binarias COL_k, CRT_k por COMPARTIMENTO con Big-M y mutual exclusion.
# Ver Model.ipynb lineas 463-512 (DV24): COL_k[C1_C2], CRT_k[C1_C2] con restriccion COL_k + CRT_k <= 1

# O12: COL/CRT Especial - COL and CRT cargo cannot be in same compartment (aircraft-specific)
uld_with_COL = [j.index for j in cargo.uld if j in results_3D_BPP and any(i.COL == 1 for i in results_3D_BPP[j])] + [j.index for j in cargo.uld if j.COL == 1]
uld_with_CRT = [j.index for j in cargo.uld if j in results_3D_BPP and any(i.CRT == 1 for i in results_3D_BPP[j])] + [j.index for j in cargo.uld if j.CRT == 1]

if str(aircraft.aircraft_type) in ['772', '77W']:
    for t in aircraft.loadlocations_C1_C2:
        m.addConstr(quicksum(f[j, t.index] for j in uld_with_COL) + quicksum(f[k, t.index] for k in uld_with_CRT) <= 1, name=f'C_special_COL_CRT_C1_C2_{t.index}')  # BUG 10: Por posicion, no compartimento
    for t in aircraft.loadlocations_C3_C4:
        m.addConstr(quicksum(f[j, t.index] for j in uld_with_COL) + quicksum(f[k, t.index] for k in uld_with_CRT) <= 1, name=f'C_special_COL_CRT_C3_C4_{t.index}')  # BUG 10: Por posicion, no compartimento
```

---

## BUG 11: Indices de Multi-Objetivo No Secuenciales (HIGH)

**Ubicacion:** Donde se definen los objetivos del modelo

**Comentario a agregar ANTES de los setObjectiveN:**

```python
# BUG 11: Indices de multi-objetivo no secuenciales - Gurobi espera indices secuenciales (0,1,2,3...).
# Este modelo usa: 0, 5 (solo 2 objetivos, pero omite indices 1-4)
# Aunque el modelo funcione con solo 2 objetivos, usar indices no consecutivos no es best practice.
# CORRECCION: Usar indices secuenciales 0, 1 para los 2 objetivos
# Ver Model.ipynb: usa indices 0, 1, 2, 3, 4, 5 secuencialmente
```

**Comentarios inline a agregar:**

```python
# Objetivo 1: Maximizar %MAC
m.setObjectiveN(MAC_obj, index = 0, priority = 2, weight = -1)  # BUG 11: Index OK, priority correcta

# Objetivo 2: Minimizar proximity score BAX
m.setObjectiveN(obj_bax_proximity, index = 5, priority = 1, weight = 1)  # BUG 11: Deberia ser index=1 (no index=5)
```

---

## RESUMEN

Total de bugs en Optimized_Actual: **3 bugs**

- **Bug #1:** CRITICO - Compartment weights per-position (O7a-O7d)
- **Bug #10:** CRITICO - COL/CRT per-position logic (O12)
- **Bug #11:** HIGH - Multi-objective indices no secuenciales (setObjectiveN con index=0 y index=5)

**Bugs NO presentes en Optimized_Actual:**
- Bug #2 (item assignment BAX) - N/A: Es W&B only, no hace 1D-BPP
- Bug #3 (COL/CRT complex nested) - Usa logica simple per-position (tiene Bug #10 en su lugar)
- Bug #4 (variable w) - N/A: Es W&B only, no usa variable w
- Bug #5 (separation penalty) - N/A: Es W&B only, no optimiza separation
- Bug #7 (hardcoded Big-M) - No usa Big-M
- Bug #8 (position weight split) - No divide restriccion
- Bug #9 (multi-obj count) - No aplica en este contexto

**Notas adicionales:**
- Optimized_Actual es el modelo MAS SIMPLE de los benchmarks
- Solo hace Weight & Balance (W&B), no hace 1D Bin Packing
- Recibe ULDs pre-cargados de 3D-BPP y solo optimiza posiciones
- Por eso tiene menos bugs que los modelos completos (Puttaert, BAX_Fixed, Baseline)

