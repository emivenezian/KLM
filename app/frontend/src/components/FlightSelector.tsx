import React from 'react';
import './FlightSelector.css';

interface FlightSelectorProps {
  flights: string[];
  selectedFlight: string;
  onSelectFlight: (flight: string) => void;
  onRefresh: () => void;
}

const FlightSelector: React.FC<FlightSelectorProps> = ({
  flights,
  selectedFlight,
  onSelectFlight,
  onRefresh,
}) => {
  return (
    <div className="card">
      <div className="card-header">
        <h2>Select Flight</h2>
        <button className="btn btn-secondary" onClick={onRefresh}>
          Refresh
        </button>
      </div>
      <div className="input-group">
        <label>Available Flights ({flights.length})</label>
        <select
          value={selectedFlight}
          onChange={(e) => onSelectFlight(e.target.value)}
          disabled={flights.length === 0}
        >
          {flights.length === 0 ? (
            <option>No flights available</option>
          ) : (
            flights.map((flight) => (
              <option key={flight} value={flight}>
                {flight}
              </option>
            ))
          )}
        </select>
      </div>
    </div>
  );
};

export default FlightSelector;

