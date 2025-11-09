#!/usr/bin/env python3
"""
Comprehensive Statistical Analysis for KLM Fuel Optimization Project
Calculates detailed statistics including 95% confidence intervals for all metrics
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from scipy import stats
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class StatisticalAnalyzer:
    def __init__(self, results_path):
        self.results_path = Path(results_path)
        self.processing_path = Path(".")
        self.processing_path.mkdir(parents=True, exist_ok=True)
        
    def calculate_comprehensive_statistics(self, data, metric_name):
        """Calculate comprehensive statistics including 95% CI"""
        if len(data) == 0:
            return {
                'metric': metric_name,
                'count': 0,
                'mean': 0,
                'std': 0,
                'min': 0,
                'max': 0,
                'median': 0,
                'q25': 0,
                'q75': 0,
                'ci_95_lower': 0,
                'ci_95_upper': 0,
                'skewness': 0,
                'kurtosis': 0
            }
        
        # Basic statistics
        count = len(data)
        mean = np.mean(data)
        std = np.std(data, ddof=1)  # Sample standard deviation
        min_val = np.min(data)
        max_val = np.max(data)
        median = np.median(data)
        q25 = np.percentile(data, 25)
        q75 = np.percentile(data, 75)
        
        # 95% Confidence Interval
        if count > 1:
            ci_95 = stats.t.interval(0.95, count-1, loc=mean, scale=stats.sem(data))
            ci_95_lower = ci_95[0]
            ci_95_upper = ci_95[1]
        else:
            ci_95_lower = mean
            ci_95_upper = mean
        
        # Distribution shape
        skewness = stats.skew(data)
        kurtosis = stats.kurtosis(data)
        
        return {
            'metric': metric_name,
            'count': count,
            'mean': round(mean, 2),
            'std': round(std, 2),
            'min': round(min_val, 2),
            'max': round(max_val, 2),
            'median': round(median, 2),
            'q25': round(q25, 2),
            'q75': round(q75, 2),
            'ci_95_lower': round(ci_95_lower, 2),
            'ci_95_upper': round(ci_95_upper, 2),
            'skewness': round(skewness, 3),
            'kurtosis': round(kurtosis, 3)
        }
    
    def analyze_flight_data_statistics(self):
        """Analyze comprehensive statistics for all flight data"""
        logger.info("Starting comprehensive statistical analysis...")
        
        # Load the comprehensive flight analysis
        analysis_file = self.processing_path / "data" / "comprehensive_flight_analysis.csv"
        if not analysis_file.exists():
            logger.error(f"Analysis file not found: {analysis_file}")
            return None
        
        df = pd.read_csv(analysis_file)
        logger.info(f"Loaded {len(df)} flight records for statistical analysis")
        
        # Analyze different metrics
        metrics_to_analyze = {
            'total_items': 'Cargo Items per Flight',
            'total_weight': 'Weight per Flight (kg)',
            'total_volume': 'Volume per Flight (cubic meters)',
            'passenger_count': 'Passengers per Flight',
            'uld_count': 'ULDs per Flight',
            'col_items': 'COL Items per Flight',
            'crt_items': 'CRT Items per Flight'
        }
        
        all_statistics = []
        
        for column, description in metrics_to_analyze.items():
            if column in df.columns:
                # Remove any NaN values
                data = df[column].dropna()
                data = data[data >= 0]  # Remove negative values if any
                
                stats_result = self.calculate_comprehensive_statistics(data, description)
                all_statistics.append(stats_result)
                
                logger.info(f"{description}: Mean={stats_result['mean']}, CI95=[{stats_result['ci_95_lower']}, {stats_result['ci_95_upper']}]")
        
        # Create comprehensive statistics DataFrame
        stats_df = pd.DataFrame(all_statistics)
        
        # Save detailed statistics
        stats_path = self.processing_path / "data" / "comprehensive_statistics.csv"
        stats_df.to_csv(stats_path, index=False)
        
        # Analyze by route
        route_stats = self.analyze_by_route(df)
        
        # Analyze by aircraft type
        aircraft_stats = self.analyze_by_aircraft(df)
        
        # Analyze by month
        month_stats = self.analyze_by_month(df)
        
        # Generate detailed report
        self.generate_statistical_report(stats_df, route_stats, aircraft_stats, month_stats)
        
        return stats_df, route_stats, aircraft_stats, month_stats
    
    def analyze_by_route(self, df):
        """Analyze statistics by route"""
        logger.info("Analyzing statistics by route...")
        
        route_analysis = []
        
        for route in df['route'].unique():
            route_data = df[df['route'] == route]
            
            route_stats = {
                'route': route,
                'flight_count': len(route_data),
                'avg_items': route_data['total_items'].mean(),
                'avg_weight': route_data['total_weight'].mean(),
                'avg_volume': route_data['total_volume'].mean(),
                'avg_passengers': route_data['passenger_count'].mean(),
                'avg_ulds': route_data['uld_count'].mean(),
                'avg_col_items': route_data['col_items'].mean(),
                'avg_crt_items': route_data['crt_items'].mean()
            }
            
            # Calculate 95% CI for key metrics
            for metric in ['total_items', 'total_weight', 'total_volume', 'passenger_count', 'uld_count']:
                if metric in route_data.columns:
                    data = route_data[metric].dropna()
                    if len(data) > 1:
                        ci = stats.t.interval(0.95, len(data)-1, loc=data.mean(), scale=stats.sem(data))
                        route_stats[f'{metric}_ci_lower'] = round(ci[0], 2)
                        route_stats[f'{metric}_ci_upper'] = round(ci[1], 2)
                    else:
                        route_stats[f'{metric}_ci_lower'] = data.mean() if len(data) > 0 else 0
                        route_stats[f'{metric}_ci_upper'] = data.mean() if len(data) > 0 else 0
            
            route_analysis.append(route_stats)
        
        route_df = pd.DataFrame(route_analysis)
        route_path = self.processing_path / "data" / "route_statistical_analysis.csv"
        route_df.to_csv(route_path, index=False)
        
        return route_df
    
    def analyze_by_aircraft(self, df):
        """Analyze statistics by aircraft type"""
        logger.info("Analyzing statistics by aircraft type...")
        
        aircraft_analysis = []
        
        for aircraft in df['aircraft_type'].dropna().unique():
            aircraft_data = df[df['aircraft_type'] == aircraft]
            
            aircraft_stats = {
                'aircraft_type': aircraft,
                'flight_count': len(aircraft_data),
                'avg_items': aircraft_data['total_items'].mean(),
                'avg_weight': aircraft_data['total_weight'].mean(),
                'avg_volume': aircraft_data['total_volume'].mean(),
                'avg_passengers': aircraft_data['passenger_count'].mean(),
                'avg_ulds': aircraft_data['uld_count'].mean(),
                'avg_col_items': aircraft_data['col_items'].mean(),
                'avg_crt_items': aircraft_data['crt_items'].mean()
            }
            
            # Calculate 95% CI for key metrics
            for metric in ['total_items', 'total_weight', 'total_volume', 'passenger_count', 'uld_count']:
                if metric in aircraft_data.columns:
                    data = aircraft_data[metric].dropna()
                    if len(data) > 1:
                        ci = stats.t.interval(0.95, len(data)-1, loc=data.mean(), scale=stats.sem(data))
                        aircraft_stats[f'{metric}_ci_lower'] = round(ci[0], 2)
                        aircraft_stats[f'{metric}_ci_upper'] = round(ci[1], 2)
                    else:
                        aircraft_stats[f'{metric}_ci_lower'] = data.mean() if len(data) > 0 else 0
                        aircraft_stats[f'{metric}_ci_upper'] = data.mean() if len(data) > 0 else 0
            
            aircraft_analysis.append(aircraft_stats)
        
        aircraft_df = pd.DataFrame(aircraft_analysis)
        aircraft_path = self.processing_path / "data" / "aircraft_statistical_analysis.csv"
        aircraft_df.to_csv(aircraft_path, index=False)
        
        return aircraft_df
    
    def analyze_by_month(self, df):
        """Analyze statistics by month"""
        logger.info("Analyzing statistics by month...")
        
        # Extract month from flight path
        df['month'] = df['flight_path'].str.extract(r'(JAN|FEB|MAR|APR) 2024')
        
        month_analysis = []
        
        for month in df['month'].dropna().unique():
            month_data = df[df['month'] == month]
            
            month_stats = {
                'month': f"{month} 2024",
                'flight_count': len(month_data),
                'avg_items': month_data['total_items'].mean(),
                'avg_weight': month_data['total_weight'].mean(),
                'avg_volume': month_data['total_volume'].mean(),
                'avg_passengers': month_data['passenger_count'].mean(),
                'avg_ulds': month_data['uld_count'].mean(),
                'avg_col_items': month_data['col_items'].mean(),
                'avg_crt_items': month_data['crt_items'].mean()
            }
            
            # Calculate 95% CI for key metrics
            for metric in ['total_items', 'total_weight', 'total_volume', 'passenger_count', 'uld_count']:
                if metric in month_data.columns:
                    data = month_data[metric].dropna()
                    if len(data) > 1:
                        ci = stats.t.interval(0.95, len(data)-1, loc=data.mean(), scale=stats.sem(data))
                        month_stats[f'{metric}_ci_lower'] = round(ci[0], 2)
                        month_stats[f'{metric}_ci_upper'] = round(ci[1], 2)
                    else:
                        month_stats[f'{metric}_ci_lower'] = data.mean() if len(data) > 0 else 0
                        month_stats[f'{metric}_ci_upper'] = data.mean() if len(data) > 0 else 0
            
            month_analysis.append(month_stats)
        
        month_df = pd.DataFrame(month_analysis)
        month_path = self.processing_path / "data" / "month_statistical_analysis.csv"
        month_df.to_csv(month_path, index=False)
        
        return month_df
    
    def generate_statistical_report(self, stats_df, route_stats, aircraft_stats, month_stats):
        """Generate comprehensive statistical report"""
        logger.info("Generating comprehensive statistical report...")
        
        report_path = self.processing_path / "reports" / "statistical_analysis_report.md"
        
        with open(report_path, 'w') as f:
            f.write(f"# Comprehensive Statistical Analysis Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## Executive Summary\n\n")
            f.write("This report provides comprehensive statistical analysis of all flight data metrics, including 95% confidence intervals, distribution characteristics, and breakdowns by route, aircraft type, and month.\n\n")
            
            f.write("## Overall Statistical Summary\n\n")
            f.write("| Metric | Count | Mean | Std Dev | Min | Max | Median | Q25 | Q75 | 95% CI Lower | 95% CI Upper | Skewness | Kurtosis |\n")
            f.write("|--------|-------|------|---------|-----|-----|--------|-----|-----|--------------|--------------|----------|----------|\n")
            
            for _, row in stats_df.iterrows():
                f.write(f"| {row['metric']} | {row['count']} | {row['mean']} | {row['std']} | {row['min']} | {row['max']} | {row['median']} | {row['q25']} | {row['q75']} | {row['ci_95_lower']} | {row['ci_95_upper']} | {row['skewness']} | {row['kurtosis']} |\n")
            
            f.write("\n## Route Analysis\n\n")
            f.write("| Route | Flights | Avg Items | Items CI | Avg Weight | Weight CI | Avg Passengers | Passengers CI | Avg ULDs | ULDs CI |\n")
            f.write("|-------|---------|-----------|----------|------------|-----------|----------------|---------------|----------|----------|\n")
            
            for _, row in route_stats.iterrows():
                f.write(f"| {row['route']} | {row['flight_count']} | {row['avg_items']:.1f} | [{row.get('total_items_ci_lower', 0):.1f}, {row.get('total_items_ci_upper', 0):.1f}] | {row['avg_weight']:.1f} | [{row.get('total_weight_ci_lower', 0):.1f}, {row.get('total_weight_ci_upper', 0):.1f}] | {row['avg_passengers']:.1f} | [{row.get('passenger_count_ci_lower', 0):.1f}, {row.get('passenger_count_ci_upper', 0):.1f}] | {row['avg_ulds']:.1f} | [{row.get('uld_count_ci_lower', 0):.1f}, {row.get('uld_count_ci_upper', 0):.1f}] |\n")
            
            f.write("\n## Aircraft Type Analysis\n\n")
            f.write("| Aircraft | Flights | Avg Items | Items CI | Avg Weight | Weight CI | Avg Passengers | Passengers CI | Avg ULDs | ULDs CI |\n")
            f.write("|----------|---------|-----------|----------|------------|-----------|----------------|---------------|----------|----------|\n")
            
            for _, row in aircraft_stats.iterrows():
                f.write(f"| {row['aircraft_type']} | {row['flight_count']} | {row['avg_items']:.1f} | [{row.get('total_items_ci_lower', 0):.1f}, {row.get('total_items_ci_upper', 0):.1f}] | {row['avg_weight']:.1f} | [{row.get('total_weight_ci_lower', 0):.1f}, {row.get('total_weight_ci_upper', 0):.1f}] | {row['avg_passengers']:.1f} | [{row.get('passenger_count_ci_lower', 0):.1f}, {row.get('passenger_count_ci_upper', 0):.1f}] | {row['avg_ulds']:.1f} | [{row.get('uld_count_ci_lower', 0):.1f}, {row.get('uld_count_ci_upper', 0):.1f}] |\n")
            
            f.write("\n## Monthly Analysis\n\n")
            f.write("| Month | Flights | Avg Items | Items CI | Avg Weight | Weight CI | Avg Passengers | Passengers CI | Avg ULDs | ULDs CI |\n")
            f.write("|-------|---------|-----------|----------|------------|-----------|----------------|---------------|----------|----------|\n")
            
            for _, row in month_stats.iterrows():
                f.write(f"| {row['month']} | {row['flight_count']} | {row['avg_items']:.1f} | [{row.get('total_items_ci_lower', 0):.1f}, {row.get('total_items_ci_upper', 0):.1f}] | {row['avg_weight']:.1f} | [{row.get('total_weight_ci_lower', 0):.1f}, {row.get('total_weight_ci_upper', 0):.1f}] | {row['avg_passengers']:.1f} | [{row.get('passenger_count_ci_lower', 0):.1f}, {row.get('passenger_count_ci_upper', 0):.1f}] | {row['avg_ulds']:.1f} | [{row.get('uld_count_ci_lower', 0):.1f}, {row.get('uld_count_ci_upper', 0):.1f}] |\n")
            
            f.write("\n## Key Statistical Insights\n\n")
            
            # Find the metric with highest variability
            highest_std = stats_df.loc[stats_df['std'].idxmax()]
            f.write(f"### Highest Variability: {highest_std['metric']}\n")
            f.write(f"- Standard Deviation: {highest_std['std']}\n")
            f.write(f"- Coefficient of Variation: {highest_std['std']/highest_std['mean']*100:.1f}%\n")
            f.write(f"- 95% Confidence Interval: [{highest_std['ci_95_lower']}, {highest_std['ci_95_upper']}]\n\n")
            
            # Find the metric with lowest variability
            lowest_std = stats_df.loc[stats_df['std'].idxmin()]
            f.write(f"### Lowest Variability: {lowest_std['metric']}\n")
            f.write(f"- Standard Deviation: {lowest_std['std']}\n")
            f.write(f"- Coefficient of Variation: {lowest_std['std']/lowest_std['mean']*100:.1f}%\n")
            f.write(f"- 95% Confidence Interval: [{lowest_std['ci_95_lower']}, {lowest_std['ci_95_upper']}]\n\n")
            
            f.write("## Distribution Characteristics\n\n")
            for _, row in stats_df.iterrows():
                f.write(f"### {row['metric']}\n")
                f.write(f"- **Skewness:** {row['skewness']} ({'Right-skewed' if row['skewness'] > 0.5 else 'Left-skewed' if row['skewness'] < -0.5 else 'Approximately normal'})\n")
                f.write(f"- **Kurtosis:** {row['kurtosis']} ({'Heavy-tailed' if row['kurtosis'] > 0.5 else 'Light-tailed' if row['kurtosis'] < -0.5 else 'Normal-tailed'})\n")
                f.write(f"- **Range:** {row['max'] - row['min']}\n")
                f.write(f"- **IQR:** {row['q75'] - row['q25']}\n\n")
            
            f.write("## Files Generated\n\n")
            f.write("- `comprehensive_statistics.csv` - Overall statistical summary\n")
            f.write("- `route_statistical_analysis.csv` - Statistics by route\n")
            f.write("- `aircraft_statistical_analysis.csv` - Statistics by aircraft type\n")
            f.write("- `month_statistical_analysis.csv` - Statistics by month\n")
            f.write("- `statistical_analysis_report.md` - This comprehensive report\n")
        
        logger.info(f"Statistical analysis report saved to {report_path}")

def main():
    """Main function to run statistical analysis"""
    results_path = "/Users/emivenezian/Desktop/universidad/ingeniera/años/cuarto/Segundo Semestre/AviationOptimization/KLM_Projects/KLM_Modified/Results"
    
    analyzer = StatisticalAnalyzer(results_path)
    stats_df, route_stats, aircraft_stats, month_stats = analyzer.analyze_flight_data_statistics()
    
    logger.info("Comprehensive statistical analysis complete!")
    return stats_df, route_stats, aircraft_stats, month_stats

if __name__ == "__main__":
    results = main()
