"use client";

import React, { useEffect, useState } from 'react';
import { useAnalysis } from '../context/AnalysisContext';
import { Header } from '@/app/components/header';
import { ProgressBar } from '@/app/components/progress-bar';
import { useCountUp } from 'use-count-up';
import { openSans } from '@/app/layout';
import { ChevronLeftIcon, ChevronRightIcon } from 'lucide-react';

const BlueskyEmbed = ({ uri, cid }: { uri: string, cid: string }) => {
    return (
        <div>
            <blockquote className="bluesky-embed" data-bluesky-uri={uri} data-bluesky-cid={cid}></blockquote>
            <script async src="https://embed.bsky.app/static/embed.js" charSet="utf-8"></script>
        </div>
    );
};

const SocialMediaPage: React.FC<{ ticker: string }> = ({ ticker }) => {
    const analysisContext = useAnalysis();
    const { messages, setTicker } = analysisContext || {};
    const [socialMediaData, setSocialMediaData] = useState<any>(null);
    const [positiveInsights, setPositiveInsights] = useState<string | null>(null);
    const [neutralInsights, setNeutralInsights] = useState<string | null>(null);
    const [negativeInsights, setNegativeInsights] = useState<string | null>(null);
    const [overallSentiment, setOverallSentiment] = useState<number | null>(null);
    const [rawBlueskyPosts, setRawBlueskyPosts] = useState<any[]>([]);

    const [blueskyEmbeddings, setBlueskyEmbeddings] = useState<any[]>([]);

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

                const rawBlueskyPostsMatch = parsedMessage.match(/rawBlueskyPosts:\s*\[(.*?)\]/s);
                const rawBlueskyPosts = rawBlueskyPostsMatch ? JSON.parse(`[${rawBlueskyPostsMatch[1]}]`) : [];

                const bskyEmbeddingsMatch = parsedMessage.match(/<bsky_embeddings>(.*?)<\/bsky_embeddings>/s);
                const blueskyEmbeddings = bskyEmbeddingsMatch ? JSON.parse(bskyEmbeddingsMatch[1]) : [];
                setBlueskyEmbeddings(blueskyEmbeddings);

                setOverallSentiment(overallSentimentMatch ? parseFloat(overallSentimentMatch[1]) : null);
                setPositiveInsights(positiveInsightsMatch ? positiveInsightsMatch[1].trim() : null);
                setNeutralInsights(neutralInsightsMatch ? neutralInsightsMatch[1].trim() : null);
                setNegativeInsights(negativeInsightsMatch ? negativeInsightsMatch[1].trim() : null);

                setSocialMediaData({
                    positive: positiveSentimentMatch ? parseFloat(positiveSentimentMatch[1]) : null,
                    neutral: neutralSentimentMatch ? parseFloat(neutralSentimentMatch[1]) : null,
                    negative: negativeSentimentMatch ? parseFloat(negativeSentimentMatch[1]) : null,
                });

                setRawBlueskyPosts(rawBlueskyPosts);
            } catch (error) {
                console.error("Failed to parse JSON:", error);
                setSocialMediaData(null);
            }
        } else {
            setSocialMediaData(null);
        }
    }, [messages]);

    const summaries = [
        {
            title: 'Positive Summary',
            content: positiveInsights,
            color: 'text-emerald-400',
        },
        {
            title: 'Neutral Summary',
            content: neutralInsights,
            color: 'text-yellow-400',
        },
        {
            title: 'Negative Summary',
            content: negativeInsights,
            color: 'text-red-500',
        },
    ];

    const [currentIndex, setCurrentIndex] = useState(0);
    const [isAnimating, setIsAnimating] = useState(false);
    const [direction, setDirection] = useState('next');
    const [nextIndex, setNextIndex] = useState(0);
    const [isClient, setIsClient] = useState(false);

    const [postIndex, setPostIndex] = useState(0);

    useEffect(() => {
        const interval = setInterval(() => {
            setPostIndex((current) => (current + 1) % rawBlueskyPosts.length);
        }, 3500);

        return () => clearInterval(interval);
    }, [rawBlueskyPosts.length]);

    useEffect(() => {
        setIsClient(true);
    }, []);

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
        setNextIndex((currentIndex + 1) % summaries.length);
        setIsAnimating(true);
    };

    const previousSlide = () => {
        setDirection('next');
        setNextIndex((currentIndex - 1 + summaries.length) % summaries.length);
        setIsAnimating(true);
    };

    const { value: positiveScore, reset: resetPositive } = useCountUp({
        isCounting: true,
        duration: 1,
        start: 0,
        end: (socialMediaData?.positive || 0),
    });

    const { value: neutralScore, reset: resetNeutral } = useCountUp({
        isCounting: true,
        duration: 1,
        start: 0,
        end: (socialMediaData?.neutral || 0),
    });

    const { value: negativeScore, reset: resetNegative } = useCountUp({
        isCounting: true,
        duration: 1,
        start: 0,
        end: (socialMediaData?.negative || 0),
    });

    const positiveColour = 'bg-emerald-400';
    const neutralColour = 'bg-yellow-400';
    const negativeColour = 'bg-red-500';

    return (
        <div className="flex flex-col bg-neutral-900 w-full h-screen">
            <Header />
            <div className="flex flex-col px-8 pt-2 pb-8 h-full">
                <div className="flex justify-between gap-12 h-full">
                    <div className="grow w-2/5 flex flex-col gap-6">
                        <div className="w-full flex flex-col rounded-xl bg-zinc-800 p-8 items-center gap-8">
                            <p className={`text-2xl font-medium ${openSans.className}`}>Sentiment Scores Across # Posts</p>
                            <div className="flex w-full gap-4 items-center">
                                <ProgressBar value={positiveScore} colour={positiveColour} />
                                <p className="text-sm w-12">Positive</p>
                            </div>
                            <div className="flex w-full gap-4 items-center">
                                <ProgressBar value={neutralScore} colour={neutralColour} />
                                <p className="text-sm w-12">Neutral</p>
                            </div>
                            <div className="flex w-full gap-4 items-center">
                                <ProgressBar value={negativeScore} colour={negativeColour} />
                                <p className="text-sm w-12">Negative</p>
                            </div>
                        </div>
                        <div className="w-full h-1/2 relative">
                            <p className={`text-white text-xl font-medium ${openSans.className}`}>Where we pulled from...</p>
                            {isClient && blueskyEmbeddings.map((post, index) => (
                                <div
                                    key={index}
                                    className={`absolute w-full transition-opacity duration-300 ${
                                        index === postIndex ? 'opacity-100' : 'opacity-0'
                                    }`}
                                >
                                    <BlueskyEmbed uri={post.uri} cid={post.cid} />
                                </div>
                            ))}
                        </div>
                    </div>
                    <div className="grow w-3/5 h-full">
                        <div className="h-1/2 relative overflow-hidden">
                            <div className="absolute inset-0 flex flex-col rounded-xl bg-zinc-800 p-8 gap-4 h-full w-full">
                                <div className="flex justify-between items-center">
                                    <p className={`text-2xl font-medium ${summaries[currentIndex].color} ${openSans.className}`}>
                                        {summaries[currentIndex].title}
                                    </p>
                                    <div className="flex gap-2">
                                        <button
                                            onClick={previousSlide}
                                            className="p-2 rounded-full hover:bg-zinc-700"
                                        >
                                            <ChevronLeftIcon className="h-5 w-5" />
                                        </button>
                                        <button
                                            onClick={nextSlide}
                                            className="p-2 rounded-full hover:bg-zinc-700"
                                        >
                                            <ChevronRightIcon className="h-5 w-5" />
                                        </button>
                                    </div>
                                </div>
                                <div className="relative flex-1 overflow-hidden">
                                    <div className={`absolute inset-0 transition-transform duration-300 ${isAnimating ? (direction === 'next' ? 'animate-swipe-out-right' : 'animate-swipe-out-left') : ''}`}>
                                        <p className="text-sm text-neutral-300 overflow-hidden overflow-y-auto no-scrollbar h-full">
                                            {summaries[currentIndex].content}
                                        </p>
                                    </div>
                                    <div className={`absolute inset-0 transition-transform duration-300 ${isAnimating ? (direction === 'next' ? 'animate-swipe-in-left' : 'animate-swipe-in-right') : ''}`}>
                                        <p className="text-sm text-neutral-300 overflow-hidden overflow-y-auto no-scrollbar h-full">
                                            {summaries[nextIndex].content}
                                        </p>
                                    </div>
                                </div>
                                <div className="flex justify-center gap-2">
                                    {summaries.map((_, index) => (
                                        <div
                                            key={index}
                                            className={`h-2 w-2 rounded-full ${
                                                index === currentIndex ? 'bg-white' : 'bg-zinc-600'
                                            }`}
                                        />
                                    ))}
                                </div>
                            </div>
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

export default SocialMediaPage;