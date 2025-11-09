import pandas as pd

df = pd.read_csv('Inputfiles/BuildUpInformationSpotfire.csv')

print("CORRECCIÓN - Análisis de casos específicos")
print("="*80)

# CASO 1: ULD AKE96298KL
print("\n1. ULD AKE96298KL:")
uld = df[df['ULD'] == 'AKE96298KL']
print(f"Total registros: {len(uld)}")
print(f"\nAWBs únicos: {uld['AirWaybillNumber'].unique()}")
print(f"\nTotalNumberOfShipments por registro:")
print(uld[['AirWaybillNumber', 'TotalNumberOfShipments', 'AirWaybillStorageSequenceNumber', 'NrBuildupPieces']].to_string(index=False))

# CASO 2: AWB 7464227645
print(f"\n\n2. AWB 7464227645:")
awb = df[df['AirWaybillNumber'] == 7464227645]
print(f"Total registros: {len(awb)}")
print(f"NumberOfPiecesOnAWB: {awb['NumberOfPiecesOnAWB'].iloc[0]}")
print(f"\nDetalles por línea:")
cols = ['ULD', 'AirWaybillStorageSequenceNumber', 'NrBuildupPieces', 'TotalNumberOfShipments']
print(awb[cols].to_string(index=False))
print(f"\nSuma NrBuildupPieces: {awb['NrBuildupPieces'].sum()}")

# Ver en qué ULDs está
print(f"\nULDs diferentes donde aparece: {awb['ULD'].unique()}")

# HIPÓTESIS: TotalNumberOfShipments podría ser algo diferente
print(f"\n\n3. NUEVA HIPÓTESIS - TotalNumberOfShipments:")
print("="*80)

# Analizar todos los ULDs
uld_analysis = df.groupby('ULD').agg({
    'AirWaybillNumber': 'nunique',
    'TotalNumberOfShipments': lambda x: x.mode()[0] if len(x) > 0 else 0
}).rename(columns={
    'AirWaybillNumber': 'AWBs_unicos',
    'TotalNumberOfShipments': 'TotalShipments_value'
})

print(f"\nComparación ULDs:")
print(f"ULDs con 1 AWB y TotalShipments=0: {((uld_analysis['AWBs_unicos'] == 1) & (uld_analysis['TotalShipments_value'] == 0)).sum()}")
print(f"ULDs con >1 AWB y TotalShipments=0: {((uld_analysis['AWBs_unicos'] > 1) & (uld_analysis['TotalShipments_value'] == 0)).sum()}")
print(f"ULDs con 2 AWB y TotalShipments=1: {((uld_analysis['AWBs_unicos'] == 2) & (uld_analysis['TotalShipments_value'] == 1)).sum()}")

# Ejemplo específico
ake_data = uld_analysis.loc['AKE96298KL']
print(f"\nAKE96298KL: {ake_data['AWBs_unicos']} AWBs, TotalShipments={ake_data['TotalShipments_value']}")

# HIPÓTESIS: NrBuildupPieces en múltiples ULDs
print(f"\n\n4. NUEVA HIPÓTESIS - NrBuildupPieces:")
print("="*80)

# Análisis del AWB 7464227645 en detalle
awb_detail = df[df['AirWaybillNumber'] == 7464227645]
print(f"\nAWB 7464227645 aparece en {len(awb_detail['ULD'].unique())} ULDs:")

for uld_name in awb_detail['ULD'].unique():
    uld_data = awb_detail[awb_detail['ULD'] == uld_name]
    suma = uld_data['NrBuildupPieces'].sum()
    print(f"  {uld_name}: {len(uld_data)} registros, suma={suma}")

total_all_ulds = awb_detail['NrBuildupPieces'].sum()
print(f"\nSuma TOTAL en todos ULDs: {total_all_ulds}")
print(f"NumberOfPiecesOnAWB: {awb_detail['NumberOfPiecesOnAWB'].iloc[0]}")

# Verificar si se divide entre ULDs
print(f"\n\n5. VERIFICACIÓN: ¿Se reparten las piezas entre ULDs?")
print("="*80)

# Buscar AWBs en múltiples ULDs
multi_uld_awbs = df.groupby('AirWaybillNumber')['ULD'].nunique()
multi_uld_awbs = multi_uld_awbs[multi_uld_awbs > 1]

print(f"AWBs en múltiples ULDs: {len(multi_uld_awbs)}")
print(f"\nEjemplos (top 5):")
for awb_num in list(multi_uld_awbs.head(5).index):
    awb_data = df[df['AirWaybillNumber'] == awb_num]
    total_pieces = awb_data['NumberOfPiecesOnAWB'].iloc[0]
    sum_buildup = awb_data['NrBuildupPieces'].sum()
    ulds = awb_data['ULD'].nunique()
    
    print(f"\n  AWB {awb_num}:")
    print(f"    NumberOfPiecesOnAWB: {total_pieces}")
    print(f"    ULDs diferentes: {ulds}")
    print(f"    Suma total NrBuildupPieces: {sum_buildup}")
    print(f"    Por ULD:")
    for uld in awb_data['ULD'].unique()[:3]:
        uld_sum = awb_data[awb_data['ULD'] == uld]['NrBuildupPieces'].sum()
        print(f"      {uld}: {uld_sum} piezas")

print(f"\n\n6. CONCLUSIÓN:")
print("="*80)
print("""
Nueva interpretación:

TotalNumberOfShipments:
- NO es el número de otros AWBs en el ULD
- Posible: número de sub-envíos/splits del MISMO AWB
- O algún contador interno del sistema

NrBuildupPieces:
- La suma NO necesariamente = NumberOfPiecesOnAWB
- Razones posibles:
  1. AWB dividido en múltiples ULDs
  2. Piezas cargadas/descargadas múltiples veces
  3. Errores de registro en sistema
  4. Suma debe hacerse SOLO en el ULD final/correcto
""")

