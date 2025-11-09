# ULD (Unit Load Device) Data Analysis Report

## Executive Summary

This report provides a comprehensive understanding of the ULD data structure in the KLM Aviation Optimization project. The data consists of 525 complete flights with 5 CSV files per flight, containing detailed information about cargo, passengers, flight operations, and ULD specifications.

## Data Structure Overview

### Flight Data Organization
- **Total Flights**: 525 complete flights
- **Routes**: 7 active routes (AMSBLR, AMSDEL, AMSSIN, AMSIAH, AMSICN, AMSSFO, AMSLAX)
- **Aircraft Types**: Boeing 787-10 (33%), 777-200 (27%), 777-300ER (26%), 787-9 (14%)
- **Files per Flight**: 5 CSV files (BuildUpInformation, FlightInformation, LoadLocations, PaxInformation, PieceInformation)

## ULD Types and Specifications

### 1. AKE (Lower Deck Container)
- **Max Weight**: 1,587 kg
- **Volume**: 2.8 m³
- **Dimensions**: 162cm (H) × 156cm (L) × 153cm (W)
- **Special Features**: Has a cut (a=42, b=53, cut_a=1.26)
- **Usage**: Lower deck containers with special handling capabilities

### 2. PMC (Main Deck Container)
- **Max Weight**: 5,102 kg
- **Volume**: 12.5 m³
- **Dimensions**: 162cm (H) × 318cm (L) × 244cm (W)
- **Special Features**: No cut (a=0, b=0, cut_a=0)
- **Usage**: Main deck containers for larger cargo

### 3. PAG (Main Deck Container)
- **Max Weight**: 4,676 kg
- **Volume**: 11.4 m³
- **Dimensions**: 162cm (H) × 318cm (L) × 224cm (W)
- **Special Features**: No cut (a=0, b=0, cut_a=0)
- **Usage**: Alternative main deck container type

## CSV File Analysis

### 1. BuildUpInformation.csv
**Purpose**: Contains information about how cargo is built up into ULDs

**Key Columns**:
- `ULD`: ULD identifier (e.g., AKE96621KL)
- `AirWaybillNumber`: Unique cargo shipment identifier
- `NumberOfPiecesOnAWB`: Number of pieces in the air waybill
- `TotalWeightOnAWB`: Total weight of the shipment (kg)
- `TotalVolumeOnAWB`: Total volume of the shipment (cubic meters)
- `OriginStationCode`: Origin airport code
- `DestinationStationCode`: Destination airport code
- `ProductCode`: Cargo product type (R21, C01, etc.)
- `BuildupEventDateTime`: When the ULD was built up
- `BuildupLocation`: Physical location where buildup occurred
- `IsBuildUpInVG3`, `IsBuildUpInVG1`: Virtual grouping indicators

**Data Types**:
- Weight: Numeric (kg)
- Volume: Numeric (cubic meters)
- Dates: DateTime format
- Codes: String identifiers

### 2. LoadLocations.csv
**Purpose**: Contains detailed information about where each ULD is loaded on the aircraft

**Key Columns**:
- `SerialNumber`: ULD serial number
- `Weight`: Weight of cargo in ULD (kg)
- `DeadloadType`: Type of cargo (B=cargo, C=mail, etc.)
- `DeadloadSubType`: Subtype (T=transfer, Y=transit, F=forward, B=backward, G=general)
- `NumberOfItemsInUld`: Number of individual items in the ULD
- `LoadType`: Type of loading (ULD or BLK for bulk)
- `UldGrossWeight`: Total weight including ULD tare weight
- `UldTareWeight`: Weight of empty ULD (typically 57 kg for AKE)
- `Hold`: Aircraft hold location (AFT, FWD, BLK)
- `LoadLocation`: Specific position on aircraft (e.g., 43R, 12R)
- `Deck`: Aircraft deck (L=lower, U=upper)
- `SpecialHandlingCode`: Special handling requirements (COL, CRT, etc.)

**Data Types**:
- Weight: Numeric (kg)
- Locations: String codes
- Counts: Integer

### 3. PieceInformation.csv
**Purpose**: Contains detailed information about individual cargo pieces

**Key Columns**:
- `BookingAirWaybillNumber`: Air waybill number
- `BookingOriginStationCode`: Origin airport
- `BookingDestinationStationCode`: Destination airport
- `BookingTotalVolume`: Total volume (cubic meters)
- `BookingTotalWeight`: Total weight (kg)
- `BookingTotalPieceCount`: Number of pieces
- `BookingProductCode`: Product type code
- `BookingCommodityCode`: Commodity classification
- `BookingLinePieceVolume`: Volume per piece
- `BookingLinePieceWeight`: Weight per piece
- `BookingLinePieceHeight`: Height of piece (cm)
- `BookingLinePieceWidth`: Width of piece (cm)
- `BookingLinePieceLength`: Length of piece (cm)
- `BookingSegmentPiecesStackable`: Whether pieces can be stacked
- `BookingSegmentPiecesTurnable`: Whether pieces can be rotated

**Data Types**:
- Dimensions: Numeric (cm)
- Weight: Numeric (kg)
- Volume: Numeric (cubic meters)
- Boolean flags: True/False

### 4. FlightInformation.csv
**Purpose**: Contains aircraft and flight operational data

**Key Columns**:
- `AircraftType`: Aircraft type (772, 781, 789, 77W)
- `AircraftRegistration`: Aircraft registration (e.g., PHBQF)
- `ActualZeroFuelWeight`: Actual zero fuel weight (kg)
- `EstimatedZeroFuelWeight`: Estimated zero fuel weight (kg)
- `DryOperatingWeight`: Aircraft empty weight (kg)
- `MacZFW`: Mean Aerodynamic Chord for zero fuel weight
- `TakeOffFuel`: Fuel loaded for takeoff (kg)
- `TripFuel`: Fuel consumed during flight (kg)
- `CostIndex`: Flight cost index

**Data Types**:
- Weight: Numeric (kg)
- Fuel: Numeric (kg)
- Aircraft codes: String

### 5. PaxInformation.csv
**Purpose**: Contains passenger allocation information

**Key Columns**:
- `AircraftType`: Aircraft type
- `CenterOfGravityCabin`: Passenger cabin section (CABIN0A, CABIN0B, etc.)
- `PassengerCount`: Number of passengers in each section

**Data Types**:
- Passenger counts: Integer
- Cabin codes: String

## Data Quality and Statistics

### Cargo Statistics
- **Total Items**: 34,765 cargo items across all flights
- **Average Items per Flight**: 66.22 items
- **Weight per Flight**: Currently showing 0 (data processing issue)
- **Volume per Flight**: Currently showing 0 (data processing issue)

### ULD Usage Statistics
- **Average ULDs per Flight**: 39.5 ULDs
- **Range**: 18 to 164 ULDs per flight
- **Distribution**: Right-skewed (skewness: 3.582)

### Special Handling Codes
- **COL**: Cold chain cargo (temperature controlled)
- **CRT**: Critical cargo (time-sensitive)
- **Other codes**: Various special handling requirements

## Aircraft Load Locations

### Load Location System
The `LoadLocations.csv` file contains detailed aircraft-specific loading positions:
- **Format**: Position codes like "43R", "12L", "31P"
- **Hold Types**: AFT (aft), FWD (forward), BLK (bulk)
- **Deck Types**: L (lower), U (upper)
- **Aircraft Specific**: Different aircraft types have different available positions

### Proximity and Overlapping
The `Inputfiles/LoadLocations.csv` shows:
- **ProximityScore**: Distance/relationship between positions (1-4 scale)
- **Overlapping**: Which positions cannot be used simultaneously
- **Aircraft Specific**: Different proximity rules for different aircraft types

## Key Insights

1. **ULD Types**: Three main ULD types with different capacities and characteristics
2. **Data Completeness**: 100% complete data with all 5 required files per flight
3. **Special Handling**: COL and CRT items require special attention in optimization
4. **Aircraft Variety**: Four different aircraft types with different loading capabilities
5. **Route Diversity**: Seven different routes with varying cargo patterns

## Recommendations for Optimization

1. **ULD Selection**: Consider ULD type characteristics (cut vs no-cut) for optimization
2. **Special Handling**: Prioritize COL and CRT items in loading algorithms
3. **Aircraft Constraints**: Use proximity and overlapping rules for feasible loading
4. **Weight Distribution**: Consider ULD weight limits and aircraft balance
5. **Volume Optimization**: Maximize ULD utilization while respecting constraints

## Data Processing Notes

- Weight and volume data showing 0 values indicate potential data processing issues
- Special handling codes (COL, CRT) are critical for optimization constraints
- ULD serial numbers provide unique identification for tracking
- Load locations are aircraft-specific and must be validated against aircraft type
