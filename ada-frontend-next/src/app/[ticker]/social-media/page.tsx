"use client";

import { Header } from '@/app/components/header'
import { ProgressBar } from '@/app/components/progress-bar';

import { useCountUp } from 'use-count-up';

import * as Tooltip from '@radix-ui/react-tooltip';

import { geistSans, openSans } from '@/app/layout';

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
            <div className="flex flex-col px-8 pt-2 pb-8">
                <div className="flex justify-between gap-12">
                    <div className="grow w-3/5">
                        <div className="flex flex-col">
                            <div className="flex flex-col rounded-xl bg-zinc-800 p-8 items-center gap-8">
                                <p className={`text-2xl font-semibold ${openSans.className}`}>Sentiment Scores Across # Posts</p>
                                <ProgressBar value={positiveScore} colour={positiveColour}/>
                                <ProgressBar value={neutralScore} colour={neutralColour}/>
                                <ProgressBar value={negativeScore} colour={negativeColour}/>


                                {/* <p className="text-lg">Average sentiment score across <span className="font-bold">{testData.response.length}</span> sentences scraped.</p> */}
                            </div>
                        </div>
                    </div>
                    <div className="grow w-2/5">
                        <div className="flex flex-col gap-8">
                            {/* <div className="flex flex-col rounded-xl bg-zinc-800 p-6 gap-2">
                                <h2 className={`text-lg font-medium self-center ${openSans.className}`}>Highest Sentiment Sentences</h2>
                                {highestSentences.map((sentence, index) => (
                                    
                                    <div key={index} className="flex flex-col gap-1">
                                        <p className="font-semibold text-emerald-400" >{(sentence.sentiment_score * 100).toFixed(2)}%</p>
                                        <Tooltip.Provider>
                                            <Tooltip.Root>
                                                <Tooltip.Trigger asChild>
                                                    <p className="cursor-default text-xs">{sentence.sentence}</p>
                                                </Tooltip.Trigger>
                                                <Tooltip.Portal>
                                                    <Tooltip.Content 
                                                        className="TooltipContent" 
                                                        sideOffset={5}
                                                        align="start"
                                                    >
                                                        <div className="flex items-center justify-center py-0.5 px-1 rounded-md bg-zinc-950">
                                                            <a href={sentence.link} className='text-white text-xs'>{sentence.link}</a>
                                                        </div>
                                                        <Tooltip.Arrow className="TooltipArrow" />
                                                    </Tooltip.Content>
                                                </Tooltip.Portal>
                                            </Tooltip.Root>
                                        </Tooltip.Provider>
                                    </div>
                                ))}
                            </div>
                            <div className="flex flex-col rounded-xl bg-zinc-800 p-6 gap-2">
                                <h2 className={`text-lg font-medium self-center ${openSans.className}`} >Lowest Sentiment Sentences</h2>
                                {lowestSentences.map((sentence, index) => (
                                    <div key={index} className="flex flex-col gap-0.5">
                                        <p className="font-semibold text-red-400" >{(sentence.sentiment_score * 100).toFixed(2)}%</p>
                                        <Tooltip.Provider>
                                            <Tooltip.Root>
                                                <Tooltip.Trigger asChild>
                                                    <p className="cursor-default text-xs">{sentence.sentence}</p>
                                                </Tooltip.Trigger>
                                                <Tooltip.Portal>
                                                    <Tooltip.Content 
                                                        className="TooltipContent" 
                                                        sideOffset={5}
                                                        align="start"
                                                    >
                                                        <div className="flex items-center justify-center py-0.5 px-1 rounded-md bg-zinc-950">
                                                            <a href={sentence.link} className='text-white text-xs'>{sentence.link}</a>
                                                        </div>
                                                        <Tooltip.Arrow className="TooltipArrow" />
                                                    </Tooltip.Content>
                                                </Tooltip.Portal>
                                            </Tooltip.Root>
                                        </Tooltip.Provider>
                                    </div>
                                ))}
                            </div> */}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default SocialMediaPage;
