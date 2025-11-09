"""
Pydantic schemas for API request/response models
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class FlightInfo(BaseModel):
    """Flight information"""
    flight_number: str
    departure_airport: str
    arrival_airport: str
    date: str
    aircraft_type: Optional[str] = None
    aircraft_registration: Optional[str] = None

class ULDInfo(BaseModel):
    """ULD information"""
    index: int
    type: str
    serialnumber: str
    weight: float
    max_weight: Optional[float] = None
    position: Optional[str] = None
    compartment: Optional[str] = None

class CargoItem(BaseModel):
    """Cargo item information"""
    index: int
    serialnumber: str
    number_of_pieces: int
    weight: float
    volume: Optional[float] = None
    CRT: bool = False
    COL: bool = False
    dangerous: bool = False
    commodity: Optional[str] = None
    uld_assignment: Optional[int] = None

class WeightDistribution(BaseModel):
    """Weight distribution metrics"""
    by_compartment: Dict[str, float]  # C1, C2, C3, C4
    by_side: Dict[str, float]  # Left, Right
    by_position: Dict[str, float]  # Position codes
    total_weight: float
    zfw: float
    mac_zfw: float
    # Extended metrics
    weight_percentages_by_compartment: Dict[str, float] = {}  # Percentage of total weight per compartment
    weight_percentages_by_side: Dict[str, float] = {}  # Percentage Left vs Right
    balance_ratio: Optional[float] = None  # Left/Right balance ratio (1.0 = perfect balance)
    compartment_utilization: Dict[str, float] = {}  # Actual weight / max weight per compartment
    position_utilization: Dict[str, float] = {}  # Actual weight / max weight per position
    max_weight_per_compartment: Dict[str, float] = {}  # Maximum allowed weight per compartment
    max_weight_per_position: Dict[str, float] = {}  # Maximum allowed weight per position
    weight_variance: Optional[float] = None  # Variance in weight distribution
    center_of_gravity_x: Optional[float] = None  # CG position (if available)
    center_of_gravity_y: Optional[float] = None  # CG position (if available)

class ULDUtilization(BaseModel):
    """ULD utilization metrics"""
    total_ulds: int
    ulds_by_type: Dict[str, int]  # ULD type -> count
    ulds_by_side: Dict[str, int]  # Left, Right
    utilization_rate: float  # Average weight / max weight
    items_per_uld: Dict[int, int]  # ULD index -> item count
    # Extended metrics
    weight_per_uld: Dict[int, float] = {}  # ULD index -> weight
    volume_per_uld: Dict[int, float] = {}  # ULD index -> volume
    utilization_by_type: Dict[str, float] = {}  # Average utilization per ULD type
    empty_ulds: int = 0  # Number of empty/unused ULDs
    average_uld_weight: Optional[float] = None
    max_uld_weight: Optional[float] = None
    min_uld_weight: Optional[float] = None
    average_items_per_uld: Optional[float] = None
    uld_weight_distribution: Dict[str, int] = {}  # Weight ranges -> count (e.g., "0-500", "500-1000")
    ull_efficiency_score: Optional[float] = None  # Overall ULD loading efficiency (0-1)
    max_weight_by_type: Dict[str, float] = {}  # Max weight capacity per ULD type
    volume_utilization_by_type: Dict[str, float] = {}  # Volume utilization per type

class OptimizationRequest(BaseModel):
    """Request to run optimization"""
    flight_path: str  # Path to flight data folder
    model_type: str = "delgado_venezian"  # delgado_venezian, baseline, optimized_actual, bax_fixed
    restricted_locations: List[str] = []
    synthetic_data: Optional[Dict[str, Any]] = None  # If using synthetic data

class CargoMetrics(BaseModel):
    """Cargo item metrics"""
    total_items: int
    items_by_type: Dict[str, int] = {}  # Commodity type -> count
    items_by_weight_range: Dict[str, int] = {}  # Weight ranges -> count
    items_without_uld: int = 0  # Items not assigned to ULD
    average_item_weight: Optional[float] = None
    max_item_weight: Optional[float] = None
    min_item_weight: Optional[float] = None
    total_crt_items: int = 0  # Temperature-controlled items
    total_col_items: int = 0  # Col items
    total_dangerous_items: int = 0
    total_volume: Optional[float] = None
    weight_distribution_by_commodity: Dict[str, float] = {}  # Commodity -> total weight
    largest_items: List[Dict[str, Any]] = []  # Top N heaviest items

class PerformanceMetrics(BaseModel):
    """Performance and savings metrics"""
    fuel_savings_kg: Optional[float] = None
    fuel_savings_percent: Optional[float] = None
    cost_savings_usd: Optional[float] = None  # Estimated cost savings
    co2_emissions_saved_kg: Optional[float] = None  # CO2 emissions avoided
    fuel_consumption_liters: Optional[float] = None  # Total fuel consumption
    baseline_fuel_kg: Optional[float] = None  # Baseline fuel consumption
    optimized_fuel_kg: Optional[float] = None  # Optimized fuel consumption
    load_factor: Optional[float] = None  # Cargo load factor (weight/volume)
    efficiency_score: Optional[float] = None  # Overall loading efficiency (0-1)

class OptimizationMetrics(BaseModel):
    """Optimization solver metrics"""
    runtime_seconds: Optional[float] = None
    solver_status: Optional[str] = None  # Optimal, Feasible, Infeasible, etc.
    objective_value: Optional[float] = None
    gap_percent: Optional[float] = None  # MIP gap percentage
    number_of_variables: Optional[int] = None
    number_of_constraints: Optional[int] = None
    number_of_iterations: Optional[int] = None
    number_of_nodes: Optional[int] = None  # For branch-and-bound
    solution_time: Optional[float] = None  # Pure solution time (excl. setup)

class SafetyMetrics(BaseModel):
    """Safety and compliance metrics"""
    weight_limits_compliance: Dict[str, bool] = {}  # Compartment/position -> compliant
    balance_limits_compliance: Dict[str, bool] = {}  # Side balance -> compliant
    cg_limits_compliance: Optional[bool] = None  # Center of gravity within limits
    restricted_locations_used: List[str] = []  # Restricted positions used
    temperature_constraints_violated: int = 0
    separation_constraints_violated: int = 0
    max_weight_exceeded_positions: List[str] = []  # Positions exceeding max weight
    safety_score: Optional[float] = None  # Overall safety score (0-1)

class KLMActualMetrics(BaseModel):
    """KLM Actual loading metrics (what KLM actually loaded)"""
    actual_mac_zfw: Optional[float] = None
    actual_weight_by_compartment: Dict[str, float] = {}
    actual_weight_by_side: Dict[str, float] = {}
    actual_total_weight: Optional[float] = None
    actual_total_ulds: Optional[int] = None
    trip_fuel: Optional[float] = None  # Trip fuel consumption (kg)

class AnnualImpactMetrics(BaseModel):
    """Annual impact projections based on per-flight savings"""
    flights_per_year: Optional[int] = None  # Number of intercontinental flights per year
    fuel_savings_per_year_kg: Optional[float] = None  # Total fuel savings per year
    fuel_savings_per_year_liters: Optional[float] = None  # Total fuel savings in liters
    cost_savings_per_year_usd: Optional[float] = None  # Total cost savings per year
    co2_reduction_per_year_kg: Optional[float] = None  # Total CO2 reduction per year
    co2_reduction_per_year_tons: Optional[float] = None  # Total CO2 reduction in metric tons
    fuel_price_per_kg: Optional[float] = None  # Fuel price used for calculation ($/kg)
    scaling_factor: Optional[float] = None  # How many times to multiply per-flight savings

class ComparisonMetrics(BaseModel):
    """Comparison with KLM actual loading"""
    klm_actual: Optional[KLMActualMetrics] = None
    weight_difference_by_compartment: Dict[str, float] = {}  # Optimized - KLM Actual
    weight_difference_by_side: Dict[str, float] = {}  # Optimized - KLM Actual
    uld_count_difference: Optional[int] = None  # Optimized - KLM Actual ULD count
    fuel_savings_vs_klm_actual_kg: Optional[float] = None
    fuel_savings_vs_klm_actual_percent: Optional[float] = None
    cost_savings_vs_klm_actual_usd: Optional[float] = None
    co2_savings_vs_klm_actual_kg: Optional[float] = None
    mac_difference: Optional[float] = None  # MAC optimized - MAC KLM actual
    improvement_percentage: Optional[float] = None  # Overall improvement %
    annual_impact: Optional[AnnualImpactMetrics] = None  # Annual impact projections

class OptimizationResult(BaseModel):
    """Optimization result with comprehensive metrics"""
    success: bool
    flight_info: FlightInfo
    weight_distribution: WeightDistribution
    uld_utilization: ULDUtilization
    cargo_items: List[CargoItem]
    ulds: List[ULDInfo]
    cargo_metrics: Optional[CargoMetrics] = None
    performance_metrics: Optional[PerformanceMetrics] = None
    optimization_metrics: Optional[OptimizationMetrics] = None
    safety_metrics: Optional[SafetyMetrics] = None
    comparison_metrics: Optional[ComparisonMetrics] = None
    # Legacy fields for backward compatibility
    fuel_savings_kg: Optional[float] = None
    fuel_savings_percent: Optional[float] = None
    runtime_seconds: Optional[float] = None
    error_message: Optional[str] = None
    warnings: List[str] = []

class SyntheticDataRequest(BaseModel):
    """Request to generate synthetic flight data"""
    num_items: int = Field(ge=1, le=200, default=50)
    num_ulds: int = Field(ge=1, le=50, default=10)
    weight_range: tuple = (100, 1000)
    include_crt: bool = True
    include_col: bool = True
    include_dangerous: bool = False
    flight_number: str = "SYN001"
    departure_airport: str = "AMS"
    arrival_airport: str = "SIN"

class VisualizationData(BaseModel):
    """Data structure for frontend visualizations"""
    weight_by_compartment: Dict[str, float]
    weight_by_side: Dict[str, float]
    weight_by_position: Dict[str, float]
    uld_type_distribution: Dict[str, int]
    items_per_uld_chart: List[Dict[str, Any]]
    weight_per_uld_chart: List[Dict[str, Any]]
    position_map: List[Dict[str, Any]]  # For 3D visualization

