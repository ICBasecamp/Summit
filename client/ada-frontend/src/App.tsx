import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [messages, setMessages] = useState<string[]>([]);

  const handleAnalyze = () => {
    setMessages([]);
    const eventSource = new EventSource('http://127.0.0.1:5000/analyze/AAPL');

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
  }

  return (
    <>
      <div>
      </div>
      <div className="card">
        <button onClick={handleAnalyze}>Start Analysis</button>
      </div>
      <div>
        <h2>Analysis Updates</h2>
        <ul>
          {messages.map((message, index) => (
            <li key={index}>{message}</li>
          ))}
        </ul>
      </div>
    </>
  );
}

export default App;
