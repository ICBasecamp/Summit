"use client";

// filepath: /c:/Users/Samuil Georgiev/Projects/ADA/ada-frontend-next/src/app/social-media/page.tsx

import React, { useEffect, useState } from 'react';
import { useAnalysis } from '../context/AnalysisContext';
import { Header } from '@/app/components/header';
import { CircularProgress } from '@/app/components/circular-progress';
import { useCountUp } from 'use-count-up';
import * as Tooltip from '@radix-ui/react-tooltip';
import { geistSans, openSans } from '@/app/layout';

const SocialMediaPage: React.FC<{ ticker: string }> = ({ ticker }) => {
    const analysisContext = useAnalysis();
    const { messages, setTicker } = analysisContext || {};
    const [socialMediaData, setSocialMediaData] = useState<any>(null);
    const [positiveInsights, setPositiveInsights] = useState<string | null>(null);
    const [neutralInsights, setNeutralInsights] = useState<string | null>(null);
    const [negativeInsights, setNegativeInsights] = useState<string | null>(null);
    const [overallSentiment, setOverallSentiment] = useState<number | null>(null);

    useEffect(() => {
        if (ticker && setTicker) {
            setTicker(ticker);
        }
    }, [ticker, setTicker]);

    useEffect(() => {
        const socialMediaMessage = messages?.find(message => message.includes("socialMedia:"));
        if (socialMediaMessage) {
            try {
                const parsedMessage = socialMediaMessage.replace(/'/g, '"').replace(/\s+/g, ' ');

                const positiveSentimentMatch = parsedMessage.match(/Positive Sentiment: (\d+\.\d+)%/);
                const neutralSentimentMatch = parsedMessage.match(/Neutral Sentiment: (\d+\.\d+)%/);
                const negativeSentimentMatch = parsedMessage.match(/Negative Sentiment: (\d+\.\d+)%/);
                const overallSentimentMatch = parsedMessage.match(/Overall Sentiment: (\d+\.\d+)%/);

                const positiveInsightsMatch = parsedMessage.match(/Positive Posts Insights:\s*(.*?)\s*Neutral Posts Insights:/s);
                const neutralInsightsMatch = parsedMessage.match(/Neutral Posts Insights:\s*(.*?)\s*Negative Posts Insights:/s);
                const negativeInsightsMatch = parsedMessage.match(/Negative Posts Insights:\s*(.*)/s);

                setOverallSentiment(overallSentimentMatch ? parseFloat(overallSentimentMatch[1]) : null);
                setPositiveInsights(positiveInsightsMatch ? positiveInsightsMatch[1].trim() : null);
                setNeutralInsights(neutralInsightsMatch ? neutralInsightsMatch[1].trim() : null);
                setNegativeInsights(negativeInsightsMatch ? negativeInsightsMatch[1].trim() : null);

                setSocialMediaData({
                    positive: positiveSentimentMatch ? parseFloat(positiveSentimentMatch[1]) : null,
                    neutral: neutralSentimentMatch ? parseFloat(neutralSentimentMatch[1]) : null,
                    negative: negativeSentimentMatch ? parseFloat(negativeSentimentMatch[1]) : null,
                });
            } catch (error) {
                console.error("Failed to parse JSON:", error);
                setSocialMediaData(null);
            }
        } else {
            setSocialMediaData(null);
        }
    }, [messages]);

    const { value, reset } = useCountUp({
        isCounting: true,
        duration: 1,
        start: 0,
        end: overallSentiment || 0,
    });

    let sentimentColour = 'text-violet-400';

    if (overallSentiment !== null) {
        if (overallSentiment < 33.00) {
            sentimentColour = 'text-red-500';
        } else if (overallSentiment > 77.00) {
            sentimentColour = 'text-emerald-400';
        }
        else
        {
            sentimentColour = 'text-yellow-400';
        }
    }

    if (!socialMediaData) {
        return <div>Loading...</div>;
    }

    return (
        <div className="flex flex-col bg-neutral-900 w-full h-screen">
            <Header />
            <div className="flex flex-col px-8 pt-2 pb-8">
                <div className="flex justify-between gap-12">
                    <div className="grow w-3/5">
                        <div className="flex flex-col">
                            <div className="flex flex-col rounded-xl bg-zinc-800 p-8 items-center gap-8">
                                <p className={`text-2xl font-semibold ${openSans.className}`}>Overall Sentiment Score</p>
                                <CircularProgress value={value} className="size-52" colour={sentimentColour} />
                                <p className="text-lg">Overall sentiment score based on social media posts.</p>
                            </div>
                        </div>
                    </div>
                    <div className="grow w-2/5">
                        <div className="flex flex-col gap-8">
                            <div className="flex flex-col rounded-xl bg-zinc-800 p-6 gap-2 overflow-y-auto max-h-48">
                                <h2 className="text-lg font-medium self-center text-emerald-400">Positive Sentiments</h2>
                                <p>{positiveInsights}</p>
                            </div>
                            <div className="flex flex-col rounded-xl bg-zinc-800 p-6 gap-2 overflow-y-auto max-h-48">
                                <h2 className="text-lg font-medium self-center text-white">Neutral Sentiments</h2>
                                <p>{neutralInsights}</p>
                            </div>
                            <div className="flex flex-col rounded-xl bg-zinc-800 p-6 gap-2 overflow-y-auto max-h-48">
                                <h2 className="text-lg font-medium self-center text-red-500">Negative Sentiments</h2>
                                <p>{negativeInsights}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default SocialMediaPage;