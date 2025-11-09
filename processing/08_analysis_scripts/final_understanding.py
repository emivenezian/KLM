import pandas as pd

piece_info = pd.read_csv('Inputfiles/PieceInformationSpotfire.csv')

print("="*100)
print("ENTENDIMIENTO FINAL - Comparación de 3 AWBs")
print("="*100)

# AWB 1: 58692362
awb1 = piece_info[piece_info['BookingAirWaybillSerialNumber'].astype(str).str.contains('58692362', na=False)]
# AWB 2: 7459521221
awb2 = piece_info[piece_info['BookingAirWaybillSerialNumber'].astype(str).str.contains('59521221', na=False)]
# AWB 3: 5703923673
awb3 = piece_info[piece_info['BookingAirWaybillNumber'] == 5703923673]

print("\n" + "="*100)
print("AWB 1: 58692362 (22 piezas)")
print("="*100)

if len(awb1) > 0:
    print(f"Total líneas: {len(awb1)}")
    print(f"BookingTotalPieceCount: {awb1['BookingTotalPieceCount'].iloc[0]}")
    
    # Separar líneas
    info_true = awb1[awb1['BookingLinePieceIsInformational'] == True]
    info_false = awb1[awb1['BookingLinePieceIsInformational'] == False]
    
    print(f"\nLíneas IsInformational=TRUE: {len(info_true)}")
    print(f"Líneas IsInformational=FALSE: {len(info_false)}")
    
    # Analizar la línea FALSE
    if len(info_false) > 0:
        print(f"\n  Línea FALSE:")
        print(f"    PiecesID: {info_false['BookingSegmentPiecesID'].iloc[0]}")
        print(f"    PiecesCount: {info_false['BookingSegmentPiecesCount'].iloc[0]}")
        print(f"    Tiene dimensiones: {info_false['BookingLinePieceHeight'].notna().any()}")
        print(f"    Tiene weight: {info_false['BookingLinePieceWeight'].notna().any()}")
    
    # Analizar líneas TRUE
    print(f"\n  Líneas TRUE:")
    counts_true = info_true.groupby('BookingSegmentPiecesID')['BookingSegmentPiecesCount'].first()
    print(f"    PiecesID: {sorted(info_true['BookingSegmentPiecesID'].unique())}")
    print(f"    Suma de PiecesCount: {counts_true.sum()}")
    print(f"    Todas tienen dimensiones: {info_true['BookingLinePieceHeight'].notna().all()}")
    
    print(f"\n✅ INTERPRETACIÓN:")
    print(f"  → PiecesID=1 (FALSE) es PLACEHOLDER con el total (Count=22)")
    print(f"  → PiecesID 2-13 (TRUE) son los datos REALES con dimensiones")
    print(f"  → {len(info_true)} tipos de piezas diferentes")
    print(f"  → Algunos tipos se repiten (Count > 1)")

print("\n" + "="*100)
print("AWB 2: 7459521221 (17 piezas)")
print("="*100)

if len(awb2) > 0:
    print(f"Total líneas: {len(awb2)}")
    print(f"BookingTotalPieceCount: {awb2['BookingTotalPieceCount'].iloc[0]}")
    
    info_true = awb2[awb2['BookingLinePieceIsInformational'] == True]
    info_false = awb2[awb2['BookingLinePieceIsInformational'] == False]
    
    print(f"\nLíneas IsInformational=TRUE: {len(info_true)}")
    print(f"Líneas IsInformational=FALSE: {len(info_false)}")
    
    print(f"\nTodas las líneas:")
    print(f"  Todas tienen dimensiones: {awb2['BookingLinePieceHeight'].notna().all()}")
    print(f"  PiecesID únicos: {len(awb2['BookingSegmentPiecesID'].unique())}")
    print(f"  BookingSegmentPiecesCount: todos = {awb2['BookingSegmentPiecesCount'].unique()}")
    
    print(f"\n✅ INTERPRETACIÓN:")
    print(f"  → TODAS las líneas son FALSE (matriz cartesiana)")
    print(f"  → SÍ tienen dimensiones pero son ESTIMADAS/CALCULADAS")
    print(f"  → NO hay línea placeholder")
    print(f"  → Sistema generó 17×17=289 líneas para análisis")

print("\n" + "="*100)
print("AWB 3: 5703923673 (5 piezas)")
print("="*100)

if len(awb3) > 0:
    print(f"Total líneas: {len(awb3)}")
    print(f"BookingTotalPieceCount: {awb3['BookingTotalPieceCount'].iloc[0]}")
    
    info_true = awb3[awb3['BookingLinePieceIsInformational'] == True]
    info_false = awb3[awb3['BookingLinePieceIsInformational'] == False]
    
    print(f"\nLíneas IsInformational=TRUE: {len(info_true)}")
    print(f"Líneas IsInformational=FALSE: {len(info_false)}")
    
    for is_info in [False, True]:
        subset = awb3[awb3['BookingLinePieceIsInformational'] == is_info]
        if len(subset) > 0:
            print(f"\n  IsInformational={is_info}:")
            print(f"    PiecesID: {subset['BookingSegmentPiecesID'].iloc[0]}")
            print(f"    PiecesCount: {subset['BookingSegmentPiecesCount'].iloc[0]}")
            print(f"    Tiene dimensiones: {subset['BookingLinePieceHeight'].notna().any()}")
    
    print(f"\n✅ INTERPRETACIÓN:")
    print(f"  → PiecesID=1 (FALSE) sin dimensiones")
    print(f"  → PiecesID=2 (TRUE) con dimensiones reales")
    print(f"  → 5 piezas IDÉNTICAS (Count=5)")

print("\n" + "="*100)
print("CONCLUSIÓN FINAL")
print("="*100)

print("""
REGLA CORRECTA:

1. IsInformational NO depende de si tiene dimensiones
   ❌ FALSO: "Si no tiene dimensiones → IsInformational=FALSE"
   ✅ VERDAD: IsInformational marca qué líneas usar para los cálculos

2. Patrones encontrados:

   TIPO A: AWB con datos completos (58692362, 5703923673)
   ─────────────────────────────────────────────────────
   - PiecesID=1: IsInformational=FALSE
     → Línea de metadata/placeholder sin dimensiones
     → BookingSegmentPiecesCount = total de piezas
     
   - PiecesID≥2: IsInformational=TRUE
     → Datos REALES con dimensiones
     → BookingSegmentPiecesCount = cuántas de cada tipo
     → USAR ESTAS LÍNEAS para optimización
   
   
   TIPO B: AWB sin datos informativos (7459521221)
   ─────────────────────────────────────────────────────
   - TODAS las líneas: IsInformational=FALSE
     → Matriz cartesiana (17×17=289 líneas)
     → SÍ tienen dimensiones pero son calculadas/estimadas
     → Usar BookingSegmentVolume para estimar
     → El código filtra donde SegmentWeight ≈ LineWeight

3. BookingSegmentPiecesCount:
   
   - En placeholder (ID=1): Suma total de todas las piezas
   - En datos reales (ID≥2): Cuántas piezas IDÉNTICAS de ese tipo
   
   Ejemplo AWB 58692362:
   - ID=1: Count=22 (placeholder - total)
   - ID=2: Count=1  (1 pieza única)
   - ID=7: Count=2  (2 piezas idénticas)
   - ID=13: Count=4 (4 piezas idénticas)
   → Suma de ID 2-13 = 22 piezas reales ✓

4. ¿Cuándo usar qué?

   if hay líneas con IsInformational=TRUE:
       → Filtrar SOLO las TRUE
       → Usar sus dimensiones directamente
       → Repetir Count veces para piezas idénticas
   
   else:
       → NO hay datos informativos
       → Usar BookingSegmentVolume para estimar
       → Filtrar líneas donde SegmentWeight ≈ LineWeight

EL CÓDIGO ACTUAL EN Classes.ipynb YA HACE ESTO CORRECTAMENTE! ✅
""")

