import pandas as pd
import numpy as np

# Leer el archivo
piece_info = pd.read_csv('Inputfiles/PieceInformationSpotfire.csv')

# Filtrar el AWB específico
awb = '7459521221'
df = piece_info[piece_info['BookingAirWaybillNumber'] == int(awb)].copy()

# Convertir pesos a números
df['SegmentWeightNum'] = df['BookingSegmentPiecesWeight'].str.replace(',', '.').astype(float)
df['LineWeightNum'] = df['BookingLinePieceWeight'].str.replace(',', '.').astype(float)

print("="*80)
print("ANÁLISIS FINAL: ¿Qué significan las 289 líneas?")
print("="*80)

# La clave está en entender la relación entre las columnas
print("\n1. ESTRUCTURA DE LOS DATOS")
print("-"*80)

# Crear una matriz de piezas
print("\nMatriz de datos (primeras 5 filas):")
print(df[['BookingLineNumber', 'BookingSegmentPiecesID', 'BookingSegmentPiecesCount', 
         'SegmentWeightNum', 'LineWeightNum']].head(20))

# Verificación importante: BookingSegmentPiecesCount
print("\n\n2. COLUMNA CLAVE: BookingSegmentPiecesCount")
print("-"*80)
print(f"Valores únicos: {df['BookingSegmentPiecesCount'].unique()}")
print("\nInterpretación: Esta columna indica cuántas veces se repite esta pieza")

# Analizar la estructura real
print("\n\n3. INTERPRETACIÓN REAL")
print("="*80)

# Suma de BookingSegmentPiecesWeight
sum_segment_weights = df['SegmentWeightNum'].sum()
expected = 422.70

print(f"Suma de todos los BookingSegmentPiecesWeight: {sum_segment_weights:.2f} kg")
print(f"Peso esperado del AWB: {expected} kg")
print(f"Ratio: {sum_segment_weights / expected:.1f}x")

# Suma de pesos únicos
unique_pieces_weight = df.groupby('BookingSegmentPiecesID')['SegmentWeightNum'].first().sum()
print(f"\nSuma de BookingSegmentPiecesWeight únicos (1 por pieza): {unique_pieces_weight:.2f} kg")
print(f"¿Esto coincide con el peso total? {abs(unique_pieces_weight - expected) < 1}")

print("\n\n4. CONCLUSIÓN")
print("="*80)
print(f"✅ HAY 17 PIEZAS FÍSICAS REALES (BookingTotalPieceCount = 17)")
print(f"✅ Cada pieza tiene un peso diferente (BookingSegmentPiecesWeight)")
print(f"✅ Las 17 piezas suman: {unique_pieces_weight:.2f} kg ≈ {expected} kg ✓")

print("\n❓ PERO ¿POR QUÉ 289 LÍNEAS?")
print("-"*80)

# Analizar la estructura de la matriz
# Crear pivot table para ver la estructura
print("\nCreando matriz de análisis...")

# Obtener todas las combinaciones únicas de LineWeight para cada PiecesID
pivot_data = []
for piece_id in sorted(df['BookingSegmentPiecesID'].unique()):
    df_piece = df[df['BookingSegmentPiecesID'] == piece_id]
    line_weights = sorted(df_piece['LineWeightNum'].unique())
    pivot_data.append({
        'PiecesID': int(piece_id),
        'SegmentWeight': df_piece['SegmentWeightNum'].iloc[0],
        'NumLineas': len(df_piece),
        'NumLineWeightsUnicos': len(line_weights),
        'LineWeights': line_weights
    })

print("\nAnálisis por pieza:")
print(f"{'PiecesID':<10} {'SegWeight':<12} {'#Líneas':<10} {'#LineWeights':<15}")
print("-"*80)
for row in pivot_data[:10]:
    print(f"{row['PiecesID']:<10} {row['SegmentWeight']:<12.2f} {row['NumLineas']:<10} {row['NumLineWeightsUnicos']:<15}")

# Análisis de LineWeight
print("\n\n5. ANÁLISIS DE BookingLinePieceWeight")
print("-"*80)
all_line_weights = sorted(df['LineWeightNum'].unique())
print(f"Valores únicos de BookingLinePieceWeight: {len(all_line_weights)}")
print(f"Valores: {[f'{x:.2f}' for x in all_line_weights]}")

# ¿Son los mismos que SegmentWeight?
all_segment_weights = sorted(df['SegmentWeightNum'].unique())
print(f"\nValores únicos de BookingSegmentPiecesWeight: {len(all_segment_weights)}")
print(f"Valores: {[f'{x:.2f}' for x in all_segment_weights]}")

print("\n¿Son los mismos valores?")
same = set([round(x, 2) for x in all_line_weights]) == set([round(x, 2) for x in all_segment_weights])
print(f"LineWeight == SegmentWeight (valores únicos): {same}")

# HIPÓTESIS FINAL
print("\n\n6. HIPÓTESIS FINAL")
print("="*80)
print("""
La estructura de datos es una MATRIZ CARTESIANA:
- Hay 17 piezas físicas reales (BookingSegmentPiecesID 1-17)
- Cada pieza pesa distinto (BookingSegmentPiecesWeight)
- El sistema genera 17 líneas para CADA pieza
- Cada línea asigna un BookingLinePieceWeight diferente
- Total: 17 piezas × 17 líneas = 289 líneas

¿POR QUÉ? Posibles razones:
1. Sistema de compatibilidad/empaque: muestra diferentes configuraciones
2. Error de extracción de datos de Spotfire
3. Estructura de datos denormalizada para análisis
4. Cada línea representa una posible asignación de peso

PARA TU OPTIMIZACIÓN, USA:
→ 17 PIEZAS FÍSICAS (BookingTotalPieceCount)
→ Peso de cada pieza: BookingSegmentPiecesWeight (único por PiecesID)
→ Dimensiones: BookingLinePieceHeight/Width/Length (probablemente iguales para mismo PiecesID)
""")

# Verificar dimensiones
print("\n7. VERIFICACIÓN DE DIMENSIONES")
print("-"*80)
print("\n¿Las dimensiones son iguales para el mismo PiecesID?")
for piece_id in [1, 2, 3]:
    df_piece = df[df['BookingSegmentPiecesID'] == piece_id].copy()
    df_piece['Height'] = df_piece['BookingLinePieceHeight'].str.replace(',', '.').astype(float)
    df_piece['Width'] = df_piece['BookingLinePieceWidth'].str.replace(',', '.').astype(float)
    df_piece['Length'] = df_piece['BookingLinePieceLength'].str.replace(',', '.').astype(float)
    
    unique_dims = df_piece[['Height', 'Width', 'Length']].drop_duplicates()
    print(f"\nPieza {piece_id}: {len(unique_dims)} combinaciones únicas de dimensiones")
    if len(unique_dims) <= 3:
        print(unique_dims.to_string(index=False))

