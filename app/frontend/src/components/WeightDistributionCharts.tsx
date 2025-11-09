import React from 'react';
import { WeightDistribution } from '../services/api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import './WeightDistributionCharts.css';

interface WeightDistributionChartsProps {
  weightDistribution: WeightDistribution;
}

const WeightDistributionCharts: React.FC<WeightDistributionChartsProps> = ({ weightDistribution }) => {
  // Prepare data for compartment chart
  const compartmentData = Object.entries(weightDistribution.by_compartment).map(([key, value]) => ({
    compartment: key,
    weight: value,
  }));

  // Prepare data for side chart
  const sideData = Object.entries(weightDistribution.by_side).map(([key, value]) => ({
    side: key,
    weight: value,
  }));

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

  return (
    <div className="charts-container">
      <div className="card">
        <h2>Weight Distribution by Compartment</h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={compartmentData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="compartment" />
            <YAxis label={{ value: 'Weight (kg)', angle: -90, position: 'insideLeft' }} />
            <Tooltip formatter={(value: number) => `${value.toFixed(1)} kg`} />
            <Legend />
            <Bar dataKey="weight" fill="#0066cc" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="card">
        <h2>Weight Distribution by Side</h2>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={sideData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ side, weight, percent }) => `${side}: ${(percent * 100).toFixed(1)}%`}
              outerRadius={80}
              fill="#8884d8"
              dataKey="weight"
            >
              {sideData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip formatter={(value: number) => `${value.toFixed(1)} kg`} />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default WeightDistributionCharts;

