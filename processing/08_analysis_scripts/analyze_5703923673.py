import pandas as pd

piece_info = pd.read_csv('Inputfiles/PieceInformationSpotfire.csv')

awb = '5703923673'
df = piece_info[piece_info['BookingAirWaybillNumber'] == int(awb)]

print("="*100)
print(f"ANÁLISIS COMPLETO DEL AWB {awb}")
print("="*100)

print(f"\nTotal líneas: {len(df)}")
print(f"BookingTotalWeight: {df['BookingTotalWeight'].iloc[0]}")
print(f"BookingSegmentWeight: {df['BookingSegmentWeight'].iloc[0]}")
print(f"BookingTotalPieceCount: {df['BookingTotalPieceCount'].iloc[0]}")
print(f"BookingSegmentPieceCount: {df['BookingSegmentPieceCount'].iloc[0]}")

print(f"\n{'='*100}")
print("BookingLinePieceIsInformational")
print(f"{'='*100}")
print(df['BookingLinePieceIsInformational'].value_counts())

# Filtrar líneas informacionales
df_info = df[df['BookingLinePieceIsInformational'] == True]
print(f"\nLíneas informacionales: {len(df_info)}")

if len(df_info) > 0:
    print(f"\n{'='*100}")
    print("LÍNEAS INFORMACIONALES (DATOS REALES)")
    print(f"{'='*100}")
    
    cols = ['BookingSegmentPiecesID', 'BookingSegmentPiecesCount', 
            'BookingSegmentPiecesWeight', 'BookingLinePieceWeight',
            'BookingLinePieceHeight', 'BookingLinePieceWidth', 'BookingLinePieceLength',
            'BookingSegmentPiecesStackable', 'BookingSegmentPiecesTurnable']
    
    print(df_info[cols].to_string(index=False))
    
    # Verificar si SegmentWeight == LineWeight
    df_info_copy = df_info.copy()
    df_info_copy['SegmentWeightNum'] = pd.to_numeric(df_info_copy['BookingSegmentPiecesWeight'].str.replace(',', '.'), errors='coerce')
    df_info_copy['LineWeightNum'] = pd.to_numeric(df_info_copy['BookingLinePieceWeight'].str.replace(',', '.'), errors='coerce')
    df_info_copy['IsMatch'] = abs(df_info_copy['SegmentWeightNum'] - df_info_copy['LineWeightNum']) < 0.01
    
    print(f"\n\nLíneas donde SegmentWeight ≈ LineWeight: {df_info_copy['IsMatch'].sum()}")
    
    if df_info_copy['IsMatch'].sum() == 0:
        print("\n✅ CORRECTA INTERPRETACIÓN:")
        print("  → BookingSegmentPiecesWeight = Peso INDIVIDUAL de 1 pieza")
        print("  → BookingLinePieceWeight = Peso TOTAL del grupo")
        print("  → BookingSegmentPiecesCount = Número de piezas idénticas")
        
        # Calcular pesos
        for _, row in df_info.iterrows():
            piece_count = int(row['BookingSegmentPiecesCount'])
            total_weight = float(row['BookingLinePieceWeight'].replace(',', '.'))
            
            try:
                segment_weight = float(row['BookingSegmentPiecesWeight'].replace(',', '.'))
                individual_weight = total_weight / piece_count
                
                print(f"\n  Pieza ID {int(row['BookingSegmentPiecesID'])}:")
                print(f"    - Cantidad: {piece_count} piezas idénticas")
                print(f"    - Peso total: {total_weight:.2f} kg")
                print(f"    - Peso individual: {individual_weight:.2f} kg cada una")
                print(f"    - BookingSegmentPiecesWeight: {segment_weight:.2f} kg")
                print(f"    - Dimensiones: {row['BookingLinePieceHeight']} × {row['BookingLinePieceWidth']} × {row['BookingLinePieceLength']} cm")
                print(f"    - Stackable: {row['BookingSegmentPiecesStackable']}, Turnable: {row['BookingSegmentPiecesTurnable']}")
            except:
                print(f"    - SegmentWeight: {row['BookingSegmentPiecesWeight']} (NaN o vacío)")

# Analizar TODAS las líneas (incluyendo no informacionales)
print(f"\n\n{'='*100}")
print("TODAS LAS LÍNEAS (Matriz completa)")
print(f"{'='*100}")

df_copy = df.copy()
df_copy['SegmentWeightNum'] = pd.to_numeric(df_copy['BookingSegmentPiecesWeight'].str.replace(',', '.'), errors='coerce')
df_copy['LineWeightNum'] = pd.to_numeric(df_copy['BookingLinePieceWeight'].str.replace(',', '.'), errors='coerce')
df_copy['IsMatch'] = abs(df_copy['SegmentWeightNum'] - df_copy['LineWeightNum']) < 0.01

matching = df_copy[df_copy['IsMatch'] == True]
print(f"Líneas donde SegmentWeight ≈ LineWeight en TOTAL: {len(matching)}")

if len(matching) > 0:
    print("\n✅ SÍ HAY líneas donde coinciden:")
    cols_match = ['BookingSegmentPiecesID', 'SegmentWeightNum', 'LineWeightNum', 
                  'BookingLinePieceIsInformational']
    print(matching[cols_match].to_string(index=False))

print(f"\n\n{'='*100}")
print("RESUMEN FINAL")
print(f"{'='*100}")

print(f"""
AWB: {awb}
Total piezas: {df['BookingTotalPieceCount'].iloc[0]}
Peso total: {df['BookingTotalWeight'].iloc[0]} kg
Líneas informacionales: {len(df_info)}

INTERPRETACIÓN:
""")

if len(df_info) > 0:
    piece_count = int(df_info['BookingSegmentPiecesCount'].iloc[0])
    if piece_count > 1:
        print(f"✅ Este AWB tiene {piece_count} PIEZAS IDÉNTICAS (como cajas de IKEA)")
        print(f"   → Todas tienen las mismas dimensiones")
        print(f"   → El código las individualiza en el loop")
    else:
        print(f"✅ Este AWB tiene piezas diferentes")

