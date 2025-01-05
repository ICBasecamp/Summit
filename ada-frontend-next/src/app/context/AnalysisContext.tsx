import React, { createContext, useState, useEffect, ReactNode, useContext } from 'react';

interface AnalysisContextType {
  messages: string[];
  setMessages: React.Dispatch<React.SetStateAction<string[]>>;
  fetchData: (ticker: any) => () => void;
  ticker: string | null;
  setTicker: React.Dispatch<React.SetStateAction<string | null>>;
}

const AnalysisContext = createContext<AnalysisContextType | null>(null);

export const AnalysisProvider = ({ children }: { children: ReactNode }) => {
  const [messages, setMessages] = useState<string[]>(() => {
    if (typeof window !== 'undefined') {
      const savedMessages = localStorage.getItem('messages');
      return savedMessages ? JSON.parse(savedMessages) : [];
    }
    return [];
  });
  const [ticker, setTicker] = useState<string | null>(null);

  useEffect(() => {
    if (typeof window !== 'undefined') {
      localStorage.setItem('messages', JSON.stringify(messages));
    }
  }, [messages]);

  const fetchData = (ticker: any) => {
    console.log('Fetching data for ticker:', ticker);
    const eventSource = new EventSource(`http://127.0.0.1:5000/analyze/${ticker}`);

    eventSource.onmessage = (event) => {
      const newMessage = event.data;
      setMessages((prevMessages) => {
        if (!prevMessages.includes(newMessage)) {
          return [...prevMessages, newMessage];
        }
        return prevMessages;
      });
    };

    eventSource.onerror = (error) => {
      console.error('EventSource failed:', error);
      eventSource.close();
    };

    return () => {
      eventSource.close();
    };
  };

  return (
    <AnalysisContext.Provider value={{ messages, setMessages, fetchData, ticker, setTicker }}>
      {children}
    </AnalysisContext.Provider>
  );
};

export const useAnalysis = () => {
  return useContext(AnalysisContext);
};