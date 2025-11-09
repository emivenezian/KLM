#!/usr/bin/env python3
"""
Debug script to analyze why a specific flight is infeasible
"""

import sys
import os
import traceback
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

# Import the model components
from Classes import Cargo, ULD, Item, Position
from Model import solve_1D_BPP_WB

def debug_infeasible_flight():
    """Debug the infeasible flight KL835 AMSSIN 28 JAN 24"""
    
    print("🔍 DEBUGGING INFEASIBLE FLIGHT: KL835 AMSSIN 28 JAN 24")
    print("=" * 60)
    
    # Flight details from General_Information.txt
    flight_info = {
        'flight_number': 'KL835',
        'aircraft_type': '772',
        'departure': 'AMS',
        'arrival': 'SIN',
        'date': '28 JAN 24',
        'zfw': 175824.1,
        'tow': 264448.1,
        'lw': 182342.1,
        'oew': 148261.0,
        'fuel': 88624,
        'trip_fuel': 82106,
        'cargo_ulds': 7,
        'bax_ulds': 9,
        'bup_ulds': 0,
        't_ulds': 1,
        'total_pax': 148
    }
    
    print(f"📋 Flight Details:")
    print(f"   Flight: {flight_info['flight_number']} {flight_info['departure']}-{flight_info['arrival']}")
    print(f"   Aircraft: {flight_info['aircraft_type']}")
    print(f"   Date: {flight_info['date']}")
    print(f"   ZFW: {flight_info['zfw']} kg")
    print(f"   TOW: {flight_info['tow']} kg")
    print(f"   Total PAX: {flight_info['total_pax']}")
    print()
    
    # Load the flight data
    data_path = Path("Data/Flights AMSSIN JAN 2024/Flight KL835 AMSSIN 28 JAN 24")
    
    if not data_path.exists():
        print(f"❌ ERROR: Data path not found: {data_path}")
        return
    
    print(f"📁 Data Path: {data_path}")
    print()
    
    try:
        # Load cargo data
        print("🔄 Loading cargo data...")
        cargo = Cargo(data_path)
        print(f"✅ Cargo loaded successfully")
        print(f"   Items: {len(cargo.items)}")
        print(f"   ULDs: {len(cargo.uld)}")
        print()
        
        # Check for items that don't fit
        print("🔍 Checking item-ULD compatibility...")
        incompatible_items = []
        for item in cargo.items:
            fits_any_uld = False
            for uld in cargo.uld:
                if (item.length <= uld.length and 
                    item.width <= uld.width and 
                    item.height <= uld.height):
                    fits_any_uld = True
                    break
            if not fits_any_uld:
                incompatible_items.append(item)
        
        if incompatible_items:
            print(f"⚠️  Found {len(incompatible_items)} items that don't fit any ULD:")
            for item in incompatible_items:
                print(f"   Item {item.serialnumber}: {item.length}x{item.width}x{item.height} cm")
        else:
            print("✅ All items fit in available ULDs")
        print()
        
        # Try to solve the model
        print("🚀 Attempting to solve the model...")
        try:
            result = solve_1D_BPP_WB(cargo)
            print("✅ Model solved successfully!")
            print(f"   Objective value: {result.getObjectiveValue()}")
        except Exception as e:
            print(f"❌ Model failed with error: {str(e)}")
            print(f"   Error type: {type(e).__name__}")
            print()
            print("🔍 Full error traceback:")
            traceback.print_exc()
            
            # Try to identify the specific issue
            print()
            print("🔍 Analyzing potential causes:")
            
            # Check if it's a dimension issue
            if incompatible_items:
                print(f"   • {len(incompatible_items)} items don't fit any ULD dimensions")
                print("   • This is likely the main cause of infeasibility")
            
            # Check weight constraints
            total_item_weight = sum(item.weight for item in cargo.items)
            total_uld_capacity = sum(uld.max_weight for uld in cargo.uld)
            print(f"   • Total item weight: {total_item_weight:.1f} kg")
            print(f"   • Total ULD capacity: {total_uld_capacity:.1f} kg")
            if total_item_weight > total_uld_capacity:
                print("   • Weight exceeds ULD capacity - another cause of infeasibility")
            else:
                print("   • Weight within ULD capacity")
            
            # Check passenger constraints
            print(f"   • Passenger count: {flight_info['total_pax']}")
            print(f"   • Aircraft type: {flight_info['aircraft_type']}")
            
    except Exception as e:
        print(f"❌ Failed to load cargo data: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    debug_infeasible_flight()

