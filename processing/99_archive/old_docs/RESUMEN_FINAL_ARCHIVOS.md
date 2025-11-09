# 📊 RESUMEN FINAL - Sistema de Datos KLM

## 1️⃣ PieceInformationSpotfire.csv

### Estructura:
- **Con líneas informacionales (57%)**: Datos reales
- **Sin líneas informacionales (43%)**: Matriz cartesiana

### Regla Clave:
```
BookingTotalPieceCount = Σ BookingSegmentPiecesCount (por ID único)
```

### TIPO A: Con datos informativos
```
PiecesID=1: IsInformational=FALSE (placeholder, ignorar)
PiecesID≥2: IsInformational=TRUE (datos reales)

Ejemplo AWB 58692362 (22 piezas):
  - PiecesID=2: Count=1 → 1 pieza
  - PiecesID=7: Count=2 → 2 piezas idénticas
  - PiecesID=13: Count=4 → 4 piezas idénticas
  Total: 22 piezas
```

### TIPO B: Sin datos informativos (matriz cartesiana)
```
Ejemplo AWB 7459521221 (17 piezas):
  - 289 líneas totales (17×17)
  - Todas IsInformational=FALSE
  - Filtrar donde SegmentWeight ≈ LineWeight
  - Resultado: 17 líneas correctas (1 por pieza)
```

---

## 2️⃣ BuildUpInformationSpotfire.csv

### ¿Qué es cada fila?
```
CADA FILA = UN EVENTO DE CARGA
- NrBuildupPieces = piezas cargadas en ese evento
- StorageSequenceNumber = número de lote (1,2,3...)
- Múltiples filas por AWB = carga en múltiples momentos
```

### Ejemplo AKE96298KL:
```
AWB 7459521221:
  Lote 1: 5 piezas   (16:52)
  Lote 2: 3 piezas   (16:52)
  Lote 3: 1 pieza    (16:52)
  Lote 4: 8 piezas   (16:52)
  Total: 17 piezas

AWB 7464227645:
  Lote 3: 4 piezas   (16:55)
  
TOTAL ULD: 21 piezas cargadas
```

### Columnas clave:
- `TotalNumberOfShipments`: Significado incierto (contador interno)
- `AirWaybillStorageSequenceNumber`: Número de lote
- `NrBuildupPieces`: Piezas en ese lote
- `IsNotBuildUp=TRUE`: AWB no procesado (campos vacíos)

### Problema encontrado:
```
AWB puede aparecer en MÚLTIPLES ULDs con mismo StorageSeq
→ Registros duplicados/errores
→ Suma(NrBuildupPieces) puede > NumberOfPiecesOnAWB
```

---

## 3️⃣ LoadLocationsSpotfire.csv

### ¿Qué muestra?
```
Estado FINAL del ULD en el avión
- Peso total (Weight)
- Ubicación (Hold, LoadLocation)
- UldGrossWeight, UldTareWeight
```

### Ejemplo AKE96298KL:
```
4 registros con:
  - LoadType: ULD
  - DeadloadType: C
  - Weight: 473 kg
  - NumberOfItemsInUld: NaN (vacío)
```

### Relación con BuildUp:
```
BuildUp suma: 21 piezas
LoadLocations: 473 kg

473 kg ≠ 422.7 kg (AWB 7459521221 solo)
Porque incluye AWB 7464227645 parcial
```

---

## 🔗 RELACIÓN ENTRE LOS 3 ARCHIVOS

```
PieceInformation
    ↓ (detalles de piezas)
    
BuildUpInformation
    ↓ (asignación a ULDs)
    
LoadLocations
    ↓ (ubicación en avión)
```

### Flujo de datos:
1. **PieceInformation**: Qué piezas hay en cada AWB
2. **BuildUp**: Qué piezas de cada AWB van a qué ULD
3. **LoadLocations**: Qué ULDs van a qué posición del avión

---

## ✅ REGLAS VERIFICADAS

### Para optimización, usa:

**De PieceInformation:**
```python
if IsInformational=TRUE existe:
    # Usar solo líneas TRUE
    for cada PiecesID≥2:
        crear BookingSegmentPiecesCount piezas idénticas
        con dimensiones BookingLinePiece*
else:
    # Filtrar donde SegmentWeight ≈ LineWeight
    for cada PiecesID único:
        1 pieza con esas dimensiones
```

**De BuildUp:**
```python
# Agrupar por ULD
for cada ULD:
    for cada AWB en ese ULD:
        suma(NrBuildupPieces) = piezas de ese AWB en ese ULD
```

**De LoadLocations:**
```python
# Restricciones del avión
for cada ULD:
    - posición (Hold, LoadLocation)
    - peso máximo verificado con UldGrossWeight
```

---

## ⚠️ INCONSISTENCIAS ENCONTRADAS

1. **BuildUp puede tener registros duplicados**
   - Mismo AWB en múltiples ULDs
   - Suma total puede exceder piezas declaradas

2. **NumberOfItemsInUld casi siempre vacío**
   - No sirve para verificación
   - Solo Weight es confiable

3. **TotalNumberOfShipments no indica AWBs en ULD**
   - Significado desconocido
   - No usar para análisis

---

## 📝 PARA TU MODELO DE OPTIMIZACIÓN

**Inputs necesarios:**
1. Lista de piezas (de PieceInformation procesado)
2. Lista de ULDs disponibles (tipos/capacidades)
3. Restricciones de posición (de LoadLocations)

**Validar resultados con:**
1. BuildUp: ¿Qué AWBs van juntos en práctica?
2. LoadLocations: ¿Qué peso tiene cada ULD real?

**NO usar directamente:**
- Suma de NrBuildupPieces (puede tener duplicados)
- NumberOfItemsInUld (casi siempre vacío)
- TotalNumberOfShipments (significado incierto)

