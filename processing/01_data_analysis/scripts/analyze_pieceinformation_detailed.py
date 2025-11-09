"""
Análisis Exhaustivo de PieceInformationSpotfire.csv
Objetivo: Entender estructura, campos y relaciones con LoadLocations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("ANÁLISIS EXHAUSTIVO DE PIECEINFORMATIONSPOTFIRE.CSV")
print("="*80)

# Cargar datos
df = pd.read_csv('Inputfiles/PieceInformationSpotfire.csv')
print(f"\n✓ Datos cargados: {len(df)} registros, {len(df.columns)} columnas")

# ============================================================================
# 1. ESTRUCTURA GENERAL
# ============================================================================
print("\n" + "="*80)
print("1. ESTRUCTURA Y COLUMNAS")
print("="*80)

print(f"\nTotal columnas: {len(df.columns)}")
print("\nLista de columnas:")
for i, col in enumerate(df.columns, 1):
    print(f"{i:2d}. {col}")

print("\nTipos de datos:")
print(df.dtypes.value_counts())

# ============================================================================
# 2. VALORES NULOS
# ============================================================================
print("\n" + "="*80)
print("2. ANÁLISIS DE VALORES NULOS")
print("="*80)

null_counts = df.isnull().sum()
null_percentages = (null_counts / len(df) * 100).round(2)
null_df = pd.DataFrame({
    'Column': null_counts.index,
    'Nulls': null_counts.values,
    'Percentage': null_percentages.values
})
null_df = null_df[null_df['Nulls'] > 0].sort_values('Nulls', ascending=False)

if len(null_df) > 0:
    print(f"\nColumnas con valores nulos ({len(null_df)}):")
    print(null_df.to_string(index=False))
else:
    print("\n✓ No hay valores nulos en ninguna columna")

# ============================================================================
# 3. BOOKING INFORMATION
# ============================================================================
print("\n" + "="*80)
print("3. INFORMACIÓN DE BOOKING")
print("="*80)

print(f"\nAirWaybills únicos: {df['BookingAirWaybillNumber'].nunique()}")
print(f"Registros totales: {len(df)}")
print(f"Promedio de piezas por AWB: {len(df) / df['BookingAirWaybillNumber'].nunique():.2f}")

print("\nEstadísticas de BookingTotalPieceCount:")
print(df['BookingTotalPieceCount'].describe())

print("\nBookingEvaluationStatus:")
print(df['BookingEvaluationStatus'].value_counts())

print("\nBookingProductCode (Top 10):")
print(df['BookingProductCode'].value_counts().head(10))

print("\nBookingCommodityCode (Top 10):")
print(df['BookingCommodityCode'].value_counts().head(10))

# ============================================================================
# 4. RUTAS Y VUELOS
# ============================================================================
print("\n" + "="*80)
print("4. RUTAS Y VUELOS")
print("="*80)

df['Route'] = df['BookingOriginStationCode'] + '->' + df['BookingDestinationStationCode']
print("\nTop 15 rutas:")
print(df['Route'].value_counts().head(15))

print("\nOrígenes únicos:")
print(df['BookingOriginStationCode'].value_counts())

print("\nDestinos únicos (Top 10):")
print(df['BookingDestinationStationCode'].value_counts().head(10))

print("\nVuelos únicos:")
print(f"Total vuelos diferentes: {df['BookingSegmentFlight'].nunique()}")
print("\nTop 10 vuelos:")
print(df['BookingSegmentFlight'].value_counts().head(10))

# ============================================================================
# 5. CARACTERÍSTICAS ESPECIALES (Flags IS...)
# ============================================================================
print("\n" + "="*80)
print("5. CARACTERÍSTICAS ESPECIALES (FLAGS)")
print("="*80)

special_flags = ['IsBUP', 'IsCOL', 'IsCRT', 'IsPEV', 'IsICE', 
                 'IsACT', 'IsACE', 'IsDangerousGoods']

print("\nConteo de flags especiales:")
for flag in special_flags:
    true_count = (df[flag] == True).sum()
    false_count = (df[flag] == False).sum()
    pct = true_count / len(df) * 100
    print(f"{flag:20s}: TRUE={true_count:5d} ({pct:5.2f}%), FALSE={false_count:5d}")

# Registros con alguna característica especial
df['HasAnySpecial'] = df[special_flags].any(axis=1)
print(f"\nRegistros con al menos una característica especial: {df['HasAnySpecial'].sum()} ({df['HasAnySpecial'].sum()/len(df)*100:.1f}%)")

# Interpretación de flags
flag_meanings = {
    'IsBUP': 'Build-Up (consolidación)',
    'IsCOL': 'Cool/Cold Chain (refrigerado)',
    'IsCRT': 'Critical/Critters (animales)',
    'IsPEV': 'Perishable Valuable (?)',
    'IsICE': 'Dry Ice (hielo seco)',
    'IsACT': 'Active (carga activa)',
    'IsACE': 'Active Cool Extended (?)',
    'IsDangerousGoods': 'Mercancías peligrosas'
}

print("\nSignificado de flags:")
for flag, meaning in flag_meanings.items():
    print(f"  {flag}: {meaning}")

# ============================================================================
# 6. PESOS Y VOLÚMENES
# ============================================================================
print("\n" + "="*80)
print("6. ANÁLISIS DE PESOS Y VOLÚMENES")
print("="*80)

# Convertir comas a puntos para números decimales
for col in ['BookingTotalVolume', 'BookingTotalWeight', 'BookingSegmentVolume', 
            'BookingSegmentWeight', 'BookingSegmentPiecesVolume', 
            'BookingSegmentPiecesWeight', 'BookingLinePieceVolume', 
            'BookingLinePieceWeight']:
    if df[col].dtype == 'object':
        df[col] = df[col].str.replace(',', '.').astype(float)

print("\nBookingTotalWeight (peso total del booking):")
print(df['BookingTotalWeight'].describe())

print("\nBookingSegmentPiecesWeight (peso de piezas en segmento):")
print(df['BookingSegmentPiecesWeight'].describe())

print("\nBookingLinePieceWeight (peso de pieza individual):")
print(df['BookingLinePieceWeight'].describe())

print("\nBookingWeightUnitCode:")
print(df['BookingWeightUnitCode'].value_counts())

print("\n--- VOLÚMENES ---")
print("\nBookingTotalVolume:")
print(df['BookingTotalVolume'].describe())

print("\nBookingVolumeUnitCode:")
print(df['BookingVolumeUnitCode'].value_counts())

# ============================================================================
# 7. DIMENSIONES DE PIEZAS
# ============================================================================
print("\n" + "="*80)
print("7. DIMENSIONES DE PIEZAS")
print("="*80)

# Verificar si hay dimensiones
has_dims = df[['BookingLinePieceHeight', 'BookingLinePieceWidth', 
               'BookingLinePieceLength']].notna().all(axis=1).sum()
print(f"\nPiezas con dimensiones completas (H, W, L): {has_dims} ({has_dims/len(df)*100:.1f}%)")
print(f"Piezas sin dimensiones: {len(df) - has_dims} ({(len(df)-has_dims)/len(df)*100:.1f}%)")

if has_dims > 0:
    dims_df = df[df[['BookingLinePieceHeight', 'BookingLinePieceWidth', 
                     'BookingLinePieceLength']].notna().all(axis=1)]
    
    print("\nEstadísticas de dimensiones (para piezas con datos):")
    print(f"Altura (Height): {dims_df['BookingLinePieceHeight'].describe()}")
    print(f"Ancho (Width): {dims_df['BookingLinePieceWidth'].describe()}")
    print(f"Largo (Length): {dims_df['BookingLinePieceLength'].describe()}")

# ============================================================================
# 8. PROPIEDADES FÍSICAS
# ============================================================================
print("\n" + "="*80)
print("8. PROPIEDADES FÍSICAS (STACKABLE, TURNABLE)")
print("="*80)

print("\nBookingSegmentPiecesStackable (¿se puede apilar?):")
print(df['BookingSegmentPiecesStackable'].value_counts())

print("\nBookingSegmentPiecesTurnable (¿se puede voltear?):")
print(df['BookingSegmentPiecesTurnable'].value_counts())

stackable_turnable = pd.crosstab(
    df['BookingSegmentPiecesStackable'], 
    df['BookingSegmentPiecesTurnable'],
    margins=True
)
print("\nCombinaciones de Stackable vs Turnable:")
print(stackable_turnable)

# ============================================================================
# 9. INFORMACIÓN DE SEGMENTO
# ============================================================================
print("\n" + "="*80)
print("9. ANÁLISIS DE SEGMENTOS")
print("="*80)

print(f"\nBookingSegmentFlightDateUTC únicos: {df['BookingSegmentFlightDateUTC'].nunique()}")
print("\nPrimeras 10 fechas:")
print(df['BookingSegmentFlightDateUTC'].value_counts().head(10))

print(f"\nBookingSegmentAirlineDesignator:")
print(df['BookingSegmentAirlineDesignator'].value_counts())

print(f"\nBookingSegmentBoardPointStationCode (punto de embarque):")
print(df['BookingSegmentBoardPointStationCode'].value_counts())

print(f"\nBookingSegmentOffPointStationCode (punto de desembarque - Top 10):")
print(df['BookingSegmentOffPointStationCode'].value_counts().head(10))

# ============================================================================
# 10. CANALES Y ESTACIONES DE ACTUALIZACIÓN
# ============================================================================
print("\n" + "="*80)
print("10. CANALES Y ACTUALIZACIONES")
print("="*80)

print("\nBookingUpdateChannelCode (canal de actualización):")
print(df['BookingUpdateChannelCode'].value_counts())

print("\nBookingUpdateStationCode (estación de actualización):")
print(df['BookingUpdateStationCode'].value_counts())

# ============================================================================
# 11. IDs Y JERARQUÍA
# ============================================================================
print("\n" + "="*80)
print("11. SISTEMA DE IDs Y JERARQUÍA")
print("="*80)

print(f"\nBookingPartShipmentID únicos: {df['BookingPartShipmentID'].nunique()}")
print(f"BookingSegmentPiecesID únicos: {df['BookingSegmentPiecesID'].nunique()}")
print(f"BookingAirWaybillNumber únicos: {df['BookingAirWaybillNumber'].nunique()}")

# Jerarquía
print("\nJerarquía de IDs:")
print("  AirWaybillNumber (AWB)")
print("    └── PartShipmentID")
print("          └── SegmentPiecesID")

# Ejemplo de jerarquía
sample_awb = df['BookingAirWaybillNumber'].iloc[0]
sample_data = df[df['BookingAirWaybillNumber'] == sample_awb].head(5)
print(f"\nEjemplo - AWB {sample_awb}:")
print(sample_data[['BookingAirWaybillNumber', 'BookingPartShipmentID', 
                    'BookingSegmentPiecesID', 'BookingLinePieceWeight']].to_string(index=False))

# ============================================================================
# 12. RELACIÓN CON LOADLOCATIONS
# ============================================================================
print("\n" + "="*80)
print("12. RELACIÓN CON LOADLOCATIONSSPOTFIRE")
print("="*80)

print("\nEste archivo contiene información a nivel de PIEZA individual:")
print("  - Dimensiones de cada pieza")
print("  - Peso de cada pieza")
print("  - Características especiales (stackable, turnable)")
print("  - Información de booking y AWB")

print("\nLoadLocationsSpotfire contiene información a nivel de ULD/CARGA:")
print("  - Posición en el avión")
print("  - ULD completo (puede contener múltiples piezas)")
print("  - Peso total del ULD")

print("\nLa relación esperada:")
print("  Múltiples piezas (PieceInformation) → 1 DeadloadId (LoadLocations)")

# ============================================================================
# 13. CORRELACIONES Y PATRONES
# ============================================================================
print("\n" + "="*80)
print("13. CORRELACIONES Y PATRONES")
print("="*80)

# Peso por ruta
route_analysis = df.groupby('Route').agg({
    'BookingLinePieceWeight': ['count', 'sum', 'mean'],
    'BookingTotalPieceCount': 'mean'
}).round(2)
route_analysis.columns = ['Pieces', 'TotalWeight', 'AvgWeight', 'AvgPiecesPerBooking']
route_analysis = route_analysis.sort_values('TotalWeight', ascending=False).head(10)

print("\nTop 10 rutas por peso total:")
print(route_analysis)

# Pesos por características especiales
print("\n--- Peso promedio por características especiales ---")
for flag in special_flags:
    if df[flag].any():
        avg_weight = df[df[flag] == True]['BookingLinePieceWeight'].mean()
        count = (df[flag] == True).sum()
        print(f"{flag:20s}: {avg_weight:6.2f} kg (n={count})")

# ============================================================================
# 14. BOOKINGLINEPIECEISINFOMATIONAL
# ============================================================================
print("\n" + "="*80)
print("14. PIEZAS INFORMACIONALES")
print("="*80)

print("\nBookingLinePieceIsInformational:")
print(df['BookingLinePieceIsInformational'].value_counts())

informational = df[df['BookingLinePieceIsInformational'] == True]
if len(informational) > 0:
    print(f"\nPiezas informacionales: {len(informational)} ({len(informational)/len(df)*100:.2f}%)")
    print("Características de piezas informacionales:")
    print(f"  Peso promedio: {informational['BookingLinePieceWeight'].mean():.2f} kg")
    print(f"  Peso total: {informational['BookingLinePieceWeight'].sum():.2f} kg")

# ============================================================================
# 15. RESUMEN Y ESTADÍSTICAS CLAVE
# ============================================================================
print("\n" + "="*80)
print("15. RESUMEN EJECUTIVO")
print("="*80)

summary = f"""
ESTADÍSTICAS GENERALES:
- Total registros (piezas): {len(df):,}
- AWB únicos: {df['BookingAirWaybillNumber'].nunique():,}
- Vuelos únicos: {df['BookingSegmentFlight'].nunique()}
- Rutas únicas: {df['Route'].nunique()}
- Piezas promedio por AWB: {len(df) / df['BookingAirWaybillNumber'].nunique():.2f}

PESOS:
- Peso total de todas las piezas: {df['BookingLinePieceWeight'].sum():,.0f} kg
- Peso promedio por pieza: {df['BookingLinePieceWeight'].mean():.2f} kg
- Peso mediano por pieza: {df['BookingLinePieceWeight'].median():.2f} kg

CARACTERÍSTICAS ESPECIALES:
- Piezas con carga especial: {df['HasAnySpecial'].sum():,} ({df['HasAnySpecial'].sum()/len(df)*100:.1f}%)
- Piezas stackable: {(df['BookingSegmentPiecesStackable']==True).sum():,} ({(df['BookingSegmentPiecesStackable']==True).sum()/len(df)*100:.1f}%)
- Piezas turnable: {(df['BookingSegmentPiecesTurnable']==True).sum():,} ({(df['BookingSegmentPiecesTurnable']==True).sum()/len(df)*100:.1f}%)

DIMENSIONES:
- Piezas con dimensiones: {has_dims:,} ({has_dims/len(df)*100:.1f}%)

TOP 3 RUTAS:
{df['Route'].value_counts().head(3).to_string()}

TOP 3 VUELOS:
{df['BookingSegmentFlight'].value_counts().head(3).to_string()}
"""

print(summary)

print("\n" + "="*80)
print("ANÁLISIS COMPLETADO")
print("="*80)

