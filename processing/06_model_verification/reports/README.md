# 📚 Documentación de Análisis de Bugs - Modelos Benchmark

**Fecha:** Octubre 2025  
**Propósito:** Documentación completa del análisis de modelos benchmark y errores detectados

---

## 🎯 COMIENZA AQUÍ

**Lee estos archivos en este orden:**

1. **MASTER_BUG_MATRIX.md** ← EMPIEZA AQUÍ
   - Matriz completa de todos los 11 bugs por modelo
   - Vista de alto nivel de qué está mal en cada benchmark

2. **CORRECT_MODEL_REFERENCE.md**
   - Documentación completa del modelo DelgadoVenezian (referencia correcta)
   - Cada constraint explicada en detalle
   - Esta es la "verdad" contra la que se comparan los demás

3. **KEY_CORRECT_IMPLEMENTATIONS.md**
   - Foco en las 3 implementaciones clave correctas:
     * Fórmula MAC
     * Restricciones de peso por compartimento
     * Lógica COL/CRT temperatura sensible

---

## 🐛 ANÁLISIS DE BUGS POR MODELO

### **Para Modelo Puttaert:**
📄 **COMPLETE_BUG_LIST_PUTTAERT.md**
- 9 bugs encontrados en detalle
- Comparación línea por línea con DelgadoVenezian
- Explicación de cada bug con ejemplos de código

📄 **BUGS_FOUND_IN_PUTTAERT.md**
- Versión resumida de los bugs más críticos

### **Para Baseline (Sequential):**
📄 **BUGS_IN_BASELINE.md**
- 4 bugs encontrados
- 3 críticos, 1 alta prioridad
- Incluye 2 bugs nuevos no presentes en Puttaert

### **Para Optimized_Actual (W&B-focused):**
📄 **BUGS_IN_OPTIMIZED_ACTUAL.md**
- 3 bugs encontrados (el modelo más limpio!)
- 2 críticos, 1 alta prioridad
- Análisis de por qué es más simple que los demás

### **Para BAX_Fixed:**
📄 **BUGS_IN_BAX_FIXED.md**
- 7 bugs encontrados
- Confirmación: BAX_Fixed = Puttaert + BF1 constraint
- Hereda casi todos los bugs de Puttaert

---

## 🗺️ TRAZABILIDAD CÓDIGO ↔ LATEX

📄 **CONSTRAINT_MAPPING_COMPLETE.md**
- Mapeo completo de comentarios en código a tags en LaTeX
- Todos los modelos tienen numeración:
  * DelgadoVenezian: DV1-DV26
  * Optimized_Actual: O1-O12
  * Baseline: R1-R7 (1D-BPP) + W1-W12 (W&B)
  * Puttaert: P1-P30 + L1-L7 (linearization)
  * BAX_Fixed: P1-P30 + L1-L7 + BF1

📄 **VENEZIAN_DELGADO_COMPLETE.md**
- Documentación específica del modelo DelgadoVenezian
- Innovaciones y mejoras sobre Puttaert
- Mapeo detallado DV1-DV26

---

## 📊 RESUMEN EJECUTIVO

### **Bugs Críticos (Afectan Correctitud):**
1. **Bug #1:** Restricciones de peso por compartimento (TODOS)
2. **Bug #2:** Asignación de ítems incluye BAX/BUP/T (3 modelos)
3. **Bug #10:** COL/CRT por posición vs compartimento (TODOS)
4. **Bug #3:** Lógica COL/CRT excesivamente compleja (2 modelos)

### **Bugs Alta Prioridad (Afectan Eficiencia):**
5. **Bug #4:** Variable w linearización innecesaria
6. **Bug #5:** Penalización separación subóptima
7. **Bug #7:** Big-M hardcoded
8. **Bug #8:** Restricción peso posición dividida
9. **Bug #11:** Índices multi-objetivo incorrectos

### **Conteo por Modelo:**
- Puttaert: 8 bugs
- Baseline: 4 bugs
- Optimized_Actual: 3 bugs ← Más limpio
- BAX_Fixed: 7 bugs
- DelgadoVenezian: 0 bugs ✅

---

## 🎯 PRÓXIMOS PASOS

Ver archivo **PROPUESTA_ORGANIZACION.md** para plan de corrección completo.

**Plan recomendado:**
1. Corregir bugs críticos (#1, #2, #3, #10)
2. Corregir bugs alta prioridad (#4, #5, #7, #8, #11)
3. Test en subset de vuelos (10 vuelos)
4. Análisis completo con modelos corregidos

---

## 📧 COMUNICACIONES

Para emails al profesor, ver carpeta `../communications/`:
- EMAIL_FINAL_PROFESOR.txt (detallado y pedagógico)
- EMAIL_RESUMEN_MEJORADO.txt (resumen ejecutivo)

---

**Última actualización:** Octubre 28, 2025  
**Autor:** María Emilia Venezian Juricic

