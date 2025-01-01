"use client";

import React, { useEffect, useState } from 'react';
import { useAnalysis } from '../../context/AnalysisContext';
import { SidebarDemo } from '../../pages/SideTabsER';
import { Header } from '../../components/header';

const AllMessagesDisplay: React.FC = () => {
  const analysisContext = useAnalysis();
  const messages = analysisContext?.messages || [];
  const [earningsMessage, setEarningsMessage] = useState<string | null>(null);

  useEffect(() => {
    const earningsReportMessage = messages.find(message => message.includes("earnings:"));
    if (earningsReportMessage) {
      setEarningsMessage(earningsReportMessage);
    } else {
      setEarningsMessage(null);
    }
  }, [messages]);

  return (
    <div className="flex flex-col bg-neutral-900 w-full h-screen">
      <Header />
      <div className="flex flex-1">
        <SidebarDemo ticker={ticker}>
          <div className="flex-1 p-4 overflow-auto">
            <h2>Earnings Report Message</h2>
            {earningsMessage ? (
              <p>{earningsMessage}</p>
            ) : (
              <p>No earnings report message found.</p>
            )}
          </div>
        </SidebarDemo>
      </div>
    </div>
  );
};

export default AllMessagesDisplay;