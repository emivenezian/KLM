#!/usr/bin/env python3
"""
Generate Comprehensive Analysis Summary for KLM Fuel Optimization Project
Creates a summary of all completed data analysis tasks
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AnalysisSummaryGenerator:
    def __init__(self, results_path):
        self.results_path = Path(results_path)
        self.processing_path = Path("processing/05_documentation")
        self.processing_path.mkdir(parents=True, exist_ok=True)
        
    def generate_comprehensive_summary(self):
        """Generate a comprehensive summary of all analysis results"""
        logger.info("Generating comprehensive analysis summary...")
        
        summary = {
            'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'project': 'KLM Fuel Optimization through Cargo Palletization and Weight Balance Modeling',
            'author': 'María Emilia Venezian Juricic',
            'supervisor': 'Dr. Felipe Delgado',
            'institution': 'Pontificia Universidad Católica de Chile'
        }
        
        # Task 1: Flight Count Summary
        try:
            flight_count_df = pd.read_csv(self.results_path / "flight_count_summary.csv")
            summary['total_flights_in_dataset'] = int(flight_count_df['total_flights'].iloc[0])
        except:
            summary['total_flights_in_dataset'] = 'Not available'
        
        # Task 6: Route Distribution
        try:
            route_df = pd.read_csv(self.results_path / "origin_destination_counts.csv")
            summary['route_distribution'] = route_df.to_dict('records')
            summary['total_routes'] = len(route_df)
        except:
            summary['route_distribution'] = 'Not available'
            summary['total_routes'] = 0
        
        # Task 2, 3, 7: Data Completeness
        try:
            completeness_df = pd.read_csv(self.results_path / "benchmark_completeness_summary.csv")
            summary['data_completeness_rate'] = completeness_df['completeness_rate'].iloc[0]
        except:
            summary['data_completeness_rate'] = 'Not available'
        
        # Data Content Summary
        try:
            content_df = pd.read_csv(self.results_path / "data_content_summary.csv")
            summary['total_items'] = int(content_df['total_items'].iloc[0])
            summary['average_items_per_flight'] = content_df['average_items_per_flight'].iloc[0]
            summary['total_passengers'] = int(content_df['total_passengers'].iloc[0])
            summary['average_passengers_per_flight'] = content_df['average_passengers_per_flight'].iloc[0]
        except:
            summary['total_items'] = 'Not available'
            summary['average_items_per_flight'] = 'Not available'
        
        # Aircraft Type Distribution
        try:
            aircraft_df = pd.read_csv(self.results_path / "aircraft_type_distribution.csv")
            summary['aircraft_type_distribution'] = aircraft_df.to_dict('records')
        except:
            summary['aircraft_type_distribution'] = 'Not available'
        
        # Model Feasibility Comparison
        try:
            comparison_df = pd.read_csv("processing/02_infeasibility_analysis/model_feasibility_comparison.csv")
            summary['model_feasibility_comparison'] = comparison_df.to_dict('records')
        except:
            summary['model_feasibility_comparison'] = 'Not available'
        
        # Key Findings
        summary['key_findings'] = {
            'dataset_size': f"{summary['total_flights_in_dataset']} flights in original dataset",
            'data_completeness': f"{summary['data_completeness_rate']}% of flights have complete data",
            'route_coverage': f"{summary['total_routes']} unique routes analyzed",
            'cargo_volume': f"{summary['total_items']:,} total cargo items",
            'average_cargo_per_flight': f"{summary['average_items_per_flight']} items per flight",
            'passenger_volume': f"{summary['total_passengers']:,} total passengers",
            'average_passengers_per_flight': f"{summary['average_passengers_per_flight']} passengers per flight"
        }
        
        # Recommendations for Next Steps
        summary['recommendations'] = [
            "Develop 3D-BPP heuristic (First-Fit Decreasing) to address geometric packing infeasibility",
            "Test heuristic on identified infeasible flights",
            "Optimize MILP constraints for improved feasibility",
            "Run experiments on full dataset (525 flights)",
            "Generate visualizations (heatmaps, 3D-BPP outputs)",
            "Analyze results by aircraft type and route",
            "Draft article sections with updated results"
        ]
        
        # Save comprehensive summary
        summary_df = pd.DataFrame([summary])
        summary_path = self.processing_path / "comprehensive_analysis_summary.csv"
        summary_df.to_csv(summary_path, index=False)
        
        # Create markdown report
        self.create_markdown_report(summary)
        
        logger.info(f"Comprehensive summary saved to {summary_path}")
        return summary
    
    def create_markdown_report(self, summary):
        """Create a markdown report of the analysis"""
        report_path = self.processing_path / "analysis_report.md"
        
        with open(report_path, 'w') as f:
            f.write(f"# KLM Fuel Optimization Project - Data Analysis Report\n\n")
            f.write(f"**Generated:** {summary['analysis_date']}\n\n")
            f.write(f"**Project:** {summary['project']}\n\n")
            f.write(f"**Author:** {summary['author']}\n\n")
            f.write(f"**Supervisor:** {summary['supervisor']}\n\n")
            f.write(f"**Institution:** {summary['institution']}\n\n")
            
            f.write("## Executive Summary\n\n")
            f.write("This report summarizes the data analysis completed for the KLM fuel optimization project, focusing on cargo palletization and weight balance modeling for intercontinental flights.\n\n")
            
            f.write("## Dataset Overview\n\n")
            f.write(f"- **Total Flights:** {summary['total_flights_in_dataset']}\n")
            f.write(f"- **Data Completeness:** {summary['data_completeness_rate']}%\n")
            f.write(f"- **Unique Routes:** {summary['total_routes']}\n")
            f.write(f"- **Total Cargo Items:** {summary['total_items']:,}\n")
            f.write(f"- **Average Items per Flight:** {summary['average_items_per_flight']}\n")
            f.write(f"- **Total Passengers:** {summary['total_passengers']:,}\n")
            f.write(f"- **Average Passengers per Flight:** {summary['average_passengers_per_flight']}\n\n")
            
            f.write("## Route Distribution\n\n")
            if isinstance(summary['route_distribution'], list):
                f.write("| Route | Flight Count | Percentage |\n")
                f.write("|-------|--------------|------------|\n")
                for route in summary['route_distribution']:
                    f.write(f"| {route['route']} | {route['flight_count']} | {route['percentage']}% |\n")
            f.write("\n")
            
            f.write("## Aircraft Type Distribution\n\n")
            if isinstance(summary['aircraft_type_distribution'], list):
                f.write("| Aircraft Type | Flight Count | Percentage |\n")
                f.write("|---------------|--------------|------------|\n")
                for aircraft in summary['aircraft_type_distribution']:
                    f.write(f"| {aircraft['aircraft_type']} | {aircraft['flight_count']} | {aircraft['percentage']}% |\n")
            f.write("\n")
            
            f.write("## Model Feasibility Comparison\n\n")
            if isinstance(summary['model_feasibility_comparison'], list):
                f.write("| Model | Total Flights | Feasible Flights | Infeasible Flights | Feasibility Rate |\n")
                f.write("|-------|---------------|------------------|-------------------|-----------------|\n")
                for model in summary['model_feasibility_comparison']:
                    f.write(f"| {model['model']} | {model['total_flights']} | {model['feasible_flights']} | {model['infeasible_flights']} | {model['feasibility_rate']}% |\n")
            f.write("\n")
            
            f.write("## Key Findings\n\n")
            for key, finding in summary['key_findings'].items():
                f.write(f"- **{key.replace('_', ' ').title()}:** {finding}\n")
            f.write("\n")
            
            f.write("## Recommendations for Next Steps\n\n")
            for i, recommendation in enumerate(summary['recommendations'], 1):
                f.write(f"{i}. {recommendation}\n")
            f.write("\n")
            
            f.write("## Files Generated\n\n")
            f.write("- `flight_count_summary.csv` - Total flight count analysis\n")
            f.write("- `origin_destination_counts.csv` - Route distribution analysis\n")
            f.write("- `data_content_summary.csv` - Cargo and passenger data analysis\n")
            f.write("- `aircraft_type_distribution.csv` - Aircraft type distribution\n")
            f.write("- `model_feasibility_comparison.csv` - Model feasibility comparison\n")
            f.write("- `comprehensive_analysis_summary.csv` - Complete analysis summary\n")
            f.write("- `analysis_report.md` - This markdown report\n")
        
        logger.info(f"Markdown report saved to {report_path}")

def main():
    """Main function to generate analysis summary"""
    results_path = "/Users/emivenezian/Desktop/universidad/ingeniera/años/cuarto/Segundo Semestre/AviationOptimization/KLM_Projects/KLM_Modified/Results"
    
    generator = AnalysisSummaryGenerator(results_path)
    summary = generator.generate_comprehensive_summary()
    
    logger.info("Analysis summary generation complete!")
    return summary

if __name__ == "__main__":
    summary = main()
