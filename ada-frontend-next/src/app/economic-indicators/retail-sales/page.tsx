"use client";

import React, { useEffect, useState } from 'react';
import { useAnalysis } from '../../context/AnalysisContext';
import { SidebarDemo } from '../../pages/SideTabsEI';
import { Header } from '../../components/header';
import { Scatter } from 'react-chartjs-2';
import 'chart.js/auto';
import { Chart, registerables } from 'chart.js';
import { Line } from 'react-chartjs-2';

Chart.register(...registerables);

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
        const parsedMessage = retailSalesMessage.replace(/'/g, '"').replace(/\s+/g, ' ');
        console.log(parsedMessage);
        const raw_data = parsedMessage;

        // Extract correlation coefficients for "Retail Sales"
        const statisticalAnalysisData = retailSalesMessage.match(/"average_correlations": (\{(?:[^{}]*|\{(?:[^{}]*|\{[^{}]*\})*\})*\})/);
        if (statisticalAnalysisData && statisticalAnalysisData[1]) {
          const correlationsData = JSON.parse(statisticalAnalysisData[1].replace(/'/g, '"').replace(/\s+/g, ' '));
          
          const retailSalesCorrelations = {
            "Earnings Reports": parseFloat(correlationsData["Earnings Reports"]["Retail Sales"].toFixed(3)),
            "Stock Revenue": parseFloat(correlationsData["Stock Revenue"]["Retail Sales"].toFixed(3)),
            "Earnings History": parseFloat(correlationsData["Earnings History"]["Retail Sales"].toFixed(3)),
            "EPS Trend": parseFloat(correlationsData["EPS Trend"]["Retail Sales"].toFixed(3))
          };

          setCorrelations(retailSalesCorrelations);

          // Extract scatter plot data for "Retail Sales"
          const retailSalesScatterDataMatch = parsedMessage.match(/"Retail Sales":\s*\{[^}]*"Earnings Data":\s*array\(([^)]*)\),\s*"Economic Indicators":\s*array\(([^)]*)\)/);
          if (retailSalesScatterDataMatch) {
            const earningsData = retailSalesScatterDataMatch[1].replace(/[\[\]\s]/g, '').split(',').map(value => parseFloat(value));
            const economicIndicators = retailSalesScatterDataMatch[2].replace(/[\[\]\s]/g, '').split(',').map(value => parseFloat(value));

            // Normalize the data
            const normalize = (data: number[]) => {
              const max = Math.max(...data);
              const min = Math.min(...data);
              return data.map(value => (value - min) / (max - min));
            };

            const normalizedEarningsData = normalize(earningsData);
            const normalizedEconomicIndicators = normalize(economicIndicators);

            const retailSalesScatterData = {
              'Economic Indicators': normalizedEconomicIndicators,
              'Earnings Data': normalizedEarningsData
            };

            setScatterData(retailSalesScatterData);
          }
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
      const retailSalesEstimationData = retailSalesMessage.match(/\*\*Retail Sales\*\*:([\s\S]*?)\*\*/);
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
    },
    plugins: {
      legend: {
        display: false
      }
    }
  };

  const calculateLineOfBestFit = (xData: number[], yData: number[]) => {
    const n = xData.length;
    const sumX = xData.reduce((a, b) => a + b, 0);
    const sumY = yData.reduce((a, b) => a + b, 0);
    const sumXY = xData.reduce((sum, x, i) => sum + x * yData[i], 0);
    const sumX2 = xData.reduce((sum, x) => sum + x * x, 0);

    const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
    const intercept = (sumY - slope * sumX) / n;

    const lineData = xData.map(x => ({ x, y: slope * x + intercept }));
    return lineData;
  };

  const lineOfBestFit = scatterData ? calculateLineOfBestFit(scatterData['Economic Indicators'], scatterData['Earnings Data']) : [];

  return (
    <div className="flex flex-col bg-neutral-900 w-full h-screen">
      <Header />
      <div className="flex flex-1">
        <SidebarDemo>
          <div className="flex flex-col px-8 pt-2 pb-8">
            <div className="flex justify-between gap-12">
              <div className="grow w-1/2">
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
                            },
                            {
                              label: 'Line of Best Fit',
                              data: lineOfBestFit,
                              type: 'line',
                              fill: false,
                              borderColor: 'rgba(75, 192, 192, 1)',
                              borderWidth: 2,
                              pointRadius: 0
                            }
                          ]
                        }}
                        options={scatterPlotOptions}
                        height={500}
                        width={800}
                      />
                    </div>
                  )}
                </div>
              </div>
              <div className="grow w-1/3">
                <div className="flex flex-col gap-8">
                  <div className="flex flex-col rounded-xl bg-zinc-800 p-6 gap-2">
                    <h2 className="text-lg font-medium self-center">Retail Sales Analysis</h2>
                    {retailSalesEstimation && <p>{retailSalesEstimation}</p>}
                  </div>
                  <div className="flex flex-col rounded-xl bg-zinc-800 p-6 gap-2">
                    <h2 className="text-lg font-medium self-center">Pearson Correlation Coefficients</h2>
                    {correlations && (
                      <table className="table-auto w-full">
                        <thead>
                          <tr>
                            <th className="text-left">Data Type</th>
                            <th className="text-left">Retail Sales</th>
                          </tr>
                        </thead>
                        <tbody>
                          {Object.entries(correlations).map(([dataType, value]) => (
                            <tr key={dataType}>
                              <td>{dataType}</td>
                              <td>{value}%</td>
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