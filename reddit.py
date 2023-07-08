import os
import praw

reddit = praw.Reddit(
    client_id = os.environ['REDDIT_PERSONAL_USE_SCRIPT'],
    client_secret = os.environ['REDDIT_SECRET'],
    user_agent = 'TikTokGPT/0.0.1',
    username = os.environ['REDDIT_USERNAME'],
    password = os.environ['REDDIT_PASSWORD']
)

relevant_flairs = ['Not the A-hole', 'Everyone Sucks', 'Asshole']

path = "content/reddit/AITA/'{file_name}.txt'"

nbr_of_posts=100

for submission in reddit.subreddit('AmItheAsshole').top(time_filter='all', limit=nbr_of_posts):
    if submission.link_flair_text in relevant_flairs:
        if '/' not in submission.title:
            with open(path.format(file_name=submission.title), 'w+') as f:
                f.write(submission.selftext)

print('Done.')