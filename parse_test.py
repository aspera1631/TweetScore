__author__ = 'bdeutsch'

import numpy as np
import pandas as pd
import twitter_text as tt
from ttp import ttp


p = ttp.Parser()
result = p.parse("@burnettedmond, you now support #IvoWertzel's #testtag tweet parser! https://github.com/edburnett/")

'''
print "Reply: \n" + result.reply + "\n"

print "User mentions: "
for item in result.users:
    print item
print "\r"

print "Hashtags: "
for item in result.tags:
    print item
print "\r"

print "URLs: "
for item in result.urls:
    print item
print "\r"

print "HTML: \n" + result.html
'''

df = pd.DataFrame()
tweet = "@burnettedmond, you now support #IvoWertzel's #testtag tweet parser! http://github.com/edburnett/ https://github.com/edburnett/"


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

    # Get derived values
        # Note that urls will display as non-shortened versions, but should only count as 22/23 chars.
        # Need:
            # total length
            # ht_num
    df["ht_num"] = [len(result.tags)]
            # mention num
    df["user_num"] = [len(result.users)]
            # url num
    df["url_num"] = [len(result.urls)]
        # lengths

    df["https_num"] = [count_https(result.urls)]
    df["http_num"] = df["url_num"] - df["https_num"]



    df["ht_len"] = get_len(result.tags)
    df["user_len"] = get_len(result.users)

    df["txt_len_tot"] = [tweet_tt.validation.tweet_length()]
    df["txt_len_basic"] = df["txt_len_tot"] - df["user_len"] - df["ht_len"] - df["https_num"]*23 - df["http_num"]*22

    #df["txt_len_basic"] = df["txt_len_tot"] - df["ht_len"] - df["user_len"] -

    return df



df = tweet_features(df, tweet)
print df[["txt_len_tot", "txt_len_basic"]]
