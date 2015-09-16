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
df = df[df['txt_len_basic'] > -1]


print(__doc__)


# Code source: Jaques Grobler
# License: BSD 3 clause

from sklearn import datasets, linear_model
'''
# load targets
data_Y = df["rt_log"].values

# Use only one feature
data_X = df[["ht_num"]].values.tolist()

# Split the data into training/testing sets
data_X_train = data_X[:-20]
data_X_test = data_X[-20:]

# Split the targets into training/testing sets
data_y_train = data_Y[:-20]
data_y_test = data_Y[-20:]


X = np.arange(6).reshape(3, 2)

poly = PolynomialFeatures(2)
X_new = poly.fit_transform(data_X_train)
'''

print(__doc__)

import numpy as np
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn import cross_validation

np.random.seed(0)

n_samples = 30
degrees =  2

true_fun = lambda X: np.cos(1.5 * np.pi * X)
X = df["txt_len_basic"][0:1000].values
y = df["rt_log"][0:1000].values


plt.figure(figsize=(14, 5))

ax = plt.subplot(1, len(degrees), i + 1)
plt.setp(ax, xticks=(), yticks=())

polynomial_features = PolynomialFeatures(degree=degrees[i],
                                         include_bias=False)
linear_regression = LinearRegression()
pipeline = Pipeline([("polynomial_features", polynomial_features),
                     ("linear_regression", linear_regression)])
pipeline.fit(X[:, np.newaxis], y)

# Evaluate the models using crossvalidation
scores = cross_validation.cross_val_score(pipeline,
    X[:, np.newaxis], y, scoring="mean_squared_error", cv=10)

X_test = np.linspace(0, 1, 100)
plt.plot(X_test, pipeline.predict(X_test[:, np.newaxis]), label="Model")
#plt.plot(X_test, true_fun(X_test), label="True function")
plt.scatter(X, y, label="Samples")
plt.xlabel("x")
plt.ylabel("y")
plt.xlim((0, 1))
plt.ylim((-2, 2))
plt.legend(loc="best")
plt.title("Degree {}\nMSE = {:.2e}(+/- {:.2e})".format(
    degrees[i], -scores.mean(), scores.std()))
print('Coefficients: \n', pipeline.coef_)
plt.show()
