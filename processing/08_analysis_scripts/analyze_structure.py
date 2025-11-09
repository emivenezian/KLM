import pandas as pd

# Leer el archivo
piece_info = pd.read_csv('Inputfiles/PieceInformationSpotfire.csv')

# Filtrar el AWB específico
awb = '7459521221'
df = piece_info[piece_info['BookingAirWaybillNumber'] == int(awb)].copy()

# Convertir pesos a números
df['SegmentWeightNum'] = df['BookingSegmentPiecesWeight'].str.replace(',', '.').astype(float)
df['LineWeightNum'] = df['BookingLinePieceWeight'].str.replace(',', '.').astype(float)
df['LineVolumeNum'] = df['BookingLinePieceVolume'].str.replace(',', '.').astype(float)

print("="*80)
print("ANÁLISIS DE ESTRUCTURA: ¿Son 17 cajas idénticas con 17 items cada una?")
print("="*80)

# 1. ¿Son todas las piezas idénticas?
print("\n1. ¿Son todas las piezas físicas (BookingSegmentPiecesID) idénticas?")
print("-"*80)

# Analizar cada PiecesID
pieces_summary = []
for piece_id in sorted(df['BookingSegmentPiecesID'].unique()):
    df_piece = df[df['BookingSegmentPiecesID'] == piece_id]
    weight = df_piece['SegmentWeightNum'].iloc[0]
    num_lines = len(df_piece)
    pieces_summary.append({
        'PiecesID': int(piece_id),
        'Weight': weight,
        'NumLines': num_lines
    })

summary_df = pd.DataFrame(pieces_summary)
print("\nPeso de cada pieza física (BookingSegmentPiecesWeight):")
print(summary_df.to_string(index=False))

print(f"\n¿Todas las piezas tienen el mismo peso? {summary_df['Weight'].nunique() == 1}")
print(f"Pesos únicos: {sorted(summary_df['Weight'].unique())}")

# 2. ¿Qué representa cada línea dentro de una pieza?
print("\n\n2. Dentro de cada pieza, ¿qué representan las 17 líneas?")
print("-"*80)

# Analizar pieza 1
piece1 = df[df['BookingSegmentPiecesID'] == 1].copy()
piece1['LineHeightNum'] = piece1['BookingLinePieceHeight'].str.replace(',', '.').astype(float)
piece1['LineWidthNum'] = piece1['BookingLinePieceWidth'].str.replace(',', '.').astype(float)
piece1['LineLengthNum'] = piece1['BookingLinePieceLength'].str.replace(',', '.').astype(float)

print(f"\nPieza #1 (BookingSegmentPiecesID=1):")
print(f"Peso de la pieza: {piece1['SegmentWeightNum'].iloc[0]} kg")
print(f"Número de líneas: {len(piece1)}")

print("\nDetalles de cada línea:")
cols = ['BookingLineNumber', 'BookingSegmentPiecesID', 'SegmentWeightNum', 'LineWeightNum', 
        'LineVolumeNum', 'LineHeightNum', 'LineWidthNum', 'LineLengthNum']
print(piece1[cols].to_string(index=False))

# 3. Verificar si las líneas dentro de cada pieza son iguales
print("\n\n3. ¿Las 17 líneas dentro de cada pieza son iguales entre sí?")
print("-"*80)

# Comparar línea por línea entre diferentes piezas
print("\nComparando Pieza #1 vs Pieza #2:")
piece2 = df[df['BookingSegmentPiecesID'] == 2].copy()
piece2['LineWeightNum'] = piece2['BookingLinePieceWeight'].str.replace(',', '.').astype(float)

# Ordenar por BookingLineNumber
piece1_sorted = piece1.sort_values('BookingLineNumber')
piece2_sorted = piece2.sort_values('BookingLineNumber')

comparison = pd.DataFrame({
    'LineNumber': piece1_sorted['BookingLineNumber'].values,
    'P1_LineWeight': piece1_sorted['LineWeightNum'].values,
    'P2_LineWeight': piece2_sorted['LineWeightNum'].values,
    'Same': piece1_sorted['LineWeightNum'].values == piece2_sorted['LineWeightNum'].values
})
print(comparison.to_string(index=False))

all_same = comparison['Same'].all()
print(f"\n¿Todas las líneas tienen el mismo peso entre Pieza 1 y 2? {all_same}")

# 4. Interpretación correcta
print("\n\n4. INTERPRETACIÓN CORRECTA")
print("="*80)

# Verificar suma total
total_segment_weight = df['SegmentWeightNum'].sum()
expected_weight = df['BookingSegmentWeight'].iloc[0].replace(',', '.')
expected_weight_num = float(expected_weight)

print(f"Suma de todos los BookingSegmentPiecesWeight: {total_segment_weight:.2f} kg")
print(f"BookingSegmentWeight (peso total del AWB): {expected_weight_num} kg")
print(f"¿Coinciden? {abs(total_segment_weight - expected_weight_num) < 1}")

# Análisis de BookingLineNumber
print(f"\nBookingLineNumber únicos: {sorted(df['BookingLineNumber'].unique())}")

# ¿Cuántas líneas de booking hay?
unique_booking_lines = df['BookingLineNumber'].nunique()
print(f"Número de BookingLineNumber diferentes: {unique_booking_lines}")

# Contar piezas por BookingLineNumber
for line_num in sorted(df['BookingLineNumber'].unique())[:3]:  # Solo primeras 3
    df_line = df[df['BookingLineNumber'] == line_num]
    pieces = sorted(df_line['BookingSegmentPiecesID'].unique())
    print(f"  BookingLineNumber={line_num}: {len(pieces)} piezas → IDs: {pieces}")

