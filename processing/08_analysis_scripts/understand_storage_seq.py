import pandas as pd

buildup = pd.read_csv('Inputfiles/BuildUpInformationSpotfire.csv')

print("¿Por qué mismo AWB + StorageSeq en múltiples ULDs?")
print("="*80)

# Caso extremo
awb = 7463867856
awb_data = buildup[buildup['AirWaybillNumber'] == awb]

print(f"\nAWB {awb}:")
print(f"Piezas declaradas: {awb_data['NumberOfPiecesOnAWB'].iloc[0]}")

# Agrupar por StorageSeq
print(f"\nPor StorageSequenceNumber:")
for seq in sorted(awb_data['AirWaybillStorageSequenceNumber'].unique())[:10]:
    seq_data = awb_data[awb_data['AirWaybillStorageSequenceNumber'] == seq]
    ulds = seq_data['ULD'].unique()
    total_pieces = seq_data['NrBuildupPieces'].sum()
    
    print(f"\n  StorageSeq {int(seq)}:")
    print(f"    ULDs: {len(ulds)}")
    print(f"    Total NrBuildupPieces: {total_pieces}")
    print(f"    Detalles:")
    for uld in ulds[:5]:
        pieces = seq_data[seq_data['ULD'] == uld]['NrBuildupPieces'].iloc[0]
        time = seq_data[seq_data['ULD'] == uld]['BuildupEventDateTime'].iloc[0]
        print(f"      {uld}: {pieces} piezas ({time})")

# HIPÓTESIS: Múltiples intentos de carga
print(f"\n\n{'='*80}")
print("HIPÓTESIS:")
print(f"{'='*80}")

print("""
¿Por qué mismo StorageSeq en múltiples ULDs?

POSIBLES RAZONES:

1. CARGA PARALELA:
   - Mismo lote/pallet dividido entre varios ULDs
   - StorageSeq identifica el lote origen, no el ULD destino
   - Sistema registra cada "pieza" del lote en cada ULD

2. INTENTOS FALLIDOS:
   - Intentaron cargar en ULD A → fallido
   - Intentaron cargar en ULD B → fallido  
   - Intentaron cargar en ULD C → exitoso
   - Pero quedaron registrados todos los intentos

3. SPLITS/REORGANIZACIÓN:
   - Lote original dividido entre ULDs
   - Cada ULD recibe parte del mismo lote
   - Pero sistema registra el total en cada uno

4. ERROR DE SISTEMA:
   - Bug en sistema de registro
   - Duplicación automática de registros
""")

# Verificar horarios
print(f"\n\n{'='*80}")
print("VERIFICACIÓN: ¿Son simultáneos o secuenciales?")
print(f"{'='*80}")

# Ver StorageSeq 27 en detalle
seq_27 = awb_data[awb_data['AirWaybillStorageSequenceNumber'] == 27]
print(f"\nStorageSeq 27 - {len(seq_27)} registros:")
print(seq_27[['ULD', 'NrBuildupPieces', 'BuildupEventDateTime']].sort_values('BuildupEventDateTime').to_string(index=False))

# Analizar si siempre es el mismo NrBuildupPieces
pieces_same = seq_27['NrBuildupPieces'].nunique() == 1
print(f"\n¿Mismo NrBuildupPieces en todos? {pieces_same}")
if pieces_same:
    print(f"Valor: {seq_27['NrBuildupPieces'].iloc[0]} piezas")
    print(f"\n→ ¡CLAVE! Todos tienen el MISMO número de piezas")
    print(f"→ Significa: NO es que cada ULD reciba parte")
    print(f"→ Significa: Es DUPLICACIÓN del mismo registro")

# Buscar caso más simple
print(f"\n\n{'='*80}")
print("CASO SIMPLE para entender:")
print(f"{'='*80}")

# AWB en 2 ULDs con mismo StorageSeq
multi = buildup.groupby('AirWaybillNumber').agg({
    'ULD': lambda x: x.nunique(),
    'AirWaybillStorageSequenceNumber': lambda x: x.nunique()
}).reset_index()
multi = multi[(multi['ULD'] > 1) & (multi['AirWaybillStorageSequenceNumber'] < 5)]

if len(multi) > 0:
    simple_awb = multi.iloc[0]['AirWaybillNumber']
    simple_data = buildup[buildup['AirWaybillNumber'] == simple_awb]
    
    print(f"\nAWB {simple_awb}:")
    print(f"Piezas declaradas: {simple_data['NumberOfPiecesOnAWB'].iloc[0]}")
    print(f"ULDs: {simple_data['ULD'].nunique()}")
    print(f"\nDetalle:")
    cols = ['ULD', 'AirWaybillStorageSequenceNumber', 'NrBuildupPieces', 'BuildupEventDateTime']
    print(simple_data[cols].to_string(index=False))

print(f"\n\n{'='*80}")
print("CONCLUSIÓN:")
print(f"{'='*80}")
print("""
NrBuildupPieces = piezas que se INTENTARON cargar en ese lote

Cuando mismo AWB + StorageSeq aparece en múltiples ULDs:
→ Sistema registró múltiples intentos/ubicaciones
→ PERO las piezas físicas existen solo 1 vez
→ Registros duplicados = intentos, errores o splits

Para optimización:
→ NO sumar todos los NrBuildupPieces
→ Usar solo registros del ULD FINAL (probablemente en LoadLocations)
→ O filtrar por fecha más reciente
→ O usar IsNotBuildUp para descartar fallidos
""")

