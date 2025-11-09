import axios from 'axios';
import { API_ENDPOINTS } from '../config';

// API client
const api = axios.create({
  baseURL: API_ENDPOINTS.optimization.run.split('/api')[0],
  headers: {
    'Content-Type': 'application/json',
  },
});

// Types (matching backend schemas)
export interface FlightInfo {
  flight_number: string;
  departure_airport: string;
  arrival_airport: string;
  date: string;
  aircraft_type?: string;
  aircraft_registration?: string;
}


export interface ULDUtilization {
  total_ulds: number;
  ulds_by_type: { [key: string]: number };
  ulds_by_side: { [key: string]: number };
  utilization_rate: number;
  items_per_uld: { [key: number]: number };
  // Extended metrics
  weight_per_uld?: { [key: number]: number };
  volume_per_uld?: { [key: number]: number };
  utilization_by_type?: { [key: string]: number };
  empty_ulds?: number;
  average_uld_weight?: number;
  max_uld_weight?: number;
  min_uld_weight?: number;
  average_items_per_uld?: number;
  uld_weight_distribution?: { [key: string]: number };
  ull_efficiency_score?: number;
  max_weight_by_type?: { [key: string]: number };
  volume_utilization_by_type?: { [key: string]: number };
}

export interface WeightDistribution {
  by_compartment: { [key: string]: number };
  by_side: { [key: string]: number };
  by_position: { [key: string]: number };
  total_weight: number;
  zfw: number;
  mac_zfw: number;
  // Extended metrics
  weight_percentages_by_compartment?: { [key: string]: number };
  weight_percentages_by_side?: { [key: string]: number };
  balance_ratio?: number;
  compartment_utilization?: { [key: string]: number };
  position_utilization?: { [key: string]: number };
  max_weight_per_compartment?: { [key: string]: number };
  max_weight_per_position?: { [key: string]: number };
  weight_variance?: number;
  center_of_gravity_x?: number;
  center_of_gravity_y?: number;
}

export interface CargoMetrics {
  total_items: number;
  items_by_type?: { [key: string]: number };
  items_by_weight_range?: { [key: string]: number };
  items_without_uld?: number;
  average_item_weight?: number;
  max_item_weight?: number;
  min_item_weight?: number;
  total_crt_items?: number;
  total_col_items?: number;
  total_dangerous_items?: number;
  total_volume?: number;
  weight_distribution_by_commodity?: { [key: string]: number };
  largest_items?: Array<{ index: number; serialnumber: string; weight: number; commodity?: string }>;
}

export interface PerformanceMetrics {
  fuel_savings_kg?: number;
  fuel_savings_percent?: number;
  cost_savings_usd?: number;
  co2_emissions_saved_kg?: number;
  fuel_consumption_liters?: number;
  baseline_fuel_kg?: number;
  optimized_fuel_kg?: number;
  load_factor?: number;
  efficiency_score?: number;
}

export interface OptimizationMetrics {
  runtime_seconds?: number;
  solver_status?: string;
  objective_value?: number;
  gap_percent?: number;
  number_of_variables?: number;
  number_of_constraints?: number;
  number_of_iterations?: number;
  number_of_nodes?: number;
  solution_time?: number;
}

export interface SafetyMetrics {
  weight_limits_compliance?: { [key: string]: boolean };
  balance_limits_compliance?: { [key: string]: boolean };
  cg_limits_compliance?: boolean;
  restricted_locations_used?: string[];
  temperature_constraints_violated?: number;
  separation_constraints_violated?: number;
  max_weight_exceeded_positions?: string[];
  safety_score?: number;
}

export interface KLMActualMetrics {
  actual_mac_zfw?: number;
  actual_weight_by_compartment?: { [key: string]: number };
  actual_weight_by_side?: { [key: string]: number };
  actual_total_weight?: number;
  actual_total_ulds?: number;
  trip_fuel?: number;
}

export interface AnnualImpactMetrics {
  flights_per_year?: number;
  fuel_savings_per_year_kg?: number;
  fuel_savings_per_year_liters?: number;
  cost_savings_per_year_usd?: number;
  co2_reduction_per_year_kg?: number;
  co2_reduction_per_year_tons?: number;
  fuel_price_per_kg?: number;
  scaling_factor?: number;
}

export interface ComparisonMetrics {
  klm_actual?: KLMActualMetrics;
  weight_difference_by_compartment?: { [key: string]: number };
  weight_difference_by_side?: { [key: string]: number };
  uld_count_difference?: number;
  fuel_savings_vs_klm_actual_kg?: number;
  fuel_savings_vs_klm_actual_percent?: number;
  cost_savings_vs_klm_actual_usd?: number;
  co2_savings_vs_klm_actual_kg?: number;
  mac_difference?: number;
  improvement_percentage?: number;
  annual_impact?: AnnualImpactMetrics;
}

export interface OptimizationResult {
  success: boolean;
  flight_info: FlightInfo;
  weight_distribution: WeightDistribution;
  uld_utilization: ULDUtilization;
  cargo_items: any[];
  ulds: any[];
  cargo_metrics?: CargoMetrics;
  performance_metrics?: PerformanceMetrics;
  optimization_metrics?: OptimizationMetrics;
  safety_metrics?: SafetyMetrics;
  comparison_metrics?: ComparisonMetrics;
  fuel_savings_kg?: number;
  fuel_savings_percent?: number;
  runtime_seconds?: number;
  error_message?: string;
  warnings: string[];
}

export interface OptimizationRequest {
  flight_path: string;
  model_type?: string;
  restricted_locations?: string[];
}

// API functions
export const optimizationAPI = {
  run: async (request: OptimizationRequest): Promise<OptimizationResult> => {
    const response = await api.post(API_ENDPOINTS.optimization.run, request);
    return response.data;
  },

  listFlights: async (): Promise<string[]> => {
    const response = await api.get(API_ENDPOINTS.optimization.flights);
    return response.data;
  },

  generateSynthetic: async (params: any) => {
    const response = await api.post(API_ENDPOINTS.optimization.synthetic, params);
    return response.data;
  },
};

export const exportAPI = {
  toSheets: async (result: OptimizationResult, spreadsheetId: string, worksheetName?: string) => {
    const response = await api.post(API_ENDPOINTS.export.sheets, {
      result,
      spreadsheet_id: spreadsheetId,
      worksheet_name: worksheetName || 'Optimization Results',
    });
    return response.data;
  },

  sheetsStatus: async () => {
    const response = await api.get(API_ENDPOINTS.export.sheetsStatus);
    return response.data;
  },
};

