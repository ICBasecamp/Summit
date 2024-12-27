// src/App.tsx
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import TickerForm from './TickerForm';
import AnalysisResults from './AnalysisResults';

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<TickerForm />} />
        <Route path="/results/:ticker" element={<AnalysisResults />} />
      </Routes>
    </Router>
  );
};

export default App;