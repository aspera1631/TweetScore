__author__ = 'bdeutsch'

import numpy as np
import pandas as pd
import MySQLdb

def import_data():
    database = "TweetScore"
    table = "twitter"
    con = MySQLdb.connect(host='localhost', user='root', passwd='', db=database)

    df = pd.read_sql_query("select * from %s" % table, con, index_col=None, coerce_float=True, params=None, parse_dates=None, chunksize=None)
    return df


def make_bins(max_lbl, step):
    range1 = np.arange(0, max_lbl + step, step)
    bins = np.append((range1 - float(step)/2), [1000])
    labels = []
    for item in range1:
        labels.append(str(int(item)))
    labels.pop()
    labels.append(str(range1[-1]) + "+")
    labels_out = tuple(labels)
    return [bins, labels_out]



def bin_data(df):
    ## Rebins a dataframe according to some provided vectors.


    # Tweet length
    # 0-140, bins of 5
    len_tot_max = 140
    len_tot_step = 5
    len_tot_bins = make_bins(len_tot_max, len_tot_step)[0]
    len_tot_labels = make_bins(len_tot_max, len_tot_step)[1]

    # Basic text length
    # 0-140, bins of 5
    len_bas_max = 140
    len_bas_step = 5
    len_bas_bins = make_bins(len_bas_max, len_bas_step)[0]
    len_bas_labels = make_bins(len_bas_max, len_bas_step)[1]

    # Number of hashtags
    # [0,1,2,3,4,5,6+]
    ht_max = 6
    ht_step = 1
    ht_bins = make_bins(ht_max, ht_step)[0]
    ht_labels = make_bins(ht_max, ht_step)[1]

    # Number of user mentions
    # [0,1,2,3,4,5,6+]
    user_max = 6
    user_step = 1
    user_bins = make_bins(user_max, user_step)[0]
    user_labels = make_bins(user_max, user_step)[1]

    # Number of URLs
    # [0,1,2+]
    url_max = 2
    url_step = 1
    url_bins = make_bins(url_max, url_step)[0]
    url_labels = make_bins(url_max, url_step)[1]

    # Number of pictures
    # [0,1,2+]
    media_max = 2
    media_step = 1
    media_bins = make_bins(media_max, media_step)[0]
    media_labels = make_bins(media_max, media_step)[1]

    # Number of emoji
    # [0,1,2,3,4,5,6+]
    emo_max = 6
    emo_step = 1
    emo_bins = make_bins(len_bas_max, emo_step)[0]
    emo_labels = make_bins(len_bas_max, emo_step)[1]



    ## Load data
    #df = sql_to_df("TweetScore", "twitter")


    ## Make a new datafram with binned data
    feat_bins = pd.DataFrame()

    feat_bins["txt_len_total"] = pd.cut(df["txt_len_total"], len_tot_bins, labels=False)
    feat_bins["txt_len_basic"] = pd.cut(df["txt_len_basic"], len_bas_bins, labels=False)
    feat_bins["ht_num"] = pd.cut(df["ht_num"], ht_bins, labels=False)
    feat_bins["user_num"] = pd.cut(df["user_num"], user_bins, labels=False)
    feat_bins["media_num"] = pd.cut(df["media_num"], media_bins, labels=False)
    feat_bins["emo_num"] = pd.cut(df["emo_num"], emo_bins, labels=False)
    feat_bins["url_num"] = pd.cut(df["url_num"], url_bins, labels=False)
    feat_bins["rt_log"] = df["retweets"].apply(lambda tweet: np.log10(tweet + 1))

    return feat_bins

# save to SQL
#con = MySQLdb.connect(host='localhost', user='root', passwd='', db='TweetScore')  # may need to add some other options to connect


def pickle_to_sql(filein, tableName, mode):
    ## pickle_to_sql: open a file in pickle format, load into an SQL database.
    # open file and load into a dataframe
    df = pd.read_pickle(filein)
    # Connect to server
    con = MySQLdb.connect(host='localhost', user='root', passwd='', db='TweetScore')  # may need to add some other options to connect
    # Convert to to sql
    df.to_sql(con=con, name=tableName, if_exists=mode, flavor='mysql')

    return True


#df = import_data()
#feat_bins = bin_data(df)
#con = MySQLdb.connect(host='localhost', user='root', passwd='', db='TweetScore')
#feat_bins[120001:].to_sql(con=con, name="binned", if_exists="append", flavor='mysql')