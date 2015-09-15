__author__ = 'bdeutsch'

import json
import MySQLdb
import numpy as np
import pandas as pd
import re
import twitter_text as tt
from ttp import ttp


# Function to replace "&amp;" with "&"
def replace_codes(text):
    newtext = text.replace('&amp;','&').replace('&gt;','>').replace('&lt;','<')
    return newtext

# Counts the number of emoji in a tweet
def emoji_txt(text):
    m = re.findall('(\\\U\w{8}|\\\u\w{4})', text)
    #m = re.findall('', text.encode)
    if m:
        return len(m)
    else: return 0

# Finds total length of emoji in a tweet
def get_emo_len(number):
    return number*2

# Function to count the total length of all hashtags, etc
def get_ent_len(entities):
    totlen = 0
    if len(entities) > 0:
        for item in entities:
            indices = item.get("indices", [0,0])
            len1 = indices[1] - indices[0]
            totlen = totlen + len1
    return totlen

def clean_tweets(filein, fileout):

    # Define path to raw tweet file
    tweets_data_path = filein

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
    tweets['hashtags'] = map(lambda tweet: tweet.get("retweeted_status", tweet).get("entities", {}).get("hashtags", []), tweets_data)
    tweets['users'] =  map(lambda tweet: tweet.get("retweeted_status", tweet).get("entities", {}).get("user_mentions", []), tweets_data)
    tweets['urls'] = map(lambda tweet: tweet.get("retweeted_status", tweet).get("entities", {}).get("urls", []), tweets_data)
    tweets['symbols'] = map(lambda tweet: tweet.get("retweeted_status", tweet).get("entities", {}).get("symbols", []), tweets_data)
    tweets['media'] = map(lambda tweet: tweet.get("retweeted_status", tweet).get("entities", {}).get("media", []), tweets_data)
    tweets['ext_ent'] = map(lambda tweet: tweet.get("retweeted_status", tweet).get("entities", {}).get("extended_entities", []), tweets_data)

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

    # get the user ID and the number of followers of that user
    tweets['user_id'] = map(lambda tweet: tweet.get("retweeted_status", tweet).get("user", {}).get("screen_name"), tweets_data)
    tweets['followers'] = map(lambda tweet: tweet.get("retweeted_status", tweet).get("user", {}).get("followers_count"), tweets_data)

    # get number of retweets and favories.
    tweets['retweets'] = map(lambda tweet: tweet.get("retweeted_status", {}).get("retweet_count", 0), tweets_data)
    tweets['favorites'] = map(lambda tweet: tweet.get("retweeted_status", {}).get("favorite_count", 0), tweets_data)

    # Select only one version of each tweet, with the maximum retweets
    tw_unique = tweets.groupby('tw_id').first()

    #features = tw_unique['tw_id']
    features = tw_unique[["emo_num", "ht_num", "user_num", "url_num", "sym_num", "media_num", "ext_num", "txt_len_total", "txt_len_basic", "user_id", "followers", "retweets", "favorites"]]

    #(optional) save in pickle format
    features.to_pickle(fileout)

    return True



def pickle_to_sql(filein):
    ## pickle_to_sql: open a file in pickle format, load into an SQL database.

    # open file and load into a dataframe
    tweets = pd.read_pickle(filein)

    # Connect to server
    con = MySQLdb.connect(host='localhost', user='root', passwd='', db='TweetScore')  # may need to add some other options to connect

    # Convert to to sql
    tweets.to_sql(con=con, name='twitter', if_exists='append', flavor='mysql')

    return True


def get_len(list):
    len1 = 0
    for item in list:
        len1 += len(item) + 1
    return len1

def count_https(list):
    count = 0
    for item in list:
        if item[:5] =='https':
            count += 1
    return count

def tweet_features(df, tweet):
    # run a tweet through the parser
    p = ttp.Parser()
    result = p.parse(tweet)

    # Use the twitter text py package to validate length
    tweet_tt = tt.TwitterText(tweet)

    df["ht_num"] = [len(result.tags)]                   # number of hashtags
    df["user_num"] = [len(result.users)]                # number of user mentions
    df["url_num"] = [len(result.urls)]                  # number of urls
    df["https_num"] = [count_https(result.urls)]        # Number of secure urls
    df["http_num"] = df["url_num"] - df["https_num"]    # number of other urls
    df["ht_len"] = get_len(result.tags)                 # total lentgh of all hashtags
    df["user_len"] = get_len(result.users)              # total length of all user mentions
    df["txt_len_tot"] = [tweet_tt.validation.tweet_length()]    # total length of tweet
    # length of basic text in tweet (no urls, hashtags, user mentions)
    df["txt_len_basic"] = df["txt_len_tot"] - df["user_len"] - df["ht_len"] - df["https_num"]*23 - df["http_num"]*22

    return df

def parse_input_tweet(tweet):
    df = pd.DataFrame()
    df = tweet_features(df, tweet)

    return df


def sql_to_df(database, table):
    con = MySQLdb.connect(host='localhost', user='root', passwd='', db=database)

    df = pd.read_sql_query("select * from %s" % table, con, index_col=None, coerce_float=True, params=None, parse_dates=None, chunksize=None)

    return df


#clean_tweets('data_7.json', 'features_07')

#pickle_to_sql('features_07')




#df = sql_to_df("TweetScore", "twitter")
#print df.head()



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