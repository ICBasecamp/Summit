// src/app/context/AnalysisContext.tsx
import React, { createContext, useState, useContext, ReactNode } from 'react';

interface AnalysisData {
  socialMedia: string;
  earnings: string;
  news: string;
  economicIndicators: string;
}

interface AnalysisContextType {
  data: AnalysisData | null;
  setData: (data: AnalysisData) => void;
}

const AnalysisContext = createContext<AnalysisContextType | undefined>(undefined);

export const AnalysisProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [data, setData] = useState<AnalysisData | null>(null);

  return (
    <AnalysisContext.Provider value={{ data, setData }}>
      {children}
    </AnalysisContext.Provider>
  );
};

export const useAnalysis = () => {
  const context = useContext(AnalysisContext);
  if (!context) {
    throw new Error('useAnalysis must be used within an AnalysisProvider');
  }
  return context;
};