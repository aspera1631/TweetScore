__author__ = 'bdeutsch'

import json
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import re

# partly from http://adilmoujahid.com/posts/2014/07/twitter-analytics/
# Imports the tweets into a dataframe, only taking relevant columns. If it's a retweet, use the origninal text instead of retweeted text.
# Use this to convert from Tweet json files to pickle files.

# Define path to raw tweet file
#tweets_data_path = 'eng_20k.json'
#tweets_data_path = "eng_20k.json"
tweets_data_path = "data_3.json"

# Load tweets as json into a nested dictionary
tweets_data = []
tweets_file = open(tweets_data_path, "r")
count = 0
for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
    except:
        continue
        count += 1

# Function to count the total length of all hashtags, etc
def get_ent_len(entities):
    totlen = 0
    if len(entities) > 0:
        for item in entities:
            indices = item.get("indices", [0,0])
            len1 = indices[1] - indices[0]
            totlen = totlen + len1
    return totlen

# Function to replace "&amp;" with "&"
def replace_codes(text):
    newtext = text.replace('&amp;','&').replace('&gt;','>').replace('&lt;','<')
    return newtext

def emoji_txt(text):
    m = re.findall('\\\U.{8}', text)
    #m = re.findall('', text.encode)
    if m:
        return len(m)
    else: return 0

def get_emo_len(number):
    return number*2

# Define an empty dataframe
tweets = pd.DataFrame()


# Select and fill dataframe columns. If it's a retweet, use original tweet. If not, use regular values.

# tweet ID. This will be the ID used in the dataframe
tweets['tw_id'] = map(lambda tweet: tweet.get("retweeted_status", tweet).get("id"), tweets_data)
# Tweet text
#tweets['text'] = map(lambda tweet: tweet.get("retweeted_status", tweet).get("text", {}).replace('\n', ''), tweets_data)
tweets['text'] = map(lambda tweet: tweet.get("retweeted_status", tweet).get("text", {}).replace('\n', ''), tweets_data)

# Replace '&and;' with '&' in the text
tweets['text'] = tweets['text'].apply(replace_codes)


# get lists of all info for all hashtags, urls, etc. If none, this is an empty set.
tweets['hashtags'] = map(lambda tweet:
                         tweet.get("retweeted_status", tweet).get("entities", {}).get("hashtags", []), tweets_data)
tweets['users'] =  map(lambda tweet:
                       tweet.get("retweeted_status", tweet).get("entities", {}).get("user_mentions", []), tweets_data)
tweets['urls'] = map(lambda tweet:
                     tweet.get("retweeted_status", tweet).get("entities", {}).get("urls", []), tweets_data)
tweets['symbols'] = map(lambda tweet:
                        tweet.get("retweeted_status", tweet).get("entities", {}).get("symbols", []), tweets_data)
tweets['media'] = map(lambda tweet:
                      tweet.get("retweeted_status", tweet).get("entities", {}).get("media", []), tweets_data)
tweets['ext_ent'] = map(lambda tweet:
                        tweet.get("retweeted_status", tweet).get("entities", {}).get("extended_entities", []), tweets_data)

# Count the hashtags, etc.
tweets['emo_num'] = map(lambda tweet: emoji_txt(str(tweet)), tweets_data)
tweets['ht_num'] = tweets['hashtags'].apply(len)
tweets['user_num'] = tweets['users'].apply(len)
tweets['url_num'] = tweets['urls'].apply(len)
tweets['sym_num'] = tweets['symbols'].apply(len)                            # stuff like Coke or Pepsi
tweets['media_num'] = tweets['media'].apply(len)                            # Twitter photos
tweets['ext_num'] = tweets['ext_ent'].apply(len)                            # Multi-photos or videos

# find the total length of all hashtags, etc.
tweets['emo_len'] = tweets['emo_num'].apply(get_emo_len)
tweets['ht_len'] = tweets['hashtags'].apply(get_ent_len)
tweets['user_len'] = tweets['users'].apply(get_ent_len)
tweets['url_len'] = tweets['urls'].apply(get_ent_len)
tweets['sym_len'] = tweets['symbols'].apply(get_ent_len)
tweets['media_len'] = tweets['media'].apply(get_ent_len)
tweets['ext_len'] = tweets['ext_ent'].apply(get_ent_len)

# Get the length of the text, and then subtract all of the entity lengths.
tweets['txt_len_total'] = tweets['text'].apply(len) - tweets['emo_num']  #accounts for double-counting of emoji chars
tweets['txt_len_basic'] = tweets['txt_len_total'] \
                          - tweets[['ht_len','url_len','user_len','sym_len','media_len','ext_len','emo_num']].sum(axis=1)
# This accounts for the fact that

# get the user ID and the number of followers of that user
tweets['user_id'] = map(lambda tweet: tweet.get("retweeted_status", tweet).get("user", {}).get("screen_name"), tweets_data)
tweets['followers'] = map(lambda tweet: tweet.get("retweeted_status", tweet).get("user", {}).get("followers_count"), tweets_data)

# get number of retweets and favories.
tweets['retweets'] = map(lambda tweet: tweet.get("retweeted_status", {}).get("retweet_count", 0), tweets_data)
tweets['favorites'] = map(lambda tweet: tweet.get("retweeted_status", {}).get("favorite_count", 0), tweets_data)


# Select only one version of each tweet, with the maximum retweets
tw_unique = tweets.groupby('tw_id').first()

# (optional) print some of the tweets
print tw_unique.head(20)

#features = tw_unique['tw_id']
features = tw_unique[["emo_num", "ht_num", "user_num", "url_num", "sym_num", "media_num", "ext_num", "txt_len_total", "txt_len_basic", "user_id", "followers", "retweets", "favorites"]]

#(optional) save in pickle format
features.to_pickle('features_03')


# Fields are:
# tw_id:        Unique tweet ID supplied by Twitter
# text:         Full text of the original tweet
# hashtags:     List of all hashtag entity data (no '#' symbol)
# users:        List of user mentions (no '@' symbol)
# urls          List of all url data
# symbols:      List of symbol data (like Coke or Pepsi symbols)
# media:        Twitter Picture entities
# ext_ent:      Extended entities, including multi-pictures and videos
# emo_num:      Number of emoji
# ht_num:       Number of hashtags
# user_num:     Number of user mentions in original tweet
# url_num:      Number of URLs in tweet
# sym_num:      Number of symbols
# media_num:    Number of media (twitter picture) elements
# ext_num:      Number of extended elements
# emo_len:      Length of emoji in parsed data (just 2x emo_num)
# ht_len:       Length of all hashtags
# user_len:     Length of all user mentions
# url_len:      Length of all URLs (22 or 23 char each)
# sym_len:      Length of all symbols
# media_len:    Length of all media elements
# ext_len:      Length of all extended entities
# txt_len_total Length of tweet
# txt_len_basic Length of simple text in tweet
# user_id:      Screen name of user for original tweet
# followers:    Number of followers of user
# retweets:     (max) Number of retweets for this tweet_id
# favorites:    (max) Number of favorites for this tweet_id

# Fields recorded in processed DataFrame:
# tw_id:        Unique tweet ID supplied by Twitter
# emo_num:      Number of emoji
# ht_num:       Number of hashtags
# user_num:     Number of user mentions in original tweet
# url_num:      Number of URLs in tweet
# sym_num:      Number of symbols
# media_num:    Number of media (twitter picture) elements
# ext_num:      Number of extended elements
# txt_len_total Length of tweet
# txt_len_basic Length of simple text in tweet
# user_id:      Screen name of user for original tweet
# followers:    Number of followers of user
# retweets:     (max) Number of retweets for this tweet_id
# favorites:    (max) Number of favorites for this tweet_id