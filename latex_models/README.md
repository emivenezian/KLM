# Documentación LaTeX - Modelos de Optimización KLM

Este directorio contiene la documentación LaTeX completa para los diferentes modelos de optimización de carga aérea implementados en el proyecto KLM.

## Archivos Incluidos

### 1. `baseline.tex`
**Modelo Baseline** - Implementa una estrategia de optimización en cascada que combina 1D-BPP, 3D-BPP y Weight & Balance.

**Características principales:**
- Enfoque secuencial de tres etapas
- Sistema de feedback loop iterativo
- Tasa de éxito: 77.0%
- Tasa de infactibilidad: 23.0%

### 2. `bax_fixed.tex`
**Modelo BAX Fixed** - Variante que implementa restricciones fijas para ULDs de tipo BAX.

**Características principales:**
- Posiciones fijas para ULDs BAX
- Optimización libre para ULDs regulares
- Tasa de éxito: 66.8%
- Tasa de infactibilidad: 33.2%

### 3. `optimized_actual.tex`
**Modelo Optimized Actual** - Optimización directa de Weight & Balance sin etapas intermedias.

**Características principales:**
- Enfoque simplificado y directo
- Omite empaquetado 1D y 3D
- Tasa de éxito: 84.6%
- Tasa de infactibilidad: 15.4%

### 4. `model_puttaert.tex`
**Modelo Puttaert** - Enfoque integral que combina 1D-BPP con Weight & Balance.

**Características principales:**
- Optimización integral y completa
- Sistema de feedback loop robusto
- Tasa de éxito: 72.1%
- Tasa de infactibilidad: 27.9%

## Compilación

Para compilar los archivos LaTeX, use los siguientes comandos:

```bash
# Compilar un archivo específico
pdflatex baseline.tex
pdflatex bax_fixed.tex
pdflatex optimized_actual.tex
pdflatex model_puttaert.tex

# Compilar todos los archivos
for file in *.tex; do pdflatex "$file"; done
```

## Estructura de los Documentos

Cada documento LaTeX incluye:

1. **Introducción** - Descripción general del modelo
2. **Características** - Enfoque de optimización y parámetros
3. **Variables de Decisión** - Definición matemática de variables
4. **Restricciones** - Ecuaciones y limitaciones del modelo
5. **Función Objetivo** - Objetivos de optimización
6. **Resultados** - Estadísticas de rendimiento
7. **Análisis Comparativo** - Comparación con otros modelos
8. **Ventajas y Desventajas** - Evaluación del modelo
9. **Conclusiones** - Resumen y recomendaciones

## Comparación de Rendimiento

| Modelo | Tasa de Éxito | Infactibilidad | Ranking |
|--------|---------------|----------------|---------|
| Venezian | 89.8% | 10.2% | 1 |
| Optimized Actual | 84.6% | 15.4% | 2 |
| Baseline | 77.0% | 23.0% | 3 |
| Puttaert | 72.1% | 27.9% | 4 |
| BAX Fixed | 66.8% | 33.2% | 5 |

## Notas Técnicas

- Todos los modelos utilizan Gurobi como solver
- Los modelos implementan restricciones de balance de peso
- Se incluyen restricciones para ULDs especiales (BAX, BUP, T-ULD)
- Los modelos manejan diferentes tipos de carga (CRT, COL, peligrosa)

## Autor

**María Emilia Venezian Juricic**  
Proyecto de Optimización de Combustible KLM  
Pontificia Universidad Católica de Chile  
Supervisor: Dr. Felipe Delgado

## Fecha de Generación

Documentos generados el: $(date)


