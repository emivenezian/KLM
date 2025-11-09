



#!/usr/bin/env python3
"""
Flight Data Analysis for KLM Fuel Optimization Project
Tasks 1 & 6: Count flights and create origin-destination summaries
"""

import os
import pandas as pd
import numpy as np
from pathlib import Path
import re
from collections import defaultdict
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FlightDataAnalyzer:
    def __init__(self, data_path, results_path):
        self.data_path = Path(data_path)
        self.results_path = Path(results_path)
        self.results_path.mkdir(parents=True, exist_ok=True)
        
        # Expected CSV files for complete flight data
        self.required_files = [
            'BuildUpInformation.csv',
            'FlightInformation.csv', 
            'LoadLocations.csv',
            'PaxInformation.csv',
            'PieceInformation.csv'
        ]
        
    def extract_flight_info_from_path(self, flight_path):
        """Extract flight information from directory path"""
        path_parts = flight_path.parts
        
        # Find the flight directory (contains "Flight KL")
        flight_dir = None
        for part in path_parts:
            if "Flight KL" in part:
                flight_dir = part
                break
                
        if not flight_dir:
            return None
            
        # Extract flight number, route, and date
        # Pattern: "Flight KLXXXX AMSXXX DD MMM YYYY"
        pattern = r'Flight (KL\d+) ([A-Z]{3})([A-Z]{3}) (\d{2}) ([A-Z]{3}) (\d{4})'
        match = re.match(pattern, flight_dir)
        
        if match:
            flight_num, origin, destination, day, month, year = match.groups()
            return {
                'flight_number': flight_num,
                'origin': origin,
                'destination': destination,
                'date': f"{day} {month} {year}",
                'route': f"{origin}{destination}",
                'flight_path': str(flight_path)
            }
        return None
    
    def count_total_flights(self):
        """Task 1: Count total flights by finding FlightInformation.csv files"""
        logger.info("Starting Task 1: Counting total flights...")
        
        flight_info_files = list(self.data_path.rglob("FlightInformation.csv"))
        total_flights = len(flight_info_files)
        
        logger.info(f"Found {total_flights} FlightInformation.csv files")
        
        # Create summary
        summary = {
            'total_flights': total_flights,
            'analysis_date': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
            'data_source': str(self.data_path)
        }
        
        # Save summary
        summary_df = pd.DataFrame([summary])
        summary_path = self.results_path / "flight_count_summary.csv"
        summary_df.to_csv(summary_path, index=False)
        logger.info(f"Saved flight count summary to {summary_path}")
        
        return total_flights, flight_info_files
    
    def analyze_origin_destination_distribution(self, flight_info_files):
        """Task 6: Summarize flight counts by origin-destination pair"""
        logger.info("Starting Task 6: Analyzing origin-destination distribution...")
        
        route_data = []
        route_counts = defaultdict(int)
        month_counts = defaultdict(lambda: defaultdict(int))
        aircraft_counts = defaultdict(int)
        
        for flight_file in flight_info_files:
            flight_path = flight_file.parent
            flight_info = self.extract_flight_info_from_path(flight_path)
            
            if flight_info:
                route_data.append(flight_info)
                route_counts[flight_info['route']] += 1
                
                # Extract month from path
                path_str = str(flight_path)
                if "JAN 2024" in path_str:
                    month_counts["JAN 2024"][flight_info['route']] += 1
                elif "FEB 2024" in path_str:
                    month_counts["FEB 2024"][flight_info['route']] += 1
                elif "MAR 2024" in path_str:
                    month_counts["MAR 2024"][flight_info['route']] += 1
                elif "APR 2024" in path_str:
                    month_counts["APR 2024"][flight_info['route']] += 1
        
        # Create route summary
        route_summary = []
        for route, count in sorted(route_counts.items()):
            route_summary.append({
                'route': route,
                'flight_count': count,
                'percentage': round(count / len(flight_info_files) * 100, 2)
            })
        
        route_df = pd.DataFrame(route_summary)
        route_df = route_df.sort_values('flight_count', ascending=False)
        
        # Save route summary
        route_path = self.results_path / "origin_destination_counts.csv"
        route_df.to_csv(route_path, index=False)
        logger.info(f"Saved route summary to {route_path}")
        
        # Create monthly breakdown
        monthly_data = []
        for month, routes in month_counts.items():
            for route, count in routes.items():
                monthly_data.append({
                    'month': month,
                    'route': route,
                    'flight_count': count
                })
        
        monthly_df = pd.DataFrame(monthly_data)
        monthly_path = self.results_path / "monthly_route_distribution.csv"
        monthly_df.to_csv(monthly_path, index=False)
        logger.info(f"Saved monthly distribution to {monthly_path}")
        
        # Print summary
        logger.info(f"\nRoute Distribution Summary:")
        logger.info(f"Total flights: {len(flight_info_files)}")
        logger.info(f"Unique routes: {len(route_counts)}")
        logger.info(f"Top 5 routes:")
        for i, row in route_df.head().iterrows():
            logger.info(f"  {row['route']}: {row['flight_count']} flights ({row['percentage']}%)")
        
        return route_df, monthly_df
    
    def check_flight_data_completeness(self, flight_info_files):
        """Check which flights have complete data (all 5 CSV files)"""
        logger.info("Checking flight data completeness...")
        
        complete_flights = []
        incomplete_flights = []
        
        for flight_file in flight_info_files:
            flight_path = flight_file.parent
            flight_info = self.extract_flight_info_from_path(flight_path)
            
            if not flight_info:
                continue
                
            # Check for all required files
            missing_files = []
            for required_file in self.required_files:
                file_path = flight_path / required_file
                if not file_path.exists():
                    missing_files.append(required_file)
            
            flight_data = {
                **flight_info,
                'missing_files': missing_files,
                'is_complete': len(missing_files) == 0,
                'missing_count': len(missing_files)
            }
            
            if len(missing_files) == 0:
                complete_flights.append(flight_data)
            else:
                incomplete_flights.append(flight_data)
        
        # Create completeness summary
        completeness_df = pd.DataFrame(complete_flights + incomplete_flights)
        completeness_path = self.results_path / "flight_data_completeness.csv"
        completeness_df.to_csv(completeness_path, index=False)
        
        # Create summary statistics
        total_checked = len(complete_flights) + len(incomplete_flights)
        complete_count = len(complete_flights)
        incomplete_count = len(incomplete_flights)
        
        summary_stats = {
            'total_flights_checked': total_checked,
            'complete_flights': complete_count,
            'incomplete_flights': incomplete_count,
            'completeness_rate': round(complete_count / total_checked * 100, 2) if total_checked > 0 else 0
        }
        
        summary_df = pd.DataFrame([summary_stats])
        summary_path = self.results_path / "data_completeness_summary.csv"
        summary_df.to_csv(summary_path, index=False)
        
        logger.info(f"Data completeness analysis:")
        logger.info(f"  Total flights checked: {total_checked}")
        logger.info(f"  Complete flights: {complete_count} ({summary_stats['completeness_rate']}%)")
        logger.info(f"  Incomplete flights: {incomplete_count}")
        logger.info(f"Saved completeness analysis to {completeness_path}")
        
        return complete_flights, incomplete_flights, summary_stats

def main():
    """Main analysis function"""
    # Paths
    data_path = "/Users/emivenezian/Desktop/universidad/ingeniera/años/cuarto/Segundo Semestre/AviationOptimization/KLM_Projects/KLM_Original/Data"
    results_path = "/Users/emivenezian/Desktop/universidad/ingeniera/años/cuarto/Segundo Semestre/AviationOptimization/KLM_Projects/KLM_Modified/Results"
    
    # Initialize analyzer
    analyzer = FlightDataAnalyzer(data_path, results_path)
    
    logger.info("Starting KLM Flight Data Analysis")
    logger.info("=" * 50)
    
    # Task 1: Count total flights
    total_flights, flight_info_files = analyzer.count_total_flights()
    
    # Task 6: Analyze origin-destination distribution
    route_df, monthly_df = analyzer.analyze_origin_destination_distribution(flight_info_files)
    
    # Check data completeness
    complete_flights, incomplete_flights, completeness_stats = analyzer.check_flight_data_completeness(flight_info_files)
    
    logger.info("=" * 50)
    logger.info("Analysis Complete!")
    logger.info(f"Results saved to: {results_path}")
    
    return {
        'total_flights': total_flights,
        'complete_flights': len(complete_flights),
        'incomplete_flights': len(incomplete_flights),
        'completeness_rate': completeness_stats['completeness_rate']
    }

if __name__ == "__main__":
    results = main()
