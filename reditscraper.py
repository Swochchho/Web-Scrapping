import praw
import pandas as pd

# create a Reddit instance with login credentials
reddit = praw.Reddit(user_agent=True, client_id='KXfugcLA-4EOHhfsdqpW',
                     client_secret='sV7zWjKbM5DGX4siD4rMKFpWIMKUbVzJ', username='machienist', password='jKaoiKerotelKo')

# create a list of subreddits to scrape
subreddit_list = ['worldnews', 'AskReddit', 'todayilearned']

# create empty lists to store scraped data
author_list = []
id_list = []
link_flair_text_list = []
num_comments_list = []
score_list = []
title_list = []
upvote_ratio_list = []

# loop through each subreddit in the list
for sub in subreddit_list:

    # select the subreddit
    subreddit = reddit.subreddit(sub)

    # scrape the "hot" posts, up to a limit of 150
    hot_post = subreddit.hot(limit=150)

    # loop through each post in the "hot" section
    for post in hot_post:
        try:
            # append the data from each post to the appropriate list
            author_list.append(post.author)
            id_list.append(post.id)
            link_flair_text_list.append(post.link_flair_text)
            num_comments_list.append(post.num_comments)
            score_list.append(post.score)
            title_list.append(post.title)
            upvote_ratio_list.append(post.upvote_ratio)
        except:
            # if an error occurs, skip the post and move on to the next one
            continue

    # print a message indicating that the subreddit has been scraped
    print(sub, 'completed; ', end='')
    print('total', len(author_list), 'posts has been scraped')

# create a pandas DataFrame from the lists
df = pd.DataFrame({'ID': id_list,
                   'Author': author_list,
                   'Title': title_list,
                   'Count_of_Comments': num_comments_list,
                   'Upvote_Count': score_list,
                   'Upvote_Ratio': upvote_ratio_list,
                   'Flair': link_flair_text_list
                   })

# write the DataFrame to a CSV file
df.to_csv('reddit_lists.csv', index=False)
