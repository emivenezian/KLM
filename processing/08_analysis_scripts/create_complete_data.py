#!/usr/bin/env python3
"""
Create Data_Only_Complete folder with only complete flights (all 5 CSV files)
"""

import pandas as pd
import shutil
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_complete_data_folder():
    """Create Data_Only_Complete folder with only complete flights organized by month and route"""
    
    # Paths
    original_data_path = Path("/Users/emivenezian/Desktop/universidad/ingeniera/años/cuarto/Segundo Semestre/AviationOptimization/KLM_Projects/KLM_Original/Data")
    complete_data_path = Path("Data_Only_Complete")
    analysis_data_path = Path("processing/01_data_analysis/data/comprehensive_flight_analysis.csv")
    
    # Create destination directory
    complete_data_path.mkdir(exist_ok=True)
    
    # Load the comprehensive flight analysis to get complete flights
    logger.info("Loading comprehensive flight analysis data...")
    df = pd.read_csv(analysis_data_path)
    
    # Filter for complete flights (is_complete = True)
    complete_flights = df[df['is_complete'] == True]
    logger.info(f"Found {len(complete_flights)} complete flights out of {len(df)} total flights")
    
    # Required CSV files
    required_files = [
        'BuildUpInformation.csv',
        'FlightInformation.csv', 
        'LoadLocations.csv',
        'PaxInformation.csv',
        'PieceInformation.csv'
    ]
    
    copied_count = 0
    
    # Group flights by route and month for organized structure
    for _, flight in complete_flights.iterrows():
        # Get the original flight path
        original_flight_path = Path(flight['flight_path'])
        
        # Extract route and month information
        origin = flight['origin']
        destination = flight['destination']
        date = flight['date']
        
        # Parse date to get month and year
        from datetime import datetime
        date_obj = datetime.strptime(date, '%d %b %Y')
        month_year = date_obj.strftime('%b %Y').upper()
        
        # Create route-month directory structure
        route = f"{origin}{destination}"
        route_month_dir = f"Flights {route} {month_year}"
        
        # Create destination path with organized structure
        dest_route_month_path = complete_data_path / route_month_dir
        dest_route_month_path.mkdir(parents=True, exist_ok=True)
        
        # Create flight directory name (same as original)
        flight_number = flight['flight_number']
        dest_flight_name = f"Flight {flight_number} {route} {date}"
        dest_flight_path = dest_route_month_path / dest_flight_name
        
        # Create destination directory
        dest_flight_path.mkdir(parents=True, exist_ok=True)
        
        # Copy all 5 required CSV files
        files_copied = 0
        for csv_file in required_files:
            source_file = original_flight_path / csv_file
            dest_file = dest_flight_path / csv_file
            
            if source_file.exists():
                shutil.copy2(source_file, dest_file)
                files_copied += 1
            else:
                logger.warning(f"Missing file: {source_file}")
        
        # Verify all 5 files were copied
        if files_copied == 5:
            copied_count += 1
            logger.info(f"Copied complete flight: {route_month_dir}/{dest_flight_name}")
        else:
            logger.error(f"Failed to copy all files for: {dest_flight_name} ({files_copied}/5 files)")
    
    logger.info(f"Successfully copied {copied_count} complete flights to Data_Only_Complete/")
    
    # Create a summary file
    summary_path = complete_data_path / "complete_flights_summary.txt"
    with open(summary_path, 'w') as f:
        f.write("Complete Flights Data Summary\n")
        f.write("=" * 40 + "\n\n")
        f.write(f"Total complete flights: {copied_count}\n")
        f.write(f"Source: KLM_Original/Data\n")
        f.write(f"Destination: Data_Only_Complete/\n")
        f.write(f"Files per flight: 5 CSV files\n")
        f.write("\nRequired files per flight:\n")
        for file in required_files:
            f.write(f"- {file}\n")
        f.write("\nOrganized structure (by route and month):\n")
        f.write("Data_Only_Complete/\n")
        f.write("├── Flights AMSXXX MMM YYYY/\n")
        f.write("│   ├── Flight KLXXXX AMSXXX DD MMM YYYY/\n")
        f.write("│   │   ├── BuildUpInformation.csv\n")
        f.write("│   │   ├── FlightInformation.csv\n")
        f.write("│   │   ├── LoadLocations.csv\n")
        f.write("│   │   ├── PaxInformation.csv\n")
        f.write("│   │   └── PieceInformation.csv\n")
        f.write("│   └── ...\n")
        f.write("└── ...\n")
    
    logger.info(f"Summary saved to: {summary_path}")

if __name__ == "__main__":
    create_complete_data_folder()
