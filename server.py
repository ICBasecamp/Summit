from flask import Flask, Response, request, stream_with_context
import asyncio
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from economic_indicators.NLPAnalysis import EI_NLPAnalysis
from earnings.NLPAnalysis import NLP as ER_NLPAnalysis
from social_media.NLPAnalysis import social_media_sentiment_analysis as SM_NLPAnalysis
from news.sentiment_analysis import sentiment_analysis_on_ticker as NA_NLPAnalysis

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    ticker = data.get('ticker')
    print(f"Received ticker: {ticker}")

    @stream_with_context
    def workflow():
        try:
            yield "Starting analysis...\n"

            # Social Media Analysis
            yield "Analyzing social media...\n"
            social_media = asyncio.run(SM_NLPAnalysis(ticker))
            # yield f"{social_media}\n"

            # Earnings Analysis
            yield "Analyzing earnings reports...\n"
            earnings = asyncio.run(ER_NLPAnalysis(ticker))
            # yield f"{earnings}\n"

            # News Analysis
            yield "Analyzing news articles...\n"
            news = asyncio.run(NA_NLPAnalysis(ticker))
            # yield f"{news}\n"

            # Economic Indicators Analysis
            yield "Analyzing economic indicators...\n"
            economic_indicators = asyncio.run(EI_NLPAnalysis(ticker))
            # yield f"{economic_indicators}\n"

            # Final result
            result = {
                "socialMedia": social_media,
                "earnings": earnings,
                "news": news,
                "economicIndicators": economic_indicators
            }
            yield f"Final Result: {result}\n"
        except Exception as e:
            yield f"An error occurred: {str(e)}\n"

    return Response(workflow(), content_type='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)
