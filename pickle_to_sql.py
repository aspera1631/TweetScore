__author__ = 'bdeutsch'

## pickle_to_sql: open a file in pickle format, load into an SQL database.

import pandas as pd
import MySQLdb

# open file and load into a dataframe
tweets = pd.read_pickle('features_03')

# Connect to server
con = MySQLdb.connect(host='localhost', user='root', passwd='', db='TweetScore')  # may need to add some other options to connect

# Convert to to sql
tweets.to_sql(con=con, name='twitter', if_exists='append', flavor='mysql')

#print tweets.head()