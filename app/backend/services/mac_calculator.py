"""
Calculate MAC ZFW from weight distribution
Uses aircraft geometry constants
"""
import pandas as pd
from pathlib import Path
from typing import Dict, Optional

def calculate_mac_zfw_from_distribution(
    weight_by_compartment: Dict[str, float],
    aircraft_type: str,
    zfw: float,
    pax_weight: Optional[float] = None
) -> Optional[float]:
    """
    Calculate MAC ZFW from weight distribution using aircraft geometry
    
    Formula: MAC = (((C * (ZFW_index - K)) / ZFW) + reference_arm - lemac) / (mac_formula / 100)
    Where: ZFW_index = DOI + INDEX_PAX + sum(weight_compartment * delta_index_compartment)
    
    Args:
        weight_by_compartment: Dict with C1, C2, C3, C4 weights
        aircraft_type: Aircraft type code (e.g., '781', '789', '772', '77W')
        zfw: Zero Fuel Weight
        pax_weight: Passenger weight (estimated if None)
    
    Returns:
        MAC ZFW percentage or None if calculation fails
    """
    try:
        # Try to load aircraft data - try Main.csv first (it has aircraft geometry)
        aircraft_data_path = Path(__file__).parent.parent.parent.parent / "Inputfiles" / "Main.csv"
        
        if not aircraft_data_path.exists():
            # Try AircraftInformation.csv
            aircraft_data_path = Path(__file__).parent.parent.parent.parent / "Inputfiles" / "AircraftInformation.csv"
        
        if not aircraft_data_path.exists():
            # Try alternative path
            aircraft_data_path = Path(__file__).parent.parent.parent.parent / "Main.csv"
        
        if not aircraft_data_path.exists():
            return None
        
        # Load aircraft data
        aircraft_df = pd.read_csv(aircraft_data_path)
        aircraft_row = aircraft_df[aircraft_df['ACType'] == str(aircraft_type)]
        
        if len(aircraft_row) == 0:
            return None
        
        aircraft_row = aircraft_row.iloc[0]
        
        # Get aircraft constants
        C = float(aircraft_row.get('C', 0))
        K = float(aircraft_row.get('K', 0))
        reference_arm = float(aircraft_row.get('ReferenceArm', 0))
        lemac = float(aircraft_row.get('LEMAC', 0))
        mac_formula = float(aircraft_row.get('MACFormula', 100))
        DOI = float(aircraft_row.get('DOIIndex', aircraft_row.get('DOI', 0)))
        
        # Delta index values for compartments
        delta_C1 = float(aircraft_row.get('DeltaIndexCargoC1', 0))
        delta_C2 = float(aircraft_row.get('DeltaIndexCargoC2', 0))
        delta_C3 = float(aircraft_row.get('DeltaIndexCargoC3', 0))
        delta_C4 = float(aircraft_row.get('DeltaIndexCargoC4', 0))
        
        # Calculate INDEX_PAX (passenger index)
        if pax_weight is None:
            # Estimate: typical 787 has ~290 passengers * 84 kg = ~24,360 kg
            # Estimate INDEX_PAX based on aircraft type
            pax_weight = 24360 if '787' in str(aircraft_type) else 21000
        
        # Get passenger delta indices (estimate if not available)
        delta_pax_0A = float(aircraft_row.get('DeltaIndexPax0A', 0))
        delta_pax_0B = float(aircraft_row.get('DeltaIndexPax0B', 0))
        delta_pax_0C = float(aircraft_row.get('DeltaIndexPax0C', 0))
        delta_pax_0D = float(aircraft_row.get('DeltaIndexPax0D', 0))
        delta_pax_0E = float(aircraft_row.get('DeltaIndexPax0E', 0))
        delta_pax_0F = float(aircraft_row.get('DeltaIndexPax0F', 0))
        delta_pax_0G = float(aircraft_row.get('DeltaIndexPax0G', 0))
        
        # Estimate INDEX_PAX from passenger distribution
        # Use average delta if individual values not meaningful
        if all(v == 0 for v in [delta_pax_0A, delta_pax_0B, delta_pax_0C, delta_pax_0D, delta_pax_0E, delta_pax_0F, delta_pax_0G]):
            # Fallback: use a default estimate
            INDEX_PAX = pax_weight * 0.1  # Rough estimate
        else:
            # Use actual passenger delta indices
            pax_distribution = [delta_pax_0A, delta_pax_0B, delta_pax_0C, delta_pax_0D, delta_pax_0E, delta_pax_0F, delta_pax_0G]
            avg_delta_pax = sum(pax_distribution) / len([d for d in pax_distribution if d != 0]) if any(pax_distribution) else 0.1
            INDEX_PAX = pax_weight * avg_delta_pax
        
        # Calculate ZFW_index from weight distribution
        weight_C1 = weight_by_compartment.get('C1', 0)
        weight_C2 = weight_by_compartment.get('C2', 0)
        weight_C3 = weight_by_compartment.get('C3', 0)
        weight_C4 = weight_by_compartment.get('C4', 0)
        
        ZFW_index = (
            DOI +
            INDEX_PAX +
            (weight_C1 * delta_C1) +
            (weight_C2 * delta_C2) +
            (weight_C3 * delta_C3) +
            (weight_C4 * delta_C4)
        )
        
        # Calculate MAC ZFW
        # Formula: MAC = (((C * (ZFW_index - K)) / ZFW) + reference_arm - lemac) / (mac_formula / 100)
        if zfw > 0 and mac_formula > 0:
            # First calculate the arm position
            arm_position = ((C * (ZFW_index - K)) / zfw) + reference_arm
            
            # Then calculate MAC percentage
            mac_zfw = (arm_position - lemac) / (mac_formula / 100)
            
            # MAC should typically be between 0-50%, negative or very high values suggest calculation error
            if mac_zfw < 0 or mac_zfw > 50:
                # Try alternative calculation - maybe need to use OEW instead of ZFW
                return None
            
            return mac_zfw
        
        return None
    
    except Exception as e:
        print(f"Error calculating MAC ZFW: {e}")
        import traceback
        traceback.print_exc()
        return None

