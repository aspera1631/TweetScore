__author__ = 'bdeutsch'

import json
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import MySQLdb


def sql_to_df(database, table):
    con = MySQLdb.connect(host='localhost', user='root', passwd='', db=database)

    df = pd.read_sql_query("select * from %s" % table, con, index_col=None, coerce_float=True, params=None, parse_dates=None, chunksize=None)

    return df

# Load data
#tweets = pd.read_pickle('processed_20k_03')

df = sql_to_df("TweetScore", "twitter")

## Plot retweets vs basic text length

# Take log of retweets
df["rt_log"] = df["retweets"].apply(lambda tweet: np.log10(tweet + 1))




# Bin the data by text length
df_bins_txt = df.groupby(pd.cut(df["txt_len_total"], bins=15, labels=False)).mean()

df_bins_fol = df.groupby(pd.cut(df["txt_len_total"], bins=10, labels=False)).mean()


'''
# log(RTs) vs basic length
sns.set_context("talk", font_scale=1)
ax = sns.pointplot(x=df_bins.index, y=df_bins["rt_log"], fit_reg=False)
ax.set(xlabel='Basic text length', ylabel='retweets')
##ax.set_yscale('log')
plt.show()
'''


'''
# log (RTs) vs total length
sns.set_context("talk", font_scale=1)
ax = sns.pointplot(x=df_bins.index, y=df_bins["rt_log"], fit_reg=False)
ax.set(xlabel='Basic text length', ylabel='retweets')
##ax.set_yscale('log')
plt.show()
'''

'''
# log (RTs) vs followers
sns.set_context("talk", font_scale=1)
ax = sns.pointplot(x=df_bins_fol["followers"], y=df_bins_fol["rt_log"], fit_reg=False)
ax.set(xlabel='Number of followers', ylabel='log(rewteets + 1)')
##ax.set_yscale('log')
plt.show()
'''




#print tweets
#print df

# create plot of retweets vs

#counts1 = tweets[["ht_num", "user_num"]]
#ax = sns.heatmap(counts1)




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
