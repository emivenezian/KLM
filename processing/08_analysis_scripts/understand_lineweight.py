import pandas as pd

# Leer el archivo
piece_info = pd.read_csv('Inputfiles/PieceInformationSpotfire.csv')

awb = '7459521221'
df = piece_info[piece_info['BookingAirWaybillNumber'] == int(awb)].copy()

# Convertir a números
df['SegmentWeightNum'] = df['BookingSegmentPiecesWeight'].str.replace(',', '.').astype(float)
df['LineWeightNum'] = df['BookingLinePieceWeight'].str.replace(',', '.').astype(float)
df['SegmentVolumeNum'] = df['BookingSegmentPiecesVolume'].str.replace(',', '.').astype(float)
df['LineVolumeNum'] = df['BookingLinePieceVolume'].str.replace(',', '.').astype(float)

print("="*100)
print("ANÁLISIS: ¿Qué es BookingLinePieceWeight?")
print("="*100)

print("\n1. CREANDO TABLA PIVOTE - Pieza vs LineWeight")
print("-"*100)

# Crear una matriz: para cada PiecesID, qué LineWeights aparecen
matrix_data = []
for piece_id in sorted(df['BookingSegmentPiecesID'].unique()):
    df_piece = df[df['BookingSegmentPiecesID'] == piece_id]
    segment_weight = df_piece['SegmentWeightNum'].iloc[0]
    line_weights = df_piece['LineWeightNum'].tolist()
    
    matrix_data.append({
        'PiecesID': int(piece_id),
        'SegmentWeight': segment_weight,
        'LineWeights': sorted(line_weights)
    })

print("\nPrimeras 5 piezas:")
print(f"{'PiecesID':<12} {'SegmentWeight':<15} {'LineWeights (primeros 5)'}")
print("-"*100)
for row in matrix_data[:5]:
    weights_str = ', '.join([f'{w:.2f}' for w in row['LineWeights'][:5]])
    print(f"{row['PiecesID']:<12} {row['SegmentWeight']:<15.2f} {weights_str}...")

print("\n\n2. HIPÓTESIS: ¿Es una matriz de todas las piezas?")
print("-"*100)

# Crear matriz visual
pivot = df.pivot_table(
    index='BookingSegmentPiecesID',
    columns='LineWeightNum',
    values='BookingLineNumber',
    aggfunc='count',
    fill_value=0
)

print(f"\nMatriz: {pivot.shape[0]} piezas × {pivot.shape[1]} valores de LineWeight")
print("\nColumnas (LineWeights únicos):")
print([f'{col:.2f}' for col in pivot.columns])

print("\n¿Cada pieza tiene exactamente una aparición de cada LineWeight?")
print(pivot.head(10))

print("\n\n3. ANÁLISIS DETALLADO DE UNA PIEZA")
print("-"*100)

# Analizar Pieza 1 en detalle
piece1 = df[df['BookingSegmentPiecesID'] == 1].copy()
piece1 = piece1.sort_values('LineWeightNum')

print(f"\nPieza #1 (BookingSegmentPiecesWeight = {piece1['SegmentWeightNum'].iloc[0]:.2f} kg)")
print(f"Número de líneas: {len(piece1)}")

print("\n¿Qué dimensiones tiene cada LineWeight?")
piece1['Height'] = piece1['BookingLinePieceHeight'].str.replace(',', '.').astype(float)
piece1['Width'] = piece1['BookingLinePieceWidth'].str.replace(',', '.').astype(float)
piece1['Length'] = piece1['BookingLinePieceLength'].str.replace(',', '.').astype(float)

print("\nTabla completa:")
print(piece1[['LineWeightNum', 'LineVolumeNum', 'Height', 'Width', 'Length']].to_string(index=False))

print("\n\n4. ¿SON LAS DIMENSIONES DE LAS OTRAS PIEZAS?")
print("-"*100)

# Comparar con las dimensiones de todas las piezas
print("\nPeso y dimensiones de cada pieza (BookingSegmentPieces):")
print(f"{'PiezaID':<10} {'SegWeight':<12} {'SegVolume':<12}")
print("-"*50)

for piece_id in sorted(df['BookingSegmentPiecesID'].unique()):
    df_piece = df[df['BookingSegmentPiecesID'] == piece_id]
    seg_weight = df_piece['SegmentWeightNum'].iloc[0]
    seg_volume = df_piece['SegmentVolumeNum'].iloc[0]
    print(f"{int(piece_id):<10} {seg_weight:<12.2f} {seg_volume:<12.2f}")

print("\n\n5. CONCLUSIÓN: ¿QUÉ ES BookingLinePieceWeight?")
print("="*100)

# Verificar si LineWeight corresponde a las otras piezas
print("\nComparación:")
all_segment_weights = sorted(df['SegmentWeightNum'].unique())
all_line_weights = sorted(df['LineWeightNum'].unique())

print(f"Valores únicos de SegmentWeight: {[f'{w:.2f}' for w in all_segment_weights]}")
print(f"Valores únicos de LineWeight:    {[f'{w:.2f}' for w in all_line_weights]}")

match = set([round(x, 2) for x in all_segment_weights]) == set([round(x, 2) for x in all_line_weights])
print(f"\n¿Son los mismos? {match}")

if match:
    print("\n✅ INTERPRETACIÓN:")
    print("="*100)
    print("""
BookingLinePieceWeight NO es el peso de la línea, sino el peso de OTRA pieza.

La estructura es una MATRIZ DE COMPATIBILIDAD o MATRIZ DE TODAS LAS COMBINACIONES:
    
    Cada fila representa: "Si tengo la Pieza X (SegmentWeight), 
                          ¿qué pasa si la combino con la Pieza Y (LineWeight)?"

    Ejemplo para Pieza #1:
    - SegmentWeight = 46.14 kg (peso de la pieza #1)
    - LineWeight toma los valores de TODAS las otras piezas (1.21, 2.01, 3.23, etc.)
    - Cada fila muestra una combinación posible
    
    ¿POR QUÉ EXISTE ESTO?
    Probablemente el sistema de Spotfire genera todas las combinaciones posibles
    para análisis de empaquetado o compatibilidad.
    
    PARA TU OPTIMIZACIÓN:
    ❌ NO uses las 289 líneas
    ✅ USA solo las 17 piezas únicas (BookingTotalPieceCount)
    ✅ Para cada pieza, usa BookingSegmentPiecesID, BookingSegmentPiecesWeight
    ✅ Las dimensiones probablemente estén mezcladas, necesitas filtrar correctamente
    """)

print("\n\n6. ¿CÓMO OBTENER LAS DIMENSIONES CORRECTAS DE CADA PIEZA?")
print("="*100)

print("\nBuscando la línea donde SegmentWeight == LineWeight para cada pieza:")
print(f"{'PiezaID':<10} {'Weight':<12} {'Volume':<12} {'Height':<10} {'Width':<10} {'Length':<10}")
print("-"*80)

for piece_id in sorted(df['BookingSegmentPiecesID'].unique()):
    df_piece = df[df['BookingSegmentPiecesID'] == piece_id]
    seg_weight = df_piece['SegmentWeightNum'].iloc[0]
    
    # Buscar la línea donde LineWeight == SegmentWeight
    matching_row = df_piece[abs(df_piece['LineWeightNum'] - seg_weight) < 0.01]
    
    if len(matching_row) > 0:
        row = matching_row.iloc[0]
        height = float(row['BookingLinePieceHeight'].replace(',', '.'))
        width = float(row['BookingLinePieceWidth'].replace(',', '.'))
        length = float(row['BookingLinePieceLength'].replace(',', '.'))
        volume = float(row['BookingLinePieceVolume'].replace(',', '.'))
        
        print(f"{int(piece_id):<10} {seg_weight:<12.2f} {volume:<12.4f} {height:<10.2f} {width:<10.2f} {length:<10.2f}")
    else:
        print(f"{int(piece_id):<10} {seg_weight:<12.2f} NO ENCONTRADO")

