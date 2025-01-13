"use client";

import React, { useEffect, useState } from 'react';
import { useAnalysis } from '../../context/AnalysisContext';
import { SidebarDemo } from '../../pages/SideTabsER';
import { Header } from '../../components/header';
import { Bar, Line } from 'react-chartjs-2';
import 'chart.js/auto';

const AnalystPage: React.FC<{ ticker: string }> = ({ ticker }) => {
  const analysisContext = useAnalysis();
  const { messages, setTicker } = analysisContext || {};
  const [rawData, setRawData] = useState<any>(null);
  const [nlpAnalysis, setNlpAnalysis] = useState<string>('');

  useEffect(() => {
    if (ticker && setTicker) {
      setTicker(ticker);
    }
  }, [ticker, setTicker]);

  useEffect(() => {
    const earningsReportMessage = messages?.find(message => message.includes("earnings:"));
    if (earningsReportMessage) {
      // Extract non_statistical_analysis
      const nonStatisticalAnalysisMatch = earningsReportMessage.match(/non_statistical_analysis: (\{(?:[^{}]*|\{(?:[^{}]*|\{[^{}]*\})*\})*\})/);
      if (nonStatisticalAnalysisMatch && nonStatisticalAnalysisMatch[1]) {
        let jsonString = nonStatisticalAnalysisMatch[1];
        jsonString = jsonString.replace(/'/g, '"');
        jsonString = jsonString.replace(/nan/g, 'null'); // Replace NaN with null
        console.log("JSON String:", jsonString); // Log the JSON string
        // Convert numeric keys to string keys for margins, quarterly_growth_rates, and price_gap
        jsonString = jsonString.replace(/"Quarter":\s*\{([^}]*)\}/g, (match, p1) => {
            const updated = p1.replace(/(\d+):/g, '"$1":');
            return `"Quarter": {${updated}}`;
          });
          jsonString = jsonString.replace(/"Margin":\s*\{([^}]*)\}/g, (match, p1) => {
            const updated = p1.replace(/(\d+):/g, '"$1":');
            return `"Margin": {${updated}}`;
          });
          jsonString = jsonString.replace(/"Revenue Growth":\s*\{([^}]*)\}/g, (match, p1) => {
            const updated = p1.replace(/(\d+):/g, '"$1":');
            return `"Revenue Growth": {${updated}}`;
          });
          jsonString = jsonString.replace(/"Earnings Growth":\s*\{([^}]*)\}/g, (match, p1) => {
            const updated = p1.replace(/(\d+):/g, '"$1":');
            return `"Earnings Growth": {${updated}}`;
          });
          jsonString = jsonString.replace(/"Current Price":\s*\{([^}]*)\}/g, (match, p1) => {
            const updated = p1.replace(/(\d+):/g, '"$1":');
            return `"Current Price": {${updated}}`;
          });
          jsonString = jsonString.replace(/"Average Price":\s*\{([^}]*)\}/g, (match, p1) => {
            const updated = p1.replace(/(\d+):/g, '"$1":');
            return `"Average Price": {${updated}}`;
          });
          jsonString = jsonString.replace(/"Price Gap \(%\)":\s*\{([^}]*)\}/g, (match, p1) => {
            const updated = p1.replace(/(\d+):/g, '"$1":');
            return `"Price Gap (%)": {${updated}}`;
          });
        try {
          setRawData(JSON.parse(jsonString));
        } catch (error) {
          console.error("Failed to parse JSON:", error);
        }
      }

      // Extract Analyst NLP
      const nlpAnalysisMatch = earningsReportMessage.match(/\*\*Non-Statistical Estimate\*\*([\s\S]*?)\*\*Financial Estimate\*\*/);
      if (nlpAnalysisMatch && nlpAnalysisMatch[1]) {
        setNlpAnalysis(nlpAnalysisMatch[1].trim());
      }
    }
  }, [messages]);

  if (!rawData) {
    return <div>Loading...</div>;
  }

  const averageScoresData = {
    labels: Object.keys(rawData.average_scores_by_rating['Overall Score']),
    datasets: [
      {
        label: 'Overall Score',
        data: Object.values(rawData.average_scores_by_rating['Overall Score']),
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
      },
      {
        label: 'Direction Score',
        data: Object.values(rawData.average_scores_by_rating['Direction Score']),
        backgroundColor: 'rgba(192, 75, 75, 0.6)',
        borderColor: 'rgba(192, 75, 75, 1)',
        borderWidth: 1,
      }
    ],
  };

  // Adjust the time series analysis to scale the overall score
  const overallScores = Object.values(rawData.time_series_analysis['Overall Score']);
  const priceTargets = Object.values(rawData.time_series_analysis['Price Target']);
  const averagePriceTarget = priceTargets.reduce((sum, value) => sum + value, 0) / priceTargets.length;
  const adjustedOverallScores = overallScores.map(score => score + averagePriceTarget);
  const labels = Object.keys(rawData.time_series_analysis['Overall Score']);

  // Filter out missing values and scale the overall score
  const filteredData = labels.reduce((acc, label, index) => {
    if (adjustedOverallScores[index] !== null && priceTargets[index] !== null) {
      acc.labels.push(label);
      acc.overallScores.push(adjustedOverallScores[index] / 4); // Scale down overall scores to match price target scale
      acc.priceTargets.push(priceTargets[index]);
    }
    return acc;
  }, { labels: [], overallScores: [], priceTargets: [] });

  const timeSeriesData = {
    labels: filteredData.labels,
    datasets: [
      {
        label: 'Price Target',
        data: filteredData.priceTargets,
        fill: false,
        borderColor: 'rgba(192, 75, 75, 1)',
        tension: 0.1,
      },
    ],
  };

  return (
    <div className="flex flex-col bg-neutral-900 w-full h-screen">
      <Header />
      <div className="flex flex-1">
        <SidebarDemo>
          <div className="flex flex-col px-8 pt-2 pb-8">
            <div className="flex flex-row gap-12">
              <div className="flex flex-col flex-1 gap-12">
                <div className="flex flex-col rounded-xl bg-zinc-800 p-6 gap-2">
                  <h2 className="text-lg font-medium self-center">Analyst Ratings</h2>
                  <Bar data={averageScoresData} />
                </div>
              </div>
              <div className="flex flex-col flex-1 gap-12">
                <div className="flex flex-col rounded-xl bg-zinc-800 p-6 gap-2">
                  <h2 className="text-lg font-medium self-center">Analyst Analysis</h2>
                  <p>{nlpAnalysis}</p>
                </div>
                <div className="flex flex-col rounded-xl bg-zinc-800 p-6 gap-2">
                  <h2 className="text-lg font-medium self-center">Time Series Analysis</h2>
                  <Line data={timeSeriesData} />
                </div>
              </div>
            </div>
          </div>
        </SidebarDemo>
      </div>
    </div>
  );
};

export default AnalystPage;