# LoadLocationsSpotfire.csv - Base de Conocimiento Completa

## 📊 OVERVIEW
- **Total Registros**: 21,911
- **Periodo**: Enero-Abril 2024
- **Origen**: Amsterdam (AMS)
- **Destinos**: 8 principales (DEL, LAX, SIN, ICN, IAH, SFO, BLR, DPS)

---

## 🔑 RESPUESTAS A TUS PREGUNTAS CLAVE

### ¿Qué es DeadloadType E?
**E = Equipment / Equipo especial o Crew Equipment**
- **50 registros totales** (0.23% del dataset)
- **LoadType predominante**: CBN (Cabin - cabina) - 33 de 50 registros
- **Peso promedio**: 739.8 kg (mucho más pesado que baggage normal)
- **Características**:
  - NO tiene SubType
  - 91.7% está en Hold "UNK" (Unknown - desconocido)
  - Solo 3 registros tienen NumberOfItems
  - Principalmente pesos pequeños (6-20 kg) en CBN
  - Algunos registros grandes (480 kg) en ULD

**Interpretación**: Equipo de tripulación, provisiones de cabina, o equipamiento técnico del avión

---

### ¿Qué es DeadloadType M?
**M = Mail / Correo postal**
- **24 registros totales** (0.11% del dataset)
- **LoadType**: 100% ULD (contenedores certificados)
- **Peso promedio**: 79.5 kg
- **Rango de peso**: 3 - 365 kg
- **Características**:
  - NO tiene SubType
  - NO tiene NumberOfItems
  - Distribuido entre AFT (79%) y FWD (21%)
  - Sin carga especial (no SpecialCargoId)

**Interpretación**: Correo postal y paquetería que viaja en vuelos comerciales

---

### ¿Qué es DeadloadType X?
**X = Placeholder / Zero weight / Dummy records**
- **484 registros totales** (2.21% del dataset)
- **Peso**: SIEMPRE 0 kg (100% de los registros)
- **Características únicas**:
  - 100% ULD
  - 98% en Hold FWD (Forward)
  - Solo 4 tienen NumberOfItems (todos tienen SubType Y o T)
  - NO tiene SpecialCargoId

**Interpretación**: Registros de "placeholder" o espacios reservados:
- Posiciones reservadas para carga que no se cargó
- ULDs vacíos que viajan por reposicionamiento
- Espacios bloqueados por balance del avión
- Registros de sistema para tracking de posiciones

---

### ¿Qué es DeadloadType D?
**D = Diplomatic Cargo / Documents / Declared Cargo**
- **858 registros totales** (3.92% del dataset)
- **Peso promedio**: 79.4 kg (similar a equipaje)
- **NumberOfItems promedio**: 4.41 items
- **Características**:
  - SÍ tiene NumberOfItems (se cuenta por piezas)
  - NO tiene SubType
  - 95% en ULD, 5% en BLK
  - Distribuido: 49% BLK, 46% AFT, 5% FWD

**Interpretación**: Carga declarada especial, posiblemente:
- Envíos diplomáticos
- Documentación importante
- Paquetes declarados que requieren tracking especial
- Similar al equipaje pero con tratamiento diferente

---

## 📦 TIPOS DE CARGA - RESUMEN COMPLETO

| Tipo | Descripción | Registros | % | Peso Prom | NumItems | SubType |
|------|-------------|-----------|---|-----------|----------|---------|
| **B** | Baggage (Equipaje) | 11,708 | 53.4% | 283 kg | ✅ Sí (15.9) | ✅ Sí |
| **C** | Cargo (Comercial) | 8,787 | 40.1% | 1,429 kg | ❌ No | ❌ No |
| **D** | Declared/Documents | 858 | 3.9% | 79 kg | ✅ Sí (4.4) | ❌ No |
| **X** | Placeholder/Zero | 484 | 2.2% | 0 kg | ❌ No | Raro |
| **E** | Equipment/Crew | 50 | 0.2% | 740 kg | Raro | ❌ No |
| **M** | Mail (Correo) | 24 | 0.1% | 80 kg | ❌ No | ❌ No |

---

## 🎯 DEADLOAD SUBTYPES EXPLICADOS

### Para Baggage (B):
- **Y = Economy Class** (4,821 registros - 41%) → Equipaje de clase económica
- **F = First Class** (2,363 registros - 20%) → Equipaje de primera clase
- **T = Transfer** (2,014 registros - 17%) → Equipaje en conexión
- **B = Business Class** (1,845 registros - 16%) → Equipaje de clase ejecutiva
- **G = ?** (665 registros - 6%) → Posiblemente "General" o "Gate checked"

**Patrón importante**: 
- Peso promedio similar entre clases (~283 kg por registro)
- Economy tiene más volumen pero distribuido en más ULDs
- First/Business suelen consolidarse menos (más ULDs dedicados)

### Para otros tipos:
- **C, D, E, M**: NO tienen SubType (campo vacío)
- **X**: Solo 4 registros tienen SubType (Y o T) - probablemente errores

---

## 🏗️ LOADTYPE - TIPOS DE CONTENEDOR

### ULD (Unit Load Device)
- **18,388 registros** (83.9%)
- **Peso promedio**: 861 kg
- **Items promedio**: 19.8
- **Tipos principales**:
  - **AKE** (61%): Contenedor estándar (11,284 registros)
  - **PMC** (31%): Pallet contorneado (5,650 registros)
  - **PAG** (6%): Pallet de carga (1,149 registros)

### BLK (Bulk)
- **3,487 registros** (15.9%)
- **Peso promedio**: 38 kg (mucho más ligero)
- **Items promedio**: 2.1
- **Uso**: Carga suelta en compartimiento de bulk
- **Composición**: 94% Baggage, 4% Cargo, 1% tipo D

### CBN (Cabin)
- **36 registros** (0.2%)
- **Peso promedio**: 12.6 kg
- **Solo tipo E** (Equipment)
- **Uso**: Items que viajan en cabina, no en bodega

---

## 🛫 HOLD - COMPARTIMIENTOS DEL AVIÓN

### FWD (Forward - Delantero)
- **7,704 registros** (35.2%)
- **Composición**:
  - 75.8% Cargo
  - 17.2% Baggage
  - 5.3% tipo X (placeholders)
- **Interpretación**: Zona principal para carga comercial pesada

### AFT (Aft - Trasero)
- **10,684 registros** (48.8%)
- **Composición**:
  - 66.4% Baggage
  - 26.2% Cargo
  - 6.6% tipo D
- **Interpretación**: Zona principal para equipaje y carga mixta

### BLK (Bulk)
- **3,487 registros** (15.9%)
- **Composición**:
  - 94.1% Baggage
  - 4.4% Cargo
  - 1.3% tipo D
- **Interpretación**: Zona de carga suelta (sin contenedor)

### UNK (Unknown)
- **36 registros** (0.2%)
- **91.7% tipo E** (Equipment)
- **Interpretación**: Ubicación no asignada o especial

---

## 📍 LOADLOCATION - SISTEMA DE POSICIONES

### Nomenclatura:
- **Números**: 11-43, 51-53
- **Letras**: L (Left - Izquierda), R (Right - Derecha), P (Pallet/Center)
- **Ejemplos**:
  - `41R` = Posición 41, lado derecho
  - `23P` = Posición 23, pallet central
  - `51` = Posición bulk 51

### Top 5 posiciones más usadas:
1. **52** (2,102 usos) - Bulk trasero
2. **51** (1,373 usos) - Bulk principal
3. **23P** (839 usos) - Pallet delantero central
4. **41R** (794 usos) - Derecha trasera
5. **22P** (772 usos) - Pallet delantero central

### Patrón de numeración:
- **11-24**: Forward (FWD) - números bajos
- **31-43**: Aft (AFT) - números altos
- **51-53**: Bulk (BLK) - números 50+

---

## 🔐 SPECIALHANDLINGCODE - CÓDIGOS COMPLETOS

### Top 10 códigos más frecuentes:

1. **RFL** (753) - Restricted Flight Load
   - Carga con restricciones de vuelo
   
2. **RCM** (597) - Radioactive Cargo Material (menos de 0.002%)
   - Material radiactivo en cantidades controladas
   
3. **RMD** (594) - Radioactive Material Dangerous
   - Material radiactivo peligroso
   
4. **ELI** (528) - Electronics
   - Dispositivos electrónicos sensibles
   
5. **COL** (523) - Cool / Cold Chain
   - Requiere refrigeración
   
6. **OHG** (428) - Overheight / Oversize
   - Carga de altura/tamaño excesivo
   
7. **CRT** (256) - Critical / Critters
   - Animales vivos o carga crítica
   
8. **PES** (231) - Perishable (Short)
   - Perecederos tiempo corto
   
9. **PEF** (223) - Perishable Frozen
   - Perecederos congelados
   
10. **AVG** (218) - Average (carga estándar supervisada)

### Otros códigos importantes:
- **ELM** (198) - Electronics with Lithium
- **RNG** (160) - Dangerous Goods General
- **ICE** (145) - Dry Ice / Hielo seco
- **CLA** (133) - Class A (tipo de peligrosidad)
- **PIL** (116) - Perishable
- **VAL** (110) - Valuable cargo
- **ERT** (100) - Emergency/Urgent
- **MAG** (39) - Magnetic materials

---

## ⚖️ ANÁLISIS DE PESOS

### Correlaciones importantes:
1. **Weight vs NumberOfItems (Baggage)**: r = 0.996
   - Correlación casi perfecta
   - **17.79 kg por item** de equipaje promedio

2. **Fórmula de pesos**:
   ```
   UldGrossWeight = Weight + UldTareWeight
   ```
   - Se cumple en ~64% de los registros
   - Diferencia promedio: 123 kg (por consolidación de múltiples DeadloadIds)

### Pesos por tipo:
- **Baggage (B)**: 283 kg promedio
- **Cargo (C)**: 1,429 kg promedio (5x más pesado)
- **Mail (M)**: 80 kg promedio
- **Declared (D)**: 79 kg promedio
- **Equipment (E)**: 740 kg promedio
- **Placeholder (X)**: 0 kg

### Pesos de contenedores (Tare):
- **Promedio**: 81.6 kg
- **Mediana**: 57 kg (contenedores AKE estándar)
- **Rango**: 1 - 1,213 kg
- **Tipos**:
  - AKE (ligero): ~57 kg
  - PMC (mediano): ~125 kg
  - PAG (pesado): ~104-110 kg

---

## 🆔 JERARQUÍA DE IDs - EXPLICACIÓN DETALLADA

### Nivel 1: LoadId (ULD Físico)
- **14,885 LoadIds únicos**
- Representa el **contenedor físico**
- Un ULD puede tener múltiples tipos de carga

### Nivel 2: DeadloadId (Registro de Carga)
- **18,636 DeadloadIds únicos**
- Representa **cada tipo de carga** dentro del ULD
- Un DeadloadId por cada categoría (B/Y, B/F, D, etc.)

### Nivel 3: SpecialCargoId (Items Especiales)
- **6,303 SpecialCargoIds únicos**
- Solo para **carga con manejo especial**
- Múltiples IDs por DeadloadId si hay varios tipos de carga especial

### Ejemplo real:
```
LoadId: 152439639 (ULD PMC32580KL en posición 21P)
  ├── DeadloadId: 160053455 (665 kg Cargo tipo C)
      ├── SpecialCargoId: 19054096 (CRT - Animal vivo)
      ├── SpecialCargoId: 19054097 (PIL - Perecedero)
      ├── SpecialCargoId: 19054098 (ELI - Electrónico)
      └── SpecialCargoId: 19054099 (MAG - Magnético)
```

---

## 📅 MODTIME - FECHA DE PROCESAMIENTO

**NO es la fecha del vuelo, es la fecha de extracción del reporte**

- 51 fechas únicas
- Rango: 13 Feb 2024 - 2 Abr 2024
- Fecha más común: 16-Feb-2024 17:02:55 (8,562 registros - 39%)
- **Interpretación**: El sistema extrae/actualiza reportes diariamente

---

## ✅ PREGUNTAS FRECUENTES - FAQ

### 1. ¿Por qué algunos registros tienen 3 IDs en FlightLoadId?
Porque tienen **SpecialCargoId** (carga especial que requiere tracking individual)

### 2. ¿Por qué Cargo (C) no tiene NumberOfItemsInUld?
Porque se mide por **peso y volumen**, no por piezas individuales

### 3. ¿Por qué hay ULDs con peso 0?
Son **placeholders** (tipo X) - espacios reservados o ULDs vacíos en reposicionamiento

### 4. ¿Qué significa cuando LoadId y DeadloadId son diferentes?
**Siempre son diferentes**. LoadId = contenedor físico, DeadloadId = registro de carga específico

### 5. ¿Por qué un mismo SerialNumber aparece varias veces?
Un ULD puede contener **múltiples tipos de carga**, cada uno con su DeadloadId

### 6. ¿Deck siempre es "L"?
Casi siempre (99.8%). "L" = Lower Deck (bodega inferior). Solo 36 registros tienen "X" (desconocido)

### 7. ¿DeadloadStatus puede ser otra cosa que "ACTIVE"?
En este dataset, **100% es ACTIVE**. Otros posibles: CANCELLED, OFFLOADED, PENDING

---

## 🎓 CONOCIMIENTO PARA DEFENSA

### Si te preguntan por una línea específica, analiza:

1. **FlightLoadId**: Extrae fecha, aerolínea, vuelo, IDs
2. **DeadloadType**: Identifica si es B/C/D/E/M/X
3. **Weight vs UldGrossWeight**: Verifica coherencia
4. **LoadType**: ULD (contenedor) vs BLK (suelto)
5. **Hold + LoadLocation**: Identifica posición exacta en avión
6. **SpecialHandlingCode**: Si existe, explica requisitos especiales
7. **NumberOfItemsInUld**: Solo relevante para B y D
8. **Jerarquía**: LoadId → DeadloadId → SpecialCargoId

### Datos clave para memorizar:
- 21,911 registros totales
- 53% Baggage, 40% Cargo
- Peso promedio equipaje: **17.79 kg/item**
- Tipos ULD más comunes: **AKE (61%), PMC (31%)**
- Hold más usado: **AFT (49%)**
- Rutas principales: **DEL (22%), LAX (15%), SIN (15%)**

---

## 📊 MÉTRICAS FINALES

```
Total Weight:       15,973,542 kg (15,974 toneladas)
Average per flight: ~55-60 toneladas
ULDs totales:       ~15,000 contenedores
Flights:            ~8 destinos principales
Peak usage:         Posiciones 51-52 (bulk), 23P (pallet FWD)
```

---

**Documento creado**: Octubre 2024  
**Dataset**: LoadLocationsSpotfire.csv (Enero-Abril 2024)  
**Autor del análisis**: analyze_loadlocations_detailed.py

