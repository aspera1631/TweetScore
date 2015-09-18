__author__ = 'bdeutsch'

import numpy as np
import pandas as pd



ts = pd.read_pickle('goodness_ind')

coord = pd.DataFrame()

cols = ["emo+", "ht+", "med+", "txt+", "url+", "usr+", "emo-", "ht-", "med-", "txt-", "url-", "usr-"]
gradient = pd.DataFrame(columns=cols, index=ts.index)


def make_index(coord):
    #new_ind = ""
    new_ind = str(coord)
    return new_ind


## Calculate partial derivates
# choose a row
count = 0
for ind in ts.index:
    count += 1
    #print ts.loc[ind].values
    coord = ts.loc[ind].values[0:6]
    goodness = ts.loc[ind].values[6]
    # addition loop
    gradient_row = []
    for feature in range(len(coord)):
        # take a step
        new_coord = coord
        new_coord[feature] += 1
        # convert the coordinate to an index
        new_ind = make_index(new_coord)

        # look up cost at these coordinates
        try:
            new_goodness = ts.loc[new_ind].values[6]
        except:
            new_goodness = np.nan
        # aggregate the gradient for this row. NaN should propagate
        gradient_row.append(new_goodness - goodness)


    # subtraction loop
    for feature in range(len(coord)):
        # take a step
        new_coord = coord
        new_coord[feature] -= 1
        # convert the coordinate to an index
        new_ind = make_index(new_coord)

        # look up cost at these coordinates
        try:
            new_goodness = ts.loc[new_ind].values[6]
        except:
            new_goodness = np.nan
        # aggregate the gradient for this row. NaN should propagate
        gradient_row.append(new_goodness - goodness)

    # add gradient row to the dataframe
    gradient.loc[ind] = gradient_row
    if count%1000 == 0:
        print count

#gradient.to_pickle("gradient_df")
