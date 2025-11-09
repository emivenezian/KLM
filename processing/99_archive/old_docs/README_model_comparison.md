# Model Comparison Tool

This tool compares metrics between old and new cargo optimization models for KLM flights. It processes output files from both models and generates detailed comparisons, statistics, and visualizations.

## Features

- Processes multiple flights automatically
- Extracts metrics from Model_Information.txt and General_Information.txt files
- Generates detailed CSV comparisons
- Creates summary statistics
- Produces visualization plots
- Handles errors gracefully with logging

## Requirements

- Python 3.6+
- Required packages:
  - pandas
  - matplotlib
  - seaborn

Install requirements:
```bash
pip install pandas matplotlib seaborn
```

## Usage

Run the script from the command line:

```bash
python compare_models.py --old-model /path/to/old/model/results --new-model /path/to/new/model/results --output /path/to/output
```

### Arguments

- `--old-model`: Path to the directory containing old model results
- `--new-model`: Path to the directory containing new model results
- `--output`: Path where comparison results will be saved

### Example

```bash
python compare_models.py --old-model Results_Baseline --new-model Results_Optimized_Actual --output comparison_results
```

## Output Files

The script generates the following files in the output directory:

1. `detailed_comparison.csv`: Contains all metrics and their comparisons
   - Flight identifier
   - Category (Model Information or General Information)
   - Metric name
   - Old model value
   - New model value
   - Difference
   - Percentage change

2. `summary_statistics.csv`: Aggregated statistics for each metric
   - Mean difference
   - Standard deviation of differences
   - Mean percentage change
   - Standard deviation of percentage changes

3. `time_comparison.png`: Bar plot showing total time differences by flight

4. `items_fit_comparison.png`: Bar plot showing items fit differences by flight

5. `model_comparison.log`: Log file with processing details and any errors

## Metrics Extracted

### Model Information
- Number of iterations
- Total optimization time
- 1D BPP WB time
- 3D BPP time

### General Information
- Flight details (number, aircraft type, departure, arrival, date)
- Weights (ZFW, TOW, LW, OEW)
- Fuel information
- ULD counts (Cargo, BAX, BUP, T)
- Passenger distribution
- Item fit statistics

## Error Handling

The script includes comprehensive error handling:
- Logs errors without stopping execution
- Continues processing other flights if one fails
- Records parsing errors in the log file

## Extending the Script

To add new metrics:
1. Add new regex patterns in the `parse_model_info` or `parse_general_info` methods
2. Add the new metrics to the metrics dictionary
3. The comparison and visualization will automatically include the new metrics

## Notes

- The script assumes consistent file naming across all flight directories
- Missing files or malformed data are logged but don't stop execution
- Non-numeric metrics are preserved without calculating differences 