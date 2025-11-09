"""
Service to load KLM actual loading data for comparison
KLM Actual = what KLM actually loaded (from LoadLocations.csv)
"""
import sys
import re
from pathlib import Path
from typing import Dict, Any, Optional
import pandas as pd
import numpy as np

# Add parent directory to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import settings
from utils.path_utils import get_flight_data_path

def load_klm_actual_data(flight_path: str) -> Optional[Dict[str, Any]]:
    """
    Load KLM actual loading data from LoadLocations.csv and FlightInformation.csv
    
    Args:
        flight_path: Relative path from Data/ folder
    
    Returns:
        Dictionary with KLM actual data (weight distribution, MAC ZFW, fuel consumption)
    """
    try:
        data_paths = get_flight_data_path(flight_path)
        
        # Load flight information to get actual MAC ZFW
        flight_df = pd.read_csv(data_paths['flight_information'])
        flight_row = flight_df.iloc[0]
        
        # Get actual MAC ZFW (what KLM actually loaded)
        actual_mac_zfw = flight_row.get('MacZFW')
        if pd.notna(actual_mac_zfw):
            actual_mac_zfw = float(actual_mac_zfw)
            # Handle different formats (like in Classes.ipynb)
            if 1 < actual_mac_zfw < 10:
                actual_mac_zfw = actual_mac_zfw * 10
            if actual_mac_zfw < 1:
                actual_mac_zfw = actual_mac_zfw * 100
        else:
            return None
        
        # Get Trip Fuel (for fuel savings calculation)
        trip_fuel = flight_row.get('TripFuel', flight_row.get('TripF', None))
        if pd.notna(trip_fuel):
            trip_fuel = float(trip_fuel)
        else:
            # Estimate based on route (typical long-haul: ~60,000 kg)
            trip_fuel = 60000
        
        # Load LoadLocations.csv to get actual weight distribution
        load_locations_df = pd.read_csv(data_paths['load_locations'])
        
        # Filter for cargo ULDs (DeadloadType == 'C' for Cargo)
        cargo_ulds = load_locations_df[load_locations_df['DeadloadType'] == 'C'].copy()
        
        # Calculate weight distribution from actual positions
        weight_by_compartment = {'C1': 0, 'C2': 0, 'C3': 0, 'C4': 0}
        weight_by_side = {'Left': 0, 'Right': 0}
        weight_by_position = {}
        total_weight = 0
        
        # Get weight column
        weight_col = None
        for col in ['UldGrossWeight', 'Weight', 'TotalWeight']:
            if col in cargo_ulds.columns:
                weight_col = col
                break
        
        if weight_col:
            # Group by LoadLocation to get weights per position
            for _, row in cargo_ulds.iterrows():
                location = str(row.get('LoadLocation', ''))
                weight = float(row.get(weight_col, 0))
                
                if location and pd.notna(weight) and weight > 0:
                    # Extract compartment from position (first digit)
                    if location and len(location) > 0:
                        first_char = location[0]
                        if first_char == '1':
                            compartment = 'C1'
                        elif first_char == '2':
                            compartment = 'C2'
                        elif first_char == '3':
                            compartment = 'C3'
                        elif first_char == '4':
                            compartment = 'C4'
                        else:
                            compartment = 'C1'  # Default
                        
                        weight_by_compartment[compartment] += weight
                        
                        # Determine side
                        if 'L' in location.upper():
                            weight_by_side['Left'] += weight
                        elif 'R' in location.upper():
                            weight_by_side['Right'] += weight
                        
                        weight_by_position[location] = weight_by_position.get(location, 0) + weight
                        total_weight += weight
        
        # Count ULDs actually used
        unique_ulds = cargo_ulds['SerialNumber'].nunique() if 'SerialNumber' in cargo_ulds.columns else 0
        
        return {
            'actual_mac_zfw': actual_mac_zfw,
            'trip_fuel': trip_fuel,
            'weight_by_compartment': weight_by_compartment,
            'weight_by_side': weight_by_side,
            'weight_by_position': weight_by_position,
            'total_weight': total_weight,
            'total_ulds': unique_ulds,
            'aircraft_type': str(flight_row.get('AircraftType', ''))
        }
    
    except Exception as e:
        print(f"Error loading KLM actual data: {e}")
        import traceback
        traceback.print_exc()
        return None

def calculate_fuel_savings_vs_klm_actual(
    optimized_mac_zfw: float,
    actual_mac_zfw: float,
    trip_fuel: float,
    aircraft_type: str
) -> Dict[str, float]:
    """
    Calculate fuel savings vs KLM actual using fuel efficiency brackets
    
    Args:
        optimized_mac_zfw: MAC ZFW from optimization model
        actual_mac_zfw: MAC ZFW from KLM actual loading
        trip_fuel: Trip fuel consumption (kg)
        aircraft_type: Aircraft type code (e.g., '787', '772', '77W')
    
    Returns:
        Dictionary with fuel_savings_percent and fuel_savings_kg
    """
    # Fuel efficiency brackets based on MAC ZFW (from Classes.ipynb)
    aircraft_type_str = str(aircraft_type).strip()
    
    if '787' in aircraft_type_str or aircraft_type_str == '787':
        fuel_efficiency_brackets = np.array([
            (0, 2.2),
            (16, 2.2),
            (18, 2),
            (20, 1.6),
            (22, 1.3),
            (24, 1),
            (26, 0.6),
            (28, 0.4),
            (32, 0),
            (34, -0.3),
            (36, -0.4),
            (40, -0.5),
            (43, -0.5)
        ])
    elif '772' in aircraft_type_str or aircraft_type_str == '772':
        fuel_efficiency_brackets = np.array([
            (0, 1.3),
            (16, 1.3),
            (18, 1.3),
            (20, 1.2),
            (22, 0.9),
            (24, 0.6),
            (26, 0.4),
            (28, 0.2),
            (32, 0),
            (34, -0.4),
            (36, -0.5),
            (40, -0.7),
            (43, -0.7)
        ])
    elif '77W' in aircraft_type_str or aircraft_type_str == '77W':
        fuel_efficiency_brackets = np.array([
            (0, 1.7),
            (16, 1.7),
            (18, 1.5),
            (20, 1.2),
            (22, 0.9),
            (24, 0.6),
            (26, 0.4),
            (28, 0.2),
            (32, 0),
            (34, -0.4),
            (36, -0.5),
            (40, -0.6),
            (43, -0.6)
        ])
    else:
        # Default to 787 brackets
        fuel_efficiency_brackets = np.array([
            (0, 2.2),
            (16, 2.2),
            (18, 2),
            (20, 1.6),
            (22, 1.3),
            (24, 1),
            (26, 0.6),
            (28, 0.4),
            (32, 0),
            (34, -0.3),
            (36, -0.4),
            (40, -0.5),
            (43, -0.5)
        ])
    
    # Interpolate fuel efficiency increment for optimized MAC
    model_increment = None
    for i in range(len(fuel_efficiency_brackets) - 1):
        if fuel_efficiency_brackets[i][0] <= optimized_mac_zfw <= fuel_efficiency_brackets[i + 1][0]:
            x1, y1 = fuel_efficiency_brackets[i]
            x2, y2 = fuel_efficiency_brackets[i + 1]
            model_increment = y1 + (y2 - y1) * (optimized_mac_zfw - x1) / (x2 - x1)
            break
    
    # Interpolate fuel efficiency increment for actual MAC
    actual_increment = None
    for i in range(len(fuel_efficiency_brackets) - 1):
        if fuel_efficiency_brackets[i][0] <= actual_mac_zfw <= fuel_efficiency_brackets[i + 1][0]:
            x1, y1 = fuel_efficiency_brackets[i]
            x2, y2 = fuel_efficiency_brackets[i + 1]
            actual_increment = y1 + (y2 - y1) * (actual_mac_zfw - x1) / (x2 - x1)
            break
    
    if model_increment is not None and actual_increment is not None:
        # Fuel savings percentage (difference in fuel efficiency increments)
        fuel_savings_percent = model_increment - actual_increment
        
        # Fuel savings in kg
        fuel_savings_kg = trip_fuel * (fuel_savings_percent / 100)
        
        return {
            'fuel_savings_percent': fuel_savings_percent,
            'fuel_savings_kg': fuel_savings_kg,
            'model_fuel_efficiency_increment': model_increment,
            'actual_fuel_efficiency_increment': actual_increment
        }
    
    return {
        'fuel_savings_percent': None,
        'fuel_savings_kg': None,
        'model_fuel_efficiency_increment': None,
        'actual_fuel_efficiency_increment': None
    }

