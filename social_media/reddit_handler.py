import os
from dotenv import load_dotenv
import praw
import json
import asyncio

load_dotenv()
reddit = praw.Reddit(
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'), 
    user_agent=os.getenv('USER_AGENT')        
)

async def fetch_reddit(subreddit_name: str, stock: str):
    posts = []

    subreddit = reddit.subreddit(subreddit_name)

    if not subreddit:
        print(f"Subreddit {subreddit_name} not found")
        return None
    
    for post in subreddit.search(stock, sort='new', limit=15):
        combined_content = f"Title: {post.title}\nBody: {post.selftext}\nLink: {post.url}"
        posts.append({
            'Content': combined_content,
            'Source': 'Reddit'
        })

    return posts