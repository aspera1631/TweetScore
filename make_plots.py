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

# Create bins and labels for a data set
def make_bins(max_lbl, step):
    range1 = np.arange(0, max_lbl + step, step)
    bins = np.append((range1 - step/2), 1000)
    labels = []
    for item in range1:
        labels.append(str(int(item)))
    labels.pop()
    labels.append(str(range1[-1]) + "+")
    labels_out = tuple(labels)
    return [bins, labels_out]

# Load data
df = pd.read_pickle('features_test')

#df = sql_to_df("TweetScore", "twitter")

## Plot retweets vs basic text length

# Take log of retweets
df["rt_log"] = df["retweets"].apply(lambda tweet: np.log10(tweet + 1))

df["fol_log"] = df["followers"].apply(lambda tweet: np.log10(tweet + 1))



# Bin the data by text length
df_bins_txt = df.groupby(pd.cut(df["txt_len_total"], bins=15, labels=False)).mean()

#df_bins_emo = df.groupby(pd.cut(df["emo_num"], bins=20, labels=False)).mean()

#df_emo_test = df.groupby(pd.cut(df["emo_num"], bins=20, labels=False))


'''
## Plot log(RTs) vs length of text
# Create bins and labels for follwoer counts
labels = range(0, max(df["txt_len_total"]), 5)
df["txt_tot_bins"] = pd.cut(df["txt_len_total"], range(0, max(df["txt_len_total"])+5, 5), right=False, labels=labels)

sns.set_context("talk", font_scale=1)
df.sort(columns="txt_tot_bins")
ax = sns.lmplot(x="txt_tot_bins", y="rt_log", data=df, x_estimator=np.mean, fit_reg=False)
ax.set(xlabel='Total tweet length', ylabel='log(Rewteets + 1)')
#ax.set_yscale('log')
plt.show()
'''

'''
bin_info = make_bins(140,5)
df["txt_tot_bins"] = pd.cut(df["txt_len_total"], bins=bin_info[0], labels=False)

sns.set_context("talk", font_scale=1)
df.sort(columns="txt_tot_bins")
ax = sns.lmplot(x="txt_tot_bins", y="rt_log", data=df, x_estimator=np.mean, fit_reg=False)
ax.set(xlabel='Total tweet length', ylabel='log(Rewteets + 1)')
#ax.set_yscale('log')
plt.show()
'''

'''
## Plot log(RTs) vs length of text
# Create bins and labels for follwoer counts
labels = range(0, max(df["txt_len_basic"]), 5)
df["txt_basic_bins"] = pd.cut(df["txt_len_basic"], range(0, max(df["txt_len_basic"])+5, 5), right=False, labels=labels)

sns.set_context("talk", font_scale=1)
df.sort(columns="txt_basic_bins")
ax = sns.lmplot(x="txt_basic_bins", y="rt_log", data=df, x_estimator=np.mean, fit_reg=False)
ax.set(xlabel='Simple text characters', ylabel='log(Rewteets + 1)')
#ax.set_yscale('log')
plt.show()
'''


'''
## Plot log(RTs) vs number of followers
# Create bins and labels for follwoer counts
labels = range(0, int(np.ceil(max(df["fol_log"]))), 1)
df["fol_bins"] = pd.cut(df["fol_log"], range(0, int(np.ceil(max(df["fol_log"])))+1, 1), right=False, labels=labels)

sns.set_context("talk", font_scale=1)
df.sort(columns="fol_bins")
ax = sns.lmplot(x="fol_bins", y="rt_log", data=df, x_estimator=np.mean, fit_reg=False)
ax.set(xlabel='log(Followers + 1)', ylabel='log(Rewteets + 1)')
#ax.set_yscale('log')
plt.show()
'''


'''
# log(RTs) vs basic length
sns.set_context("talk", font_scale=1)
ax = sns.pointplot(x=df_bins_txt.index, y=df_bins_txt["rt_log"], fit_reg=False)
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
# Plot log(RTs) vs number of hashtag
sns.set_context("talk", font_scale=1)
df.sort(columns="ht_num")
ax = sns.lmplot(x="ht_num", y="rt_log", data=df, x_estimator=np.mean, fit_reg=False)
ax.set(xlabel='Number of hashtags', ylabel='log(Rewteets + 1)')
#ax.set_yscale('log')
plt.show()
'''

'''
# Plot log(RTs) vs number of urls
sns.set_context("talk", font_scale=1)
df.sort(columns="url_num")
ax = sns.lmplot(x="url_num", y="rt_log", data=df, x_estimator=np.mean, fit_reg=False)
ax.set(xlabel='Number of URLs', ylabel='log(Rewteets + 1)')
#ax.set_yscale('log')
plt.show()
'''

'''
# Plot log(RTs) vs number of pictures
sns.set_context("talk", font_scale=1)
df.sort(columns="media_num")
ax = sns.lmplot(x="media_num", y="rt_log", data=df, x_estimator=np.mean, fit_reg=False)
ax.set(xlabel='Number of Pictures', ylabel='log(Rewteets + 1)')
#ax.set_yscale('log')
plt.show()
'''



'''
# Plot log(RTs) vs number of user mentions
sns.set_context("talk", font_scale=1)
df.sort(columns="user_num")
ax = sns.lmplot(x="user_num", y="rt_log", data=df, x_estimator=np.mean, fit_reg=False)
ax.set(xlabel='Number of user mentions', ylabel='log(Rewteets + 1)')
#ax.set_yscale('log')
plt.show()
'''


# Plot log(RTs) vs number of emoji
sns.set_context("talk", font_scale=1)
df.sort(columns="emo_num")
ax = sns.lmplot(x="emo_num", y="rt_log", data=df, x_estimator=np.mean, fit_reg=False)
ax.set(xlabel='Number of emoji', ylabel='log(Rewteets + 1)')
#ax.set_yscale('log')
plt.show()



#print tweets
#print df.head()

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
