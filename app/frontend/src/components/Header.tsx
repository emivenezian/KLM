import React from 'react';
import './Header.css';

const Header: React.FC = () => {
  return (
    <header className="header">
      <div className="header-content">
        <h1>✈️ KLM Cargo Optimization</h1>
        <p className="subtitle">Cargo Loading Optimization Dashboard</p>
      </div>
    </header>
  );
};

export default Header;

