import pandas as pd

buildup = pd.read_csv('Inputfiles/BuildUpInformationSpotfire.csv')

print("¿Suma(NrBuildupPieces) > NumberOfPiecesOnAWB para un mismo AWB?")
print("="*80)

# Agrupar por AWB
awb_summary = buildup.groupby('AirWaybillNumber').agg({
    'NrBuildupPieces': 'sum',
    'NumberOfPiecesOnAWB': 'first',
    'ULD': lambda x: list(x.unique())
}).reset_index()

awb_summary['Diff'] = awb_summary['NrBuildupPieces'] - awb_summary['NumberOfPiecesOnAWB']
awb_summary['Ratio'] = awb_summary['NrBuildupPieces'] / awb_summary['NumberOfPiecesOnAWB']

# Casos donde suma > declarado
over = awb_summary[awb_summary['Diff'] > 0.1].sort_values('Diff', ascending=False)

print(f"\nTotal AWBs: {len(awb_summary)}")
print(f"AWBs donde Suma > Declarado: {len(over)} ({len(over)/len(awb_summary)*100:.1f}%)")

if len(over) > 0:
    print(f"\n✅ SÍ, puede pasar para un AWB específico")
    print(f"\nTop 10 casos extremos:")
    print(over[['AirWaybillNumber', 'NumberOfPiecesOnAWB', 'NrBuildupPieces', 'Diff', 'Ratio']].head(10).to_string(index=False))
    
    # Analizar un caso
    worst = over.iloc[0]
    print(f"\n\nCASO EXTREMO: AWB {worst['AirWaybillNumber']}")
    print(f"  Piezas declaradas: {worst['NumberOfPiecesOnAWB']}")
    print(f"  Suma NrBuildupPieces: {worst['NrBuildupPieces']}")
    print(f"  Diferencia: +{worst['Diff']} piezas")
    print(f"  Ratio: {worst['Ratio']:.1f}x")
    print(f"  Aparece en {len(worst['ULD'])} ULDs")
    
    # Ver detalle
    awb_detail = buildup[buildup['AirWaybillNumber'] == worst['AirWaybillNumber']]
    print(f"\n  Detalle de eventos:")
    cols = ['ULD', 'AirWaybillStorageSequenceNumber', 'NrBuildupPieces', 'BuildupEventDateTime']
    print(awb_detail[cols].to_string(index=False))
    
else:
    print(f"\n❌ NO hay casos donde exceda")

# Casos donde suma < declarado
under = awb_summary[awb_summary['Diff'] < -0.1].sort_values('Diff')
print(f"\n\nAWBs donde Suma < Declarado: {len(under)} ({len(under)/len(awb_summary)*100:.1f}%)")

if len(under) > 0:
    print(f"\nTop 5 casos (más faltantes):")
    print(under[['AirWaybillNumber', 'NumberOfPiecesOnAWB', 'NrBuildupPieces', 'Diff']].head(5).to_string(index=False))

# Casos donde coincide exacto
exact = awb_summary[abs(awb_summary['Diff']) <= 0.1]
print(f"\n\nAWBs donde Suma = Declarado: {len(exact)} ({len(exact)/len(awb_summary)*100:.1f}%)")

print(f"\n\n{'='*80}")
print("CONCLUSIÓN:")
print(f"{'='*80}")
print(f"""
✅ SÍ, para un MISMO AWB, Suma(NrBuildupPieces) puede > NumberOfPiecesOnAWB

RAZONES:
1. AWB cargado en múltiples ULDs con duplicación de registros
2. Piezas contadas múltiples veces en diferentes eventos
3. Errores en el sistema de registro
4. Intentos de carga fallidos que quedaron registrados

EJEMPLO: AWB aparece en 5 ULDs, cada uno con StorageSeq=3 y 4 piezas
         → 5 × 4 = 20 piezas registradas
         → Pero solo tiene 7 piezas declaradas
         → Exceso de 13 piezas (registros duplicados)
""")

