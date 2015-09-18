__author__ = 'bdeutsch'

import numpy as np
import pandas as pd


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
'''

def get_txt_len(dfrow):
    # weights represent number of characters per bin of each type of data
    weight = pd.DataFrame([1, 2, 23, 5, 22, 2], index=["emo_num", "ht_num", "media_num", "txt_len_basic", "url_num", "user_num"])

    len1 = dfrow.dot(weight)
    return len1

# for each possible tweet, create a row of a dataframe
test = cartesian((emo_vals, ht_vals, media_vals, txt_bas_vals, url_vals, user_vals))
#test = [[141,0,0,0,0,0]]

# label the columns
tweetspace = pd.DataFrame(test, columns=["emo_num", "ht_num", "media_num", "txt_len_basic", "url_num", "user_num"])

tweetspace["len_tot"] = tweetspace.apply(get_txt_len, axis = 1)

legal_tweets = tweetspace[tweetspace["len_tot"] <= 140]

legal_tweets.to_pickle("legal_tweets_3")

