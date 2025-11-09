"""
Google Sheets export service
"""
import gspread
from google.oauth2.service_account import Credentials
from typing import Dict, Any, List, Optional
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.schemas import OptimizationResult
from config import settings
import pandas as pd

class GoogleSheetsService:
    """Service for exporting results to Google Sheets"""
    
    def __init__(self):
        self.client = None
        if settings.GOOGLE_SHEETS_ENABLED and settings.GOOGLE_SHEETS_CREDENTIALS_PATH:
            self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Google Sheets client"""
        try:
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
            creds = Credentials.from_service_account_file(
                settings.GOOGLE_SHEETS_CREDENTIALS_PATH,
                scopes=scope
            )
            self.client = gspread.authorize(creds)
        except Exception as e:
            print(f"Warning: Could not initialize Google Sheets client: {e}")
            self.client = None
    
    def export_optimization_result(
        self,
        result: OptimizationResult,
        spreadsheet_id: str,
        worksheet_name: str = "Optimization Results"
    ) -> bool:
        """
        Export optimization result to Google Sheets
        
        Args:
            result: OptimizationResult to export
            spreadsheet_id: Google Sheets spreadsheet ID
            worksheet_name: Name of worksheet to create/update
        
        Returns:
            True if successful, False otherwise
        """
        if not self.client:
            return False
        
        try:
            spreadsheet = self.client.open_by_key(spreadsheet_id)
            
            # Try to get existing worksheet or create new one
            try:
                worksheet = spreadsheet.worksheet(worksheet_name)
                worksheet.clear()
            except:
                worksheet = spreadsheet.add_worksheet(title=worksheet_name, rows=1000, cols=20)
            
            # Prepare data for export
            data = []
            
            # Flight information header
            data.append(["Flight Information"])
            data.append(["Flight Number", result.flight_info.flight_number])
            data.append(["Departure", result.flight_info.departure_airport])
            data.append(["Arrival", result.flight_info.arrival_airport])
            data.append(["Date", result.flight_info.date])
            data.append(["Aircraft Type", result.flight_info.aircraft_type])
            data.append([])
            
            # Weight distribution
            data.append(["Weight Distribution"])
            data.append(["Compartment", "Weight (kg)"])
            for comp, weight in result.weight_distribution.by_compartment.items():
                data.append([comp, weight])
            data.append([])
            
            data.append(["Side", "Weight (kg)"])
            for side, weight in result.weight_distribution.by_side.items():
                data.append([side, weight])
            data.append([])
            
            # ULD information
            data.append(["ULD Information"])
            data.append(["Index", "Type", "Serial", "Weight (kg)", "Position", "Compartment", "Items"])
            for uld in result.ulds:
                item_count = result.uld_utilization.items_per_uld.get(uld.index, 0)
                data.append([
                    uld.index,
                    uld.type,
                    uld.serialnumber,
                    uld.weight,
                    uld.position or "Unassigned",
                    uld.compartment or "Unknown",
                    item_count
                ])
            data.append([])
            
            # Cargo items
            data.append(["Cargo Items"])
            data.append(["Index", "Serial", "Pieces", "Weight (kg)", "ULD Assignment", "CRT", "COL", "Dangerous"])
            for item in result.cargo_items[:100]:  # Limit to first 100 items
                data.append([
                    item.index,
                    item.serialnumber,
                    item.number_of_pieces,
                    item.weight,
                    item.uld_assignment if item.uld_assignment is not None else "Unassigned",
                    "Yes" if item.CRT else "No",
                    "Yes" if item.COL else "No",
                    "Yes" if item.dangerous else "No"
                ])
            
            # Write data to sheet
            worksheet.update('A1', data)
            
            return True
            
        except Exception as e:
            print(f"Error exporting to Google Sheets: {e}")
            return False
    
    def is_available(self) -> bool:
        """Check if Google Sheets export is available"""
        return self.client is not None

