import pandas as pd

piece_info = pd.read_csv('Inputfiles/PieceInformationSpotfire.csv')

awb = '7459521221'
df = piece_info[piece_info['BookingAirWaybillSerialNumber'].astype(str).str.contains('59521221', na=False)]

print("="*100)
print(f"ANÁLISIS CORRECTO DEL AWB {awb}")
print("="*100)

print(f"\nTotal líneas: {len(df)}")
print(f"BookingTotalWeight: {df['BookingTotalWeight'].iloc[0]}")
print(f"BookingSegmentWeight: {df['BookingSegmentWeight'].iloc[0]}")
print(f"BookingTotalPieceCount: {df['BookingTotalPieceCount'].iloc[0]}")

# Convertir pesos
df_copy = df.copy()
df_copy['SegmentWeightNum'] = pd.to_numeric(df_copy['BookingSegmentPiecesWeight'].str.replace(',', '.'), errors='coerce')
df_copy['LineWeightNum'] = pd.to_numeric(df_copy['BookingLinePieceWeight'].str.replace(',', '.'), errors='coerce')
df_copy['IsMatch'] = abs(df_copy['SegmentWeightNum'] - df_copy['LineWeightNum']) < 0.01

# Líneas coincidentes
matching = df_copy[df_copy['IsMatch'] == True].copy()

print(f"\n{'='*100}")
print("LÍNEAS DONDE SegmentWeight == LineWeight (DATOS CORRECTOS)")
print(f"{'='*100}")

print(f"\nTotal líneas coincidentes: {len(matching)}")

# Ver piezas únicas
print(f"\nPiezas únicas (BookingSegmentPiecesID):")
unique_pieces = matching.groupby('BookingSegmentPiecesID').agg({
    'SegmentWeightNum': 'first',
    'BookingSegmentPiecesCount': 'first'
}).reset_index()

print(unique_pieces.to_string(index=False))

print(f"\n\nNúmero de PiecesID únicos: {len(unique_pieces)}")
print(f"Suma de pesos únicos: {unique_pieces['SegmentWeightNum'].sum():.2f} kg")
print(f"BookingSegmentWeight esperado: {df['BookingSegmentWeight'].iloc[0]}")

# Buscar el 3714
print(f"\n\n{'='*100}")
print("BUSCANDO EL PESO 3714")
print(f"{'='*100}")

# Buscar en todas las columnas de peso
print("\n¿Aparece 3714 en alguna parte?")

# Verificar BookingTotalWeight
df_copy['TotalWeightNum'] = pd.to_numeric(df_copy['BookingTotalWeight'].str.replace(',', '.'), errors='coerce')
print(f"BookingTotalWeight: {df_copy['TotalWeightNum'].iloc[0]}")

# Verificar sumas
print(f"\nSuma de TODOS los SegmentWeight: {df_copy['SegmentWeightNum'].sum():.2f} kg")
print(f"Suma de TODOS los LineWeight: {df_copy['LineWeightNum'].sum():.2f} kg")

# Buscar 3714 en el archivo
print(f"\n\nBuscando '3714' en todo el archivo de este AWB...")
text_search = df.astype(str).apply(lambda x: x.str.contains('3714', na=False)).any()
if text_search.any():
    cols_with_3714 = text_search[text_search].index.tolist()
    print(f"Encontrado en columnas: {cols_with_3714}")
    for col in cols_with_3714:
        print(f"  {col}: {df[col].unique()}")
else:
    print("❌ NO se encontró '3714' en este AWB")

# Buscar AWBs con peso 3714
print(f"\n\n{'='*100}")
print("BUSCANDO AWBs CON PESO ~3714")
print(f"{'='*100}")

all_data = piece_info.copy()
all_data['TotalWeightNum'] = pd.to_numeric(all_data['BookingTotalWeight'].str.replace(',', '.'), errors='coerce')
all_data['SegmentWeightNum'] = pd.to_numeric(all_data['BookingSegmentWeight'].str.replace(',', '.'), errors='coerce')

heavy_awbs = all_data[(all_data['TotalWeightNum'] > 3700) & (all_data['TotalWeightNum'] < 3730)]

if len(heavy_awbs) > 0:
    print(f"\nEncontrados {len(heavy_awbs)} líneas con peso entre 3700-3730 kg")
    print(f"AWBs únicos:")
    for awb in heavy_awbs['BookingAirWaybillNumber'].unique()[:5]:
        awb_data = all_data[all_data['BookingAirWaybillNumber'] == awb]
        print(f"  AWB {awb}: {awb_data['BookingTotalWeight'].iloc[0]} kg, {awb_data['BookingTotalPieceCount'].iloc[0]} piezas")
        
# Tal vez el usuario se refiere a otro AWB
print(f"\n\n{'='*100}")
print("¿SERÁ OTRO AWB SIMILAR?")
print(f"{'='*100}")

# Buscar AWBs con números parecidos
similar_awbs = piece_info[piece_info['BookingAirWaybillSerialNumber'].astype(str).str.contains('521221', na=False)]
unique_similar = similar_awbs['BookingAirWaybillSerialNumber'].unique()

if len(unique_similar) > 1:
    print(f"\nEncontrados {len(unique_similar)} AWBs similares:")
    for serial in unique_similar[:10]:
        awb_data = piece_info[piece_info['BookingAirWaybillSerialNumber'] == serial]
        print(f"  Serial {serial}: {awb_data['BookingTotalWeight'].iloc[0]} kg")

