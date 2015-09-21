__author__ = 'bdeutsch'

import numpy as np
import pandas as pd
import MySQLdb


def sql_to_df(database, table):
    con = MySQLdb.connect(host='localhost', user='root', passwd='', db=database)

    df = pd.read_sql_query("select * from %s" % table, con, index_col=None, coerce_float=True, params=None, parse_dates=None, chunksize=None)

    return df


def pickle_to_sql(filein, tableName, mode):
    ## pickle_to_sql: open a file in pickle format, load into an SQL database.

    # open file and load into a dataframe
    tweets = pd.read_pickle(filein)

    # Connect to server
    con = MySQLdb.connect(host='localhost', user='root', passwd='', db='TweetScore')  # may need to add some other options to connect

    # Convert to to sql
    tweets.to_sql(con=con, name=tableName, if_exists=mode, flavor='mysql')

    return True

# load binned data from sql
df = sql_to_df('tweetscore', 'binned')

# re-index
df = df.set_index("desig")

# group
df_group = df.groupby(level=0)

# new df
df2 = pd.DataFrame()
df2["emo_num"] = df_group["emo_num"].first()
df2["ht_num"] = df_group["ht_num"].first()
df2["media_num"] = df_group["media_num"].first()
df2["txt_len_basic"] = df_group["txt_len_basic"].first()
df2["url_num"] = df_group["url_num"].first()
df2["user_num"] = df_group["user_num"].first()
df2["rt_prob"] = df_group["rt"].mean()
df2["weights"] = df_group["rt"].count().apply(np.sqrt)


# write to pickle file
df2.to_pickle("probabilities")

pickle_to_sql("probabilities", "probabilities", "replace")