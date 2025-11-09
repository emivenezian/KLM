"""
Service to prepare data for frontend visualizations
"""
from typing import Dict, Any, List
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.schemas import OptimizationResult, VisualizationData

class VisualizationService:
    """Prepares visualization data from optimization results"""
    
    @staticmethod
    def prepare_visualization_data(result: OptimizationResult) -> VisualizationData:
        """
        Convert optimization result to visualization-ready data
        
        Args:
            result: OptimizationResult from model execution
        
        Returns:
            VisualizationData ready for frontend charts
        """
        weight_dist = result.weight_distribution
        uld_util = result.uld_utilization
        
        # Prepare items per ULD chart data
        items_per_uld_chart = [
            {
                'uld_index': idx,
                'uld_serial': uld.serialnumber,
                'item_count': uld_util.items_per_uld.get(idx, 0),
                'weight': uld.weight
            }
            for idx, uld in enumerate(result.ulds)
        ]
        
        # Prepare weight per ULD chart data
        weight_per_uld_chart = [
            {
                'uld_index': idx,
                'uld_serial': uld.serialnumber,
                'uld_type': uld.type,
                'weight': uld.weight,
                'position': uld.position or 'Unassigned',
                'compartment': uld.compartment or 'Unknown'
            }
            for idx, uld in enumerate(result.ulds)
        ]
        
        # Prepare position map for 3D visualization
        position_map = []
        for idx, uld in enumerate(result.ulds):
            if uld.position:
                position_map.append({
                    'uld_index': idx,
                    'uld_serial': uld.serialnumber,
                    'position': uld.position,
                    'compartment': uld.compartment or 'Unknown',
                    'weight': uld.weight,
                    'x': 0,  # Will be calculated based on position
                    'y': 0,  # Will be calculated based on position
                    'z': 0   # Will be calculated based on position
                })
        
        return VisualizationData(
            weight_by_compartment=weight_dist.by_compartment,
            weight_by_side=weight_dist.by_side,
            weight_by_position=weight_dist.by_position,
            uld_type_distribution=uld_util.ulds_by_type,
            items_per_uld_chart=items_per_uld_chart,
            weight_per_uld_chart=weight_per_uld_chart,
            position_map=position_map
        )

