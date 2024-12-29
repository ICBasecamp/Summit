"use client";

import { Header } from '@/app/components/header'
import { CircularProgress } from '@/app/components/circular-progress';

import { useCountUp } from 'use-count-up';

import * as Tooltip from '@radix-ui/react-tooltip';

const testJsonResponse = [
    {
        Link: "https://finance.yahoo.com/news/microsoft-corporation-msft-leads-ai-031051641.html",
        Sentiments: [
            { sentence: "We recently compiled a list of the 9 Trending AI Stocks on Latest News and Ratings.", sentiment_score: 0.9332724 },
            { sentence: "In this article, we are going to take a look at where Microsoft Corporation (NASDAQ:MSFT) stands against the other AI stocks.", sentiment_score: 0.94106907 },
            { sentence: "A Bloomberg report from December 13, AI Wants More Data.", sentiment_score: 0.93741614 },
            { sentence: "More Chips.", sentiment_score: 0.9341822 },
            { sentence: "More Real Estate.", sentiment_score: 0.9383361 },
            { sentence: "More Power.", sentiment_score: 0.92113954 },
            { sentence: "More Water.", sentiment_score: 0.92024726 },
            { sentence: "More Everything, explores the resource-intensive nature of artificial intelligence, emphasizing its demands on electricity, water, and infrastructure.", sentiment_score: 0.9168238 },
            { sentence: "Number of Hedge Fund Holders: 279\nMicrosoft Corporation (NASDAQ:MSFT) uses AI across its cloud services, productivity tools, and business solutions to enhance automation, security, and user experience.", sentiment_score: 0.7505022 },
            { sentence: "Its AI initiatives include intelligent cloud services, AI-driven applications for business operations, and advanced capabilities in language processing and cloud computing.", sentiment_score: 0.92186314 },
            { sentence: "Omidia, a technology consultancy estimates that Microsoft purchased 485,000 of Nvidia's Hopper GPUs in 2024, as reported by Financial Times.", sentiment_score: 0.9121019 },
            { sentence: "Overall MSFT ranks 2nd on our list of the trending AI stocks.", sentiment_score: 0.72807175 },
            { sentence: "While we acknowledge the potential of MSFT as an investment, our conviction lies in the belief that AI stocks hold greater promise for delivering higher returns and doing so within a shorter timeframe.", sentiment_score: 0.04312906 }
        ]
    },
    {
        Link: "https://finance.yahoo.com/news/asked-5-ai-chatbots-pick-193700333.html",
        Sentiments: [
            { sentence: "The year 2025 is virtually here, bringing with it a wave of curiosity from investors eager to see what the stock market holds.", sentiment_score: 0.50006336 },
            { sentence: "To capture the pulse of the moment, Quartz asked five AI chatbots — OpenAI's ChatGPT, Google's (GOOGL) Gemini, Meta (META) AI, Microsoft's (MSFT) Copilot, and Groq — to share predictions on the stocks that may outperform in 2025.", sentiment_score: 0.4835702 },
            { sentence: "Microsoft (MSFT): Microsoft's strong product lineup, including Windows, Office, and Azure cloud platform, positions it well for future growth.", sentiment_score: 0.07472271 },
            { sentence: "Its focus on productivity and collaboration tools is also driving strong demand.", sentiment_score: 0.2506462 },
            { sentence: "Apple (AAPL): Apple's innovative products, including the iPhone, iPad, and Mac, continue to be popular with consumers.", sentiment_score: 0.52340305 },
            { sentence: "Its strong brand loyalty and ecosystem of services provide a solid foundation for future growth.", sentiment_score: 0.17264448 },
            { sentence: "Tesla (TSLA): Tesla is leading the electric vehicle revolution and is rapidly expanding its production capacity.", sentiment_score: 0.066005215 },
            { sentence: "Its strong brand recognition and innovative technology give it a competitive advantage in the market.", sentiment_score: 0.10793233 },
            { sentence: "Apple Inc. (AAPL): Apple continues to be a leader in technology with strong growth in its services segment, including payment processing and streaming media.", sentiment_score: 0.06272849 }
    
        ]
    }
];

const testData = {
    response: testJsonResponse.flatMap((json) => 
        json.Sentiments.map((sentiment) => ({
            link: json.Link,
            sentence: sentiment.sentence,
            sentiment_score: sentiment.sentiment_score
        }))
    ),
};

const negativeSentThreshold = -15.00;
const positiveSentThreshold = 15.00;

const NewsPage = () => {

    const averageSentiment = parseFloat(((testData.response.reduce((acc, curr) => acc + curr.sentiment_score, 0) / testData.response.length) * 100).toFixed(2));

    const sortedSentences = testData.response.sort((a, b) => b.sentiment_score - a.sentiment_score);
    const highestSentences = sortedSentences.slice(0, 3);
    const lowestSentences = sortedSentences.slice(-3).reverse();

    const { value, reset } = useCountUp({
        isCounting: true,
        duration: 1,
        start: 0,
        end: averageSentiment,
      });

    let sentimentColour = 'text-violet-400';

    if (averageSentiment < negativeSentThreshold) {
        sentimentColour = 'text-red-500';
    } else if (averageSentiment > positiveSentThreshold) {
        sentimentColour = 'text-emerald-400';
    }

    return (
        <div className="flex flex-col bg-neutral-900 w-full h-screen">
            <Header />
            <div className="flex flex-col px-8 pt-2 pb-8">
                <div className="flex justify-between gap-8">
                    <div className="grow w-2/5">
                        <div className="flex flex-col">
                            <div className="flex flex-col rounded-xl bg-zinc-800 p-8 items-center gap-8">
                                <CircularProgress value={value} className="size-52" colour={sentimentColour}/>
                                <p className="text-lg">Average sentiment score across <span className="font-bold">{testData.response.length}</span> sentences scraped.</p>
                            </div>
                        </div>
                    </div>
                    <div className="grow w-3/5">
                        <div className="flex flex-col gap-8">
                            <div className="flex flex-col rounded-xl bg-zinc-800 p-6 gap-2">
                                <h2 className="text-lg font-semibold self-center">Highest Sentiment Sentences</h2>
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
                                <h2 className="text-lg font-semibold self-center">Lowest Sentiment Sentences</h2>
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
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default NewsPage;