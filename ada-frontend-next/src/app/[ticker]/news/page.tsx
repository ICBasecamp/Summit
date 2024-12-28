"use client";

import { Header } from '@/app/components/header'

const testData = {
    sentences: [
        {'sentence': 'Microsoft led the purchases with 615,000 units, but Chinese firms ByteDance and Tencent bought about 230,000 each, which meets U.S. export restrictions.', 'sentiment_score': 0.8326189},
        {'sentence': "However, Amazon and Google's purchase of 196,000 and 169,000 Hopper chips, respectively, demonstrates a competitive shift in the cloud computing market as the companies pursue their own development pipelines of custom AI chips.", 'sentiment_score': -0.50443673},
        {'sentence': 'Microsoft led the purchases with 615,000 units, but Chinese firms ByteDance and Tencent bought about 230,000 each, which meets U.S. export restrictions.', 'sentiment_score': 0.8326189},
        {'sentence': "However, Amazon and Google's purchase of 196,000 and 169,000 Hopper chips, respectively, demonstrates a competitive shift in the cloud computing market as the companies pursue their own development pipelines of custom AI chips.", 'sentiment_score': -0.50443673},
        {'sentence': 'Microsoft led the purchases with 615,000 units, but Chinese firms ByteDance and Tencent bought about 230,000 each, which meets U.S. export restrictions.', 'sentiment_score': 0.8326189},
        {'sentence': "However, Amazon and Google's purchase of 196,000 and 169,000 Hopper chips, respectively, demonstrates a competitive shift in the cloud computing market as the companies pursue their own development pipelines of custom AI chips.", 'sentiment_score': -0.50443673}
    ]
}

const NewsPage = () => {


    return (
        <div className="flex flex-col">
            <Header />
            <h1>News Page</h1>
        </div>
    );
}

export default NewsPage;