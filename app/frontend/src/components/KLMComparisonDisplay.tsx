import React from 'react';
import { ComparisonMetrics } from '../services/api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts';
import './KLMComparisonDisplay.css';

interface KLMComparisonDisplayProps {
  comparisonMetrics: ComparisonMetrics;
}

const KLMComparisonDisplay: React.FC<KLMComparisonDisplayProps> = ({ comparisonMetrics }) => {
  // Show comparison even if KLM actual data is not available - show what we can
  if (!comparisonMetrics || (!comparisonMetrics.klm_actual && !comparisonMetrics.annual_impact)) {
    return (
      <div className="card">
        <h2>Comparison vs KLM Actual</h2>
        <p className="info-text">KLM actual loading data not available for this flight.</p>
      </div>
    );
  }

  const klmActual = comparisonMetrics.klm_actual || {};

  // Prepare weight comparison data by compartment (only if KLM actual data exists)
  const compartmentComparisonData = klmActual && klmActual.actual_weight_by_compartment ? [
    {
      compartment: 'C1',
      optimized: (klmActual.actual_weight_by_compartment?.['C1'] || 0) + (comparisonMetrics.weight_difference_by_compartment?.['C1'] || 0),
      klmActual: klmActual.actual_weight_by_compartment?.['C1'] || 0,
      difference: comparisonMetrics.weight_difference_by_compartment?.['C1'] || 0,
    },
    {
      compartment: 'C2',
      optimized: (klmActual.actual_weight_by_compartment?.['C2'] || 0) + (comparisonMetrics.weight_difference_by_compartment?.['C2'] || 0),
      klmActual: klmActual.actual_weight_by_compartment?.['C2'] || 0,
      difference: comparisonMetrics.weight_difference_by_compartment?.['C2'] || 0,
    },
    {
      compartment: 'C3',
      optimized: (klmActual.actual_weight_by_compartment?.['C3'] || 0) + (comparisonMetrics.weight_difference_by_compartment?.['C3'] || 0),
      klmActual: klmActual.actual_weight_by_compartment?.['C3'] || 0,
      difference: comparisonMetrics.weight_difference_by_compartment?.['C3'] || 0,
    },
    {
      compartment: 'C4',
      optimized: (klmActual.actual_weight_by_compartment?.['C4'] || 0) + (comparisonMetrics.weight_difference_by_compartment?.['C4'] || 0),
      klmActual: klmActual.actual_weight_by_compartment?.['C4'] || 0,
      difference: comparisonMetrics.weight_difference_by_compartment?.['C4'] || 0,
    },
  ] : [];

  // Side comparison data (only if KLM actual data exists)
  const sideComparisonData = klmActual && klmActual.actual_weight_by_side ? [
    {
      side: 'Left',
      optimized: (klmActual.actual_weight_by_side?.['Left'] || 0) + (comparisonMetrics.weight_difference_by_side?.['Left'] || 0),
      klmActual: klmActual.actual_weight_by_side?.['Left'] || 0,
      difference: comparisonMetrics.weight_difference_by_side?.['Left'] || 0,
    },
    {
      side: 'Right',
      optimized: (klmActual.actual_weight_by_side?.['Right'] || 0) + (comparisonMetrics.weight_difference_by_side?.['Right'] || 0),
      klmActual: klmActual.actual_weight_by_side?.['Right'] || 0,
      difference: comparisonMetrics.weight_difference_by_side?.['Right'] || 0,
    },
  ] : [];

  // Format currency
  const formatCurrency = (value?: number) => {
    if (value === undefined || value === null) return 'N/A';
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    }).format(value);
  };

  // Format weight
  const formatWeight = (value?: number) => {
    if (value === undefined || value === null) return 'N/A';
    return `${value.toFixed(1)} kg`;
  };

  // Get color for savings (green for positive, red for negative)
  const getSavingsColor = (value?: number) => {
    if (value === undefined || value === null) return '#666';
    return value >= 0 ? '#00C49F' : '#FF8042';
  };

  return (
    <div className="klm-comparison-container">
      <div className="card">
        <h2>Comparison vs KLM Actual Loading</h2>
        <p className="info-text">
          This compares your optimization model results with what KLM actually loaded on this flight.
        </p>

        {/* Fuel & Cost Savings Summary */}
        {(comparisonMetrics.fuel_savings_vs_klm_actual_kg !== undefined || 
          comparisonMetrics.cost_savings_vs_klm_actual_usd !== undefined ||
          comparisonMetrics.co2_savings_vs_klm_actual_kg !== undefined ||
          comparisonMetrics.mac_difference !== undefined) && (
        <div className="comparison-summary-grid">
          {comparisonMetrics.fuel_savings_vs_klm_actual_kg !== undefined && (
            <div className="summary-item">
              <label>FUEL SAVINGS</label>
              <div className={`value ${comparisonMetrics.fuel_savings_vs_klm_actual_kg >= 0 ? 'positive' : 'negative'}`}>
                {comparisonMetrics.fuel_savings_vs_klm_actual_kg >= 0 ? '+' : ''}{formatWeight(comparisonMetrics.fuel_savings_vs_klm_actual_kg)}
              </div>
              {comparisonMetrics.fuel_savings_vs_klm_actual_percent !== undefined && (
                <div className={`sub-value ${comparisonMetrics.fuel_savings_vs_klm_actual_percent >= 0 ? 'positive' : 'negative'}`}>
                  ({comparisonMetrics.fuel_savings_vs_klm_actual_percent >= 0 ? '+' : ''}{comparisonMetrics.fuel_savings_vs_klm_actual_percent.toFixed(2)}%)
                </div>
              )}
            </div>
          )}

          {comparisonMetrics.cost_savings_vs_klm_actual_usd !== undefined && (
            <div className="summary-item">
              <label>COST SAVINGS</label>
              <div className={`value ${comparisonMetrics.cost_savings_vs_klm_actual_usd >= 0 ? 'positive' : 'negative'}`}>
                {formatCurrency(comparisonMetrics.cost_savings_vs_klm_actual_usd)}
              </div>
              <div className="sub-value">per flight</div>
            </div>
          )}

          {comparisonMetrics.co2_savings_vs_klm_actual_kg !== undefined && (
            <div className="summary-item">
              <label>CO₂ REDUCTION</label>
              <div className={`value ${comparisonMetrics.co2_savings_vs_klm_actual_kg >= 0 ? 'positive' : 'negative'}`}>
                {comparisonMetrics.co2_savings_vs_klm_actual_kg >= 0 ? '+' : ''}{formatWeight(comparisonMetrics.co2_savings_vs_klm_actual_kg)}
              </div>
              <div className="sub-value">emissions avoided</div>
            </div>
          )}

          {comparisonMetrics.mac_difference !== undefined && (
            <div className="summary-item">
              <label>MAC ZFW DIFFERENCE</label>
              <div className={`value ${Math.abs(comparisonMetrics.mac_difference) < 2 ? 'positive' : comparisonMetrics.mac_difference > 0 ? 'negative' : 'positive'}`}>
                {comparisonMetrics.mac_difference > 0 ? '+' : ''}{comparisonMetrics.mac_difference.toFixed(2)}%
              </div>
              <div className="sub-value">
                {comparisonMetrics.klm_actual?.actual_mac_zfw !== undefined && klmActual.actual_mac_zfw !== undefined && (
                  <>Optimized: {(klmActual.actual_mac_zfw + comparisonMetrics.mac_difference).toFixed(2)}% → KLM Actual: {klmActual.actual_mac_zfw.toFixed(2)}%</>
                )}
              </div>
            </div>
          )}
        </div>
        )}

        {/* Weight Distribution Comparison - Only show if data available */}
        {compartmentComparisonData.length > 0 && (
          <div className="comparison-section">
            <h3>Weight Distribution by Compartment</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={compartmentComparisonData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="compartment" />
                <YAxis label={{ value: 'Weight (kg)', angle: -90, position: 'insideLeft' }} />
                <Tooltip formatter={(value: number) => `${value.toFixed(1)} kg`} />
                <Legend />
                <Bar dataKey="optimized" fill="#0088FE" name="Optimized Model" />
                <Bar dataKey="klmActual" fill="#FF8042" name="KLM Actual" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Side Comparison - Only show if data available */}
        {sideComparisonData.length > 0 && (
          <div className="comparison-section">
            <h3>Weight Distribution by Side</h3>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={sideComparisonData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="side" />
                <YAxis label={{ value: 'Weight (kg)', angle: -90, position: 'insideLeft' }} />
                <Tooltip formatter={(value: number) => `${value.toFixed(1)} kg`} />
                <Legend />
                <Bar dataKey="optimized" fill="#0088FE" name="Optimized Model" />
                <Bar dataKey="klmActual" fill="#FF8042" name="KLM Actual" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Key Metrics Table - Only show if KLM actual data available */}
        {klmActual && Object.keys(klmActual).length > 0 && (
          <div className="comparison-section">
            <h3>Key Metrics Comparison</h3>
            <table className="comparison-table">
            <thead>
              <tr>
                <th>Metric</th>
                <th>Optimized Model</th>
                <th>KLM Actual</th>
                <th>Difference</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Total Weight</td>
                <td>
                  {formatWeight(
                    klmActual.actual_total_weight && comparisonMetrics.weight_difference_by_compartment
                      ? klmActual.actual_total_weight + Object.values(comparisonMetrics.weight_difference_by_compartment).reduce((a, b) => a + b, 0)
                      : undefined
                  )}
                </td>
                <td>{formatWeight(klmActual.actual_total_weight)}</td>
                <td>
                  {formatWeight(
                    comparisonMetrics.weight_difference_by_compartment
                      ? Object.values(comparisonMetrics.weight_difference_by_compartment).reduce((a, b) => a + b, 0)
                      : undefined
                  )}
                </td>
              </tr>
              <tr>
                <td>Total ULDs</td>
                <td>
                  {klmActual.actual_total_ulds && comparisonMetrics.uld_count_difference !== undefined
                    ? klmActual.actual_total_ulds + comparisonMetrics.uld_count_difference
                    : 'N/A'}
                </td>
                <td>{klmActual.actual_total_ulds ?? 'N/A'}</td>
                <td>
                  {comparisonMetrics.uld_count_difference !== undefined
                    ? `${comparisonMetrics.uld_count_difference > 0 ? '+' : ''}${comparisonMetrics.uld_count_difference}`
                    : 'N/A'}
                </td>
              </tr>
              <tr>
                <td>MAC ZFW</td>
                <td>
                  {klmActual.actual_mac_zfw && comparisonMetrics.mac_difference !== undefined
                    ? (klmActual.actual_mac_zfw + comparisonMetrics.mac_difference).toFixed(2) + '%'
                    : 'N/A'}
                </td>
                <td>{klmActual.actual_mac_zfw?.toFixed(2)}%</td>
                <td>
                  {comparisonMetrics.mac_difference !== undefined
                    ? `${comparisonMetrics.mac_difference > 0 ? '+' : ''}${comparisonMetrics.mac_difference.toFixed(2)}%`
                    : 'N/A'}
                </td>
              </tr>
            </tbody>
          </table>
          </div>
        )}

        {/* Annual Impact Section - Always show if available */}
        {comparisonMetrics.annual_impact && (
          <div className="comparison-section annual-impact-section">
            <h3>Annual Impact Projection</h3>
            <p className="info-text">
              Projected annual impact if optimization is applied to all KLM intercontinental flights (~{comparisonMetrics.annual_impact.flights_per_year?.toLocaleString()} flights/year)
            </p>
            
            <div className="annual-impact-grid">
              {comparisonMetrics.annual_impact.cost_savings_per_year_usd !== undefined && (
                <div className={`impact-card ${comparisonMetrics.annual_impact.cost_savings_per_year_usd >= 0 ? 'highlight' : ''}`}>
                  <div className="impact-label">Annual Cost Impact</div>
                  <div className={`impact-value ${comparisonMetrics.annual_impact.cost_savings_per_year_usd >= 0 ? '' : 'negative'}`}>
                    {formatCurrency(comparisonMetrics.annual_impact.cost_savings_per_year_usd)}
                  </div>
                  <div className="impact-subtext">per year</div>
                </div>
              )}

              {comparisonMetrics.annual_impact.fuel_savings_per_year_kg !== undefined && (
                <div className="impact-card">
                  <div className="impact-label">Annual Fuel Impact</div>
                  <div className={`impact-value ${comparisonMetrics.annual_impact.fuel_savings_per_year_kg >= 0 ? '' : 'negative'}`}>
                    {comparisonMetrics.annual_impact.fuel_savings_per_year_kg >= 0 ? '+' : ''}{formatWeight(comparisonMetrics.annual_impact.fuel_savings_per_year_kg)}
                  </div>
                  {comparisonMetrics.annual_impact.fuel_savings_per_year_liters && (
                    <div className="impact-subtext">
                      ({comparisonMetrics.annual_impact.fuel_savings_per_year_liters >= 0 ? '+' : ''}{comparisonMetrics.annual_impact.fuel_savings_per_year_liters.toLocaleString(undefined, {maximumFractionDigits: 0})} liters)
                    </div>
                  )}
                </div>
              )}

              {comparisonMetrics.annual_impact.co2_reduction_per_year_tons !== undefined && (
                <div className="impact-card">
                  <div className="impact-label">Annual CO₂ Impact</div>
                  <div className={`impact-value ${comparisonMetrics.annual_impact.co2_reduction_per_year_tons >= 0 ? '' : 'negative'}`}>
                    {comparisonMetrics.annual_impact.co2_reduction_per_year_tons >= 0 ? '+' : ''}{comparisonMetrics.annual_impact.co2_reduction_per_year_tons.toLocaleString(undefined, {maximumFractionDigits: 1})} tons
                  </div>
                  <div className="impact-subtext">{comparisonMetrics.annual_impact.co2_reduction_per_year_tons >= 0 ? 'emissions avoided' : 'additional emissions'} per year</div>
                </div>
              )}
            </div>

            <div className="impact-note">
              <strong>Note:</strong> Based on {comparisonMetrics.annual_impact.flights_per_year?.toLocaleString()} intercontinental flights per year. 
              Fuel price assumption: ${comparisonMetrics.annual_impact.fuel_price_per_kg?.toFixed(2)}/kg.
              {comparisonMetrics.annual_impact.cost_savings_per_year_usd !== undefined && comparisonMetrics.annual_impact.cost_savings_per_year_usd < 0 && (
                <><br/><strong>Warning:</strong> Negative values indicate the optimization model resulted in higher fuel consumption than KLM's actual loading.</>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default KLMComparisonDisplay;

