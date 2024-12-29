import pandas as pd
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import nltk
from clean import clean_unstructured_data

import sys
import os
import asyncio

from handler import fetch_articles

# accepts ticker as input, scrapes news articles and performs sentiment analysis, returning
# as an array of dictionaries of individual sentences and their sentiment scores
async def sentiment_analysis_on_ticker(ticker):

    # df = await fetch_articles(ticker)

    # if df.empty:
    #     print("No articles found for the ticker.")
    #     return []

    # temporarily reading/storing from csv for testing, reduce time fetching
    # df.to_csv('news/results/raw_data.csv', index=False)

    df = pd.read_csv('news/results/raw_data.csv')
    df = df.head(3)
    
    df['Sentiments'] = None

    # using automodel instead of pipeline
    sentiment_model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
    tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
    
    def calculate_sentiment_score(sentiment):
        scores = sentiment.logits.softmax(dim=-1).detach().cpu().numpy()[0]
        sentiment_score = scores[2]  # positive - negative
        return sentiment_score
    
    def analyze_sentiment(row):
        sentences = nltk.sent_tokenize(row['Content'])
        sentiments = []
        
        for sentence in sentences:
            cleaned_sentence = ' '.join(clean_unstructured_data(sentence))
            inputs = tokenizer(cleaned_sentence, padding=True, truncation=True, return_tensors="pt")
            sentiment = sentiment_model(**inputs)
            sentiment_score = calculate_sentiment_score(sentiment)
            sentiments.append({
                'sentence': sentence,
                # 'sentiment': sentiment, # raw output not necessary right now
                'sentiment_score': sentiment_score
            })
    
        return sentiments
    
    df['Sentiments'] = df.apply(analyze_sentiment, axis=1)
    
    sentiment_columns = ['Title', 'Link', 'Sentiments']
    df = df[sentiment_columns]
    
    df.to_csv('news/results/sentiment_analysis_results.csv', index=False)

    print("Sentiment Analysis completed.")
    return df['Sentiments'].tolist()

asyncio.run(sentiment_analysis_on_ticker('MSFT')) # for testing
