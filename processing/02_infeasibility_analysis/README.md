# Análisis de Infeasibilidad - Directorio 02

## Contenido

Este directorio contiene el análisis completo y consolidado de infactibilidad de todos los modelos de optimización de carga de KLM.

## Archivos

- **`complete_infeasibility_analysis.md`**: Análisis completo consolidado con todas las correcciones y aclaraciones
- **`infeasibility_summary_table.csv`**: Tabla resumen con todos los números por modelo
- **`README.md`**: Este archivo

## Definición de Infeasibilidad

**INFEASIBLE**: Results.txt vacío O no existe (el modelo no pudo resolver el problema)
**VÁLIDO**: Results.txt existe Y tiene contenido (el modelo encontró una solución)

## Resultados Clave

1. **Venezian es el mejor modelo** (89.8% éxito, 5.4% infactibilidad)
2. **Los 102 vuelos comunes** son los que todos los modelos pudieron resolver
3. **Venezian tiene 82 vuelos únicos** que otros modelos no pudieron resolver
4. **Estrategia inteligente**: Venezian ejecutó solo vuelos prometedores

## Ubicación de Archivos Relacionados

- **Excel files**: `../../results/all_klm_variants_*.xlsx`
- **Scripts**: `../../results/scripts/extract_all_klm_variants_to_excel.py`
- **Base de datos**: `../Data_Only_Complete/` (525 vuelos completos)
