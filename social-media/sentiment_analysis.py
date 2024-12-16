import json
import pandas as pd
from transformers import pipeline
import nltk
from nltk.corpus import stopwords
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
    # Load the JSON files
    with open('social-media/results/bluesky_posts.json', 'r') as f:
        bluesky_posts = json.load(f)
    with open('social-media/results/stockwits_posts.json', 'r') as f:
        stockwits_posts = json.load(f)
    with open('social-media/results/reddit_posts.json', 'r') as f:
        reddit_posts = json.load(f)
    
    # Combine all posts
    posts = bluesky_posts + stockwits_posts + reddit_posts

    # Convert to DataFrame
    df = pd.DataFrame(posts)

    # Clean the data
    df['Cleaned_Content'] = df['Content'].apply(clean_text)

    # Convert tickers to company names
    df['Cleaned_Content'] = df['Cleaned_Content'].apply(lambda x: re.sub(r'\$(\w+)', lambda m: ticker_to_company(m.group(1)), x))

    # Sentiment Analysis using FinBERT
    sentiment_model = pipeline("sentiment-analysis", model="ProsusAI/finbert")

    def truncate_text(text, max_length=512):
        tokens = text.split()
        if len(tokens) > max_length:
            return ' '.join(tokens[:max_length])
        return text

    df['Cleaned_Content'] = df['Cleaned_Content'].apply(lambda x: truncate_text(x))

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

    # Group posts by sentiment
    positive_posts = df[df['Sentiment'] == 'positive']
    neutral_posts = df[df['Sentiment'] == 'neutral']
    negative_posts = df[df['Sentiment'] == 'negative']
    
    df.to_csv('social-media/results/sentiment_analysis_results.csv', index=False)

    print("Sentiment Analysis completed.")
    return sentiment_counts, positive_posts, neutral_posts, negative_posts
