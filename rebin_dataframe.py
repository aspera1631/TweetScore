__author__ = 'bdeutsch'

import numpy as np
import pandas as pd
import MySQLdb


def sql_to_df(database, table):
    con = MySQLdb.connect(host='localhost', user='root', passwd='', db=database)

    df = pd.read_sql_query("select * from %s" % table, con, index_col=None, coerce_float=True, params=None, parse_dates=None, chunksize=None)

    return df

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
#tweets = pd.read_pickle('processed_20k_03')

#df = sql_to_df("TweetScore", "twitter")


## Rebins a dataframe according to some provided vectors.


# Tweet length
# 0-140, bins of 5
len_tot_binsize = 5
len_tot_bins = range(0,140 + len_tot_binsize, len_tot_binsize)

# Basic text length
# 0-140, bins of 5
len_bas_binsize = 5
len_bas_bins = range(0,140 + len_tot_binsize, len_tot_binsize)

# Number of hashtags
# [0,1,2,3,4,5,6+]
ht_binmax= 6
ht_bins = range(-1, ht_binmax)

# Number of user mentions
# [0,1,2,3,4,5,6+]
user_binmax= 6
user_bins = range(0, user_binmax + 1)

# Number of URLs
# [0,1,2+]
url_binmax= 2
url_bins = range(0, url_binmax + 1)

# Number of pictures
# [0,1,2+]
media_binmax= 2
media_bins = range(0, media_binmax + 1)

# Number of emoji
# [0,1,2,3,4,5,6+]
emo_binmax = 6
emo_bins = range(0, emo_binmax + 1)


## Make a new dataframe where the colums are the bin numbers.

#df_bins = pd.DataFrame()

#df_bins["ht_num"] = pd.cut(df["txt_len_total"], ht_bins, right=False, labels=["0","1","2","3","4"])



test = make_bins(140,5)

print test[0]
print test[1]
#test = pd.cut(np.array([0, 1, 2, 6.2, 9.7, 2.1]), [-.5,.5,1.5,2.5,100], labels=["0","1","2","3+"], retbins=True)
#print test