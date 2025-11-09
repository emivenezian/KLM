# Frontend Dashboard

React TypeScript dashboard for KLM Cargo Optimization.

## Structure

```
frontend/
├── public/          # Static files
├── src/
│   ├── components/  # React components
│   │   ├── Dashboard.tsx
│   │   ├── FlightSelector.tsx
│   │   ├── OptimizationControls.tsx
│   │   ├── ResultsVisualization.tsx
│   │   ├── FlightSummary.tsx
│   │   ├── WeightDistributionCharts.tsx
│   │   └── ULDUtilizationCharts.tsx
│   ├── services/    # API client
│   │   └── api.ts
│   ├── config.ts    # Configuration
│   ├── App.tsx      # Main app
│   └── index.tsx    # Entry point
└── package.json
```

## Features

- **Flight Selection**: Choose from available flights
- **Optimization Controls**: Run optimization with model selection
- **Visualizations**:
  - Weight distribution by compartment
  - Weight distribution by side (Left/Right)
  - ULD type distribution
  - Items per ULD
  - Weight per ULD
  - Flight summary metrics

## Running

```bash
cd app/frontend
npm install
npm start
```

Dashboard opens at http://localhost:3000

## Configuration

Edit `src/config.ts` to change API URL:

```typescript
export const API_BASE_URL = 'http://localhost:8000';
```

## Dependencies

- React 18
- TypeScript
- Recharts (for charts)
- Axios (for API calls)

