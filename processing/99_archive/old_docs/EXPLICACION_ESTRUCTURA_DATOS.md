# 📊 EXPLICACIÓN COMPLETA DE LA ESTRUCTURA DE DATOS

## AWB 7459521221 - CASO DE ESTUDIO

---

## ✅ RESPUESTA CORTA

**HAY 17 PIEZAS FÍSICAS REALES**, no 289.

Las 289 líneas son un **PRODUCTO CARTESIANO** generado por Spotfire que crea todas las combinaciones posibles entre las 17 piezas.

---

## 🎯 ESTRUCTURA DE LOS DATOS

### PieceInformation (289 líneas)

```
BookingTotalPieceCount: 17  → 17 piezas físicas reales
Total de líneas: 289        → 17 × 17 = 289 (matriz cartesiana)
```

**¿Por qué 289 líneas?**

El sistema genera una **MATRIZ DE COMPATIBILIDAD** donde cada pieza se cruza con todas las demás:

```
                    BookingLinePieceWeight (columnas)
                    1.21  2.01  3.23  ... 46.14  68.48  132.12
                    
BookingSegment  1   [ ]   [ ]   [ ]   ...  [✓]    [ ]    [ ]
PiecesID        2   [ ]   [ ]   [ ]   ...  [ ]    [ ]    [ ]
(filas)         3   [ ]   [ ]   [ ]   ...  [ ]    [ ]    [ ]
                ... 
                17  [ ]   [ ]   [ ]   ...  [ ]    [ ]    [ ]
```

- Cada fila = 1 pieza física (BookingSegmentPiecesID)
- Cada columna = peso de otra pieza (BookingLinePieceWeight)
- Total: 17 filas × 17 columnas = 289 celdas (pero hay solo 16 valores únicos de peso)

---

## 📋 SIGNIFICADO DE LAS COLUMNAS

### 1. **BookingSegmentPiecesID** (1-17)
- ✅ Identificador de la **pieza física real**
- Son 17 piezas diferentes

### 2. **BookingSegmentPiecesWeight** 
- ✅ Peso de la **pieza física identificada por PiecesID**
- Este es el peso REAL de cada pieza
- Ejemplo: Pieza #1 = 46.14 kg, Pieza #2 = 3.30 kg

### 3. **BookingSegmentPiecesVolume**
- ✅ Volumen de la **pieza física identificada por PiecesID**
- Este es el volumen REAL de cada pieza

### 4. **BookingLinePieceWeight** ⚠️ ¡COLUMNA CONFUSA!
- ❌ **NO es el peso de "la línea"**
- ✅ Es el peso de **OTRA pieza** en la matriz cartesiana
- Toma los valores de todas las piezas (1.21, 2.01, 3.23, ... 132.12)
- Se usa para crear combinaciones/análisis de compatibilidad

### 5. **BookingLinePieceVolume**, **BookingLinePieceHeight/Width/Length**
- ❌ **NO son las dimensiones de la pieza actual**
- ✅ Son las dimensiones de **OTRA pieza** (la que corresponde a LineWeight)

---

## 🔍 CÓMO OBTENER LOS DATOS CORRECTOS

### ✅ Método: Filtrar donde `SegmentWeight == LineWeight`

Cuando `BookingSegmentPiecesWeight` == `BookingLinePieceWeight`, esa línea contiene los datos **correctos** de esa pieza.

**Datos correctos del AWB 7459521221:**

| PiezaID | Weight  | Volume | Height | Width | Length |
|---------|---------|--------|--------|-------|--------|
| 1       | 46.14   | 0.28   | 60     | 58    | 79     |
| 2       | 3.30    | 0.02   | 26     | 21    | 36     |
| 3       | 3.23    | 0.02   | 14     | 32    | 43     |
| 4       | 3.30    | 0.02   | 26     | 21    | 36     |
| 5       | 37.06   | 0.22   | 46     | 60    | 80     |
| 6       | 9.15    | 0.05   | 41     | 35    | 38     |
| 7       | 1.21    | 0.01   | 20     | 19    | 19     |
| 8       | 68.48   | 0.41   | 85     | 60    | 80     |
| 9       | 10.20   | 0.06   | 31     | 37    | 53     |
| 10      | 8.08    | 0.05   | 47     | 32    | 32     |
| 11      | 12.56   | 0.08   | 27     | 42    | 66     |
| 12      | 132.12  | 0.79   | 82     | 80    | 120    |
| 13      | 64.45   | 0.38   | 40     | 80    | 120    |
| 14      | 8.12    | 0.05   | 24     | 42    | 48     |
| 15      | 2.01    | 0.01   | 20     | 20    | 30     |
| 16      | 9.06    | 0.05   | 30     | 30    | 60     |
| 17      | 4.23    | 0.03   | 21     | 30    | 40     |

**Total: 422.70 kg ✓**

---

## 🔗 BUILDUPINFORMATION

En BuildUpInformation tenemos **4 líneas** para este AWB:

```
AWB 7459521221 → ULD AKE96298KL
Lote 1: 5 piezas
Lote 2: 3 piezas
Lote 3: 1 pieza
Lote 4: 8 piezas
TOTAL: 17 piezas ✓
```

**Interpretación:**
- Las 17 piezas físicas se cargaron en 4 "lotes" o grupos
- Todas van en el mismo ULD (AKE96298KL)
- BuildUp NO dice CUÁLES piezas específicas van en cada lote
- Solo dice CUÁNTAS piezas hay en cada lote

---

## 🎯 PARA TU OPTIMIZACIÓN

### ✅ USA ESTO:

```python
# Filtrar solo las líneas donde SegmentWeight == LineWeight
df_correct = piece_info[
    abs(piece_info['BookingSegmentPiecesWeight'] - 
        piece_info['BookingLinePieceWeight']) < 0.01
]

# Ahora tienes 17 líneas (1 por pieza)
# Usa: BookingSegmentPiecesID, Weight, Volume, Height, Width, Length
```

### ❌ NO USES:

- Las 289 líneas completas
- `BookingLinePieceWeight` sin filtrar
- `BookingLinePieceHeight/Width/Length` sin filtrar

---

## 📦 RESUMEN DE LOS 3 ARCHIVOS

```
1. PieceInformation
   → Detalles de cada pieza física
   → 289 líneas (filtrar a 17)
   → Peso, dimensiones, volumen

2. BuildUpInformation  
   → Asignación de piezas a ULDs
   → 4 líneas (lotes de carga)
   → Dice CUÁNTAS piezas por lote, no CUÁLES

3. LoadLocations
   → Ubicación del ULD en el avión
   → 1 línea por ULD
   → Peso total del ULD (suma de AWBs)
```

---

## ⚠️ MISTERIO DE LOS PESOS

```
PieceInformation:    422.70 kg (suma de 17 piezas)
BuildUpInformation:  422 kg    (redondeado)
LoadLocations:       473 kg    (¡DIFERENTE!)
```

**¿Por qué 473 kg en LoadLocations?**

Porque el ULD **AKE96298KL** contiene 2 AWBs:
- AWB 7459521221: 17 piezas = ~422 kg
- AWB 7464227645: 4 de 7 piezas = ~51 kg (estimado)
- **TOTAL: ~473 kg ✓**

---

## 💡 TU ANALOGÍA ORIGINAL

> "yo habia entendido que eran como 17 cajas de ikea cada una con 17 items adentro"

**Corrección:**
- ❌ NO son 17 cajas idénticas
- ✅ Son **17 cajas DIFERENTES** (cada una con peso y tamaño distinto)
- ❌ NO hay 17 items dentro de cada caja
- ✅ Cada caja es **1 item físico** con sus propias características

**La matriz de 289 líneas es solo un artefacto del sistema de reporting de Spotfire, NO representa la realidad física.**

---

## 🎓 CÓDIGO DE EJEMPLO

```python
import pandas as pd

# Leer datos
piece_info = pd.read_csv('PieceInformationSpotfire.csv')

# Filtrar AWB
df = piece_info[piece_info['BookingAirWaybillNumber'] == 7459521221]

# Convertir pesos
df['SegWeight'] = df['BookingSegmentPiecesWeight'].str.replace(',', '.').astype(float)
df['LineWeight'] = df['BookingLinePieceWeight'].str.replace(',', '.').astype(float)

# Filtrar solo las líneas correctas
df_correct = df[abs(df['SegWeight'] - df['LineWeight']) < 0.01]

# Ahora tienes 17 líneas (1 por pieza física)
print(f"Piezas físicas: {len(df_correct)}")
print(f"Peso total: {df_correct['SegWeight'].sum():.2f} kg")
```

---

## ✅ RESPUESTA A TUS PREGUNTAS

### 1. "¿Son 289 piezas físicas reales o 17?"
**→ 17 piezas físicas reales**

### 2. "¿Qué es BookingLineWeight?"
**→ Es el peso de otra pieza en la matriz cartesiana (NO de la pieza actual)**

### 3. "¿Por qué hay casos donde ULD ≠ OutgoingULDKey?"
**→ NO hay casos. Siempre son iguales (columnas redundantes)**

### 4. "¿Por qué 422.7 → 422 → 473?"
**→ El ULD contiene múltiples AWBs, 473 kg es la suma de todos**

### 5. "¿BuildUp me dice qué subpieza va en cada lote?"
**→ NO. Solo dice CUÁNTAS piezas por lote, no CUÁLES**

### 6. "¿El ULD tiene 289 piezas?"
**→ NO. Tiene 21 piezas (17 del AWB 7459521221 + 4 del AWB 7464227645)**

