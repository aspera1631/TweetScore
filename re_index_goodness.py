__author__ = 'bdeutsch'

import numpy as np
import pandas as pd



ts = pd.read_pickle('goodness_2')


def make_index(row):
    #new_ind = ""
    new_ind = str(row.values[0:6])
    return new_ind

# convert each row to a vector and then a string. Use it as the index.
ts['desig'] = ts.apply(lambda row: make_index(row), axis=1)

ts2 = ts.set_index("desig")

#print len(ts2.index.values)
ts2.to_pickle("goodness_ind_2")
