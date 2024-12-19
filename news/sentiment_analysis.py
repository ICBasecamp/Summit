import json
import pandas as pd
from transformers import pipeline, AutoTokenizer
import nltk
from nltk.corpus import stopwords
import re
import yfinance as yf
from clean import clean_unstructured_data

import sys
import os
import asyncio
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from handler import fetch

async def main():
    ticker = "MSFT"
    df = await fetch(ticker)

    # Clean the data
    # df['Cleaned_Content'] = df['Content'].apply(clean_unstructured_data)

    # Sentiment Analysis using FinBERT
    sentiment_model = pipeline("sentiment-analysis", model="ProsusAI/finbert")
    tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")

    def overall_sentiment(content):
        tokens = tokenizer(content, truncation=True, padding=True, return_tensors="pt")
        sentiments = [sentiment_model(chunk)[0]['label'] for chunk in tokens]
        sentiment = max(set(sentiments), key=sentiments.count)
        return sentiment

    df['Sentiment'] = df['Content'].apply(overall_sentiment)

    # Volume Tracking
    sentiment_counts = df['Sentiment'].value_counts()
    # Group posts by sentiment
    positive_posts = df[df['Sentiment'] == 'positive']
    neutral_posts = df[df['Sentiment'] == 'neutral']
    negative_posts = df[df['Sentiment'] == 'negative']

    sentiment_columns = ['Title', 'Link', 'Sentiment']
    df = df[sentiment_columns]
    
    df.to_csv('news/results/sentiment_analysis_results.csv', index=False)

    print("Sentiment Analysis completed.")
    return sentiment_counts, positive_posts, neutral_posts, negative_posts

if __name__ == "__main__":
    sentiment_counts, positive_posts, neutral_posts, negative_posts = asyncio.run(main())

