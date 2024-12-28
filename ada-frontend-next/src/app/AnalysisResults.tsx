"use client";

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

const AnalysisResults: React.FC = () => {
  const router = useRouter();
  const { ticker } = router.query;
  const [socialMedia, setSocialMedia] = useState<string>('');
  const [earnings, setEarnings] = useState<string>('');
  const [news, setNews] = useState<string>('');
  const [economicIndicators, setEconomicIndicators] = useState<string>('');
  const [error, setError] = useState<string>('');

  useEffect(() => {
    if (!ticker) return;

    const eventSource = new EventSource(`http://127.0.0.1:5000/analyze/${ticker}`);

    eventSource.onmessage = (event) => {
      const data = event.data;
      if (data.includes('socialMedia')) {
        setSocialMedia(data);
      } else if (data.includes('earnings')) {
        setEarnings(data);
      } else if (data.includes('news')) {
        setNews(data);
      } else if (data.includes('economicIndicators')) {
        setEconomicIndicators(data);
      } else if (data.includes('An error occurred')) {
        setError(data);
      }
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
      {error && <div className="error">{error}</div>}
      <section>
        <h2>Social Media Analysis</h2>
        <pre>{socialMedia}</pre>
      </section>
      <section>
        <h2>Earnings Analysis</h2>
        <pre>{earnings}</pre>
      </section>
      <section>
        <h2>News Analysis</h2>
        <pre>{news}</pre>
      </section>
      <section>
        <h2>Economic Indicators Analysis</h2>
        <pre>{economicIndicators}</pre>
      </section>
    </div>
  );
};

export default AnalysisResults;