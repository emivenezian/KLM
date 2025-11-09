import React from 'react';
import { CargoMetrics } from '../services/api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './CargoMetricsDisplay.css';

interface CargoMetricsDisplayProps {
  metrics: CargoMetrics;
}

const CargoMetricsDisplay: React.FC<CargoMetricsDisplayProps> = ({ metrics }) => {
  // Prepare weight range data
  const weightRangeData = Object.entries(metrics.items_by_weight_range || {}).map(([range, count]) => ({
    range,
    count,
  }));

  // Prepare commodity distribution data
  const commodityData = Object.entries(metrics.weight_distribution_by_commodity || {})
    .map(([commodity, weight]) => ({
      commodity: commodity.substring(0, 15), // Truncate long names
      weight: Math.round(weight),
    }))
    .sort((a, b) => b.weight - a.weight)
    .slice(0, 10); // Top 10

  return (
    <div className="cargo-metrics-container">
      <div className="card">
        <h2>Cargo Metrics</h2>
        <div className="metrics-grid">
          <div className="metric-item">
            <label>Total Items</label>
            <div className="metric-value">{metrics.total_items}</div>
          </div>
          {metrics.average_item_weight && (
            <div className="metric-item">
              <label>Avg Item Weight</label>
              <div className="metric-value">{metrics.average_item_weight.toFixed(1)} kg</div>
            </div>
          )}
          {metrics.max_item_weight && (
            <div className="metric-item">
              <label>Max Item Weight</label>
              <div className="metric-value">{metrics.max_item_weight.toFixed(1)} kg</div>
            </div>
          )}
          {metrics.min_item_weight && (
            <div className="metric-item">
              <label>Min Item Weight</label>
              <div className="metric-value">{metrics.min_item_weight.toFixed(1)} kg</div>
            </div>
          )}
          {metrics.total_volume && (
            <div className="metric-item">
              <label>Total Volume</label>
              <div className="metric-value">{metrics.total_volume.toFixed(2)} m³</div>
            </div>
          )}
          {metrics.items_without_uld !== undefined && (
            <div className="metric-item">
              <label>Items Without ULD</label>
              <div className="metric-value">{metrics.items_without_uld}</div>
            </div>
          )}
          {metrics.total_crt_items !== undefined && (
            <div className="metric-item">
              <label>CRT Items</label>
              <div className="metric-value">{metrics.total_crt_items}</div>
            </div>
          )}
          {metrics.total_col_items !== undefined && (
            <div className="metric-item">
              <label>COL Items</label>
              <div className="metric-value">{metrics.total_col_items}</div>
            </div>
          )}
          {metrics.total_dangerous_items !== undefined && (
            <div className="metric-item">
              <label>Dangerous Items</label>
              <div className="metric-value">{metrics.total_dangerous_items}</div>
            </div>
          )}
        </div>
      </div>

      {weightRangeData.length > 0 && (
        <div className="card">
          <h2>Items by Weight Range</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={weightRangeData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="range" />
              <YAxis label={{ value: 'Count', angle: -90, position: 'insideLeft' }} />
              <Tooltip />
              <Bar dataKey="count" fill="#0088FE" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

      {commodityData.length > 0 && (
        <div className="card">
          <h2>Weight by Commodity (Top 10)</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={commodityData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="commodity" angle={-45} textAnchor="end" height={80} />
              <YAxis label={{ value: 'Weight (kg)', angle: -90, position: 'insideLeft' }} />
              <Tooltip formatter={(value: number) => `${value} kg`} />
              <Bar dataKey="weight" fill="#00C49F" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

      {metrics.largest_items && metrics.largest_items.length > 0 && (
        <div className="card">
          <h2>Largest Items (Top 10)</h2>
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Serial Number</th>
                  <th>Weight (kg)</th>
                  <th>Commodity</th>
                </tr>
              </thead>
              <tbody>
                {metrics.largest_items.map((item, idx) => (
                  <tr key={idx}>
                    <td>{item.serialnumber}</td>
                    <td>{item.weight.toFixed(1)}</td>
                    <td>{item.commodity || 'N/A'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

export default CargoMetricsDisplay;

