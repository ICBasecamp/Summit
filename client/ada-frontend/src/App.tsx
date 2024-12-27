import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, useNavigate, useParams } from 'react-router-dom';
import './App.css';

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

const AnalysisResults: React.FC = () => {
  const { ticker } = useParams<{ ticker: string }>();
  const [messages, setMessages] = useState<string[]>([]);

  React.useEffect(() => {
    setMessages([]);
    const eventSource = new EventSource(`http://127.0.0.1:5000/analyze/${ticker}`);

    eventSource.onmessage = (event) => {
      setMessages((prevMessages) => [...prevMessages, event.data]);
    };

    eventSource.onerror = (error) => {
      console.error('EventSource failed:', error);
      eventSource.close();
    };

    return () => {
      eventSource.close();
    };
  }, [ticker]);

  return (
    <div>
      <h1>Stock Analysis Results for {ticker}</h1>
      <div>
        <h2>Analysis Updates</h2>
        <ul>
          {messages.map((message, index) => (
            <li key={index}>{message}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};

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