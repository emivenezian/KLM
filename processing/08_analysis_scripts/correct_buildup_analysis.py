import pandas as pd

buildup = pd.read_csv('Inputfiles/BuildUpInformationSpotfire.csv')
loadloc = pd.read_csv('Inputfiles/LoadLocationsSpotfire.csv')

print("ANÁLISIS CORRECTO - BuildUp")
print("="*80)

# 1. Verificar AKE94567KL
print("\n1. ¿AKE94567KL existe en BuildUp?")
test_uld = buildup[buildup['ULD'] == 'AKE94567KL']
print(f"   Resultado: {len(test_uld)} registros")
if len(test_uld) > 0:
    print("   SÍ EXISTE")
else:
    print("   NO EXISTE - mi análisis anterior fue erróneo")

# 2. ¿Qué es cada fila en BuildUp?
print(f"\n2. ¿QUÉ REPRESENTA CADA FILA EN BUILDUP?")
print("-"*80)

# Ejemplo con ULD conocido
uld_example = 'AKE96298KL'
uld_data = buildup[buildup['ULD'] == uld_example]

print(f"\nEjemplo: {uld_example}")
print(f"Total filas: {len(uld_data)}")
print(f"\nDetalle de cada fila:")
cols = ['ULD', 'AirWaybillNumber', 'AirWaybillStorageSequenceNumber', 
        'NrBuildupPieces', 'NumberOfPiecesOnAWB', 'BuildupEventDateTime']
print(uld_data[cols].to_string(index=False))

print(f"\n✅ INTERPRETACIÓN:")
print(f"   - Cada FILA = un EVENTO de carga")
print(f"   - Un AWB puede tener múltiples filas (múltiples eventos/lotes)")
print(f"   - NrBuildupPieces = cuántas piezas se cargaron en ESE evento")
print(f"   - StorageSequenceNumber = número de evento/lote")

# 3. Relación BuildUp con LoadLocations
print(f"\n\n3. RELACIÓN BUILDUP + DEADLOAD = LOADLOCATIONS")
print("="*80)

# Para cada ULD en LoadLocations, sumar BuildUp
loadloc_unique = loadloc[['SerialNumber']].drop_duplicates()

results = []
for idx, row in loadloc_unique.head(20).iterrows():
    uld = row['SerialNumber']
    
    # Suma en BuildUp
    buildup_data = buildup[buildup['ULD'] == uld]
    buildup_total = buildup_data['NrBuildupPieces'].sum() if len(buildup_data) > 0 else 0
    
    # LoadLocations
    loadloc_data = loadloc[loadloc['SerialNumber'] == uld]
    num_items = loadloc_data['NumberOfItemsInUld'].iloc[0] if len(loadloc_data) > 0 else None
    deadload_count = len(loadloc_data[loadloc_data['LoadType'] != 'ULD'])
    
    results.append({
        'ULD': uld,
        'BuildUp_Sum': buildup_total,
        'LoadLoc_Items': num_items,
        'LoadLoc_Deadload': deadload_count,
        'LoadLoc_Total_Rows': len(loadloc_data)
    })

results_df = pd.DataFrame(results)
print(results_df.to_string(index=False))

# 4. Ejemplo detallado con un ULD
print(f"\n\n4. EJEMPLO DETALLADO: AKE96298KL")
print("="*80)

uld = 'AKE96298KL'

# BuildUp
print(f"\nBUILDUP:")
buildup_uld = buildup[buildup['ULD'] == uld]
print(f"  Total filas: {len(buildup_uld)}")
print(f"  AWBs distintos: {buildup_uld['AirWaybillNumber'].nunique()}")
print(f"  Suma NrBuildupPieces: {buildup_uld['NrBuildupPieces'].sum()}")

print(f"\n  Detalle por AWB:")
for awb in buildup_uld['AirWaybillNumber'].unique():
    awb_data = buildup_uld[buildup_uld['AirWaybillNumber'] == awb]
    suma = awb_data['NrBuildupPieces'].sum()
    total = awb_data['NumberOfPiecesOnAWB'].iloc[0]
    print(f"    AWB {awb}: {suma}/{total} piezas cargadas")

# LoadLocations
print(f"\nLOADLOCATIONS:")
loadloc_uld = loadloc[loadloc['SerialNumber'] == uld]
print(f"  Total filas: {len(loadloc_uld)}")
print(f"  NumberOfItemsInUld: {loadloc_uld['NumberOfItemsInUld'].unique()}")

print(f"\n  Por LoadType:")
for load_type in loadloc_uld['LoadType'].unique():
    count = len(loadloc_uld[loadloc_uld['LoadType'] == load_type])
    print(f"    {load_type}: {count} registros")

# Ver detalles
print(f"\n  Detalles:")
cols = ['LoadType', 'DeadloadType', 'DeadloadSubType', 'NumberOfItemsInUld', 'Weight']
print(loadloc_uld[cols].to_string(index=False))

# 5. HIPÓTESIS FINAL
print(f"\n\n5. HIPÓTESIS FINAL:")
print("="*80)
print("""
CADA FILA EN BUILDUP representa:
  - Un EVENTO de carga de un AWB en un ULD
  - NrBuildupPieces = piezas cargadas en ese evento específico
  - Múltiples filas por AWB = carga en múltiples momentos (lotes)

LOADLOCATIONS muestra:
  - El estado FINAL del ULD
  - Puede tener múltiples filas por ULD (diferentes tipos de carga)
  - NumberOfItemsInUld generalmente está vacío para ULDs con carga

RELACIÓN:
  - BuildUp registra el PROCESO de carga (eventos individuales)
  - LoadLocations registra el RESULTADO final (qué va en el avión)
  - NO son directamente sumables porque:
    1. LoadLocations puede tener deadload no registrado en BuildUp
    2. BuildUp puede tener eventos duplicados/errores
    3. NumberOfItemsInUld a menudo está vacío
""")

