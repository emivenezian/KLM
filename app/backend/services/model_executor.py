"""
Service to execute optimization models
Integrates with the actual Model.ipynb logic
"""
import sys
import os
import time
import traceback
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
import pandas as pd
import numpy as np

# Add parent directory to path to import existing classes
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import settings
from models.schemas import (
    OptimizationResult, FlightInfo, WeightDistribution, ULDUtilization, 
    CargoItem, ULDInfo, CargoMetrics, PerformanceMetrics, OptimizationMetrics,
    SafetyMetrics, ComparisonMetrics, KLMActualMetrics, AnnualImpactMetrics
)
from utils.path_utils import get_flight_data_path
from services.model_runner import run_optimization_model
from services.results_loader import load_precomputed_results
from services.klm_actual_loader import load_klm_actual_data, calculate_fuel_savings_vs_klm_actual
from services.mac_calculator import calculate_mac_zfw_from_distribution

def to_native_type(value):
    """Convert NumPy/Pandas types to native Python types"""
    if pd.isna(value):
        return None
    if isinstance(value, (np.integer, np.int64, np.int32)):
        return int(value)
    if isinstance(value, (np.floating, np.float64, np.float32)):
        return float(value)
    if isinstance(value, np.ndarray):
        return value.tolist()
    return value

def to_string_safe(value, default=''):
    """Convert value to string safely, handling None and numeric types"""
    if value is None or pd.isna(value):
        return default
    return str(value)

class ModelExecutor:
    """Executes optimization models using the actual model logic"""
    
    def execute_model(
        self, 
        flight_path: str, 
        model_type: str = "delgado_venezian",
        restricted_locations: List[str] = None
    ) -> OptimizationResult:
        """
        Execute optimization model for a flight
        
        Args:
            flight_path: Relative path from Data/ folder
            model_type: Type of model to run
            restricted_locations: List of restricted load locations
        
        Returns:
            OptimizationResult with results or error
        """
        start_time = time.time()
        
        try:
            # Get flight data paths
            data_paths = get_flight_data_path(flight_path)
            
            # Load flight information
            flight_df = pd.read_csv(data_paths['flight_information'])
            flight_row = flight_df.iloc[0]
            
            # Extract flight info - ensure all fields are proper types (strings for FlightInfo)
            flight_info = FlightInfo(
                flight_number=to_string_safe(flight_row.get('FlightNumber'), 'UNKNOWN'),
                departure_airport=to_string_safe(flight_row.get('DepartureAirport'), ''),
                arrival_airport=to_string_safe(flight_row.get('ArrivalAirport'), ''),
                date=to_string_safe(flight_row.get('FlightDate'), ''),
                aircraft_type=to_string_safe(flight_row.get('AircraftType'), ''),
                aircraft_registration=to_string_safe(flight_row.get('AircraftRegistration'), '')
            )
            
            # ==========================================
            # STEP 1: ATTEMPT REAL-TIME MODEL EXECUTION
            # ==========================================
            real_model_success = False
            model_results = None
            try:
                model_results = run_optimization_model(
                    piece_information_csv=data_paths['piece_information'],
                    flight_information_csv=data_paths['flight_information'],
                    load_locations_csv=data_paths['load_locations'],
                    pax_information_csv=data_paths['pax_information'],
                    buildup_information_csv=data_paths['buildup_information'],
                    arrival_airport=flight_info.arrival_airport,
                    restricted_locations=restricted_locations,
                    model_type=model_type
                )
                
                if model_results.get('success', False):
                    # ✅ REAL MODEL EXECUTION SUCCESS!
                    # Extract results from actual Gurobi optimization
                    cargo = model_results.get('cargo')
                    aircraft = model_results.get('aircraft')
                    
                    # Extract ULD information with ACTUAL positions from model
                    uld_info = self._extract_uld_info_from_model(cargo, aircraft)
                    cargo_items = self._extract_cargo_items_from_model(cargo)
                    weight_dist = self._calculate_weight_distribution_from_model(cargo, aircraft, flight_row, flight_path)
                    uld_util = self._calculate_uld_utilization_from_model(cargo, aircraft)
                    warnings = ["✅ REAL-TIME OPTIMIZATION COMPLETED - Results from actual Gurobi model"]
                    real_model_success = True
                    
            except Exception as model_error:
                real_model_success = False
                model_error_msg = str(model_error)
            
            # ==========================================
            # STEP 2: IF REAL MODEL FAILED, TRY PRE-COMPUTED RESULTS
            # ==========================================
            if not real_model_success:
                precomputed_results = None
                try:
                    precomputed_results = load_precomputed_results(flight_path, model_type)
                    print(f"DEBUG: Pre-computed results check for flight '{flight_path}' (model: {model_type}): {precomputed_results is not None}")
                except Exception as load_error:
                    print(f"DEBUG: Error loading pre-computed results: {load_error}")
                    traceback.print_exc()
                
                if precomputed_results:
                    try:
                        # ✅ USE PRE-COMPUTED RESULTS FROM Results/ FOLDER
                        print(f"DEBUG: Extracting from pre-computed results, ULDs: {len(precomputed_results.get('ulds', []))}")
                        uld_info, cargo_items, weight_dist, uld_util = self._extract_from_precomputed_results(
                            precomputed_results, flight_row, data_paths
                        )
                        warnings = [
                            "⚠️ Real-time model execution failed.",
                            f"✅ Using pre-computed results from Results/ folder: {precomputed_results.get('results_folder', 'N/A')}",
                            "These are actual optimization results (not estimated)."
                        ]
                        print(f"DEBUG: Successfully extracted {len(uld_info)} ULDs from pre-computed results")
                    except Exception as precomputed_error:
                        # If pre-computed extraction fails, fall back to CSV
                        print(f"WARNING: Failed to extract from pre-computed results: {precomputed_error}")
                        traceback.print_exc()
                        precomputed_results = None  # Force CSV fallback
                
                if not precomputed_results:
                    # ==========================================
                    # STEP 3: LAST RESORT - CSV INPUT DATA FALLBACK
                    # ==========================================
                    # Only if no pre-computed results exist or extraction failed
                    piece_df = pd.read_csv(data_paths['piece_information'])
                    buildup_df = pd.read_csv(data_paths['buildup_information'])
                    
                    # Try to load LoadLocations.csv to get actual ULD positions
                    load_locations_df = None
                    try:
                        load_locations_df = pd.read_csv(data_paths['load_locations'])
                    except:
                        pass  # If LoadLocations doesn't exist, continue without it
                    
                    uld_info = self._extract_uld_info(buildup_df, load_locations_df)
                    cargo_items = self._extract_cargo_items(piece_df, buildup_df)
                    weight_dist = self._calculate_weight_distribution(buildup_df, uld_info, flight_row, load_locations_df)
                    uld_util = self._calculate_uld_utilization(buildup_df, uld_info)
                    
                    # More helpful error message
                    model_error_info = model_error_msg if 'model_error_msg' in locals() else 'Unknown error'
                    warnings = [
                        f"⚠️ Real-time model execution failed: {model_error_info}",
                        "⚠️ No pre-computed results found in Results/ folder for this flight.",
                        "💡 Tip: Some flights have pre-computed results. Try flights like:",
                        "   • Flights AMSSIN JAN 2024/Flight KL0835 AMSSIN 01 JAN 2024",
                        "   • Flights AMSLAX JAN 2024/Flight KL0601 AMSLAX 04 JAN 2024",
                        "Using CSV input data as fallback - weight distribution is ESTIMATED (not optimized)."
                    ]
            
            runtime = time.time() - start_time
            
            # Load KLM actual data for comparison
            klm_actual_data = load_klm_actual_data(flight_path)
            
            # Calculate all extended metrics
            cargo_metrics = self._calculate_cargo_metrics(cargo_items)
            performance_metrics = self._calculate_performance_metrics(weight_dist, runtime, model_results if real_model_success else None)
            optimization_metrics = self._calculate_optimization_metrics(runtime, model_results if real_model_success else None)
            safety_metrics = self._calculate_safety_metrics(weight_dist, uld_info, flight_row)
            
            # Calculate comparison metrics vs KLM actual
            comparison_metrics = self._calculate_comparison_metrics_vs_klm_actual(
                weight_dist, uld_util, performance_metrics, klm_actual_data, flight_row
            )
            
            # Enhance weight_distribution and uld_utilization with extended metrics
            weight_dist = self._enhance_weight_distribution(weight_dist, uld_info, flight_row)
            uld_util = self._enhance_uld_utilization(uld_util, uld_info, cargo_items)
            
            return OptimizationResult(
                success=True,
                flight_info=flight_info,
                weight_distribution=weight_dist,
                uld_utilization=uld_util,
                cargo_items=cargo_items,
                ulds=uld_info,
                    cargo_metrics=cargo_metrics,
                    performance_metrics=performance_metrics,
                    optimization_metrics=optimization_metrics,
                    safety_metrics=safety_metrics,
                    comparison_metrics=comparison_metrics,
                    fuel_savings_kg=comparison_metrics.fuel_savings_vs_klm_actual_kg if comparison_metrics else (performance_metrics.fuel_savings_kg if performance_metrics else None),
                    fuel_savings_percent=comparison_metrics.fuel_savings_vs_klm_actual_percent if comparison_metrics else (performance_metrics.fuel_savings_percent if performance_metrics else None),
                    runtime_seconds=runtime,
                    warnings=warnings if 'warnings' in locals() else []
                )
            
        except Exception as e:
            runtime = time.time() - start_time
            error_msg = str(e)
            error_trace = traceback.format_exc()
            
            return OptimizationResult(
                success=False,
                flight_info=FlightInfo(
                    flight_number="ERROR",
                    departure_airport="",
                    arrival_airport="",
                    date=""
                ),
                weight_distribution=WeightDistribution(
                    by_compartment={},
                    by_side={},
                    by_position={},
                    total_weight=0,
                    zfw=0,
                    mac_zfw=0
                ),
                uld_utilization=ULDUtilization(
                    total_ulds=0,
                    ulds_by_type={},
                    ulds_by_side={},
                    utilization_rate=0,
                    items_per_uld={}
                ),
                cargo_items=[],
                ulds=[],
                runtime_seconds=runtime,
                error_message=error_msg,
                warnings=[error_trace]
            )
    
    def _extract_uld_info_from_model(self, cargo, aircraft) -> List[ULDInfo]:
        """Extract ULD information from REAL model results"""
        ulds = []
        for idx, uld in enumerate(cargo.uld):
            if hasattr(uld, 'position') and uld.position:
                position = str(uld.position)
            else:
                position = None
            
            # Determine compartment from position
            compartment = None
            if position:
                if position[0] == '1' or position[0] == '2':
                    compartment = 'C1' if 'L' in position or int(position[0]) < 2 else 'C2'
                elif position[0] == '3':
                    compartment = 'C3'
                elif position[0] == '4':
                    compartment = 'C4'
            
            uld_info = ULDInfo(
                index=idx,
                type=uld.type,
                serialnumber=uld.serialnumber,
                weight=round(uld.weight, 2),
                max_weight=uld.max_weight if hasattr(uld, 'max_weight') else None,
                position=position,
                compartment=compartment
            )
            ulds.append(uld_info)
        
        return ulds
    
    def _extract_cargo_items_from_model(self, cargo) -> List[CargoItem]:
        """Extract cargo items from REAL model results"""
        items = []
        for idx, item in enumerate(cargo.items):
            # Find ULD assignment
            uld_assignment = None
            # This would need to be extracted from the model's p[i,j] variables
            # For now, we'll need to track this during model execution
            
            cargo_item = CargoItem(
                index=idx,
                serialnumber=item.serialnumber,
                number_of_pieces=item.number_of_pieces if hasattr(item, 'number_of_pieces') else 1,
                weight=round(item.weight, 2),
                volume=item.volume if hasattr(item, 'volume') else None,
                CRT=item.CRT if hasattr(item, 'CRT') else False,
                COL=item.COL if hasattr(item, 'COL') else False,
                dangerous=item.dangerous if hasattr(item, 'dangerous') else False,
                commodity=item.commodity if hasattr(item, 'commodity') else None,
                uld_assignment=uld_assignment
            )
            items.append(cargo_item)
        
        return items
    
    def _calculate_weight_distribution_from_model(self, cargo, aircraft, flight_row: pd.Series, flight_path: Optional[str] = None) -> WeightDistribution:
        """Calculate weight distribution from REAL model results"""
        # Calculate by compartment
        weight_by_compartment = {'C1': 0, 'C2': 0, 'C3': 0, 'C4': 0}
        weight_by_side = {'Left': 0, 'Right': 0}
        weight_by_position = {}
        
        for uld in cargo.uld:
            if hasattr(uld, 'position') and uld.position:
                position = str(uld.position)
                
                # Determine compartment
                if position[0] == '1':
                    compartment = 'C1'
                elif position[0] == '2':
                    compartment = 'C2'
                elif position[0] == '3':
                    compartment = 'C3'
                elif position[0] == '4':
                    compartment = 'C4'
                else:
                    compartment = 'C1'  # Default
                
                weight_by_compartment[compartment] += uld.weight
                
                # Determine side
                if 'L' in position:
                    weight_by_side['Left'] += uld.weight
                elif 'R' in position:
                    weight_by_side['Right'] += uld.weight
                
                weight_by_position[position] = weight_by_position.get(position, 0) + uld.weight
        
        total_weight = sum(weight_by_compartment.values())
        zfw = float(flight_row.get('ActualZeroFuelWeight', total_weight + 132000))
        
        # Calculate MAC ZFW from weight distribution (don't use KLM's actual MAC)
        aircraft_type = str(flight_row.get('AircraftType', ''))
        klm_actual_mac = float(flight_row.get('MacZFW', 18.5))
        
        mac_zfw = calculate_mac_zfw_from_distribution(
            weight_by_compartment=weight_by_compartment,
            aircraft_type=aircraft_type,
            zfw=zfw
        )
        
        # If calculation fails, estimate MAC change based on weight shift from KLM actual
        if mac_zfw is None and flight_path:
            # Try to estimate MAC change from weight distribution differences
            # Forward compartments (C1, C2) shift MAC forward (lower %), aft (C3, C4) shift aft (higher %)
            # Use KLM actual as baseline and estimate change
            try:
                klm_actual_weights = load_klm_actual_data(flight_path)
                if klm_actual_weights:
                    klm_C1 = klm_actual_weights.get('weight_by_compartment', {}).get('C1', 0)
                    klm_C2 = klm_actual_weights.get('weight_by_compartment', {}).get('C2', 0)
                    klm_C3 = klm_actual_weights.get('weight_by_compartment', {}).get('C3', 0)
                    klm_C4 = klm_actual_weights.get('weight_by_compartment', {}).get('C4', 0)
                    
                    # Calculate weight shift (optimized - KLM actual)
                    forward_shift = (weight_by_compartment.get('C1', 0) - klm_C1) + (weight_by_compartment.get('C2', 0) - klm_C2)
                    aft_shift = (weight_by_compartment.get('C3', 0) - klm_C3) + (weight_by_compartment.get('C4', 0) - klm_C4)
                    
                    # Estimate MAC change: Moving weight aft increases MAC, forward decreases it
                    # Rough estimate: ~0.02% MAC per 1000kg net shift aft
                    net_shift_kg = aft_shift - forward_shift
                    mac_change = net_shift_kg / 1000 * 0.02
                    mac_zfw = klm_actual_mac + mac_change
                else:
                    mac_zfw = klm_actual_mac  # Use KLM actual as fallback
            except:
                mac_zfw = klm_actual_mac  # Use KLM actual as fallback
        elif mac_zfw is None:
            mac_zfw = klm_actual_mac  # Use KLM actual as fallback
        
        return WeightDistribution(
            by_compartment=weight_by_compartment,
            by_side=weight_by_side,
            by_position=weight_by_position,
            total_weight=total_weight,
            zfw=zfw,
            mac_zfw=mac_zfw
        )
    
    def _calculate_uld_utilization_from_model(self, cargo, aircraft) -> ULDUtilization:
        """Calculate ULD utilization from REAL model results"""
        ulds_by_type = {}
        ulds_by_side = {'Left': 0, 'Right': 0}
        items_per_uld = {}
        
        for idx, uld in enumerate(cargo.uld):
            # Count by type
            ulds_by_type[uld.type] = ulds_by_type.get(uld.type, 0) + 1
            
            # Count by side
            if hasattr(uld, 'position') and uld.position:
                pos = str(uld.position)
                if 'L' in pos:
                    ulds_by_side['Left'] += 1
                elif 'R' in pos:
                    ulds_by_side['Right'] += 1
        
        # Calculate utilization
        total_weight = sum(uld.weight for uld in cargo.uld)
        total_max_weight = sum(uld.max_weight if hasattr(uld, 'max_weight') else 3000 for uld in cargo.uld)
        utilization_rate = min(total_weight / total_max_weight if total_max_weight > 0 else 0.75, 1.0)
        
        return ULDUtilization(
            total_ulds=len(cargo.uld),
            ulds_by_type=ulds_by_type,
            ulds_by_side=ulds_by_side,
            utilization_rate=utilization_rate,
            items_per_uld=items_per_uld
        )
    
    def _extract_from_precomputed_results(
        self,
        precomputed: Dict[str, Any],
        flight_row: pd.Series,
        data_paths: Dict[str, str]
    ) -> Tuple[List[ULDInfo], List[CargoItem], WeightDistribution, ULDUtilization]:
        """
        Extract data from pre-computed Results folder
        
        Args:
            precomputed: Dictionary from load_precomputed_results()
            flight_row: Flight information row
            data_paths: Paths to input CSV files
        
        Returns:
            Tuple of (uld_info, cargo_items, weight_dist, uld_util)
        """
        # Extract ULDs with positions from Results.txt
        uld_info = []
        uld_serial_to_idx = {}
        
        for idx, uld_data in enumerate(precomputed.get('ulds', [])):
            uld = ULDInfo(
                index=idx,
                type=uld_data['serial'][:3] if len(uld_data['serial']) >= 3 else 'UNK',
                serialnumber=uld_data['serial'],
                weight=uld_data['weight'],
                position=uld_data['position'],
                compartment=uld_data['compartment']
            )
            uld_info.append(uld)
            uld_serial_to_idx[uld_data['serial']] = idx
        
        # Extract cargo items from input CSV (need this for full info)
        piece_df = pd.read_csv(data_paths['piece_information'])
        buildup_df = pd.read_csv(data_paths['buildup_information'])
        cargo_items = self._extract_cargo_items(piece_df, buildup_df)
        
        # Update cargo items with ULD assignments from buildup
        awb_to_uld = {}
        for _, row in buildup_df.iterrows():
            awb = str(row.get('AirWaybillNumber', ''))
            uld_serial = row.get('ULD', '')
            if awb not in awb_to_uld:
                awb_to_uld[awb] = uld_serial
        
        for item in cargo_items:
            # Try to find ULD assignment
            for awb, uld_serial in awb_to_uld.items():
                if awb in item.serialnumber or item.serialnumber.split('-')[-1] == awb:
                    item.uld_assignment = uld_serial_to_idx.get(uld_serial)
                    break
        
        # Calculate weight distribution from pre-computed compartment weights
        weight_by_compartment = precomputed.get('weight_by_compartment', {})
        total_weight = sum(weight_by_compartment.values())
        
        # Calculate by side from ULD positions
        weight_by_side = {'Left': 0, 'Right': 0}
        weight_by_position = {}
        
        for uld_data in precomputed.get('ulds', []):
            weight = uld_data['weight']
            position = uld_data['position']
            side = uld_data.get('side')
            
            if side == 'Left':
                weight_by_side['Left'] += weight
            elif side == 'Right':
                weight_by_side['Right'] += weight
            
            weight_by_position[position] = weight_by_position.get(position, 0) + weight
        
        # Get ZFW from General_Information.txt or flight_row
        zfw = precomputed.get('zfw') or float(flight_row.get('ActualZeroFuelWeight', total_weight + 132000))
        mac_zfw = precomputed.get('mac_zfw') or float(flight_row.get('MacZFW', 18.5))
        
        weight_dist = WeightDistribution(
            by_compartment=weight_by_compartment,
            by_side=weight_by_side,
            by_position=weight_by_position,
            total_weight=total_weight,
            zfw=zfw,
            mac_zfw=mac_zfw
        )
        
        # Calculate ULD utilization
        ulds_by_type = {}
        ulds_by_side = {'Left': 0, 'Right': 0}
        items_per_uld = {}
        
        for uld_data in precomputed.get('ulds', []):
            uld_type = uld_data['serial'][:3] if len(uld_data['serial']) >= 3 else 'UNK'
            ulds_by_type[uld_type] = ulds_by_type.get(uld_type, 0) + 1
            
            side = uld_data.get('side')
            if side == 'Left':
                ulds_by_side['Left'] += 1
            elif side == 'Right':
                ulds_by_side['Right'] += 1
        
        # Count items per ULD from buildup
        for _, row in buildup_df.iterrows():
            uld_serial = row.get('ULD', '')
            if uld_serial in uld_serial_to_idx:
                uld_idx = uld_serial_to_idx[uld_serial]
                items_per_uld[uld_idx] = items_per_uld.get(uld_idx, 0) + 1
        
        # Calculate utilization rate
        total_uld_weight = sum(uld.weight for uld in uld_info)
        max_weights = {'PMC': 4500, 'PAG': 4500, 'AAP': 4500, 'AKE': 1588, 'AAK': 1588}
        total_max_weight = sum(max_weights.get(uld.type, 3000) for uld in uld_info)
        utilization_rate = min(total_uld_weight / total_max_weight if total_max_weight > 0 else 0.75, 1.0)
        
        uld_util = ULDUtilization(
            total_ulds=len(uld_info),
            ulds_by_type=ulds_by_type,
            ulds_by_side=ulds_by_side,
            utilization_rate=utilization_rate,
            items_per_uld=items_per_uld
        )
        
        return uld_info, cargo_items, weight_dist, uld_util
    
    def _extract_uld_info(self, buildup_df: pd.DataFrame, load_locations_df: Optional[pd.DataFrame] = None) -> List[ULDInfo]:
        """Extract ULD information from CSV (fallback)"""
        ulds = []
        
        # Find ULD column name (could be 'ULD', 'ULDSerialNumber', etc.)
        uld_col = None
        for col in ['ULD', 'ULDSerialNumber', 'DeadloadId']:
            if col in buildup_df.columns:
                uld_col = col
                break
        
        if uld_col is None:
            return ulds  # No ULD column found
        
        unique_ulds = buildup_df[uld_col].unique()
        
        # Find weight column name (could be 'Weight', 'TotalWeightOnAWB', 'TotalWeight', etc.)
        weight_col = None
        for col in ['Weight', 'TotalWeightOnAWB', 'TotalWeight', 'WeightOnAWB']:
            if col in buildup_df.columns:
                weight_col = col
                break
        
        # Try to get positions from LoadLocations.csv
        position_map = {}  # uld_serial -> position
        if load_locations_df is not None:
            # Find SerialNumber and LoadLocation columns
            serial_col = None
            location_col = None
            for col in ['SerialNumber', 'ULDSerialNumber', 'DeadloadId']:
                if col in load_locations_df.columns:
                    serial_col = col
                    break
            for col in ['LoadLocation', 'Position', 'Location']:
                if col in load_locations_df.columns:
                    location_col = col
                    break
            
            if serial_col and location_col:
                # Map serial numbers to positions
                for _, row in load_locations_df.iterrows():
                    serial = str(row.get(serial_col, ''))
                    location = str(row.get(location_col, ''))
                    if serial and location and pd.notna(location):
                        # Keep the most recent position (if duplicate)
                        position_map[serial] = location
        
        for idx, uld_serial in enumerate(unique_ulds):
            uld_type = str(uld_serial)[:3] if len(str(uld_serial)) >= 3 else 'UNK'
            
            # Calculate weight for this ULD
            if weight_col:
                uld_df = buildup_df[buildup_df[uld_col] == uld_serial]
                uld_weight = uld_df[weight_col].sum() if len(uld_df) > 0 else 0.0
            else:
                # Fallback: count items and estimate weight
                uld_df = buildup_df[buildup_df[uld_col] == uld_serial]
                uld_weight = len(uld_df) * 100.0  # Rough estimate
            
            # Get position from LoadLocations if available
            position = position_map.get(str(uld_serial))
            
            # Determine compartment from position
            compartment = None
            if position:
                if position[0] == '1':
                    compartment = 'C1'
                elif position[0] == '2':
                    compartment = 'C2'
                elif position[0] == '3':
                    compartment = 'C3'
                elif position[0] == '4':
                    compartment = 'C4'
            
            uld_info = ULDInfo(
                index=idx,
                type=uld_type,
                serialnumber=str(uld_serial),
                weight=round(uld_weight, 2),
                position=position,
                compartment=compartment
            )
            ulds.append(uld_info)
        
        return ulds
    
    def _extract_cargo_items(self, piece_df: pd.DataFrame, buildup_df: pd.DataFrame) -> List[CargoItem]:
        """Extract cargo items from CSV"""
        items = []
        
        # Find column names with fallbacks
        def get_col(df, alternatives, default=None):
            for alt in alternatives:
                if alt in df.columns:
                    return alt
            return default
        
        serial_col = get_col(piece_df, ['SerialNumber', 'BookingAirWaybillNumber', 'AirWaybillNumber'], 'SerialNumber')
        pieces_col = get_col(piece_df, ['NumberOfPieces', 'BookingSegmentPieceCount', 'BookingTotalPieceCount'], 'NumberOfPieces')
        weight_col = get_col(piece_df, ['Weight', 'BookingLinePieceWeight', 'BookingSegmentPiecesWeight', 'BookingTotalWeight'], 'Weight')
        volume_col = get_col(piece_df, ['Volume', 'BookingLinePieceVolume', 'BookingSegmentVolume', 'BookingTotalVolume'], 'Volume')
        crt_col = get_col(piece_df, ['CRT', 'IsCRT'], 'CRT')
        col_col = get_col(piece_df, ['COL', 'IsCOL'], 'COL')
        dangerous_col = get_col(piece_df, ['Dangerous', 'IsDangerousGoods', 'DangerousGoods'], 'Dangerous')
        commodity_col = get_col(piece_df, ['Commodity', 'BookingCommodityCode'], 'Commodity')
        
        for idx, row in piece_df.iterrows():
            # Get values with defaults
            serial = str(row.get(serial_col, f'ITEM-{idx}')) if serial_col else f'ITEM-{idx}'
            pieces = int(row.get(pieces_col, 1)) if pieces_col and pd.notna(row.get(pieces_col)) else 1
            weight = float(row.get(weight_col, 0)) if weight_col and pd.notna(row.get(weight_col)) else 0.0
            volume_val = row.get(volume_col) if volume_col else None
            volume = float(volume_val) if volume_val is not None and pd.notna(volume_val) else None
            
            crt = bool(row.get(crt_col, False)) if crt_col and pd.notna(row.get(crt_col)) else False
            col = bool(row.get(col_col, False)) if col_col and pd.notna(row.get(col_col)) else False
            dangerous = bool(row.get(dangerous_col, False)) if dangerous_col and pd.notna(row.get(dangerous_col)) else False
            
            commodity_val = row.get(commodity_col) if commodity_col else None
            commodity = str(commodity_val) if commodity_val is not None and pd.notna(commodity_val) else None
            
            cargo_item = CargoItem(
                index=idx,
                serialnumber=serial,
                number_of_pieces=pieces,
                weight=weight,
                volume=volume,
                CRT=crt,
                COL=col,
                dangerous=dangerous,
                commodity=commodity,
                uld_assignment=None
            )
            items.append(cargo_item)
        
        return items
    
    def _calculate_weight_distribution(self, buildup_df: pd.DataFrame, ulds: List[ULDInfo], flight_row: pd.Series, load_locations_df: Optional[pd.DataFrame] = None) -> WeightDistribution:
        """Calculate weight distribution (CSV fallback)"""
        total_weight = sum(uld.weight for uld in ulds)
        
        # Try to load LoadLocations.csv to get actual positions
        weight_by_compartment = {'C1': 0, 'C2': 0, 'C3': 0, 'C4': 0}
        weight_by_side = {'Left': 0, 'Right': 0}
        weight_by_position = {}
        
        # Try to find LoadLocations.csv from the flight data paths
        try:
            # Get the flight directory path
            flight_path = str(flight_row.get('FlightPath', '')) if 'FlightPath' in flight_row else None
            if not flight_path:
                # Try to construct from flight info
                from utils.path_utils import get_flight_data_path
                # This won't work here, so we'll check if we can get positions from ULDs
                pass
        except:
            pass
        
        # If ULDs have positions, use them
        ulds_with_positions = [uld for uld in ulds if uld.position]
        if ulds_with_positions:
            # Calculate from actual ULD positions
            for uld in ulds_with_positions:
                if uld.position:
                    position = str(uld.position)
                    # Determine compartment from position
                    if position[0] == '1':
                        compartment = 'C1'
                    elif position[0] == '2':
                        compartment = 'C2'
                    elif position[0] == '3':
                        compartment = 'C3'
                    elif position[0] == '4':
                        compartment = 'C4'
                    else:
                        compartment = 'C1'
                    
                    weight_by_compartment[compartment] += uld.weight
                    
                    # Determine side
                    if 'L' in position:
                        weight_by_side['Left'] += uld.weight
                    elif 'R' in position:
                        weight_by_side['Right'] += uld.weight
                    
                    weight_by_position[position] = weight_by_position.get(position, 0) + uld.weight
        else:
            # Fallback: estimate distribution (but don't force 50/50)
            # Use a more realistic distribution if we have no position data
            # Distribute based on ULD type and typical locations
            left_weight = 0
            right_weight = 0
            
            for idx, uld in enumerate(ulds):
                # Alternate left/right based on index (not perfect, but better than 50/50)
                if idx % 2 == 0:
                    left_weight += uld.weight
                else:
                    right_weight += uld.weight
                
                # Estimate compartment based on ULD type (larger ULDs tend to go in C1/C2)
                if uld.type in ['PMC', 'PAG', 'AAP']:
                    if idx % 2 == 0:
                        weight_by_compartment['C1'] += uld.weight * 0.6
                        weight_by_compartment['C2'] += uld.weight * 0.4
                    else:
                        weight_by_compartment['C2'] += uld.weight * 0.6
                        weight_by_compartment['C3'] += uld.weight * 0.4
                else:
                    # Smaller ULDs (AKE, AAK) often go in C3/C4
                    if idx % 2 == 0:
                        weight_by_compartment['C3'] += uld.weight * 0.6
                        weight_by_compartment['C4'] += uld.weight * 0.4
                    else:
                        weight_by_compartment['C4'] += uld.weight * 0.6
                        weight_by_compartment['C3'] += uld.weight * 0.4
            
            weight_by_side['Left'] = left_weight
            weight_by_side['Right'] = right_weight
        
        zfw = float(flight_row.get('ActualZeroFuelWeight', total_weight + 132000))
        
        # Calculate MAC ZFW from weight distribution
        aircraft_type = str(flight_row.get('AircraftType', ''))
        mac_zfw = calculate_mac_zfw_from_distribution(
            weight_by_compartment=weight_by_compartment,
            aircraft_type=aircraft_type,
            zfw=zfw
        )
        
        # Fallback to flight_row MAC if calculation fails
        if mac_zfw is None:
            mac_zfw = float(flight_row.get('MacZFW', 18.5))
        
        return WeightDistribution(
            by_compartment=weight_by_compartment,
            by_side=weight_by_side,
            by_position=weight_by_position,
            total_weight=total_weight,
            zfw=zfw,
            mac_zfw=mac_zfw
        )
    
    def _calculate_uld_utilization(self, buildup_df: pd.DataFrame, ulds: List[ULDInfo]) -> ULDUtilization:
        """Calculate ULD utilization metrics (CSV fallback)"""
        # Find ULD column name
        uld_col = None
        for col in ['ULD', 'ULDSerialNumber', 'DeadloadId']:
            if col in buildup_df.columns:
                uld_col = col
                break
        
        if uld_col is None:
            # Return empty if no ULD column
            return ULDUtilization(
                total_ulds=len(ulds),
                ulds_by_type={},
                ulds_by_side={},
                utilization_rate=0.0,
                items_per_uld={}
            )
        
        # Count items per ULD
        items_per_uld = {}
        uld_item_counts = buildup_df.groupby(uld_col).size()
        
        for idx, uld in enumerate(ulds):
            count = uld_item_counts.get(uld.serialnumber, 0)
            items_per_uld[idx] = int(count)
        
        # Count ULDs by type
        ulds_by_type = {}
        for uld in ulds:
            ulds_by_type[uld.type] = ulds_by_type.get(uld.type, 0) + 1
        
        # Mock side distribution - distribute evenly
        total_ulds = len(ulds)
        ulds_by_side = {
            'Left': total_ulds // 2,
            'Right': total_ulds - total_ulds // 2
        }
        
        # Calculate utilization rate (estimate based on typical max weights)
        # Typical max weights: PMC ~4500kg, PAG ~4500kg, AKE ~1588kg
        max_weights = {
            'PMC': 4500,
            'PAG': 4500,
            'AAP': 4500,
            'AKE': 1588,
            'AAK': 1588
        }
        
        total_max_weight = sum(max_weights.get(uld.type, 3000) for uld in ulds)
        total_weight = sum(uld.weight for uld in ulds)
        
        # Calculate utilization rate properly - average of individual ULD utilizations
        if total_max_weight > 0 and len(ulds) > 0:
            # Calculate utilization per ULD and average
            utilizations = []
            for uld in ulds:
                max_w = max_weights.get(uld.type, 3000)
                if max_w > 0:
                    utilizations.append(uld.weight / max_w)
            
            if utilizations:
                avg_utilization = np.mean(utilizations)
            else:
                avg_utilization = total_weight / total_max_weight if total_max_weight > 0 else 0.75
        else:
            avg_utilization = 0.75  # Default if no data
        
        # Cap at 100% but don't force it
        utilization_rate = min(avg_utilization, 1.0)
        
        return ULDUtilization(
            total_ulds=len(ulds),
            ulds_by_type=ulds_by_type,
            ulds_by_side=ulds_by_side,
            utilization_rate=utilization_rate,
            items_per_uld=items_per_uld
        )
    
    def _calculate_cargo_metrics(self, cargo_items: List[CargoItem]) -> CargoMetrics:
        """Calculate comprehensive cargo item metrics"""
        if not cargo_items:
            return CargoMetrics(total_items=0)
        
        total_items = len(cargo_items)
        weights = [item.weight for item in cargo_items]
        volumes = [item.volume for item in cargo_items if item.volume]
        
        # Items by type/commodity
        items_by_type = {}
        weight_by_commodity = {}
        for item in cargo_items:
            if item.commodity:
                items_by_type[item.commodity] = items_by_type.get(item.commodity, 0) + 1
                weight_by_commodity[item.commodity] = weight_by_commodity.get(item.commodity, 0) + item.weight
        
        # Items by weight range
        weight_ranges = {
            "0-100": 0, "100-500": 0, "500-1000": 0, 
            "1000-2000": 0, "2000-5000": 0, "5000+": 0
        }
        for weight in weights:
            if weight < 100:
                weight_ranges["0-100"] += 1
            elif weight < 500:
                weight_ranges["100-500"] += 1
            elif weight < 1000:
                weight_ranges["500-1000"] += 1
            elif weight < 2000:
                weight_ranges["1000-2000"] += 1
            elif weight < 5000:
                weight_ranges["2000-5000"] += 1
            else:
                weight_ranges["5000+"] += 1
        
        # Count special items
        total_crt = sum(1 for item in cargo_items if item.CRT)
        total_col = sum(1 for item in cargo_items if item.COL)
        total_dangerous = sum(1 for item in cargo_items if item.dangerous)
        items_without_uld = sum(1 for item in cargo_items if item.uld_assignment is None)
        
        # Largest items (top 10)
        sorted_items = sorted(cargo_items, key=lambda x: x.weight, reverse=True)
        largest_items = [
            {
                "index": item.index,
                "serialnumber": item.serialnumber,
                "weight": item.weight,
                "commodity": item.commodity or "Unknown"
            }
            for item in sorted_items[:10]
        ]
        
        return CargoMetrics(
            total_items=total_items,
            items_by_type=items_by_type,
            items_by_weight_range=weight_ranges,
            items_without_uld=items_without_uld,
            average_item_weight=np.mean(weights) if weights else None,
            max_item_weight=max(weights) if weights else None,
            min_item_weight=min(weights) if weights else None,
            total_crt_items=total_crt,
            total_col_items=total_col,
            total_dangerous_items=total_dangerous,
            total_volume=sum(volumes) if volumes else None,
            weight_distribution_by_commodity=weight_by_commodity,
            largest_items=largest_items
        )
    
    def _calculate_performance_metrics(
        self, 
        weight_dist: WeightDistribution, 
        runtime: float,
        model_results: Optional[Dict] = None
    ) -> PerformanceMetrics:
        """Calculate performance and savings metrics"""
        # Extract fuel savings from model results or pre-computed results
        fuel_savings_kg = None
        fuel_savings_percent = None
        
        if model_results:
            fuel_savings_kg = model_results.get('fuel_savings_kg')
            fuel_savings_percent = model_results.get('fuel_savings_percent')
        
        # Estimate cost savings (realistic bulk jet fuel price: $1.50/kg)
        # Airlines negotiate bulk contracts with fuel suppliers, typically 20-40% discount
        # Current market ~$2.00-2.50/kg retail, bulk contracts ~$1.20-1.80/kg
        cost_savings_usd = fuel_savings_kg * 1.50 if fuel_savings_kg else None
        
        # Estimate CO2 emissions saved (rough: 3.15 kg CO2 per kg fuel)
        co2_saved = fuel_savings_kg * 3.15 if fuel_savings_kg else None
        
        # Calculate load factor (weight/volume ratio, normalized)
        # Load factor = actual cargo weight / (volume capacity * typical cargo density)
        # Without actual volume data, we can't calculate this accurately
        # So set to None unless we have real volume data
        load_factor = None
        # Note: Load factor requires actual volume data, which we don't have reliably
        # from CSV fallback. Only calculate if we have volume data from model results.
        
        # Efficiency score (combination of utilization and balance)
        efficiency_score = None
        if weight_dist.balance_ratio is not None and weight_dist.total_weight > 0:
            # Balance score: closer to 1.0 (perfect balance) is better
            # 1.0 = perfect balance (left/right ratio = 1.0)
            balance_ratio_val = weight_dist.balance_ratio
            # Score decreases as we move away from 1.0
            # If ratio is 0.9 or 1.1, score is 0.9; if 0.5 or 2.0, score is 0.5
            balance_score = 1.0 - min(abs(1.0 - balance_ratio_val), 1.0)
            
            # Utilization score: how much of available capacity is used
            # Don't force 100% - calculate based on actual weight vs aircraft capacity
            available_cargo_capacity = weight_dist.zfw - 132000  # Approximate empty weight
            if available_cargo_capacity > 0:
                utilization_score = min(weight_dist.total_weight / available_cargo_capacity, 1.0)
            else:
                utilization_score = 0.8  # Default if we can't calculate
            
            efficiency_score = (balance_score * 0.5 + utilization_score * 0.5)
        elif weight_dist.total_weight > 0:
            # If no balance ratio, just use utilization
            available_cargo_capacity = weight_dist.zfw - 132000
            if available_cargo_capacity > 0:
                utilization_score = min(weight_dist.total_weight / available_cargo_capacity, 1.0)
                efficiency_score = utilization_score
        
        return PerformanceMetrics(
            fuel_savings_kg=fuel_savings_kg,
            fuel_savings_percent=fuel_savings_percent,
            cost_savings_usd=cost_savings_usd,
            co2_emissions_saved_kg=co2_saved,
            load_factor=load_factor,
            efficiency_score=efficiency_score
        )
    
    def _calculate_optimization_metrics(
        self,
        runtime: float,
        model_results: Optional[Dict] = None
    ) -> OptimizationMetrics:
        """Calculate optimization solver metrics"""
        solver_status = "Feasible"
        objective_value = None
        gap_percent = None
        
        if model_results:
            solver_status = model_results.get('solver_status', 'Feasible')
            objective_value = model_results.get('objective_value')
            gap_percent = model_results.get('gap_percent')
        
        return OptimizationMetrics(
            runtime_seconds=runtime,
            solver_status=solver_status,
            objective_value=objective_value,
            gap_percent=gap_percent
        )
    
    def _calculate_safety_metrics(
        self,
        weight_dist: WeightDistribution,
        ulds: List[ULDInfo],
        flight_row: pd.Series
    ) -> SafetyMetrics:
        """Calculate safety and compliance metrics"""
        # Weight limits compliance per compartment
        max_compartment_weights = {
            'C1': 20000, 'C2': 20000, 'C3': 15000, 'C4': 15000
        }
        
        weight_limits_compliance = {}
        for comp, weight in weight_dist.by_compartment.items():
            max_weight = max_compartment_weights.get(comp, 20000)
            weight_limits_compliance[comp] = weight <= max_weight
        
        # Balance compliance (typically ±5% difference)
        balance_compliance = {}
        if weight_dist.by_side.get('Left', 0) > 0 and weight_dist.by_side.get('Right', 0) > 0:
            total_side_weight = weight_dist.by_side['Left'] + weight_dist.by_side['Right']
            left_pct = weight_dist.by_side['Left'] / total_side_weight if total_side_weight > 0 else 0.5
            right_pct = weight_dist.by_side['Right'] / total_side_weight if total_side_weight > 0 else 0.5
            balance_compliance['Left'] = 0.45 <= left_pct <= 0.55  # ±5% tolerance
            balance_compliance['Right'] = 0.45 <= right_pct <= 0.55
        
        # CG compliance (MAC ZFW should be within certain range, typically 15-35%)
        cg_compliance = None
        if weight_dist.mac_zfw:
            cg_compliance = 15.0 <= weight_dist.mac_zfw <= 35.0
        
        # Safety score (0-1)
        safety_score = None
        compliant_count = sum(1 for v in weight_limits_compliance.values() if v)
        total_checks = len(weight_limits_compliance) + len(balance_compliance) + (1 if cg_compliance is not None else 0)
        passed_checks = compliant_count + sum(1 for v in balance_compliance.values() if v) + (1 if cg_compliance else 0)
        safety_score = passed_checks / total_checks if total_checks > 0 else 1.0
        
        return SafetyMetrics(
            weight_limits_compliance=weight_limits_compliance,
            balance_limits_compliance=balance_compliance,
            cg_limits_compliance=cg_compliance,
            safety_score=safety_score
        )
    
    def _calculate_comparison_metrics_vs_klm_actual(
        self,
        weight_dist: WeightDistribution,
        uld_util: ULDUtilization,
        performance_metrics: Optional[PerformanceMetrics],
        klm_actual_data: Optional[Dict[str, Any]],
        flight_row: pd.Series
    ) -> ComparisonMetrics:
        """Calculate comparison metrics vs KLM actual loading"""
        if not klm_actual_data:
            return ComparisonMetrics(klm_actual=None)
        
        # Create KLM actual metrics object
        klm_actual_metrics = KLMActualMetrics(
            actual_mac_zfw=klm_actual_data.get('actual_mac_zfw'),
            actual_weight_by_compartment=klm_actual_data.get('weight_by_compartment', {}),
            actual_weight_by_side=klm_actual_data.get('weight_by_side', {}),
            actual_total_weight=klm_actual_data.get('total_weight'),
            actual_total_ulds=klm_actual_data.get('total_ulds'),
            trip_fuel=klm_actual_data.get('trip_fuel')
        )
        
        # Calculate weight differences by compartment
        weight_diff_by_compartment = {}
        for comp in ['C1', 'C2', 'C3', 'C4']:
            optimized_weight = weight_dist.by_compartment.get(comp, 0)
            actual_weight = klm_actual_data.get('weight_by_compartment', {}).get(comp, 0)
            weight_diff_by_compartment[comp] = optimized_weight - actual_weight
        
        # Calculate weight differences by side
        weight_diff_by_side = {}
        for side in ['Left', 'Right']:
            optimized_weight = weight_dist.by_side.get(side, 0)
            actual_weight = klm_actual_data.get('weight_by_side', {}).get(side, 0)
            weight_diff_by_side[side] = optimized_weight - actual_weight
        
        # ULD count difference
        uld_count_diff = uld_util.total_ulds - klm_actual_data.get('total_ulds', 0) if klm_actual_data.get('total_ulds') else None
        
        # MAC difference
        mac_diff = weight_dist.mac_zfw - klm_actual_data.get('actual_mac_zfw') if klm_actual_data.get('actual_mac_zfw') else None
        
        # Calculate fuel savings vs KLM actual
        fuel_savings_data = None
        if weight_dist.mac_zfw and klm_actual_data.get('actual_mac_zfw'):
            aircraft_type = str(flight_row.get('AircraftType', ''))
            trip_fuel = klm_actual_data.get('trip_fuel', 60000)
            
            fuel_savings_data = calculate_fuel_savings_vs_klm_actual(
                optimized_mac_zfw=weight_dist.mac_zfw,
                actual_mac_zfw=klm_actual_data['actual_mac_zfw'],
                trip_fuel=trip_fuel,
                aircraft_type=aircraft_type
            )
        
        # Cost savings (realistic bulk jet fuel price: $1.50/kg)
        # Airlines get bulk discounts, typically $1.20-1.80/kg vs market $2.00-2.50/kg
        cost_savings_usd = None
        if fuel_savings_data and fuel_savings_data.get('fuel_savings_kg'):
            cost_savings_usd = fuel_savings_data['fuel_savings_kg'] * 1.50
        
        # CO2 savings (3.15 kg CO2 per kg fuel)
        co2_savings_kg = None
        if fuel_savings_data and fuel_savings_data.get('fuel_savings_kg'):
            co2_savings_kg = fuel_savings_data['fuel_savings_kg'] * 3.15
        
        # Overall improvement percentage (based on fuel savings)
        improvement_percent = None
        if fuel_savings_data and fuel_savings_data.get('fuel_savings_percent'):
            improvement_percent = fuel_savings_data['fuel_savings_percent']
        
        # Calculate annual impact
        annual_impact = self._calculate_annual_impact(
            fuel_savings_kg=fuel_savings_data.get('fuel_savings_kg') if fuel_savings_data else None,
            cost_savings_usd=cost_savings_usd,
            co2_savings_kg=co2_savings_kg
        )
        
        return ComparisonMetrics(
            klm_actual=klm_actual_metrics,
            weight_difference_by_compartment=weight_diff_by_compartment,
            weight_difference_by_side=weight_diff_by_side,
            uld_count_difference=uld_count_diff,
            fuel_savings_vs_klm_actual_kg=fuel_savings_data.get('fuel_savings_kg') if fuel_savings_data else None,
            fuel_savings_vs_klm_actual_percent=fuel_savings_data.get('fuel_savings_percent') if fuel_savings_data else None,
            cost_savings_vs_klm_actual_usd=cost_savings_usd,
            co2_savings_vs_klm_actual_kg=co2_savings_kg,
            mac_difference=mac_diff,
            improvement_percentage=improvement_percent,
            annual_impact=annual_impact
        )
    
    def _calculate_annual_impact(
        self,
        fuel_savings_kg: Optional[float],
        cost_savings_usd: Optional[float],
        co2_savings_kg: Optional[float]
    ) -> Optional[AnnualImpactMetrics]:
        """
        Calculate annual impact based on per-flight savings
        
        Based on research:
        - KLM operates ~12,000-15,000 intercontinental flights per year
        - Average fuel savings per flight: ~360 kg (from thesis)
        - Fuel price: ~$1.50/kg (jet fuel bulk purchase, accounts for airline discounts)
          Market rate: ~$2.00-2.50/kg retail (as of 2024-2025)
          Bulk airline contracts: typically $1.20-1.80/kg (20-40% discount)
          Using $1.50/kg as conservative estimate for KLM bulk purchases
        - CO2 conversion: 3.15 kg CO2 per kg fuel
        """
        # Calculate annual impact even for negative savings (to show the cost)
        # Only skip if fuel_savings_kg is None (not calculated)
        if fuel_savings_kg is None:
            return None
        
        # Realistic jet fuel price for airline bulk purchases
        # Airlines negotiate bulk contracts with fuel suppliers
        # Current market (2024-2025): ~$2.00-2.50/kg retail
        # Bulk airline contracts: typically $1.20-1.80/kg (discounts of 20-40%)
        # Using $1.50/kg as conservative estimate for KLM bulk purchases
        fuel_price_per_kg = 1.50
        
        # Research-based estimates for KLM intercontinental flights
        # KLM operates wide-body aircraft (777, 787) on intercontinental routes
        # Based on data: ~525 flights in dataset covering several months
        # Conservative estimate: ~12,000 intercontinental flights per year
        # (considering KLM has ~300 wide-body aircraft and each makes ~40 intercontinental flights/year)
        flights_per_year = 12000  # Conservative estimate for intercontinental flights
        
        # Calculate annual totals
        fuel_savings_per_year_kg = fuel_savings_kg * flights_per_year
        
        # Convert to liters (jet fuel density ~0.8 kg/L)
        fuel_savings_per_year_liters = fuel_savings_per_year_kg / 0.8
        
        # Cost savings (use cost_savings_usd per flight if available, otherwise estimate)
        if cost_savings_usd:
            cost_savings_per_year_usd = cost_savings_usd * flights_per_year
        else:
            # Estimate using realistic bulk fuel price
            cost_savings_per_year_usd = fuel_savings_per_year_kg * fuel_price_per_kg
        
        # CO2 reduction
        if co2_savings_kg:
            co2_reduction_per_year_kg = co2_savings_kg * flights_per_year
        else:
            # Estimate: 3.15 kg CO2 per kg fuel
            co2_reduction_per_year_kg = fuel_savings_per_year_kg * 3.15
        
        co2_reduction_per_year_tons = co2_reduction_per_year_kg / 1000
        
        return AnnualImpactMetrics(
            flights_per_year=flights_per_year,
            fuel_savings_per_year_kg=fuel_savings_per_year_kg,
            fuel_savings_per_year_liters=fuel_savings_per_year_liters,
            cost_savings_per_year_usd=cost_savings_per_year_usd,
            co2_reduction_per_year_kg=co2_reduction_per_year_kg,
            co2_reduction_per_year_tons=co2_reduction_per_year_tons,
            fuel_price_per_kg=fuel_price_per_kg,  # $1.50/kg jet fuel (bulk airline price)
            scaling_factor=flights_per_year
        )
    
    def _enhance_weight_distribution(
        self,
        weight_dist: WeightDistribution,
        ulds: List[ULDInfo],
        flight_row: pd.Series
    ) -> WeightDistribution:
        """Enhance weight distribution with extended metrics"""
        # Calculate percentages
        total = weight_dist.total_weight
        weight_percentages_by_compartment = {
            k: (v / total * 100) if total > 0 else 0
            for k, v in weight_dist.by_compartment.items()
        }
        
        side_total = weight_dist.by_side.get('Left', 0) + weight_dist.by_side.get('Right', 0)
        weight_percentages_by_side = {
            'Left': (weight_dist.by_side.get('Left', 0) / side_total * 100) if side_total > 0 else 50,
            'Right': (weight_dist.by_side.get('Right', 0) / side_total * 100) if side_total > 0 else 50
        }
        
        # Balance ratio
        left_weight = weight_dist.by_side.get('Left', 0)
        right_weight = weight_dist.by_side.get('Right', 0)
        balance_ratio = left_weight / right_weight if right_weight > 0 else 1.0
        
        # Compartment utilization - check actual max weights per aircraft type
        # Default max weights (kg) - these vary by aircraft type
        # C3 max weight is typically lower than C1/C2
        max_compartment_weights = {'C1': 20000, 'C2': 20000, 'C3': 15000, 'C4': 15000}
        
        # Try to get actual max weights from aircraft data if available
        try:
            aircraft_type = str(flight_row.get('AircraftType', ''))
            aircraft_data_path = PROJECT_ROOT / "Inputfiles" / "Main.csv"
            if aircraft_data_path.exists():
                aircraft_df = pd.read_csv(aircraft_data_path)
                aircraft_row = aircraft_df[aircraft_df['ACType'] == aircraft_type]
                if len(aircraft_row) > 0:
                    row = aircraft_row.iloc[0]
                    max_compartment_weights = {
                        'C1': float(row.get('MaxWeightC1', 20000)),
                        'C2': float(row.get('MaxWeightC2', 20000)),
                        'C3': float(row.get('MaxWeightC3', 15000)),
                        'C4': float(row.get('MaxWeightC4', 15000))
                    }
        except Exception as e:
            print(f"Warning: Could not load max weights from Main.csv: {e}")
            pass  # Use defaults
        compartment_utilization = {
            k: v / max_compartment_weights.get(k, 20000)
            for k, v in weight_dist.by_compartment.items()
        }
        
        # Weight variance
        compartment_weights = list(weight_dist.by_compartment.values())
        weight_variance = np.var(compartment_weights) if len(compartment_weights) > 1 else 0
        
        # Create enhanced WeightDistribution - get base fields and add extended ones
        # Use model_dump(exclude=...) to avoid including extended fields if they already exist
        base_dict = weight_dist.model_dump(exclude={
            'weight_percentages_by_compartment',
            'weight_percentages_by_side',
            'balance_ratio',
            'compartment_utilization',
            'max_weight_per_compartment',
            'max_weight_per_position',
            'weight_variance',
            'center_of_gravity_x',
            'center_of_gravity_y'
        })
        
        # Add extended fields
        base_dict.update({
            'weight_percentages_by_compartment': weight_percentages_by_compartment,
            'weight_percentages_by_side': weight_percentages_by_side,
            'balance_ratio': balance_ratio,
            'compartment_utilization': compartment_utilization,
            'max_weight_per_compartment': max_compartment_weights,
            'weight_variance': weight_variance
        })
        
        return WeightDistribution(**base_dict)
    
    def _enhance_uld_utilization(
        self,
        uld_util: ULDUtilization,
        ulds: List[ULDInfo],
        cargo_items: List[CargoItem]
    ) -> ULDUtilization:
        """Enhance ULD utilization with extended metrics"""
        # Weight per ULD
        weight_per_uld = {uld.index: uld.weight for uld in ulds}
        
        # Items per ULD - ensure it's populated by counting cargo items per ULD
        items_per_uld = uld_util.items_per_uld.copy() if uld_util.items_per_uld else {}
        
        # If items_per_uld is empty, populate it from cargo_items
        if not items_per_uld or len(items_per_uld) == 0:
            for item in cargo_items:
                if item.uld_assignment is not None:
                    items_per_uld[item.uld_assignment] = items_per_uld.get(item.uld_assignment, 0) + 1
        
        # Ensure all ULDs have an entry (even if 0 items)
        for uld in ulds:
            if uld.index not in items_per_uld:
                items_per_uld[uld.index] = 0
        
        # Calculate statistics
        weights = [uld.weight for uld in ulds if uld.weight > 0]
        item_counts = list(items_per_uld.values())
        
        # Utilization by type
        utilization_by_type = {}
        max_weights_by_type = {'PMC': 4500, 'PAG': 4500, 'AAP': 4500, 'AKE': 1588, 'AAK': 1588}
        for uld_type, count in uld_util.ulds_by_type.items():
            type_ulds = [uld for uld in ulds if uld.type == uld_type]
            if type_ulds:
                avg_weight = np.mean([uld.weight for uld in type_ulds])
                max_weight = max_weights_by_type.get(uld_type, 3000)
                utilization_by_type[uld_type] = avg_weight / max_weight if max_weight > 0 else 0
        
        # Weight distribution ranges
        weight_ranges = {"0-500": 0, "500-1000": 0, "1000-2000": 0, "2000-3000": 0, "3000+": 0}
        for weight in weights:
            if weight < 500:
                weight_ranges["0-500"] += 1
            elif weight < 1000:
                weight_ranges["500-1000"] += 1
            elif weight < 2000:
                weight_ranges["1000-2000"] += 1
            elif weight < 3000:
                weight_ranges["2000-3000"] += 1
            else:
                weight_ranges["3000+"] += 1
        
        # Efficiency score
        utilization_rate = uld_util.utilization_rate
        
        # Get base fields excluding extended ones to avoid duplicates
        base_dict = uld_util.model_dump(exclude={
            'weight_per_uld',
            'volume_per_uld',
            'utilization_by_type',
            'empty_ulds',
            'average_uld_weight',
            'max_uld_weight',
            'min_uld_weight',
            'average_items_per_uld',
            'uld_weight_distribution',
            'ull_efficiency_score',
            'max_weight_by_type',
            'volume_utilization_by_type'
        })
        
        # Add extended fields
        base_dict.update({
            'weight_per_uld': weight_per_uld,
            'utilization_by_type': utilization_by_type,
            'empty_ulds': sum(1 for w in weights if w == 0),
            'average_uld_weight': float(np.mean(weights)) if weights else None,
            'max_uld_weight': float(max(weights)) if weights else None,
            'min_uld_weight': float(min(weights)) if weights else None,
            'average_items_per_uld': float(np.mean(item_counts)) if item_counts else None,
            'uld_weight_distribution': weight_ranges,
            'ull_efficiency_score': utilization_rate,
            'max_weight_by_type': max_weights_by_type
        })
        
        # Update utilization_rate in base_dict as well
        base_dict['utilization_rate'] = utilization_rate
        
        return ULDUtilization(**base_dict)
