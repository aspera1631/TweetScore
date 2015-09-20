__author__ = 'bdeutsch'
## do a polynomial fit on the data, calculate the goodness of tweet for each coordinate in tweetspace.
# next, find the gradient and make recommendations.
from sklearn.preprocessing import PolynomialFeatures
import numpy as np
import pandas as pd
import MySQLdb
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model

def sql_to_df(database, table):
    con = MySQLdb.connect(host='localhost', user='root', passwd='', db=database)

    df = pd.read_sql_query("select * from %s" % table, con, index_col=None, coerce_float=True, params=None, parse_dates=None, chunksize=None)

    return df


# Import data from SQL
df = sql_to_df('TweetScore', 'binned2')

test_num = 50000

# Code source: Jaques Grobler
# License: BSD 3 clause

# load targets
data_Y = df["retweets"][:-test_num].values
test_Y = df["retweets"][-test_num:].values

# Load features
data_X = df[["emo_num", "ht_num", "media_num", "txt_len_basic", "url_num", "user_num"]][:-test_num].values
test_X = df[["emo_num", "ht_num", "media_num", "txt_len_basic", "url_num", "user_num"]][-test_num:].values

# Turn the linear features into polynomial features
poly = PolynomialFeatures(4)
# Apply this transformation
X_new = poly.fit_transform(data_X)
X_new_test = poly.fit_transform(test_X)

# Create linear regression object
regr = linear_model.LinearRegression()

# Train the model using the training sets
regr.fit(X_new, data_Y)


# The coefficients
print('Coefficients: \n', regr.coef_)
# The mean square error
print("Residual sum of squares for training set: %.2f" % np.mean((regr.predict(X_new) - data_Y) ** 2))
print("Residual sum of squares for test set: %.2f" % np.mean((regr.predict(X_new_test) - test_Y) ** 2))
# Explained variance score: 1 is perfect prediction
print('Variance score for training set: %.2f' % regr.score(X_new, data_Y))
print('Variance score for test set: %.2f' % regr.score(X_new_test, test_Y))
# plots
#x_axis = np.array(range(max(data_X)+2))[:, np.newaxis]
#y_pred = regr.predict(poly.fit_transform(x_axis))
# Plot outputs
#plt.scatter(data_X, data_Y,  color='black')
#plt.plot(x_axis, y_pred, color='blue', linewidth=3)

#plt.xticks(())
#plt.yticks(())

#plt.show()



## use the regression result to create the goodness function

# load all possible tweets <= 140 characters
tweetspace = pd.read_pickle('legal_tweets_3')
print tweetspace


# calcuate the goodness column (-cost)
goodness = []

cols=["emo_num", "ht_num", "media_num", "txt_len_basic", "url_num", "user_num"]

#test = regr.predict(poly.fit_transform(tweetspace[cols].loc[1].values))

for ind in tweetspace.index:
    goodness.append(regr.predict(poly.fit_transform(tweetspace[cols].loc[ind].values))[0])
    if ind%1000 == 0:
        print ind

# put the results in the dataframe
tweetspace["goodness"] = goodness
#print tweetspace.tail()

cols2 = ["emo_num", "ht_num", "media_num", "txt_len_basic", "url_num", "user_num", "goodness"]


def make_index(row):
    #new_ind = ""
    new_ind = str(row.values[0:6])
    return new_ind

# convert each row to a vector and then a string. Use it as the index.
tweetspace['desig'] = tweetspace.apply(lambda row: make_index(row), axis=1)

ts = tweetspace.set_index("desig")

#print len(ts2.index.values)
ts.to_pickle("goodness_ord4")
# ADD IN RE_INDEX_GOODNESS.PY

