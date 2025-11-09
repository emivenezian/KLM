// API configuration
export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
export const API_V1_PREFIX = '/api/v1';

export const API_ENDPOINTS = {
  optimization: {
    run: `${API_BASE_URL}${API_V1_PREFIX}/optimization/run`,
    flights: `${API_BASE_URL}${API_V1_PREFIX}/optimization/flights`,
    synthetic: `${API_BASE_URL}${API_V1_PREFIX}/optimization/synthetic/generate`,
    visualization: `${API_BASE_URL}${API_V1_PREFIX}/optimization/visualization/prepare`
  },
  export: {
    sheets: `${API_BASE_URL}${API_V1_PREFIX}/export/sheets`,
    sheetsStatus: `${API_BASE_URL}${API_V1_PREFIX}/export/sheets/status`
  }
};

