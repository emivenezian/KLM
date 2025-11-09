import pandas as pd

# Leer el archivo
piece_info = pd.read_csv('Inputfiles/PieceInformationSpotfire.csv')

print("="*100)
print("BUSCANDO AWBs CON LÍNEAS INFORMACIONALES")
print("="*100)

# Encontrar AWBs con líneas informacionales
informational_data = piece_info[piece_info['BookingLinePieceIsInformational'] == True]

print(f"\nTotal líneas con IsInformational=True: {len(informational_data)}")
print(f"Porcentaje: {len(informational_data)/len(piece_info)*100:.2f}%")

if len(informational_data) > 0:
    # Encontrar AWBs únicos
    awbs_with_info = informational_data['BookingAirWaybillNumber'].unique()
    print(f"\nAWBs con líneas informacionales: {len(awbs_with_info)}")
    
    # Analizar el primer AWB
    first_awb = awbs_with_info[0]
    print(f"\n{'='*100}")
    print(f"ANÁLISIS DEL PRIMER AWB CON DATOS INFORMACIONALES: {first_awb}")
    print(f"{'='*100}")
    
    df_awb = piece_info[piece_info['BookingAirWaybillNumber'] == first_awb]
    df_info = df_awb[df_awb['BookingLinePieceIsInformational'] == True]
    
    print(f"\nTotal líneas: {len(df_awb)}")
    print(f"Líneas informacionales: {len(df_info)}")
    print(f"BookingTotalPieceCount: {df_awb['BookingTotalPieceCount'].iloc[0]}")
    print(f"BookingSegmentPieceCount: {df_awb['BookingSegmentPieceCount'].iloc[0]}")
    
    # Analizar BookingSegmentPiecesCount
    print(f"\nBookingSegmentPiecesCount en líneas informacionales:")
    print(df_info['BookingSegmentPiecesCount'].value_counts().sort_index())
    
    total_from_count = df_info['BookingSegmentPiecesCount'].sum()
    print(f"\nSuma de BookingSegmentPiecesCount: {total_from_count}")
    print(f"BookingTotalPieceCount: {df_awb['BookingTotalPieceCount'].iloc[0]}")
    print(f"¿Coinciden? {abs(total_from_count - df_awb['BookingTotalPieceCount'].iloc[0]) < 0.1}")
    
    # Mostrar primeras líneas informacionales
    print(f"\nPrimeras líneas informacionales:")
    cols = ['BookingSegmentPiecesID', 'BookingSegmentPiecesCount', 'BookingSegmentPiecesWeight',
            'BookingLinePieceWeight', 'BookingLinePieceHeight', 'BookingLinePieceWidth', 
            'BookingLinePieceLength']
    print(df_info[cols].head(20).to_string(index=False))
    
    # Verificar si SegmentWeight == LineWeight en líneas informacionales
    df_info_copy = df_info.copy()
    df_info_copy['SegmentWeightNum'] = df_info_copy['BookingSegmentPiecesWeight'].str.replace(',', '.').astype(float)
    df_info_copy['LineWeightNum'] = df_info_copy['BookingLinePieceWeight'].str.replace(',', '.').astype(float)
    df_info_copy['IsMatch'] = abs(df_info_copy['SegmentWeightNum'] - df_info_copy['LineWeightNum']) < 0.01
    
    matches = df_info_copy['IsMatch'].sum()
    print(f"\n\nLíneas donde SegmentWeight ≈ LineWeight: {matches}/{len(df_info_copy)}")
    
    if matches == len(df_info_copy):
        print("✅ TODAS las líneas informacionales tienen SegmentWeight == LineWeight")
    elif matches == 0:
        print("❌ NINGUNA línea informacional tiene SegmentWeight == LineWeight")
    else:
        print(f"⚠️ Solo {matches} de {len(df_info_copy)} coinciden")
        
    # Analizar la estructura
    print(f"\n\n{'='*100}")
    print("INTERPRETACIÓN FINAL")
    print(f"{'='*100}")
    
    print("""
    HIPÓTESIS REVISADA:
    
    1. BookingLinePieceIsInformational = True marca las líneas que tienen datos REALES
    2. Estas líneas pueden o no coincidir con SegmentWeight == LineWeight
    3. BookingSegmentPiecesCount indica cuántas piezas idénticas hay
    4. El código repite las dimensiones n veces para crear items individuales
    """)

else:
    print("\n❌ No se encontraron líneas con IsInformational=True")
    print("\nEsto explica por qué el AWB 7459521221 usa el bloque 'else' del código")
    print("que estima dimensiones basadas en proporciones de commodity.")

