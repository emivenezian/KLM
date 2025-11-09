"""
Service to load pre-computed optimization results from Results/ folder
"""
import os
import re
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
import pandas as pd

# Add parent directory to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import settings

def find_results_folder(flight_path: str, model_type: str = "delgado_venezian") -> Optional[Path]:
    """
    Find the Results folder for a given flight and model type
    
    Args:
        flight_path: Relative path from Data/ (e.g., "Flights AMSBLR FEB 2024/Flight KL0879 AMSBLR 02 FEB 2024")
        model_type: Type of model (delgado_venezian, baseline, optimized_actual, bax_fixed)
    
    Returns:
        Path to results folder if found, None otherwise
    """
    # Map model type to Results folder
    results_folders = {
        "delgado_venezian": "Results",
        "baseline": "Results_Baseline",
        "optimized_actual": "Results_Optimized_Actual",
        "bax_fixed": "Results_BAX_Fixed"
    }
    
    results_base = PROJECT_ROOT / results_folders.get(model_type, "Results")
    
    # Extract flight info from path
    # flight_path format: "Flights AMSBLR FEB 2024/Flight KL0879 AMSBLR 02 FEB 2024"
    parts = flight_path.split('/')
    if len(parts) < 2:
        return None
    
    route_info = parts[0]  # "Flights AMSBLR FEB 2024"
    flight_folder = parts[1]  # "Flight KL0879 AMSBLR 02 FEB 2024"
    
    # Extract route and date info
    # Route format: "Flights AMSBLR FEB 2024" -> need "AMSBLR FEB 2024"
    route_match = re.search(r'Flights (.+)', route_info)
    if not route_match:
        return None
    
    route_date = route_match.group(1)  # "AMSBLR FEB 2024"
    
    # Find matching Results folder
    # Results folder format: "Results AMSBLR FEB 2024" or "Results AMSSIN JAN 2024"
    for results_route_folder in results_base.iterdir():
        if not results_route_folder.is_dir():
            continue
        
        # Check if route matches (format: "Results AMSBLR FEB 2024")
        if route_date in results_route_folder.name:
            # Look for matching flight folder
            # Flight folder format: "Flight KL835 AMSSIN 08 JAN 24"
            for result_flight_folder in results_route_folder.iterdir():
                if not result_flight_folder.is_dir():
                    continue
                
                # Extract flight number and date from both paths
                # Try to match flight number (handle leading zeros)
                flight_num_match = re.search(r'KL(\d+)', flight_folder)
                result_flight_num_match = re.search(r'KL(\d+)', result_flight_folder.name)
                
                if flight_num_match and result_flight_num_match:
                    # Compare as integers to handle leading zeros (e.g., "0835" == "835")
                    if int(flight_num_match.group(1)) == int(result_flight_num_match.group(1)):
                        # Found matching flight!
                        return result_flight_folder
    
    return None

def parse_results_txt(results_folder: Path) -> Dict[str, Any]:
    """
    Parse Results.txt file to extract optimization results
    
    Args:
        results_folder: Path to results folder
    
    Returns:
        Dictionary with parsed results
    """
    results_file = results_folder / "Results.txt"
    if not results_file.exists():
        return {}
    
    results = {
        'ulds': [],
        'weight_by_compartment': {},
        'weight_by_position': {},
        'mac_zfw': None,
        'fuel_savings_kg': None,
        'number_of_ulds': 0
    }
    
    try:
        with open(results_file, 'r') as f:
            content = f.read()
            
            # Parse ULD positions
            # Format: "ULD PMC32298KL with weight 1234.5 kg is loaded to position 11L"
            # Also: "ULD PAG-26 with weight 88.0 kg with a volume loadfactor..."
            # Also: "ULD BAX-0 with weight 307.0 kg is loaded to position 12L"
            uld_patterns = [
                r'ULD ([A-Z0-9-]+) with weight ([\d.]+) kg.*?loaded to position (\w+)',  # Full format with loadfactor
                r'ULD ([A-Z0-9-]+) with weight ([\d.]+) kg is loaded to position (\w+)',  # Simple format
            ]
            
            parsed_ulds = set()  # Track already parsed ULDs to avoid duplicates
            
            for pattern in uld_patterns:
                for match in re.finditer(pattern, content):
                    uld_serial = match.group(1)
                    weight = float(match.group(2))
                    position = match.group(3)
                    
                    # Skip if already parsed (handle multiple patterns matching same line)
                    if (uld_serial, position) in parsed_ulds:
                        continue
                    parsed_ulds.add((uld_serial, position))
                    
                    # Determine compartment from position
                    compartment = None
                    if position[0] == '1':
                        compartment = 'C1'
                    elif position[0] == '2':
                        compartment = 'C2'
                    elif position[0] == '3':
                        compartment = 'C3'
                    elif position[0] == '4':
                        compartment = 'C4'
                    
                    # Determine side
                    side = 'Left' if 'L' in position else 'Right' if 'R' in position else None
                    
                    results['ulds'].append({
                        'serial': uld_serial,
                        'weight': weight,
                        'position': position,
                        'compartment': compartment,
                        'side': side
                    })
            
            # Parse compartment weights
            # Format: "Weight in Compartment 1: 1234.5 kg"
            for i in range(1, 5):
                pattern = f'Weight in Compartment {i}: ([\d.]+) kg'
                match = re.search(pattern, content)
                if match:
                    results['weight_by_compartment'][f'C{i}'] = float(match.group(1))
            
            # Parse %MAC ZFW
            mac_pattern = r'%MAC ZFW is ([\d.]+)'
            match = re.search(mac_pattern, content)
            if match:
                results['mac_zfw'] = float(match.group(1))
            
            # Parse fuel savings
            fuel_pattern = r'Resulting in a fuel deviation of.*?or ([\d.]+) kg'
            match = re.search(fuel_pattern, content)
            if match:
                results['fuel_savings_kg'] = float(match.group(1))
            
            # Parse number of ULDs
            uld_count_pattern = r'(\d+) ULDs are built by the model'
            match = re.search(uld_count_pattern, content)
            if match:
                results['number_of_ulds'] = int(match.group(1))
                
    except Exception as e:
        print(f"Error parsing Results.txt: {e}")
        return {}
    
    return results

def parse_general_information(results_folder: Path) -> Dict[str, Any]:
    """
    Parse General_Information.txt to get flight details
    
    Args:
        results_folder: Path to results folder
    
    Returns:
        Dictionary with flight information
    """
    gen_info_file = results_folder / "General_Information.txt"
    if not gen_info_file.exists():
        return {}
    
    info = {}
    try:
        with open(gen_info_file, 'r') as f:
            content = f.read()
            
            # Extract flight number
            flight_match = re.search(r'Flight Number: (KL\d+)', content)
            if flight_match:
                info['flight_number'] = flight_match.group(1)
            
            # Extract aircraft type
            aircraft_match = re.search(r'Aircraft Type: (\w+)', content)
            if aircraft_match:
                info['aircraft_type'] = aircraft_match.group(1)
            
            # Extract ZFW, TOW, LW
            zfw_match = re.search(r'ZFW: ([\d.]+) kg', content)
            if zfw_match:
                info['zfw'] = float(zfw_match.group(1))
            
            tow_match = re.search(r'TOW: ([\d.]+) kg', content)
            if tow_match:
                info['tow'] = float(tow_match.group(1))
                
    except Exception as e:
        print(f"Error parsing General_Information.txt: {e}")
        return {}
    
    return info

def load_precomputed_results(
    flight_path: str,
    model_type: str = "delgado_venezian"
) -> Optional[Dict[str, Any]]:
    """
    Load pre-computed results from Results folder
    
    Args:
        flight_path: Relative path from Data/
        model_type: Type of model
    
    Returns:
        Dictionary with results if found, None otherwise
    """
    results_folder = find_results_folder(flight_path, model_type)
    if not results_folder:
        return None
    
    # Parse results files
    results_data = parse_results_txt(results_folder)
    gen_info = parse_general_information(results_folder)
    
    if not results_data:
        return None
    
    # Combine data
    combined = {
        **results_data,
        **gen_info,
        'results_folder': str(results_folder)
    }
    
    return combined

