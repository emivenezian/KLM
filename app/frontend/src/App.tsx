import React, { useState, useEffect } from 'react';
import './App.css';
import Dashboard from './components/Dashboard';
import Header from './components/Header';

function App() {
  return (
    <div className="app-container">
      <Header />
      <Dashboard />
    </div>
  );
}

export default App;

