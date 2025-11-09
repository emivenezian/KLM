# KLM Fuel Optimization Project - Data Analysis Report

**Generated:** 2025-09-24 14:06:29

**Project:** KLM Fuel Optimization through Cargo Palletization and Weight Balance Modeling

**Author:** María Emilia Venezian Juricic

**Supervisor:** Dr. Felipe Delgado

**Institution:** Pontificia Universidad Católica de Chile

## Executive Summary

This report summarizes the data analysis completed for the KLM fuel optimization project, focusing on cargo palletization and weight balance modeling for intercontinental flights.

## Dataset Overview

- **Total Flights:** 525
- **Data Completeness:** 100.0%
- **Unique Routes:** 7
- **Total Cargo Items:** 34,765
- **Average Items per Flight:** 66.22
- **Total Passengers:** 2,960
- **Average Passengers per Flight:** 5.64

## Route Distribution

| Route | Flight Count | Percentage |
|-------|--------------|------------|
| AMSDEL | 91          | 17.33%     |
| AMSSIN | 90          | 17.14%     |
| AMSLAX | 89          | 16.95%     |
| AMSIAH | 67          | 12.76%     |
| AMSICN | 64          | 12.19%     |
| AMSSFO | 63          | 12.0%      |
| AMSBLR | 61          | 11.62%     |

## Aircraft Type Distribution

| Aircraft Type | Flight Count | Percentage |
|---------------|--------------|------------|
| 781 | 174 | 33.14% |
| 772 | 143 | 27.24% |
| 77W | 137 | 26.1% |
| 789 | 71 | 13.52% |

## Model Feasibility Comparison

| Model | Total Flights | Feasible Flights | Infeasible Flights | Feasibility Rate |
|-------|---------------|------------------|-------------------|-----------------|
| proposed_model | 185 | 102 | 83 | 55.14% |
| puttaert_model | 200 | 138 | 62 | 69.0% |

## Key Findings

- **Dataset Size:** 525 flights in original dataset
- **Data Completeness:** 100.0% of flights have complete data
- **Route Coverage:** 7 unique routes analyzed
- **Cargo Volume:** 34,765 total cargo items
- **Average Cargo Per Flight:** 66.22 items per flight
- **Passenger Volume:** 2,960 total passengers
- **Average Passengers Per Flight:** 5.64 passengers per flight

## Recommendations for Next Steps

1. Develop 3D-BPP heuristic (First-Fit Decreasing) to address geometric packing infeasibility
2. Test heuristic on identified infeasible flights
3. Optimize MILP constraints for improved feasibility
4. Run experiments on full dataset (525 flights)
5. Generate visualizations (heatmaps, 3D-BPP outputs)
6. Analyze results by aircraft type and route
7. Draft article sections with updated results

## Files Generated

- `flight_count_summary.csv` - Total flight count analysis
- `origin_destination_counts.csv` - Route distribution analysis
- `data_content_summary.csv` - Cargo and passenger data analysis
- `aircraft_type_distribution.csv` - Aircraft type distribution
- `model_feasibility_comparison.csv` - Model feasibility comparison
- `comprehensive_analysis_summary.csv` - Complete analysis summary
- `analysis_report.md` - This markdown report
