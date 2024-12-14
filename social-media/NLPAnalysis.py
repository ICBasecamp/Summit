import os
from groq import Groq
import asyncio
from dotenv import load_dotenv
from sentiment_analysis import main as sentiment_analysis_main, ticker_to_company
from stockwits_handler import fetch_stockwits
from bluesky_handler import fetch_bluesky

# Configure Groq API
load_dotenv()
groq_api_key = os.getenv("groq_api_key")
client = Groq(api_key=groq_api_key)

async def call_groqapi_service(text):
    prompt_template = """
    Give a summary of the posts provided, write it in one paragraph no bullet points. Just sentences that make sense and add statistics if needed.

    Social Media Posts:
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

async def fetch_posts():
    ticker = 'NVDA'
    await fetch_bluesky(ticker_to_company(ticker) + " stock", limit=100)
    await fetch_stockwits(ticker, limit=100)

async def main():
    # Fetch posts
    await fetch_posts()

    # Run sentiment analysis and get the results
    sentiment_counts, positive_posts, neutral_posts, negative_posts = sentiment_analysis_main()

    total_posts = sentiment_counts.sum()
    positive_percentage = (sentiment_counts.get('positive', 0) / total_posts) * 100
    neutral_percentage = (sentiment_counts.get('neutral', 0) / total_posts) * 100
    negative_percentage = (sentiment_counts.get('negative', 0) / total_posts) * 100

    overall_sentiment = "neutral"
    if positive_percentage > max(neutral_percentage, negative_percentage):
        overall_sentiment = "bullish"
    elif negative_percentage > max(positive_percentage, neutral_percentage):
        overall_sentiment = "bearish"

    positive_insights = await call_groqapi_service("\n".join(positive_posts['Content'].tolist()))
    neutral_insights = await call_groqapi_service("\n".join(neutral_posts['Content'].tolist()))
    negative_insights = await call_groqapi_service("\n".join(negative_posts['Content'].tolist()))

    insights = f"""
    Sentiment Analysis Summary:
    Positive Sentiment: {positive_percentage:.2f}%
    Neutral Sentiment: {neutral_percentage:.2f}%
    Negative Sentiment: {negative_percentage:.2f}%
    Overall Sentiment: {overall_sentiment}

    Positive Posts Insights:
    {positive_insights}

    Neutral Posts Insights:
    {neutral_insights}

    Negative Posts Insights:
    {negative_insights}
    """

    print("NLP Insights:")
    print(insights)

    # Save the insights to a file
    with open('social-media/results/nlp_insights.txt', 'w') as f:
        f.write(insights)

if __name__ == "__main__":
    asyncio.run(main())