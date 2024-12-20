import pandas as pd
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import nltk
from clean import clean_unstructured_data

import sys
import os
import asyncio
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from handler import fetch

async def main():
    ticker = "MSFT"
    df = await fetch(ticker)

    # temporarily reading/storing from csv for testing, reduce time fetching
    # df.to_csv('news/results/raw_data.csv', index=False)

    # df = pd.read_csv('news/results/raw_data.csv')
    # df = df.head(1)

    df['Sentiments'] = None

    # using automodel instead of pipeline
    sentiment_model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
    tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
    
    def calculate_sentiment_score(sentiment):
        scores = sentiment.logits.softmax(dim=-1).detach().cpu().numpy()[0]
        sentiment_score = scores[2] - scores[0]  # positive - negative
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

if __name__ == "__main__":
    sentiments = asyncio.run(main())

