# PieceInformationSpotfire.csv - Base de Conocimiento Completa

## 📊 OVERVIEW
- **Total Registros**: 37,417 piezas individuales
- **AWB únicos**: 15,725 Air Waybills
- **Vuelos**: 8 (KL0835, KL0661, KL0871, KL0855, KL0601, KL0879, KL0605, KL0603)
- **Rutas**: 695 combinaciones origen-destino
- **Periodo**: Febrero-Marzo 2024
- **Columnas**: 49 campos

---

## 🎯 ¿QUÉ ES ESTE ARCHIVO?

`PieceInformationSpotfire.csv` contiene información **a nivel de PIEZA INDIVIDUAL** de carga.

### Diferencia con LoadLocations:
| Archivo | Nivel | Información |
|---------|-------|-------------|
| **PieceInformation** | Pieza individual | Dimensiones, peso por pieza, AWB, booking |
| **LoadLocations** | ULD/Contenedor | Posición en avión, peso total ULD, DeadloadIds |

**Relación**: Múltiples piezas (PieceInformation) → 1 DeadloadId (LoadLocations) → 1 ULD

---

## 📋 ESTRUCTURA DE COLUMNAS (49 CAMPOS)

### Grupo 1: Información de Booking (1-16)
1. **BookingUpdateDatetimeUTC** - Fecha/hora de actualización del booking
2. **BookingAirWaybillPrefix** - Prefijo del AWB (ej: 6 para código IATA)
3. **BookingAirWaybillSerialNumber** - Número de serie del AWB
4. **BookingAirWaybillNumber** - AWB completo (ej: 640548303)
5. **BookingOriginStationCode** - Aeropuerto de origen
6. **BookingDestinationStationCode** - Aeropuerto de destino
7. **BookingEvaluationStatus** - Estado del booking (A=Activo, R=Rechazado, Q=?)
8. **BookingTotalVolume** - Volumen total del booking
9. **BookingVolumeUnitCode** - Unidad de volumen (MC = metro cúbico)
10. **BookingTotalWeight** - Peso total del booking
11. **BookingWeightUnitCode** - Unidad de peso (K = kg, L = lbs)
12. **BookingTotalPieceCount** - Cantidad total de piezas en el booking
13. **BookingProductCode** - Código de producto (R21, M21, M25, etc.)
14. **BookingCommodityCode** - Tipo de mercancía (GENE, BOAT, PHAR, etc.)
15. **BookingUpdateStationCode** - Estación que actualizó el booking
16. **BookingUpdateChannelCode** - Canal de actualización (FFM, MYC, BFE, etc.)

### Grupo 2: Características Especiales (17-24) - FLAGS
17. **IsBUP** - Build-Up (consolidación)
18. **IsCOL** - Cool/Cold Chain (refrigerado)
19. **IsCRT** - Critical/Critters (animales vivos)
20. **IsPEV** - Perishable Valuable
21. **IsICE** - Dry Ice (hielo seco)
22. **IsACT** - Active (carga activa)
23. **IsACE** - Active Cool Extended
24. **IsDangerousGoods** - Mercancías peligrosas

### Grupo 3: Información de Segmento (25-36)
25. **BookingPartShipmentID** - ID del envío parcial
26. **BookingSegmentAirlineDesignator** - Aerolínea (KL = KLM)
27. **BookingSegmentFlightNumber** - Número de vuelo
28. **BookingSegmentFlight** - Vuelo completo (ej: KL0835)
29. **BookingSegmentOperationalSuffix** - Sufijo operacional (siempre vacío)
30. **BookingSegmentBoardPointStationCode** - Punto de embarque (siempre AMS)
31. **BookingSegmentOffPointStationCode** - Punto de desembarque
32. **BookingSegmentFlightDateUTC** - Fecha de vuelo (UTC)
33. **BookingSegmentFlightDateLT** - Fecha de vuelo (hora local)
34. **BookingSegmentVolume** - Volumen del segmento
35. **BookingSegmentWeight** - Peso del segmento
36. **BookingSegmentPieceCount** - Cantidad de piezas en el segmento

### Grupo 4: Información de Piezas en Segmento (37-43)
37. **BookingLineNumber** - Número de línea
38. **BookingSegmentPiecesID** - ID de piezas en el segmento (valores 1-17)
39. **BookingSegmentPiecesVolume** - Volumen de piezas
40. **BookingSegmentPiecesWeight** - Peso de piezas
41. **BookingSegmentPiecesCount** - Cantidad de piezas
42. **BookingSegmentPiecesStackable** - ¿Se puede apilar? (TRUE/FALSE)
43. **BookingSegmentPiecesTurnable** - ¿Se puede voltear? (TRUE/FALSE)

### Grupo 5: Información de Pieza Individual (44-49)
44. **BookingLinePieceVolume** - Volumen de la pieza individual
45. **BookingLinePieceWeight** - Peso de la pieza individual
46. **BookingLinePieceHeight** - Altura de la pieza (cm)
47. **BookingLinePieceWidth** - Ancho de la pieza (cm)
48. **BookingLinePieceLength** - Largo de la pieza (cm)
49. **BookingLinePieceIsInformational** - ¿Es informacional? (TRUE/FALSE)

---

## 🔑 CAMPOS CLAVE EXPLICADOS

### BookingEvaluationStatus
- **A** (37,391 - 99.9%) = Activo/Aprobado
- **R** (19) = Rechazado
- **Q** (6) = En cuarentena/Cuestionado

### BookingProductCode (Tipo de producto de carga)
```
R21: 20,683 (55.3%) - Premium Express?
M21:  5,110 (13.7%) - Mail Service?
M25:  3,113 (8.3%)  - Mail Priority?
R91:  1,898 (5.1%)  - Regular?
S23:  1,690 (4.5%)  - Special Service?
C01:  1,324 (3.5%)  - Cargo Standard?
S30:  1,018 (2.7%)  - Special Express?
```

### BookingCommodityCode (Tipo de mercancía)
```
GENE: 21,817 (58.3%) - General cargo
BOAT:  4,882 (13.0%) - Boats/Watercraft
CNSL:  1,924 (5.1%)  - Consolidado
DGRS:  1,784 (4.8%)  - Dangerous Goods Restricted
PHAR:  1,411 (3.8%)  - Pharmaceuticals
GOLD:    779 (2.1%)  - Oro/Precious metals
VARI:    692 (1.8%)  - Varios
ACFT:    626 (1.7%)  - Aircraft parts
FLWR:    525 (1.4%)  - Flores
SLMN:    499 (1.3%)  - Salmon (peces)
```

### BookingUpdateChannelCode
```
FFM:    36,175 (96.7%) - Flight Freight Manifest
MYC:       620 (1.7%)  - MyCargo (portal web)
BFE:       357 (1.0%)  - Back End File Exchange
FWB:       172 (0.5%)  - Forward Booking
RCSRCT:     53 (0.1%)  - RC System
FPLN:       25 (0.1%)  - Flight Plan
```
**FFM** = Manifesto de carga del vuelo (mensaje estándar IATA)

---

## 🚩 CARACTERÍSTICAS ESPECIALES (FLAGS)

### Distribución:
| Flag | TRUE | % | Significado |
|------|------|---|-------------|
| **IsDangerousGoods** | 4,374 | 11.7% | Mercancías peligrosas (DG) |
| **IsCOL** | 2,328 | 6.2% | Cadena de frío (refrigerado) |
| **IsCRT** | 606 | 1.6% | Animales vivos o crítico |
| **IsICE** | 292 | 0.8% | Con hielo seco |
| **IsBUP** | 146 | 0.4% | Build-up (consolidación) |
| **IsACE** | 21 | 0.06% | Cool activo extendido |
| **IsPEV** | 14 | 0.04% | Perecedero valioso |
| **IsACT** | 0 | 0% | Activo (ninguno en dataset) |

### Piezas con características especiales:
- **Total**: 7,226 piezas (19.3%)
- **Sin características**: 30,191 piezas (80.7%)

---

## ⚖️ ANÁLISIS DE PESOS

### Estadísticas generales:
```
Peso total de todas las piezas: 3,085,662 kg (3,086 toneladas)
Peso promedio por pieza:        136.90 kg
Peso mediano por pieza:         64.00 kg
Mínimo:                         0.00 kg (registros sin peso)
Máximo:                         2,618.00 kg
```

### Por nivel de agregación:
| Campo | Promedio | Mediana | Descripción |
|-------|----------|---------|-------------|
| **BookingTotalWeight** | 516.7 kg | 193 kg | Peso total del booking completo |
| **BookingSegmentPiecesWeight** | 125.1 kg | 50.2 kg | Peso de piezas en un segmento |
| **BookingLinePieceWeight** | 136.9 kg | 64 kg | Peso de pieza individual |

### Peso promedio por característica especial:
```
IsBUP (Build-up):         445.32 kg - Más pesado (consolidado)
IsPEV (Perishable Val):   416.35 kg - Valioso y pesado
IsCOL (Cool):             151.44 kg - Refrigerado mediano
IsACE (Active Cool Ext):  164.54 kg - Activo medio
IsCRT (Critters):         140.74 kg - Animales vivos
IsDangerousGoods:          65.61 kg - Peligrosos más ligeros
IsICE (Dry Ice):           64.06 kg - Con hielo (ligeros)
```

**Patrón**: Carga consolidada (BUP) y valiosa (PEV) es más pesada. Mercancías peligrosas y con hielo seco tienden a ser más ligeras.

---

## 📏 DIMENSIONES DE PIEZAS

### Disponibilidad:
- **Con dimensiones completas (H, W, L)**: 22,106 piezas (59.1%)
- **Sin dimensiones**: 15,311 piezas (40.9%)

### Dimensiones más comunes:
```
Altura (Height):  20 cm (765 piezas) - más común
Ancho (Width):    80 cm (4,734 piezas) - estándar
Largo (Length):   120 cm (5,332 piezas) - más frecuente
```

**Caja típica**: 120 cm (L) × 80 cm (W) × 20 cm (H) = 0.192 m³

### Volumen:
```
Promedio:  2.25 m³
Mediana:   0.90 m³
Mínimo:    0.01 m³
Máximo:    90 m³
Unidad:    MC (metro cúbico)
```

---

## 🎲 PROPIEDADES FÍSICAS

### Stackable (¿Se puede apilar?)
- **TRUE**: 36,274 piezas (96.9%) ✅
- **FALSE**: 16 piezas (0.04%) ❌

**Interpretación**: La gran mayoría de la carga puede apilarse.

### Turnable (¿Se puede voltear/rotar?)
- **TRUE**: 35,920 piezas (96.0%) ✅
- **FALSE**: 370 piezas (1.0%) ❌

**Interpretación**: La mayoría puede reorientarse para optimizar espacio.

### Combinaciones:
```
Stackable=TRUE  + Turnable=TRUE:  35,920 (98.5%) - Máxima flexibilidad
Stackable=TRUE  + Turnable=FALSE:    354 (1.0%)  - Apilar solo
Stackable=FALSE + Turnable=FALSE:     16 (0.04%) - Sin manipulación
```

**Las 16 piezas no stackable ni turnable** probablemente son:
- Carga muy frágil
- Formas irregulares
- Equipos con orientación fija
- Animales vivos (IsCRT)

---

## 🗺️ RUTAS Y DESTINOS

### Top 10 rutas por volumen:
```
1. AMS->SIN:  5,664 piezas (15.1%) - Singapur
2. AMS->IAH:  2,196 piezas (5.9%)  - Houston
3. AMS->LAX:  1,965 piezas (5.3%)  - Los Ángeles
4. AMS->ICN:  1,519 piezas (4.1%)  - Seúl
5. AMS->SFO:  1,418 piezas (3.8%)  - San Francisco
6. AMS->DEL:  1,379 piezas (3.7%)  - Delhi
7. RTM->SIN:    900 piezas (2.4%)  - Rotterdam-Singapur
8. LIM->DEL:    895 piezas (2.4%)  - Lima-Delhi
9. RTM->IAH:    687 piezas (1.8%)  - Rotterdam-Houston
10. HAM->SIN:   492 piezas (1.3%)  - Hamburgo-Singapur
```

### Orígenes principales:
```
AMS: 14,897 (39.8%) - Amsterdam (hub principal)
RTM:  1,986 (5.3%)  - Rotterdam
FRA:  1,789 (4.8%)  - Frankfurt
SWK:  1,558 (4.2%)  - ?
HAM:    944 (2.5%)  - Hamburgo
+ 141 orígenes adicionales
```

### Destinos principales:
```
SIN: 10,856 (29.0%) - Singapur (destino #1)
IAH:  7,444 (19.9%) - Houston
DEL:  4,467 (11.9%) - Delhi
ICN:  4,440 (11.9%) - Seúl
LAX:  3,809 (10.2%) - Los Ángeles
BLR:  2,787 (7.4%)  - Bangalore
SFO:  2,507 (6.7%)  - San Francisco
```

---

## ✈️ VUELOS

### Distribución por vuelo:
```
KL0835: 10,856 (29.0%) - AMS->SIN (Singapur)
KL0661:  8,223 (22.0%) - AMS->IAH (Houston)
KL0871:  4,467 (11.9%) - AMS->DEL (Delhi)
KL0855:  4,442 (11.9%) - AMS->ICN (Seúl)
KL0601:  3,824 (10.2%) - AMS->LAX (Los Ángeles)
KL0879:  2,787 (7.4%)  - AMS->BLR (Bangalore)
KL0605:  2,727 (7.3%)  - AMS->SFO (San Francisco)
KL0603:     91 (0.2%)  - Vuelo secundario
```

**Patrón**: 
- 3 vuelos a Asia (SIN, ICN, DEL) = 51% del total
- 3 vuelos a USA (IAH, LAX, SFO) = 39% del total
- 1 vuelo a India (BLR) = 7%

---

## 🆔 JERARQUÍA DE IDs

### Sistema de identificación:
```
AirWaybillNumber (AWB) - 15,725 únicos
  └── PartShipmentID - 15,999 únicos
        └── SegmentPiecesID - 17 únicos (valores: 1-17)
```

### Explicación:
1. **AWB**: Identificador del booking completo (como factura)
2. **PartShipmentID**: Envío parcial (si un AWB se divide en múltiples envíos)
3. **SegmentPiecesID**: Agrupación de piezas dentro del segmento (1-17)

### Promedio:
- **2.38 piezas por AWB**
- **Rango**: 1 - 1,045 piezas por booking

---

## 📊 PIEZAS INFORMACIONALES

### ¿Qué es BookingLinePieceIsInformational?

**TRUE** = 21,379 piezas (57.14%)
- Piezas que son **informativas** en el manifiesto
- Pueden ser consolidaciones o referencias
- Peso promedio: 157.99 kg (más pesadas)

**FALSE** = 14,575 piezas (38.96%)
- Piezas **físicas reales**
- Peso promedio: menor

**NULL** = 1,463 piezas (3.91%)
- Sin información

---

## 🔗 RELACIÓN CON LOADLOCATIONSSPOTFIRE

### Mapping conceptual:
```
PieceInformation                    LoadLocations
==================                  ===================
BookingAirWaybillNumber  ------>   (No directo)
                                    ↓
Multiple Pieces          ------>   1 DeadloadId
                                    ↓
                         ------>   1 LoadId (ULD físico)
                                    ↓
                         ------>   1 LoadLocation (posición en avión)
```

### Ejemplo:
```
AWB: 640548303
  ├── Piece 1: 6.67 kg, 0.01 m³, Stackable=TRUE
  ├── Piece 2: 6.67 kg, 0.01 m³, Stackable=TRUE
  └── Piece 3: 6.67 kg, 0.01 m³, Stackable=TRUE
       ↓
  DeadloadId: 159853711 (20 kg total)
       ↓
  LoadId: 152230046 (ULD: AKE96367KL)
       ↓
  LoadLocation: 41R (AFT)
```

---

## 💡 VALORES NULOS - ANÁLISIS

### Columnas con más nulos:

| Columna | Nulos | % | Razón |
|---------|-------|---|-------|
| **BookingSegmentOperationalSuffix** | 37,417 | 100% | Campo no utilizado |
| **BookingSegmentPiecesWeight** | 22,448 | 60% | No siempre se registra |
| **BookingLinePieceHeight/Width/Length** | 15,311 | 41% | Dimensiones no siempre disponibles |
| **BookingLinePieceWeight** | 14,877 | 40% | Peso no siempre individual |
| **BookingLinePieceVolume** | 1,463 | 4% | Volumen calculado o no registrado |
| **BookingSegmentPiecesID** | 1,127 | 3% | No todas las piezas están agrupadas |

**Patrón**: Las dimensiones y pesos individuales no siempre están disponibles, especialmente para carga consolidada.

---

## 📈 TOP 10 RUTAS POR PESO TOTAL

```
1. AMS->SIN: 249,336 kg (249 tons) - 3,545 piezas
2. AMS->LAX: 153,014 kg (153 tons) - 1,446 piezas
3. AMS->SFO: 150,456 kg (150 tons) -   941 piezas (más pesadas por pieza!)
4. AMS->IAH: 107,167 kg (107 tons) - 1,327 piezas
5. AMS->ICN:  70,650 kg (71 tons)  -   926 piezas
6. AMS->DEL:  68,087 kg (68 tons)  -   551 piezas
7. SWK->IAH:  58,670 kg (59 tons)  -   188 piezas (muy pesadas!)
8. FRA->BLR:  58,071 kg (58 tons)  -   226 piezas
9. RTM->SIN:  48,046 kg (48 tons)  -   404 piezas
10. FRA->SIN: 45,591 kg (46 tons)  -   212 piezas
```

**Peso promedio por pieza por ruta**:
- SWK->IAH: 312 kg/pieza (¡la más pesada!)
- FRA->BLR: 257 kg/pieza
- FRA->SIN: 215 kg/pieza
- AMS->SFO: 160 kg/pieza
- AMS->SIN: 70 kg/pieza

---

## 🎓 PREGUNTAS FRECUENTES - FAQ

### 1. ¿Cuál es la diferencia entre PieceInformation y LoadLocations?
**PieceInformation** = Piezas individuales con dimensiones y AWB  
**LoadLocations** = ULDs completos con posición en el avión

### 2. ¿Qué significa BookingLinePieceIsInformational=TRUE?
Es una pieza informativa en el manifiesto, no necesariamente física separada. Puede ser una consolidación.

### 3. ¿Por qué 40% de las piezas no tienen dimensiones?
Carga consolidada, bulk, o registros donde las dimensiones no fueron capturadas individualmente.

### 4. ¿Todas las piezas se pueden apilar?
No. El 0.04% (16 piezas) no son stackable, probablemente por fragilidad o forma.

### 5. ¿Qué es IsDangerousGoods?
Mercancías peligrosas (11.7% de las piezas) que requieren manejo y documentación especial según IATA.

### 6. ¿Por qué hay más PartShipmentID que AWB?
Un AWB puede dividirse en múltiples envíos parciales (por ejemplo, si va en diferentes vuelos).

### 7. ¿Qué significa BookingProductCode R21?
Código de producto de carga, probablemente relacionado con el nivel de servicio (R = Regular, M = Mail, S = Special, C = Cargo).

### 8. ¿Las piezas pesadas van a destinos específicos?
Sí. SWK->IAH y FRA->BLR tienen las piezas más pesadas en promedio (250-312 kg/pieza).

---

## 📊 MÉTRICAS FINALES

```
Total registros:              37,417 piezas
Total AWBs:                   15,725
Peso total:                   3,085,662 kg (3,086 toneladas)
Volumen total:                ~84,163 m³
Peso promedio/pieza:          136.90 kg
Piezas promedio/AWB:          2.38
Piezas con características
  especiales:                 7,226 (19.3%)
Piezas stackable:             36,274 (96.9%)
Piezas turnable:              35,920 (96.0%)
Piezas con dimensiones:       22,106 (59.1%)

Destino principal:            SIN (29.0%)
Vuelo principal:              KL0835 (29.0%)
Origen principal:             AMS (39.8%)
Mercancía principal:          GENE (58.3%)
Producto principal:           R21 (55.3%)
Canal principal:              FFM (96.7%)
```

---

**Documento creado**: Octubre 2024  
**Dataset**: PieceInformationSpotfire.csv  
**Autor del análisis**: analyze_pieceinformation_detailed.py


