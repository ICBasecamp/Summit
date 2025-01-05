"use client";

import React, { useEffect, useState } from 'react';
import { useAnalysis } from '../../context/AnalysisContext';
import { SidebarDemo } from '../../pages/SideTabsER';
import { Header } from '../../components/header';
import { Bar } from 'react-chartjs-2';
import 'chart.js/auto';

const AllMessagesDisplay: React.FC<{ ticker: string }> = ({ ticker }) => {
  const analysisContext = useAnalysis();
  const { messages, setTicker } = analysisContext || {};
  const [earningsMessage, setEarningsMessage] = useState<string | null>(null);
  const [earningsEstimation, setEarningsEstimation] = useState<string | null>(null);
  const [featureImportances, setFeatureImportances] = useState<any>(null);
  const [pcaValues, setPcaValues] = useState<any>(null);
  
  useEffect(() => {
    if (ticker && setTicker) {
      setTicker(ticker);
    }
  }, [ticker, setTicker]);
  
  useEffect(() => {
    const earningsReportMessage = messages?.find(message => message.includes("earnings:"));
    if (earningsReportMessage) {
      const revenueDataMatch = earningsReportMessage.match(/'name': 'revenue_df', 'random_forest_importances': (\{(?:[^{}]*|\{(?:[^{}]*|\{[^{}]*\})*\})*\}), 'pca_components': (\{(?:[^{}]*|\{(?:[^{}]*|\{[^{}]*\})*\})*\})/);
      if (revenueDataMatch && revenueDataMatch[1] && revenueDataMatch[2]) {
        try {
          let rfJsonString = revenueDataMatch[1].replace(/'/g, '"');
          let pcaJsonString = revenueDataMatch[2].replace(/'/g, '"');
          const rfParsedData = JSON.parse(rfJsonString);
          const pcaParsedData = JSON.parse(pcaJsonString);
          setFeatureImportances(rfParsedData.Importance);
          setPcaValues(pcaParsedData);
          setEarningsMessage(`${rfJsonString.trim()} ${pcaJsonString.trim()}`);
        } catch (error) {
          console.error("Failed to parse JSON:", error);
          setEarningsMessage(null);
          setFeatureImportances(null);
          setPcaValues(null);
        }
      } else {
        setEarningsMessage(null);
        setFeatureImportances(null);
        setPcaValues(null);
      }
    } else {
      setEarningsMessage(null);
      setFeatureImportances(null);
      setPcaValues(null);
    }
  }, [messages]);

  useEffect(() => {
    const earningsReportMessage = messages?.find(message => message.includes("earnings:"));
    if (earningsReportMessage) {
      const earningsEstimationData = earningsReportMessage.match(/\*\*Revenue Estimate\*\*([\s\S]*?)\*\*/);
      if (earningsEstimationData && earningsEstimationData[1]) {
        setEarningsEstimation(earningsEstimationData[1].trim());
      } else {
        setEarningsEstimation(null);
      }
    } else {
      setEarningsEstimation(null);
    }
  }, [messages]);

  const featureImportanceData = {
    labels: featureImportances ? Object.keys(featureImportances) : [],
    datasets: [
      {
        label: 'Feature Importance',
        data: featureImportances ? Object.values(featureImportances).map((value: number) => parseFloat(value.toFixed(2))) : [],
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
      },
    ],
  };

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
                    <h2 className="text-2xl font-semibold">Feature Importances</h2>
                    <Bar data={featureImportanceData} />
                  </div>
                </div>
              </div>
              <div className="grow w-2/5">
                <div className="flex flex-col gap-8">
                  <div className="flex flex-col rounded-xl bg-zinc-800 p-6 gap-2">
                    <h2 className="text-lg font-medium self-center">Revenue Analysis</h2>
                    {earningsEstimation ? (
                      <p>{earningsEstimation}</p>
                    ) : (
                      <p>No earnings estimation found.</p>
                    )}
                  </div>
                  <div className="flex flex-col rounded-xl bg-zinc-800 p-6 gap-2">
                    <h2 className="text-lg font-medium self-center">Feature Importances Values</h2>
                    {featureImportances ? (
                      <ul>
                        {Object.entries(featureImportances).map(([key, value]) => (
                          <li key={key}>{`${key}: ${parseFloat((value as number).toFixed(2))}`}</li>
                        ))}
                      </ul>
                    ) : (
                      <p>No feature importances found.</p>
                    )}
                  </div>
                  <div className="flex flex-col rounded-xl bg-zinc-800 p-6 gap-2">
                    <h2 className="text-lg font-medium self-center">PCA Values</h2>
                    {pcaValues ? (
                      <div className="flex justify-between">
                        {Object.entries(pcaValues).map(([key, value]) => (
                          <div key={key} className="flex flex-col items-center">
                            <h3 className="text-md font-medium">{key}</h3>
                            {Object.entries(value as { [key: string]: number }).map(([subKey, subValue]) => (
                              <div key={subKey}>{`${subKey}: ${parseFloat(subValue.toFixed(2))}`}</div>
                            ))}
                          </div>
                        ))}
                      </div>
                    ) : (
                      <p>No PCA values found.</p>
                    )}
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

export default AllMessagesDisplay;