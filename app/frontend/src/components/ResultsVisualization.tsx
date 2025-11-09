import React from 'react';
import { OptimizationResult } from '../services/api';
import WeightDistributionCharts from './WeightDistributionCharts';
import ULDUtilizationCharts from './ULDUtilizationCharts';
import FlightSummary from './FlightSummary';
import CargoMetricsDisplay from './CargoMetricsDisplay';
import PerformanceMetricsDisplay from './PerformanceMetricsDisplay';
import SafetyMetricsDisplay from './SafetyMetricsDisplay';
import OptimizationMetricsDisplay from './OptimizationMetricsDisplay';
import KLMComparisonDisplay from './KLMComparisonDisplay';
import './ResultsVisualization.css';

interface ResultsVisualizationProps {
  result: OptimizationResult;
}

const ResultsVisualization: React.FC<ResultsVisualizationProps> = ({ result }) => {
  if (!result.success) {
    return (
      <div className="card error">
        <h2>Optimization Failed</h2>
        <p>{result.error_message}</p>
      </div>
    );
  }

  return (
    <div className="results-container">
      <FlightSummary result={result} />
      
      {result.performance_metrics && (
        <PerformanceMetricsDisplay metrics={result.performance_metrics} />
      )}
      
      {result.optimization_metrics && (
        <OptimizationMetricsDisplay metrics={result.optimization_metrics} />
      )}
      
      <WeightDistributionCharts
        weightDistribution={result.weight_distribution}
      />
      
      <ULDUtilizationCharts
        uldUtilization={result.uld_utilization}
        ulds={result.ulds}
      />
      
      {result.cargo_metrics && (
        <CargoMetricsDisplay metrics={result.cargo_metrics} />
      )}
      
      {result.safety_metrics && (
        <SafetyMetricsDisplay metrics={result.safety_metrics} />
      )}
      
      {result.comparison_metrics && (
        <KLMComparisonDisplay comparisonMetrics={result.comparison_metrics} />
      )}
    </div>
  );
};

export default ResultsVisualization;

