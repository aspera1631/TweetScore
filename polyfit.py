__author__ = 'bdeutsch'

from sklearn.preprocessing import PolynomialFeatures
import numpy as np
import pandas as pd
import MySQLdb
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures


def sql_to_df(database, table):
    con = MySQLdb.connect(host='localhost', user='root', passwd='', db=database)

    df = pd.read_sql_query("select * from %s" % table, con, index_col=None, coerce_float=True, params=None, parse_dates=None, chunksize=None)

    return df

df = sql_to_df('TweetScore', 'binned')[0:10000]
df = df[df['ht_num'] > -1]
#print df.tail(5)


print(__doc__)


# Code source: Jaques Grobler
# License: BSD 3 clause

from sklearn import datasets, linear_model

# load targets
data_Y = df["rt_log"][0:100].values

# Use only one feature
data_X = df["txt_len_basic"][0:100].values[:, np.newaxis]


poly = PolynomialFeatures(2)
X_new = poly.fit_transform(data_X)

print X_new

#poly = PolynomialFeatures(interaction_only=True)
#poly.fit_transform(X)

# Create linear regression object
regr = linear_model.LinearRegression()

# Train the model using the training sets
#regr.fit(data_X_train, data_y_train)
regr.fit(X_new, data_Y)


# The coefficients
print('Coefficients: \n', regr.coef_)
# The mean square error
print("Residual sum of squares: %.2f"
      % np.mean((regr.predict(X_new) - data_Y) ** 2))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % regr.score(X_new, data_Y))


# Plot outputs
plt.scatter(data_X, data_Y,  color='black')
#plt.plot(range(28), regr.predict(data_X), color='blue',
         linewidth=3)

#plt.xticks(())
#plt.yticks(())

plt.show()

