import React from 'react';
import { OptimizationResult } from '../services/api';
import './FlightSummary.css';

interface FlightSummaryProps {
  result: OptimizationResult;
}

const FlightSummary: React.FC<FlightSummaryProps> = ({ result }) => {
  const { flight_info, weight_distribution, fuel_savings_kg, runtime_seconds, warnings } = result;
  
  // Check if using real model or fallback
  const isRealModel = warnings.length === 0 || warnings.some(w => w.includes('REAL-TIME OPTIMIZATION'));
  const isFallback = warnings.some(w => w.includes('fallback') || w.includes('FAILED'));

  return (
    <div className="card">
      <h2>Flight Summary</h2>
      {isRealModel && (
        <div className="success" style={{ marginBottom: '16px' }}>
          ✅ <strong>Real-time optimization completed!</strong> Results from actual Gurobi model execution.
        </div>
      )}
      {isFallback && (
        <div className="error" style={{ marginBottom: '16px' }}>
          ⚠️ <strong>Using CSV input data fallback.</strong> Real model execution failed. Weight distribution is estimated from input files (not pre-computed results).
        </div>
      )}
      <div className="summary-grid">
        <div className="summary-item">
          <label>Flight Number</label>
          <div className="value">{flight_info.flight_number}</div>
        </div>
        <div className="summary-item">
          <label>Route</label>
          <div className="value">{flight_info.departure_airport} → {flight_info.arrival_airport}</div>
        </div>
        <div className="summary-item">
          <label>Date</label>
          <div className="value">{flight_info.date}</div>
        </div>
        <div className="summary-item">
          <label>Aircraft Type</label>
          <div className="value">{flight_info.aircraft_type}</div>
        </div>
        <div className="summary-item">
          <label>Total Weight</label>
          <div className="value">{weight_distribution.total_weight.toFixed(1)} kg</div>
        </div>
        <div className="summary-item">
          <label>ZFW</label>
          <div className="value">{weight_distribution.zfw.toFixed(1)} kg</div>
        </div>
        <div className="summary-item">
          <label>%MAC ZFW</label>
          <div className="value">{weight_distribution.mac_zfw.toFixed(2)}%</div>
        </div>
        {fuel_savings_kg && (
          <div className="summary-item highlight">
            <label>Fuel Savings</label>
            <div className="value">{fuel_savings_kg.toFixed(1)} kg</div>
          </div>
        )}
        {runtime_seconds && (
          <div className="summary-item">
            <label>Runtime</label>
            <div className="value">{runtime_seconds.toFixed(2)}s</div>
          </div>
        )}
      </div>
    </div>
  );
};

export default FlightSummary;

