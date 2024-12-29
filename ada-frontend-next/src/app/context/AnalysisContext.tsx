import React, { createContext, useContext, useState, ReactNode, FC } from 'react';

interface AnalysisData {
  socialMedia?: string;
  earnings?: string;
  news?: string;
  economicIndicators?: string;
  nonJsonMessages?: string[];
}

interface AnalysisContextType {
  data: AnalysisData | null;
  setData: (data: AnalysisData) => void;
}

const AnalysisContext = createContext<AnalysisContextType | undefined>(undefined);

export const AnalysisProvider: FC<{ children: ReactNode }> = ({ children }) => {
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