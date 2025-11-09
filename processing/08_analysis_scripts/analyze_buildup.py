import pandas as pd

buildup = pd.read_csv('Inputfiles/BuildUpInformationSpotfire.csv')

print("BUILDUP - ESTRUCTURA BÁSICA")
print("="*80)
print(f"Total registros: {len(buildup)}")
print(f"\nColumnas: {list(buildup.columns)}")

print(f"\n\nPRIMERAS 10 FILAS:")
print(buildup.head(10))

print(f"\n\nCOLUMNAS CLAVE:")
print(f"- ULD únicos: {buildup['ULD'].nunique()}")
print(f"- OutgoingULDKey únicos: {buildup['OutgoingULDKey'].nunique()}")
print(f"- AWBs únicos: {buildup['AirWaybillNumber'].nunique()}")

print(f"\n\nEJEMPLO AWB 7459521221:")
awb = buildup[buildup['AirWaybillNumber'].astype(str).str.contains('59521221', na=False)]
if len(awb) > 0:
    cols = ['ULD', 'AirWaybillNumber', 'AirWaybillStorageSequenceNumber', 
            'NumberOfPiecesOnAWB', 'NrBuildupPieces', 'OutgoingULDKey']
    print(awb[cols])

print(f"\n\n¿QUÉ SIGNIFICA CADA COLUMNA?")
print("- AirWaybillStorageSequenceNumber: Lote/grupo de carga")
print("- NrBuildupPieces: Piezas en ESTE lote")
print("- NumberOfPiecesOnAWB: Total piezas del AWB")
print("- OutgoingULDKey: ULD destino (siempre = ULD)")

