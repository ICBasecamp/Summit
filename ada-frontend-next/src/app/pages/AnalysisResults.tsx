"use client";

import React, { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { useAnalysis } from '../context/AnalysisContext';
import { Spinner } from '@nextui-org/spinner';

const AnalysisResults: React.FC<{ ticker: string | null }> = ({ ticker }) => {
  const analysisContext = useAnalysis();
  if (!analysisContext) {
    return <div>Error: Analysis context is not available.</div>;
  }
  const { fetchData, messages, setMessages } = analysisContext;
  const [latestMessage, setLatestMessage] = useState<string>('');
  const router = useRouter();
  const hasFetchedData = useRef(false);

  useEffect(() => {
    if (!ticker || hasFetchedData.current) return;

    // Clear messages and localStorage before starting a new analysis
    setMessages([]);
    localStorage.removeItem('messages');

    setLatestMessage('');
    fetchData(ticker);
    hasFetchedData.current = true;
  }, [ticker, fetchData, setMessages]);

  useEffect(() => {
    if (messages.length > 0) {
      const lastMessage = messages[messages.length - 1];
      console.log(lastMessage);
      setLatestMessage(lastMessage);

      if (lastMessage.includes("Analysis complete.")) {
        router.push(`/news`);
      }
    }
  }, [messages, router, ticker]);

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