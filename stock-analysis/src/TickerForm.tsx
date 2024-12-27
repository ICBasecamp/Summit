// src/TickerForm.tsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const TickerForm: React.FC = () => {
  const [ticker, setTicker] = useState<string>('');
  const navigate = useNavigate();

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    navigate(`/results/${ticker}`);
  };

  return (
    <div>
      <h1>Enter Ticker</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={ticker}
          onChange={(e) => setTicker(e.target.value)}
          placeholder="Enter ticker symbol"
          required
        />
        <button type="submit">Analyze</button>
      </form>
    </div>
  );
};

export default TickerForm;