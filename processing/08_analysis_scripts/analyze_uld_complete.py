import pandas as pd

# Leer archivos
piece_info = pd.read_csv('Inputfiles/PieceInformationSpotfire.csv')
buildup = pd.read_csv('Inputfiles/BuildUpInformationSpotfire.csv')
loadloc = pd.read_csv('Inputfiles/LoadLocationsSpotfire.csv')

uld = 'AKE96298KL'
awb1 = '7459521221'

print("="*80)
print(f"ANÁLISIS COMPLETO DEL ULD: {uld}")
print("="*80)

# 1. BuildUp Information para este ULD
print("\n1. BUILDUP INFORMATION - ¿Qué AWBs hay en este ULD?")
print("-" * 80)
buildup_uld = buildup[buildup['OutgoingULDKey'] == uld]
print(f"Total líneas en BuildUp para {uld}: {len(buildup_uld)}")

# Agrupar por AWB
awb_summary = buildup_uld.groupby('AirWaybillNumber').agg({
    'NrBuildupPieces': 'sum',
    'TotalWeightOnAWB': 'first',
    'NumberOfPiecesOnAWB': 'first',
    'ULD': lambda x: ', '.join(x.unique()) if len(x.unique()) > 1 else x.iloc[0]
}).reset_index()

print("\nAWBs cargados en este ULD:")
for idx, row in awb_summary.iterrows():
    print(f"  AWB {row['AirWaybillNumber']}: {int(row['NrBuildupPieces'])} piezas cargadas de {int(row['NumberOfPiecesOnAWB'])} totales, {row['TotalWeightOnAWB']} kg")
    
total_buildup = awb_summary['NrBuildupPieces'].sum()
print(f"\nTotal piezas en BuildUp: {int(total_buildup)}")

# 2. Diferencias ULD vs OutgoingULDKey
print("\n\n2. ULD vs OUTGOING ULD KEY")
print("-" * 80)
buildup_awb1 = buildup[buildup['AirWaybillNumber'] == int(awb1)]
print(f"AWB {awb1} - columna ULD vs OutgoingULDKey:")
print(buildup_awb1[['ULD', 'OutgoingULDKey', 'AirWaybillStorageSequenceNumber', 'NrBuildupPieces']].to_string(index=False))

# Verificar si hay casos donde son diferentes
buildup['ULD_Different'] = buildup['ULD'] != buildup['OutgoingULDKey']
diff_cases = buildup[buildup['ULD_Different'] == True]
print(f"\n¿Hay casos donde ULD ≠ OutgoingULDKey? {len(diff_cases) > 0}")
if len(diff_cases) > 0:
    print(f"Total casos: {len(diff_cases)}")
    print("\nEjemplos:")
    print(diff_cases[['AirWaybillNumber', 'ULD', 'OutgoingULDKey', 'NrBuildupPieces']].head(5).to_string(index=False))

# 3. LoadLocations - peso total
print("\n\n3. LOAD LOCATIONS - Peso total del ULD")
print("-" * 80)
loadloc_uld = loadloc[loadloc['SerialNumber'] == uld]
if len(loadloc_uld) > 0:
    print(f"Registros en LoadLocations: {len(loadloc_uld)}")
    print(f"Peso (Weight): {loadloc_uld['Weight'].iloc[0]} {loadloc_uld['WeightUnit'].iloc[0]}")
    print(f"UldGrossWeight: {loadloc_uld['UldGrossWeight'].iloc[0]}")
    print(f"UldTareWeight: {loadloc_uld['UldTareWeight'].iloc[0]}")
    print(f"Peso Neto calculado: {loadloc_uld['UldGrossWeight'].iloc[0] - loadloc_uld['UldTareWeight'].iloc[0]}")

# 4. Análisis de pesos
print("\n\n4. ANÁLISIS DE PESOS - ¿Por qué 422.7 → 422 → 473?")
print("-" * 80)
piece_awb1 = piece_info[piece_info['BookingAirWaybillNumber'] == int(awb1)]
print(f"PieceInformation - BookingSegmentWeight: {piece_awb1['BookingSegmentWeight'].iloc[0]}")

buildup_awb1_weight = buildup_awb1['TotalWeightOnAWB'].iloc[0]
print(f"BuildUp - TotalWeightOnAWB: {buildup_awb1_weight}")

# Buscar el otro AWB en el ULD
other_awbs = buildup_uld[buildup_uld['AirWaybillNumber'] != int(awb1)]
if len(other_awbs) > 0:
    print(f"\nOtro AWB en el mismo ULD:")
    for awb_num in other_awbs['AirWaybillNumber'].unique():
        awb_data = buildup[buildup['AirWaybillNumber'] == awb_num]
        pieces_in_uld = buildup_uld[buildup_uld['AirWaybillNumber'] == awb_num]['NrBuildupPieces'].sum()
        total_pieces = awb_data['NumberOfPiecesOnAWB'].iloc[0]
        total_weight_str = awb_data['TotalWeightOnAWB'].iloc[0]
        
        # Convertir peso a número
        try:
            total_weight = float(str(total_weight_str).replace(',', '.'))
        except:
            total_weight = float(total_weight_str)
        
        # Calcular peso proporcional
        if total_pieces > 0:
            weight_in_uld = (pieces_in_uld / total_pieces) * total_weight
        else:
            weight_in_uld = 0
            
        print(f"  AWB {awb_num}: {int(pieces_in_uld)}/{int(total_pieces)} piezas → ~{weight_in_uld:.0f} kg de {total_weight:.0f} kg totales")

# 5. Estructura de PieceInformation
print("\n\n5. ESTRUCTURA DE PIECEINFORMATION - ¿289 líneas = 289 piezas?")
print("-" * 80)
print(f"Total líneas para AWB {awb1}: {len(piece_awb1)}")
print(f"BookingTotalPieceCount: {piece_awb1['BookingTotalPieceCount'].iloc[0]}")
print(f"BookingSegmentPieceCount: {piece_awb1['BookingSegmentPieceCount'].iloc[0]}")

# Convertir pesos
piece_awb1_copy = piece_awb1.copy()
piece_awb1_copy['LineWeightNum'] = piece_awb1_copy['BookingLinePieceWeight'].str.replace(',', '.').astype(float)
total_line_weight = piece_awb1_copy['LineWeightNum'].sum()
piece_awb1_copy['SegmentWeightNum'] = piece_awb1_copy['BookingSegmentPiecesWeight'].str.replace(',', '.').astype(float)

print(f"\nSuma de TODOS los BookingLinePieceWeight: {total_line_weight:.2f} kg")
print(f"BookingSegmentWeight: {piece_awb1['BookingSegmentWeight'].iloc[0]}")
print(f"Ratio: {total_line_weight / 422.70:.1f}x")

print("\n¡CONCLUSIÓN!")
print(f"  → Las 289 líneas representan 17 LÍNEAS DE BOOKING")
print(f"  → Cada línea de booking contiene las 17 piezas físicas")
print(f"  → 289 líneas / 17 piezas = {len(piece_awb1) / 17:.0f} líneas de booking")
print(f"  → PIEZAS FÍSICAS REALES: 17")

# 6. BookingSegmentPiecesWeight explicado
print("\n\n6. ¿QUÉ ES BookingSegmentPiecesWeight?")
print("-" * 80)
print("Ejemplo con BookingSegmentPiecesID = 3:")
piece3 = piece_awb1_copy[piece_awb1_copy['BookingSegmentPiecesID'] == 3].copy()
print(f"\nTotal líneas con PiecesID=3: {len(piece3)}")
print(f"BookingSegmentPiecesWeight (todas iguales): {piece3['BookingSegmentPiecesWeight'].iloc[0]}")
print(f"Suma de los 17 BookingLinePieceWeight: {piece3['LineWeightNum'].sum():.2f} kg")
print(f"\n→ BookingSegmentPiecesWeight = Peso de la pieza física #3")
print(f"→ BookingLinePieceWeight = Peso total de toda la línea de booking")
print(f"→ Cada una de las 17 líneas suma 422.70 kg (el peso total del AWB)")

