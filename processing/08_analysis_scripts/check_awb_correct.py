import pandas as pd

# Leer el archivo
piece_info = pd.read_csv('Inputfiles/PieceInformationSpotfire.csv')

awb = '7459521221'

print("="*100)
print(f"VERIFICACIÓN DEL AWB {awb}")
print("="*100)

# Buscar todas las apariciones
df = piece_info[piece_info['BookingAirWaybillSerialNumber'].astype(str).str.contains(awb, na=False)]

if len(df) == 0:
    # Intentar como número completo
    df = piece_info[piece_info['BookingAirWaybillNumber'].astype(str).str.contains(awb, na=False)]

print(f"\nTotal líneas encontradas: {len(df)}")

if len(df) > 0:
    print(f"\nBookingAirWaybillNumber únicos: {df['BookingAirWaybillNumber'].unique()}")
    print(f"BookingAirWaybillSerialNumber únicos: {df['BookingAirWaybillSerialNumber'].unique()}")
    print(f"BookingTotalWeight únicos: {df['BookingTotalWeight'].unique()}")
    print(f"BookingSegmentWeight únicos: {df['BookingSegmentWeight'].unique()}")
    print(f"BookingTotalPieceCount: {df['BookingTotalPieceCount'].unique()}")
    print(f"BookingSegmentPieceCount: {df['BookingSegmentPieceCount'].unique()}")
    
    print(f"\nBookingLinePieceIsInformational:")
    print(df['BookingLinePieceIsInformational'].value_counts())
    
    # Convertir a números y verificar
    df_copy = df.copy()
    df_copy['SegmentWeightNum'] = pd.to_numeric(df_copy['BookingSegmentPiecesWeight'].str.replace(',', '.'), errors='coerce')
    df_copy['LineWeightNum'] = pd.to_numeric(df_copy['BookingLinePieceWeight'].str.replace(',', '.'), errors='coerce')
    
    # Verificar líneas donde son iguales
    df_copy['IsMatch'] = abs(df_copy['SegmentWeightNum'] - df_copy['LineWeightNum']) < 0.01
    matches = df_copy['IsMatch'].sum()
    
    print(f"\n\nLíneas donde SegmentWeight ≈ LineWeight: {matches}")
    
    if matches > 0:
        print("\n✅ SÍ HAY líneas donde coinciden!")
        print("\nPrimeras líneas coincidentes:")
        matching_rows = df_copy[df_copy['IsMatch'] == True]
        cols = ['BookingSegmentPiecesID', 'BookingSegmentPiecesCount', 'SegmentWeightNum', 
                'LineWeightNum', 'BookingLinePieceHeight', 'BookingLinePieceWidth', 
                'BookingLinePieceLength', 'BookingLinePieceIsInformational']
        print(matching_rows[cols].head(20).to_string(index=False))
        
        print(f"\n\nSuma de SegmentWeight de líneas coincidentes: {matching_rows['SegmentWeightNum'].sum():.2f}")
    else:
        print("\n❌ NO hay líneas donde coinciden")
        
        # Mostrar algunos ejemplos
        print("\nEjemplos de los datos:")
        print(df_copy[['BookingSegmentPiecesID', 'SegmentWeightNum', 'LineWeightNum']].head(10).to_string(index=False))
    
    # Mostrar primeras líneas completas
    print("\n\nPrimeras 3 líneas (todas las columnas relevantes):")
    cols_display = ['BookingAirWaybillSerialNumber', 'BookingTotalWeight', 'BookingSegmentWeight',
                   'BookingTotalPieceCount', 'BookingSegmentPieceCount', 
                   'BookingSegmentPiecesID', 'BookingSegmentPiecesCount',
                   'BookingSegmentPiecesWeight', 'BookingLinePieceWeight',
                   'BookingLinePieceIsInformational']
    print(df[cols_display].head(3))

else:
    print(f"\n❌ No se encontró el AWB {awb}")
    
    # Buscar AWBs similares
    print("\nBuscando AWBs similares...")
    similar = piece_info[piece_info['BookingAirWaybillSerialNumber'].astype(str).str.contains('59521221', na=False)]
    if len(similar) > 0:
        print(f"Encontrados {len(similar)} con '59521221'")
        print(f"SerialNumbers: {similar['BookingAirWaybillSerialNumber'].unique()[:10]}")

