"""
Utility functions for handling file paths
"""
import os
from pathlib import Path
from typing import Optional
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import settings

def get_flight_data_path(flight_path: str) -> dict:
    """
    Get paths to all required CSV files for a flight
    
    Args:
        flight_path: Path to flight folder (relative to Data/ or absolute)
    
    Returns:
        Dictionary with paths to all required files
    """
    # Handle both relative and absolute paths
    if os.path.isabs(flight_path):
        flight_dir = Path(flight_path)
    else:
        flight_dir = settings.DATA_ROOT / flight_path
    
    if not flight_dir.exists():
        raise FileNotFoundError(f"Flight directory not found: {flight_dir}")
    
    files = {
        'piece_information': flight_dir / 'PieceInformation.csv',
        'flight_information': flight_dir / 'FlightInformation.csv',
        'load_locations': flight_dir / 'LoadLocations.csv',
        'pax_information': flight_dir / 'PaxInformation.csv',
        'buildup_information': flight_dir / 'BuildUpInformation.csv'
    }
    
    # Check if all files exist
    missing_files = [k for k, v in files.items() if not v.exists()]
    if missing_files:
        raise FileNotFoundError(f"Missing required files: {missing_files}")
    
    return {k: str(v) for k, v in files.items()}

def get_inputfiles_path(filename: str) -> Path:
    """
    Get path to a file in Inputfiles folder
    
    Args:
        filename: Name of the file
    
    Returns:
        Path object
    """
    file_path = settings.INPUTFILES_ROOT / filename
    if not file_path.exists():
        raise FileNotFoundError(f"Input file not found: {file_path}")
    return file_path

def list_available_flights() -> list:
    """
    List all available flights in the Data folder
    
    Returns:
        List of flight folder paths (relative to Data/)
    """
    flights = []
    if not settings.DATA_ROOT.exists():
        return flights
    
    for route_folder in settings.DATA_ROOT.iterdir():
        if route_folder.is_dir():
            for flight_folder in route_folder.iterdir():
                if flight_folder.is_dir() and flight_folder.name.startswith('Flight'):
                    # Return relative path from Data/
                    rel_path = flight_folder.relative_to(settings.DATA_ROOT)
                    flights.append(str(rel_path))
    
    return sorted(flights)

def list_available_flights_with_item_count() -> list:
    """
    List all available flights with their item counts, sorted by item count (smallest first)
    
    Returns:
        List of tuples: (flight_path, item_count) sorted by item_count
    """
    import pandas as pd
    
    flights_with_counts = []
    if not settings.DATA_ROOT.exists():
        return []
    
    for route_folder in settings.DATA_ROOT.iterdir():
        if route_folder.is_dir():
            for flight_folder in route_folder.iterdir():
                if flight_folder.is_dir() and flight_folder.name.startswith('Flight'):
                    rel_path = flight_folder.relative_to(settings.DATA_ROOT)
                    flight_path_str = str(rel_path)
                    
                    # Try to count items in PieceInformation.csv
                    piece_info_path = flight_folder / 'PieceInformation.csv'
                    try:
                        if piece_info_path.exists():
                            piece_df = pd.read_csv(piece_info_path)
                            item_count = len(piece_df)
                            flights_with_counts.append((flight_path_str, item_count))
                        else:
                            # If no PieceInformation, try BuildUpInformation
                            buildup_path = flight_folder / 'BuildUpInformation.csv'
                            if buildup_path.exists():
                                buildup_df = pd.read_csv(buildup_path)
                                item_count = len(buildup_df)
                                flights_with_counts.append((flight_path_str, item_count))
                            else:
                                # Fallback: count as 0
                                flights_with_counts.append((flight_path_str, 0))
                    except Exception:
                        # If error reading, count as 0
                        flights_with_counts.append((flight_path_str, 0))
    
    # Sort by item count (smallest first), then by flight path
    flights_with_counts.sort(key=lambda x: (x[1], x[0]))
    
    return flights_with_counts

