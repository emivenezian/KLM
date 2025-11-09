import React from 'react';
import { SafetyMetrics } from '../services/api';
import './SafetyMetricsDisplay.css';

interface SafetyMetricsDisplayProps {
  metrics: SafetyMetrics;
}

const SafetyMetricsDisplay: React.FC<SafetyMetricsDisplayProps> = ({ metrics }) => {
  const getComplianceIcon = (compliant: boolean) => {
    return compliant ? '✅' : '❌';
  };

  return (
    <div className="safety-metrics-container">
      <div className="card">
        <h2>Safety & Compliance Metrics</h2>
        
        {metrics.safety_score !== undefined && metrics.safety_score !== null && (
          <div className="safety-score">
            <label>Overall Safety Score</label>
            <div className={`metric-value-large ${metrics.safety_score >= 0.9 ? 'good' : metrics.safety_score >= 0.7 ? 'warning' : 'error'}`}>
              {(metrics.safety_score * 100).toFixed(1)}%
            </div>
          </div>
        )}

        <div className="metrics-grid">
          {metrics.weight_limits_compliance && Object.entries(metrics.weight_limits_compliance).length > 0 && (
            <>
              <h3>Weight Limits Compliance</h3>
              {Object.entries(metrics.weight_limits_compliance).map(([compartment, compliant]) => (
                <div key={compartment} className="metric-item">
                  <label>{compartment}</label>
                  <div className="metric-value">
                    {getComplianceIcon(compliant)} {compliant ? 'Compliant' : 'Exceeded'}
                  </div>
                </div>
              ))}
            </>
          )}

          {metrics.balance_limits_compliance && Object.entries(metrics.balance_limits_compliance).length > 0 && (
            <>
              <h3>Balance Limits Compliance</h3>
              {Object.entries(metrics.balance_limits_compliance).map(([side, compliant]) => (
                <div key={side} className="metric-item">
                  <label>{side} Side</label>
                  <div className="metric-value">
                    {getComplianceIcon(compliant)} {compliant ? 'Compliant' : 'Out of Range'}
                  </div>
                </div>
              ))}
            </>
          )}

          {metrics.cg_limits_compliance !== undefined && metrics.cg_limits_compliance !== null && (
            <div className="metric-item">
              <label>CG Limits</label>
              <div className="metric-value">
                {getComplianceIcon(metrics.cg_limits_compliance)} {metrics.cg_limits_compliance ? 'Compliant' : 'Out of Range'}
              </div>
            </div>
          )}

          {metrics.restricted_locations_used && metrics.restricted_locations_used.length > 0 && (
            <div className="metric-item warning">
              <label>Restricted Locations Used</label>
              <div className="metric-value">{metrics.restricted_locations_used.join(', ')}</div>
            </div>
          )}

          {metrics.temperature_constraints_violated !== undefined && metrics.temperature_constraints_violated > 0 && (
            <div className="metric-item error">
              <label>Temperature Violations</label>
              <div className="metric-value">{metrics.temperature_constraints_violated}</div>
            </div>
          )}

          {metrics.separation_constraints_violated !== undefined && metrics.separation_constraints_violated > 0 && (
            <div className="metric-item error">
              <label>Separation Violations</label>
              <div className="metric-value">{metrics.separation_constraints_violated}</div>
            </div>
          )}

          {metrics.max_weight_exceeded_positions && metrics.max_weight_exceeded_positions.length > 0 && (
            <div className="metric-item error">
              <label>Positions Exceeding Max Weight</label>
              <div className="metric-value">{metrics.max_weight_exceeded_positions.join(', ')}</div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default SafetyMetricsDisplay;

