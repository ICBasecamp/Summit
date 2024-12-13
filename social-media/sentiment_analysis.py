import json
import asyncio
import pandas as pd
from transformers import pipeline
from bertopic import BERTopic
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from nltk.corpus import stopwords
from bluesky_handler import fetch_bluesky
from stockwits_handler import fetch_stockwits
import re
import yfinance as yf

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Data Cleaning function
def clean_text(text):
    text = re.sub(r'http\S+', '', text)  # Remove URLs
    text = re.sub(r'@\w+', '', text)  # Remove mentions
    text = text.lower()  # Convert to lowercase
    text = ' '.join([word for word in text.split() if word not in stop_words])  # Remove stopwords
    return text

# Function to convert ticker to company name and clean it
def ticker_to_company(ticker):
    try:
        company = yf.Ticker(ticker).info['longName']
        # Remove common company endings
        company = re.sub(r'\b(LLC|Corporation|Corp|Inc|Incorporated|Ltd|Limited|PLC|Group|Holdings|Holding|Company|Co)\b', '', company, flags=re.IGNORECASE).strip()
        return company
    except Exception as e:
        print(f"Error converting ticker {ticker} to company name: {e}")
        return ticker

def main():
    # Load the JSON file
    with open('social-media/results/bluesky_posts.json', 'r') as f:
        bluesky_posts = json.load(f)
    with open('social-media/results/stockwits_posts.json', 'r') as f:
        stockwits_posts = json.load(f)
    
    # Combine both posts
    posts = bluesky_posts + stockwits_posts

    # Convert to DataFrame
    df = pd.DataFrame(posts)

    # Clean the data
    df['Cleaned_Content'] = df['Content'].apply(clean_text)

    # Convert tickers to company names
    df['Cleaned_Content'] = df['Cleaned_Content'].apply(lambda x: re.sub(r'\$(\w+)', lambda m: ticker_to_company(m.group(1)), x))

    # Sentiment Analysis using FinBERT
    sentiment_model = pipeline("sentiment-analysis", model="ProsusAI/finbert")
    df['Sentiment'] = df['Cleaned_Content'].apply(lambda x: sentiment_model(x)[0]['label'])
    
    def weighted_sentiment(text):
        sentiment = sentiment_model(text)[0]['label']
        if 'bullish' in text.lower():
            return 'positive'
        elif 'bearish' in text.lower():
            return 'negative'
        return sentiment

    df['Sentiment'] = df['Cleaned_Content'].apply(weighted_sentiment)

    # Volume Tracking
    sentiment_counts = df['Sentiment'].value_counts()
    print("Sentiment Counts:")
    print(sentiment_counts)

    # Hashtag and Keyword Analysis
    hashtags = df['Content'].str.findall(r'#\w+').explode().value_counts()
    print("Trending Hashtags:")
    print(hashtags)

    # Topic Modeling using BERTopic
    vectorizer_model = CountVectorizer(stop_words="english")
    topic_model = BERTopic(vectorizer_model=vectorizer_model)
    topics = topic_model.fit_transform(df['Cleaned_Content'])

    # Ensure the length of topics matches the length of the DataFrame
    if len(topics) == len(df):
        df['Topic'] = topics
    else:
        print(f"Length of topics ({len(topics)}) does not match length of DataFrame ({len(df)}).")
        df['Topic'] = [None] * len(df)

    # Save the results to a CSV file
    df.to_csv('social-media/results/sentiment_analysis_results.csv', index=False)

    # Save topic representations to a CSV file
    topic_info = topic_model.get_topic_info()
    topic_info.to_csv('social-media/results/topic_representations.csv', index=False)

    print("Sentiment Analysis and Topic Modeling completed.")

if __name__ == "__main__":
    ticker = 'NVDA'
    asyncio.run(fetch_bluesky(ticker_to_company(ticker) + " stock", limit=100))
    asyncio.run(fetch_stockwits(ticker, limit=100))
    main()