import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency

# Leer datos
piece_info = pd.read_csv('Inputfiles/PieceInformationSpotfire.csv')

print("="*100)
print("ANÁLISIS ESTADÍSTICO: Relación entre columnas")
print("="*100)

# Preparar datos
df = piece_info.copy()

# Crear columnas auxiliares
df['HasLineWeight'] = ~df['BookingLinePieceWeight'].isna()
df['HasSegmentWeight'] = ~df['BookingSegmentPiecesWeight'].isna()
df['HasDimensions'] = ~df['BookingLinePieceHeight'].isna()

print(f"\nTotal registros: {len(df)}")

# 1. ANÁLISIS DE BookingLinePieceIsInformational
print(f"\n{'='*100}")
print("1. DISTRIBUCIÓN DE BookingLinePieceIsInformational")
print(f"{'='*100}")

informational_counts = df['BookingLinePieceIsInformational'].value_counts()
print(f"\n{informational_counts}")
print(f"\nPorcentajes:")
print(f"{(informational_counts / len(df) * 100).round(2)}")

# 2. RELACIÓN CON BookingLinePieceWeight
print(f"\n{'='*100}")
print("2. RELACIÓN: IsInformational vs HasLineWeight")
print(f"{'='*100}")

cross_lineweight = pd.crosstab(
    df['BookingLinePieceIsInformational'], 
    df['HasLineWeight'],
    margins=True
)
print(f"\n{cross_lineweight}")

# Porcentajes
print(f"\nPorcentajes por fila:")
cross_pct = pd.crosstab(
    df['BookingLinePieceIsInformational'], 
    df['HasLineWeight'],
    normalize='index'
) * 100
print(f"{cross_pct.round(2)}")

# Chi-cuadrado
if len(df[df['BookingLinePieceIsInformational'] == True]) > 0:
    contingency = pd.crosstab(
        df['BookingLinePieceIsInformational'], 
        df['HasLineWeight']
    )
    chi2, p_value, dof, expected = chi2_contingency(contingency)
    print(f"\nTest Chi-cuadrado:")
    print(f"  Chi2 = {chi2:.2f}, p-value = {p_value:.4f}")
    if p_value < 0.05:
        print(f"  ✅ HAY relación estadísticamente significativa")
    else:
        print(f"  ❌ NO hay relación significativa")

# 3. RELACIÓN CON BookingSegmentPiecesID
print(f"\n{'='*100}")
print("3. RELACIÓN: IsInformational vs BookingSegmentPiecesID")
print(f"{'='*100}")

# Estadísticas por IsInformational
for is_info in [True, False]:
    subset = df[df['BookingLinePieceIsInformational'] == is_info]
    if len(subset) > 0:
        print(f"\nIsInformational = {is_info}:")
        print(f"  PiecesID mínimo: {subset['BookingSegmentPiecesID'].min()}")
        print(f"  PiecesID máximo: {subset['BookingSegmentPiecesID'].max()}")
        print(f"  PiecesID promedio: {subset['BookingSegmentPiecesID'].mean():.2f}")
        print(f"  PiecesID más común: {subset['BookingSegmentPiecesID'].mode().values}")
        
        # Distribución
        value_counts = subset['BookingSegmentPiecesID'].value_counts().head(10)
        print(f"  Top 10 valores:")
        for val, count in value_counts.items():
            print(f"    ID {val}: {count} veces ({count/len(subset)*100:.2f}%)")

# 4. ANÁLISIS POR AWB
print(f"\n{'='*100}")
print("4. ANÁLISIS A NIVEL AWB")
print(f"{'='*100}")

# Agrupar por AWB
awb_analysis = df.groupby('BookingAirWaybillNumber').agg({
    'BookingLinePieceIsInformational': lambda x: x.sum(),  # Cuántas son True
    'BookingAirWaybillNumber': 'count',  # Total líneas
    'BookingSegmentPiecesID': lambda x: x.nunique(),  # Piezas únicas
    'BookingTotalPieceCount': 'first'
}).rename(columns={
    'BookingLinePieceIsInformational': 'NumInformational',
    'BookingAirWaybillNumber': 'TotalLines',
    'BookingSegmentPiecesID': 'UniquePiecesID'
})

awb_analysis['PctInformational'] = (awb_analysis['NumInformational'] / awb_analysis['TotalLines'] * 100).round(2)

print(f"\nEstadísticas de AWBs:")
print(f"  AWBs con 0% líneas informacionales: {(awb_analysis['PctInformational'] == 0).sum()}")
print(f"  AWBs con 1-50% líneas informacionales: {((awb_analysis['PctInformational'] > 0) & (awb_analysis['PctInformational'] <= 50)).sum()}")
print(f"  AWBs con 51-99% líneas informacionales: {((awb_analysis['PctInformational'] > 50) & (awb_analysis['PctInformational'] < 100)).sum()}")
print(f"  AWBs con 100% líneas informacionales: {(awb_analysis['PctInformational'] == 100).sum()}")

# Mostrar ejemplos
print(f"\n\nEjemplos de AWBs con diferentes porcentajes:")
for pct in [0, 50, 100]:
    if pct == 0:
        example = awb_analysis[awb_analysis['PctInformational'] == pct].head(3)
    elif pct == 50:
        example = awb_analysis[(awb_analysis['PctInformational'] > 40) & (awb_analysis['PctInformational'] < 60)].head(3)
    else:
        example = awb_analysis[awb_analysis['PctInformational'] == 100].head(3)
    
    if len(example) > 0:
        print(f"\n  {pct}% informacionales:")
        print(example[['TotalLines', 'NumInformational', 'UniquePiecesID', 'BookingTotalPieceCount']])

# 5. PATRONES EN CASOS ESPECÍFICOS
print(f"\n{'='*100}")
print("5. ANÁLISIS DE PATRONES ESPECÍFICOS")
print(f"{'='*100}")

# Ejemplo: AWB 5703923673
awb_5703 = df[df['BookingAirWaybillNumber'] == 5703923673]
if len(awb_5703) > 0:
    print(f"\nAWB 5703923673 (3714 kg, 5 piezas):")
    cols_analyze = ['BookingSegmentPiecesID', 'BookingSegmentPiecesCount', 
                    'BookingLinePieceIsInformational', 'HasLineWeight', 'HasDimensions']
    print(awb_5703[cols_analyze].to_string(index=False))

# Ejemplo: AWB 7459521221
awb_7459 = df[df['BookingAirWaybillSerialNumber'].astype(str).str.contains('59521221', na=False)]
if len(awb_7459) > 0:
    print(f"\n\nAWB 7459521221 (422.70 kg, 17 piezas):")
    print(f"Total líneas: {len(awb_7459)}")
    print(f"Líneas informacionales: {awb_7459['BookingLinePieceIsInformational'].sum()}")
    
    # Ver distribución de PiecesID
    pieces_dist = awb_7459.groupby('BookingSegmentPiecesID').agg({
        'BookingLinePieceIsInformational': 'sum',
        'BookingSegmentPiecesID': 'count'
    }).rename(columns={'BookingSegmentPiecesID': 'Count', 'BookingLinePieceIsInformational': 'NumInformational'})
    print(f"\nDistribución por PiecesID (primeras 10):")
    print(pieces_dist.head(10))

# 6. HIPÓTESIS SOBRE LA RELACIÓN
print(f"\n{'='*100}")
print("6. HIPÓTESIS Y CONCLUSIONES")
print(f"{'='*100}")

print("""
OBSERVACIONES:

1. IsInformational vs HasLineWeight:
   - La gran mayoría de líneas tienen LineWeight (informacional o no)
   - IsInformational marca líneas con datos dimensionales REALES

2. IsInformational vs PiecesID:
   - No parece haber correlación directa con el valor numérico del ID
   - Más bien depende de la estructura del AWB

3. Patrones encontrados:
   a) AWBs con piezas IDÉNTICAS → Pocas líneas, algunas informacionales
   b) AWBs con piezas DIFERENTES → Muchas líneas (matriz), ninguna informacional
   
4. La clave es BookingSegmentPiecesCount:
   - Si > 1 → piezas idénticas → puede tener líneas informacionales
   - Si = 1 → piezas únicas → menos probable tener informacionales
""")

# 7. ANÁLISIS DE BookingSegmentPiecesCount
print(f"\n{'='*100}")
print("7. RELACIÓN: IsInformational vs BookingSegmentPiecesCount")
print(f"{'='*100}")

df['PiecesCountNum'] = pd.to_numeric(df['BookingSegmentPiecesCount'], errors='coerce')

for is_info in [True, False]:
    subset = df[df['BookingLinePieceIsInformational'] == is_info].copy()
    if len(subset) > 0:
        print(f"\nIsInformational = {is_info}:")
        print(f"  PiecesCount promedio: {subset['PiecesCountNum'].mean():.2f}")
        print(f"  PiecesCount mediana: {subset['PiecesCountNum'].median():.2f}")
        print(f"  PiecesCount mínimo: {subset['PiecesCountNum'].min():.2f}")
        print(f"  PiecesCount máximo: {subset['PiecesCountNum'].max():.2f}")
        
        # Distribución
        print(f"  Distribución:")
        for val in [1, 2, 3, 5, 10]:
            count = (subset['PiecesCountNum'] == val).sum()
            if count > 0:
                print(f"    Count = {val}: {count} líneas ({count/len(subset)*100:.2f}%)")
        
        count_gt_1 = (subset['PiecesCountNum'] > 1).sum()
        print(f"    Count > 1: {count_gt_1} líneas ({count_gt_1/len(subset)*100:.2f}%)")

# 8. TABLA DE CONTINGENCIA COMPLETA
print(f"\n{'='*100}")
print("8. TABLA DE CONTINGENCIA: IsInformational vs PiecesCount")
print(f"{'='*100}")

df['PiecesCount_Cat'] = pd.cut(df['PiecesCountNum'], 
                                bins=[0, 1, 2, 5, 10, float('inf')],
                                labels=['1', '2', '3-5', '6-10', '>10'])

cross_complete = pd.crosstab(
    df['BookingLinePieceIsInformational'],
    df['PiecesCount_Cat'],
    margins=True
)
print(f"\n{cross_complete}")

print(f"\n\nPorcentajes por fila (% dentro de cada IsInformational):")
cross_pct_row = pd.crosstab(
    df['BookingLinePieceIsInformational'],
    df['PiecesCount_Cat'],
    normalize='index'
) * 100
print(f"{cross_pct_row.round(2)}")

