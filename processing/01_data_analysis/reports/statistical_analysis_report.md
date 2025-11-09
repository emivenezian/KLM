# Comprehensive Statistical Analysis Report

**Generated:** 2025-09-26 09:33:15

## Executive Summary

This report provides comprehensive statistical analysis of all flight data metrics, including 95% confidence intervals, distribution characteristics, and breakdowns by route, aircraft type, and month.

## Overall Statistical Summary

| Metric | Count | Mean | Std Dev | Min | Max | Median | Q25 | Q75 | 95% CI Lower | 95% CI Upper | Skewness | Kurtosis |
|--------|-------|------|---------|-----|-----|--------|-----|-----|--------------|--------------|----------|----------|
| Cargo Items per Flight | 525 | 66.22 | 46.85 | 2 | 690 | 56.0 | 38.0 | 87.0 | 62.2 | 70.24 | 5.011 | 58.608 |
| Weight per Flight (kg) | 525 | 0.0 | 0.0 | 0 | 0 | 0.0 | 0.0 | 0.0 | nan | nan | nan | nan |
| Volume per Flight (cubic meters) | 525 | 0.0 | 0.0 | 0 | 0 | 0.0 | 0.0 | 0.0 | nan | nan | nan | nan |
| Passengers per Flight | 525 | 267.27 | 59.48 | 113 | 399 | 287.0 | 220.0 | 309.0 | 262.17 | 272.37 | -0.5 | -0.44 |
| ULDs per Flight | 525 | 39.5 | 14.18 | 18 | 164 | 36.0 | 31.0 | 44.0 | 38.28 | 40.71 | 3.582 | 20.539 |
| COL Items per Flight | 525 | 4.26 | 4.51 | 0 | 26 | 3.0 | 0.0 | 7.0 | 3.87 | 4.65 | 1.273 | 1.775 |
| CRT Items per Flight | 525 | 1.11 | 2.04 | 0 | 11 | 0.0 | 0.0 | 2.0 | 0.93 | 1.28 | 2.125 | 4.343 |

## Route Analysis

| Route | Flights | Avg Items | Items CI | Avg Weight | Weight CI | Avg Passengers | Passengers CI | Avg ULDs | ULDs CI |
|-------|---------|-----------|----------|------------|-----------|----------------|---------------|----------|----------|
| AMSBLR | 61 | 45.7 | [41.1, 50.3] | 0.0 | [nan, nan] | 246.1 | [233.1, 259.2] | 32.1 | [31.0, 33.1] |
| AMSDEL | 91 | 49.1 | [44.7, 53.5] | 0.0 | [nan, nan] | 327.7 | [320.3, 335.1] | 52.7 | [47.9, 57.5] |
| AMSSIN | 90 | 119.0 | [103.8, 134.3] | 0.0 | [nan, nan] | 198.6 | [190.3, 206.9] | 48.2 | [45.9, 50.5] |
| AMSIAH | 67 | 99.9 | [92.2, 107.6] | 0.0 | [nan, nan] | 223.7 | [211.0, 236.5] | 31.1 | [30.1, 32.1] |
| AMSSFO | 63 | 42.4 | [38.3, 46.5] | 0.0 | [nan, nan] | 274.7 | [264.1, 285.4] | 31.5 | [30.1, 32.8] |
| AMSICN | 64 | 56.7 | [51.1, 62.3] | 0.0 | [nan, nan] | 300.0 | [293.5, 306.4] | 36.3 | [34.4, 38.2] |
| AMSLAX | 89 | 42.8 | [38.5, 47.0] | 0.0 | [nan, nan] | 293.5 | [287.6, 299.4] | 36.7 | [35.4, 37.9] |

## Aircraft Type Analysis

| Aircraft | Flights | Avg Items | Items CI | Avg Weight | Weight CI | Avg Passengers | Passengers CI | Avg ULDs | ULDs CI |
|----------|---------|-----------|----------|------------|-----------|----------------|---------------|----------|----------|
| 789 | 71 | 77.8 | [69.1, 86.6] | 0.0 | [nan, nan] | 218.2 | [208.4, 228.0] | 30.9 | [30.1, 31.8] |
| 772 | 143 | 61.2 | [56.4, 66.0] | 0.0 | [nan, nan] | 269.3 | [259.9, 278.8] | 35.8 | [34.4, 37.2] |
| 781 | 174 | 46.2 | [42.5, 49.9] | 0.0 | [nan, nan] | 284.3 | [278.8, 289.8] | 37.2 | [35.4, 39.0] |
| 77W | 137 | 90.9 | [79.1, 102.7] | 0.0 | [nan, nan] | 268.9 | [255.9, 282.0] | 50.7 | [47.7, 53.8] |

## Monthly Analysis

| Month | Flights | Avg Items | Items CI | Avg Weight | Weight CI | Avg Passengers | Passengers CI | Avg ULDs | ULDs CI |
|-------|---------|-----------|----------|------------|-----------|----------------|---------------|----------|----------|
| FEB 2024 | 169 | 71.1 | [61.7, 80.5] | 0.0 | [nan, nan] | 262.2 | [252.6, 271.7] | 37.8 | [35.7, 39.8] |
| MAR 2024 | 183 | 72.3 | [66.9, 77.8] | 0.0 | [nan, nan] | 268.2 | [259.6, 276.8] | 41.3 | [38.8, 43.7] |
| JAN 2024 | 167 | 55.6 | [50.0, 61.1] | 0.0 | [nan, nan] | 270.8 | [262.1, 279.4] | 39.2 | [37.5, 41.0] |
| APR 2024 | 6 | 37.8 | [23.4, 52.2] | 0.0 | [nan, nan] | 285.2 | [222.0, 348.3] | 40.8 | [32.5, 49.2] |

## Key Statistical Insights

### Highest Variability: Passengers per Flight
- Standard Deviation: 59.48
- Coefficient of Variation: 22.3%
- 95% Confidence Interval: [262.17, 272.37]

### Lowest Variability: Weight per Flight (kg)
- Standard Deviation: 0.0
- Coefficient of Variation: nan%
- 95% Confidence Interval: [nan, nan]

## Distribution Characteristics

### Cargo Items per Flight
- **Skewness:** 5.011 (Right-skewed)
- **Kurtosis:** 58.608 (Heavy-tailed)
- **Range:** 688
- **IQR:** 49.0

### Weight per Flight (kg)
- **Skewness:** nan (Approximately normal)
- **Kurtosis:** nan (Normal-tailed)
- **Range:** 0
- **IQR:** 0.0

### Volume per Flight (cubic meters)
- **Skewness:** nan (Approximately normal)
- **Kurtosis:** nan (Normal-tailed)
- **Range:** 0
- **IQR:** 0.0

### Passengers per Flight
- **Skewness:** -0.5 (Approximately normal)
- **Kurtosis:** -0.44 (Normal-tailed)
- **Range:** 286
- **IQR:** 89.0

### ULDs per Flight
- **Skewness:** 3.582 (Right-skewed)
- **Kurtosis:** 20.539 (Heavy-tailed)
- **Range:** 146
- **IQR:** 13.0

### COL Items per Flight
- **Skewness:** 1.273 (Right-skewed)
- **Kurtosis:** 1.775 (Heavy-tailed)
- **Range:** 26
- **IQR:** 7.0

### CRT Items per Flight
- **Skewness:** 2.125 (Right-skewed)
- **Kurtosis:** 4.343 (Heavy-tailed)
- **Range:** 11
- **IQR:** 2.0

## Files Generated

- `comprehensive_statistics.csv` - Overall statistical summary
- `route_statistical_analysis.csv` - Statistics by route
- `aircraft_statistical_analysis.csv` - Statistics by aircraft type
- `month_statistical_analysis.csv` - Statistics by month
- `statistical_analysis_report.md` - This comprehensive report
