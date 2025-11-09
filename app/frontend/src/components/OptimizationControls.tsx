import React, { useState } from 'react';
import { OptimizationRequest } from '../services/api';
import './OptimizationControls.css';

interface OptimizationControlsProps {
  selectedFlight: string;
  onRun: (request: OptimizationRequest) => void;
  loading: boolean;
}

const OptimizationControls: React.FC<OptimizationControlsProps> = ({
  selectedFlight,
  onRun,
  loading,
}) => {
  const [modelType, setModelType] = useState('delgado_venezian');

  const handleRun = () => {
    if (!selectedFlight) {
      alert('Please select a flight first');
      return;
    }

    const request: OptimizationRequest = {
      flight_path: selectedFlight,
      model_type: modelType,
      restricted_locations: [],
    };

    onRun(request);
  };

  return (
    <div className="card">
      <h2>Optimization Controls</h2>
      <div className="controls-grid">
        <div className="input-group">
          <label>Model Type</label>
          <select
            value={modelType}
            onChange={(e) => setModelType(e.target.value)}
          >
            <option value="delgado_venezian">DelgadoVenezian</option>
            <option value="baseline">Baseline</option>
            <option value="optimized_actual">Optimized Actual</option>
            <option value="bax_fixed">BAX Fixed</option>
          </select>
        </div>
        <div className="button-group">
          <button
            className="btn btn-primary"
            onClick={handleRun}
            disabled={loading || !selectedFlight}
          >
            {loading ? 'Running...' : 'Run Optimization'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default OptimizationControls;

