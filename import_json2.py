__author__ = 'bdeutsch'

import json
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns


# mostly from http://adilmoujahid.com/posts/2014/07/twitter-analytics/
# Imports the tweets into a dataframe, only taking relevant columns. If it's a retweet, use the origninal text instead of retweeted text.



tweets_data_path = 'eng_20k.json'

tweets_data = []
tweets_file = open(tweets_data_path, "r")
count = 0
for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
        count += 1
    except:
        continue

def get_ent_len(entities):
    totlen = 0
    if len(entities) > 0:
        for item in entities:
            indices = item.get("indices", [0,0])
            len1 = indices[1] - indices[0]
            totlen = totlen + len1
    return totlen

def replace_amper(text):
    newtext = text.replace('&amp;','&')
    return newtext

#print len(tweets_data)

tweets = pd.DataFrame()

# Select and fill dataframe columns. If it's a retweet, use original tweet. If not, use regular values.

tweets['tw_id'] = map(lambda tweet: tweet.get("retweeted_status", tweet).get("id", {}), tweets_data)
tweets['text'] = map(lambda tweet: tweet.get("retweeted_status", tweet).get("text", {}), tweets_data)
# Replace '&and;' with '&'
tweets['text'] = tweets['text'].apply(replace_amper)

tweets['hashtags'] = map(lambda tweet: tweet.get("retweeted_status", tweet).get("entities",{}).get("hashtags", []), tweets_data)
tweets['users'] =  map(lambda tweet: tweet.get("retweeted_status", tweet).get("entities",{}).get("user_mentions", []), tweets_data)
tweets['urls'] = map(lambda tweet: tweet.get("retweeted_status", tweet).get("entities",{}).get("urls", []), tweets_data)
tweets['symbols'] = map(lambda tweet: tweet.get("retweeted_status", tweet).get("entities",{}).get("symbols", []), tweets_data)
tweets['media'] = map(lambda tweet: tweet.get("retweeted_status", tweet).get("entities",{}).get("media", []), tweets_data)
tweets['ext_ent'] = map(lambda tweet: tweet.get("retweeted_status", tweet).get("entities",{}).get("extended_entities", []), tweets_data)

#tweets['ht_num'] = tweets.hashtags.map(len)
tweets['ht_num'] = tweets['hashtags'].apply(len)
tweets['user_num'] = tweets['users'].apply(len)
tweets['url_num'] = tweets['urls'].apply(len)
tweets['sym_num'] = tweets['symbols'].apply(len)
tweets['media_num'] = tweets['media'].apply(len)
tweets['ext_num'] = tweets['ext_ent'].apply(len)

tweets['ht_len'] = tweets['hashtags'].apply(get_ent_len)
tweets['user_len'] = tweets['users'].apply(get_ent_len)
tweets['url_len'] = tweets['urls'].apply(get_ent_len)
tweets['sym_len'] = tweets['symbols'].apply(get_ent_len)
tweets['media_len'] = tweets['media'].apply(get_ent_len)
tweets['ext_len'] = tweets['ext_ent'].apply(get_ent_len)

tweets['txt_len_total'] = tweets['text'].apply(len)
tweets['txt_len_basic'] = tweets['txt_len_total'] - tweets[['ht_len','url_len','user_len','sym_len','media_len','ext_len']].sum(axis=1)



tweets['user_id'] = map(lambda tweet: tweet.get("retweeted_status", tweet).get("user", {}).get("id"), tweets_data)
tweets['followers'] = map(lambda tweet: tweet.get("retweeted_status", tweet).get("user", {}).get("followers_count"), tweets_data)

tweets['retweets'] = map(lambda tweet: tweet.get("retweeted_status", {}).get("retweet_count", 0), tweets_data)
tweets['favorites'] = map(lambda tweet: tweet.get("retweeted_status", {}).get("favorite_count", 0), tweets_data)

#tweets['lang'] = map(lambda tweet: tweet['lang'], tweets_data)
#tweets['country'] = map(lambda tweet: tweet['place']['country'] if tweet['place'] != None else None, tweets_data)


# Select only one version of each tweet, with the maximum retweets
tw_unique = tweets.groupby('tw_id').first()

#tw_unique[['sym_num']].apply(+1)

print tw_unique.head(40)

#save in pickle format
#tw_unique.to_pickle('processed_20k_01')

#tweets_comp = tw_unique[["retweets", "followers", "ht_num"]]

# Calculate the text length, not including entities
# Assume that each URL is 23 characters.



# Print pairplot
#ax = sns.pairplot(tweets_comp)
#ax.set(xlabel='Log(Followers + 1)', ylabel='Log(Rewteets + 1)', ylim=(1, 1000000), xlim=(1, 1000000))
#ax.set_xscale('log')
#ax.set_yscale('log')


#print tweets_comp.head()

# use this one if you want to see the retweeted text including "RT"
#tweets['text'] = map(lambda tweet: tweet.get("text", {}), tweets_data)

'''
# select only tweets with no hashtags, user mentions, or links
tweets_plain = tweets[(tweets["ht_num"] == 0) & (tweets["url_num"] == 0) & (tweets["media_num"] == 0)]
# plot retweets vs tweet length
sns.set_context("talk", font_scale=1)
plt.figure(figsize=(11, 8))
ax = sns.regplot(x="txt_len", y="retweets", data=tweets_plain, fit_reg=False)
ax.set(xlabel='Text length', ylabel='log(Retweets + 1)')
ax.set_yscale('log')
'''


#pd.options.display.max_rows = 200
#print tweets

# plot retweets vs tweet length
#sns.set_context("talk", font_scale=1)
#plt.figure(figsize=(11, 8))
#ax = sns.regplot(x="txt_len", y="retweets", data=tweets, fit_reg=False)
##ax = sns.lmplot(x="txt_len", y="retweets", data=tweets, x_estimator=np.mean, fit_reg=False);
#ax.set(xlabel='Text length', ylabel='log(Retweets + 1)', xlim=(0, 150), ylim=(1, 100000))
#ax.set_yscale('log')

# create plot of hashtags vs retweets
#sns.set_context("talk", font_scale=1)
#plt.figure(figsize=(11, 8))
#ax = sns.regplot(x="ht_num", y="retweets", data=tweets, fit_reg=False)
##ax = sns.lmplot(x="txt_len", y="retweets", data=tweets, x_estimator=np.mean, fit_reg=False);
#ax.set(xlabel='Number of hashtags', ylabel='log(Retweets + 1)', ylim=(1, 1000000), xlim=(-.5,11))
#ax.set_yscale('log')


# create plot of hashtags vs user mentions
#sns.set_context("talk", font_scale=1)
#plt.figure(figsize=(11, 8))
#ax = sns.regplot(x="ht_num", y="user_num", data=tweets, fit_reg=False)
#ax.set(xlabel='Number of hashtags', ylabel='Number of user mentions', ylim=(-.5, 12), xlim=(-.5, 11))

"""
# create plot of retweets vs favorites
sns.set_context("talk", font_scale=1)
plt.figure(figsize=(8, 8))
ax = sns.regplot(x="favorites", y="retweets", data=tweets, fit_reg=False)
ax.set(xlabel='Log(Favorites + 1)', ylabel='Log(Retweets + 1)')
ax.set_xscale('log')
ax.set_yscale('log')
"""

'''
# create plot of retweets vs number of followers
sns.set_context("talk", font_scale=1)
plt.figure(figsize=(8, 8))
ax = sns.regplot(x="followers", y="retweets", data=tweets, fit_reg=False)
ax.set(xlabel='Log(Followers + 1)', ylabel='Log(Rewteets + 1)', ylim=(1, 1000000), xlim=(1, 1000000))
ax.set_xscale('log')
ax.set_yscale('log')
'''

'''
# select only tweets in a certain follower number bin
df2 = tweets[(tweets["followers"] > 50000) & (tweets["followers"] <= 100000)]
print df2
# Make a histogram of rewteets for fixed number of followers
sns.set_context("talk", font_scale=1)
plt.figure(figsize=(8, 8))
ax = sns.distplot(np.log(df2[["retweets"]]), kde=False)
ax.set(xlabel="Log(Retweets + 1)", ylabel="Population")
'''

'''
# create plot of retweets vs number of followers
sns.set_context("talk", font_scale=1)
plt.figure(figsize=(8, 8))
ax = sns.regplot(x="followers", y="retweets", data=tweets, fit_reg=False)
ax.set(xlabel='Log(Followers + 1)', ylabel='Log(Rewteets + 1)', ylim=(1, 1000000), xlim=(1, 1000000))
ax.set_xscale('log')
ax.set_yscale('log')
'''

'''
# create plot of retweets vs number of followers
sns.set_context("talk", font_scale=1)
plt.figure(figsize=(8, 8))
ax = sns.pairplot(tweets)
#ax.set(xlabel='Log(Followers + 1)', ylabel='Log(Rewteets + 1)', ylim=(1, 1000000), xlim=(1, 1000000))
#ax.set_xscale('log')
#ax.set_yscale('log')
'''

#print tweets
#print df

# create plot of retweets vs

#counts1 = tweets[["ht_num", "user_num"]]
#ax = sns.heatmap(counts1)


#show plot
sns.plt.show()