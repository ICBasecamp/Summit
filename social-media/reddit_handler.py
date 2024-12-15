import os
from dotenv import load_dotenv
import asyncpraw
import json

load_dotenv()
reddit = asyncpraw.Reddit(
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'), 
    user_agent=os.getenv('USER_AGENT')        
)

async def fetch_reddit(subreddit_name: str, stock: str):
    posts = []

    subreddit = await reddit.subreddit(subreddit_name)

    if not subreddit:
        print(f"Subreddit {subreddit_name} not found")
        return None
      
    async for post in subreddit.search(stock, sort='new', limit=25):
        combined_content = f"Title: {post.title}\nBody: {post.selftext}\nLink: {post.url}"
        posts.append({
            'Content': combined_content
        })

    # Save the results to a JSON file
    with open('social-media/results/reddit_posts.json', 'w') as f:
        json.dump(posts, f, indent=4)

    await reddit.close()  # Close the client session

    return posts