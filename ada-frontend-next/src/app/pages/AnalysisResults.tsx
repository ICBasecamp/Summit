"use client";

import React, { useState, useEffect } from 'react';

const AnalysisResults: React.FC<{ ticker: string | null }> = ({ ticker }) => {
  const [messages, setMessages] = useState<string[]>([]);

  useEffect(() => {
    if (!ticker) return;

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

  if (!ticker) {
    return <div>Please enter a ticker symbol.</div>;
  }

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

export default AnalysisResults;