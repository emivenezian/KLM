import React from 'react';
import { ULDUtilization } from '../services/api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import './ULDUtilizationCharts.css';

interface ULDUtilizationChartsProps {
  uldUtilization: ULDUtilization;
  ulds: any[];
}

const ULDUtilizationCharts: React.FC<ULDUtilizationChartsProps> = ({ uldUtilization, ulds }) => {
  // Prepare ULD type distribution data
  const uldTypeData = Object.entries(uldUtilization.ulds_by_type).map(([type, count]) => ({
    type,
    count,
  }));

  // Prepare items per ULD data - use weight_per_uld or serialnumbers for labels
  const itemsPerULDData = Object.entries(uldUtilization.items_per_uld || {})
    .map(([uldIndex, itemCount]) => {
      const uldIndexNum = parseInt(uldIndex);
      const uld = ulds[uldIndexNum];
      return {
        uld: uld ? `${uld.serialnumber.substring(0, 10)}` : `ULD ${uldIndex}`,
        items: itemCount as number,
        weight: uldUtilization.weight_per_uld?.[uldIndexNum] || uld?.weight || 0,
      };
    })
    .filter(item => item.items > 0) // Only show ULDs with items
    .slice(0, 20); // Limit to first 20 for readability

  // Prepare weight per ULD data
  const weightPerULDData = ulds.slice(0, 20).map((uld, idx) => ({
    uld: uld.serialnumber.substring(0, 10),
    weight: uld.weight,
  }));

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8'];

  return (
    <div className="uld-charts-container">
      <div className="card">
        <h2>ULD Type Distribution</h2>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={uldTypeData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ type, count, percent }) => `${type}: ${count} (${(percent * 100).toFixed(1)}%)`}
              outerRadius={80}
              fill="#8884d8"
              dataKey="count"
            >
              {uldTypeData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>

      <div className="card">
        <h2>Items per ULD</h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={itemsPerULDData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="uld" angle={-45} textAnchor="end" height={80} />
            <YAxis label={{ value: 'Number of Items', angle: -90, position: 'insideLeft' }} />
            <Tooltip />
            <Legend />
            <Bar dataKey="items" fill="#0066cc" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="card">
        <h2>Weight per ULD</h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={weightPerULDData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="uld" angle={-45} textAnchor="end" height={80} />
            <YAxis label={{ value: 'Weight (kg)', angle: -90, position: 'insideLeft' }} />
            <Tooltip formatter={(value: number) => `${value.toFixed(1)} kg`} />
            <Legend />
            <Bar dataKey="weight" fill="#00C49F" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="card">
        <h2>ULD Utilization Metrics</h2>
        <div className="metrics-grid">
          <div className="metric-item">
            <label>Total ULDs</label>
            <div className="metric-value">{uldUtilization.total_ulds}</div>
          </div>
          <div className="metric-item">
            <label>Average Utilization</label>
            <div className="metric-value">{(uldUtilization.utilization_rate * 100).toFixed(1)}%</div>
          </div>
          <div className="metric-item">
            <label>Left Side ULDs</label>
            <div className="metric-value">{uldUtilization.ulds_by_side.Left || 0}</div>
          </div>
          <div className="metric-item">
            <label>Right Side ULDs</label>
            <div className="metric-value">{uldUtilization.ulds_by_side.Right || 0}</div>
          </div>
          {uldUtilization.average_uld_weight && (
            <div className="metric-item">
              <label>Avg ULD Weight</label>
              <div className="metric-value">{uldUtilization.average_uld_weight.toFixed(1)} kg</div>
            </div>
          )}
          {uldUtilization.average_items_per_uld && (
            <div className="metric-item">
              <label>Avg Items/ULD</label>
              <div className="metric-value">{uldUtilization.average_items_per_uld.toFixed(1)}</div>
            </div>
          )}
          {uldUtilization.empty_ulds !== undefined && (
            <div className="metric-item">
              <label>Empty ULDs</label>
              <div className="metric-value">{uldUtilization.empty_ulds}</div>
            </div>
          )}
          {uldUtilization.max_uld_weight && (
            <div className="metric-item">
              <label>Max ULD Weight</label>
              <div className="metric-value">{uldUtilization.max_uld_weight.toFixed(1)} kg</div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ULDUtilizationCharts;

