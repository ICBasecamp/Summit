"use client";

import React, { useEffect, useState } from 'react';
import { useAnalysis } from '../../context/AnalysisContext';
import { SidebarDemo } from '../../pages/SideTabsER';
import Header from '../../components/header';
import { Calendar } from 'react-calendar';
import 'react-calendar/dist/Calendar.css';
import './CalendarStyles.css';

const FinancialStatsPage: React.FC<{ ticker: string }> = ({ ticker }) => {
  const analysisContext = useAnalysis();
  const { messages, setTicker } = analysisContext || {};
  const [financialStats, setFinancialStats] = useState<any>(null);
  const [nlpAnalysis, setNlpAnalysis] = useState<string>('');
  const [earningsDate, setEarningsDate] = useState<Date | null>(null);
  const [daysTillEarnings, setDaysTillEarnings] = useState<number | null>(null);

  useEffect(() => {
    if (ticker && setTicker) {
      setTicker(ticker);
    }
  }, [ticker, setTicker]);

  useEffect(() => {
    const earningsReportMessage = messages?.find(message => message.includes("earnings:"));
    if (earningsReportMessage) {
      const financialStatsMatch = earningsReportMessage.match(/financial_stats: (\{(?:[^{}]*|\{(?:[^{}]*|\{[^{}]*\})*\})*\})/);
      if (financialStatsMatch && financialStatsMatch[1]) {
        let jsonString = financialStatsMatch[1];
        jsonString = jsonString.replace(/'/g, '"');
        try {
          const parsedData = JSON.parse(jsonString);
          setFinancialStats(parsedData);
          const earningsDateString = parsedData['Earnings Date'];
          const earningsDate = new Date(earningsDateString.split(' - ')[0]);
          setEarningsDate(earningsDate);
          const today = new Date();
          const timeDiff = earningsDate.getTime() - today.getTime();
          const daysDiff = Math.ceil(timeDiff / (1000 * 3600 * 24));
          setDaysTillEarnings(daysDiff);
        } catch (error) {
          console.error("Failed to parse JSON:", error);
        }
      }

      const nlpAnalysisMatch = earningsReportMessage.match(/Financial Estimate\*\* (.*?) financial_stats:/);
      if (nlpAnalysisMatch && nlpAnalysisMatch[1]) {
        setNlpAnalysis(nlpAnalysisMatch[1].trim());
      }
    }
  }, [messages]);

  if (!financialStats) {
    return <div>Loading...</div>;
  }

  return (
    <div className="flex flex-col bg-neutral-900 w-full h-screen">
      <Header />
      <div className="flex flex-1">
        <SidebarDemo>
          <div className="flex flex-col px-8 pt-2 pb-8">
            <div className="flex justify-between gap-12">
              <div className="grow w-3/5">
                <div className="flex flex-col">
                  <div className="flex flex-col rounded-xl bg-zinc-800 p-8 items-center gap-8">
                    <h2 className="text-2xl font-semibold">Earnings Date: {earningsDate?.toLocaleDateString()}</h2>
                    {earningsDate && (
                      <div className="flex flex-col items-center">
                        <Calendar
                          value={earningsDate}
                          tileClassName={({ date, view }) =>
                            view === 'month' && date.getTime() === earningsDate.getTime() ? 'highlight' : null
                          }
                          className="big-calendar"
                        />
                        <p className="text-lg font-medium mt-4">{daysTillEarnings} days till earnings</p>
                      </div>
                    )}
                  </div>
                </div>
              </div>
              <div className="grow w-2/5">
                <div className="flex flex-col gap-8">
                  <div className="flex flex-col rounded-xl bg-zinc-800 p-6 gap-2">
                    <h2 className="text-lg font-medium self-center">Financial Analysis</h2>
                    <p>{nlpAnalysis}</p>
                  </div>
                  <div className="flex flex-col rounded-xl bg-zinc-800 p-6 gap-2">
                    <h2 className="text-lg font-medium self-center">Financial Stats</h2>
                    <ul>
                      {Object.entries(financialStats).map(([key, value]) => (
                        <li key={key}>
                          <strong>{key}:</strong> {value}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </SidebarDemo>
      </div>
    </div>
  );
};

export default FinancialStatsPage;