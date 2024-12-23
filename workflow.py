import os
import sys
import asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from economic_indicators.NLPAnalysis import EI_NLPAnalysis
from earnings.NLPAnalysis import NLP as ER_NLPAnalysis
from social_media.NLPAnalysis import social_media_sentiment_analysis as SM_NLPAnalysis
from news.sentiment_analysis import sentiment_analysis_on_ticker as NA_NLPAnalysis

ticker = 'AAPL'
async def main():
    socialMedia = await SM_NLPAnalysis(ticker)
    earnings = await ER_NLPAnalysis(ticker)
    news = await NA_NLPAnalysis(ticker)
    economicIndicators = await EI_NLPAnalysis(ticker)
    
    print("NEW SECTION")
    print(socialMedia)
    print("NEW SECTION")
    print(earnings)
    print("NEW SECTION")
    print(news)
    print("NEW SECTION")
    print(economicIndicators)

if __name__ == '__main__':
    asyncio.run(main())