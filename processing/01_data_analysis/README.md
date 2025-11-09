# 01_data_analysis

This directory contains comprehensive data analysis scripts and results for the KLM Fuel Optimization Project.

## Directory Structure

```
01_data_analysis/
├── data/                           # CSV data files
│   ├── comprehensive_flight_analysis.csv    # Complete flight analysis with COL/CRT counts
│   ├── comprehensive_statistics.csv         # Overall statistical summary
│   ├── route_statistical_analysis.csv       # Statistics by route
│   ├── aircraft_statistical_analysis.csv    # Statistics by aircraft type
│   ├── month_statistical_analysis.csv       # Statistics by month
│   ├── route_month_breakdown.csv           # Route-month matrix
│   ├── route_statistics.csv                # Route summary statistics
│   ├── month_statistics.csv                # Month summary statistics
│   └── comprehensive_data_summary.csv      # Overall data summary
├── reports/                        # Markdown reports
│   ├── comprehensive_data_report.md        # Complete data analysis report
│   └── statistical_analysis_report.md      # Statistical analysis report
├── scripts/                        # Python analysis scripts
│   ├── comprehensive_data_analysis.py      # Main data analysis script
│   ├── statistical_analysis_report.py     # Statistical analysis script
│   └── flight_count_and_route_analysis.py # Route analysis script
└── README.md                       # This file
```

## Key Findings

### Data Overview
- **Total Flights:** 525 complete flights
- **Routes:** 7 active routes (AMSDEL, AMSSIN, AMSLAX, AMSIAH, AMSICN, AMSSFO, AMSBLR)
- **Aircraft Types:** Boeing 787-10 (33%), 777-200 (27%), 777-300ER (26%), 787-9 (14%)
- **Data Completeness:** 100% complete (all 5 required CSV files present)

### Cargo Statistics
- **Total Items:** 34,765 cargo items
- **Average Items per Flight:** 66.22
- **COL Items per Flight:** 4.26 (mean), 95% CI [3.87, 4.65]
- **CRT Items per Flight:** 1.11 (mean), 95% CI [0.93, 1.28]
- **Passengers per Flight:** 267.27 (mean), 95% CI [262.17, 272.37]
- **ULDs per Flight:** 39.5 (mean), 95% CI [38.28, 40.71]

### Route Analysis
- **AMSSIN:** Most problematic route (119.0 avg items/flight)
- **AMSIAH:** Most stable route (99.9 avg items/flight)
- **AMSBLR:** Moderate complexity (45.7 avg items/flight)

## Scripts Description

### comprehensive_data_analysis.py
- Analyzes all 525 flights in the dataset
- Extracts COL and CRT items from PieceInformation.csv (IsCOL, IsCRT columns)
- Generates comprehensive flight analysis with all metrics
- Creates route and month breakdowns

### statistical_analysis_report.py
- Performs detailed statistical analysis on all metrics
- Calculates 95% confidence intervals
- Analyzes distribution characteristics (skewness, kurtosis)
- Generates breakdowns by route, aircraft type, and month

### flight_count_and_route_analysis.py
- Analyzes flight counts and route patterns
- Identifies data completeness issues
- Generates route-specific statistics

## Data Sources

- **Input:** `KLM_Projects/KLM_Original/Data/` (read-only)
- **Output:** Files saved in appropriate subdirectories (`data/`, `reports/`)

## File Organization Rules

Following Cursor project rules:
- **CSV files:** Saved in `data/` subdirectory
- **Markdown reports:** Saved in `reports/` subdirectory  
- **Python scripts:** Located in `scripts/` subdirectory
- **No files in root directories** (except README.md)

## Usage

To run the complete analysis:

```bash
cd scripts/
python comprehensive_data_analysis.py
python statistical_analysis_report.py
```

## Recent Updates

- **Fixed COL/CRT counting:** Corrected to use IsCOL/IsCRT boolean columns from PieceInformation.csv
- **Updated file organization:** Moved all files to appropriate subdirectories
- **Enhanced statistical analysis:** Added 95% confidence intervals and distribution analysis
