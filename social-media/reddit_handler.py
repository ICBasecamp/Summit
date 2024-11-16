import os
from dotenv import load_dotenv

import praw
import pandas as pd

load_dotenv()
reddit = praw.Reddit(
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'), 
    user_agent=os.getenv('USER_AGENT')        
)

def fetch_reddit(subreddit_name: str, stock: str):

    posts = []

    subreddit = reddit.subreddit(subreddit_name)

    if not subreddit:
        print(f"Subreddit {subreddit_name} not found")
        return None
      
    for post in subreddit.search(stock, sort='new', limit=25):
        posts.append({
            'Title': post.title,
            'Body': post.selftext,
            'Score': post.score,
            'Comments': post.num_comments,
            'Link': post.url
        })

    df = pd.DataFrame(posts)
    return df

# test
df = fetch_reddit('stocks', 'AAPL')
print(df)