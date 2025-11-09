import pandas as pd
import numpy as np

df = pd.read_csv('Inputfiles/BuildUpInformationSpotfire.csv')

print("ANÁLISIS DE PATRONES - BUILDUP")
print("="*80)

# Columnas de interés
cols = ['TotalNumberOfShipments', 'AirWaybillSequenceNumber', 
        'AirWaybillStorageSequenceNumber', 'NumberOfPiecesOnAWB',
        'BuildupEventDateTime', 'NrBuildupPieces', 'IsNotBuildUp']

# 1. VALORES NULOS
print("\n1. VALORES NULOS/VACÍOS:")
for col in cols:
    nulls = df[col].isna().sum()
    print(f"  {col}: {nulls} ({nulls/len(df)*100:.1f}%)")

# 2. PATRONES DE NULOS
print("\n2. PATRONES CUANDO HAY NULOS:")
empty_storage = df[df['AirWaybillStorageSequenceNumber'].isna()]
print(f"\nCuando AirWaybillStorageSequenceNumber está vacío ({len(empty_storage)} casos):")
print(f"  NrBuildupPieces vacío: {empty_storage['NrBuildupPieces'].isna().sum()}")
print(f"  BuildupEventDateTime vacío: {empty_storage['BuildupEventDateTime'].isna().sum()}")
print(f"  IsNotBuildUp=TRUE: {empty_storage['IsNotBuildUp'].sum()}")

# 3. ISNOTBUILDUP
print(f"\n3. IsNotBuildUp:")
print(df['IsNotBuildUp'].value_counts())

not_buildup = df[df['IsNotBuildUp'] == True]
print(f"\nCuando IsNotBuildUp=TRUE ({len(not_buildup)} casos):")
print(f"  AirWaybillStorageSequenceNumber vacío: {not_buildup['AirWaybillStorageSequenceNumber'].isna().sum()}")
print(f"  NrBuildupPieces vacío: {not_buildup['NrBuildupPieces'].isna().sum()}")
print(f"  BuildupEventDateTime vacío: {not_buildup['BuildupEventDateTime'].isna().sum()}")

# 4. TOTALNUMBEROFSHIPMENTS
print(f"\n4. TotalNumberOfShipments (otros AWBs en el ULD):")
print(df['TotalNumberOfShipments'].value_counts().head(10))

print(f"\nPromedio de shipments por ULD: {df['TotalNumberOfShipments'].mean():.2f}")
print(f"Máximo: {df['TotalNumberOfShipments'].max()}")

# 5. AIRWAYBILLSEQUENCENUMBER
print(f"\n5. AirWaybillSequenceNumber:")
print(df['AirWaybillSequenceNumber'].value_counts())

# 6. CORRELACIÓN ENTRE VARIABLES NUMÉRICAS
print(f"\n6. CORRELACIONES:")
numeric_df = df[['TotalNumberOfShipments', 'AirWaybillSequenceNumber',
                 'AirWaybillStorageSequenceNumber', 'NumberOfPiecesOnAWB',
                 'NrBuildupPieces']].copy()

# Convertir a numérico
for col in numeric_df.columns:
    numeric_df[col] = pd.to_numeric(numeric_df[col], errors='coerce')

corr = numeric_df.corr()
print("\nMatriz de correlación:")
print(corr.round(3))

# 7. PATRONES POR AWB
print(f"\n7. PATRONES POR AWB (ejemplos):")

# AWB con múltiples Storage Sequence
multi_storage = df.groupby('AirWaybillNumber')['AirWaybillStorageSequenceNumber'].nunique()
multi_storage = multi_storage[multi_storage > 1].sort_values(ascending=False)

print(f"\nAWBs con múltiples StorageSequence: {len(multi_storage)}")
print(f"Ejemplo top 3:")
for awb in multi_storage.head(3).index:
    awb_data = df[df['AirWaybillNumber'] == awb]
    print(f"\n  AWB {awb}:")
    print(f"    Total piezas: {awb_data['NumberOfPiecesOnAWB'].iloc[0]}")
    print(f"    Lotes (StorageSeq): {sorted(awb_data['AirWaybillStorageSequenceNumber'].dropna().unique())}")
    print(f"    Piezas por lote: {list(awb_data['NrBuildupPieces'].dropna().values)}")
    print(f"    Suma: {awb_data['NrBuildupPieces'].sum()}")

# 8. REGLAS ENCONTRADAS
print(f"\n\n8. REGLAS IDENTIFICADAS:")
print("="*80)
print("""
✅ REGLA 1: StorageSequenceNumber vacío ↔ IsNotBuildUp=TRUE
   - Cuando no hay StorageSeq → no hay NrBuildupPieces
   - Indica que el AWB NO se procesó en build-up
   
✅ REGLA 2: TotalNumberOfShipments = otros AWBs en el MISMO ULD
   - 0 = este AWB es único en el ULD
   - N = hay N otros AWBs diferentes en el ULD
   
✅ REGLA 3: AirWaybillSequenceNumber casi siempre = 1
   - Indica orden de procesamiento del AWB
   
✅ REGLA 4: StorageSequenceNumber = número de "lote" de carga
   - 1, 2, 3... = piezas cargadas en diferentes momentos
   - NrBuildupPieces = cuántas piezas en ese lote
   - Suma(NrBuildupPieces) ≈ NumberOfPiecesOnAWB
   
✅ REGLA 5: BuildupEventDateTime vacío → IsNotBuildUp=TRUE
   - Sin fecha = no se hizo build-up real
""")

# 9. VERIFICAR REGLA 4
print(f"\n9. VERIFICACIÓN: Suma NrBuildupPieces = NumberOfPiecesOnAWB:")
valid = df[df['IsNotBuildUp'] == False].groupby('AirWaybillNumber').agg({
    'NrBuildupPieces': 'sum',
    'NumberOfPiecesOnAWB': 'first'
})
valid['Diff'] = abs(valid['NrBuildupPieces'] - valid['NumberOfPiecesOnAWB'])
matches = (valid['Diff'] < 0.1).sum()
print(f"  AWBs donde coincide: {matches}/{len(valid)} ({matches/len(valid)*100:.1f}%)")

