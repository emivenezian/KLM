"""
API endpoints for optimization operations
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.schemas import (
    OptimizationRequest,
    OptimizationResult,
    SyntheticDataRequest,
    VisualizationData
)
from services.model_executor import ModelExecutor
from services.visualization_data import VisualizationService
from services.synthetic_data import generate_synthetic_flight
from utils.path_utils import list_available_flights, list_available_flights_with_item_count
import json

router = APIRouter()
model_executor = ModelExecutor()
viz_service = VisualizationService()

@router.post("/run", response_model=OptimizationResult)
async def run_optimization(request: OptimizationRequest):
    """
    Run optimization model for a flight
    
    Args:
        request: OptimizationRequest with flight path and model type
    
    Returns:
        OptimizationResult with results
    """
    try:
        result = model_executor.execute_model(
            flight_path=request.flight_path,
            model_type=request.model_type,
            restricted_locations=request.restricted_locations
        )
        
        if not result.success:
            raise HTTPException(status_code=400, detail=result.error_message)
        
        return result
    
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=f"Flight data not found: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error running optimization: {str(e)}")

@router.get("/flights", response_model=List[str])
async def list_flights():
    """
    List all available flights (sorted by item count, smallest first)
    
    Returns:
        List of flight folder paths, sorted by item count ascending
    """
    try:
        flights_with_counts = list_available_flights_with_item_count()
        # Return just the flight paths (sorted by item count)
        flights = [flight_path for flight_path, _ in flights_with_counts]
        return flights
    except Exception as e:
        # Fallback to simple list if there's an error
        try:
            flights = list_available_flights()
            return flights
        except:
            raise HTTPException(status_code=500, detail=f"Error listing flights: {str(e)}")

@router.get("/flights/with-counts")
async def list_flights_with_counts():
    """
    List all available flights with their item counts and pre-computed results status
    
    Returns:
        List of dicts with flight_path, item_count, and has_precomputed_results, sorted by item_count
    """
    try:
        from services.results_loader import load_precomputed_results
        
        flights_with_counts = list_available_flights_with_item_count()
        result = []
        
        for flight_path, count in flights_with_counts:
            # Check if this flight has pre-computed results
            has_results = load_precomputed_results(flight_path, "delgado_venezian") is not None
            result.append({
                "flight_path": flight_path,
                "item_count": count,
                "has_precomputed_results": has_results
            })
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing flights: {str(e)}")

@router.post("/synthetic/generate")
async def generate_synthetic_flight_data(request: SyntheticDataRequest):
    """
    Generate synthetic flight data for testing
    
    Args:
        request: SyntheticDataRequest with parameters
    
    Returns:
        Dictionary with paths to generated files
    """
    try:
        files = generate_synthetic_flight(
            num_items=request.num_items,
            num_ulds=request.num_ulds,
            weight_range=request.weight_range,
            include_crt=request.include_crt,
            include_col=request.include_col,
            include_dangerous=request.include_dangerous,
            flight_number=request.flight_number,
            departure_airport=request.departure_airport,
            arrival_airport=request.arrival_airport
        )
        
        # Convert Path objects to strings
        return {
            'success': True,
            'files': {k: str(v) for k, v in files.items()},
            'message': f'Synthetic flight data generated: {request.flight_number}'
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating synthetic data: {str(e)}")

@router.post("/visualization/prepare", response_model=VisualizationData)
async def prepare_visualization(result: OptimizationResult):
    """
    Prepare visualization data from optimization result
    
    Args:
        result: OptimizationResult
    
    Returns:
        VisualizationData ready for frontend
    """
    try:
        viz_data = viz_service.prepare_visualization_data(result)
        return viz_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error preparing visualization: {str(e)}")

