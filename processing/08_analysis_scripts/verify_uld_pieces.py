import pandas as pd

buildup = pd.read_csv('Inputfiles/BuildUpInformationSpotfire.csv')
loadloc = pd.read_csv('Inputfiles/LoadLocationsSpotfire.csv')

print("VERIFICACIÓN: NrBuildupPieces por ULD vs LoadLocations")
print("="*80)

# Suma por ULD en BuildUp
buildup_sum = buildup.groupby('ULD')['NrBuildupPieces'].sum().reset_index()
buildup_sum.columns = ['ULD', 'TotalNrBuildupPieces']

print(f"\n1. BuildUp: {len(buildup_sum)} ULDs")
print(f"LoadLocations: {len(loadloc['SerialNumber'].unique())} ULDs")

# Merge con LoadLocations
merged = loadloc.merge(buildup_sum, left_on='SerialNumber', right_on='ULD', how='inner')

print(f"\nULDs en común: {len(merged)}")

# Ver campos de LoadLocations
print(f"\n2. Campos en LoadLocations:")
print(loadloc.columns.tolist())

# Ejemplo PMC24809KL
print(f"\n3. ULD PMC24809KL:")
uld_buildup = buildup[buildup['ULD'] == 'PMC24809KL']
print(f"BuildUp - Suma NrBuildupPieces: {uld_buildup['NrBuildupPieces'].sum()}")

uld_loadloc = loadloc[loadloc['SerialNumber'] == 'PMC24809KL']
if len(uld_loadloc) > 0:
    print(f"\nLoadLocations:")
    cols = ['SerialNumber', 'LoadType', 'Weight', 'NumberOfItemsInUld']
    print(uld_loadloc[cols].head())
else:
    print("No encontrado en LoadLocations")

# Buscar ULD con LoadType != Cargo
print(f"\n4. Buscando ULDs con LoadType ≠ Cargo:")
non_cargo = loadloc[loadloc['LoadType'] != 'Cargo']
print(f"LoadType valores: {loadloc['LoadType'].unique()}")
print(f"Non-cargo ULDs: {len(non_cargo)}")

# Tomar un ULD con items
uld_with_items = loadloc[loadloc['NumberOfItemsInUld'].notna()].head(5)
print(f"\n5. ULDs con NumberOfItemsInUld:")
for idx, row in uld_with_items.iterrows():
    uld_name = row['SerialNumber']
    items = row['NumberOfItemsInUld']
    load_type = row['LoadType']
    
    # Buscar en buildup
    buildup_data = buildup[buildup['ULD'] == uld_name]
    buildup_sum_val = buildup_data['NrBuildupPieces'].sum()
    
    print(f"\n  {uld_name} (LoadType={load_type}):")
    print(f"    LoadLocations - NumberOfItemsInUld: {items}")
    print(f"    BuildUp - Suma NrBuildupPieces: {buildup_sum_val}")
    print(f"    ¿Coincide? {abs(float(items) - buildup_sum_val) < 0.1 if items else False}")

# Análisis general
print(f"\n6. ANÁLISIS GENERAL:")
# Solo ULDs con NumberOfItemsInUld
loadloc_with_items = loadloc[loadloc['NumberOfItemsInUld'].notna()].copy()
loadloc_with_items['NumberOfItemsInUld_num'] = pd.to_numeric(loadloc_with_items['NumberOfItemsInUld'], errors='coerce')

merged_items = loadloc_with_items.merge(buildup_sum, left_on='SerialNumber', right_on='ULD', how='inner')
merged_items['Diff'] = abs(merged_items['NumberOfItemsInUld_num'] - merged_items['TotalNrBuildupPieces'])

matches = (merged_items['Diff'] < 0.1).sum()
print(f"ULDs con NumberOfItemsInUld: {len(merged_items)}")
print(f"Coinciden con BuildUp: {matches} ({matches/len(merged_items)*100:.1f}%)")

# Mostrar casos que NO coinciden
non_matches = merged_items[merged_items['Diff'] >= 0.1].head(5)
if len(non_matches) > 0:
    print(f"\nEjemplos que NO coinciden:")
    for idx, row in non_matches.iterrows():
        print(f"  {row['SerialNumber']}: LoadLoc={row['NumberOfItemsInUld_num']}, BuildUp={row['TotalNrBuildupPieces']}, Diff={row['Diff']}")

