from flask import Flask, Response, request, stream_with_context
from flask_cors import CORS
import asyncio
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from economic_indicators.NLPAnalysis import EI_NLPAnalysis
from earnings.NLPAnalysis import NLP as ER_NLPAnalysis
from social_media.NLPAnalysis import social_media_sentiment_analysis as SM_NLPAnalysis
from news.sentiment_analysis import sentiment_analysis_on_ticker as NA_NLPAnalysis

app = Flask(__name__)
CORS(app)

@app.route('/analyze/<ticker>')
def analyze(ticker):
    print(f"Received ticker: {ticker}")

    @stream_with_context
    def workflow():
        try:
            yield "data: Starting analysis...\n\n"

            # Social Media Analysis
            yield "data: Analyzing social media...\n\n"
            social_media = asyncio.run(SM_NLPAnalysis(ticker))
            if isinstance(social_media, list):
                social_media = ' '.join(map(str, social_media))
            yield f"data: socialMedia: {social_media.replace('\n', ' ')}\n\n"

            # Earnings Analysis
            yield "data: Analyzing earnings reports...\n\n"
            earnings = asyncio.run(ER_NLPAnalysis(ticker))
            if isinstance(earnings, (list, tuple)):
                earnings = ' '.join(map(str, earnings))
            yield f"data: earnings: {earnings.replace('\n', ' ')}\n\n"

            # News Analysis
            yield "data: Analyzing news articles...\n\n"
            news = asyncio.run(NA_NLPAnalysis(ticker))
            if isinstance(news, list):
                news = ' '.join(map(str, news))
            yield f"data: news: {news.replace('\n', ' ')}\n\n"

            # Economic Indicators Analysis
            yield "data: Analyzing economic indicators...\n\n"
            economic_indicators = asyncio.run(EI_NLPAnalysis(ticker))
            if isinstance(economic_indicators, (list, tuple)):
                economic_indicators = ' '.join(map(str, economic_indicators))
            yield f"data: economicIndicators: {economic_indicators.replace('\n', ' ')}\n\n"

            yield "data: Analysis complete.\n\n"
        except Exception as e:
            yield f"data: error: {str(e).replace('\n', ' ')}\n\n"

    return Response(workflow(), content_type='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)