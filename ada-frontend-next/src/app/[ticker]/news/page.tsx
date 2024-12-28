"use client";

import { Header } from '@/app/components/header'
import { CircularProgress } from '@/app/components/circular-progress';

import { useCountUp } from 'use-count-up';


const testData = {
    sentences: [
        {'sentence': 'Microsoft led the purchases with 615,000 units, but Chinese firms ByteDance and Tencent bought about 230,000 each, which meets U.S. export restrictions.', 'sentiment_score': 0.8326189},
        {'sentence': "However, Amazon and Google's purchase of 196,000 and 169,000 Hopper chips, respectively, demonstrates a competitive shift in the cloud computing market as the companies pursue their own development pipelines of custom AI chips.", 'sentiment_score': -0.50443673},
        {'sentence': 'Microsoft led the purchases with 615,000 units, but Chinese firms ByteDance and Tencent bought about 230,000 each, which meets U.S. export restrictions.', 'sentiment_score': 0.8326189},
        {'sentence': "However, Amazon and Google's purchase of 196,000 and 169,000 Hopper chips, respectively, demonstrates a competitive shift in the cloud computing market as the companies pursue their own development pipelines of custom AI chips.", 'sentiment_score': -0.50443673},
        {'sentence': 'Microsoft led the purchases with 615,000 units, but Chinese firms ByteDance and Tencent bought about 230,000 each, which meets U.S. export restrictions.', 'sentiment_score': 0.8326189},
        {'sentence': "However, Amazon and Google's purchase of 196,000 and 169,000 Hopper chips, respectively, demonstrates a competitive shift in the cloud computing market as the companies pursue their own development pipelines of custom AI chips.", 'sentiment_score': -0.50443673},
        {'sentence': "However, Amazon and Google's purchase of 196,000 and 169,000 Hopper chips, respectively, demonstrates a competitive shift in the cloud computing market as the companies pursue their own development pipelines of custom AI chips.", 'sentiment_score': -0.50443673}
    ]
};

const negativeSentThreshold = -15.00;
const positiveSentThreshold = 15.00;

const NewsPage = () => {

    const averageSentiment = parseFloat(((testData.sentences.reduce((acc, curr) => acc + curr.sentiment_score, 0) / testData.sentences.length) * 100).toFixed(2));

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
            <div className="flex flex-col p-16">
                <div className="flex justify-between">
                    <div className="flex flex-col rounded-lg bg-zinc-800 p-8 items-center gap-8 max-w-1/2">
                        <CircularProgress value={value} className="size-52" colour={sentimentColour}/>
                        <p className="text-lg">Average sentiment score across <span className="font-bold">{testData.sentences.length}</span> sentences scraped.</p>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default NewsPage;