import React from 'react';
import { OptimizationMetrics } from '../services/api';
import './OptimizationMetricsDisplay.css';

interface OptimizationMetricsDisplayProps {
  metrics: OptimizationMetrics;
}

const OptimizationMetricsDisplay: React.FC<OptimizationMetricsDisplayProps> = ({ metrics }) => {
  const formatRuntime = (seconds?: number) => {
    if (seconds === undefined || seconds === null) return 'N/A';
    if (seconds < 1) return `${(seconds * 1000).toFixed(0)} ms`;
    if (seconds < 60) return `${seconds.toFixed(2)}s`;
    const minutes = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${minutes}m ${secs.toFixed(0)}s`;
  };

  const getStatusColor = (status?: string) => {
    if (!status) return '';
    const statusLower = status.toLowerCase();
    if (statusLower.includes('optimal')) return 'good';
    if (statusLower.includes('feasible')) return 'warning';
    if (statusLower.includes('infeasible') || statusLower.includes('error')) return 'error';
    return '';
  };

  return (
    <div className="optimization-metrics-container">
      <div className="card">
        <h2>Optimization Solver Metrics</h2>
        <div className="metrics-grid">
          {metrics.solver_status && (
            <div className="metric-item">
              <label>Solver Status</label>
              <div className={`metric-value ${getStatusColor(metrics.solver_status)}`}>
                {metrics.solver_status}
              </div>
            </div>
          )}
          
          {metrics.runtime_seconds !== undefined && metrics.runtime_seconds !== null && (
            <div className="metric-item">
              <label>Runtime</label>
              <div className="metric-value">{formatRuntime(metrics.runtime_seconds)}</div>
            </div>
          )}
          
          {metrics.objective_value !== undefined && metrics.objective_value !== null && (
            <div className="metric-item">
              <label>Objective Value</label>
              <div className="metric-value">{metrics.objective_value.toFixed(2)}</div>
            </div>
          )}
          
          {metrics.gap_percent !== undefined && metrics.gap_percent !== null && (
            <div className="metric-item">
              <label>MIP Gap</label>
              <div className="metric-value">{metrics.gap_percent.toFixed(2)}%</div>
            </div>
          )}
          
          {metrics.number_of_variables !== undefined && metrics.number_of_variables !== null && (
            <div className="metric-item">
              <label>Variables</label>
              <div className="metric-value">{metrics.number_of_variables.toLocaleString()}</div>
            </div>
          )}
          
          {metrics.number_of_constraints !== undefined && metrics.number_of_constraints !== null && (
            <div className="metric-item">
              <label>Constraints</label>
              <div className="metric-value">{metrics.number_of_constraints.toLocaleString()}</div>
            </div>
          )}
          
          {metrics.number_of_iterations !== undefined && metrics.number_of_iterations !== null && (
            <div className="metric-item">
              <label>Iterations</label>
              <div className="metric-value">{metrics.number_of_iterations.toLocaleString()}</div>
            </div>
          )}
          
          {metrics.number_of_nodes !== undefined && metrics.number_of_nodes !== null && (
            <div className="metric-item">
              <label>Nodes</label>
              <div className="metric-value">{metrics.number_of_nodes.toLocaleString()}</div>
            </div>
          )}
          
          {metrics.solution_time !== undefined && metrics.solution_time !== null && (
            <div className="metric-item">
              <label>Solution Time</label>
              <div className="metric-value">{formatRuntime(metrics.solution_time)}</div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default OptimizationMetricsDisplay;

