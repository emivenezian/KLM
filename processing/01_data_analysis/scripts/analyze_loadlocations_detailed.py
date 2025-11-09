"""
Análisis Exhaustivo de LoadLocationsSpotfire.csv
Objetivo: Entender cada campo, relaciones y patrones en la base de datos
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# Configurar visualización
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Cargar datos
print("="*80)
print("ANÁLISIS EXHAUSTIVO DE LOADLOCATIONSSPOTFIRE.CSV")
print("="*80)

df = pd.read_csv('Inputfiles/LoadLocationsSpotfire.csv')
print(f"\n✓ Datos cargados: {len(df)} registros, {len(df.columns)} columnas")
print(f"✓ Columnas: {list(df.columns)}")

# ============================================================================
# 1. ESTRUCTURA Y TIPOS DE DATOS
# ============================================================================
print("\n" + "="*80)
print("1. ESTRUCTURA DE LOS DATOS")
print("="*80)

print("\nTipos de datos por columna:")
print(df.dtypes)

print("\nValores nulos por columna:")
null_counts = df.isnull().sum()
null_percentages = (null_counts / len(df) * 100).round(2)
null_df = pd.DataFrame({
    'Nulls': null_counts,
    'Percentage': null_percentages
})
print(null_df[null_df['Nulls'] > 0].sort_values('Nulls', ascending=False))

# ============================================================================
# 2. ANÁLISIS DE DEADLOADTYPE (B, C, D, E, M, X)
# ============================================================================
print("\n" + "="*80)
print("2. ANÁLISIS DE DEADLOADTYPE")
print("="*80)

deadload_analysis = df.groupby('DeadloadType').agg({
    'DeadloadType': 'count',
    'NumberOfItemsInUld': lambda x: x.notna().sum(),
    'DeadloadSubType': lambda x: x.notna().sum(),
    'SpecialCargoId': lambda x: x.notna().sum(),
    'SpecialHandlingCode': lambda x: x.notna().sum(),
    'Weight': ['mean', 'sum', 'std']
}).round(2)

deadload_analysis.columns = ['Count', 'HasNumItems', 'HasSubType', 'HasSpecialCargoId', 
                               'HasSpecialHandling', 'AvgWeight', 'TotalWeight', 'StdWeight']
print("\nResumen por DeadloadType:")
print(deadload_analysis)

# Análisis detallado por tipo
print("\n--- DEADLOADTYPE B (Baggage) ---")
b_data = df[df['DeadloadType'] == 'B']
print(f"Total: {len(b_data)} registros")
print(f"SubTypes: {b_data['DeadloadSubType'].value_counts().to_dict()}")
print(f"Promedio items por ULD: {b_data['NumberOfItemsInUld'].mean():.2f}")
print(f"Peso promedio: {b_data['Weight'].mean():.2f} KG")

print("\n--- DEADLOADTYPE C (Cargo) ---")
c_data = df[df['DeadloadType'] == 'C']
print(f"Total: {len(c_data)} registros")
print(f"SubTypes únicos: {c_data['DeadloadSubType'].nunique()}")
print(f"Con SpecialCargoId: {c_data['SpecialCargoId'].notna().sum()} ({c_data['SpecialCargoId'].notna().sum()/len(c_data)*100:.1f}%)")
print(f"Peso promedio: {c_data['Weight'].mean():.2f} KG")
print(f"SpecialHandlingCodes: {c_data['SpecialHandlingCode'].value_counts().head(10).to_dict()}")

print("\n--- DEADLOADTYPE D (?) ---")
d_data = df[df['DeadloadType'] == 'D']
print(f"Total: {len(d_data)} registros")
print(f"SubTypes únicos: {d_data['DeadloadSubType'].nunique()}")
print(f"Promedio items por ULD: {d_data['NumberOfItemsInUld'].mean():.2f}")
print(f"Peso promedio: {d_data['Weight'].mean():.2f} KG")
print(f"Ejemplo SubTypes: {d_data['DeadloadSubType'].value_counts().head().to_dict()}")

print("\n--- DEADLOADTYPE E (?) ---")
e_data = df[df['DeadloadType'] == 'E']
print(f"Total: {len(e_data)} registros")
print(f"SubTypes únicos: {e_data['DeadloadSubType'].nunique()}")
print(f"Con NumberOfItems: {e_data['NumberOfItemsInUld'].notna().sum()}")
print(f"Peso promedio: {e_data['Weight'].mean():.2f} KG")
print(f"SubTypes: {e_data['DeadloadSubType'].value_counts().to_dict()}")
print(f"Ejemplos de registros E:")
print(e_data[['DeadloadType', 'DeadloadSubType', 'NumberOfItemsInUld', 'Weight', 'LoadType']].head(10))

print("\n--- DEADLOADTYPE M (?) ---")
m_data = df[df['DeadloadType'] == 'M']
print(f"Total: {len(m_data)} registros")
print(f"SubTypes únicos: {m_data['DeadloadSubType'].nunique()}")
print(f"Peso promedio: {m_data['Weight'].mean():.2f} KG")
print(f"SubTypes: {m_data['DeadloadSubType'].value_counts().to_dict()}")
print(f"Ejemplos de registros M:")
print(m_data[['DeadloadType', 'DeadloadSubType', 'NumberOfItemsInUld', 'Weight', 'LoadType']].head())

print("\n--- DEADLOADTYPE X (?) ---")
x_data = df[df['DeadloadType'] == 'X']
print(f"Total: {len(x_data)} registros")
print(f"SubTypes únicos: {x_data['DeadloadSubType'].nunique()}")
print(f"Peso promedio: {x_data['Weight'].mean():.2f} KG")
print(f"SubTypes: {x_data['DeadloadSubType'].value_counts().head(10).to_dict()}")
print(f"Con NumberOfItems: {x_data['NumberOfItemsInUld'].notna().sum()}")
print(f"Ejemplos de registros X:")
print(x_data[['DeadloadType', 'DeadloadSubType', 'NumberOfItemsInUld', 'Weight', 'LoadType']].head())

# ============================================================================
# 3. ANÁLISIS DE DEADLOADSUBTYPE
# ============================================================================
print("\n" + "="*80)
print("3. ANÁLISIS DETALLADO DE DEADLOADSUBTYPE")
print("="*80)

print("\nSubTypes por DeadloadType:")
for dtype in ['B', 'C', 'D', 'E', 'M', 'X']:
    data = df[df['DeadloadType'] == dtype]
    if len(data) > 0:
        print(f"\n{dtype}: {data['DeadloadSubType'].value_counts().to_dict()}")

# ============================================================================
# 4. ANÁLISIS DE LOADTYPE (ULD vs BLK)
# ============================================================================
print("\n" + "="*80)
print("4. ANÁLISIS DE LOADTYPE")
print("="*80)

loadtype_analysis = df.groupby('LoadType').agg({
    'LoadType': 'count',
    'SerialNumber': lambda x: x.notna().sum(),
    'Weight': ['mean', 'sum'],
    'NumberOfItemsInUld': 'mean'
}).round(2)
loadtype_analysis.columns = ['Count', 'HasSerialNumber', 'AvgWeight', 'TotalWeight', 'AvgItems']
print("\nLoadType Analysis:")
print(loadtype_analysis)

print("\nDeadloadType por LoadType:")
print(pd.crosstab(df['LoadType'], df['DeadloadType']))

# ============================================================================
# 5. ANÁLISIS DE HOLD Y DECK
# ============================================================================
print("\n" + "="*80)
print("5. ANÁLISIS DE HOLD (Compartimiento) Y DECK")
print("="*80)

print("\nValores únicos de Hold:")
print(df['Hold'].value_counts())

print("\nValores únicos de Deck:")
print(df['Deck'].value_counts())

print("\nDistribución de DeadloadType por Hold:")
hold_deadload = pd.crosstab(df['Hold'], df['DeadloadType'], normalize='index') * 100
print(hold_deadload.round(1))

# ============================================================================
# 6. ANÁLISIS DE LOADLOCATION
# ============================================================================
print("\n" + "="*80)
print("6. ANÁLISIS DE LOADLOCATION (Posiciones en el avión)")
print("="*80)

print(f"\nTotal de LoadLocations únicas: {df['LoadLocation'].nunique()}")
print("\nTop 20 LoadLocations más usadas:")
print(df['LoadLocation'].value_counts().head(20))

# Análisis por compartimiento
print("\nLoadLocations por Hold:")
for hold in df['Hold'].unique():
    if pd.notna(hold):
        locs = df[df['Hold'] == hold]['LoadLocation'].unique()
        print(f"{hold}: {len(locs)} posiciones - {sorted(locs)[:10]}...")

# ============================================================================
# 7. ANÁLISIS DE MODTIME
# ============================================================================
print("\n" + "="*80)
print("7. ANÁLISIS DE MODTIME (Modification Time)")
print("="*80)

df['ModTime_parsed'] = pd.to_datetime(df['ModTime'], format='%d-%m-%Y %H:%M:%S', errors='coerce')
print(f"\nModTime único(s): {df['ModTime'].nunique()}")
print(f"Valores de ModTime:")
print(df['ModTime'].value_counts())

print("\nInterpretación: ModTime parece ser la fecha de extracción/modificación del reporte")
print("No es la fecha del vuelo, sino cuándo se procesó la información")

# ============================================================================
# 8. ANÁLISIS DE SPECIALCARGOCODE
# ============================================================================
print("\n" + "="*80)
print("8. ANÁLISIS DE SPECIALHANDLINGCODE")
print("="*80)

print(f"\nTotal de registros con SpecialHandlingCode: {df['SpecialHandlingCode'].notna().sum()}")
print("\nTop 20 códigos especiales:")
print(df['SpecialHandlingCode'].value_counts().head(20))

# Diccionario de códigos conocidos
special_codes = {
    'CRT': 'Critical (Crítico)',
    'PIL': 'Perishable (Perecedero)',
    'ELI': 'Electronics (Electrónicos)',
    'MAG': 'Magnetic (Magnético)',
    'ERT': 'Emergency/Urgente',
    'OHG': 'Overheight (Sobrepeso altura)',
    'RMD': 'Radioactive Material Dangerous',
    'RFL': 'Restricted Flight Load',
    'COL': 'Cool (Refrigerado)',
    'HEA': 'Heavy (Pesado)',
    'VAL': 'Valuable (Valioso)',
    'DGR': 'Dangerous Goods Radioactive'
}

print("\nCódigos identificados:")
for code, description in special_codes.items():
    count = (df['SpecialHandlingCode'] == code).sum()
    if count > 0:
        print(f"{code}: {description} - {count} registros")

# ============================================================================
# 9. ANÁLISIS DE PESOS Y ULD
# ============================================================================
print("\n" + "="*80)
print("9. ANÁLISIS DE PESOS")
print("="*80)

print("\nEstadísticas de Weight (Peso neto):")
print(df['Weight'].describe())

print("\nEstadísticas de UldGrossWeight (Peso bruto ULD):")
print(df['UldGrossWeight'].describe())

print("\nEstadísticas de UldTareWeight (Peso del contenedor vacío):")
print(df['UldTareWeight'].describe())

# Verificar la fórmula: GrossWeight = Weight + TareWeight
df['WeightCheck'] = df['UldGrossWeight'] - df['UldTareWeight']
df['WeightDiff'] = abs(df['WeightCheck'] - df['Weight'])

print(f"\nVerificación: UldGrossWeight = Weight + UldTareWeight")
print(f"Registros donde la fórmula se cumple (diff < 1 kg): {(df['WeightDiff'] < 1).sum()} / {len(df)}")
print(f"Promedio de diferencia: {df['WeightDiff'].mean():.2f} kg")

# ============================================================================
# 10. ANÁLISIS DE IDs (LoadId, DeadloadId, SpecialCargoId)
# ============================================================================
print("\n" + "="*80)
print("10. ANÁLISIS DE SISTEMA DE IDs")
print("="*80)

print(f"\nLoadIds únicos: {df['LoadId'].nunique()}")
print(f"DeadloadIds únicos: {df['DeadloadId'].nunique()}")
print(f"SpecialCargoIds únicos: {df['SpecialCargoId'].nunique()}")

# Analizar jerarquía
print("\nJerarquía de IDs:")
print("- 1 LoadId puede tener múltiples DeadloadIds (diferentes tipos de carga en el mismo ULD)")
print("- 1 DeadloadId puede tener múltiples SpecialCargoIds (múltiples tipos de carga especial)")

# Ejemplo de jerarquía
sample_loadid = df[df['SpecialCargoId'].notna()]['LoadId'].iloc[0]
print(f"\nEjemplo - LoadId {sample_loadid}:")
example = df[df['LoadId'] == sample_loadid][['LoadId', 'DeadloadId', 'SpecialCargoId', 
                                               'SerialNumber', 'Weight', 'SpecialHandlingCode']]
print(example)

# ============================================================================
# 11. ANÁLISIS DE RUTAS
# ============================================================================
print("\n" + "="*80)
print("11. ANÁLISIS DE RUTAS (DeadloadOrigin -> DeadloadDestination)")
print("="*80)

df['Route'] = df['DeadloadOrigin'] + '->' + df['DeadloadDestination']
print("\nTop 20 rutas más frecuentes:")
print(df['Route'].value_counts().head(20))

print("\nOrigen único(s):")
print(df['DeadloadOrigin'].value_counts())

print("\nTop destinos:")
print(df['DeadloadDestination'].value_counts().head(20))

# ============================================================================
# 12. PATRONES Y CORRELACIONES
# ============================================================================
print("\n" + "="*80)
print("12. PATRONES Y CORRELACIONES")
print("="*80)

# Correlación entre peso y número de items
baggage_data = df[df['DeadloadType'] == 'B'].copy()
if len(baggage_data) > 0:
    correlation = baggage_data['Weight'].corr(baggage_data['NumberOfItemsInUld'])
    print(f"\nCorrelación Weight vs NumberOfItemsInUld (para Baggage): {correlation:.3f}")
    
    avg_weight_per_item = baggage_data['Weight'].sum() / baggage_data['NumberOfItemsInUld'].sum()
    print(f"Peso promedio por item de equipaje: {avg_weight_per_item:.2f} kg")

# Análisis de ULDs más comunes
print("\nTop 10 tipos de ULD más usados:")
uld_types = df[df['SerialNumber'].notna()]['SerialNumber'].apply(lambda x: x[:3])
print(uld_types.value_counts().head(10))

# ============================================================================
# 13. DEADLOADSTATUS
# ============================================================================
print("\n" + "="*80)
print("13. ANÁLISIS DE DEADLOADSTATUS")
print("="*80)

print("\nValores de DeadloadStatus:")
print(df['DeadloadStatus'].value_counts())

print("\nInterpretación: ACTIVE = carga confirmada y activa en el vuelo")

# ============================================================================
# 14. RESUMEN Y CONCLUSIONES
# ============================================================================
print("\n" + "="*80)
print("14. RESUMEN Y DEFINICIONES")
print("="*80)

summary = """
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
"""

print(summary)

print("\n" + "="*80)
print("ANÁLISIS COMPLETADO")
print("="*80)

