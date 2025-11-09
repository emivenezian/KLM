"""
Synthetic flight data generator for testing optimization models
"""
import pandas as pd
import numpy as np
import random
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime, timedelta
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import settings

def generate_synthetic_flight(
    num_items: int = 50,
    num_ulds: int = 10,
    weight_range: tuple = (100, 1000),
    include_crt: bool = True,
    include_col: bool = True,
    include_dangerous: bool = False,
    flight_number: str = "SYN001",
    departure_airport: str = "AMS",
    arrival_airport: str = "SIN",
    output_dir: Path = None
) -> Dict[str, Path]:
    """
    Generate synthetic flight data for testing
    
    Args:
        num_items: Number of cargo items
        num_ulds: Number of ULDs
        weight_range: (min_weight, max_weight) in kg
        include_crt: Include CRT (Cooling Required) items
        include_col: Include COL (Cold) items
        include_dangerous: Include dangerous goods
        flight_number: Flight number
        departure_airport: Departure airport code
        arrival_airport: Arrival airport code
        output_dir: Directory to save synthetic data (default: app/data/synthetic)
    
    Returns:
        Dictionary with paths to generated CSV files
    """
    if output_dir is None:
        output_dir = Path(__file__).parent.parent.parent / "data" / "synthetic"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # ULD types commonly used
    uld_types = ['PMC', 'PAG', 'AAP', 'AKE', 'AAK']
    
    # Generate ULD serial numbers
    uld_serials = []
    for i in range(num_ulds):
        uld_type = random.choice(uld_types)
        uld_serials.append(f"{uld_type}{random.randint(10000, 99999)}KL")
    
    # Generate cargo items
    items = []
    destinations = ['BLR', 'SIN', 'DEL', 'ICN', 'LAX', 'SFO', 'IAH']
    origins = ['AMS', 'CDG', 'FRA', 'LHR', 'DXB', 'ATL', 'JFK']
    commodities = ['R21', 'M25', 'M21', 'R81', 'R82']
    
    for i in range(num_items):
        weight = random.uniform(weight_range[0], weight_range[1])
        num_pieces = random.randint(1, 5)
        
        # Determine temperature requirements
        crt = include_crt and random.random() < 0.1  # 10% CRT
        col = include_col and random.random() < 0.15  # 15% COL
        
        item = {
            'SerialNumber': f"{random.choice(origins)}-{random.randint(1000000, 9999999)}",
            'NumberOfPieces': num_pieces,
            'Weight': round(weight, 2),
            'Volume': round(weight / random.uniform(150, 300), 2),  # Realistic density
            'ProductCode': random.choice(commodities),
            'CRT': 'True' if crt else 'False',
            'COL': 'True' if col else 'False',
            'Dangerous': 'True' if (include_dangerous and random.random() < 0.05) else 'False',
            'OriginStationCode': random.choice(origins),
            'DestinationStationCode': random.choice(destinations),
            'DepartureFlightPrefix': 'KL',
            'DepartureFlightNumber': flight_number.replace('KL', ''),
            'DepartureFlight': f"KL{flight_number.replace('KL', '')}",
            'DepartureFlightDate': datetime.now().strftime('%Y-%m-%d'),
            'BookingSegmentFlightDateLT': datetime.now().strftime('%Y-%m-%d'),
        }
        items.append(item)
    
    # Generate PieceInformation.csv
    piece_df = pd.DataFrame(items)
    piece_info_path = output_dir / 'PieceInformation.csv'
    piece_df.to_csv(piece_info_path, index=False)
    
    # Generate FlightInformation.csv
    flight_date = datetime.now()
    flight_info = {
        'FlightLegUtcId': f"{flight_date.strftime('%Y-%m-%d')}|KL|{flight_number.replace('KL', '')}",
        'Airline': 'KL',
        'FlightNumber': flight_number.replace('KL', ''),
        'LegDepartureDateUtc': flight_date.strftime('%Y-%m-%d'),
        'DepartureAirport': departure_airport,
        'ArrivalAirport': arrival_airport,
        'ActualZeroFuelWeight': round(sum(item['Weight'] for item in items) + 132000, 1),  # Estimated with base weight
        'EstimatedZeroFuelWeight': round(sum(item['Weight'] for item in items) + 132000, 1),
        'DryOperatingWeight': 132000,  # Typical for 777
        'MacZFW': round(random.uniform(15, 25), 1),
        'ModTime': flight_date.strftime('%m/%d/%Y %H:%M'),
        'AircraftType': '777',
        'AircraftRegistration': f"PH{random.choice(['B', 'C', 'D'])}{random.choice(['K', 'L', 'M'])}{random.choice(['H', 'I', 'J'])}",
        'FlightCancelled': 'False',
        'CostIndex': 10,
        'TakeOffFuel': 55000,
        'TripFuel': 48000
    }
    flight_df = pd.DataFrame([flight_info])
    flight_info_path = output_dir / 'FlightInformation.csv'
    flight_df.to_csv(flight_info_path, index=False)
    
    # Generate LoadLocations.csv (simplified - using common positions)
    load_locations = []
    positions = ['11L', '11R', '12L', '12R', '13L', '13R', '21L', '21R', '22L', '22R', 
                 '23L', '23R', '31L', '31R', '32L', '32R', '33L', '33R', '41L', '41R', 
                 '42L', '42R', '43L', '43R']
    
    for pos in positions[:num_ulds]:
        load_locations.append({
            'Location': pos,
            'Index': len(load_locations) + 1
        })
    
    load_locs_df = pd.DataFrame(load_locations)
    load_locs_path = output_dir / 'LoadLocations.csv'
    load_locs_df.to_csv(load_locs_path, index=False)
    
    # Generate PaxInformation.csv (simplified)
    pax_info = {
        'DepartureFlight': f"KL{flight_number.replace('KL', '')}",
        'LocalDepartureDate': flight_date.strftime('%Y-%m-%d'),
        'TotalPax': random.randint(200, 350),
        'TotalPaxWeight': random.randint(15000, 25000)
    }
    pax_df = pd.DataFrame([pax_info])
    pax_info_path = output_dir / 'PaxInformation.csv'
    pax_df.to_csv(pax_info_path, index=False)
    
    # Generate BuildUpInformation.csv
    buildup_info = []
    for i, uld_serial in enumerate(uld_serials):
        # Assign items to ULDs
        items_per_uld = random.randint(3, 8)
        assigned_items = items[i*items_per_uld:(i+1)*items_per_uld] if (i+1)*items_per_uld <= len(items) else items[i*items_per_uld:]
        
        for j, item in enumerate(assigned_items):
            buildup_info.append({
                'ULD': uld_serial,
                'TotalNumberOfShipments': len(assigned_items),
                'AirWaybillNumber': item['SerialNumber'].split('-')[1] if '-' in item['SerialNumber'] else str(random.randint(1000000, 9999999)),
                'AirWaybillSequenceNumber': 1,
                'AirWaybillStorageSequenceNumber': j + 1,
                'ProductCode': item['ProductCode'],
                'NumberOfPiecesOnAWB': item['NumberOfPieces'],
                'TotalWeightOnAWB': item['Weight'],
                'TotalVolumeOnAWB': item['Volume'],
                'OriginStationCode': item['OriginStationCode'],
                'DestinationStationCode': item['DestinationStationCode'],
                'DepartureFlightPrefix': 'KL',
                'DepartureFlightNumber': flight_number.replace('KL', ''),
                'DepartureFlight': f"KL{flight_number.replace('KL', '')}",
                'DepartureFlightDate': flight_date.strftime('%Y-%m-%d'),
                'FlightOrTruck': 'Aircraft',
                'BuildupEventDateTime': (flight_date - timedelta(days=1)).strftime('%m/%d/%Y %H:%M'),
                'BuildupLocation': f"PM{random.randint(1, 5):02d}",
                'BuildupLocationGroup': 'VG2/3',
                'BuildupLocationBuilding': 'VG2/3',
                'OutgoingULDKey': uld_serial,
                'NrBuildupPieces': item['NumberOfPieces'],
                'IsNotBuildUp': 'False',
                'IsBuildUpInVG3': 'True',
                'IsBuildUpInVG1': 'False'
            })
    
    buildup_df = pd.DataFrame(buildup_info)
    buildup_info_path = output_dir / 'BuildUpInformation.csv'
    buildup_df.to_csv(buildup_info_path, index=False)
    
    return {
        'piece_information': piece_info_path,
        'flight_information': flight_info_path,
        'load_locations': load_locs_path,
        'pax_information': pax_info_path,
        'buildup_information': buildup_info_path,
        'output_directory': output_dir
    }

