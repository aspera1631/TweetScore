__author__ = 'bdeutsch'

## Calculates and saves the gradient given a "goodness" matrix that measures the quality of every tweet in tweetspace

import numpy as np
import pandas as pd


# function that converts coordinates to index
def make_index(coord):
    #new_ind = ""
    new_ind = str(coord)
    return new_ind



# Load goodness dataframe
ts = pd.read_pickle('goodness_prob2')
# Create new dataframe of tweet coordinates
coord = pd.DataFrame()


# create new dataframe to hold the gradient
cols = ["emo+", "ht+", "med+", "txt+", "url+", "usr+", "emo-", "ht-", "med-", "txt-", "url-", "usr-"]
gradient = pd.DataFrame(columns=cols, index=ts.index)


## Calculate finite differences
count = 0

# choose a row
for ind in ts.index:
    count += 1
    # get current tweet coordinates
    coord = ts.loc[ind].values[0:6]
    # Find goodness at those coordinates
    goodness = ts.loc[ind].values[7]
    # addition loop
    gradient_row = []
    # For every possible "up" transition
    for feature in range(len(coord)):
        # take a step up
        new_coord = coord
        new_coord[feature] += 1
        # convert the new coordinate to an index
        new_ind = make_index(new_coord)
        # look up cost at these coordinates. If it's not there, return NaN.
        try:
            new_goodness = ts.loc[new_ind].values[7]
        except:
            new_goodness = np.nan
        # aggregate the gradient for this row. NaN should propagate
        gradient_row.append(new_goodness - goodness)

# Maybe I added a race condition? Maybe it tries to execute these in parallel?
    # subtraction loop
    # for every possible step down
    for feature in range(len(coord)):
        # take a step down
        new_coord = coord
        new_coord[feature] = new_coord[feature] - 2
        # convert the coordinate to an index
        new_ind = make_index(new_coord)
        # look up cost at these coordinates
        try:
            new_goodness = ts.loc[new_ind].values[7]
        except:
            new_goodness = np.nan
        # aggregate the gradient for this row. NaN should propagate
        #print new_goodness - goodness
        gradient_row.append(new_goodness - goodness)

    # add gradient row to the dataframe
    gradient.loc[ind] = gradient_row
    #print gradient
    if count%1000 == 0:
        print count

#print ts.loc["[  1.   2.   1.  10.   0.   6.]"][7]

# save dataframe as pickle file
gradient.to_pickle("gradient_prob")
