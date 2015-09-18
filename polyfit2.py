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


feature = "ht_num"
row_num = 10

df = sql_to_df('TweetScore', 'binned')



# Code source: Jaques Grobler
# License: BSD 3 clause

# load targets
data_Y = df["rt_log"].values

# Use only one feature
#data_X = df[feature][0:10000].values[:, np.newaxis]
data_X = df[["emo_num", "ht_num", "media_num", "txt_len_basic", "url_num", "user_num"]].values
#data_X = df[["emo_num", "ht_num"]].values

# Turn the linear features into polynomial features
poly = PolynomialFeatures(3)
# Apply this transformation
X_new = poly.fit_transform(data_X)

# Create linear regression object
regr = linear_model.LinearRegression()

# Train the model using the training sets
regr.fit(X_new, data_Y)


# The coefficients
print('Coefficients: \n', regr.coef_)
# The mean square error
print("Residual sum of squares: %.2f" % np.mean((regr.predict(X_new) - data_Y) ** 2))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % regr.score(X_new, data_Y))

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
tweetspace = pd.read_pickle('legal_tweets')

# calcuate the goodness column (-cost)
goodness = []

cols=["emo_num", "ht_num", "media_num", "txt_len_basic", "url_num", "user_num"]

test = regr.predict(poly.fit_transform(tweetspace[cols].loc[1].values))

for ind in tweetspace.index:
    goodness.append(regr.predict(poly.fit_transform(tweetspace[cols].loc[ind].values))[0])
    if ind%1000 == 0:
        print ind

# put the results in the dataframe
tweetspace["goodness"] = goodness
#print tweetspace.tail()

cols2 = ["emo_num", "ht_num", "media_num", "txt_len_basic", "url_num", "user_num", "goodness"]
tweetspace[cols2].to_pickle("goodness_func")