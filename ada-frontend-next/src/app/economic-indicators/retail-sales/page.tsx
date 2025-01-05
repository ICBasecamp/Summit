"use client";

import React, { useEffect, useState } from 'react';
import { useAnalysis } from '../../context/AnalysisContext';
import { SidebarDemo } from '../../pages/SideTabsER';
import { Header } from '../../components/header';
import { Scatter } from 'react-chartjs-2';
import 'chart.js/auto';

const RetailSalesPage: React.FC<{ ticker: string }> = ({ ticker }) => {
  const analysisContext = useAnalysis();
  const { messages, setTicker } = analysisContext || {};
  const [retailSalesMessage, setRetailSalesMessage] = useState<string | null>(null);
  const [retailSalesEstimation, setRetailSalesEstimation] = useState<string | null>(null);
  const [scatterData, setScatterData] = useState<any>(null);
  const [correlations, setCorrelations] = useState<any>(null);

  useEffect(() => {
    if (ticker && setTicker) {
      setTicker(ticker);
    }
  }, [ticker, setTicker]);

  useEffect(() => {
    const retailSalesMessage = messages?.find(message => message.includes("economicIndicators:"));
    if (retailSalesMessage) {
      try {
        const parsedMessage = retailSalesMessage.replace(/'/g, '"');
        const { raw_data } = parsedMessage;

        // Extract correlation coefficients for "Retail Sales"
        const statisticalAnalysisData = retailSalesMessage.match(/"average_correlations": (\{(?:[^{}]*|\{(?:[^{}]*|\{[^{}]*\})*\})*\})/);
        console.log(statisticalAnalysisData);
        if (statisticalAnalysisData && statisticalAnalysisData[1]) {
          const correlationsData = JSON.parse(statisticalAnalysisData[1].replace(/'/g, '"'));
          const retailSalesCorrelations = {
            "Earnings Reports": correlationsData["Earnings Reports"]["Retail Sales"],
            "Stock Revenue": correlationsData["Stock Revenue"]["Retail Sales"],
            "Earnings History": correlationsData["Earnings History"]["Retail Sales"],
            "EPS Trend": correlationsData["EPS Trend"]["Retail Sales"]
          };

          // Extract scatter plot data for "Retail Sales"
          const retailSalesScatterData = raw_data["Retail Sales"];

          setCorrelations(retailSalesCorrelations);
          setScatterData(retailSalesScatterData);
        } else {
          setCorrelations(null);
          setScatterData(null);
        }
      } catch (error) {
        console.error("Failed to parse JSON:", error);
        setRetailSalesMessage(null);
        setScatterData(null);
        setCorrelations(null);
      }
    } else {
      setRetailSalesMessage(null);
      setScatterData(null);
      setCorrelations(null);
    }
  }, [messages]);

  useEffect(() => {
    const retailSalesMessage = messages?.find(message => message.includes("economicIndicators:"));
    if (retailSalesMessage) {
      const retailSalesEstimationData = retailSalesMessage.match(/\*\*Retail Sales\*\*([\s\S]*?)\*\*/);
      if (retailSalesEstimationData && retailSalesEstimationData[1]) {
        setRetailSalesEstimation(retailSalesEstimationData[1].trim());
      } else {
        setRetailSalesEstimation(null);
      }
    } else {
      setRetailSalesEstimation(null);
    }
  }, [messages]);

  const scatterPlotOptions = {
    scales: {
      x: {
        title: {
          display: true,
          text: 'Economic Indicators'
        }
      },
      y: {
        title: {
          display: true,
          text: 'Earnings Data'
        }
      }
    }
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
                    <h2 className="text-2xl font-semibold">Retail Sales Analysis</h2>
                    {retailSalesEstimation && <p>{retailSalesEstimation}</p>}
                  </div>
                </div>
              </div>
              <div className="grow w-2/5">
                <div className="flex flex-col gap-8">
                  {scatterData && (
                    <div className="flex flex-col rounded-xl bg-zinc-800 p-6 gap-2">
                      <h2 className="text-lg font-medium self-center">Retail Sales Scatter Plot</h2>
                      <Scatter
                        data={{
                          datasets: [
                            {
                              label: 'Retail Sales vs Earnings Data',
                              data: scatterData['Economic Indicators'].map((indicator: number, index: number) => ({
                                x: indicator,
                                y: scatterData['Earnings Data'][index]
                              })),
                              backgroundColor: 'rgba(75, 192, 192, 0.6)',
                              borderColor: 'rgba(75, 192, 192, 1)',
                              borderWidth: 1
                            }
                          ]
                        }}
                        options={scatterPlotOptions}
                      />
                    </div>
                  )}
                  <div className="flex flex-col rounded-xl bg-zinc-800 p-6 gap-2">
                    <h2 className="text-lg font-medium self-center">Pearson Correlation Coefficients</h2>
                    {correlations && (
                      <table className="table-auto w-full">
                        <thead>
                          <tr>
                            <th>Data Type</th>
                            <th>Retail Sales</th>
                          </tr>
                        </thead>
                        <tbody>
                          {Object.entries(correlations).map(([dataType, value]) => (
                            <tr key={dataType}>
                              <td>{dataType}</td>
                              <td>{value}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
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

export default RetailSalesPage;