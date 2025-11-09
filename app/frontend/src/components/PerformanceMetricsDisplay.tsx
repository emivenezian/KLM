import React from 'react';
import { PerformanceMetrics } from '../services/api';
import './PerformanceMetricsDisplay.css';

interface PerformanceMetricsDisplayProps {
  metrics: PerformanceMetrics;
}

const PerformanceMetricsDisplay: React.FC<PerformanceMetricsDisplayProps> = ({ metrics }) => {
  return (
    <div className="performance-metrics-container">
      <div className="card highlight">
        <h2>Performance & Savings Metrics</h2>
        <div className="metrics-grid-large">
          {metrics.fuel_savings_kg !== undefined && metrics.fuel_savings_kg !== null && (
            <div className="metric-item-large">
              <label>Fuel Savings</label>
              <div className="metric-value-large">{metrics.fuel_savings_kg.toFixed(1)} kg</div>
              {metrics.fuel_savings_percent && (
                <div className="metric-subtext">({metrics.fuel_savings_percent.toFixed(2)}%)</div>
              )}
            </div>
          )}
          {metrics.cost_savings_usd !== undefined && metrics.cost_savings_usd !== null && (
            <div className="metric-item-large">
              <label>Cost Savings</label>
              <div className="metric-value-large">${metrics.cost_savings_usd.toFixed(2)}</div>
            </div>
          )}
          {metrics.co2_emissions_saved_kg !== undefined && metrics.co2_emissions_saved_kg !== null && (
            <div className="metric-item-large">
              <label>CO₂ Emissions Saved</label>
              <div className="metric-value-large">{metrics.co2_emissions_saved_kg.toFixed(1)} kg</div>
            </div>
          )}
          {metrics.load_factor !== undefined && metrics.load_factor !== null && (
            <div className="metric-item-large">
              <label>Load Factor</label>
              <div className="metric-value-large">{(metrics.load_factor * 100).toFixed(1)}%</div>
            </div>
          )}
          {metrics.efficiency_score !== undefined && metrics.efficiency_score !== null && (
            <div className="metric-item-large">
              <label>Efficiency Score</label>
              <div className="metric-value-large">{(metrics.efficiency_score * 100).toFixed(1)}%</div>
            </div>
          )}
          {metrics.baseline_fuel_kg !== undefined && metrics.baseline_fuel_kg !== null && (
            <div className="metric-item-large">
              <label>Baseline Fuel</label>
              <div className="metric-value-large">{metrics.baseline_fuel_kg.toFixed(1)} kg</div>
            </div>
          )}
          {metrics.optimized_fuel_kg !== undefined && metrics.optimized_fuel_kg !== null && (
            <div className="metric-item-large">
              <label>Optimized Fuel</label>
              <div className="metric-value-large">{metrics.optimized_fuel_kg.toFixed(1)} kg</div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default PerformanceMetricsDisplay;

