__author__ = 'bdeutsch'

import json
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns


# mostly from http://adilmoujahid.com/posts/2014/07/twitter-analytics/

def get_ent_len(entities):
    totlen = 0
    for item in entities:
        indices = item.get("indices",[0,0])
        len1 = indices[1] - indices[0]
        totlen = totlen + len1
    return totlen

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

#print len(tweets_data)

tweets = pd.DataFrame()

#tweets['text'] = map(lambda tweet: tweet['text'], tweets_data)
tweets['lang'] = map(lambda tweet: tweet['lang'], tweets_data)
#tweets['country'] = map(lambda tweet: tweet['place']['country'] if tweet['place'] != None else None, tweets_data)
#tweets['user_id'] = map(lambda tweet: tweet["user"]["id"], tweets_data)
tweets['followers'] = map(lambda tweet: tweet["user"]["followers_count"], tweets_data)
tweets['txt_len'] = map(lambda tweet: len(tweet["text"]), tweets_data)
tweets['retweets'] = map(lambda tweet: 1 + tweet.get("retweeted_status", {}).get("retweet_count", 0), tweets_data)
tweets['favorites'] = map(lambda tweet: 1 + tweet.get("retweeted_status", {}).get("favorite_count", 0), tweets_data)
tweets['ht_num'] = map(lambda tweet: len(tweet.get("entities", {}).get("hashtags", {})), tweets_data)
tweets['user_num'] = map(lambda tweet: len(tweet.get("entities", {}).get("user_mentions", {})), tweets_data)
tweets['url_num'] = map(lambda tweet: len(tweet.get("entities", {}).get("urls", {})), tweets_data)
tweets['media_num'] = map(lambda tweet: len(tweet.get("entities", {}).get("media", {})), tweets_data)
tweets['ext_ent_num'] = map(lambda tweet: len(tweet.get("entities", {}).get("extended_entities", {})), tweets_data)


# select only tweets with no hashtags, user mentions, or links
tweets_plain = tweets[(tweets["ht_num"] == 0) & (tweets["url_num"] == 0) & (tweets["media_num"] == 0)]
# plot retweets vs tweet length
sns.set_context("talk", font_scale=1)
plt.figure(figsize=(11, 8))
ax = sns.regplot(x="txt_len", y="retweets", data=tweets_plain, fit_reg=False)
ax.set(xlabel='Text length', ylabel='log(Retweets + 1)')
ax.set_yscale('log')



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

print tweets_plain
# create plot of retweets vs

#counts1 = tweets[["ht_num", "user_num"]]
#ax = sns.heatmap(counts1)


#show plot
sns.plt.show()