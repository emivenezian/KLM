# Email para Profesor Delgado - Análisis de Modelos Benchmark

---

**Asunto:** Avance Tesis: Análisis Profundo de Modelos Benchmark y Errores Detectados

Estimado Profesor Delgado,

Espero que se encuentre bien. Le escribo para actualizar el progreso de mi tesis y consultar cómo proceder con los hallazgos que he descubierto. Como me indicó en nuestra última reunión, me he sumergido profundamente en cada modelo benchmark para entender qué hace cada uno y verificar su correctitud matemática. Este email reemplaza nuestra reunión presencial, así que intentaré ser lo más detallada y pedagógica posible.

---

## 1️⃣ CONTEXTO: LOS 5 MODELOS BENCHMARK

Para poder comparar mi modelo (DelgadoVenezian) de forma justa con los benchmarks existentes, primero necesitaba entender exactamente qué hace cada uno y asegurarme de que estén correctamente implementados. Los modelos son:

### **A. Actual (KLM Real)**
- **Qué es:** Los datos reales de cómo KLM cargó el avión en cada vuelo
- **Fuente:** Viene directamente de `LoadLocationsSpotfire.csv` (campo `MacZFW`)
- **No es un modelo:** Son resultados históricos, no hay código que optimice
- **Propósito:** Benchmark de referencia - "así lo hace KLM actualmente"

### **B. Baseline (Sequential)**
- **Qué hace:** Enfoque secuencial en 3 etapas separadas
  - **Etapa 1:** 1D-BPP (asignar ítems a ULDs sin considerar posición)
  - **Etapa 2:** 3D-BPP (empaquetar físicamente en cada ULD)
  - **Etapa 3:** W&B (asignar ULDs a posiciones para optimizar %MAC)
- **Lógica:** Primero empaca, luego optimiza balance
- **Ventaja:** Simple, modular
- **Desventaja:** No considera W&B durante el empaquetado (subóptimo)

### **C. Optimized_Actual (W&B-focused)**
- **Qué hace:** Solo optimiza Weight & Balance (sin re-empaquetar)
- **Asume:** Los ULDs ya vienen armados con los ítems que tenían en la realidad
- **Optimiza:** Solo la asignación de ULDs a posiciones para maximizar %MAC
- **Ventaja:** Simple, rápido
- **Desventaja:** No puede reorganizar ítems entre ULDs

### **D. Model_Puttaert**
- **Qué hace:** MILP integrado que combina 1D-BPP + W&B simultáneamente
- **Idea:** Considerar el impacto en %MAC mientras se empaqueta
- **Base:** Modelo de tesis de Puttaert (2024)
- **Problema:** Tiene varios errores de implementación (detallados abajo)

### **E. BAX_Fixed**
- **Qué hace:** Igual que Puttaert PERO fija las posiciones de los BAX containers
- **Restricción adicional (BF1):** `f[j_BAX, t_actual] = 1` 
- **Propósito:** Ver impacto de fijar posiciones BAX vs permitir que el modelo las optimice
- **Código:** Esencialmente Puttaert + 1 constraint extra

### **F. DelgadoVenezian (Nuestro Modelo)**
- **Qué hace:** Versión corregida y mejorada de Puttaert
- **Mejoras clave:**
  1. Corrección de errores matemáticos de Puttaert
  2. Cálculo %MAC específico por tipo de avión
  3. Manejo mejorado de carga COL/CRT (temperatura sensible)
  4. Penalización mejorada de separación de bookings (variables Y y Z)
  5. Manejo explícito de posiciones superpuestas
  6. Feedback loop para items diferidos

---

## 2️⃣ METODOLOGÍA: CÓMO ANALICÉ LOS MODELOS

Para asegurar comparabilidad, seguí este proceso sistemático:

**Paso 1:** Documenté completamente mi modelo (Model.ipynb) como referencia "correcta"

**Paso 2:** Comparé constraint por constraint Model.ipynb vs Model_Puttaert.ipynb para identificar qué errores específicos yo había corregido

**Paso 3:** Busqué esos mismos errores en Baseline, Optimized_Actual, y BAX_Fixed

**Paso 4:** Además, busqué activamente otros errores no presentes en la lista inicial

---

## 3️⃣ ERRORES ENCONTRADOS: 11 BUGS TOTALES

He encontrado **11 errores distintos** distribuidos en los benchmarks. Los clasifico por severidad:

### **🔥 CRÍTICOS (Afectan Correctitud Matemática)**

#### **Bug #1: Restricciones de Peso por Compartimento** 
**Presente en:** Puttaert, Baseline, Optimized_Actual, BAX_Fixed (TODOS)

**El Error:**
```python
# ❌ INCORRECTO: Una restricción POR POSICIÓN
for t in aircraft.loadlocations_C1:
    m.addConstr(peso_en_t <= aircraft.max_weight_C1)
```

Si C1 tiene 3 posiciones (11L, 12L, 13L) con límite de 5000 kg:
- Crea 3 restricciones: peso_11L ≤ 5000, peso_12L ≤ 5000, peso_13L ≤ 5000
- **Permite hasta 15,000 kg total en C1** (3 × 5000) - ¡INCORRECTO!

**Debería ser:**
```python
# ✅ CORRECTO: Una restricción para TODO el compartimento
m.addConstr(
    quicksum(peso for t in aircraft.loadlocations_C1) <= aircraft.max_weight_C1
)
```

**Impacto:** El modelo permite sobrecargar compartimentos. Esto cambia fundamentalmente la región factible y podría generar soluciones inviables en la práctica.

**Aplica a:** C1, C2, C3, C4, C1+C2, C3+C4 (6 grupos de restricciones por modelo)

---

#### **Bug #2: Restricción de Asignación de Ítems**
**Presente en:** Puttaert, Baseline, BAX_Fixed

**El Error:**
```python
# ❌ INCORRECTO: Permite asignar ítems a CUALQUIER ULD (incluso BAX/BUP/T)
for i in cargo.items:
    m.addConstr(quicksum(p[i.index, j.index] for j in cargo.uld) == 1)
```

**Debería ser:**
```python
# ✅ CORRECTO: Solo ULDs regulares pueden llevar ítems de carga
for i in cargo.items:
    m.addConstr(quicksum(p[i.index, j.index] 
                        for j in cargo.uld if j.isNeitherBAXnorBUPnorT) == 1)
```

**Impacto:** La restricción fundamental está mal formulada. Aunque otra restricción (p[i,j]=0 para BAX) lo previene, es inconsistente tener que depender de eso. La formulación base debe ser correcta.

---

#### **Bug #10: Lógica COL/CRT por Posición en vez de por Compartimento**
**Presente en:** Puttaert, Baseline, Optimized_Actual, BAX_Fixed (TODOS)

**El Error:**
```python
# ❌ INCORRECTO: Restricción por posición individual
if aircraft_type in ['772', '77W']:
    for t in aircraft.loadlocations_C1_C2:
        m.addConstr(f[COL_ULD, t] + f[CRT_ULD, t] <= 1)
```

**Problema:** Esto dice "no puedes poner COL y CRT en la **misma posición**", pero:
- **Permite** COL en posición 11L y CRT en posición 12L (ambas en compartimento frontal)
- **Pero la regla real** es: COL y CRT no pueden estar en el **mismo compartimento**

**Debería ser:**
```python
# ✅ CORRECTO: Nivel compartimento con big-M
COL_front = m.addVar(vtype=GRB.BINARY)  # 1 si hay COL en C1+C2
CRT_front = m.addVar(vtype=GRB.BINARY)  # 1 si hay CRT en C1+C2

m.addConstr(sum(f[COL_ULDs] en front) <= big_M * COL_front)
m.addConstr(sum(f[CRT_ULDs] en front) <= big_M * CRT_front)
m.addConstr(COL_front + CRT_front <= 1)  # Exclusión mutua
```

**Impacto:** Error lógico crítico - permite violar reglas de temperatura de carga farmacéutica.

---

#### **Bug #3: Lógica CRT/COL Excesivamente Compleja**
**Presente en:** Puttaert, BAX_Fixed

**El Error:**
- Crea variables auxiliares para cada combinación (i_COL, i_CRT, j, t)
- Complejidad: O(n_COL × n_CRT × n_ULD × n_positions)
- Lógica confusa con `quicksum(COL_C1_C2 + CRT_C1_C2 for t in ...) == 0`

**Debería ser:** La formulación limpia con big-M del Bug #10 (nivel compartimento)

**Impacto:** Ineficiencia extrema + lógica poco clara

---

### **⚠️ ALTA PRIORIDAD (Afectan Eficiencia/Calidad)**

#### **Bug #4: Variable w de Linearización Innecesaria**
**Presente en:** Puttaert, BAX_Fixed

Crea variable continua `w[i,j,t]` con 7 restricciones de linearización cuando se puede usar directamente `i.weight * z[i,j,t]` con solo 3 restricciones.

**Impacto:** O(n_items × n_ULD × n_positions) variables extras + 7× restricciones extras → tiempos de solución más lentos

---

#### **Bug #5: Penalización de Separación Subóptima**
**Presente en:** Puttaert, Baseline, BAX_Fixed

Usa variable binaria "¿está separado?" en vez de contar cuántos ULDs usa cada booking.

**Impacto:** Menos efectivo para mantener bookings juntos

---

#### **Bug #7: Big-M Hardcoded**
**Presente en:** Puttaert solamente (BAX_Fixed ya lo corrigió)

`M = 100000000000` en vez de `M = max(item_weights)`

**Impacto:** Problemas numéricos potenciales en el solver

---

#### **Bug #8: Restricción de Peso por Posición Dividida**
**Presente en:** Puttaert, BAX_Fixed

Crea 2 restricciones separadas (una para ítems, una para ULDs) en vez de combinarlas.

**Impacto:** 2× restricciones innecesarias

---

#### **Bug #11: Índices de Multi-Objetivo Incorrectos**
**Presente en:** Baseline, Optimized_Actual

**El Error:**
```python
# Solo 2 objetivos pero usa índice 5
m.setObjectiveN(MAC_obj, index=0, ...)
m.setObjectiveN(obj4, index=5, ...)  # ❌ Debería ser index=1

bax_env = m.getMultiobjEnv(5)  # ❌ ERROR - solo existen índices 0-1
```

**Impacto:** Posible error en runtime o comportamiento indefinido

---

### **📊 PRIORIDAD MEDIA (Diferencias de Diseño)**

#### **Bug #6: Jerarquía de Objetivos Diferente**
Cada modelo tiene estructura de objetivos distinta (diseño intencional, no error per se)

#### **Bug #9: Conteo de Objetivos No Coincide**
Relacionado con Bug #6 - diferentes números de objetivos

---

## 4️⃣ MATRIZ COMPLETA DE ERRORES

| Bug | Descripción | Puttaert | Baseline | Opt_Actual | BAX_Fixed | Prioridad |
|-----|-------------|----------|----------|------------|-----------|-----------|
| #1 | Peso compartimento | ❌ | ❌ | ❌ | ❌ | 🔥 CRÍTICO |
| #2 | Asignación items | ❌ | ❌ | N/A | ❌ | 🔥 CRÍTICO |
| #3 | COL/CRT complejo | ❌ | ✅ | ✅ | ❌ | 🔥 CRÍTICO |
| #10 | COL/CRT por posición | ❌ | ❌ | ❌ | ❌ | 🔥 CRÍTICO |
| #4 | Variable w innecesaria | ❌ | ✅ | ✅ | ❌ | ⚠️ ALTA |
| #5 | Separación subóptima | ❌ | ❌ | N/A | ❌ | ⚠️ ALTA |
| #7 | Big-M hardcoded | ❌ | N/A | N/A | ✅ | ⚠️ ALTA |
| #8 | Peso posición split | ❌ | ✅ | ✅ | ❌ | 📊 MEDIA |
| #11 | Índice multi-obj | ✅ | ❌ | ❌ | ✅ | ⚠️ ALTA |
| #6 | Jerarquía objetivos | ❌ | ❌ | ✅ | ❌ | 📊 DISEÑO |
| #9 | Conteo objetivos | ⚠️ | ✅ | ✅ | ✅ | 📊 DISEÑO |

**Totales por modelo:**
- **Puttaert:** 8 bugs (4 críticos, 4 alta prioridad)
- **Baseline:** 4 bugs (3 críticos, 1 alta)
- **Optimized_Actual:** 3 bugs (2 críticos, 1 alta) ← El más limpio
- **BAX_Fixed:** 7 bugs (4 críticos, 3 alta) ← Hereda de Puttaert
- **DelgadoVenezian (mi modelo):** 0 bugs ✅

---

## 5️⃣ EJEMPLO DETALLADO: BUG #1 (El Más Crítico)

Permítame explicar en detalle el error más grave que encontré, porque ilustra bien la importancia de revisar cada constraint:

### **Contexto:**
Cada avión tiene 4 compartimentos de carga (C1, C2, C3, C4), cada uno con un límite de peso. Por ejemplo:
- C1: máximo 5000 kg
- C2: máximo 4500 kg
- Etc.

### **Lo que Puttaert (y los demás) hacen:**
```python
# Para compartimento C1 que tiene 3 posiciones (11L, 12L, 13L)
for t in aircraft.loadlocations_C1:  # ← Loop sobre cada posición
    m.addConstr(
        quicksum(peso en posición t) <= aircraft.max_weight_C1
    )
```

**Esto crea:**
- Restricción 1: peso_en_11L ≤ 5000 kg
- Restricción 2: peso_en_12L ≤ 5000 kg  
- Restricción 3: peso_en_13L ≤ 5000 kg

**Problema:** ¡Permite hasta 15,000 kg total en C1! Cada posición individual puede tener hasta 5000 kg, cuando 5000 kg es el límite del **compartimento completo**.

### **Lo que debería hacer (y que nuestro modelo hace bien):**
```python
# UNA sola restricción para TODO el compartimento
m.addConstr(
    quicksum(peso en posición t for t in aircraft.loadlocations_C1) <= aircraft.max_weight_C1
)
```

**Esto crea:**
- Restricción única: peso_total_C1 ≤ 5000 kg ✅

### **Por qué importa:**
- **Seguridad:** Podría generar configuraciones que violan límites estructurales del avión
- **Comparabilidad:** Los modelos con este bug tienen una región factible artificialmente más grande
- **Validez:** Las soluciones podrían no ser implementables en la realidad

---

## 6️⃣ VERIFICACIÓN: BAX_FIXED = PUTTAERT + BF1

Confirmé que BAX_Fixed es esencialmente una copia de Puttaert con una restricción adicional:

**Código único en BAX_Fixed:**
```python
# BF1: Fijar posiciones BAX a las reales
for j in cargo.uld:
    if j.isBAX:
        index_position_bax = [t.index for t in aircraft.loadlocations 
                             if t.location == j.actual_position_bax][0]
        m.addConstr(f[j.index, index_position_bax] == 1)
```

**Errores heredados:** BAX_Fixed tiene los mismos 8 bugs que Puttaert (excepto Bug #7 que ya corrigió: usa Big-M dinámico).

---

## 7️⃣ ¿POR QUÉ ESTOS ERRORES NO SE NOTARON ANTES?

**Teoría 1:** Los modelos aún producen soluciones factibles
- Aunque las restricciones están mal formuladas, otras restricciones (como límites por posición) pueden parcialmente compensar
- Las soluciones son "viables" pero la región factible es incorrecta

**Teoría 2:** Impacto visible solo en casos específicos
- Con cargas ligeras, nunca se alcanzan los límites
- Los bugs solo causan problemas con vuelos muy llenos

**Teoría 3:** Comparación relativa aún válida
- Si todos tienen el mismo bug, la comparación relativa podría mantenerse
- Pero esto no justifica dejar errores matemáticos

---

## 8️⃣ DOCUMENTACIÓN CREADA

He generado documentación exhaustiva:

1. **CORRECT_MODEL_REFERENCE.md** - Documentación completa de mi modelo (referencia correcta)
2. **KEY_CORRECT_IMPLEMENTATIONS.md** - Foco en las 3 implementaciones clave correctas
3. **COMPLETE_BUG_LIST_PUTTAERT.md** - 9 bugs encontrados en Puttaert
4. **BUGS_IN_BASELINE.md** - 4 bugs en Baseline
5. **BUGS_IN_OPTIMIZED_ACTUAL.md** - 3 bugs en Optimized_Actual
6. **BUGS_IN_BAX_FIXED.md** - 7 bugs en BAX_Fixed
7. **MASTER_BUG_MATRIX.md** - Matriz completa de bugs por modelo

Además, agregué:
- **Comentarios con números de constraint** en cada modelo .ipynb
- **Tags \tag{DV#}** en cada ecuación LaTeX para trazabilidad perfecta

---

## 9️⃣ PLAN DE CORRECCIÓN PROPUESTO

### **Opción 2: Corregir TODOS los Bugs** ← MI RECOMENDACIÓN

**Razón:** Para tener una comparación justa "manzanas con manzanas", todos los modelos deben:
- Estar matemáticamente correctos
- Usar la misma lógica eficiente donde aplicable
- Permitir comparación de performance real

**Modelos a corregir:**
1. Baseline.ipynb (4 bugs)
2. Optimized_Actual.ipynb (3 bugs)
3. BAX_Fixed.ipynb (7 bugs)

**NO corregir:** Model_Puttaert.ipynb (decidimos no incluirlo en comparación final)

### **Método de Corrección:**
- **Fixes in-place** en los notebooks existentes (no crear versiones duplicadas)
- **Documentar cada cambio** detalladamente en logs
- **Verificar sintaxis** después de cada fix
- **Testear** que los modelos aún corren

### **Orden de Corrección:**
**Fase A - CRÍTICOS:**
1. Bug #1: Compartimento weights (todos)
2. Bug #2: Item assignment (Baseline, BAX_Fixed)
3. Bug #10: COL/CRT compartimento (todos)
4. Bug #3: COL/CRT simplificar (BAX_Fixed)

**Fase B - ALTA PRIORIDAD:**
5. Bug #11: Multi-obj índices (Baseline, Optimized_Actual)
6. Bug #4: Eliminar variable w (BAX_Fixed)
7. Bug #5: Separación penalty (Baseline, BAX_Fixed)
8. Bug #8: Combinar peso posición (BAX_Fixed)

---

## 🔟 PREGUNTAS PARA USTED

### **A. Sobre la Estrategia de Corrección:**

**1.** ¿Está de acuerdo con corregir **todos los bugs** (no solo los críticos) para tener máxima comparabilidad?

**2.** ¿Prefiere que corrija directamente los notebooks existentes, o que cree versiones "_corrected"?

**3.** ¿Hay algún bug que prefiera NO corregir para preservar la lógica original del benchmark?

### **B. Sobre Inclusión de Modelos:**

**4.** Confirmé que BAX_Fixed = Puttaert + BF1. ¿Tiene sentido incluir ambos en la comparación final, o solo BAX_Fixed?

**5.** ¿Debería incluir Model_Puttaert en la comparación (con bugs documentados) como "versión original" vs mi versión corregida?

### **C. Sobre Próximos Pasos:**

Después de corregir los bugs, podemos continuar con:

**Opción A: Heurísticas**
- Analizar y potencialmente mejorar las heurísticas de 3D-BPP (extreme points)
- Revisar lógica de feedback loop
- Optimizar criterios de "item diferido"

**Opción B: Infeasibilities**
- Investigar causas de infactibilidades cuando ocurren
- Mejorar manejo de casos extremos
- Fortalecer lógica de reopening ULDs

**Opción C: Ejecutar Código Corregido**
- Correr los modelos corregidos en el conjunto de 102 vuelos
- Comparar resultados antes/después de las correcciones
- Analizar si los bugs afectaban significativamente los resultados

**6.** ¿Cuál de estas opciones prefiere abordar primero?

**7.** ¿O prefiere que corrija todos los bugs primero y luego decidimos el siguiente paso basado en los resultados?

### **D. Sobre Documentación para la Tesis:**

**8.** ¿Debería incluir en la tesis una sección sobre "Errores detectados y corregidos en modelos benchmark" para transparencia metodológica?

**9.** ¿Los fixes aplicados ameritan reconocimiento en contribuciones (ej: "se identificaron y corrigieron X errores en los modelos de referencia")?

---

## 🎯 MI RECOMENDACIÓN

Basándome en lo que he encontrado, sugiero:

**Paso 1:** Corregir todos los bugs críticos (#1, #2, #3, #10) en los 3 benchmarks
- Esto asegura correctitud matemática
- ~2-3 horas de trabajo cuidadoso

**Paso 2:** Corregir bugs de alta prioridad (#4, #5, #7, #8, #11)
- Asegura eficiencia y comparabilidad justa
- ~1-2 horas adicionales

**Paso 3:** Ejecutar modelos corregidos en subconjunto de vuelos (ej: 10 vuelos)
- Verificar que las correcciones no rompan nada
- Ver si los resultados cambian significativamente

**Paso 4:** Decisión basada en resultados
- Si bugs afectan mucho → documentar en tesis
- Si bugs no afectan → proceder con análisis completo

**Paso 5:** Análisis completo de 102 vuelos con benchmarks corregidos

---

## 📚 ARCHIVOS ADJUNTOS

Adjunto la documentación completa para su revisión:
- `MASTER_BUG_MATRIX.md` - Tabla resumen de todos los bugs
- `CORRECT_MODEL_REFERENCE.md` - Referencia de mi modelo correcto
- Archivos individuales de bugs por modelo

---

Quedo atenta a sus comentarios y orientación sobre cómo proceder. Esta revisión profunda ha revelado más de lo que anticipaba, y quiero asegurarme de que tomamos la decisión correcta sobre qué corregir y cómo documentarlo.

Muchas gracias por su guía constante.

Saludos cordiales,

**María Emilia Venezian Juricic**  
Estudiante de Ingeniería Civil Industrial  
Pontificia Universidad Católica de Chile

---

**P.D.:** Todos los archivos están en la carpeta del proyecto con documentación detallada. Si necesita que profundice en algún bug específico o quiere discutir algún aspecto técnico, estoy disponible.

