// src/AnalysisResults.tsx
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

const AnalysisResults: React.FC = () => {
  const { ticker } = useParams<{ ticker: string }>();
  const [socialMedia, setSocialMedia] = useState<string>('');
  const [earnings, setEarnings] = useState<string>('');
  const [news, setNews] = useState<string>('');
  const [economicIndicators, setEconomicIndicators] = useState<string>('');
  const [error, setError] = useState<string>('');

  useEffect(() => {
    const fetchData = async () => {
      const response = await fetch('http://localhost:5000/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ ticker }),
      });

      const reader = response.body?.getReader();
      const decoder = new TextDecoder('utf-8');

      if (reader) {
        let result = '';
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          result += decoder.decode(value, { stream: true });
          const data = result.trim().split('\n').pop();
          if (data?.includes('socialMedia')) {
            setSocialMedia(data);
          } else if (data?.includes('earnings')) {
            setEarnings(data);
          } else if (data?.includes('news')) {
            setNews(data);
          } else if (data?.includes('economicIndicators')) {
            setEconomicIndicators(data);
          } else if (data?.includes('An error occurred')) {
            setError(data);
          }
        }
      }
    };

    fetchData();
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