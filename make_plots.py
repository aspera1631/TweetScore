__author__ = 'bdeutsch'

import json
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
tweets = pd.read_pickle('processed_20k_03')
#'processed_20k_03' is 20k tweets in english. Fields are:
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

len_plot = tweets[['txt_len_total', 'txt_len_basic', 'retweets']]

'''
# print retweets vs length
ax = sns.regplot(x="txt_len_total", y="retweets", data=len_plot, fit_reg=False)
ax.set(xlabel='Text length', ylabel='retweets')
ax.set_yscale('log')
plt.show()
'''



# print retweets vs length, pointplot
ax = sns.pointplot(x="txt_len_total", y="retweets", data=len_plot, ci=None)
ax.set(xlabel='Text length', ylabel='retweets')
ax.set_yscale('log')
plt.show()


#sorted1 = tweets.sort('txt_len_total', ascending=0)
#print sorted1['text']



# print retweets vs hashtags






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