# COMENTARIOS DE BUGS PARA BASELINE.IPYNB

**Formato:** Español, sin emojis  
**Total de bugs:** 4 (Bug #1, #2, #5, #10, #11)

---

## BUG 1: Peso de Compartimento Por Posicion (CRITICO)

**Ubicacion:** Celda `solve_WB`, antes de linea `# W6a: Peso Compartimento C1`

**Comentario a agregar ANTES de W6a:**

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
# W6a: Peso Compartimento C1 - Total weight in compartment 1 limit
for t in aircraft.loadlocations_C1:  # BUG 1: Loop por posicion, no por compartimento
    m.addConstr(quicksum(j.weight * f[j.index, t.index] for j in cargo.uld)
                <= aircraft.max_weight_C1, name = f'C_Added_1_{t.index}')

# W6b: Peso Compartimento C2 - Total weight in compartment 2 limit
for t in aircraft.loadlocations_C2:  # BUG 1: Loop por posicion, no por compartimento
    m.addConstr(quicksum(j.weight * f[j.index, t.index] for j in cargo.uld)
                <= aircraft.max_weight_C2, name = f'C_Added_2_{t.index}')

# W6c: Peso Compartimento C3 - Total weight in compartment 3 limit
for t in aircraft.loadlocations_C3:  # BUG 1: Loop por posicion, no por compartimento
    m.addConstr(quicksum(j.weight * f[j.index, t.index] for j in cargo.uld)
                <= aircraft.max_weight_C3, name = f'C_Added_3_{t.index}')

# W6d: Peso Compartimento C4 - Total weight in compartment 4 limit
for t in aircraft.loadlocations_C4:  # BUG 1: Loop por posicion, no por compartimento
    m.addConstr(quicksum(j.weight * f[j.index, t.index] for j in cargo.uld)
                <= aircraft.max_weight_C4, name = f'C_Added_4_{t.index}')
```

---

## BUG 2: Asignacion Incluye BAX/BUP/T (CRITICO)

**Ubicacion:** Celda `solve_1D_BPP_WB`, antes de linea `# R5: Asignación Única`

**Comentario a agregar ANTES de R5:**

```python
# BUG 2: Asignacion incluye BAX/BUP/T - La suma incluye TODOS los ULDs (incluyendo BAX/BUP/T).
# Los ULDs BAX/BUP/T son contenedores pre-construidos que NO pueden recibir items de optimizacion.
# Esto puede crear soluciones infactibles o forzar items en contenedores BAX.
# CORRECCION: Agregar filtro "if j.isNeitherBAXnorBUPnorT" en el quicksum
# Ver Model.ipynb linea 211: quicksum(p[i.index, j.index] for j in cargo.uld if j.isNeitherBAXnorBUPnorT) == 1
```

**Comentario inline a agregar:**

```python
# R5: Asignación Única - Every item must be placed in exactly one ULD
for i in cargo.items:
    m.addConstr(quicksum(p[i.index, j.index] for j in cargo.uld) == 1, name = f'C3_{i.index}')  # BUG 2: Falta filtro isNeitherBAXnorBUPnorT
```

---

## BUG 5: Sistema de Penalizacion Suboptimal (HIGH)

**Ubicacion:** Celda `solve_1D_BPP_WB`, antes de linea `'''Objective function 4'''`

**Comentario a agregar ANTES del objetivo 4:**

```python
'''Objective function 4 --> Minimize the separation of items with the same serialnumber prefix over different ULDs [Medium Priority]'''

# BUG 5: Sistema de penalizacion suboptimal - Solo cuenta si un ULD es usado o no (binario 0 o 1).
# No cuenta el NUMERO de ULDs usados por booking. 
# Ejemplo: booking con 10 piezas split en 5 ULDs tiene penalty=5, igual que split en 2 ULDs (penalty=2).
# Sistema correcto: usar variables Y[b_i] (integer) y Z[b_i,j] (binary) para contar ULDs por booking.
# CORRECCION: Ver sistema Y-Z en Model.ipynb lineas 584-617 (DV20-DV21)

prefix_groups = cargo.get_prefix_groups()

separation_penalty = {}  # BUG 5: Deberia ser Y (integer) para contar ULDs, no binary penalty
for prefix, items in prefix_groups.items():
    for j in cargo.uld:
        separation_penalty[prefix, j.index] = m.addVar(vtype=GRB.BINARY, name=f'sep_penalty_{prefix}_{j.index}')

for prefix, items in prefix_groups.items():
    for j in cargo.uld:
        m.addConstr(quicksum(p[i.index, j.index] for i in items) <= len(items) * separation_penalty[prefix, j.index], name=f'C_separation_{prefix}_{j.index}')

        
obj3 = quicksum(separation_penalty.values())  # BUG 5: Deberia minimizar sum(Y[b_i])
m.setObjectiveN(obj3, index = 4, priority = 1, weight = 1)
```

---

## BUG 10: COL/CRT Por Posicion (CRITICO)

**Ubicacion:** Celda `solve_WB`, antes de las restricciones COL/CRT

**Comentario a agregar ANTES de W12:**

```python
# BUG 10: Logica COL/CRT por posicion (no por compartimento) - Restriccion es PER-POSITION, no per-compartment.
# COL y CRT son carga con control de temperatura que no pueden compartir MISMO COMPARTIMENTO (no posicion).
# Ejemplo: En C1_C2 (frente) con 10 posiciones: COL en posicion 1, CRT en posicion 2 -> AMBOS en C1_C2! (malo)
# CORRECCION: Usar variables binarias COL_k, CRT_k por COMPARTIMENTO con Big-M y mutual exclusion.
# Ver Model.ipynb lineas 463-512 (DV24): COL_k[C1_C2], CRT_k[C1_C2] con restriccion COL_k + CRT_k <= 1

# W12: COL/CRT Especial - COL and CRT cargo cannot be in same compartment (aircraft-specific)
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

**Ubicacion:** Multiples celdas (solve_1D_BPP_WB y solve_WB)

**Comentario a agregar en solve_1D_BPP_WB (antes de todos los setObjectiveN):**

```python
# BUG 11: Indices de multi-objetivo no secuenciales - Gurobi espera indices secuenciales (0,1,2,3,4,5...).
# Este modelo usa: 1, 2, 3, 4 (en 1D-BPP) y luego 0, 5 (en W&B).
# Total: 1, 2, 3, 4, 0, 5 (no secuencial, omite indices y usa 0 fuera de orden)
# CORRECCION: Usar indices secuenciales 0, 1, 2, 3, 4, 5
# Ver Model.ipynb: usa indices 0, 1, 2, 3, 4, 5 en orden correcto
```

**Comentarios inline a agregar:**

```python
# En solve_1D_BPP_WB:
m.setObjectiveN(obj_volume_preference, index = 1, priority = 4, weight = 1)  # BUG 11: Deberia ser index=0
m.setObjectiveN(obj2, index = 2, priority = 3, weight = 1)  # BUG 11: Deberia ser index=1
m.setObjectiveN(obj_underutilization, index=3, priority=2, weight=1)  # BUG 11: Deberia ser index=2
m.setObjectiveN(obj3, index = 4, priority = 1, weight = 1)  # BUG 11: Deberia ser index=3

# En solve_WB:
m.setObjectiveN(MAC_obj, index = 0, priority = 2, weight = -1)  # BUG 11: Esta OK, pero deberia ser index=4 secuencialmente
m.setObjectiveN(obj4, index = 5, priority = 1, weight = 1)  # BUG 11: Deberia ser index=5 si MAC es index=4, o saltar a 5 no es secuencial
```

---

## RESUMEN

Total de bugs en Baseline: **4 bugs**

- **Bug #1:** CRITICO - Compartment weights per-position (W6a-W6d)
- **Bug #2:** CRITICO - Item assignment includes BAX/BUP/T (R5)
- **Bug #5:** HIGH - Separation penalty suboptimal (Objective 4)
- **Bug #10:** CRITICO - COL/CRT per-position logic (W12)
- **Bug #11:** HIGH - Multi-objective indices no secuenciales (todos los setObjectiveN)

**Bugs NO presentes en Baseline:**
- Bug #3 (COL/CRT complex nested) - Baseline usa logica mas simple
- Bug #4 (variable w) - Baseline no usa variable w
- Bug #7 (hardcoded Big-M) - Baseline no usa Big-M
- Bug #8 (position weight split) - Baseline no divide restriccion
- Bug #9 (multi-obj count) - No aplica en este contexto

