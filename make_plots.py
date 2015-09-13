__author__ = 'bdeutsch'

import json
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
tweets = pd.read_pickle('processed_20k_01')

len_plot = tweets[['txt_len_basic', 'retweets']]

'''
# print retweets vs length
ax = sns.regplot(x="txt_len_basic", y="retweets", data=len_plot, fit_reg=False)
ax.set(xlabel='Text length', ylabel='retweets')
ax.set_yscale('log')
plt.show()
'''

sorted1 = tweets.sort('txt_len_basic', ascending=0)
print sorted1['text'][642174673116119040]



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