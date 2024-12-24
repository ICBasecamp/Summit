from flask import Flask, Response, request, stream_with_context, jsonify
import asyncio
import time
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from economic_indicators.NLPAnalysis import EI_NLPAnalysis
from earnings.NLPAnalysis import NLP as ER_NLPAnalysis
from social_media.NLPAnalysis import social_media_sentiment_analysis as SM_NLPAnalysis
from news.sentiment_analysis import sentiment_analysis_on_ticker as NA_NLPAnalysis

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
async def run_workflow():
    data = request.get_json()
    ticker = data.get('ticker')
    print(f"Received ticker: {ticker}")

    socialMedia = await SM_NLPAnalysis(ticker)
    earnings = await ER_NLPAnalysis(ticker)
    news = await NA_NLPAnalysis(ticker)
    economicIndicators = await EI_NLPAnalysis(ticker)
    
    res = {
        "socialMedia": socialMedia,
        "earnings": earnings,
        "news": news,
        "economicIndicators": economicIndicators
    }

    return jsonify(res)

if __name__ == '__main__':
    app.run(debug=True)
