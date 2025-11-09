import pandas as pd

piece_info = pd.read_csv('Inputfiles/PieceInformationSpotfire.csv')

awb = '58692362'
df = piece_info[piece_info['BookingAirWaybillSerialNumber'].astype(str).str.contains(awb, na=False)]

print("="*100)
print(f"ANÁLISIS DEL AWB {awb}")
print("="*100)

if len(df) == 0:
    # Buscar por número completo
    df = piece_info[piece_info['BookingAirWaybillNumber'].astype(str).str.contains(awb, na=False)]

if len(df) > 0:
    print(f"\nTotal líneas: {len(df)}")
    print(f"BookingTotalPieceCount: {df['BookingTotalPieceCount'].iloc[0]}")
    print(f"BookingSegmentPieceCount: {df['BookingSegmentPieceCount'].iloc[0]}")
    print(f"BookingTotalWeight: {df['BookingTotalWeight'].iloc[0]}")
    
    print(f"\n{'='*100}")
    print("COLUMNAS CLAVE")
    print(f"{'='*100}")
    
    # Ver las columnas importantes
    cols = ['BookingSegmentPiecesID', 'BookingSegmentPiecesCount', 
            'BookingSegmentPiecesWeight', 'BookingLinePieceWeight',
            'BookingLinePieceHeight', 'BookingLinePieceWidth', 'BookingLinePieceLength',
            'BookingLinePieceIsInformational']
    
    print("\nTodas las líneas:")
    print(df[cols].to_string(index=False))
    
    print(f"\n{'='*100}")
    print("ANÁLISIS DE LA ESTRUCTURA")
    print(f"{'='*100}")
    
    # Verificar BookingSegmentPiecesID
    unique_ids = sorted(df['BookingSegmentPiecesID'].unique())
    print(f"\nBookingSegmentPiecesID únicos: {unique_ids}")
    print(f"Cantidad de IDs únicos: {len(unique_ids)}")
    print(f"Rango: {min(unique_ids)} - {max(unique_ids)}")
    
    # BookingSegmentPiecesCount por cada ID
    print(f"\n\nBookingSegmentPiecesCount para cada PiecesID:")
    for piece_id in unique_ids:
        subset = df[df['BookingSegmentPiecesID'] == piece_id]
        count_value = subset['BookingSegmentPiecesCount'].iloc[0]
        num_lines = len(subset)
        print(f"  PiecesID {int(piece_id):2d}: Count={count_value:6.1f}, Aparece en {num_lines} líneas")
    
    # Suma de BookingSegmentPiecesCount
    df_unique_pieces = df.groupby('BookingSegmentPiecesID')['BookingSegmentPiecesCount'].first()
    total_count = df_unique_pieces.sum()
    print(f"\n\nSuma de BookingSegmentPiecesCount (únicas por ID): {total_count}")
    print(f"BookingSegmentPieceCount (del header): {df['BookingSegmentPieceCount'].iloc[0]}")
    print(f"¿Coinciden? {abs(total_count - df['BookingSegmentPieceCount'].iloc[0]) < 0.1}")
    
    # IsInformational
    print(f"\n{'='*100}")
    print("BookingLinePieceIsInformational")
    print(f"{'='*100}")
    
    print(df['BookingLinePieceIsInformational'].value_counts())
    
    # Dimensiones
    print(f"\n\n¿Tienen dimensiones?")
    has_dims = df['BookingLinePieceHeight'].notna().any()
    print(f"  BookingLinePieceHeight tiene valores: {has_dims}")
    
    if has_dims:
        info_true = df[df['BookingLinePieceIsInformational'] == True]
        info_false = df[df['BookingLinePieceIsInformational'] == False]
        
        print(f"\n  En líneas IsInformational=TRUE:")
        print(f"    Con dimensiones: {info_true['BookingLinePieceHeight'].notna().sum()}")
        
        print(f"\n  En líneas IsInformational=FALSE:")
        print(f"    Con dimensiones: {info_false['BookingLinePieceHeight'].notna().sum()}")
    
    # Interpretación
    print(f"\n\n{'='*100}")
    print("INTERPRETACIÓN")
    print(f"{'='*100}")
    
    print(f"""
BookingSegmentPieceCount (header): {df['BookingSegmentPieceCount'].iloc[0]}
→ Total de piezas en el segmento

BookingSegmentPiecesID: {len(unique_ids)} IDs únicos
→ Grupos de piezas (puede haber diferentes tipos)

BookingSegmentPiecesCount (por ID):
→ Cuántas piezas hay de CADA grupo
→ Ejemplo: PiecesID=1 con Count=3 significa 3 piezas idénticas del tipo 1
→ Suma de todos los Counts = Total de piezas

RELACIÓN:
- {len(unique_ids)} grupos diferentes de piezas
- Cada grupo puede tener múltiples piezas idénticas
- Total: {total_count} piezas
    """)
    
else:
    print(f"\n❌ No se encontró el AWB {awb}")
    
    # Buscar AWBs similares
    print("\nBuscando AWBs similares...")
    similar = piece_info[piece_info['BookingAirWaybillSerialNumber'].astype(str).str.contains('692362', na=False)]
    if len(similar) > 0:
        print(f"Encontrados con '692362': {similar['BookingAirWaybillSerialNumber'].unique()}")

