import json
import pandas as pd
from transformers import pipeline, AutoTokenizer
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

# Function to split text into chunks using the tokenizer
def split_text(text, tokenizer, max_length=300):
    tokens = tokenizer.tokenize(text)
    chunks = []
    for i in range(0, len(tokens), max_length):
        chunk_tokens = tokens[i:i + max_length]
        chunk_text = tokenizer.convert_tokens_to_string(chunk_tokens)
        chunks.append(chunk_text)
    return chunks

def calculate_sentiment():
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

    # Sentiment Analysis using FinBERT
    sentiment_model = pipeline("sentiment-analysis", model="ProsusAI/finbert")
    tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")

    def weighted_sentiment(text):
        chunks = split_text(text, tokenizer)
        sentiments = [sentiment_model(chunk)[0]['label'] for chunk in chunks]
        sentiment = max(set(sentiments), key=sentiments.count)  # Use the most common sentiment
        if 'bullish' in text.lower():
            return 'positive'
        elif 'bearish' in text.lower():
            return 'negative'
        return sentiment

    df['Sentiment'] = df['Cleaned_Content'].apply(weighted_sentiment)

    # Volume Tracking
    sentiment_counts = df['Sentiment'].value_counts()
    # Group posts by sentiment
    positive_posts = df[df['Sentiment'] == 'positive']
    neutral_posts = df[df['Sentiment'] == 'neutral']
    negative_posts = df[df['Sentiment'] == 'negative']
    
    df.to_csv('social-media/results/sentiment_analysis_results.csv', index=False)

    print("Sentiment Analysis completed.")
    return sentiment_counts, positive_posts, neutral_posts, negative_posts
