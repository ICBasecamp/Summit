"use client";

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAnalysis } from '../context/AnalysisContext';
import { Spinner } from '@nextui-org/spinner';

const AnalysisResults: React.FC<{ ticker: string | null }> = ({ ticker }) => {
  const { setData } = useAnalysis();
  const [latestMessage, setLatestMessage] = useState<string>('');
  const router = useRouter();

  useEffect(() => {
    if (!ticker) return;

    setLatestMessage('');
    const eventSource = new EventSource(`http://127.0.0.1:5000/analyze/${ticker}`);

    eventSource.onmessage = (event) => {
      const newMessage = event.data;
      setLatestMessage(newMessage);

      // Assuming the event data is in JSON format and contains the analysis data
      const parsedData = newMessage;
      setData(parsedData);

      if (newMessage === "Analysis complete.") {
        router.push(`/${ticker}/news`);
      }
    };

    eventSource.onerror = (error) => {
      console.error('EventSource failed:', error);
      eventSource.close();
    };

    return () => {
      eventSource.close();
    };
  }, [ticker, setData, router]);

  if (!ticker) {
    return <div>Please enter a ticker symbol.</div>;
  }

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
      <Spinner color='default' size='lg' label={latestMessage} />
    </div>
  );
};

export default AnalysisResults;