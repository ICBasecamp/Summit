"use client";

import { Header } from '@/app/components/header'
import { ProgressBar } from '@/app/components/progress-bar';

import { useCountUp } from 'use-count-up';

import { openSans } from '@/app/layout';

import { useState, useEffect } from 'react';
import { ChevronLeftIcon, ChevronRightIcon } from 'lucide-react';

const testJsonResponse = {
    positiveSummary: `The stock market has continued to soar to new heights, with the Dow, S&P 500, and Russell 2000 reaching record highs despite threats of tariffs from former President Trump. Additionally, AI chipmaker Nvidia has taken a backseat to a lesser-known Ohio-based cooling technology stock, which has seen its market cap balloon in just two years since the launch of ChatGPT. Meanwhile, MicroStrategy, a tech company, has emerged as the best-performing stock in the Russell 1000 over the last seven years, with a return of over 3,400%. Despite some volatility, Nvidia's stock price has displayed a strong inverse head and shoulders pattern, leading many analysts to predict a bullish break-out above $135.70, potentially pushing the stock price to $141 or even $160, which could be a Christmas 
gift in itself.`,
    neutralSummary: `The provided social media posts are a mix of opinions and speculation about Nvidia's stock performance, with some users expressing concerns about its potential collapse and others being optimistic about its future growth. However, many of the posts also discuss the importance of Nvidia and other tech companies 
to the state's social safety net, as they generate significant tax revenue. Additionally, some posts mention the company's recent stock performance and predictions for its future, with some users even claiming that its stock will continue to rise over the next year.`,
    negativeSummary: `The Chinese central economic work conference has announced plans for greater liquidity, interest rate cuts, and larger fiscal deficits, sparking concern among economists. Meanwhile, problems with NVIDIA's "Blackwell" chip servers have further delayed the development of generative AI models, leading some to worry about the potential economic impact if AI technology suddenly becomes unreliable. Additionally, the vast investment in AI technology means that a collapse could have far-reaching consequences, potentially even destabilizing the economy. In the face of these challenges, investors are divided, with some urging caution and others, like Jim Cramer, refusing to sell their stocks in companies like Apple and NVIDIA. Despite these concerns, the S&P 500 index has continued to 
rise, with the current level standing 22.9% above projections for Q2 2024 in the June 2024 budget forecast.`,
    positiveScore: 0.3953,
    neutralScore: 0.4884,
    negativeScore: 0.1163,

}

const SocialMediaPage = () => {
    const summaries = [
        {
            title: 'Positive Summary',
            content: testJsonResponse.positiveSummary,
        },
        {
            title: 'Neutral Summary',
            content: testJsonResponse.neutralSummary,
        },
        {
            title: 'Negative Summary',
            content: testJsonResponse.negativeSummary,
        },
    ];

    const [currentIndex, setCurrentIndex] = useState(0);
    const [isAnimating, setIsAnimating] = useState(false);
    const [direction, setDirection] = useState('next');
    const [nextIndex, setNextIndex] = useState(0);

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
        setDirection('next');
        setNextIndex((currentIndex + 1) % summaries.length);
        setIsAnimating(true);
    };

    const previousSlide = () => {
        setDirection('prev');
        setNextIndex((currentIndex - 1 + summaries.length) % summaries.length);
        setIsAnimating(true);
    };

    let overallSentiment = "neutral";
    if (testJsonResponse.positiveScore > testJsonResponse.neutralScore && testJsonResponse.positiveScore > testJsonResponse.negativeScore) {
        overallSentiment = "positive";
    } else if (testJsonResponse.negativeScore > testJsonResponse.neutralScore && testJsonResponse.negativeScore > testJsonResponse.positiveScore) {
        overallSentiment = "negative";
    }

    const { value: positiveScore, reset: resetPositive } = useCountUp({
        isCounting: true,
        duration: 1,
        start: 0,
        end: testJsonResponse.positiveScore * 100,
    });

    const { value: neutralScore, reset: resetNeutral } = useCountUp({
        isCounting: true,
        duration: 1,
        start: 0,
        end: testJsonResponse.neutralScore * 100,
    });

    const { value: negativeScore, reset: resetNegative } = useCountUp({
        isCounting: true,
        duration: 1,
        start: 0,
        end: testJsonResponse.negativeScore * 100,
    });

    const positiveColour = 'bg-emerald-400';
    const neutralColour = 'bg-violet-400';
    const negativeColour = 'bg-red-500';

    return (
        <div className="flex flex-col bg-neutral-900 w-full h-screen">
            <Header />
            <div className="flex flex-col px-8 pt-2 pb-8 h-full">
                <div className="flex justify-between gap-12 h-full">
                    <div className="grow w-2/5">
                        <div className="w-full flex flex-col rounded-xl bg-zinc-800 p-8 items-center gap-8">
                            <p className={`text-2xl font-medium ${openSans.className}`}>Sentiment Scores Across # Posts</p>
                            <div className="flex w-full gap-4 items-center">
                                <ProgressBar value={positiveScore} colour={positiveColour}/>
                                <p className="text-sm w-12">Positive</p>
                            </div>
                            <div className="flex w-full gap-4 items-center">
                                <ProgressBar value={neutralScore} colour={neutralColour}/>
                                <p className="text-sm w-12">Neutral</p>
                            </div>
                            <div className="flex w-full gap-4 items-center">
                                <ProgressBar value={negativeScore} colour={negativeColour}/>
                                <p className="text-sm w-12">Negative</p>
                            </div>
                        </div>
                    </div>
                    <div className="grow w-3/5 h-full">
                        <div className="h-1/2 relative overflow-hidden">
                            <div className="absolute inset-0 flex flex-col rounded-xl bg-zinc-800 p-8 gap-4 h-full w-full">
                                <div className="flex justify-between items-center">
                                    <p className={`text-2xl font-medium ${openSans.className}`}>
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
                                <div className="relative flex-1 overflow-scroll">
                                    <div className={`absolute inset-0 transition-transform duration-300 ${isAnimating ? (direction === 'next' ? 'animate-swipe-out-right' : 'animate-swipe-out-left') : ''}`}>
                                        <p className="text-sm text-neutral-300">
                                            {summaries[currentIndex].content}
                                        </p>
                                    </div>
                                    <div className={`absolute inset-0 transition-transform duration-300 ${isAnimating ? (direction === 'next' ? 'animate-swipe-in-left' : 'animate-swipe-in-right') : ''}`}>
                                        <p className="text-sm text-neutral-300">
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
            `}</style>
        </div>
    );
}

export default SocialMediaPage;
