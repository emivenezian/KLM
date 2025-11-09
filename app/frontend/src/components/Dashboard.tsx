import React, { useState, useEffect } from 'react';
import { optimizationAPI, OptimizationResult, OptimizationRequest } from '../services/api';
import FlightSelector from './FlightSelector';
import OptimizationControls from './OptimizationControls';
import ResultsVisualization from './ResultsVisualization';
import './Dashboard.css';

const Dashboard: React.FC = () => {
  const [flights, setFlights] = useState<string[]>([]);
  const [selectedFlight, setSelectedFlight] = useState<string>('');
  const [result, setResult] = useState<OptimizationResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadFlights();
  }, []);

  const loadFlights = async () => {
    try {
      const flightList = await optimizationAPI.listFlights();
      setFlights(flightList);
      if (flightList.length > 0) {
        setSelectedFlight(flightList[0]);
      }
    } catch (err: any) {
      setError(`Failed to load flights: ${err.message}`);
    }
  };

  const runOptimization = async (request: OptimizationRequest) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const optimizationResult = await optimizationAPI.run(request);
      setResult(optimizationResult);
    } catch (err: any) {
      setError(err.response?.data?.detail || `Optimization failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="main-content">
      <FlightSelector
        flights={flights}
        selectedFlight={selectedFlight}
        onSelectFlight={setSelectedFlight}
        onRefresh={loadFlights}
      />

      <OptimizationControls
        selectedFlight={selectedFlight}
        onRun={runOptimization}
        loading={loading}
      />

      {error && (
        <div className="error">
          <strong>Error:</strong> {error}
        </div>
      )}

      {result && (
        <ResultsVisualization result={result} />
      )}
    </div>
  );
};

export default Dashboard;

