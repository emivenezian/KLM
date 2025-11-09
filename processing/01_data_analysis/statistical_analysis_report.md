# Comprehensive Statistical Analysis Report

**Generated:** 2025-09-24 15:10:44

## Executive Summary

This report provides comprehensive statistical analysis of all flight data metrics, including 95% confidence intervals, distribution characteristics, and breakdowns by route, aircraft type, and month.

## Overall Statistical Summary

| Metric | Count | Mean | Std Dev | Min | Max | Median | Q25 | Q75 | 95% CI Lower | 95% CI Upper | Skewness | Kurtosis |
|--------|-------|------|---------|-----|-----|--------|-----|-----|--------------|--------------|----------|----------|
| Cargo Items per Flight | 525 | 66.22 | 46.85 | 2 | 690 | 56.0 | 38.0 | 87.0 | 62.2 | 70.24 | 5.011 | 58.608 |
| Weight per Flight (kg) | 525 | 0.0 | 0.0 | 0 | 0 | 0.0 | 0.0 | 0.0 | nan | nan | nan | nan |
| Volume per Flight (cubic meters) | 525 | 0.0 | 0.0 | 0 | 0 | 0.0 | 0.0 | 0.0 | nan | nan | nan | nan |
| Passengers per Flight | 525 | 5.64 | 0.95 | 5 | 8 | 5.0 | 5.0 | 7.0 | 5.56 | 5.72 | 1.055 | -0.434 |
| ULDs per Flight | 525 | 39.5 | 14.18 | 18 | 164 | 36.0 | 31.0 | 44.0 | 38.28 | 40.71 | 3.582 | 20.539 |
| COL Items per Flight | 525 | 0.0 | 0.0 | 0 | 0 | 0.0 | 0.0 | 0.0 | nan | nan | nan | nan |
| CRT Items per Flight | 525 | 0.0 | 0.0 | 0 | 0 | 0.0 | 0.0 | 0.0 | nan | nan | nan | nan |

## Route Analysis

| Route | Flights | Avg Items | Items CI | Avg Weight | Weight CI | Avg Passengers | Passengers CI | Avg ULDs | ULDs CI |
|-------|---------|-----------|----------|------------|-----------|----------------|---------------|----------|----------|
| AMSBLR | 61 | 45.7 | [41.1, 50.3] | 0.0 | [nan, nan] | 5.0 | [5.0, 5.1] | 32.1 | [31.0, 33.1] |
| AMSDEL | 91 | 49.1 | [44.7, 53.5] | 0.0 | [nan, nan] | 6.2 | [6.0, 6.4] | 52.7 | [47.9, 57.5] |
| AMSSIN | 90 | 119.0 | [103.8, 134.3] | 0.0 | [nan, nan] | 6.9 | [6.7, 7.1] | 48.2 | [45.9, 50.5] |
| AMSIAH | 67 | 99.9 | [92.2, 107.6] | 0.0 | [nan, nan] | 5.1 | [5.0, 5.2] | 31.1 | [30.1, 32.1] |
| AMSSFO | 63 | 42.4 | [38.3, 46.5] | 0.0 | [nan, nan] | 5.1 | [5.0, 5.2] | 31.5 | [30.1, 32.8] |
| AMSICN | 64 | 56.7 | [51.1, 62.3] | 0.0 | [nan, nan] | 5.2 | [5.1, 5.4] | 36.3 | [34.4, 38.2] |
| AMSLAX | 89 | 42.8 | [38.5, 47.0] | 0.0 | [nan, nan] | 5.2 | [5.1, 5.3] | 36.7 | [35.4, 37.9] |

## Aircraft Type Analysis

| Aircraft | Flights | Avg Items | Items CI | Avg Weight | Weight CI | Avg Passengers | Passengers CI | Avg ULDs | ULDs CI |
|----------|---------|-----------|----------|------------|-----------|----------------|---------------|----------|----------|
| 789 | 71 | 77.8 | [69.1, 86.6] | 0.0 | [nan, nan] | 5.1 | [5.0, 5.1] | 30.9 | [30.1, 31.8] |
| 772 | 143 | 61.2 | [56.4, 66.0] | 0.0 | [nan, nan] | 5.1 | [5.1, 5.2] | 35.8 | [34.4, 37.2] |
| 781 | 174 | 46.2 | [42.5, 49.9] | 0.0 | [nan, nan] | 5.1 | [5.1, 5.2] | 37.2 | [35.4, 39.0] |
| 77W | 137 | 90.9 | [79.1, 102.7] | 0.0 | [nan, nan] | 7.1 | [7.1, 7.2] | 50.7 | [47.7, 53.8] |

## Monthly Analysis

| Month | Flights | Avg Items | Items CI | Avg Weight | Weight CI | Avg Passengers | Passengers CI | Avg ULDs | ULDs CI |
|-------|---------|-----------|----------|------------|-----------|----------------|---------------|----------|----------|
| FEB 2024 | 169 | 71.1 | [61.7, 80.5] | 0.0 | [nan, nan] | 5.6 | [5.4, 5.7] | 37.8 | [35.7, 39.8] |
| MAR 2024 | 183 | 72.3 | [66.9, 77.8] | 0.0 | [nan, nan] | 5.7 | [5.6, 5.8] | 41.3 | [38.8, 43.7] |
| JAN 2024 | 167 | 55.6 | [50.0, 61.1] | 0.0 | [nan, nan] | 5.6 | [5.5, 5.8] | 39.2 | [37.5, 41.0] |
| APR 2024 | 6 | 37.8 | [23.4, 52.2] | 0.0 | [nan, nan] | 6.0 | [4.8, 7.2] | 40.8 | [32.5, 49.2] |

## Key Statistical Insights

### Highest Variability: Cargo Items per Flight
- Standard Deviation: 46.85
- Coefficient of Variation: 70.7%
- 95% Confidence Interval: [62.2, 70.24]
- Mean 66.62

### Lowest Variability: Weight per Flight (kg)
- Standard Deviation: 0.0
- Coefficient of Variation: nan%
- 95% Confidence Interval: [nan, nan]

## Distribution Characteristics

### Cargo Items per Flight
- **Skewness:** 5.011 (Right-skewed)
- **Kurtosis:** 58.608 (Heavy-tailed)
- **Range:** 688
- **IQR:** 49.0

### Weight per Flight (kg)
- **Skewness:** nan (Approximately normal)
- **Kurtosis:** nan (Normal-tailed)
- **Range:** 0
- **IQR:** 0.0

### Volume per Flight (cubic meters)
- **Skewness:** nan (Approximately normal)
- **Kurtosis:** nan (Normal-tailed)
- **Range:** 0
- **IQR:** 0.0

### Passengers per Flight
- **Skewness:** 1.055 (Right-skewed)
- **Kurtosis:** -0.434 (Normal-tailed)
- **Range:** 3
- **IQR:** 2.0
- Mean 5

### ULDs per Flight
- **Skewness:** 3.582 (Right-skewed)
- **Kurtosis:** 20.539 (Heavy-tailed)
- **Range:** 146
- **IQR:** 13.0

### COL Items per Flight
- **Skewness:** nan (Approximately normal)
- **Kurtosis:** nan (Normal-tailed)
- **Range:** 0
- **IQR:** 0.0

### CRT Items per Flight
- **Skewness:** nan (Approximately normal)
- **Kurtosis:** nan (Normal-tailed)
- **Range:** 0athe 
- **IQR:** 0.0

## Files Generated

- `comprehensive_statistics.csv` - Overall statistical summary
- `route_statistical_analysis.csv` - Statistics by route
- `aircraft_statistical_analysis.csv` - Statistics by aircraft type
- `month_statistical_analysis.csv` - Statistics by month
- `statistical_analysis_report.md` - This comprehensive report


================================================================================
ANÁLISIS EXHAUSTIVO DE LOADLOCATIONSSPOTFIRE.CSV
================================================================================

✓ Datos cargados: 21911 registros, 22 columnas
✓ Columnas: ['FlightLoadId', 'FlightLegDepartureKey', 'DeadloadStatus', 'DeadloadOrigin', 'DeadloadDestination', 'Weight', 'WeightUnit', 'DeadloadType', 'DeadloadSubType', 'NumberOfItemsInUld', 'LoadType', 'SerialNumber', 'UldGrossWeight', 'UldTareWeight', 'ModTime', 'Hold', 'LoadLocation', 'Deck', 'LoadId', 'DeadloadId', 'SpecialCargoId', 'SpecialHandlingCode']

================================================================================
1. ESTRUCTURA DE LOS DATOS
================================================================================

Tipos de datos por columna:
FlightLoadId              object
FlightLegDepartureKey     object
DeadloadStatus            object
DeadloadOrigin            object
DeadloadDestination       object
Weight                     int64
WeightUnit                object
DeadloadType              object
DeadloadSubType           object
NumberOfItemsInUld       float64
LoadType                  object
SerialNumber              object
UldGrossWeight           float64
UldTareWeight            float64
ModTime                   object
Hold                      object
LoadLocation              object
Deck                      object
LoadId                     int64
DeadloadId                 int64
SpecialCargoId           float64
SpecialHandlingCode       object
dtype: object

Valores nulos por columna:
                     Nulls  Percentage
SpecialCargoId       15608       71.23
SpecialHandlingCode  15608       71.23
DeadloadSubType      10199       46.55
NumberOfItemsInUld    9300       42.44
SerialNumber          3521       16.07
UldGrossWeight        3521       16.07
UldTareWeight         3521       16.07

================================================================================
2. ANÁLISIS DE DEADLOADTYPE
================================================================================

Resumen por DeadloadType:
              Count  HasNumItems  HasSubType  ...  AvgWeight  TotalWeight  StdWeight
DeadloadType                                  ...                                   
B             11708        11708       11708  ...     283.12      3314788     274.39
C              8787           38           0  ...    1428.56     12552726     972.47
D               858          858           0  ...      79.41        68130      63.01
E                50            3           0  ...     739.80        36990    1593.96
M                24            0           0  ...      79.50         1908     131.97
X               484            4           4  ...       0.00            0       0.00

[6 rows x 8 columns]

--- DEADLOADTYPE B (Baggage) ---
Total: 11708 registros
SubTypes: {'Y': 4821, 'F': 2363, 'T': 2014, 'B': 1845, 'G': 665}
Promedio items por ULD: 15.91
Peso promedio: 283.12 KG

--- DEADLOADTYPE C (Cargo) ---
Total: 8787 registros
SubTypes únicos: 0
Con SpecialCargoId: 6186 (70.4%)
Peso promedio: 1428.56 KG
SpecialHandlingCodes: {'RFL': 753, 'RCM': 597, 'RMD': 594, 'ELI': 528, 'COL': 523, 'OHG': 428, 'CRT': 256, 'PES': 231, 'PEF': 223, 'AVG': 218}

--- DEADLOADTYPE D (?) ---
Total: 858 registros
SubTypes únicos: 0
Promedio items por ULD: 4.41
Peso promedio: 79.41 KG
Ejemplo SubTypes: {}

--- DEADLOADTYPE E (?) ---
Total: 50 registros
SubTypes únicos: 0
Con NumberOfItems: 3
Peso promedio: 739.80 KG
SubTypes: {}
Ejemplos de registros E:
     DeadloadType DeadloadSubType  NumberOfItemsInUld  Weight LoadType
228             E             NaN                 NaN      14      CBN
230             E             NaN                 NaN      20      CBN
270             E             NaN                 NaN       6      CBN
595             E             NaN                 NaN     480      ULD
885             E             NaN                 NaN      10      CBN
1063            E             NaN                 NaN     480      ULD
1064            E             NaN                 NaN      34      CBN
1318            E             NaN                 NaN       8      CBN
1390            E             NaN                 NaN       8      CBN
1842            E             NaN                 NaN      10      CBN

--- DEADLOADTYPE M (?) ---
Total: 24 registros
SubTypes únicos: 0
Peso promedio: 79.50 KG
SubTypes: {}
Ejemplos de registros M:
     DeadloadType DeadloadSubType  NumberOfItemsInUld  Weight LoadType
1728            M             NaN                 NaN      53      ULD
2608            M             NaN                 NaN     277      ULD
3168            M             NaN                 NaN     365      ULD
4286            M             NaN                 NaN       3      ULD
5097            M             NaN                 NaN      23      ULD

--- DEADLOADTYPE X (?) ---
Total: 484 registros
SubTypes únicos: 2
Peso promedio: 0.00 KG
SubTypes: {'Y': 3, 'T': 1}
Con NumberOfItems: 4
Ejemplos de registros X:
    DeadloadType DeadloadSubType  NumberOfItemsInUld  Weight LoadType
143            X             NaN                 NaN       0      ULD
144            X             NaN                 NaN       0      ULD
145            X             NaN                 NaN       0      ULD
146            X             NaN                 NaN       0      ULD
147            X             NaN                 NaN       0      ULD

================================================================================
3. ANÁLISIS DETALLADO DE DEADLOADSUBTYPE
================================================================================

SubTypes por DeadloadType:

B: {'Y': 4821, 'F': 2363, 'T': 2014, 'B': 1845, 'G': 665}

C: {}

D: {}

E: {}

M: {}

X: {'Y': 3, 'T': 1}

================================================================================
4. ANÁLISIS DE LOADTYPE
================================================================================

LoadType Analysis:
          Count  HasSerialNumber  AvgWeight  TotalWeight  AvgItems
LoadType                                                          
BLK        3487                2      38.32       133615      2.09
CBN          36                0      12.64          455       NaN
ULD       18388            18388     861.46     15840472     19.82

DeadloadType por LoadType:
DeadloadType     B     C    D   E   M    X
LoadType                                  
BLK           3283   152   44   3   5    0
CBN              0     3    0  33   0    0
ULD           8425  8632  814  14  19  484

================================================================================
5. ANÁLISIS DE HOLD (Compartimiento) Y DECK
================================================================================

Valores únicos de Hold:
Hold
AFT    10684
FWD     7704
BLK     3487
UNK       36
Name: count, dtype: int64

Valores únicos de Deck:
Deck
L    21875
X       36
Name: count, dtype: int64

Distribución de DeadloadType por Hold:
DeadloadType     B     C    D     E    M    X
Hold                                         
AFT           66.4  26.2  6.6   0.1  0.1  0.7
BLK           94.1   4.4  1.3   0.1  0.1  0.0
FWD           17.2  75.8  1.5   0.1  0.1  5.3
UNK            0.0   8.3  0.0  91.7  0.0  0.0

================================================================================
6. ANÁLISIS DE LOADLOCATION (Posiciones en el avión)
================================================================================

Total de LoadLocations únicas: 93

Top 20 LoadLocations más usadas:
LoadLocation
52     2102
51     1373
23P     839
41R     794
22P     772
21P     737
41L     722
42L     704
11P     703
42R     666
13P     600
31P     551
24P     513
33R     484
43L     472
33L     455
43R     448
32P     433
34R     415
34L     402
Name: count, dtype: int64

LoadLocations por Hold:
AFT: 39 posiciones - ['31', '31L', '31P', '31R', '32', '32L', '32P', '32R', '33', '33L']...
BLK: 3 posiciones - ['51', '52', '53']...
FWD: 43 posiciones - ['11', '11L', '11P', '11R', '12', '12L', '12P', '12R', '13', '13L']...
UNK: 8 posiciones - ['0', '0A', '0B', '0C', '0D', '0E', '0F', '0G']...

================================================================================
7. ANÁLISIS DE MODTIME (Modification Time)
================================================================================

ModTime único(s): 51
Valores de ModTime:
ModTime
16-2-2024 17:02:55    8562
13-2-2024 04:28:48    1733
1/4/2024 4:28          411
23-3-2024 04:28:06     377
8/3/2024 10:16         326
4/3/2024 4:35          323
17-3-2024 04:27:50     304
10/3/2024 4:27         295
16-3-2024 04:28:23     279
2/4/2024 4:30          277
26-2-2024 09:37:02     275
24-3-2024 04:27:17     274
18-3-2024 04:30:14     272
30-3-2024 04:27:14     272
25-3-2024 04:30:20     271
21-3-2024 04:27:31     270
13-3-2024 04:45:50     266
3/3/2024 4:29          263
12/3/2024 8:02         262
28-2-2024 04:32:05     257
28-3-2024 04:29:34     257
2/3/2024 4:29          254
15-3-2024 04:27:39     243
14-3-2024 04:27:57     243
5/3/2024 4:31          240
29-3-2024 04:28:19     239
26-3-2024 04:28:01     237
18-2-2024 04:38:59     234
20-2-2024 04:33:26     230
23-2-2024 04:31:52     230
22-3-2024 04:28:41     229
19-2-2024 04:29:20     217
25-2-2024 05:10:53     217
1/3/2024 4:30          216
24-2-2024 04:42:50     215
7/3/2024 4:46          210
21-2-2024 04:27:30     208
19-3-2024 04:33:58     207
16-2-2024 04:27:44     202
31-3-2024 04:27:23     196
22-2-2024 04:31:57     192
14-2-2024 04:27:47     186
6/3/2024 4:30          183
15-2-2024 04:27:26     182
29-2-2024 04:34:28     181
20-3-2024 04:28:06     175
9/3/2024 4:27          175
27-3-2024 04:30:20     174
27-2-2024 04:30:55     147
11/3/2024 4:29         143
17-2-2024 04:29:36      80
Name: count, dtype: int64

Interpretación: ModTime parece ser la fecha de extracción/modificación del reporte
No es la fecha del vuelo, sino cuándo se procesó la información

================================================================================
8. ANÁLISIS DE SPECIALHANDLINGCODE
================================================================================

Total de registros con SpecialHandlingCode: 6303

Top 20 códigos especiales:
SpecialHandlingCode
RFL    753
RCM    597
RMD    594
ELI    528
COL    523
OHG    428
CRT    256
PES    231
PEF    223
AVG    218
ELM    198
RNG    160
ICE    145
CLA    133
PIL    116
VAL    110
COI    105
REQ    100
ERT    100
RLI     69
Name: count, dtype: int64

Códigos identificados:
CRT: Critical (Crítico) - 256 registros
PIL: Perishable (Perecedero) - 116 registros
ELI: Electronics (Electrónicos) - 528 registros
MAG: Magnetic (Magnético) - 39 registros
ERT: Emergency/Urgente - 100 registros
OHG: Overheight (Sobrepeso altura) - 428 registros
RMD: Radioactive Material Dangerous - 594 registros
RFL: Restricted Flight Load - 753 registros
COL: Cool (Refrigerado) - 523 registros
VAL: Valuable (Valioso) - 110 registros

================================================================================
9. ANÁLISIS DE PESOS
================================================================================

Estadísticas de Weight (Peso neto):
count    21911.000000
mean       729.064945
std        869.793675
min          0.000000
25%         59.000000
50%        490.000000
75%        979.000000
max       5375.000000
Name: Weight, dtype: float64

Estadísticas de UldGrossWeight (Peso bruto ULD):
count    18390.000000
mean      1066.009244
std        830.959932
min         57.000000
25%        628.000000
50%        756.000000
75%       1300.000000
max       5500.000000
Name: UldGrossWeight, dtype: float64

Estadísticas de UldTareWeight (Peso del contenedor vacío):
count    18390.000000
mean        81.575095
std         46.003618
min          1.000000
25%         57.000000
50%         57.000000
75%        110.000000
max       1213.000000
Name: UldTareWeight, dtype: float64

Verificación: UldGrossWeight = Weight + UldTareWeight
Registros donde la fórmula se cumple (diff < 1 kg): 11735 / 21911
Promedio de diferencia: 123.07 kg

================================================================================
10. ANÁLISIS DE SISTEMA DE IDs
================================================================================

LoadIds únicos: 14885
DeadloadIds únicos: 18636
SpecialCargoIds únicos: 6303

Jerarquía de IDs:
- 1 LoadId puede tener múltiples DeadloadIds (diferentes tipos de carga en el mismo ULD)
- 1 DeadloadId puede tener múltiples SpecialCargoIds (múltiples tipos de carga especial)

Ejemplo - LoadId 152243415:
       LoadId  DeadloadId  ...  Weight SpecialHandlingCode
22  152243415   159844314  ...     865                 CRT

[1 rows x 6 columns]

================================================================================
11. ANÁLISIS DE RUTAS (DeadloadOrigin -> DeadloadDestination)
================================================================================

Top 20 rutas más frecuentes:
Route
AMS->DEL    4792
AMS->LAX    3376
AMS->SIN    3321
AMS->ICN    2829
AMS->IAH    2563
AMS->SFO    2014
AMS->BLR    1956
AMS->DPS    1060
Name: count, dtype: int64

Origen único(s):
DeadloadOrigin
AMS    21911
Name: count, dtype: int64

Top destinos:
DeadloadDestination
DEL    4792
LAX    3376
SIN    3321
ICN    2829
IAH    2563
SFO    2014
BLR    1956
DPS    1060
Name: count, dtype: int64

================================================================================
12. PATRONES Y CORRELACIONES
================================================================================

Correlación Weight vs NumberOfItemsInUld (para Baggage): 0.996
Peso promedio por item de equipaje: 17.79 kg

Top 10 tipos de ULD más usados:
SerialNumber
AKE    11284
PMC     5650
PAG     1149
PLB      147
RKN       60
AAP       34
AKY       31
RAP       14
PLA        9
P1P        7
Name: count, dtype: int64

================================================================================
13. ANÁLISIS DE DEADLOADSTATUS
================================================================================

Valores de DeadloadStatus:
DeadloadStatus
ACTIVE    21911
Name: count, dtype: int64

Interpretación: ACTIVE = carga confirmada y activa en el vuelo

================================================================================
14. RESUMEN Y DEFINICIONES
================================================================================

DEFINICIONES DE COLUMNAS:
========================

1. FlightLoadId: ID compuesto del registro (Fecha|Origen|Aerolínea|Vuelo||Fecha|D|LoadId|DeadloadId[|SpecialCargoId])
2. FlightLegDepartureKey: Identificador del leg de vuelo
3. DeadloadStatus: Estado de la carga (ACTIVE = confirmada)
4. DeadloadOrigin: Aeropuerto de origen (siempre AMS en este dataset)
5. DeadloadDestination: Aeropuerto de destino
6. Weight: Peso neto de la carga (sin contenedor)
7. WeightUnit: Unidad de peso (KG)
8. DeadloadType: Tipo de carga
   - B: Baggage (Equipaje) - tiene NumberOfItems, tiene SubType
   - C: Cargo (Carga comercial) - NO tiene NumberOfItems, a veces SpecialCargoId
   - D: Probablemente "Deadload" o carga especial/extra - tiene NumberOfItems
   - E: Tipo especial (50 registros) - análisis sugiere carga especial
   - M: Posiblemente "Mail" (Correo) - 24 registros
   - X: Tipo especial (484 registros) - necesita más análisis
9. DeadloadSubType: Subtipo dentro de cada categoría
   - B: Y(economy), F(first), T(transfer), B(business), G(?)
   - C: vacío (carga comercial sin clasificación por clase)
   - D, E, M, X: varios
10. NumberOfItemsInUld: Cantidad de piezas (solo para tipos que se cuentan por unidad)
11. LoadType: Tipo de contenedor
    - ULD: Unit Load Device (contenedor certificado)
    - BLK: Bulk (carga suelta, sin contenedor)
12. SerialNumber: Número de serie del ULD (ej: AKE96367KL)
13. UldGrossWeight: Peso bruto total (carga + contenedor)
14. UldTareWeight: Peso del contenedor vacío
15. ModTime: Fecha de modificación/extracción del reporte
16. Hold: Compartimiento del avión
    - FWD: Forward (delantero)
    - AFT: Aft (trasero)
    - BLK: Bulk (zona de carga suelta)
17. LoadLocation: Posición específica en el avión (ej: 41R, 21P)
18. Deck: Cubierta (L = Lower deck, cubierta inferior de carga)
19. LoadId: ID del contenedor/ULD físico
20. DeadloadId: ID del registro de carga dentro del contenedor
21. SpecialCargoId: ID adicional para carga especial (múltiples por DeadloadId)
22. SpecialHandlingCode: Código de manejo especial (CRT, PIL, ELI, MAG, etc.)

JERARQUÍA DE IDs:
=================
LoadId (ULD físico)
  └── DeadloadId (tipo de carga en el ULD)
        └── SpecialCargoId (items especiales individuales) [opcional]

TIPOS DE CARGA ESPECIAL:
========================
CRT: Critical/Critters (animales vivos)
PIL: Perishable (perecederos - requieren temperatura)
ELI: Electronics (electrónicos - sensibles)
MAG: Magnetic (magnéticos - separación especial)
ERT: Emergency/Urgent
OHG: Overheight (altura excesiva)
RMD: Radioactive Material Dangerous
COL: Cool (refrigerado)
HEA: Heavy (pesado - requiere refuerzos)
VAL: Valuable (valioso - seguridad extra)


================================================================================
ANÁLISIS COMPLETADO
================================================================================
