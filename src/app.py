import os
from dotenv import load_dotenv
import tweepy
import pandas as pd
import requests 

# load the .env file variables
load_dotenv()

consumer_key = os.environ.get('CONSUMER_KEY')
consumer_secret = os.environ.get('CONSUMER_SECRET')
access_token = os.environ.get('ACCESS_TOKEN')
access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')
bearer_token = os.environ.get('BEARER_TOKEN')

# your app code here

# connection with API v2

client = tweepy.Client( bearer_token=bearer_token, 
                        consumer_key=consumer_key, 
                        consumer_secret=consumer_secret, 
                        access_token=access_token, 
                        access_token_secret=access_token_secret, 
                        return_type = requests.Response,
                        wait_on_rate_limit=True)
## search recent tweets

# Define query
query = '#100daysofcode (pandas OR python) -is:retweet'

# get max. 100 tweets
tweets = client.search_recent_tweets(query=query, 
                                    tweet_fields=['author_id','created_at'],
                                     max_results=100)


## convert to pandas dataframe

# Save data as dictionary
tweets_dict = tweets.json() 

# Extract "data" value from dictionary
tweets_data = tweets_dict['data'] 

# Transform to pandas Dataframe
tweets_df = pd.json_normalize(tweets_data)


# Add column with user name using author_id and client.get_user

user_name_ls=[]

for index, row in tweets_df.iterrows():
    user = client.get_user(id=row["author_id"])
    # Save data as dictionary
    user_dict = user.json()
    # get username
    user_name=user_dict['data']['username']
    user_name_ls.append(user_name)

tweets_df["user_name"]=user_name_ls

print(tweets_df.head())

print("Number of observations:", len(tweets_df))



## save df
tweets_df.to_csv("/workspace/interacting-with-the-twitter-api-project-tutorial/assets/coding-tweets.csv", index=None)