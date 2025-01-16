import pandas as pd
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import nltk
import sys
import os
import asyncio
import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from news.clean import clean_unstructured_data
from news.handler import fetch_articles
from dotenv import load_dotenv
from groq import Groq

nltk.download('punkt')

# Configure Groq API
load_dotenv()
groq_api_key = os.getenv("groq_api_key")
client = Groq(api_key=groq_api_key)

async def call_groqapi_service(text, category):
    prompt_template = f"""
    Summarize the following {category} sentences in one paragraph. Include key points and statistics if available, clean up
    any characters that do not below, round stats to 2 decimal places, and make sure the summary is coherent and detailed. Just give the data after the label
    don't say anything like "Here is a summary of the positive sentences in one paragraph, including key points and statistics:" or "Note: I removed the error messages and irrelevant text from the original paragraph."

    Sentences:
    {text}
    """
    prompt = prompt_template.format(text=text)
    chat_completion = await asyncio.get_event_loop().run_in_executor(
        None,
        lambda: client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192"
        )
    )
    return chat_completion.choices[0].message.content.strip()

# accepts ticker as input, scrapes news articles and performs sentiment analysis, returning
# as an array of dictionaries of individual sentences and their sentiment scores
async def sentiment_analysis_on_ticker(ticker):
    df = await fetch_articles(ticker)

    if df.empty:
        print("No articles found for the ticker.")
        return []

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
                'sentiment_score': sentiment_score
            })
    
        return sentiments
    
    df['Sentiments'] = df.apply(analyze_sentiment, axis=1)
    
    sentiment_columns = ['Title', 'Link', 'Sentiments']
    df = df[sentiment_columns]

    # Extract positive, neutral, and negative sentences
    positive_sentences = []
    neutral_sentences = []
    negative_sentences = []

    for sentiments in df['Sentiments']:
        for sentiment in sentiments:
            if sentiment['sentiment_score'] > 0.66:
                positive_sentences.append(sentiment['sentence'])
            elif sentiment['sentiment_score'] < 0.33:
                negative_sentences.append(sentiment['sentence'])
            else:
                neutral_sentences.append(sentiment['sentence'])

    # Summarize each category using Groq
    positive_summary = await call_groqapi_service("\n".join(positive_sentences), "positive")
    neutral_summary = await call_groqapi_service("\n".join(neutral_sentences), "neutral")
    negative_summary = await call_groqapi_service("\n".join(negative_sentences), "negative")

    summaries = {
        'positive_summary': positive_summary,
        'neutral_summary': neutral_summary,
        'negative_summary': negative_summary
    }

    print("Sentiment Analysis completed.")
    return summaries, df['Sentiments'].tolist()