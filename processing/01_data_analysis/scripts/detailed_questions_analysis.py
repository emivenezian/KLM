"""
Análisis detallado respondiendo preguntas específicas sobre LoadLocationsSpotfire.csv
"""

import pandas as pd
import numpy as np

print("="*80)
print("RESPUESTAS A PREGUNTAS ESPECÍFICAS - LOADLOCATIONSSPOTFIRE.CSV")
print("="*80)

df = pd.read_csv('Inputfiles/LoadLocationsSpotfire.csv')

# ============================================================================
# PREGUNTA 1: ¿Hay E que no sean CBN?
# ============================================================================
print("\n" + "="*80)
print("1. ¿HAY TIPO E QUE NO SEAN CBN?")
print("="*80)

e_data = df[df['DeadloadType'] == 'E']
print(f"\nTotal registros tipo E: {len(e_data)}")
print("\nDistribución por LoadType y Hold:")
print(pd.crosstab(e_data['LoadType'], e_data['Hold']))

print("\nRESPUESTA: SÍ, hay E que no son CBN:")
print(f"- CBN (Cabin): {len(e_data[e_data['LoadType']=='CBN'])} registros (66%)")
print(f"- ULD: {len(e_data[e_data['LoadType']=='ULD'])} registros (28%)")
print(f"- BLK: {len(e_data[e_data['LoadType']=='BLK'])} registros (6%)")

print("\nEjemplos de E que NO son CBN:")
non_cbn_e = e_data[e_data['LoadType'] != 'CBN'][['DeadloadType', 'LoadType', 'Hold', 
                                                    'Weight', 'SerialNumber', 'LoadLocation']]
print(non_cbn_e.head(10))

# ============================================================================
# PREGUNTA 2: ¿Qué significan AFT, FWD, BLK, UNK?
# ============================================================================
print("\n" + "="*80)
print("2. SIGNIFICADO DE AFT, FWD, BLK, UNK")
print("="*80)

hold_meanings = {
    'AFT': 'Aft (Trasero) - Compartimiento trasero de carga',
    'FWD': 'Forward (Delantero) - Compartimiento delantero de carga',
    'BLK': 'Bulk (A granel) - Zona de carga suelta sin contenedor',
    'UNK': 'Unknown (Desconocido) - Posición no determinada'
}

print("\nSignificados:")
for hold, meaning in hold_meanings.items():
    count = len(df[df['Hold'] == hold])
    pct = count / len(df) * 100
    print(f"  {hold}: {meaning}")
    print(f"       → {count} registros ({pct:.1f}%)")

print("\nCaracterísticas por Hold:")
for hold in ['AFT', 'FWD', 'BLK', 'UNK']:
    hold_data = df[df['Hold'] == hold]
    print(f"\n{hold}:")
    print(f"  - Peso promedio: {hold_data['Weight'].mean():.1f} kg")
    print(f"  - DeadloadTypes: {hold_data['DeadloadType'].value_counts().to_dict()}")
    print(f"  - LoadTypes: {hold_data['LoadType'].value_counts().to_dict()}")

# ============================================================================
# PREGUNTA 3: ¿Por qué 8,562 registros tienen ModTime 16-2-2024 17:02:55?
# ============================================================================
print("\n" + "="*80)
print("3. ¿POR QUÉ 8,562 REGISTROS TIENEN EL MISMO MODTIME?")
print("="*80)

print(f"\nTotal ModTimes únicos: {df['ModTime'].nunique()}")
print("\nTop 5 ModTimes más frecuentes:")
print(df['ModTime'].value_counts().head())

modtime_analysis = df.groupby('ModTime').agg({
    'FlightLoadId': 'count',
    'DeadloadOrigin': lambda x: x.nunique(),
    'DeadloadDestination': lambda x: x.nunique()
}).rename(columns={'FlightLoadId': 'Records', 'DeadloadOrigin': 'Origins', 
                   'DeadloadDestination': 'Destinations'})

print("\nAnálisis del ModTime más frecuente (16-2-2024 17:02:55):")
most_common_modtime = df['ModTime'].value_counts().index[0]
most_common_data = df[df['ModTime'] == most_common_modtime]
print(f"  - Registros: {len(most_common_data)}")
print(f"  - Fechas de vuelo: {most_common_data['FlightLegDepartureKey'].str.split('|').str[0].nunique()} únicas")
print(f"  - Vuelos únicos: {most_common_data['FlightLegDepartureKey'].nunique()}")

print("\nRESPUESTA: ModTime NO es la fecha del vuelo.")
print("Es la fecha de extracción/procesamiento del reporte desde el sistema Spotfire.")
print("Un reporte puede contener datos de múltiples vuelos de diferentes fechas.")
print(f"El reporte del 16-Feb-2024 contiene {len(most_common_data)} registros de múltiples vuelos.")

# ============================================================================
# PREGUNTA 4: Líneas 708-711 - ¿Son repetidas?
# ============================================================================
print("\n" + "="*80)
print("4. LÍNEAS 708-711 - ¿SON REPETIDAS?")
print("="*80)

lines_708_711 = df.iloc[707:711]
print("\nDatos de las líneas 708-711:")
print(lines_708_711[['LoadId', 'DeadloadId', 'SpecialCargoId', 'Weight', 
                      'SerialNumber', 'SpecialHandlingCode']])

print("\nAnálisis:")
print(f"  - LoadId: {lines_708_711['LoadId'].nunique()} único (152397731)")
print(f"  - DeadloadId: {lines_708_711['DeadloadId'].nunique()} único (160008765)")
print(f"  - SpecialCargoId: {lines_708_711['SpecialCargoId'].nunique()} únicos")
print(f"  - Weight: {lines_708_711['Weight'].nunique()} valor (2175 kg en todos)")
print(f"  - SerialNumber: {lines_708_711['SerialNumber'].nunique()} único (PMC31780KL)")
print(f"  - SpecialHandlingCode: {lines_708_711['SpecialHandlingCode'].nunique()} únicos")

print("\nRESPUESTA: NO son líneas repetidas. Son registros VÁLIDOS.")
print("Representan el MISMO DeadloadId (2175 kg de carga) pero con MÚLTIPLES tipos")
print("de carga especial (RCM, ELM, RMD, EAT) que requieren tracking separado.")
print("\nEl peso es el mismo porque es el peso TOTAL del DeadloadId,")
print("pero cada SpecialCargoId registra un componente diferente de esa carga.")

# ============================================================================
# PREGUNTA 5: ¿Hay líneas completamente duplicadas?
# ============================================================================
print("\n" + "="*80)
print("5. ¿HAY LÍNEAS COMPLETAMENTE DUPLICADAS?")
print("="*80)

duplicates = df[df.duplicated(keep=False)]
print(f"\nLíneas completamente duplicadas: {len(duplicates)}")

if len(duplicates) > 0:
    print("\nEjemplos de duplicados:")
    print(duplicates.head())
else:
    print("\nRESPUESTA: NO hay líneas completamente duplicadas en el dataset.")

# Verificar duplicados en IDs clave
print("\n¿Hay duplicados en combinaciones de IDs?")
print(f"  - FlightLoadId duplicados: {df['FlightLoadId'].duplicated().sum()}")
print(f"  - LoadId duplicados: {df['LoadId'].duplicated().sum()} (normal - un ULD puede tener múltiples cargas)")
print(f"  - DeadloadId duplicados: {df['DeadloadId'].duplicated().sum()} (normal - por SpecialCargoId)")
print(f"  - (LoadId + DeadloadId) duplicados: {df[['LoadId', 'DeadloadId']].duplicated().sum()}")

# ============================================================================
# PREGUNTA 6: ¿Por qué hay menos UldGrossWeight count que Weight?
# ============================================================================
print("\n" + "="*80)
print("6. ¿POR QUÉ HAY MENOS ULDGROSSWEIGHT QUE WEIGHT?")
print("="*80)

print(f"\nWeight (no nulo): {df['Weight'].notna().sum()}")
print(f"UldGrossWeight (no nulo): {df['UldGrossWeight'].notna().sum()}")
print(f"Diferencia: {df['Weight'].notna().sum() - df['UldGrossWeight'].notna().sum()}")

# Analizar registros sin UldGrossWeight
no_gross = df[df['UldGrossWeight'].isna()]
print(f"\nRegistros sin UldGrossWeight: {len(no_gross)}")
print("\nDistribución por LoadType:")
print(no_gross['LoadType'].value_counts())

print("\nRESPUESTA: Los registros sin UldGrossWeight son:")
print(f"  - BLK (Bulk): {len(no_gross[no_gross['LoadType']=='BLK'])} → Carga suelta SIN contenedor")
print(f"  - CBN (Cabin): {len(no_gross[no_gross['LoadType']=='CBN'])} → Items de cabina SIN ULD")
print(f"  - ULD sin datos: {len(no_gross[no_gross['LoadType']=='ULD'])} → Posibles errores de datos")

print("\nConclusión: BLK y CBN NO tienen contenedor físico (ULD),")
print("por lo tanto NO tienen UldGrossWeight ni UldTareWeight.")

# ============================================================================
# PREGUNTA 7: ¿El ULD más liviano pesa 1kg?
# ============================================================================
print("\n" + "="*80)
print("7. ¿EL ULD MÁS LIVIANO PESA 1 KG?")
print("="*80)

tare_stats = df[df['UldTareWeight'].notna()]['UldTareWeight'].describe()
print("\nEstadísticas de UldTareWeight:")
print(tare_stats)

min_tare = df[df['UldTareWeight'].notna()]['UldTareWeight'].min()
min_tare_records = df[df['UldTareWeight'] == min_tare]

print(f"\nULD(s) más liviano(s) (TareWeight = {min_tare} kg):")
print(min_tare_records[['SerialNumber', 'UldTareWeight', 'UldGrossWeight', 
                         'Weight', 'DeadloadType']].drop_duplicates('SerialNumber'))

# Análisis de tipos de ULD
print("\nPesos típicos por tipo de ULD:")
df['ULD_Type'] = df['SerialNumber'].str[:3]
uld_weights = df[df['UldTareWeight'].notna()].groupby('ULD_Type')['UldTareWeight'].agg(['mean', 'min', 'max', 'count'])
uld_weights = uld_weights.sort_values('count', ascending=False).head(10)
print(uld_weights.round(1))

print("\nRESPUESTA: SÍ, hay ULD(s) con TareWeight de 1 kg.")
print("Son principalmente pallets tipo PLB.")
print("Esto probablemente indica:")
print("  - Pallet sin red/estructura (solo base)")
print("  - Error en los datos")
print("  - Pallet especial muy ligero")

# ============================================================================
# PREGUNTA 8: ¿DEADLOAD es carga y LOAD es contenedor?
# ============================================================================
print("\n" + "="*80)
print("8. ¿DEADLOAD ES CARGA Y LOAD ES CONTENEDOR?")
print("="*80)

print("\nTerminología aeronáutica:")
print("\n1. LOAD (LoadId):")
print("   - Representa el contenedor/ULD físico")
print("   - Un número único por ULD")
print(f"   - Total LoadIds únicos: {df['LoadId'].nunique()}")

print("\n2. DEADLOAD (DeadloadId):")
print("   - Representa un registro de carga dentro del ULD")
print("   - 'Dead' = carga inerte (no pasajeros, no tripulación)")
print("   - Incluye: equipaje, cargo, correo, etc.")
print(f"   - Total DeadloadIds únicos: {df['DeadloadId'].nunique()}")

# Ejemplo de jerarquía
sample_loadid = df[df['DeadloadId'].duplicated()]['LoadId'].iloc[0]
sample_data = df[df['LoadId'] == sample_loadid][['LoadId', 'DeadloadId', 'DeadloadType', 
                                                   'Weight', 'SerialNumber']].head()
print(f"\nEjemplo - LoadId {sample_loadid}:")
print(sample_data)

print("\nRESPUESTA: SÍ, exactamente.")
print("  - LOAD = Contenedor físico (ULD)")
print("  - DEADLOAD = Carga inerte dentro del contenedor")
print("\nUn LOAD puede contener múltiples DEADLOADs de diferentes tipos.")

# ============================================================================
# PREGUNTA 9: ¿Por qué a veces no tiene SerialNumber?
# ============================================================================
print("\n" + "="*80)
print("9. ¿POR QUÉ A VECES NO TIENE SERIALNUMBER?")
print("="*80)

print(f"\nRegistros con SerialNumber: {df['SerialNumber'].notna().sum()}")
print(f"Registros SIN SerialNumber: {df['SerialNumber'].isna().sum()}")

no_serial = df[df['SerialNumber'].isna()]
print("\nDistribución de registros SIN SerialNumber:")
print(f"  - Por LoadType: {no_serial['LoadType'].value_counts().to_dict()}")
print(f"  - Por DeadloadType: {no_serial['DeadloadType'].value_counts().to_dict()}")
print(f"  - Por Hold: {no_serial['Hold'].value_counts().to_dict()}")

print("\nRESPUESTA: No tienen SerialNumber porque NO son ULDs certificados.")
print("\nCasos sin SerialNumber:")
print("  1. BLK (Bulk) - Carga suelta sin contenedor")
print("  2. CBN (Cabin) - Items en cabina, no en bodega")
print("  3. Algunos registros de placeholder (tipo X)")
print("\nSolo los ULDs (Unit Load Devices) tienen SerialNumber.")

# ============================================================================
# RESUMEN FINAL
# ============================================================================
print("\n" + "="*80)
print("RESUMEN DE RESPUESTAS")
print("="*80)

summary = """
1. ¿Hay E que no sean CBN? 
   → SÍ: 66% CBN, 28% ULD, 6% BLK

2. Significado de AFT/FWD/BLK/UNK:
   → AFT = Trasero, FWD = Delantero, BLK = Bulk/A granel, UNK = Desconocido

3. ¿Por qué 8,562 registros con mismo ModTime?
   → ModTime = fecha de extracción del reporte, NO fecha del vuelo

4. Líneas 708-711 ¿son repetidas?
   → NO. Mismo DeadloadId con múltiples SpecialCargoIds

5. ¿Hay líneas duplicadas?
   → NO hay líneas completamente duplicadas

6. ¿Por qué menos UldGrossWeight que Weight?
   → BLK y CBN no tienen contenedor, por tanto no tienen UldGrossWeight

7. ¿ULD más liviano 1 kg?
   → SÍ. Pallets PLB con 1 kg (posible error o pallet sin estructura)

8. ¿Deadload = carga, Load = contenedor?
   → SÍ. Load = ULD físico, Deadload = carga inerte dentro

9. ¿Por qué sin SerialNumber?
   → BLK y CBN no son ULDs, por tanto no tienen SerialNumber
"""

print(summary)

print("\n" + "="*80)
print("ANÁLISIS COMPLETADO")
print("="*80)


