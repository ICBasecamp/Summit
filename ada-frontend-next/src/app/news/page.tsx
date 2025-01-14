"use client";

import React, { useEffect, useState } from 'react';
import { useAnalysis } from '../context/AnalysisContext';
import Header from '@/app/components/header';
import { CircularProgress } from '@/app/components/circular-progress';
import { ChevronLeftIcon, ChevronRightIcon } from 'lucide-react';
import { openSans } from '@/app/layout';

const NewsPage: React.FC<{ ticker: string }> = ({ ticker }) => {
  const analysisContext = useAnalysis();
  const { messages, setTicker } = analysisContext || {};
  const [newsData, setNewsData] = useState<any[]>([]);
  const [averageSentiment, setAverageSentiment] = useState<number>(0);
  const [highestSentences, setHighestSentences] = useState<any[]>([]);
  const [lowestSentences, setLowestSentences] = useState<any[]>([]);
  const [summaries, setSummaries] = useState<any[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isAnimating, setIsAnimating] = useState(false);
  const [direction, setDirection] = useState('next');
  const [nextIndex, setNextIndex] = useState(0);

  useEffect(() => {
    if (ticker && setTicker) {
      setTicker(ticker);
    }
  }, [ticker, setTicker]);

  useEffect(() => {
    const newsMessage = messages?.find(message => message.includes("newsSentiments:"));
    if (newsMessage) {
      try {
        const parsedMessage = newsMessage.replace(/'/g, '"').replace(/\s+/g, ' ');
        const regex = /{"sentence":\s*"(.*?)",\s*"sentiment_score":\s*np\.float32\((.*?)\)}/g;
        const matches = [...parsedMessage.matchAll(regex)];
        const newsItems = matches.map(match => ({
          sentence: match[1],
          sentiment_score: parseFloat(match[2])
        }));
        setNewsData(newsItems);

        // Calculate average sentiment score
        const totalSentiment = newsItems.reduce((acc, item) => acc + item.sentiment_score, 0);
        setAverageSentiment(totalSentiment / newsItems.length);

        // Sort sentences by sentiment score
        const sortedBySentiment = [...newsItems].sort((a, b) => b.sentiment_score - a.sentiment_score);
        setHighestSentences(sortedBySentiment.slice(0, 5));
        setLowestSentences(sortedBySentiment.slice(-5).reverse());
      } catch (error) {
        console.error("Failed to parse JSON:", error);
        setNewsData([]);
      }
    } else {
      setNewsData([]);
    }
  }, [messages]);

  useEffect(() => {
    const newsSummariesMessage = messages?.find(message => message.includes("newsSummaries:"));
    if (newsSummariesMessage) {
      try {
        const positiveSummaryMatch = newsSummariesMessage.match(/positive_summary:\s*(.*?)\s*neutral_summary:/s);
        const neutralSummaryMatch = newsSummariesMessage.match(/neutral_summary:\s*(.*?)\s*negative_summary:/s);
        const negativeSummaryMatch = newsSummariesMessage.match(/negative_summary:\s*(.*)/s);

        const positiveSummary = positiveSummaryMatch ? positiveSummaryMatch[1].trim() : '';
        const neutralSummary = neutralSummaryMatch ? neutralSummaryMatch[1].trim() : '';
        const negativeSummary = negativeSummaryMatch ? negativeSummaryMatch[1].trim() : '';

        setSummaries([
          {
            title: 'Positive Summary',
            content: positiveSummary,
            color: 'text-emerald-400',
          },
          {
            title: 'Neutral Summary',
            content: neutralSummary,
            color: 'text-yellow-400',
          },
          {
            title: 'Negative Summary',
            content: negativeSummary,
            color: 'text-red-500',
          },
        ]);
      } catch (error) {
        console.error("Failed to parse news summaries:", error);
      }
    }
  }, [messages]);

  useEffect(() => {
    if (isAnimating) {
      const timeout = setTimeout(() => {
        setCurrentIndex(nextIndex);
        setIsAnimating(false);
      }, 300); // Duration of the animation

      return () => clearTimeout(timeout);
    }
  }, [isAnimating, nextIndex]);

  const nextSlide = () => {
    setDirection('prev');
    setNextIndex((currentIndex - 1 + summaries.length) % summaries.length);
    setIsAnimating(true);
  };

  const previousSlide = () => {
    setDirection('next');
    setNextIndex((currentIndex + 1) % summaries.length);
    setIsAnimating(true);
  };

  const sentimentColour = averageSentiment > 0.5 ? 'text-emerald-400' : 'text-red-500';
  const value = (averageSentiment * 100).toFixed(2);

  return (
    <div className="flex flex-col bg-neutral-900 w-full h-screen">
      <Header />
      <div className="flex flex-col px-8 pt-2 pb-8 h-full">
        <div className="flex justify-between gap-12 h-full">
          <div className="grow w-2/5 flex flex-col gap-6">
            <div className="w-full flex flex-col rounded-xl bg-zinc-800 p-8 items-center gap-8">
              <p className={`text-2xl font-medium ${openSans.className}`}>Average Sentiment Score</p>
              <CircularProgress value={value} className="size-52" colour={sentimentColour} />
              <p className="text-lg">Average sentiment score across <span className="font-bold">{newsData.length}</span> sentences scraped.</p>
            </div>
            <div className="h-1/2 relative overflow-hidden">
              <div className="absolute inset-0 flex flex-col rounded-xl bg-zinc-800 p-8 gap-4 h-full w-full overflow-y-auto">
                <div className="flex justify-between items-center">
                  <p className={`text-2xl font-medium ${summaries[currentIndex]?.color} ${openSans.className}`}>
                    {summaries[currentIndex]?.title}
                  </p>
                  <div className="flex gap-2">
                    <button
                      onClick={nextSlide}
                      className="p-2 rounded-full hover:bg-zinc-700"
                    >
                      <ChevronLeftIcon className="h-5 w-5" />
                    </button>
                    <button
                      onClick={previousSlide}
                      className="p-2 rounded-full hover:bg-zinc-700"
                    >
                      <ChevronRightIcon className="h-5 w-5" />
                    </button>
                  </div>
                </div>
                <div className="relative flex-1 overflow-y-auto no-scrollbar">
                  <div className={`absolute inset-0 transition-transform duration-300 ${isAnimating ? (direction === 'next' ? 'animate-swipe-out-left' : 'animate-swipe-out-right') : ''}`}>
                    <p className="text-sm text-neutral-300">
                      {summaries[currentIndex]?.content}
                    </p>
                  </div>
                  <div className={`absolute inset-0 transition-transform duration-300 ${isAnimating ? (direction === 'next' ? 'animate-swipe-in-right' : 'animate-swipe-in-left') : ''}`}>
                    <p className="text-sm text-neutral-300">
                      {summaries[nextIndex]?.content}
                    </p>
                  </div>
                </div>
                <div className="flex justify-center gap-2">
                  {summaries.map((_, index) => (
                    <div
                      key={index}
                      className={`h-2 w-2 rounded-full ${index === currentIndex ? 'bg-white' : 'bg-zinc-600'}`}
                    />
                  ))}
                </div>
              </div>
            </div>
          </div>
          <div className="grow w-3/5 flex flex-col gap-6">
            <div className="flex flex-col rounded-xl bg-zinc-800 p-6 gap-2">
              <h2 className="text-lg font-medium self-center text-green-500">Top Positive Sentiments</h2>
              {highestSentences.map((sentence: any, index: number) => (
                <div key={index} className="flex items-center justify-between">
                  <p className="text-sm">{sentence.sentence}</p>
                  <p className="text-sm font-bold text-green-500">{(sentence.sentiment_score * 100).toFixed(2)}%</p>
                </div>
              ))}
            </div>
            <div className="flex flex-col rounded-xl bg-zinc-800 p-6 gap-2">
              <h2 className="text-lg font-medium self-center text-red-500">Top Negative Sentiments</h2>
              {lowestSentences.map((sentence: any, index: number) => (
                <div key={index} className="flex items-center justify-between">
                  <p className="text-sm">{sentence.sentence}</p>
                  <p className="text-sm font-bold text-red-500">{(sentence.sentiment_score * 100).toFixed(2)}%</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
  
      <style jsx>{`
        @keyframes swipe-out-left {
          from { transform: translateX(0); }
          to { transform: translateX(-100%); }
        }
        @keyframes swipe-out-right {
          from { transform: translateX(0); }
          to { transform: translateX(100%); }
        }
        @keyframes swipe-in-left {
          from { transform: translateX(-100%); }
          to { transform: translateX(0); }
        }
        @keyframes swipe-in-right {
          from { transform: translateX(100%); }
          to { transform: translateX(0); }
        }
        .animate-swipe-out-left {
          animation: swipe-out-left 0.3s forwards;
        }
        .animate-swipe-out-right {
          animation: swipe-out-right 0.3s forwards;
        }
        .animate-swipe-in-left {
          animation: swipe-in-left 0.3s forwards;
        }
        .animate-swipe-in-right {
          animation: swipe-in-right 0.3s forwards;
        }
        .no-scrollbar::-webkit-scrollbar {
          display: none;
        }
        .no-scrollbar {
          -ms-overflow-style: none;
          scrollbar-width: none;
        }
      `}</style>
    </div>
  );
};

export default NewsPage;