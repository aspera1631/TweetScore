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
data_Y = df["rt_log"][0:row_num].values

# Use only one feature
#data_X = df[feature][0:10000].values[:, np.newaxis]
data_X = df[["emo_num", "ht_num", "media_num", "txt_len_basic", "url_num", "user_num"]][0:row_num]

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

print regr.predict(X_new)



## use the regression result to create the goodness function


def cartesian(arrays, out=None):

    arrays = [np.asarray(x) for x in arrays]
    dtype = arrays[0].dtype

    n = np.prod([x.size for x in arrays])
    if out is None:
        out = np.zeros([n, len(arrays)], dtype=dtype)

    m = n / arrays[0].size
    out[:,0] = np.repeat(arrays[0], m)
    if arrays[1:]:
        cartesian(arrays[1:], out=out[0:m,1:])
        for j in xrange(1, arrays[0].size):
            out[j*m:(j+1)*m,1:] = out[0:m,1:]
    return out

'''
emo_vals = range(0,7)
ht_vals = range(0,7)
media_vals = range(0,3)
txt_bas_vals = range(0,29)
url_vals = range(0,3)
user_vals = range(0,7)
'''
# generate the space of all possible tweets
emo_vals = range(0,2)
ht_vals = range(0,2)
media_vals = range(0,2)
txt_bas_vals = range(0,2)
url_vals = range(0,2)
user_vals = range(0,2)

# for each possible tweet, craete a row of a dataframe
test = cartesian((emo_vals, ht_vals, media_vals, txt_bas_vals, url_vals, user_vals))
# label the columns
tweetspace = pd.DataFrame(test, columns=["emo_num", "ht_num", "media_num", "txt_len_basic", "url_num", "user_num"])

# calcuate the goodness column (-cost)
goodness = []
for ind in tweetspace.index:
    goodness.append(regr.predict(poly.fit_transform(tweetspace.loc[ind])))
# put the results in the dataframe
tweetspace["goodness"] = goodness
print tweetspace.tail()


## calculate a gradient
