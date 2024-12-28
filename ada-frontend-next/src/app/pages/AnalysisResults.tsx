"use client";

import React, { useState, useEffect } from 'react';
import { useAnalysis } from '../context/AnalysisContext';

const AnalysisResults: React.FC<{ ticker: string }> = ({ ticker }) => {
  const { data, setData } = useAnalysis();
  const [progress, setProgress] = useState<string>('');

  useEffect(() => {
    if (!ticker) return;

    const eventSource = new EventSource(`http://127.0.0.1:5000/analyze/${ticker}`);

    eventSource.onmessage = (event) => {
      const data = event.data;
      if (data.includes('socialMedia')) {
        setProgress('Analyzing social media...');
      } else if (data.includes('earnings')) {
        setProgress('Analyzing earnings reports...');
      } else if (data.includes('news')) {
        setProgress('Analyzing news articles...');
      } else if (data.includes('economicIndicators')) {
        setProgress('Analyzing economic indicators...');
      } else if (data.includes('An error occurred')) {
        setProgress('An error occurred');
      } else {
        setProgress(data);
      }

      if (data.includes('socialMedia:')) {
        setData((prevData) => ({ ...prevData, socialMedia: data }));
      } else if (data.includes('earnings:')) {
        setData((prevData) => ({ ...prevData, earnings: data }));
      } else if (data.includes('news:')) {
        setData((prevData) => ({ ...prevData, news: data }));
      } else if (data.includes('economicIndicators:')) {
        setData((prevData) => ({ ...prevData, economicIndicators: data }));
      }
    };

    eventSource.onerror = (error) => {
      console.error('EventSource failed:', error);
      setProgress('An error occurred while connecting to the server.');
      eventSource.close();
    };

    return () => {
      eventSource.close();
    };
  }, [ticker, setData]);

  return (
    <div>
      <h1>Stock Analysis Results for {ticker}</h1>
      <div>
        <h2>Progress</h2>
        <pre>{progress}</pre>
      </div>
    </div>
  );
};

export default AnalysisResults;